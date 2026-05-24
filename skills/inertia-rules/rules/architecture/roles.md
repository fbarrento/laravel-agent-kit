# Frontend roles

> **[Page](../../LANGUAGE.md)**, **feature**, and **hook** are defined in `LANGUAGE.md`; this file owns the role graph that places them.

The role graph is the placement system for `resources/js`. Every file has
one role; the role decides what it may contain and what it may import.
This is the frontend counterpart to the backend's CQRS boundary.

```txt
pages/<resource>/*    route adapters only
features/<resource>/* resource-local workflow UI + behavior
components/ui/*        token-bound, domain-free primitives
components/app/*       reusable, generic app components
layouts/*             app shells
lib/*                 pure, framework-free helpers
hooks/*               generic, framework-bound hooks (bottom tier, peer of lib/)
types/generated.ts    read-only backend-derived types (one generated module)
types/shared/*        small generic frontend-only types
```

## Rule: pages are thin route adapters

A page file receives typed Inertia props, selects a layout, and composes
feature/app components. It holds no resource workflow UI, no tables or
forms, no formatting. **The only type a page declares is its own props —
a local, un-exported alias of the generated `*PageData`** (never a
handwritten field shape, never `any`).

**Why:** pages map 1:1 to routes, so they are the worst place to bury
reusable logic — nothing else can import a page. Keeping them thin makes
the real UI live in `features/*`, where it is reusable and testable in
isolation (a story), and keeps the route surface scannable. The props
type is page-specific (only this page receives these props), so it lives
in the page as a local alias — not exported, not in a feature file.

```tsx
// Good — props type is a local alias of the generated PageData; thin adapter
import type { VehicleIndexPageData } from '@/types/generated'
import { AppLayout } from '@/layouts/app-layout'
import { VehicleTable } from '@/features/vehicles/vehicle-table'

type VehicleIndexPageProps = VehicleIndexPageData // local, not exported

export default function VehiclesIndex({ vehicles, can, copy }: VehicleIndexPageProps) {
  return (
    <AppLayout>
      <VehicleTable vehicles={vehicles} can={can} copy={copy} />
    </AppLayout>
  )
}

// Bad — handwritten field shape (or `any`), page owns the table and formats
export default function VehiclesIndex({ vehicles }: { vehicles: { id: number; price: number }[] }) {
  return <table>{vehicles.map(v => <tr>{new Intl.NumberFormat().format(v.price)}</tr>)}</table>
}
```

## Rule: pages mirror Laravel resource controllers

Page files map to the **read** actions of a resource controller. Mutating
actions never become pages — they are generated Wayfinder calls.

| Laravel action | Page | Notes |
|---|---|---|
| `VehicleController@index` | `pages/vehicles/index.tsx` | thin adapter |
| `@show` | `pages/vehicles/show.tsx` | thin adapter |
| `@create` | `pages/vehicles/create.tsx` | thin adapter |
| `@edit` | `pages/vehicles/edit.tsx` | thin adapter |
| `@store` / `@update` / `@destroy` | none | use generated Wayfinder action |

**Non-resource screens are first-class.** Not every page maps to a resource
controller — a dashboard, a settings overview, an onboarding flow is a
cohesive *screen*, not a CRUD resource. It still gets a thin page
(`pages/dashboard/index.tsx`) and its composing UI still lives in a feature
(`features/dashboard/*`); it just isn't backed by `index/show/create/edit`.
A page is keyed on a cohesive **concept** — usually a resource, sometimes a
screen — and stays an adapter either way: it composes features and owns no
workflow UI.

## Rule: pages are flat — one resource folder deep, never nested

`pages/` has exactly one level of resource folder, each holding only
action files. Do **not** create nested page trees. A nested or dot
resource is **flattened** to a single kebab-case page folder.

```txt
// Good — flat
pages/vehicles/index.tsx
pages/organization-vehicles/index.tsx     // nested resource, flattened

// Bad — nested page tree
pages/organizations/vehicles/index.tsx
```

Folder names are kebab-case from the route resource name
(`organization-settings`).

**Why:** a deep `pages/` tree forces you to guess the hierarchy to find a
page and couples the page path to a backend route shape that can change.
A flat, one-level-per-resource layout keeps every page reachable at a
predictable `pages/<resource>/<action>` and matches the flat-folder
discipline used everywhere else.

## Rule: resource UI lives in `features/<resource>`, not in global buckets

Resource-specific tables, forms, filters, empty states, view-model state,
and any resource-local hook live under `features/<resource>/`. **Never put a
*resource's* behaviour in a global bucket, and do not create top-level
`queries/`, `forms/`, or `composables/` folders.** The ban is about a
*resource's* behaviour scattering — not about every global folder: the one
sanctioned **hand-written** global bucket is `hooks/`, for **generic**
(non-resource) hooks only (next rule); `resources/js/actions` and `routes`
hold **generated** Wayfinder output only.

**Why:** global behavior buckets scatter one *resource's* UI across many
trees and invite cross-resource coupling. Co-locating by resource keeps a
feature's surface in one folder, mirrors how Laravel groups a resource, and
makes the unit you delete-or-move atomic. A `hooks/` folder holding *only*
app-wide hooks scatters no single resource, so it is compatible with that
rationale.

```txt
// Good
features/vehicles/vehicle-table.tsx
features/vehicles/use-vehicle-filters.ts   // resource-local hook, named locally

// Bad
hooks/use-vehicles.ts                       // a RESOURCE hook in a global bucket → features/vehicles
forms/vehicle-form.tsx
actions/vehicles.ts                         // not generated → forbidden
```

If UI is **domain-free** (it names no resource concept and reads identically
for any resource), it belongs in `components/app/*` — build it there as soon
as you judge it reusable, even with a single consumer
([../design-system/components.md](../design-system/components.md) owns the
promotion rule). Domain-bound UI stays in the feature; when a second feature
needs it, **generify** it (strip the resource vocabulary, drive by props) on
the way to `components/app` — never import it sideways from another feature
(see the import rule below).

## Rule: feature folders are flat — files self-index, no internal subfolders

A `features/<resource>/` folder is **flat**: its components, its
resource-local hook, and its `*.types.ts` all sit at one level, named to
self-index (`vehicle-table.tsx`, `vehicle-row.tsx`, `vehicle-filters.tsx`,
`use-vehicle-filters.ts`, `vehicle.types.ts`). Do **not** add `components/`,
`hooks/`, or `types/` subfolders inside a feature.

**Why:** a flat feature mirrors the flat-folder discipline used in `pages/`
and the backend — the filename predicts the file, with no hierarchy to guess.
A feature that feels like it *needs* subfolders is usually two concepts; split
it into sibling features rather than nesting one.

## Rule: place a hook by the decision tree — pure → `lib/`, resource → `features/`, generic → `hooks/`

Decide where a hook (or hook-shaped helper) lives in this order:

1. **Pure — no React, no Inertia router?** It is *not a hook*; it is a plain
   function in `lib/` (`get-initials`, `cleanup-mobile-navigation`). Keeping it
   a "hook" only to colocate it is a smell.
2. **Tied to one resource?** It lives in `features/<resource>/`
   (`use-vehicle-filters`, `use-two-factor-auth`), named locally
   ([../naming/conventions.md](../naming/conventions.md)).
3. **Generic (app-wide) *and* framework-bound?** It lives in the top-level
   **`hooks/`** tier — `use-appearance`, `use-current-url` (`usePage()`),
   `use-flash-toast` (router), `use-clipboard` (`useState`), `use-mobile`
   (`useSyncExternalStore`).

`hooks/` is a **bottom tier, a peer of `lib/`** — so anything may import
`@/hooks/*`, **including a primitive** (`components/ui/sidebar → @/hooks/use-mobile`)
without an upward import. It is the one hand-written global bucket, and it must
hold **only** generic hooks: a resource hook here is a violation
([naming](../naming/conventions.md) governs the name; this rule the home).

**Why:** the role graph previously had no slot for a hook that is generic *and*
framework-bound — not resource-local (so not `features/`), not pure (so excluded
from `lib/`). Forcing it into `features/` mislabels it as one resource's; into
`lib/` it breaks `lib/`'s framework-free guarantee; colocating it in
`components/ui`/`app` splits one concept to dodge the import rule. A dedicated
bottom tier closes the gap with one predictable home that the
downward-import rule already permits everyone to reach.

## Rule: imports point downward; never upward or sideways into pages

The dependency direction is `pages → features → components/app →
components/ui → lib / types / hooks`. A lower role never imports a higher one.

- A **feature** never imports a **page** or a page-owned type, and never
  imports **another feature** (no sideways coupling): cross-feature
  composition happens at the **page** — the only composer that reaches
  multiple features — and genuinely shared UI is generified into
  `components/app`.
- A **primitive** (`components/ui`) never imports a feature, app
  component, or any resource/domain concept — but it **may** import the bottom
  tier: `lib/*`, `types/*`, and `@/hooks/*` (e.g. `ui/sidebar → @/hooks/use-mobile`),
  since those sit at or below it.
- An **app component** (`components/app`) never references a specific
  resource by name.
- `lib/*` contains no components and no Inertia router calls; `hooks/*` is the
  home for the framework-bound generic behaviour `lib/*` may not hold.

**Why:** the direction is what keeps primitives reusable and pages
disposable. An upward import (feature → page) makes the feature
un-reusable and the page un-deletable; a domain concept in a primitive
poisons the whole design system with one resource's vocabulary.

## Rule: one export per file

A module with a runtime export holds **exactly one exported symbol** — one
component per file, one hook per file. Inline declarations that are *not*
exported (a page's local props type, a small helper used only in that
file) don't count against the rule.

**Exception: type-only files.** A `*.types.ts` module has no runtime
export and may group a resource's related type aliases (see
[../types/generated.md](../types/generated.md) and
[../naming/conventions.md](../naming/conventions.md)).

```tsx
// Good — one exported component; props type declared inline, not exported
type VehicleTableProps = { vehicles: VehicleListItem[] }
export function VehicleTable({ vehicles }: VehicleTableProps) { /* ... */ }

// Bad — two components exported from one file
export function VehicleTable() { /* ... */ }
export function VehicleRow() { /* ... */ }   // give it its own file
```

**Why:** one export per file means the filename predicts the symbol, every
component is independently findable, importable, and story-able, and diffs
stay legible. Type-only files are exempt because grouped type aliases have
no "hidden second component" problem — the risk the rule guards against.

## Checklist

- Page is a thin adapter: typed props in, layout selected, features
  composed; no tables/forms/formatting. Its only declared type is its own
  props, a local un-exported alias of the generated `*PageData`.
- Resource pages exist only for `index`/`show`/`create`/`edit`; mutations use
  Wayfinder, not page files. Non-resource screens (dashboard, settings) get a
  thin page too, just not backed by a resource controller.
- Resource UI is under `features/<resource>`; no global
  `queries/forms/composables` folders, and no *resource* behaviour in a global
  bucket.
- Feature folders are flat (files self-index); no `components/`/`hooks/`/`types/`
  subfolders inside a feature.
- Cross-feature reuse goes through `components/app` (generified) or page-level
  composition; features never import each other.
- A hook is placed by the tree: pure → `lib/` (a plain function, not a hook);
  resource → `features/<resource>`; generic + framework-bound → top-level
  `hooks/` (the one hand-written global bucket — generic hooks only).
- One exported symbol per runtime module (component/hook); `*.types.ts`
  may group type aliases.
- Imports point downward; no feature→page or feature→feature imports, no
  domain concepts in `components/ui` (which may still import the
  `lib`/`types`/`hooks` bottom tier), no resource names in `components/app`.
- `resources/js/actions` and `resources/js/routes` hold only generated
  output.
