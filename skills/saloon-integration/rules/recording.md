# Recording workflow

How fixtures actually get on disk. Read this when (a) adding a new
endpoint, (b) the test suite says "fixture not found", or (c) a test
fails on an assertion that worked yesterday (it's almost always a
poisoned fixture).

## `.env` setup

Recording fires real API calls. CI must never have these vars set;
local `.env` must have them for the human running the recording.

```
FORGE_TOKEN=<your real OAuth or PAT>
FORGE_TEST_TOKEN=<usually same as above>
FORGE_TEST_ORG_SLUG=<your real org slug>
FORGE_TEST_SERVER_ID=<a real server id you own — needed for nested-resource tests>
```

Plus resource-specific ones as needed (e.g.
`FORGE_TEST_HETZNER_CREDENTIAL_ID`, `FORGE_TEST_HETZNER_REGION`,
`FORGE_TEST_HETZNER_SIZE`, `FORGE_TEST_HETZNER_NETWORK_ID` for the
Servers create lifecycle).

The test reads each env with a fallback so non-recording runs still
work:

```php
$token = ($_ENV['FORGE_TEST_TOKEN'] ?? '') ?: 'test-token';
```

## Run the test once to record

With `.env` populated and no existing fixture file for the test, just
run the test in isolation:

```bash
vendor/bin/pest tests/Unit/Resources/WidgetResourceTest.php --no-coverage
```

Saloon detects the fixture is missing, makes the real HTTP call,
applies the redactions defined on the fixture class, writes the JSON
file, and replays subsequent runs from disk.

Verify after recording:

```bash
# Did the file land where expected?
ls tests/Fixtures/Saloon/widgets/

# Is anything sensitive still in there?
grep -rE '(real-org-slug|192\.168|ssh-rsa|sudo_password)' tests/Fixtures/Saloon/widgets/
```

## Lifecycle tests (create / update / delete)

Write **one** end-to-end test per resource that exercises every write
operation in sequence, inside `try/finally` so cleanup happens even on
failure:

```php
test('lifecycle: create -> list -> get -> delete',
    /** @throws Throwable */
    function (): void {
        $token = ($_ENV['FORGE_TEST_TOKEN'] ?? '') ?: 'test-token';
        $org = ($_ENV['FORGE_TEST_ORG_SLUG'] ?? '') ?: 'test-org';
        $serverId = ($_ENV['FORGE_TEST_SERVER_ID'] ?? '') ?: '1';

        $mockClient = new MockClient([
            CreateSshKey::class => new ServerFixture('ssh-keys/create'),
            GetSshKeys::class => new ServerFixture('ssh-keys/list'),
            GetSshKey::class => new ServerFixture('ssh-keys/get'),
            DeleteSshKey::class => new ServerFixture('ssh-keys/delete'),
        ]);
        $forge = new Forge($token, $org)->withMockClient($mockClient);

        $createdId = null;
        try {
            $forge->server($serverId)->sshKeys()->create(/* ... */);

            // Recover the new id via list (when create returns 202/empty
            // body, the test can't capture the id from the response).
            $page = $forge->server($serverId)->sshKeys()->all();
            expect($page->data)->not->toBeEmpty();
            $createdId = $page->data[0]->id;

            $fetched = $forge->server($serverId)->sshKey($createdId)->get();
            expect($fetched)->toBeInstanceOf(SshKey::class);

            $forge->server($serverId)->sshKey($createdId)->delete();
            $createdId = null;
        } finally {
            if ($createdId !== null) {
                try {
                    $forge->server($serverId)->sshKey($createdId)->delete();
                } catch (Throwable) {
                    // best-effort; original failure surfaces
                }
            }
        }
    });
```

The lifecycle test records **all** the relevant fixtures (create, list,
get, delete) in one pass with one real resource — so list/get fixtures
contain real data instead of empty pages.

## When the same resource is reachable via different request classes

Use class-keyed `MockClient` mapping so Saloon picks the right fixture
per request type:

```php
new MockClient([
    CreateWidget::class => new WidgetFixture('widgets/create'),
    GetWidgets::class => new WidgetFixture('widgets/list'),
    GetWidget::class => new WidgetFixture('widgets/get'),
    DeleteWidget::class => new WidgetFixture('widgets/delete'),
]);
```

Use **sequential** mapping (just an array) when the same request class
is called multiple times in a row with different expected responses
(cursor walks):

```php
new MockClient([
    new ServerFixture('servers/list-page-1'),
    new ServerFixture('servers/list-page-2'),
]);
```

## Recover from a poisoned fixture

If a fixture got recorded with an error response (4xx/5xx — usually
because `.env` was wrong on the first attempt), the test now replays
the error forever. Wipe it and re-record:

```bash
rm tests/Fixtures/Saloon/widgets/create.json
vendor/bin/pest tests/Unit/Resources/WidgetResourceTest.php --no-coverage
```

Inspect any newly-recorded fixture for sensitive leaks before
committing:

```bash
python3 -c "import json; f = json.load(open('tests/Fixtures/Saloon/widgets/create.json')); print('status:', f['statusCode']); print('body:', f['data'][:1000])"
```

## When the API can't reproduce the case you want to test

You **can't** hand-craft a fixture JSON file. If the case is genuinely
unreachable from the real API (e.g. a malformed-response branch), the
cleanest answer is to remove the defensive branch from production code
and let PHP's type system handle the error — see [resources.md](resources.md).

For "empty page" tests, record a real call with a filter that matches
nothing (`filter[name]=__nonexistent__`). For "cursor walk" tests,
record with `page[size]=1` against a parent that has ≥2 children, and
break out of iteration after the second yield (see
[testing.md](testing.md)).
