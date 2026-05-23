---
name: saloon-laravel-integration
description: Integrate a third-party HTTP API into a Laravel app with SaloonPHP using a ports-and-adapters layout — Saloon connector/resources/DTOs as the adapter, a Contract + Service as the port, domain Data objects the rest of the app consumes. Covers multi-tenant credential storage, per-tenant rate limiting, domain-layer caching, webhooks/queues/events, and a human-in-the-loop (HITL) fixture-recording ritual where the agent asks the human to set up third-party state before recording. Use when wiring a Saloon-based integration into a Laravel app (e.g. a FinnHub quote service), adding a contract-backed integration service, recording fixtures that need live third-party state, or debugging multi-tenant token/refresh issues.
---

# Saloon Laravel Integration (ports & adapters)

Use this skill when integrating a third-party API **into a Laravel app**
(in-app code, no separate composer package) with SaloonPHP, behind a
domain Contract.

**This skill layers on `saloon-integration`.** That skill owns the
Saloon mechanics — connector, resources, requests, output/input DTOs,
fixture redaction, the recording workflow. Read it first; this skill
only adds the Laravel concerns: the ports-and-adapters boundary,
container wiring, multi-tenant credentials, resilience, the write/push
side, and the HITL recording ritual. For non-Saloon Pest conventions,
see `pest-package-tests`.

Assumes `saloonphp/laravel-plugin` is installed. If you can't add it,
fall back to the plugin-free `MockClient` patterns in `saloon-integration`.

## The shape (ports & adapters)

```
app/Http/Integrations/FinnHub/        # ADAPTER (Saloon, vendor vocabulary)
  FinnHubConnector.php  FinnHubConnectorFactory.php
  Data/  Requests/  Resources/  Enums/  Exceptions/
app/Contracts/                        # PORT + implementations (flat)
  SymbolQuoteService.php              #   the interface
  FinnHubSymbolQuoteService.php       #   Saloon-backed adapter-impl
  InMemorySymbolQuoteService.php      #   test/dev default
app/Data/                             # DOMAIN Data (provider-agnostic)
  SymbolQuote.php
```

**The one rule that governs everything: dependency points
adapter → domain, never the reverse.** Nothing in `app/Contracts/` or
`app/Data/` may import anything under `app/Http/Integrations/`. The
domain must not know a provider exists. Consumers (controllers, actions,
jobs, webhook handlers) depend on the **Contract**, never the connector.

## HITL recording is the headline behavior

Fixtures are recorded from the **live** API, never hand-crafted (one
narrow exception: response shapes you cannot reproduce by manipulating
the request — 5xx, malformed/truncated bodies). Recording needs real
third-party state (an account, an API key, specific records). **Only a
human can create that state**, so before recording the agent runs a
4-step dialogue ritual: detect record mode → brief the human on exactly
what state is needed → wait for go-ahead → record, then handle the
outcome and prompt for cleanup. See [rules/testing.md](rules/testing.md).

## Rule index

1. **Architecture** → [rules/architecture.md](rules/architecture.md) —
   the four parts, dependency direction, container bindings, the
   connector factory (single- vs multi-tenant), the polymorphic
   `integrations` table, encryption, and the two-path token lifecycle.
2. **Contracts & translation** → [rules/contracts.md](rules/contracts.md)
   — the port, the Saloon-backed impl, the `InMemory` fluent builder,
   adapter→domain translation, and hybrid failure handling.
3. **Testing & HITL** → [rules/testing.md](rules/testing.md) — three-tier
   layering, `RECORD_INTEGRATIONS_FIXTURES` mode + CI safety, the 4-step
   HITL ritual, the never-hand-craft rule.
4. **Resilience** → [rules/resilience.md](rules/resilience.md) —
   per-tenant rate limiting, domain-layer caching, key/TTL rules.
5. **Webhooks, queues, events** →
   [rules/webhooks-queues-events.md](rules/webhooks-queues-events.md) —
   the write/push side; skip for pure read-pull adapters.
6. **Pitfalls** → [rules/pitfalls.md](rules/pitfalls.md) —
   Laravel-specific footguns + the per-provider `FINDINGS.md` convention.

## How to apply

1. Confirm you're in a Laravel app integrating a third-party API behind
   a Contract. If you're building a standalone SDK package instead, use
   `saloon-integration` directly.
2. Build the adapter (Saloon side) per `saloon-integration`, then the
   port + Service + `InMemory` impl per [rules/contracts.md](rules/contracts.md).
3. Wire the container binding (`Contract → Service`) and the factory
   per [rules/architecture.md](rules/architecture.md).
4. Write tests tier by tier; when a test needs to record a fixture,
   run the HITL ritual in [rules/testing.md](rules/testing.md) — never
   fabricate fixture JSON.
