# Pitfalls

Laravel-specific footguns. For Saloon-level traps (`#[Override]` on
`defaultBody()`, MockClient class-vs-sequence mode, clone helpers
dropping the mock, coverage attribution) see `saloon-integration`'s
`pitfalls.md`.

## Dependency-direction leaks

- A domain/contract file importing `App\Http\Integrations\…` inverts the
  dependency. Guard with:
  ```bash
  grep -rEl 'App\\Http\\Integrations' app/Contracts app/Data   # must be empty
  ```
- A named constructor like `SymbolQuote::fromFinnHub()` is the subtle
  form of the same leak — keep translation in the Service.

## Secrets

- **Tokens in job payloads.** Serializing a connector/token into a
  queued job writes the secret to Redis/DB in plaintext. Store the
  tenant id; re-resolve via the factory in `handle()`.
- **Tokens in logs/fixtures.** Redact in fixtures (base skill) and in
  Laravel log scrubbing. Tokens never leave the Service/Factory boundary.

## Token refresh (OAuth)

- **Refresh without a lock** double-refreshes under concurrency and can
  invalidate a just-issued token on providers that rotate refresh
  tokens. Wrap refresh in `Cache::lock("integration:{$id}:refresh")`.
- **Refreshing inside the connector** tangles HTTP with persistence and
  breaks the InMemory/test seam. The factory owns persistence.

## Testing

- **Poisoned fixture (committed 4xx).** Usually a wrong `.env.testing`
  on the first record. CI replays the error forever. Delete and
  re-record (base skill); never commit a non-2xx fixture except the
  documented non-reproducible-error exception.
- **Cache masking the wire.** A live cache hit during recording produces
  no real call. Bypass cache when `RECORD_INTEGRATIONS_FIXTURES=true`.
- **Auto-record on in CI.** If you forget `throwOnMissingFixtures()`, a
  missing fixture in CI fires a real call with whatever creds happen to
  be present (or 401s and poisons the fixture). Replay mode is the
  default; recording is opt-in.
- **Hand-crafting fixtures** because the live setup is annoying. Don't —
  run the HITL ritual instead. The only exception is genuinely
  non-reproducible responses (5xx, malformed/truncated bodies).
- **InMemory drifting from the contract.** When the contract gains a
  method or a new domain exception, update `InMemory` in lockstep — a
  stale InMemory makes feature tests pass against behavior the real
  adapter no longer provides.

## FINDINGS log

Carry over the base skill's convention, per provider:
`docs/integrations/<provider>/FINDINGS.md`. When the provider's actual
response surprises you (undocumented field, spec-vs-runtime mismatch,
auth quirk), append a dated entry so the next recording session doesn't
relearn it.
