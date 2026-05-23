# Pitfalls

Real things that have caught us at least once. Read before recording
fixtures or extending the test bed; cross-reference `docs/FINDINGS.md`
for project-specific runtime quirks.

## Saloon API traps

### `#[Override]` on `defaultBody()` is a fatal error

```php
final class CreateWidget extends Request implements HasBody
{
    use HasJsonBody;

    #[Override]                            // <-- WRONG. Fatal at class load.
    protected function defaultBody(): array { /* ... */ }
}
```

`HasJsonBody` is a trait. The trait calls `defaultBody()` if the
subclass defines it, but doesn't declare it as an abstract method on
any parent class — so PHP's `#[Override]` validator sees no method to
override. Remove the attribute.

`#[Override]` IS correct on `resolveEndpoint()` and `defaultQuery()`
(both declared on `Saloon\Http\Request`).

### The org-context clone drops the MockClient

```php
public function org(string $slug): self
{
    return new self($this->token, $slug);  // <-- WRONG. Test escapes the mock.
}
```

Saloon's `MockClient` is attached to a specific connector instance via
`->withMockClient()`. A fresh `new self(...)` doesn't inherit it, so
the cloned connector makes a real HTTP call.

```php
public function org(string $slug): self
{
    $clone = new self($this->token, $slug);
    if (($mock = $this->getMockClient()) instanceof MockClient) {
        $clone->withMockClient($mock);
    }
    return $clone;
}
```

### `MockClient` class-mode vs sequence-mode

- **Class-mode** (`[GetWidget::class => $fixture]`): every call to that
  request class returns the same fixture. Use for happy-path tests
  where the URL varies but the recorded response is reusable.
- **Sequence-mode** (`[$fixture1, $fixture2]`): consumed in order
  regardless of request class. Use for cursor walks where each call
  needs a different response.

Mixing the two in one `MockClient` is undefined — pick one mode per
test.

### `MockClient` auto-records failure responses too

If the first run hits a 4xx, Saloon writes that 4xx body to the
fixture file. Future runs replay the failure. Always inspect a
freshly-recorded fixture's `statusCode` field before committing, and
wipe + re-record on any non-2xx.

## Coverage attribution quirks

### `match (true)` envelope lines are uncovered

The PCOV / xdebug coverage formats don't attribute hits to the `match`
expression line itself, only to the arm expressions. Under a 100%
coverage gate, this produces a false-negative gap on a fully-tested
mapper. Use an if-chain instead:

```php
// BAD (gate fails on the `match` line)
return match (true) {
    $status === 400 => new BadRequestException($response),
    $status === 401 => new UnauthorizedException($response),
    default => new ApiException($response),
};

// GOOD
if ($status === 400) return new BadRequestException($response);
if ($status === 401) return new UnauthorizedException($response);
return new ApiException($response);
```

### `foreach ($items as $item) { yield $item; }` is uncovered

The `yield $item` line doesn't get hit-counted reliably. Use
`yield from $items;`:

```php
// BAD
foreach ($page as $item) {
    yield $item;
}

// GOOD
yield from $page;
```

### `XDEBUG_MODE=coverage` for any script that loads `.env`

Herd's default `XDEBUG_MODE=develop` dumps function arguments on every
notice/deprecation, which leaks env vars (including `FORGE_TEST_TOKEN`)
through vlucas/phpdotenv's `parse()` traceback. Set
`XDEBUG_MODE=coverage` in `composer.json`'s `test:unit` script:

```json
"test:unit": [
    "@putenv XDEBUG_MODE=coverage",
    "pest --parallel --coverage --exactly=100"
]
```

## Redaction interferes with assertions

`<Sdk>Fixture::defineSensitiveJsonParameters()` runs leaf-key
replacement across the response body — including fields the test wants
to assert on.

Example: `name` redacted to `'Test User'` everywhere broke a "find the
key by name" lookup in the SSH-keys lifecycle test. Workarounds:

1. **Don't assert on redacted fields.** Take `$page->data[0]` instead
   of `array_filter($page->data, fn ($k) => $k->name === 'sdk-test-key')`.
   Guarantee the test environment has only one matching record (lifecycle
   tests do — they create their own).
2. **Move the redaction to a subclass** so the base only redacts
   what's universally sensitive. If `name` matters in the SSH-key
   domain but is PII in the org domain, override
   `defineSensitiveJsonParameters()` in the SSH-key subclass to
   re-expose it.

## Spec-vs-runtime divergence

Forge's OpenAPI spec is not load-bearing. Record what the API actually
returns, accommodate the surprise, document it.

When you find a new divergence, append to `docs/FINDINGS.md`:

```md
## YYYY-MM-DD — Short headline of the surprise

**Spec:** What `docs/forge.openapi.json` says.

**Runtime:** What the API actually does.

**SDK impact:** What in `src/` accommodates it (DTO nullability,
resource-method return type, etc.) — and any env-var requirement
recording-mode needs.
```

Common kinds we've already hit:

- **Field nullability**: spec says required-non-null, runtime returns
  null (e.g. `revoked`, `connection_status` on freshly-created servers).
  → DTO field is `?T`, hydration uses `optionalX()` helper.
- **Hidden required fields**: spec marks a field optional, runtime
  rejects payloads missing it (e.g. Hetzner `network_id`). → Document
  in FINDINGS plus the new `FORGE_TEST_*` env var.
- **Format quirks**: spec says `"type": "string"`, runtime requires a
  specific format (e.g. Hetzner `size_id` accepts only the size *code*,
  not the numeric Forge id). → Document in FINDINGS; the DTO field
  stays a plain string.
- **Async empty bodies**: spec says POST returns a resource, runtime
  returns 202 with empty body (e.g. POST `/ssh-keys`). → Resource
  method returns `void`; caller lists afterwards.
- **Sensitive data leaks not in spec**: e.g. `meta.sudo_password` on
  create-server response. → Add to the domain `<X>Fixture` redactions
  immediately, wipe + re-record any fixtures that captured the secret.

## Skeleton-php Pint + Rector concat conflict

Two formatters disagree on space-around-concat. Resolution: **no space
on either side of `.`**. Both linters tolerate that.

```php
// BAD — Pint or Rector will rewrite, then the other will rewrite back
$message = 'prefix ' . $value . ' suffix';

// GOOD
$message = 'prefix '.$value.' suffix';
```
