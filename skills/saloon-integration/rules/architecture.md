# Architecture

## Namespace layout

```
src/
├── <SdkName>.php                 # the Connector (single class, root namespace)
├── Data/                         # readonly DTOs (output + input + list-options)
├── Enums/                        # ONLY for spec-enumerated closed sets
├── Exceptions/                   # base + per-HTTP-status subclasses
├── Requests/<Domain>/            # one Saloon Request class per endpoint
└── Resources/                    # BaseResource subclasses
    └── Concerns/ParsesPage.php   # shared cursor-pagination trait
```

Tests mirror `src/`:

```
tests/
├── Factories/                    # fbarrento/data-factory per Data class
├── Fixtures/Saloon/<domain>/     # recorded JSON, gitignored from PII
├── Unit/Data/                    # DTO tests
├── Unit/Enums/                   # enum sanity tests
├── Unit/Exceptions/              # exception class tests
├── Unit/Requests/<Domain>/       # endpoint URL/method/body composition
├── Unit/Resources/               # resource happy paths via fixtures
└── Utils/                        # ForgeFixture-style redaction subclasses
```

Once `tests/Unit/<SdkName>Test.php` passes ~15 tests, split it per-method:
`tests/Unit/<SdkName>/<Method>Test.php` (Constructor, FromEnvironment,
FromConfig, Accessors, etc.).

## The Connector

Single class at the root namespace, `final class <SdkName> extends Connector`.
Responsibilities:

- Token authentication (`defaultAuth(): TokenAuthenticator`)
- Default headers (`defaultHeaders(): array`)
- Base URL (`resolveBaseUrl(): string`)
- HTTP-status → exception mapping (`getRequestException(): Throwable`)
- Wrap `Saloon\Exceptions\Request\FatalRequestException` →
  `ConnectionException` so callers catch one exception family
- `use AlwaysThrowOnErrors` trait — every non-2xx becomes an exception
- Resource accessors: `me()`, `organizations()`, `organization($slug)`,
  `providers()`, `provider($id)`, etc.
- Optional credential factories: `static fromEnvironment()`,
  `static fromConfig(?string $path = null)` — read token + default org
  from env / JSON file

The connector exposes resource collections (plural method) and individual
resources (singular method taking an id). Example:

```php
public function servers(): ServersResource { return new ServersResource($this, $this->requireOrganization('servers')); }
public function server(int|string $id): ServerResource { return new ServerResource($this, $this->requireOrganization('server'), $id); }
```

`int|string` for ids: the upstream API may accept either; let callers pass
what they have.

## Exception hierarchy

```
RuntimeException                          (PHP stdlib)
└── <Sdk>Exception                        (abstract base)
    ├── ConnectionException               (network-layer fatal)
    ├── ApiException                      (any non-2xx — has Response)
    │   ├── BadRequestException           (400)
    │   ├── UnauthorizedException         (401)
    │   ├── ForbiddenException            (403)
    │   ├── NotFoundException             (404)
    │   ├── ValidationException           (422 — exposes ->errors())
    │   ├── RateLimitException            (429)
    │   └── ServerException               (5xx)
    └── OrganizationNotSetException       (client-side guard, not HTTP)
```

`getRequestException()` on the connector maps HTTP status → typed
exception. Prefer an `if`-chain over `match (true)` — the coverage tool
attributes hits to each branch consistently with `if`, but skips the
`match (true)` envelope line.

## Nested resources

Use the chain: `$sdk->server($id)->sshKeys()->all()`.

- `ServerResource` (item) exposes `sshKeys(): SshKeysResource` and
  `sshKey($id): SshKeyResource`.
- Nested resource constructors receive the parent's identifying state
  (org slug, server id) so request classes have what they need to
  resolve the URL.

```php
public function sshKeys(): SshKeysResource {
    return new SshKeysResource($this->connector, $this->organization, $this->id);
}
```

Request file naming stays flat: `src/Requests/Servers/CreateSshKey.php`
(not `src/Requests/Servers/SshKeys/Create.php`). The class name encodes
the operation; the parent folder encodes the domain.

## Org-context (hybrid model)

For SDKs whose URL paths are scoped by org slug:

- Constructor takes `?string $defaultOrganization = null`.
- `org(string $slug): self` returns an **immutable clone** bound to the
  new slug. **The clone must carry over `$this->getMockClient()`** —
  forgetting this is a real bug we hit (test chains escape the mock and
  hit the real API).
- Org-scoped accessors call `$this->requireOrganization('accessor-name')`
  which throws `OrganizationNotSetException` (extends base exception,
  NOT `ApiException`) if no org is bound.
- Non-org accessors (`me()`, `providers()`, etc.) stay reachable
  regardless of org state.

```php
public function org(string $slug): self {
    $clone = new self($this->token, $slug);
    if (($mock = $this->getMockClient()) instanceof MockClient) {
        $clone->withMockClient($mock);
    }
    return $clone;
}
```
