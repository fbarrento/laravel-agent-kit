# Naming

Cross-cutting naming for `resources/js`. Consistent names are what let a
flat, feature-sliced layout stay navigable — you find a file by guessing
its name, not by browsing folders.

The **kinds** being named (page, feature, component, generated type,
page-props alias, hook, `data-part`) are defined in
[../../LANGUAGE.md](../../LANGUAGE.md); the rules below say how to spell
them.

## Rule: domain names come from `CONTEXT.md`

`LANGUAGE.md` names the **frontend architecture** (page, feature,
generated type); the project's `CONTEXT.md` names the **domain** (Signup,
Invoice, Vehicle). A resource folder, feature, or type alias is named with
the **domain** term — `features/vehicles/`, `VehicleListItem` — where
`vehicle` is the `CONTEXT.md` term (matching the backend route resource).

- If the repo has a `CONTEXT.md` / `CONTEXT-MAP.md`, name every domain
  concept with **its** term, and never with a term that glossary lists
  under `_Avoid_`. Keep the frontend resource name aligned with the
  backend route resource and the `CONTEXT.md` term — all three should read
  the same.
- If the concept isn't in the glossary, that's a signal — either you're
  inventing language the project doesn't use (reconsider) or there's a
  real gap; surface it and suggest `/grill-with-docs` rather than coining
  a term silently.
- No `CONTEXT.md` at all → proceed silently. The glossary is produced by
  `/grill-with-docs`, not by this skill.

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

**Documentation-page titles** use a fixed top-level vocabulary so the same
title scheme drives the sidebar groups
([../stories/conventions.md](../stories/conventions.md)): `Introduction`,
`brand/<page>` (e.g. `brand/tone-of-voice`), and `design-system/<token>`
(e.g. `design-system/colors`).

## Rule: hooks are `use-<thing>.ts` / `use<Thing>`

A hook is a kebab file `use-<thing>.ts` exporting a camelCase `use<Thing>`
(`use-vehicle-filters.ts` → `useVehicleFilters`). The name is identical
wherever it lives; only the **home** differs, by the hook decision tree
([../architecture/roles.md](../architecture/roles.md)): a **resource-local**
hook lives in its feature folder (`features/vehicles/use-vehicle-filters.ts`); a
**generic, framework-bound** hook lives in the top-level `hooks/` tier
(`hooks/use-mobile.ts`). A pure helper is a plain function in `lib/`, not a hook.

## Rule: frontend type aliases drop the backend `Data` suffix and name for intent

Aliases drop the `Data` suffix the transformer produces and name for
intent:

| Generated (imported by name) | Frontend alias | Lives in |
|---|---|---|
| `VehicleIndexPageData` | `VehicleIndexPageProps` | the page file (local) |
| `VehicleListItemData` | `VehicleListItem` | `vehicle.types.ts` (shared) |
| `VehicleFormData` | `VehicleFormValues` | `vehicle.types.ts` (shared) |
| `VehicleFiltersData` | `VehicleFilters` | `vehicle.types.ts` (shared) |

The **page-props** alias is the firm case — every page names its props
**locally** in the page file, not exported
([../architecture/roles.md](../architecture/roles.md)). **Feature-type
aliases are optional** readability sugar: import and use the generated
`*Data` name directly, or alias it (in the feature's `*.types.ts`, when
shared across ≥2 files) where the rename reads better at use sites.

```ts
// pages/vehicles/index.tsx — page-props alias is local, not exported
import type { VehicleIndexPageData } from '@/types/generated'
type VehicleIndexPageProps = VehicleIndexPageData

// features/vehicles/vehicle.types.ts — optional shared aliases (grouped; type-only file)
import type { VehicleListItemData, VehicleFormData, VehicleFiltersData } from '@/types/generated'
export type VehicleListItem = VehicleListItemData
export type VehicleFormValues = VehicleFormData
export type VehicleFilters = VehicleFiltersData
```

**Why:** the alias is the frontend's vocabulary — `VehicleListItem` reads
better at use sites than `VehicleListItemData`, and `…PageProps` says "this
is what a page receives." It also gives one place to absorb a backend
rename. The *generated* symbol shape (`<Name>Data`, a flat `PascalCase`
name imported from `@/types/generated`) is owned by
[../types/generated.md](../types/generated.md); this rule only governs the
frontend alias.

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
  component path. Doc-page titles use the fixed vocab `Introduction` /
  `brand/<page>` / `design-system/<token>`.
- Hooks are `use-<thing>.ts` / `use<Thing>`; resource hooks in the feature
  folder, generic framework-bound hooks in the top-level `hooks/` tier.
- Page-props type is a local alias of the generated `*PageData`;
  feature-type aliases (drop `Data`, name for intent) are optional;
  generated symbol shape deferred to `types/generated.md`.
- Stable selectors use `data-part`, never generated classes or DOM
  position.
