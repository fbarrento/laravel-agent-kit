# Language

The vocabulary this skill reasons in — the **roles and artifacts** of a
Laravel + Inertia frontend (`resources/js`). Use them exactly; reach for the
listed term before inventing a synonym, and never use an `_Avoid_` alias.

This file is the **canonical home for each term's definition** (the *what*
and its aliases). The `rules/` files own the *grammar* — the role graph, the
token tiers, the story contract — and link back here for the definition
rather than restating it.

Two distinct vocabularies are in play, and they must not blur:

- **This file (`LANGUAGE.md`)** names the **frontend architecture** — page,
  feature, primitive, token. It ships with the skill and is the same in
  every project.
- **The project's `CONTEXT.md`** names the **domain** — Signup, Invoice,
  Vehicle. It lives in the target repo, is written by `/grill-with-docs`,
  and differs per project.

So you write *"the `vehicles` **feature**"* — `vehicle` from `CONTEXT.md`,
`feature` from here. Domain naming is governed by
[rules/naming/conventions.md](rules/naming/conventions.md).

Sibling to **laravel-rules**, which owns the backend vocabulary. Where a
term crosses the boundary (below), this file defers to laravel-rules **by
name**, not by path — the skills install independently.

## Terms

Each term is defined once below — what it **is**, the rule file that owns
its *grammar*, and the `_Avoid_` aliases never to use for it. **Roles &
artifacts** are the things you build; **cross-cutting concerns** are the
disciplines that apply across them.

### Roles & artifacts

| Term | Definition (what it *is*) | Grammar | `_Avoid_` |
|---|---|---|---|
| **Page** | A thin route adapter (`pages/<resource>/*`): takes typed props, picks a layout, composes feature/app components. No workflow UI/formatting. Declares only its page-props alias. | [roles](rules/architecture/roles.md) | screen, view, container, controller |
| **Feature** | Resource-local workflow UI + behavior (`features/<resource>/*`) — the tables, forms, hooks for **one** resource. Frontend counterpart to a backend resource. | [roles](rules/architecture/roles.md) | module, widget, section, partial |
| **Component** | Reusable UI in one of three roles: **primitive** (`ui/*`, domain-free, owns `ds-` tokens, defines variants), **app** (`app/*`, generic), **feature** (`features/<resource>/*`, knows one resource). | [components](rules/design-system/components.md) | "component" for a page/layout; styling a primitive via `ds-` classes from outside |
| **Token** | A design-system value in the **three-tier** model: Tier 1 raw primitives → Tier 2 semantic `--ds-*` → Tier 3 Tailwind `ds-` utility bridge. App code consumes `ds-` utilities. | [tokens](rules/design-system/tokens.md) | raw hex/px in component code; a hard-coded Tailwind class where a `ds-` utility exists |
| **Generated type** | A read-only `*Data` type imported from `@/types/generated` (from Spatie Data / PHP enums). The backend **Data object** (**laravel-rules**) as it arrives on the frontend — never handwritten. | [generated](rules/types/generated.md) | handwriting page-prop/enum/form-value types; duplicating a backend contract; "interface" for a backend-derived shape |
| **Page-props alias** | The **local, un-exported** alias a page declares for its generated `*PageData` (`type VehicleIndexPageProps = VehicleIndexPageData`). Feature-type aliases are optional sugar. | [naming](rules/naming/conventions.md) | exporting page-props; reusing one page's props type in another |
| **Story** | A colocated `*.stories.tsx` — the **runtime contract** for reusable UI, an executable proof of a component's states. Required for primitives + app components. | [stories](rules/stories/conventions.md) | stories as marketing docs; a story standing in for a route's browser test |
| **Hook** | A `use-<thing>.ts` exporting `use<Thing>` — **resource-local** (feature folder) or **generic, framework-bound** (top-level `hooks/`). A pure helper is a `lib/` function, not a hook. | [naming](rules/naming/conventions.md), [roles](rules/architecture/roles.md) | a "hook" holding no React state/effect (that's a `lib/` helper) |
| **`data-part`** | A named `data-part="..."` attribute giving a stable selector for tests/annotation tools — used instead of generated Tailwind classes or DOM position (not contracts). | [naming](rules/naming/conventions.md) | pinning a selector to a generated class name or DOM structure |

### Cross-cutting concerns

| Term | Definition (what it *is*) | Grammar | `_Avoid_` |
|---|---|---|---|
| **Side effect** | Implicit client-side work that should be explicit — a `useEffect` fetch, a `useState` copy of props, a shadow-copy optimistic update. The frontend counterpart to a hidden backend observer; the creed is *one source of truth, explicit mutations, no hidden work*. | [side-effects](rules/side-effects/conventions.md) | a `useEffect` doing work Inertia already does; client state mirroring server state |
| **Accessibility** | A **build-time** convention targeting **WCAG 2.2 AA** (confirm jurisdiction/level per project): semantic markup + primitive affordances. The verify a11y check is the backstop, not the strategy. | [accessibility](rules/accessibility/conventions.md) | bolt-on a11y / "audit later"; an agent self-certifying "compliant" |
| **Page meta (SEO)** | The document head — title, meta — rendered via `<Head>`. The **content is backend-owned** (the `seo` slice of a page's `*PageData`); the frontend only renders it. | [shared-data](rules/shared-data/conventions.md) | handwriting meta/title strings in the frontend; client-side title juggling |
| **Shared data** | Ambient page context (auth user, flash, app config) shared **once** via `HandleInertiaRequests::share()` and read through `usePage().props`. | [shared-data](rules/shared-data/conventions.md) | prop-drilling ambient data through pages/components; a client store for server state |
| **Capability flag (`can.*`)** | A backend-computed authorization boolean (from policies/gates) shipped as a typed prop. The frontend **renders** it (`can.update`), never **decides** it. | [authorization](rules/authorization/conventions.md) | re-deriving a permission in JS from roles, ownership (`user.id === …`), or feature flags |
| **Layout** | **Persistent** app chrome (nav, sidebar, flash region) assigned via the page's `layout` property, so chrome + its state survive client navigation. | [layouts](rules/layouts/conventions.md) | wrapping each page's JSX in `<AppLayout>…</AppLayout>`; per-visit chrome teardown |
| **Loading / empty / error states** | The three non-happy-path states every async/collection surface renders deliberately — the same canonical states a **story** proves and production renders. | [loading-states](rules/loading-states/conventions.md) | a blank/`null` render; a bare, context-free spinner |
| **Backend-owned copy & formatting** | Display-ready strings (copy, money, dates, enum labels) formatted in **Laravel** and arriving in props; the frontend renders them, never formats them. | [formatting](rules/types/formatting.md) | formatting user-facing text in render paths; client-side i18n / number/date formatting |
| **Feedback** | A human-in-the-loop UI flag (surface + locator + message + artifacts) resolved with **evidence**, not closed with prose. | [feedback](rules/feedback/conventions.md) | resolving a feedback item with prose alone |

## Relationships

- The **role graph** is the placement system: **page** (adapter) → composes
  **feature** and **component** → **primitive** owns **tokens**.
- A **page** declares exactly one **page-props alias** over a **generated
  type**; everything else it renders comes from **features** and
  **components**.
- A **generated type** is the frontend face of a backend **Data object**
  (owned by **laravel-rules**) — one source of truth, crossed at the Inertia
  seam.
- Reusable **components** ship a **story**; **primitives** are the only
  consumers of **tokens**.

## Rejected framings

- **Handwriting backend-derived shapes** "to move faster." A handwritten
  copy is a second source of truth that drifts silently — always import the
  **generated type**.
- **Styling app code with raw `ds-`/Tailwind values.** Appearance comes from
  a **primitive's** variants; only primitives touch **tokens**.
