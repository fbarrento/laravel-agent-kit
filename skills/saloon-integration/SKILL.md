---
name: saloon-integration
description: Implement third-party HTTP API SDKs in the phpdevkits style with SaloonPHP. Covers the connector + resources + DTOs + requests layout, fixture-driven Pest testing with PII redaction, and the live-recording workflow. Use when building a new Saloon-based SDK (e.g. forge-sdk, a future stripe-sdk), adding a new resource to one, debugging a fixture-related test failure, or recovering from a spec-vs-runtime API surprise.
---

# Saloon Integration (phpdevkits style)

Use this skill when working inside a SaloonPHP-based SDK in this repo's
shape — single `Connector` extending Saloon's `Connector`, organized by
`Resources/` + `Requests/` + `Data/` + `Enums/` + `Exceptions/`, with
recorded Saloon fixtures driving Pest tests at 100% coverage.

For general Pest / factory conventions that aren't Saloon-specific (no
`it()`, factories under `tests/Factories/`, exception-test styles), see
the **pest-package-tests** skill — this skill assumes those and only
covers the Saloon side.

## Quick start

A minimal slice (one resource, one request, one DTO, one fixture-backed test):

```php
// src/Data/Widget.php
final readonly class Widget implements JsonSerializable {
    public function __construct(public string $id, public string $name) {}
    public static function from(array $data): self { /* hydration + validation */ }
    public function jsonSerialize(): array { /* snake_case */ }
}

// src/Requests/GetWidget.php
final class GetWidget extends Request {
    protected Method $method = Method::GET;
    public function __construct(private readonly int|string $id) {}
    #[Override] public function resolveEndpoint(): string {
        return sprintf('/widgets/%s', $this->id);
    }
}

// src/Resources/WidgetResource.php
final class WidgetResource extends BaseResource {
    public function get(): Widget {
        $data = $this->connector->send(new GetWidget($this->id))->json('data');
        return Widget::from($data);
    }
}

// tests/Unit/Resources/WidgetResourceTest.php
test('get() returns a hydrated Widget', function (): void {
    $mockClient = new MockClient([
        GetWidget::class => new WidgetFixture('widgets/get'),
    ]);
    $sdk = new MySdk('token')->withMockClient($mockClient);
    expect($sdk->widget(1)->get())->toBeInstanceOf(Widget::class);
});
```

The `WidgetFixture` is a project-local subclass of a base
`Tests\Utils\<SdkName>Fixture` that adds resource-specific redaction
rules — see [TESTING.md](rules/testing.md).

## Rule index

1. **Architecture** → [rules/architecture.md](rules/architecture.md) —
   namespace layout, connector responsibilities, exception hierarchy,
   org-context / nested-resource chains.
2. **Resources** → [rules/resources.md](rules/resources.md) — collection
   vs. item resources, `ParsesPage` for cursor pagination, `iterate()`
   helpers, action methods, write-DTO patterns.
3. **DTOs** → [rules/data.md](rules/data.md) — readonly output DTOs
   (`from()` / `jsonSerialize()`), input DTOs (`toArray()` stripping
   nulls), when to add enums.
4. **Requests** → [rules/requests.md](rules/requests.md) — `Request`
   class shape, `HasJsonBody` body trait, query params via
   `defaultQuery()`, common Saloon API gotchas.
5. **Testing & fixtures** → [rules/testing.md](rules/testing.md) —
   `ForgeFixture`-style PII redaction, no `MockResponse::make()`, no
   hand-crafted fixtures, lifecycle tests with try/finally cleanup.
6. **Recording workflow** → [rules/recording.md](rules/recording.md) —
   `.env` setup, Saloon auto-record default, poisoned-fixture recovery,
   cursor-walk recording.
7. **Pitfalls** → [rules/pitfalls.md](rules/pitfalls.md) — common
   spec-vs-runtime mismatches, Saloon traps (`#[Override]` on
   `defaultBody()`, MockClient class-vs-sequence mode, clone helpers
   dropping the mock), coverage attribution quirks.

## How to apply

1. Confirm you're in a SaloonPHP-based SDK matching the namespace
   layout in [rules/architecture.md](rules/architecture.md). If not, this
   skill doesn't apply — fall back to upstream Saloon docs.
2. Identify which slice you're building (a new resource? new endpoint
   on an existing resource?). Read the matching rule file before writing
   code.
3. For new resources, scaffold the DTO + factory first, then the request
   class, then the resource, then the test. Run the test once with no
   fixture to record from the live API.
4. Whenever Forge's actual response surprises you, append to
   `docs/FINDINGS.md` with the date — see [rules/pitfalls.md](rules/pitfalls.md)
   for the entry template.
