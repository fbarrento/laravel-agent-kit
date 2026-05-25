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

## STOP — how this skill works

This file is a ROUTER, not the rules. Reading it does NOT mean you have
"applied the skill." The actual rules live in `rules/**/*.md` and are NOT in
your context yet.

Before you write or edit ANY component, page, hook, or type you MUST, in order:

1. Identify the building block you are touching (a page, a feature component, a
   primitive/app component, a form, a hook, a layout, a story, a generated
   type, …).
2. Open and READ IN FULL the matching rule file(s) from the Routing Table
   below. The table gives pointers only — never rule content. You cannot
   satisfy a rule you have not read.
3. Before emitting any code in your reply, output a line:
   `Rules consulted: <comma-separated relative paths of every rule file you read>`
   If that line would be empty, you are NOT ready to write code — return to
   step 2.
4. After writing the code, re-read the `## Checklist` section of each rule file
   you used and confirm every item against your code. Report any item you
   cannot satisfy instead of silently skipping it.

Hard rules:
- Do not work from memory, from the Routing Table labels, or from a single
  nearby example. Nearby code may itself violate these rules.
- If you are about to create or edit a component/page/hook/type without the
  governing rule file in context, STOP and read it first.
- This applies to EVERY agent: orchestrators, sub-agents, and you. A sub-agent
  that writes code must perform steps 1–4 itself; it may not assume the
  orchestrator did.

## Glossary

The frontend vocabulary this skill reasons in — **roles & artifacts**
(page, feature, component, token, generated type, page-props alias, story,
hook, `data-part`) and **cross-cutting concerns** (side effects, accessibility, page
meta/SEO, shared data, capability flags, layouts, loading/empty/error
states, backend-owned copy, feedback) — is defined once in
[LANGUAGE.md](LANGUAGE.md). Use
those terms exactly; rule files carry the grammar and link back to the
definition. Name the **frontend architecture** from `LANGUAGE.md`; name
the **domain** from the project's `CONTEXT.md` (see
[naming](rules/naming/conventions.md)). The backend **Data object** that
becomes a frontend *generated type* is owned by **laravel-rules**.

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
- **all markup, tokens, and layout live in `ui` primitives** — features/pages/
  layouts render components, not raw HTML; appearance via variant props,
  arrangement via a layout primitive's props, not raw Tailwind or inline `ds-`
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

## Routing Table

The right column is a POINTER. It tells you which file applies — never what the
rule says. You must open the file.

| You are touching… | Read (in full) |
|---|---|
| A page (route adapter) | `rules/architecture/roles.md` |
| A feature component | `rules/architecture/roles.md`, `rules/design-system/components.md` |
| A design-system primitive or app component | `rules/design-system/components.md`, `rules/design-system/styling.md`, `rules/design-system/tokens.md` |
| Styling / Tailwind / `ds-` classes / layout arrangement | `rules/design-system/styling.md`, `rules/design-system/tokens.md` |
| Raw HTML / markup inside a feature, page, or layout | `rules/design-system/components.md` |
| A hook | `rules/architecture/roles.md` |
| Backend-derived / generated types | `rules/types/generated.md` |
| Rendering backend text, money, dates, enum labels | `rules/types/formatting.md` |
| A form | `rules/forms/conventions.md` |
| Navigation & data loading (partial reloads, deferred props, prefetch, polling, infinite scroll) | `rules/navigation/conventions.md` |
| Optimistic updates or a non-Inertia request | `rules/interactivity/conventions.md` |
| Shared / ambient page data, flash, or page title/meta | `rules/shared-data/conventions.md` |
| A layout | `rules/layouts/conventions.md` |
| Code splitting / lazy loading / asset perf | `rules/performance/conventions.md` |
| A Storybook story | `rules/stories/conventions.md` |
| Running the headless story suite / story CI | `rules/stories/operations.md` |
| Client-side side effects (effects, prop-copy, optimism) | `rules/side-effects/conventions.md` |
| Client vs server state ownership | `rules/state/conventions.md` |
| Loading / empty / error states | `rules/loading-states/conventions.md` |
| Capability-gated UI / authorization in the UI | `rules/authorization/conventions.md` |
| Accessibility (semantic HTML, labels, focus) | `rules/accessibility/conventions.md` |
| Writing a frontend test | `rules/testing/conventions.md` |
| Naming a file, component, hook, type, or story id | `rules/naming/conventions.md` |
| Brand copy / brand contract | `rules/brand/conventions.md` |
| Boost vs this skill (tool boundary) | `rules/architecture/boost-boundary.md` |
| A human-in-the-loop feedback item | `rules/feedback/conventions.md` |
| Pre-handoff verification | `rules/verification/conventions.md` |
| Self-check before handoff | `rules/audit/conventions.md` |
| Assembling a handoff | `rules/handoff/conventions.md` |

Building-block vocabulary (page, feature, primitive/app component, generated
type, story, hook, layout, …) is defined in [LANGUAGE.md](LANGUAGE.md). Use
those terms exactly.

## How to apply

1. Read the project's `CONTEXT.md` / `CONTEXT-MAP.md` (if present) and any
   relevant `docs/adr/` before touching code. Name resources, features, and
   types from the domain glossary; never an `_Avoid_` alias.
2. Follow the STOP gate at the top of this file. It is not optional.
3. Before building UI, confirm the backend contract exists: generated types
   (Spatie Data) and routes/actions (Wayfinder). If they're missing, that's a
   backend task first — do not handwrite the shapes.
4. When rules conflict, this skill wins over Boost's Inertia/React guidance and
   `.agents/skills/laravel-best-practices` on frontend shape.
5. Before handoff, run the verification checklist and assemble handoff evidence.

## Enforcement: mechanical where a tool exists, a hard checklist where it doesn't

Mechanically checkable rules MUST be backed by an automated check WHEN the
consuming project has tooling for it. Where no tool exists, the rule is a
MANDATORY manual checklist item that is never skipped — the inertia-rules
skill is intentionally CLI-agnostic (see its "Conventions-only" section).

The executing agent MUST first read the project's `package.json` scripts and
lint/TS config and bind each rule to a check that ACTUALLY exists. Do not name
a script, lint rule, or test suite the project does not define.

Automated (bind to the project's real scripts before claiming done):
- Generated types are regenerated, never hand-edited — run the
  laravel-typescript-transformer generate step, then `tsc --noEmit` (or the
  project's type-check script); the generated-file diff must be intentional.
  See `rules/types/generated.md`.
- Lint and type-check scripts pass with zero new errors.
- Storybook build succeeds; reusable UI has a story (`rules/stories/conventions.md`).
- If an a11y test runner exists, it passes (`rules/accessibility/conventions.md`).

Manual checklist (no command assumed — verify by hand, per rule file):
- Pages are thin route adapters (`rules/architecture/roles.md`).
- Styling goes through design-system primitives, not raw Tailwind in features
  (`rules/design-system/styling.md`).
- User-facing copy/format comes from backend props (`rules/types/formatting.md`).
- Verification done per `rules/verification/conventions.md`.

Do not invent tooling. A valuable check with no tool yields a TODO to add that
tooling — never a hallucinated command.
