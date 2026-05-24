# Component roles

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
appearance rule below). Layout primitives (`Stack`, `Grid`, `Row`) are
primitives too — they own the spacing scale. Requirements:

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

## Rule: appearance is variant props; arrangement is layout primitives + structural utilities

Two separate axes, two separate mechanisms:

- **Appearance** (color, intent, emphasis, size) is selected by passing a
  primitive's **variant props** — `<Badge tone="danger" variant="outlined">` —
  never by writing `ds-` classes on a consumer. If no existing variant fits,
  **add a variant to the primitive**; never inline a one-off `ds-` value in a
  feature/app/page.
- **Arrangement** (rows, stacks, grids, spacing between regions) uses the
  layout **primitives** (`Stack`/`Grid`/`Row`) for the common cases, with raw
  **structural** utilities (`flex`, `grid`, `gap`, sizing) as an escape for
  one-off layouts — including structural arbitrary values like
  `grid-cols-[1fr_auto]`. Structural utilities are *not* `ds-` tokens, so they
  are allowed outside `ui` ([styling.md](styling.md)).

```tsx
// Good — appearance via props, arrangement via layout + structural utility
<Stack direction="row" gap="3" align="center">
  <StatusPill tone="danger" variant="outlined" />
  <Text>{vehicle.name}</Text>
</Stack>

// Bad — appearance hand-styled with ds- classes in a feature
<div className="ds-text-danger ds-rounded-control">{vehicle.name}</div>
```

**Why:** routing every visual decision through a primitive's variants is what
keeps tokens in `ui` (the theme-swap guarantee). Splitting arrangement off as
a separate, token-free axis lets layout be expressed freely without leaking
design tokens upward.

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

- Primitives: the only role that writes `ds-` tokens; domain-free, finite
  typed variant/size API, colocated story. Layout primitives live here too.
- App components: domain-free, **token-free** (compose primitives; appearance
  via variant props), no resource names, colocated story. Lone exception: a
  framework-coupled styled component (`NavLink`) may use `ds-` here.
- Feature components: generated types, typed fixtures, story when
  reusable/stateful. Domain-free UI is built in `components/app` instead
  (anticipatory); features never import each other.
- Appearance via variant props (add a variant if none fits — never inline
  `ds-`); arrangement via layout primitives + structural utilities.
- Role chosen via the Decision above (domain, not use-count), not by where the
  file was first dropped.
