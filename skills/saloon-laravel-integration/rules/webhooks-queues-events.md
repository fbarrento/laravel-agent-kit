# Webhooks, queues & events

The write/push side. **Skip this chapter for pure read-pull adapters**
(a quote service needs none of it). One architectural rule spans all
three: **webhook handlers and jobs are *consumers* — they depend on the
Contract, never the connector.**

## Webhooks (inbound)

- **Location.** Dedicated `routes/integrations.php`; controllers at
  `app/Http/Controllers/Integrations/<Provider>/`.
- **Pipeline (thin controller):** verify signature → dedupe → persist
  raw → dispatch job → return 2xx fast.
  1. **Verify signature** in middleware (HMAC from the webhook secret).
     Reject invalid early. Global secret in config for single-tenant;
     per-tenant secret in `Integration.metadata` for multi-tenant.
  2. **Dedupe** by provider event-id (a `webhook_events` table or
     cache) — providers retry, so process each event once.
  3. **Persist** the raw verified payload.
  4. **Dispatch a queued job** and return `2xx` immediately.
- **Reuse the seam.** The job parses the payload into the **same
  `Data/` vendor DTO layer** and translates to domain via the **same
  Service/translation boundary** — webhooks do not invent a parallel
  path.
- **Testing/HITL.** Inbound payloads are fixtures too, but *captured*:
  the human triggers a real event in the provider, you capture the
  verified payload once and replay it. Signature tests use a known fixed
  secret.

## Queues (outbound async)

- **When.** Writes, slow calls, anything that would block a web request.
  Cached reads stay synchronous.
- **Hard rule — no secrets in job payloads.** Store the **tenant id**
  (`integration_id`/`user_id`) on the job and re-resolve the connector
  via the factory inside `handle()`. Serializing a connector or token
  into the payload leaks secrets into the queue store (Redis/DB) in
  plaintext.

  ```php
  public function __construct(public int $integrationId) {}

  public function handle(SymbolQuoteService $service): void { /* … */ }
  ```

- **Retry/backoff.** `$tries` + `backoff()`; on `IntegrationRateLimited`,
  `release()` with the `Retry-After` delay — this is the queued context
  where sleep-style waiting is acceptable (see
  [resilience.md](resilience.md)).
- Jobs call the **Contract**, not the connector.

## Events

- **Domain events** (`app/Events/`: `IntegrationConnected`,
  `IntegrationTokenRefreshed`, `QuoteRefreshed`, …) fire from the Service
  or consuming job at meaningful business moments. These drive app
  reactions.
- **Saloon HTTP-lifecycle events** (sending/sent, via the Laravel
  plugin) are for **telemetry/Telescope only**. Never hang business
  logic off transport hooks.
