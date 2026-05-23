# Naming

Cross-cutting naming for `resources/js`. Consistent names are what let a
flat, feature-sliced layout stay navigable — you find a file by guessing
its name, not by browsing folders.

## Rule: casing by kind

| Kind | Casing | Example |
|---|---|---|
| Files & folders | `kebab-case` | `vehicle-table.tsx`, `organization-settings/` |
| Components & types | `PascalCase` | `VehicleTable`, `VehicleListItem` |
| Hooks, functions, variables | `camelCase` | `useVehicleFilters`, `selectedIds` |
| Story state exports | `PascalCase` (fixed set) | `Default`, `Empty`, `Error` |

**Why:** kebab file names are stable across React/Vue/Svelte and avoid
case-sensitivity bugs across OSes; Pascal vs camel at the symbol level is
the ecosystem norm (a `PascalCase` identifier reads as a component/type, a
`camelCase` one as a value). One file can therefore be `vehicle-table.tsx`
exporting `VehicleTable` without ambiguity.

```tsx
// file: features/vehicles/vehicle-table.tsx
export function VehicleTable(/* ... */) { /* ... */ }
```

## Rule: plural resource folder, singular file basename

A resource folder is the **plural** route name; the files inside use the
**singular** entity name.

```txt
features/vehicles/            // plural folder
  vehicle.types.ts            // singular basenames
  vehicle.fixtures.ts
  vehicle-table.tsx
  use-vehicle-filters.ts
pages/vehicles/               // plural folder (flat — see roles.md)
  index.tsx
```

**Why:** the plural folder matches the Laravel route resource
(`vehicles.index`), so the frontend folder and the backend route read the
same. Singular file basenames name the *thing* the file is about (a
vehicle table, a vehicle's types), which is how you'd say it out loud.

Page files are named for the **action**: `index.tsx`, `show.tsx`,
`create.tsx`, `edit.tsx`.

## Rule: story file = component basename + `.stories`

`vehicle-table.tsx` → `vehicle-table.stories.tsx`. An optional
`.spec.json` contract uses the same basename. Story `meta.title` is the
**lowercase path** to the component:

```txt
'features/vehicles/vehicle-table'
'components/ui/button'
```

…which yields a stable story id like
`features-vehicles-vehicletable--default` (title kebabbed, `--`, lowercased
export). State exports come from the fixed vocabulary in
[../stories/conventions.md](../stories/conventions.md).

**Why:** deriving the story id from a lowercase-path title makes ids
predictable and stable, so feedback, fixtures, and verification can
reference a story without anyone hand-maintaining the id.

## Rule: hooks are `use-<thing>.ts` / `use<Thing>`

A resource-local hook is a kebab file `use-vehicle-filters.ts` exporting a
camelCase `useVehicleFilters`. It lives in the feature folder, never a
global `hooks/` ([../architecture/roles.md](../architecture/roles.md)).

## Rule: frontend type aliases drop the backend `Data` suffix and name for intent

Aliases drop the `Data` suffix the transformer produces and name for
intent:

| Generated (PHP-derived) | Frontend alias | Lives in |
|---|---|---|
| `App.Data.Vehicles.VehicleIndexPageData` | `VehicleIndexPageProps` | the page file (local) |
| `…VehicleListItemData` | `VehicleListItem` | `vehicle.types.ts` (shared) |
| `…VehicleFormData` | `VehicleFormValues` | `vehicle.types.ts` (shared) |
| `…VehicleFiltersData` | `VehicleFilters` | `vehicle.types.ts` (shared) |

The **page-props** alias is page-specific, so it is declared **locally in
the page file** and not exported ([../architecture/roles.md](../architecture/roles.md)).
Aliases shared across ≥2 files live in the feature's `*.types.ts`.

```ts
// pages/vehicles/index.tsx — page-props alias is local, not exported
import type { App } from '@/types/generated'
type VehicleIndexPageProps = App.Data.Vehicles.VehicleIndexPageData

// features/vehicles/vehicle.types.ts — shared aliases (grouped; type-only file)
import type { App } from '@/types/generated'
export type VehicleListItem = App.Data.Vehicles.VehicleListItemData
export type VehicleFormValues = App.Data.Vehicles.VehicleFormData
export type VehicleFilters = App.Data.Vehicles.VehicleFiltersData
```

**Why:** the alias is the frontend's vocabulary — `VehicleListItem` reads
better at use sites than `VehicleListItemData`, and `…PageProps` says "this
is what a page receives." It also gives one place to absorb a backend
rename. The *generated* symbol shape (`App.Data.<Resource>.<Name>Data`,
always `PascalCase`) is owned by [../types/generated.md](../types/generated.md);
this rule only governs the frontend alias.

## Rule: stable selector hooks use `data-part`

For a stable selector an annotation tool or test can target, add a
`data-part="..."` attribute rather than relying on generated class names
or DOM structure.

```tsx
<div data-part="filter-bar">{/* ... */}</div>
```

**Why:** generated Tailwind classes and DOM position are not contracts —
they change when styling or layout changes, breaking any selector pinned
to them. A named `data-part` is an intentional, stable hook. (Reserve
`data-testid` for test-only targets if your project already uses it; keep
one convention, don't mix.)

## Checklist

- Files/folders kebab-case; components/types PascalCase; hooks/functions/
  vars camelCase.
- Resource folder plural; file basenames singular; page files named for
  the action.
- Story file shares the component basename; `meta.title` is the lowercase
  component path.
- Resource-local hooks are `use-<thing>.ts` / `use<Thing>`, inside the
  feature folder.
- Frontend type aliases drop `Data` and name for intent; generated symbol
  shape deferred to `types/generated.md`.
- Stable selectors use `data-part`, never generated classes or DOM
  position.
