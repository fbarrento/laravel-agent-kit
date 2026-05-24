# Frontend roles

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
and any resource-local hook live under `features/<resource>/`. **Do not
create top-level `queries/`, `actions/`, `forms/`, `hooks/`, or
`composables/` folders.**

**Why:** global behavior buckets scatter one resource's UI across five
trees and invite cross-resource coupling. Co-locating by resource keeps a
feature's surface in one folder, mirrors how Laravel groups a resource,
and makes the unit you delete-or-move atomic. `resources/js/actions` and
`resources/js/routes` are reserved for **generated** Wayfinder output
only.

```txt
// Good
features/vehicles/vehicle-table.tsx
features/vehicles/use-vehicle-filters.ts   // resource-local hook, named locally

// Bad
hooks/use-vehicles.ts
forms/vehicle-form.tsx
actions/vehicles.ts                         // not generated → forbidden
```

If behavior is pure and framework-free, it belongs in `lib/`. If a
component becomes generic across resources, promote it to
`components/app/*`.

## Rule: imports point downward; never upward or sideways into pages

The dependency direction is `pages → features → components/app →
components/ui → lib/types`. A lower role never imports a higher one.

- A **feature** never imports a **page** or a page-owned type.
- A **primitive** (`components/ui`) never imports a feature, app
  component, or any resource/domain concept.
- An **app component** (`components/app`) never references a specific
  resource by name.
- `lib/*` contains no components and no Inertia router calls.

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
- Pages exist only for `index`/`show`/`create`/`edit`; mutations use
  Wayfinder, not page files.
- Resource UI is under `features/<resource>`; no global
  `queries/actions/forms/hooks/composables` folders.
- One exported symbol per runtime module (component/hook); `*.types.ts`
  may group type aliases.
- Imports point downward; no feature→page imports, no domain concepts in
  `components/ui`, no resource names in `components/app`.
- `resources/js/actions` and `resources/js/routes` hold only generated
  output.
