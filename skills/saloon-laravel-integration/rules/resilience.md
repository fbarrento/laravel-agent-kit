# Resilience — rate limiting & caching

For quota-constrained APIs (FinnHub free tier is ~60 req/min), these two
work together: a cache hit must cost **zero** rate-limit budget.

## Rate limiting (`saloonphp/rate-limit-plugin`)

- **Key per tenant.** In multi-tenant, each user's API key has its own
  quota, so the limiter store key must include the `Integration`/user id.
  A shared global limiter wrongly throttles user B because user A was
  busy.
- **On-limit behavior depends on context:**
  - **Web request → fail fast.** Sleeping blocks an FPM worker. Let the
    plugin throw `RateLimitReached`; the Service translates it to a
    domain `IntegrationRateLimited extends IntegrationUnavailable`
    (per [contracts.md](contracts.md)).
  - **Queued/CLI → sleep-and-retry.** Blocking is fine off the request
    path. Use the job's `release()` with the `Retry-After` delay (see
    [webhooks-queues-events.md](webhooks-queues-events.md)).

## Caching — domain layer by default

Cache **inside the Service**, returning the domain Data, with
`Cache::remember`. On a hit the connector is never invoked, so it costs
zero rate-limit budget and zero translation, and `InMemory` needs no
caching at all.

```php
public function quote(Symbol $symbol): ?SymbolQuote
{
    return Cache::remember(
        $this->cacheKey($symbol),       // see keying rule
        now()->addSeconds(5),           // per-method TTL
        fn () => $this->fetchAndTranslate($symbol),
    );
}
```

HTTP-layer caching (`saloonphp/cache-plugin` middleware on the
connector) is the alternative when several Service methods reuse one
large payload, or you want conditional-request (ETag) handling. It
caches the vendor shape *before* translation and must be neutralized in
tests.

### Keying rule

- Response depends only on request params (a quote for `AAPL` is the
  same regardless of whose key fetched it) → **global key by params**.
- Response depends on *who* asks (portfolio, watchlist) →
  **tenant-scoped key** (include the owner id).

### TTL

Per method, by volatility — seconds for quotes, hours/days for reference
data (company profile). No global magic number.

### In tests

- Use the `array` cache driver.
- Assert caching explicitly at the **Service tier**: a second call does
  not re-hit the connector (verify via the `MockClient` request count).
- Recording runs (`RECORD_INTEGRATIONS_FIXTURES=true`) must **bypass
  cache** so the wire is always hit and the fixture reflects a real call.
