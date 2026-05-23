# Styling rules for agents

Style through semantic `ds-` utilities and reusable components — never raw
values. This is what makes a theme/brand swap a token edit instead of a
find-and-replace across the app.

## Rule: semantic utilities for design decisions; raw scale only for layout

Use `ds-` utilities for every design-system decision: color, component
spacing, radius, focus, intent. Plain Tailwind scale utilities are allowed
**only** for layout sizing/positioning that is not a design-system
decision (grid, fl, width, gap *between layout regions*).

Allowed:

```txt
bg-ds-surface  text-ds-default  text-ds-muted  border-ds-border-default
p-ds-inset-md  gap-ds-stack-sm  rounded-ds-control
```

Disallowed outside token/theme files:

```txt
bg-[#ffffff]   text-slate-700   bg-blue-500   p-[34px]   rounded-[11px]
style={{ color: '#fff' }}        var(--neutral-500)
```

**Why:** a raw color or arbitrary value is a design decision frozen at the
call site — it ignores the token system, breaks under theming, and can't
be audited. `ds-` utilities route every visual decision through Tier 2,
where it's named and swappable.

## The styling decision procedure

1. **Reuse** an existing primitive or app component if one already matches.
2. **Use a `ds-` semantic utility** for color, spacing, radius, focus, and
   intent-driven visuals.
3. **Use a plain Tailwind scale utility** only for layout sizing/position
   that isn't a design-system decision.
4. **No fit?** Propose a token-contract change (add a primitive + semantic
   token + bridge variable) — do not inline a one-off value.

**Why:** the order forces reuse before invention and a token change before
a literal. Most "I need a new value" moments are really "I haven't checked
the existing tokens" moments; step 4 keeps genuinely new values inside the
system.

## Rule: stories and fixtures obey the same styling rules

Story files and fixtures are not an exception. Story-only raw colors,
arbitrary spacing, or primitive variable references are violations too.

**Why:** stories are the design-system's own showroom; a raw value there
both ships (Storybook renders it) and teaches the wrong pattern by
example.

## Checklist

- Design decisions (color/spacing/radius/focus/intent) use `ds-`
  utilities.
- No raw hex, arbitrary values (`p-[34px]`), primitive color utilities
  (`bg-blue-500`), inline color styles, or direct `var(--primitive)` in
  app/story code.
- Plain scale utilities used only for non-design-system layout.
- A genuinely missing value became a token-contract change, not an inline
  literal.
- Stories/fixtures follow the same rules as production components.
