# Audit self-check

The convention-violation catalog to check your own changes against before
[verification](../verification/conventions.md) and handoff. Until the
`iak audit` command exists, this is a manual checklist (much of it is
greppable). Each item links to the rule that owns it.

Scan `resources/js` (and `resources/css`); skip `vendor`, `node_modules`,
`public/build`, and generated folders.

## Page & role violations → [../architecture/roles.md](../architecture/roles.md)

- A page declares a **handwritten** prop *shape* inline, or uses
  `any`/`unknown`/broad records for props. (A page declaring its props as
  a local alias of the generated `*PageData` is **required**, not a
  violation — see [../architecture/roles.md](../architecture/roles.md).)
- A runtime module (component/hook) exports more than one symbol — one
  export per file; `*.types.ts` may group type aliases.
- A page implements a table, list, grid, or form directly instead of
  composing a feature component.
- A page defines a layout shell inline or exports a reusable component.
- A feature imports a page module or a page-owned type.
- A domain/resource concept appears in a `components/ui/*` primitive.
- A resource-specific name appears in a `components/app/*` component.
- A new top-level `queries/`, `forms/`, or `composables/` folder exists
  (non-generated), or a **resource** hook sits in the global `hooks/` tier
  (which is for *generic* hooks only — [../architecture/roles.md](../architecture/roles.md)).

## Type violations → [../types/generated.md](../types/generated.md)

- A frontend file declares a backend-derived shape inline (page props, DTO
  copy, enum union/label map, form values, filters).
- `types/shared/*` contains a resource-specific backend name.
- A generated file under `types/generated`, `actions/generated`, or
  `routes/generated` was hand-edited.
- A route URL / route name string / controller action was handwritten
  instead of using Wayfinder.

## Formatting violations → [../types/formatting.md](../types/formatting.md)

- `Intl.NumberFormat`/`Intl.DateTimeFormat` or a date library formats
  user-facing text in a render path.
- A hard-coded enum label map, validation message, or frontend i18n
  dictionary appears in frontend code.

## Design-system violations → [../design-system/styling.md](../design-system/styling.md)

- Raw hex outside `tokens.css`.
- Arbitrary Tailwind value (`p-[34px]`, `bg-[#fff]`) outside token files.
- Primitive color utility (`bg-blue-500`, `text-slate-700`) in app/story
  code.
- Direct primitive CSS variable (`var(--neutral-500)`) outside
  token/theme files.
- Duplicate `@theme` variable name across CSS files, or a bridge variable
  not category-prefixed (`--color-ds-*`).

## Story violations → [../stories/conventions.md](../stories/conventions.md)

- A `components/ui/*` or `components/app/*` component without a colocated
  story.
- A story missing `Default`, or missing an applicable required state.
- A story/fixture with an inline backend-shaped blob or `any` where a
  generated type exists.

## How to use this

For each touched file, walk the relevant section above. Treat the first
four sections as **errors** (fix before handoff) and story-state coverage
as the bar your project has chosen. Record the result as the audit step of
[verification](../verification/conventions.md), and cite specific
file:line when reporting a violation so the fix is unambiguous.

**Why a manual catalog now:** the rules are stable even though the
tooling isn't. A grep-and-eyeball pass against this list catches the
drift the future `iak audit` will automate, and keeps handoffs honest in
the meantime.

## Checklist

- Each touched file checked against page/role, type, formatting,
  design-system, and story sections.
- Error-level violations fixed, not deferred.
- Findings reported with file:line and the owning rule.
- Result recorded as the audit step of verification.
