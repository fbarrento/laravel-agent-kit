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

Plain Tailwind **structural** utilities — `flex`, `grid`, `gap` between
regions, width/height, position — are allowed everywhere for
**layout/arrangement** that isn't a design decision, including structural
arbitrary values (`grid-cols-[1fr_auto]`). Common arrangements should prefer
the layout primitives (`Stack`/`Grid`).

Written in primitives only (`components/ui`):

```txt
bg-ds-surface  text-ds-default  text-ds-muted  border-ds-border-default
p-ds-inset-md  gap-ds-stack-sm  rounded-ds-control
```

Allowed everywhere (structural, not a design decision):

```txt
flex  grid  items-center  gap-3  w-full  grid-cols-[1fr_auto]
```

Disallowed everywhere outside token/theme files:

```txt
bg-[#ffffff]   text-slate-700   bg-blue-500   p-[34px]   rounded-[11px]
style={{ color: '#fff' }}        var(--neutral-500)
```

And disallowed *outside `components/ui`*: any `ds-` **visual** utility — pass a
variant prop instead. The one exception is a framework-coupled styled
component (`NavLink`) in `components/app`, which may use `ds-` directly
([components.md](components.md)).

**Why:** a raw color or visual arbitrary value is a design decision frozen at
the call site — it ignores the token system and breaks under theming. A `ds-`
class scattered across features defeats the same goal more subtly: the token is
used correctly but in dozens of places, so a variant change becomes a
find-and-replace. Concentrating token usage in primitive variants makes every
visual decision named, swappable, and changed in one file.

## The styling decision procedure

1. **Reuse / compose** an existing primitive or app component.
2. **Need a different look?** Pass the primitive's **variant props**
   (`tone`/`variant`/`size`) — don't reach for `ds-` classes.
3. **Variant missing?** **Add a variant to the primitive** (a token-contract
   change *there*), never inline a `ds-` value at the call site.
4. **Arranging primitives?** Use a layout primitive (`Stack`/`Grid`), or plain
   structural utilities for one-off layout.

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
- Structural utilities (`flex`/`grid`/`gap`/sizing, incl. structural
  arbitraries like `grid-cols-[1fr_auto]`) used only for arrangement; common
  layouts prefer `Stack`/`Grid` primitives.
- A missing look became a new primitive **variant** (token-contract change),
  not an inline literal or a `ds-` class in a feature.
- Stories/fixtures follow the same rules as production components.
