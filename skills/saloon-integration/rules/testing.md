# Testing & fixtures

This file covers Saloon-specific testing concerns. For Pest conventions
that aren't Saloon-related (no `it()`, factories, exception-test styles,
splitting test files past ~15 tests), see the **pest-package-tests**
skill.

## Two hard rules

1. **All HTTP-touching tests go through a `<Sdk>Fixture` class.** No
   `MockResponse::make([...])` calls anywhere in test bodies. Use a base
   `Tests\Utils\<Sdk>Fixture` (extends `Saloon\Http\Faking\Fixture`)
   that applies the SDK's standard redactions, plus per-domain
   subclasses for domain-specific redactions.
2. **Fixtures are recorded from the live API, never hand-crafted.** Saloon
   auto-records on first run; the JSON file you commit was produced by
   a real `recordResponse()` call with redactions applied. If a test
   needs a synthetic edge case (empty page, broken response) that can't
   be reproduced against the real API, **drop or restructure the test**
   instead of writing fake fixture JSON.

These constraints rule out some patterns that other Saloon codebases
use freely. They exist because (a) fixtures double as schema-drift
canaries, (b) redaction only runs at record time, (c) hand-crafted
fixtures rot silently.

## `tests/Pest.php` setup

```php
use Dotenv\Dotenv;
use Saloon\MockConfig;

foreach (['.env', '.env.testing'] as $envFile) {
    if (file_exists(dirname(__DIR__).'/'.$envFile)) {
        Dotenv::createImmutable(dirname(__DIR__), $envFile)->safeLoad();
    }
}

MockConfig::setFixturePath('tests/Fixtures/Saloon');
// Saloon's native auto-record-on-miss default is left in place.
```

Do **not** call `MockConfig::throwOnMissingFixtures()`. Recording is the
default; CI just replays whatever's committed.

## `<Sdk>Fixture` base class

Lives at `tests/Utils/<Sdk>Fixture.php`. **Must not be `final`** so
domain subclasses can extend it.

```php
class ForgeFixture extends Fixture
{
    #[Override]
    protected function defineSensitiveHeaders(): array
    {
        return [
            'set-cookie' => 'REDACTED',
            'cf-ray' => 'REDACTED',
            'date' => 'REDACTED',
            'server' => 'REDACTED',
            'x-ratelimit-remaining' => 'REDACTED',
            'x-ratelimit-limit' => 'REDACTED',
        ];
    }

    #[Override]
    protected function defineSensitiveJsonParameters(): array
    {
        return [
            'id' => '1',
            'name' => 'Test User',
            'email' => 'test@example.com',
            'created_at' => '2024-01-01T00:00:00.000000Z',
            'updated_at' => '2024-01-01T00:00:00.000000Z',
            'slug' => $this->sequentialPlaceholder('test-org-'),
        ];
    }

    #[Override]
    protected function defineSensitiveRegexPatterns(): array
    {
        $mapper = $this->sequentialPlaceholder('test-org-');
        return [
            // org slugs leak through `links.self.href` URLs — match raw OR
            // JSON-escaped slashes.
            '#\\\\?/orgs\\\\?/[a-z0-9_-]+#i' => static function (string $match) use ($mapper): string {
                $pos = strrpos($match, '/');
                return substr($match, 0, $pos + 1) . $mapper(substr($match, $pos + 1));
            },
        ];
    }

    private function sequentialPlaceholder(string $prefix): callable
    {
        $map = [];
        return static function (mixed $value) use ($prefix, &$map): string {
            if (! is_string($value)) return $prefix.'unknown';
            if (! isset($map[$value])) $map[$value] = $prefix.(count($map) + 1);
            return $map[$value];
        };
    }
}
```

## Domain subclasses

When a domain has its own sensitive fields (IPs, SSH keys, generated
passwords, opaque pagination cursors), add a subclass that extends the
base and merges in the new rules.

```php
final class ServerFixture extends ForgeFixture
{
    #[Override]
    protected function defineSensitiveJsonParameters(): array
    {
        $stableCursor = static fn (mixed $v): ?string => $v === null ? null : 'CURSOR-A';

        return [
            ...parent::defineSensitiveJsonParameters(),
            'ip_address' => '203.0.113.1',        // TEST-NET-3 RFC 5737
            'private_ip_address' => '10.0.0.1',   // RFC 1918
            'timezone' => 'UTC',
            'local_public_key' => 'REDACTED',
            'sudo_password' => 'REDACTED',
            'next_cursor' => $stableCursor,
            'prev_cursor' => $stableCursor,
        ];
    }

    #[Override]
    protected function defineSensitiveRegexPatterns(): array
    {
        return [
            ...parent::defineSensitiveRegexPatterns(),
            '#\\\\?/servers\\\\?/\d+#' => '/servers/1',  // numeric ids in URLs
        ];
    }
}
```

Use a **callable redactor that preserves null** for fields where null
is semantically meaningful (e.g. `next_cursor: null` means "no more
pages" — the iterator must terminate). A plain string replacement turns
null into the placeholder and breaks pagination on replay.

Use RFC-reserved IP ranges (`203.0.113.0/24`, `10.0.0.0/8`) for IP
redactions so the fixture is obviously test data.

## Resource test shape

```php
test('all() returns a Page<Widget>',
    /** @throws Throwable */
    function (): void {
        $token = ($_ENV['FORGE_TEST_TOKEN'] ?? '') ?: 'test-token';
        $org = ($_ENV['FORGE_TEST_ORG_SLUG'] ?? '') ?: 'test-org';
        $mockClient = new MockClient([
            GetWidgets::class => new WidgetFixture('widgets/list'),
        ]);
        $forge = new Forge($token, $org)->withMockClient($mockClient);

        $page = $forge->widgets()->all();

        expect($page)->toBeInstanceOf(Page::class)
            ->and($page->data)->not->toBeEmpty()
            ->and($page->data[0])->toBeInstanceOf(Widget::class);
    });
```

The `($_ENV[...] ?? '') ?: 'fallback'` pattern: live credentials when
present (recording mode); harmless placeholders otherwise (CI replay).

## Request URL tests (no fixture needed)

Pure unit tests on `resolveEndpoint()` don't need a fixture, a mock
client, or any connector. They're fast, deterministic, and self-contained.

```php
test('resolveEndpoint() interpolates the org slug and id',
    function (): void {
        expect(new GetWidget('acme', 42)->resolveEndpoint())->toBe('/orgs/acme/widgets/42');
    });

test('uses the POST method',
    function (): void {
        expect(new CreateWidget('acme', $data)->getMethod())->toBe(Method::POST);
    });

test('body() reflects the input DTO',
    function (): void {
        expect(new CreateWidget('acme', $data)->body()->all())->toBe([...]);
    });
```

## Cursor-walk tests

Use **sequential** `MockClient` (no class-keyed mapping) so the second
call gets a different fixture. Force termination with a `break` so the
loop doesn't fire a non-existent third page.

```php
$mockClient = new MockClient([
    new ServerFixture('servers/list-page-1'),
    new ServerFixture('servers/list-page-2'),
]);
$forge = new Forge($token, $org)->withMockClient($mockClient);

$consumed = 0;
foreach ($forge->servers()->iterate(new ListServersOptions(size: 1)) as $server) {
    if (++$consumed === 2) break;     // page-2's next_cursor is non-null after
                                       // redaction; the break prevents call #3
}

$query = $mockClient->getLastPendingRequest()?->query()->all() ?? [];
expect($query['page[cursor]'])->toBe('CURSOR-A');
```

If `next_cursor` is redacted to a stable placeholder (`CURSOR-A`) and
`prev_cursor` similarly, the test can assert exact cursor values across
recordings.

## Defensive-branch tests

Don't write resource code that branches on `if (! is_array($data))`
unless you can record both branches. The "trust the API" pattern (see
[resources.md](resources.md)) keeps coverage at 100% without inventing
synthetic fixtures.
