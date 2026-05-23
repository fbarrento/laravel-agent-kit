# Contracts & translation

The port and its implementations. All three live flat in `app/Contracts/`,
named `<Name>Service` (interface), `<Provider><Name>Service` and
`InMemory<Name>Service` (impls).

## The port

Domain vocabulary only. Declares the nullable return shape **and** the
domain exceptions it can throw (the contract both impls must honor).

```php
interface SymbolQuoteService
{
    /** @throws IntegrationUnavailable when the provider is down/rate-limited. */
    public function quote(Symbol $symbol): ?SymbolQuote; // null = no quote
}
```

## The Saloon-backed impl (adapter-impl)

The only class that imports both vendor DTOs and domain Data. Three
jobs: orchestrate the request, translate vendor → domain, translate
failures.

```php
final class FinnHubSymbolQuoteService implements SymbolQuoteService
{
    public function __construct(private FinnHubConnectorFactory $factory) {}

    public function quote(Symbol $symbol): ?SymbolQuote
    {
        try {
            $dto = $this->factory->for($this->integration)
                ->quotes()->get($symbol->value);          // returns a vendor DTO
        } catch (NotFoundException) {
            return null;                                    // expected absence
        } catch (ApiException | ConnectionException $e) {
            throw IntegrationUnavailable::from($e);         // genuine failure
        }

        return $this->toDomain($dto);                       // translation
    }

    private function toDomain(FinnHubQuote $dto): SymbolQuote { /* … */ }
}
```

## Translation — private methods first, Mapper when earned

Default: translate in **private methods on the Service** — that is the
Service's job. Extract a dedicated `<Provider><Name>Mapper` class only
when translation (a) has real logic worth isolating (computed fields,
multi-resource composition, unit/currency conversion), (b) is reused
across several methods, or (c) deserves its own unit test. The heuristic
matches the Service-tier test rule in [testing.md](testing.md): *if it's
worth a Mapper, it's worth a Service-tier test.*

**Anti-pattern (rejected):** a named constructor on the domain object
(`SymbolQuote::fromFinnHub(...)`). That makes domain import the adapter,
inverting the dependency. The domain must never know a provider exists.

## Failures — hybrid (return value vs exception)

- **Expected absence** (a 404 the adapter understands as "this just
  doesn't exist") → a nullable return / empty collection the consumer
  checks inline.
- **Genuine failure** (5xx, 429-after-retries, auth failure, network) →
  a **domain exception** in `app/Exceptions/` (e.g.
  `IntegrationUnavailable`, `IntegrationMisconfigured`,
  `IntegrationRateLimited extends IntegrationUnavailable`).
- Domain exceptions never expose HTTP status codes or Saloon types in
  their public API.
- **Nothing under `app/Http/Integrations/` escapes the Service** — every
  Saloon exception is caught and either swallowed into a return value or
  rethrown as a domain exception.

## The InMemory impl

The consumer-tier test default and a dev/demo fallback (boot the app
with no API key). Full stateful store at the **domain layer**, with a
**fluent builder** so tests shape returns inline.

```php
final class InMemorySymbolQuoteService implements SymbolQuoteService
{
    /** @var array<string, SymbolQuote> */ private array $quotes = [];
    /** @var array<string, Throwable> */   private array $throws = [];

    public static function fake(): self { return new self(); }

    public function withQuote(Symbol $s, SymbolQuote $q): self { $this->quotes[$s->value] = $q; return $this; }
    public function throwsOn(Symbol $s, Throwable $e): self     { $this->throws[$s->value] = $e; return $this; }

    public function quote(Symbol $symbol): ?SymbolQuote
    {
        if (isset($this->throws[$symbol->value])) throw $this->throws[$symbol->value];
        return $this->quotes[$symbol->value] ?? null;
    }
}
```

Scope limits:

- Mirrors behavior at the **domain layer only** — no HTTP semantics, no
  rate limits, no transport errors. Those belong to the Saloon tier.
- Speaks **domain vocabulary** — seed with domain Data factories
  (`fbarrento/data-factory`), never touch vendor DTOs.
- Deterministic IDs (`in-memory-1`, …) for write-capable contracts so
  tests assert without seeding ids by hand. State resets per test
  (fresh binding per test).
- Models **only** the domain exceptions the contract declares (its
  `throwsOn(...)` helper) — for the *same logical conditions* as the
  Saloon-backed impl. It never simulates 429/5xx; how the app reacts to
  those is a Service-tier concern with the real adapter + fixtures.
