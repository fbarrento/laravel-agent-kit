---
name: inertia-rules
description: Conventions for AI-assisted frontend work in Laravel + Inertia (v3) apps — Laravel-like frontend roles (thin page adapters, resource-local features, token-bound components), generated backend-derived types, backend-owned formatting and translation, a three-tier design-system token contract, forms (`<Form>`/`useForm`), navigation and data loading (partial reloads, deferred props, prefetch), shared data and page meta, persistent layouts, Storybook story contracts, and evidence-based verification and handoffs. Use when writing, reviewing, or refactoring Inertia pages, feature components, forms, layouts, design-system primitives, stories, or typed fixtures in a Laravel/Inertia/React app. Sibling to laravel-rules (backend); this skill owns the Inertia frontend side.
license: MIT
metadata:
  author: Francisco Barrento
---

# Inertia Rules

## STOP — how this skill works

This file is a ROUTER, not the rules. Reading it does NOT mean you have
"applied the skill." The actual rules live in `rules/**/*.md` and are NOT in
your context yet.

Before you write or edit ANY file under `resources/js` you MUST, in order:

1. Identify the role or artifact you are touching (page, feature, `ui`
   primitive, `app` component, layout, hook, generated type, design token,
   story, …).
2. Open and READ IN FULL the matching rule file(s) from the Routing Table
   below. The table gives pointers only — never rule content. You cannot
   satisfy a rule you have not read.
3. Before emitting any code in your reply, output a line:
   `Rules consulted: <comma-separated relative paths of every rule file you read>`
   If that line would be empty, you are NOT ready to write code — return to
   step 2.
4. After writing, re-read the `## Checklist` section of each rule file you
   used and confirm every item against your code. Report any item you cannot
   satisfy instead of silently skipping it.

Hard rules:
- Do not work from memory, from the Routing Table labels, or from a single
  nearby example. Nearby code may itself violate these rules.
- Before building UI, confirm the backend contract exists (generated types via
  Spatie Data, routes/actions via Wayfinder). If it is missing, that is a
  backend task first — do NOT hand-write the shapes.
- This applies to EVERY agent: orchestrators, sub-agents, and you. A sub-agent
  that writes code must perform steps 1–4 itself.

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
| A feature component | `rules/architecture/roles.md` |
| A `ui` primitive (`components/ui`) | `rules/design-system/components.md`, `rules/design-system/styling.md`, `rules/design-system/tokens.md` |
| An `app` component (`components/app`) | `rules/design-system/components.md` |
| A layout | `rules/layouts/conventions.md` |
| A hook or `lib/` helper | `rules/architecture/roles.md` |
| Backend-derived / generated types | `rules/types/generated.md` |
| User-facing copy, formatting, dates, translation | `rules/types/formatting.md` |
| Design tokens / `--ds-*` | `rules/design-system/tokens.md` |
| Styling / Tailwind / variants | `rules/design-system/styling.md` |
| A form | `rules/forms/conventions.md` |
| Navigation, partial reloads, prefetch, polling, infinite scroll | `rules/navigation/conventions.md` |
| Optimistic updates, instant visits, non-Inertia requests | `rules/interactivity/conventions.md` |
| Shared data, page meta, flash | `rules/shared-data/conventions.md` |
| Performance / code-splitting / lazy loading | `rules/performance/conventions.md` |
| Loading / empty / error states | `rules/loading-states/conventions.md` |
| Component state / props-as-state | `rules/state/conventions.md` |
| Side effects | `rules/side-effects/conventions.md` |
| Authorization / capability props | `rules/authorization/conventions.md` |
| Accessibility | `rules/accessibility/conventions.md` |
| A Storybook story | `rules/stories/conventions.md` |
| Story CI / the headless story suite | `rules/stories/operations.md` |
| Tests (story interaction / Pest Browser / Vitest) | `rules/testing/conventions.md` |
| Laravel Boost for app facts | `rules/architecture/boost-boundary.md` |
| Naming a file, component, story id, type alias, or data attribute | `rules/naming/conventions.md` |
| Brand / the brand contract | `rules/brand/conventions.md` |
| Human-in-the-loop feedback | `rules/feedback/conventions.md` |
| Pre-handoff verification | `rules/verification/conventions.md` |
| Self-check before handoff (violation catalog) | `rules/audit/conventions.md` |
| Producing a handoff | `rules/handoff/conventions.md` |

Frontend vocabulary (page, feature, component, token, generated type, story,
hook, `data-part`, …) is defined in [LANGUAGE.md](LANGUAGE.md). Use those terms
exactly.

## How to apply

1. Read the project's `CONTEXT.md` / `CONTEXT-MAP.md` (if present) before
   touching code. Name resources, features, and types from the domain
   glossary; never an `_Avoid_` alias.
2. Follow the STOP gate at the top of this file. It is not optional.
3. Confirm the backend contract exists (generated types, Wayfinder
   routes/actions) before building UI. Missing contract = backend task first.
4. When rules conflict, this skill wins over Laravel Boost's Inertia/React
   guidance — that skill is the API reference; these files own code shape.
5. Use Boost for live Laravel facts (routes, schema, logs, docs) instead of
   guessing — see `rules/architecture/boost-boundary.md`.

## Enforcement: mechanical where a tool exists, a hard checklist where it does not

Mechanically checkable rules MUST be backed by an automated check WHEN the
consuming project has tooling for it. Where no tool exists, the rule is a
MANDATORY manual checklist item that is never skipped — this skill is
intentionally CLI-agnostic (see `## Conventions-only (no CLI assumed)`).

Before mapping checks, the agent MUST read the project's `package.json`
scripts and its lint / TypeScript config, and bind each rule to a check that
ACTUALLY exists. Do not name a script, lint rule, or test suite the project
does not define. A valuable check with no tool yields a TODO to add that
tooling — never a hallucinated command.

Automated (bind to the project's real scripts; run before claiming done):
- Generated types are regenerated, never hand-edited — run the
  `laravel-typescript-transformer` generate step, then `tsc --noEmit` (or the
  project's type-check script); the generated-file diff must be intentional.
  See `rules/types/generated.md`.
- The project's lint and type-check scripts pass with zero new errors.
- The Storybook build succeeds and reusable UI has a story
  (`rules/stories/conventions.md`); honor the headless-suite gotchas in
  `rules/stories/operations.md`.
- If the project has an accessibility test step (e.g. an axe gate in the story
  suite), it passes (`rules/accessibility/conventions.md`).
- Route/interaction tests pass (`rules/testing/conventions.md`).

Manual checklist (no command assumed — verify by hand, per rule file):
- Pages are thin route adapters; resource UI lives in `features/<resource>`
  (`rules/architecture/roles.md`).
- Styling flows through design-system primitives and variant props, not raw
  Tailwind or inline `ds-` in features (`rules/design-system/styling.md`).
- User-facing copy and locale-sensitive formatting come from backend props,
  not inline strings (`rules/types/formatting.md`).
- No `useEffect` data fetching, no `useState` prop-copy
  (`rules/side-effects/conventions.md`).
- Pre-handoff verification and evidence assembled
  (`rules/verification/conventions.md`, `rules/audit/conventions.md`,
  `rules/handoff/conventions.md`).
