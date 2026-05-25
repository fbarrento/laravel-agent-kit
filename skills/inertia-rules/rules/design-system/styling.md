# Styling rules for agents

Style by composing primitives and passing their variant props — `ds-` tokens
live inside primitives, never at the call site. This is what makes a
theme/brand swap a primitive-only edit instead of a find-and-replace across
the app.

## Rule: `ds-` tokens live in primitives; everyone else passes variant props

`ds-` semantic utilities (color, component spacing, radius, focus, intent) are
written in **one place only: `components/ui` primitives**, where each is
encapsulated as a named variant ([components.md](components.md)). Features, app
components, and pages do **not** write `ds-` classes — they get appearance by
**passing a primitive's variant props** (`<Badge tone="danger">`), and reach
for a primitive (or add a variant to one) when none fits.

**Arrangement** (`flex`/`grid`/`gap`/alignment between regions, including
arbitraries like `grid-cols-[1fr_auto]`) is **also** owned by primitives — the
layout primitives (a `Stack`/`Inline`/`Grid`/`Box`, by whatever names a project
gives them). A feature/app/page selects layout through **their props**
(`gap`/`align`/`cols`), it does not hand-write structural utilities. The only
structural classes a consumer may pass via `className` are **positioning of the
element within its parent** — see the allow-list below.

Written in primitives only (`components/ui`):

```txt
bg-ds-surface  text-ds-default  text-ds-muted  border-ds-border-default
p-ds-inset-md  gap-ds-stack-sm  rounded-ds-control
flex  grid  items-center  gap-3  grid-cols-[1fr_auto]   ← arrangement, also primitives-only
```

The **only** `className` allowed in features/pages/layouts — positioning of the
element within its parent, never arrangement of its children:

```txt
m-*  mt-*/mb-*/mx-*/my-*   w-*/max-w-*/min-w-*   col-span-*/row-span-*
self-*  order-*  flex-1/grow/shrink
```

Disallowed everywhere outside token/theme files:

```txt
bg-[#ffffff]   text-slate-700   bg-blue-500   p-[34px]   rounded-[11px]
style={{ color: '#fff' }}        var(--neutral-500)
```

And disallowed *outside `components/ui`*: any `ds-` **visual** utility *and* any
**arrangement** utility (`flex`/`grid`/`gap-*`/`items-*`/`justify-*`/`grid-cols`)
— pass a variant prop or use a layout primitive instead. The one exception is a
framework-coupled styled component (`NavLink`) in `components/app`, which may
use `ds-` directly ([components.md](components.md)).

**Why:** a raw color or visual arbitrary value is a design decision frozen at
the call site — it ignores the token system and breaks under theming. A `ds-`
class scattered across features defeats the same goal more subtly: the token is
used correctly but in dozens of places, so a variant change becomes a
find-and-replace. Hand-written arrangement is the same failure for structure:
`flex items-center gap-3` re-derived in fifty files is fifty places to change a
row's spacing. Concentrating both token usage *and* layout in primitives makes
every visual and structural decision named, swappable, and changed in one file.

> **Changed (was permissive).** Earlier revisions of this rule allowed raw
> structural utilities (`<div className="flex gap-3">`) everywhere as a one-off
> escape. They are now arrangement decisions owned by layout primitives;
> hand-writing them in features/pages/layouts is a violation. A vendored copy on
> the old rule will start flagging them once this update is pulled — migrate the
> raw arrangement to layout primitives.

## The styling decision procedure

1. **Reuse / compose** an existing primitive or app component.
2. **Need a different look?** Pass the primitive's **variant props**
   (`tone`/`variant`/`size`) — don't reach for `ds-` classes.
3. **Variant missing?** **Add a variant to the primitive** (a token-contract
   change *there*), never inline a `ds-` value at the call site.
4. **Arranging primitives?** Use a layout primitive and pass its
   `gap`/`align`/`cols` props — never hand-write `flex`/`grid`/`gap` in a
   consumer. If the layout primitives can't express it, that's a missing prop
   on a primitive, not a `className` escape.

**Why:** the order forces reuse before invention and a primitive change before
a literal. Most "I need a new value" moments are really "I haven't checked the
existing variants" moments; steps 2–3 keep every genuinely new look inside the
primitive that owns the token.

## Rule: stories and fixtures obey the same styling rules

Story files and fixtures are not an exception. Story-only raw colors,
arbitrary spacing, or primitive variable references are violations too.

**Why:** stories are the design-system's own showroom; a raw value there
both ships (Storybook renders it) and teaches the wrong pattern by
example.

## Checklist

- `ds-` visual utilities appear only in `components/ui` primitives (as
  variants); features/app/pages pass variant props and write no `ds-` classes
  (lone exception: a `NavLink` in `components/app`).
- No raw hex, visual arbitrary values (`p-[34px]`, `rounded-[11px]`), primitive
  color utilities (`bg-blue-500`), inline color styles, or `var(--primitive)`
  anywhere outside token/theme files.
- Arrangement utilities (`flex`/`grid`/`gap`/`items-*`/`justify-*`/`grid-cols`,
  incl. arbitraries like `grid-cols-[1fr_auto]`) appear only in
  `components/ui` layout primitives; consumers select layout via props.
  `className` in features/pages/layouts is limited to the positioning
  allow-list (`m*`/`w*`/`col-span*`/`self-*`/`order-*`/`flex-1|grow|shrink`).
- A missing look became a new primitive **variant** (token-contract change),
  not an inline literal or a `ds-` class in a feature.
- Stories/fixtures follow the same rules as production components.
