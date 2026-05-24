---
name: inertia-rules
description: Conventions for AI-assisted frontend work in Laravel + Inertia (v3) apps — Laravel-like frontend roles (thin page adapters, resource-local features, token-bound components), generated backend-derived types, backend-owned formatting and translation, a three-tier design-system token contract, forms (`<Form>`/`useForm`), navigation and data loading (partial reloads, deferred props, prefetch), shared data and page meta, persistent layouts, Storybook story contracts, and evidence-based verification and handoffs. Use when writing, reviewing, or refactoring Inertia pages, feature components, forms, layouts, design-system primitives, stories, or typed fixtures in a Laravel/Inertia/React app. Sibling to laravel-rules (backend); this skill owns the Inertia frontend side.
license: MIT
metadata:
  author: Francisco Barrento
---

# Inertia Rules

Conventions that give AI agents Laravel-like discipline on the **Inertia
frontend**: predictable page/resource/component roles, generated
backend-derived types, backend-owned copy and formatting, a
design-system token contract, story contracts, and evidence-based
verification.

Sibling to **laravel-rules** (which owns backend PHP shape). This skill
owns the `resources/js` side of a Laravel + Inertia app. For Laravel,
Inertia, React, Tailwind, Pest, or Wayfinder API syntax, use the
framework docs (and Laravel **Boost** for live app facts — see
[boost-boundary](rules/architecture/boost-boundary.md)); use these files
for code shape.

## Priority

**Higher priority than Laravel Boost's _Inertia React Development_ skill
(and any framework-shipped Inertia/React guidance) when both apply.** That
skill is the reference for *Inertia v3 API usage* — `<Form>`/`useForm`,
`<Link>`/`router`, deferred props, prefetching, optimistic updates,
instant visits, layout props, `useHttp`, `usePoll`, `WhenVisible`,
`InfiniteScroll`. Use it for **how an API works**. Use **these files for
code shape**, and where the two differ on shape, **these win**:

- props are **typed from generated backend contracts**, never the loose
  untyped `{ users }` the Boost examples show ([types/generated.md](rules/types/generated.md));
- pages are **thin route adapters** that compose features — not pages that
  render lists/forms inline ([architecture/roles.md](rules/architecture/roles.md));
- user-facing text/format comes from **backend props**, not inline strings
  ([types/formatting.md](rules/types/formatting.md));
- styling flows through **design-system primitives and their variant props**
  (`ds-` tokens live in `ui`), not raw Tailwind or inline `ds-` in features
  ([design-system/styling.md](rules/design-system/styling.md));
- one export per file, reusable UI gets a story, etc.

So: the Boost skill shows the *mechanism* (a working `<Form>`); this skill
constrains the *shape* (where it lives, how it's typed, how errors and
copy flow). Treat a Boost example as correct API and incomplete shape —
apply these conventions on top.

## Conventions-only (no CLI assumed)

The "Inertia Agent Kit" product describes an `iak` CLI, JSON schemas, an
MCP server, and a feedback store. **None of that is assumed here.** These
files are the conventions an agent applies *by hand*, using tools that
exist today: Spatie Laravel Data, `spatie/laravel-typescript-transformer`,
Wayfinder, Storybook, Pest Browser / Playwright, and Boost. Where a rule
references "audit" or "verify", treat it as a **manual checklist**, not a
command — until the package ships.

## Scope: the Laravel + Inertia React adapter

These conventions target the **Laravel + Inertia React** adapter
(`@inertiajs/react`). The code *shape* — JSX components, `useForm`/`<Form>`,
`usePage`, the hooks — is written for React. The *principles* — backend-owned
types, copy, formatting, and authorization; props as the single source of
state; thin pages composing resource-local features — carry to the Vue and
Svelte adapters unchanged; the component and hook syntax does not. On another
adapter, keep the boundaries and translate the syntax.

## The role graph at a glance

```txt
resources/js/
  pages/<resource>/*        route adapters only (thin; mirror Laravel resource controllers)
  features/<resource>/*     resource-local workflow UI + resource-local behavior
  components/ui/*           token-bound, domain-free primitives
  components/app/*          reusable, generic app components
  layouts/*                 app shells
  lib/*                     pure, framework-free helpers
  hooks/*                   generic, framework-bound hooks (bottom tier, peer of lib/)
  types/generated.ts        read-only backend-derived types (one generated module; gitignored, regenerated)
  types/shared/*            small generic frontend-only types
```

**The one rule that governs everything:** the frontend never owns what
Laravel owns. Backend-derived types, user-facing copy, translation, and
locale-sensitive formatting come from PHP through Inertia props. The
frontend composes UI, handles interaction, and renders display-ready
values. No *resource* behaviour in a global bucket — a resource's UI lives in
`features/<resource>`; no top-level `queries/`/`forms/`/`composables/`. The one
hand-written global bucket is `hooks/`, for **generic** (non-resource)
framework-bound hooks only (pure helpers are functions in `lib/`).

## Rule index

**Architecture**
- [architecture/roles.md](rules/architecture/roles.md) — the role graph, page=thin-adapter, resource-controller→page mapping, downward import boundaries, the hook-placement decision tree (pure→lib / resource→features / generic→`hooks/` bottom tier).
- [architecture/boost-boundary.md](rules/architecture/boost-boundary.md) — use Boost for Laravel facts; this layer for Inertia/frontend discipline; the required agent loop.

**Types**
- [types/generated.md](rules/types/generated.md) — Spatie Data + typescript-transformer (flat named imports from one gitignored, Vite-regenerated module) + Wayfinder; three type-ownership zones; never handwrite or re-narrow backend-derived types.
- [types/formatting.md](rules/types/formatting.md) — backend owns formatting/translation; what is banned in render paths; what frontend formatting is allowed.

**Design system**
- [design-system/tokens.md](rules/design-system/tokens.md) — three-tier token model (primitives → semantic `--ds-*` → Tailwind bridge), bridge prefix rule, import order.
- [design-system/styling.md](rules/design-system/styling.md) — `ds-` tokens live in `ui` primitives (via variants); consumers pass variant props; structural utilities + layout primitives for arrangement; the decision procedure.
- [design-system/components.md](rules/design-system/components.md) — primitive/app/feature roles; `ui` owns tokens, `app` is token-free (bar the `NavLink` exception); anticipatory + domain-free promotion; appearance-via-variants, arrangement-via-layout-primitives.

**Runtime behavior** (Inertia v3)
- [forms/conventions.md](rules/forms/conventions.md) — `<Form>` vs `useForm`, Wayfinder actions, server-owned validation errors, processing/reset, file uploads.
- [navigation/conventions.md](rules/navigation/conventions.md) — `<Link>`, partial reloads (`only`/lazy props), deferred props + `<Deferred>`, prefetch, polling (`usePoll`), load-on-scroll (`<WhenVisible>`), infinite scroll + merge props, no parallel client cache.
- [interactivity/conventions.md](rules/interactivity/conventions.md) — instant visits, optimistic updates (props snapshot + rollback), and `useHttp` as the only sanctioned non-Inertia request escape hatch.
- [shared-data/conventions.md](rules/shared-data/conventions.md) — `HandleInertiaRequests::share`, `usePage`, flash/errors, `<Head>` title/meta.
- [layouts/conventions.md](rules/layouts/conventions.md) — persistent layouts, default-in-`createInertiaApp`, nested layouts, chrome vs content.
- [performance/conventions.md](rules/performance/conventions.md) — lazy page code-splitting (don't go eager), `React.lazy` for heavy feature components, Vite-driven asset versioning; optimize against measured cost.

**Stories**
- [stories/conventions.md](rules/stories/conventions.md) — Storybook as the reusable-UI runtime contract, required stories/states, typed fixtures, sidebar taxonomy + autodocs, foundation-page bar (live values/meaning/applying).
- [stories/operations.md](rules/stories/operations.md) — project-CI gotchas for the headless suite (vite-plugin bypass, SSR-warmup noise, a11y gate, theme/viewport); not conventions.

**Quality**
- [state/conventions.md](rules/state/conventions.md) — server state from props; no client cache; ephemeral local state; derive don't store.
- [loading-states/conventions.md](rules/loading-states/conventions.md) — explicit empty/loading/error; `<Deferred>` fallbacks; empty-state component; error boundaries.
- [authorization/conventions.md](rules/authorization/conventions.md) — gate UI from backend `can.*` capability props; never reimplement authorization client-side; gating is UX, the server still authorizes.
- [accessibility/conventions.md](rules/accessibility/conventions.md) — WCAG 2.2 AA target (laws set the level; confirm per project); semantic HTML, labelled fields + associated errors, keyboard/focus, a11y in primitives; "compliance" is build-to-standard + partial axe + human testing, not an agent certification.
- [testing/conventions.md](rules/testing/conventions.md) — the test pyramid: story interaction vs Pest Browser route tests vs Vitest unit; test behavior not implementation.

**Workflow & evidence**
- [feedback/conventions.md](rules/feedback/conventions.md) — human-in-the-loop feedback discipline; resolve only with evidence.
- [verification/conventions.md](rules/verification/conventions.md) — the pre-handoff verification checklist and the evidence it produces.
- [audit/conventions.md](rules/audit/conventions.md) — the convention-violation catalog to self-check before handoff.
- [handoff/conventions.md](rules/handoff/conventions.md) — what a complete, evidence-based handoff contains.

**Naming**
- [naming/conventions.md](rules/naming/conventions.md) — casing by kind, plural-folder/singular-file, story ids, frontend type-alias scheme, `data-part` selectors.

**Brand**
- [brand/conventions.md](rules/brand/conventions.md) — Brand OS boundary: consume the brand contract, adapt to `ds-` tokens, never own brand copy in the frontend.

## How to apply

1. Identify which role you're touching (page? feature? primitive? story?) and read the matching rule file before writing code.
2. Before building UI, confirm the backend contract exists: generated types (Spatie Data) and routes/actions (Wayfinder). If they're missing, that's a backend task first — do not handwrite the shapes.
3. Keep pages thin; put resource UI in `features/<resource>`; keep styling on semantic `ds-` utilities.
4. Before handoff, run the [verification](rules/verification/conventions.md) checklist and assemble [handoff](rules/handoff/conventions.md) evidence.
5. Use **Boost** for live Laravel facts (routes, schema, logs, docs) instead of guessing — see [boost-boundary](rules/architecture/boost-boundary.md).
