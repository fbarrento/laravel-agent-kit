# Testing & HITL recording

Builds on `saloon-integration`'s fixture rules (redaction, no
`MockResponse::make()`, fixtures recorded from the live API). This file
adds the Laravel three-tier layering, the recording-mode safety switch,
and the human-in-the-loop recording ritual.

## Three-tier layering

| Tier | Path | What it tests | Fixtures? |
|------|------|---------------|-----------|
| **Saloon** | `tests/Unit/Http/Integrations/<Provider>/` | connector, resources, request URL/method/body, vendor DTO hydration | **always** (HITL recording lives here) |
| **Service** | `tests/Unit/Contracts/` | adapter→domain translation, failure mapping | **conditional** |
| **Consumer** | `tests/Feature/` | controllers, actions, jobs depending on the Contract | **never** — bind `InMemory` |

- **Saloon tier is always real** — fixtures are the schema-drift canary
  at the boundary that actually drifts (the wire format).
- **Service tier is conditional** — write it only when translation has
  logic worth testing. Heuristic: *if removing the Service impl in your
  head changes the domain Data result, write a Service test.* Pure
  field-rename pass-throughs are already covered by Saloon-tier hydration
  tests. Translation tests use the real Saloon impl + `MockClient` +
  fixtures and assert the domain shape.
- **Consumer tier binds `InMemory` by default** — feature tests stay
  fast and need no fixtures. Provide a base-`TestCase` helper:

```php
protected function usesInMemoryIntegrations(): void
{
    $this->app->singleton(SymbolQuoteService::class, fn () => InMemorySymbolQuoteService::fake());
}
```

A consumer test that *deliberately* wants the real Saloon stack simply
doesn't call it and binds the real impl with a `MockClient` instead.

## Recording mode vs replay mode

The base skill leaves Saloon's auto-record-on-miss on. In a Laravel app
**invert that** so CI can never fire a real call or poison a fixture.

```php
// tests/Pest.php
$recording = filter_var($_ENV['RECORD_INTEGRATIONS_FIXTURES'] ?? false, FILTER_VALIDATE_BOOL);
MockConfig::setFixturePath('tests/Fixtures/Saloon');
if (! $recording) {
    MockConfig::throwOnMissingFixtures();   // CI: missing fixture = loud failure
}
```

`RECORD_INTEGRATIONS_FIXTURES=true` lives only in a dev's
`.env.testing`, alongside live credentials. CI never sets it.

## The 4-step HITL recording ritual

Recording needs real third-party state, and **only a human can create
it** (accounts, API keys, specific records). Before running any pest
test that uses a `…Fixture(...)`, the agent:

1. **Detect record mode.** Check (a) `RECORD_INTEGRATIONS_FIXTURES` is
   `true`, (b) the named fixture files exist on disk.
   - recording on + fixture missing → run the ritual below.
   - recording off + fixture missing → tell the user "this will fail in
     replay mode; turn on `RECORD_INTEGRATIONS_FIXTURES` and start
     recording?" before running.
   - fixture present → just run; no ritual.
2. **State brief.** Name the fixture about to record, list the
   prerequisites inferred from the request/test (URL params, body
   fields, env vars), and ask the human to confirm or provide them:
   > About to record `quotes/get.json`. To record this I need a symbol
   > that returns a live quote (markets open). `FINNHUB_TEST_SYMBOL` in
   > `.env.testing` should match it. Confirm `AAPL` works, or give me a
   > symbol + its API key.
3. **Wait for explicit go-ahead.** Do not run pest until the human says
   ready. Re-prompt on ambiguity.
4. **Record, then handle the outcome.** Run the test.
   - **2xx** → confirm what landed, then prompt for cleanup:
     > Recorded `quotes/get.json` (200, 1 record). Leave the test data
     > in your sandbox or clean it up?
   - **4xx** → **do not commit.** Surface the body and ask whether state
     is wrong (redo setup) or the assertion is wrong (rewrite test). A
     committed 4xx fixture replays the error forever.

## Never hand-craft fixtures

Fixtures come from the live API. **Exception (narrowed from the base
skill):** response shapes you cannot reproduce by manipulating the
request — typically 5xx, malformed-JSON, truncated bodies. If you can
trigger it with input (400, 401, 404, 422, even 429 on most APIs),
**record it**. The motivating case is Laravel 5xx-handler / retry-
middleware / job-retry code that the real API won't emit on demand.
