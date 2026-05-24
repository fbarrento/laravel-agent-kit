# Generated backend-derived types

> **[Generated type](../../LANGUAGE.md)** is defined in `LANGUAGE.md` (the frontend face of a backend Data object, owned by laravel-rules); this file owns the grammar.

PHP is the source of truth for every backend-derived shape: page props,
DTOs, enums, form payloads, filters, validation field names, capability
flags, and routes/actions. The frontend **imports** these contracts; it
never reinvents them.

Default stack:
- **Spatie Laravel Data** — page props, DTOs, form data, filters,
  display/value shapes, copy payloads.
- **`spatie/laravel-typescript-transformer`** — TypeScript output from
  those Data classes and PHP enums, emitted by `FlatModuleWriter` as a
  single importable module (see the lifecycle rule below).
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
// Good — import the generated contract by name
import type { VehicleListItemData } from '@/types/generated'
export type VehicleListItem = VehicleListItemData   // alias for intent (optional)

// Bad — handwritten copy that will drift from PHP
type VehicleStatus = 'active' | 'inactive'
interface VehicleListItem { id: number; name: string; status: string }
```

If the generated symbol doesn't exist yet, the fix is to add/annotate the
PHP Data class and regenerate — **not** to handwrite a fallback. (A
scaffold may write the *import* ahead of generation, never a fallback
shape.)

## Rule: never re-narrow a generated type on the frontend — fix the PHP type

If a generated type is too loose — `value: string` where the value is
really an enum — do **not** add a frontend alias that narrows it
(`value as TeamRole`, or a re-typed copy). Narrow it **in PHP**: type the
Data property as the enum or a precise Data class (`RoleData { value:
TeamRole }`, not `LabeledValue { value: string }`), and the generated type
narrows at the source (laravel-rules `data-objects/spatie-laravel-data` —
type Data properties precisely).

**Why:** a frontend narrowing alias is just a handwritten backend type
wearing a cast — the same drift hole as any hand-copied shape, and it lies
to the compiler. The narrowing belongs where the contract is defined.

## Rule: three type-ownership zones, no leakage between them

**1. Generated backend types** — imported by name from `@/types/generated`,
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

**The operative test for "may I handwrite this?"** is whether an
`app/Data/*` (or PHP enum) source exists. If a Data class backs the shape →
import the generated type (zones 1–2). Handwrite **only** what has *no* PHP
Data source: an Eloquent model not yet projected to a Data object
(`types/auth.ts`'s `User`), a third-party block (Fortify/passkeys), or a
purely frontend concept (navigation, UI state — zone 3). Anything with a
Data source is referenced from `@/types/generated`, never re-declared.

**Why:** the zones encode where truth lives. A backend domain name in
`types/shared` or a hand-copied DTO in a feature file means truth has been
forked; keeping each zone pure means the generated layer stays the single
authority and frontend types only ever *add* browser concerns on top.

```ts
// feature-owned: compose generated truth + add browser-only state
import type { VehicleListItemData } from '@/types/generated'
export type VehicleListItem = VehicleListItemData
export type VehicleSelectionState = { selectedIds: number[]; lastSelectedId: number | null }
```

## Rule: a page's prop type is one composed `*PageData`

Every page declares exactly **one** prop type — the generated `<Page>PageData` —
which composes the page's data DTOs plus `can` (`*PageAuthorizationData`), `copy`
(`*PageCopyData`), and `seo` (`PageSeoData`). Import that single type by name;
never declare separate prop interfaces per concern. The composition and
`<Page><Concern>Data` naming are owned by laravel-rules
`data-objects/inertia-page-data`; on the frontend it is simply the one generated
type the page imports.

```ts
import type { TeamsIndexPageData } from '@/types/generated'
type Props = TeamsIndexPageData   // the only prop type the page declares
```

**Why:** one composed contract per page means one generated type to import and one
place a backend change surfaces — instead of N concern props that drift
independently.

## Rule: generated artifacts are gitignored and regenerated, never committed or hand-edited

The generated TypeScript is a **single module file**
`resources/js/types/generated.ts` (imported as `@/types/generated`), emitted by
the transformer's `FlatModuleWriter`. It — like the Wayfinder output under
`resources/js/{actions,routes}` — is **gitignored, never committed, never
hand-edited**, and regenerated by a Vite plugin on dev-server start, on build, and
on changes to `app/Data|Enums|Models` (mirroring how Wayfinder regenerates). A
user-owned wrapper may import generated symbols, never recreate them.

**Generation must run before any type-aware tool.** `tsc`, type-aware ESLint, and
CI all need the file present, so generation is wired ahead of them
(`predev`/`prebuild` hooks, `composer ci:check`, and the lint CI step each generate
first). A fresh checkout has **no** generated types until the first generate runs —
an expected, documented state, not a failure.

**Why:** committing the artifact invites churn, merge conflicts, and
stale-but-green drift; gitignoring + regenerating makes PHP the only source and the
types always fresh — the same lifecycle the project already uses for Wayfinder. A
hand-edit is erased on the next run and, until then, masks drift.

## Rule: routes and actions come from Wayfinder

Use generated Wayfinder helpers for Inertia links, visits, forms, and
actions. Never handwrite a route URL, route name string, or controller
method contract.

```ts
// Good
import { store } from '@/actions/App/Http/Controllers/VehicleController'
import { index } from '@/routes/vehicles'

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
- Backend types are imported by name from `@/types/generated` and only
  *composed* in feature/shared files; no `App.Data.X` ambient access.
- A too-loose generated type is fixed in the PHP Data class, never
  re-narrowed by a frontend alias.
- Handwrite only shapes with **no** `app/Data/*` source (un-projected
  Eloquent model, third-party block, frontend-only concept).
- `types/shared` holds generic concepts only — no resource/domain names.
- A page declares one prop type — the generated `*PageData` (`can`/`copy`/`seo`) —
  not separate per-concern interfaces (laravel-rules `data-objects/inertia-page-data`).
- The generated artifact is gitignored + Vite-regenerated (like Wayfinder),
  never committed or hand-edited; generation runs before `tsc`/ESLint/CI.
- Routes/actions use Wayfinder helpers, never handwritten strings.
- A missing generated symbol is fixed in PHP + regeneration, not by a
  handwritten fallback.
