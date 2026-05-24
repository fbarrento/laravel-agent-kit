# Component roles

> **[Component](../../LANGUAGE.md)** (primitive / app / feature) is defined in `LANGUAGE.md`; this file owns the contracts.

Three component roles, each with a different contract. The role decides
what a component may know and what it must ship with.

| Role | Path | Knows about | Story |
|---|---|---|---|
| Primitive | `components/ui/*` | nothing domain-specific | required |
| App component | `components/app/*` | generic app concepts | required |
| Feature component | `features/<resource>/*` | one resource | when reusable/stateful |

## Rule: primitives own the design tokens and define the variants

`components/ui/*` are low-level, reusable, domain-free building blocks
(Button, Input, Badge) **and the only place that consumes `ds-` tokens
directly.** A primitive encapsulates each visual decision as a named
**variant** (`tone`, `variant`, `size`); consumers select appearance by
passing those props, never by writing `ds-` classes themselves (see the
appearance rule below). Layout primitives (e.g. a `Stack`, an `Inline`, a
`Grid`, a generic `Box`) are primitives too — they own the spacing scale and
emit the raw layout tags. **All markup lives here:** every raw HTML element the
app renders is emitted by a `components/ui` primitive; features, pages, and
layouts hand-write none (see the no-raw-HTML rule below). The primitive names
are illustrative — a project may spell them differently — but the boundary is
not. Requirements:

- colocated story (required);
- small typed public API; finite variant/size sets, all represented in the
  story;
- styling via `ds-` semantic utilities only — and this is the **only** role
  that writes them;
- state expressed through props and useful `data-*` attributes;
- **no** backend, resource, or domain concepts; **no** raw colors, inline
  hex, or primitive variables.

**Why:** a primitive is shared by the whole app, so any domain concept or raw
value in it contaminates everything downstream. Concentrating *all* token
usage here (via variants) is what makes a theme/brand swap a primitive-only
edit: nothing above `ui` references a token, so nothing above breaks.

```txt
components/ui/button.tsx
components/ui/button.stories.tsx
```

## Rule: app components are generic, token-free compositions

`components/app/*` are reusable product components above primitive level
(PageHeader, EmptyState, DataTable, FilterBar). They **compose primitives**
and accept generic data — and they do **not** write `ds-` tokens; appearance
comes from the variant props of the primitives they compose. Requirements:

- colocated story (required);
- **domain-free** — no resource-specific names or backend-specific
  assumptions. This is the *sole* bar for app membership: domain-free → here,
  domain-bound → a feature. Build a component here as soon as you judge it
  reusable, even with one consumer — promotion is **anticipatory**, not gated
  by a second use;
- composes `ui` primitives for all appearance; writes no `ds-` classes;
- generic generated/shared types allowed; resource-specific types belong in
  `features/<resource>`.

**Exception — framework-coupled styled components.** A component that needs
*both* a token-driven look *and* the Inertia router (a `NavLink` = a styled
`<Link>`) lives in `components/app`, and is the **one** place an app component
may use `ds-` tokens directly. Keeping Inertia out of `ui` outweighs token
purity here; everywhere else `app` stays token-free.

**Why:** the value of an app component is reuse across resources; the moment it
says "vehicle" it's a feature component in the wrong folder. Token-freeness
(bar that one exception) keeps the design tokens concentrated in `ui`.

## Rule: feature components own one resource's UI

`features/<resource>/*` own resource-specific workflow UI (VehicleTable,
VehicleForm, VehicleFilters). Requirements:

- use generated backend-derived types ([../types/generated.md](../types/generated.md));
- use typed local fixtures for stories
  ([../stories/conventions.md](../stories/conventions.md));
- get a story when reusable, stateful, visually important, exported, or
  likely to be edited by agents;
- if a component is **domain-free** (names no resource, reads the same for any
  resource), it doesn't belong here — build or promote it in `components/app`
  (anticipatory: as soon as it's reusable, not after a second use). A feature
  never imports another feature; cross-feature reuse goes through
  `components/app` (generify first) or page-level composition
  ([../architecture/roles.md](../architecture/roles.md)).

**Why:** resource UI is where domain knowledge legitimately lives; keeping
it in the feature folder (not in a primitive or app component) preserves
the reusability of the lower roles and keeps the resource's surface
together.

## Rule: appearance is variant props; arrangement is layout primitives

Two separate axes, two separate mechanisms — and **both** are owned by
primitives, so a feature/page/layout writes neither raw `ds-` classes nor raw
structural utilities:

- **Appearance** (color, intent, emphasis, size) is selected by passing a
  primitive's **variant props** — `<Badge tone="danger" variant="outlined">` —
  never by writing `ds-` classes on a consumer. If no existing variant fits,
  **add a variant to the primitive**; never inline a one-off `ds-` value in a
  feature/app/page.
- **Arrangement** (rows, stacks, grids, spacing between regions) uses the
  layout **primitives** — a vertical stack, a horizontal inline row, a grid, a
  generic box — selecting spacing/alignment through **their props**
  (`gap`/`align`/`cols`). A consumer does **not** hand-write `flex`/`grid`/
  `gap`/`items-*`/`justify-*` (or arbitraries like `grid-cols-[1fr_auto]`):
  those are arrangement decisions, and arrangement is the layout primitive's
  job. The only structural classes a consumer may pass are **positioning of
  the element within its parent** (margin, width, `col-span`) — the narrow
  `className` allow-list in [styling.md](styling.md).

```tsx
// Good — appearance via props, arrangement via a layout primitive's props
<Inline gap="3" align="center">
  <StatusPill tone="danger" variant="outlined" />
  <Text>{vehicle.name}</Text>
</Inline>

// Bad — appearance hand-styled, arrangement hand-rolled on a raw tag
<div className="flex items-center gap-3 ds-text-danger">{vehicle.name}</div>
```

**Why:** routing every visual decision through a primitive's variants is what
keeps tokens in `ui` (the theme-swap guarantee); routing every *arrangement*
decision through a layout primitive is what keeps structure consistent and
greppable instead of re-derived `flex`/`gap` strings scattered across pages.
Both axes collapse to the same boundary — markup, tokens, and layout all live
in `components/ui`, and nothing above it hand-writes HTML.

## Rule: features, pages, and layouts contain no raw HTML — only components

`resources/js/{features,pages,layouts}/**` render **components, not tags**.
A raw `<div>`, `<span>`, `<p>`, `<h1>`–`<h6>`, `<button>`, `<input>`, `<ul>`,
`<li>`, `<section>`, `<header>`, `<nav>`, `<main>` does not appear there — each
is emitted by a `components/ui` primitive instead. `components/ui` and the
design-system/token files are **out of scope**: primitives are where raw HTML
legitimately lives.

This is the same boundary as the token rule, widened from *styling* to *all
markup*: tokens, appearance, arrangement, **and the tags themselves** are
owned below the `ui` line. The reasons primitives own tokens (one place to
change, a typed/finite contract, a11y handled once) are exactly the reasons
they own the markup.

**A typical realization** (illustrative — a project may name and split these
differently; the boundary is the rule, the vocabulary is an example):

- generic container, padding/bg/radius/border via tokens → a `Box`;
- vertical / horizontal / grid arrangement → a `Stack` / `Inline` / `Grid`,
  spacing & alignment through props;
- the type scale → a `Heading` (owns the document outline: a required `level`
  drives the `h1`–`h6` tag, an independent `size` drives the visual scale) and
  a `Text` for non-outline copy (`body`/`label`/`caption` via `p`/`span`;
  never emits an `h*`);
- mono/tabular figures → a `Numeric` that stays **domain-free** — a generic
  `positive`/`negative` tone, not `gain`/`loss`; the domain meaning (which
  direction is "good") is applied by a wrapper **above** `ui`. (`Numeric` is
  the worked example of the no-domain-in-primitives clause above — not an
  exception to it.)
- semantic landmarks → a constrained, **typed** `as` on `Box` (a finite union,
  not `string`), with the a11y label part of the type so `nav`/`aside` *cannot
  compile* without an `aria-label` — a stronger guarantee than a lint;
- list semantics → a dedicated `List` / `ListItem` pair, so the `ul`→`li`
  parent–child contract is structural (TypeScript-checkable), not a loose
  `Box as="ul"`;
- existing primitives absorb the obvious cases: a raw `<button>` → `Button`,
  `<input>` → `Input`, a card/panel `<div>` → `Card`, an "eyebrow"/tag
  `<span>` → a `Badge` variant.

A backend-provided SVG injected via `dangerouslySetInnerHTML` (e.g. a 2FA QR)
is the documented exception — there is no component alternative.

**Enforcement.** A lint that forbids raw HTML tags in `features/pages/layouts`
(e.g. `react/forbid-elements`, scoped to exclude `components/ui` and stories)
**plus** a `className`-content check are both required: `forbid-elements`
alone cannot see through a polymorphic `as` (`<Box as="div" className="flex">`
is a laundered `<div className="flex">`), so the second check forbids
arrangement utilities (`flex`/`grid`/`gap-*`/`items-*`/`justify-*`/`grid-cols`)
in any `className` there ([styling.md](styling.md)). Without both, the "zero
raw tags" audit passes while scattered arrangement persists — the metric and
the intent diverge.

**Why:** one consistent, declarative composition layer above the `ui` line —
no per-file styling, arrangement, or tag decisions to drift. a11y (semantic
tags, labelled controls, list contracts) is handled once in the primitive that
owns the tag; restyling or re-tagging is a primitive-level edit, not a sweep
across every page.

## Decision: which role does this component belong to?

- Owns `ds-` tokens / defines a visual or layout primitive? → **primitive**
  (`components/ui`).
- Composes primitives, domain-free, token-free (or the `NavLink` exception)? →
  **app component** (`components/app`).
- Names or assumes a resource? → **feature** (`features/<resource>`).

The single discriminator between app and feature is **domain, not use-count**:
does it name or assume a resource? Yes → feature. No → app — build it there as
soon as it's reusable; you don't wait for a second consumer. A domain-bound
component that two features want is **generified** into an app component, never
shared feature-to-feature.

## Checklist

- Primitives: the only role that writes `ds-` tokens **and the only place raw
  HTML tags appear**; domain-free, finite typed variant/size API, colocated
  story. Layout primitives live here too.
- Features/pages/layouts render only components — no raw `<div>`/`<span>`/
  `<p>`/`<h*>`/`<button>`/`<ul>`/`<li>`/landmark tags (the `dangerouslySetInnerHTML`
  backend-SVG exception aside). Enforced by forbid-elements **plus** a
  `className`-content lint.
- App components: domain-free, **token-free** (compose primitives; appearance
  via variant props), no resource names, colocated story. Lone exception: a
  framework-coupled styled component (`NavLink`) may use `ds-` here.
- Feature components: generated types, typed fixtures, story when
  reusable/stateful. Domain-free UI is built in `components/app` instead
  (anticipatory); features never import each other.
- Appearance via variant props (add a variant if none fits — never inline
  `ds-`); arrangement via a layout primitive's props (never hand-written
  `flex`/`grid`/`gap` in a consumer). `className` in app code is limited to the
  positioning allow-list in [styling.md](styling.md).
- Role chosen via the Decision above (domain, not use-count), not by where the
  file was first dropped.
