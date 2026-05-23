# Architecture

Ports & adapters for an in-app Saloon integration. The base
`saloon-integration` skill owns the adapter internals; this file owns
the Laravel boundary and wiring.

## The four parts

| Part | Lives in | Speaks | Consumed by |
|------|----------|--------|-------------|
| **Adapter** (connector, resources, requests, vendor DTOs) | `app/Http/Integrations/<Provider>/` | vendor vocabulary | only the adapter-impl |
| **Port** (interface) | `app/Contracts/<Name>Service.php` | domain vocabulary | the whole app |
| **Adapter-impl** (Saloon-backed Service) + **InMemory** | `app/Contracts/` (flat, beside the port) | implements the port | bound in the container |
| **Domain Data** | `app/Data/` | domain vocabulary | the whole app |

`app/Http/Integrations/` is Saloon's `laravel-plugin` default (plural).
Use `php artisan make:saloon-connector` etc. to scaffold the adapter.

## The dependency rule (non-negotiable)

**adapter → domain, never the reverse.**

- `app/Contracts/*` and `app/Data/*` MUST NOT import anything under
  `app/Http/Integrations/`.
- The Service (adapter-impl) is the *only* place that imports both the
  vendor DTOs and the domain Data — it is the translation seam.
- Consumers (controllers, actions, jobs, webhook handlers) depend on the
  **Contract**, never the connector or vendor DTOs.

A grep that should always return nothing:

```bash
grep -rEl 'App\\Http\\Integrations' app/Contracts app/Data
```

## Container bindings

Bind the port to the Saloon-backed impl in `AppServiceProvider::register()`;
swap to `InMemory` in tests (see [testing.md](testing.md)).

```php
$this->app->bind(SymbolQuoteService::class, FinnHubSymbolQuoteService::class);
```

## The connector factory

Consumers never `new` a connector. The Service receives a factory (or,
single-tenant, the connector itself) by injection.

### Multi-tenant (default)

Users bring their own credentials, so the connector is built per-request
from the tenant's stored token. The factory owns persistence; the
connector stays storage-agnostic.

```php
final class FinnHubConnectorFactory
{
    public function for(Integration $integration): FinnHubConnector { /* … */ }
    public function forToken(string $token): FinnHubConnector { /* tests, CLIs */ }
}
```

The Service depends on the factory, not the connector:

```php
public function __construct(private FinnHubConnectorFactory $factory) {}
```

### Single-tenant simplification

One set of app-level credentials — the factory is dead weight. Bind the
connector as a singleton and inject it directly:

```php
$this->app->singleton(FinnHubConnector::class, fn () => new FinnHubConnector(
    token: config('services.finnhub.token'),
));
```

### Hybrid

Mostly multi-tenant but with app-level admin operations (webhook
handlers, scheduled syncs, admin CLIs run as the app, not as a user):
keep the factory and expose both `for(Integration $i)` and `forApp()`.

## Credential storage — polymorphic `integrations` table

```
integrations
  id
  integratable_type, integratable_id   # polymorphic owner (User, Team, …)
  provider                             # 'finnhub', 'stripe', …
  access_token        encrypted
  refresh_token       encrypted nullable
  expires_at          nullable          # plaintext — you query on it
  metadata            json nullable     # opaque provider state ONLY
  timestamps
```

`metadata` is for state the app never queries on. Anything you'd
`->where('metadata->x', …)` belongs in a real column.

### Encryption at rest

- **Default:** Laravel `encrypted` cast on `access_token` /
  `refresh_token`. `expires_at` stays plaintext.
- **Hardening (recommended when user tokens outrank your own app data —
  brokerage/OAuth tokens usually do):** a separate integration
  encryption key + custom cast, so a leaked `APP_KEY` doesn't expose
  third-party tokens and they rotate independently.
- **Regulated/enterprise:** store only a reference; fetch from a secret
  manager at runtime.
- Always: never log tokens, redact them in fixtures (base skill), tokens
  never leave the Service/Factory boundary.

### Token lifecycle — the factory branches on auth type

- **API-key providers (FinnHub):** static key in `access_token`;
  `refresh_token`/`expires_at` null. Factory reads it and sets the
  authenticator (FinnHub uses a `?token=` query param). No refresh, no
  lock.
- **OAuth2 providers:** before building the connector the factory checks
  `expires_at`; if expired (or within a skew window) it refreshes
  **under `Cache::lock("integration:{$id}:refresh")`**, persists the new
  tokens to the row, then builds the connector with a fresh
  `AccessTokenAuthenticator`. Saloon does the refresh HTTP; the factory
  owns the persist. Two footguns: (1) refreshing without the lock
  double-refreshes and can invalidate a just-issued token on providers
  that rotate refresh tokens; (2) refreshing *inside the connector*
  tangles HTTP with persistence and breaks the InMemory/test seam.
