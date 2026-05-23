# Generated backend-derived types

PHP is the source of truth for every backend-derived shape: page props,
DTOs, enums, form payloads, filters, validation field names, capability
flags, and routes/actions. The frontend **imports** these contracts; it
never reinvents them.

Default stack:
- **Spatie Laravel Data** — page props, DTOs, form data, filters,
  display/value shapes, copy payloads.
- **`spatie/laravel-typescript-transformer`** — TypeScript output from
  those Data classes and PHP enums.
- **Wayfinder** — typed routes and controller actions.

## Rule: never handwrite a backend-derived type

Do not declare, in frontend-owned files, anything that duplicates a
backend contract: page-prop interfaces, copies of Data classes, enum
unions/label maps, form-value types, filter shapes, or route strings.

**Why:** a handwritten copy is a second source of truth that drifts the
moment the PHP changes — silently, because TypeScript still compiles
against the stale copy. Importing the generated type means a backend
change surfaces as a type error at the call site, where it can be fixed.

```ts
// Good — compose the generated contract
import type { App } from '@/types/generated'
export type VehicleListItem = App.Data.Vehicles.VehicleListItemData

// Bad — handwritten copy that will drift from PHP
type VehicleStatus = 'active' | 'inactive'
interface VehicleListItem { id: number; name: string; status: string }
```

If the generated symbol doesn't exist yet, the fix is to add/annotate the
PHP Data class and regenerate — **not** to handwrite a fallback. (A
scaffold may write the *import alias* ahead of generation, never a fallback
shape.)

## Rule: three type-ownership zones, no leakage between them

**1. Generated backend types** — imported from `@/types/generated`,
Laravel-owned truth. Page props, DTOs, form payloads, filters, enums,
capability/permission payloads, display/value DTOs.

**2. Feature-owned frontend types** — live beside the feature
(`features/<resource>/<resource>.types.ts`), which groups the resource's
**shared** aliases (a `*.types.ts` file is exempt from one-export-per-file).
Allowed: aliases that *compose* generated types, browser-only UI state,
component prop types that reference generated DTOs. Disallowed: handwritten
copies of any backend shape. **A page's props type is *not* here** — it is
declared locally in the page file as an alias of the generated `*PageData`
(see [../architecture/roles.md](../architecture/roles.md)); only types
shared across ≥2 files belong in `*.types.ts`.

**3. Shared frontend-only types** — `types/shared/*`. Must stay generic
(`SortDirection`, `Density`, `TableColumnState`). Never resource-specific
backend names (`VehicleStatus`, `InvoiceState`).

**Why:** the zones encode where truth lives. A backend domain name in
`types/shared` or a hand-copied DTO in a feature file means truth has been
forked; keeping each zone pure means the generated layer stays the single
authority and frontend types only ever *add* browser concerns on top.

```ts
// feature-owned: compose generated truth + add browser-only state
import type { App } from '@/types/generated'
export type VehicleListItem = App.Data.Vehicles.VehicleListItemData
export type VehicleSelectionState = { selectedIds: number[]; lastSelectedId: number | null }
```

## Rule: generated files are owned by generators

Never hand-edit anything under `types/generated/`, `actions/generated/`,
or `routes/generated/`. They carry a "do not edit" header and are
overwritten on regeneration. User-owned wrappers may import generated
helpers, but must not recreate route strings or method signatures.

**Why:** a manual edit to a generated file is erased on the next run and,
until then, masks drift. Wrap, don't edit.

## Rule: routes and actions come from Wayfinder

Use generated Wayfinder helpers for Inertia links, visits, forms, and
actions. Never handwrite a route URL, route name string, or controller
method contract.

```ts
// Good
import { store } from '@/actions/generated/App/Http/Controllers/VehicleController'
import { index } from '@/routes/generated/vehicles'

// Bad
router.post('/vehicles')
route('vehicles.store')
const url = `/vehicles/${id}`
```

**Why:** handwritten routes are backend-derived strings with no type
safety — they break invisibly when a route is renamed. Wayfinder output
breaks at compile time instead.

## Checklist

- No frontend file declares a backend-derived shape (page props, DTO copy,
  enum union/label map, form values, filters, route strings).
- Backend types are imported from `@/types/generated` and only *composed*
  in feature/shared files.
- `types/shared` holds generic concepts only — no resource/domain names.
- Generated files are never hand-edited.
- Routes/actions use Wayfinder helpers, never handwritten strings.
- A missing generated symbol is fixed in PHP + regeneration, not by a
  handwritten fallback.
