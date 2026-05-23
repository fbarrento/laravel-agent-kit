# Design-system tokens

A three-tier token model so brand/theme values change in one place and
component code never does. App code consumes semantic utilities; the
values behind them move freely.

```txt
tokens.css   Tier 1 — primitives: raw values only
themes.css   Tier 2 — semantic --ds-* tokens, mapped to primitives
bridge.css   Tier 3 — Tailwind v4 @theme inline bridge → ds- utilities
```

Import order:

```css
@import "tailwindcss";
@import "./tokens.css";
@import "./themes.css";
@import "./bridge.css";
```

## Tier 1: primitives — raw values, nowhere else

`tokens.css` holds raw color ramps, spacing/radius/type scales, shadows,
motion, z-index. No semantic meaning. **Raw hex and raw scale values are
allowed only here.** Components, pages, features, and stories must never
reference a primitive variable directly.

**Why:** primitives are the only sanctioned home for literal values, so a
literal anywhere else is provably a leak. If a value is missing, add a
primitive and map it through Tier 2 — never inline it at the call site.

## Tier 2: semantic tokens — named by intent, `--ds-*`

`themes.css` defines `--ds-*` variables named by *intent* and pointing at
primitives:

```css
:root {
  --ds-color-surface: var(--neutral-0);
  --ds-color-text-muted: var(--neutral-500);
  --ds-space-inset-md: var(--space-4);
  --ds-radius-control: var(--radius-2);
}
```

A theme remaps semantic tokens to different primitives; components don't
change because they consume semantic utilities. Default theme is `:root`.
Dark theme must work with both `[data-theme="dark"]` and `.dark` (shadcn
compatibility).

**Why:** intent names (`surface`, `text-muted`, `action`) are stable
across brands and themes; primitive names (`neutral-500`) are not.
Components bind to intent, so reskinning is a Tier-2 edit.

## Tier 3: Tailwind bridge — category-prefixed `ds`

`bridge.css` exposes semantic tokens as Tailwind v4 utilities via
`@theme inline`. Every bridge variable is `ds`-prefixed **inside its
Tailwind category**:

```css
@theme inline {
  --color-ds-surface: var(--ds-color-surface);
  --spacing-ds-inset-md: var(--ds-space-inset-md);
  --radius-ds-control: var(--ds-radius-control);
}
```

…which generates `bg-ds-surface`, `text-ds-muted`, `p-ds-inset-md`,
`rounded-ds-control`.

**Why the prefix is structural, not stylistic:** Tailwind turns the
segment *after the category* into the utility name, so
`--color-ds-surface` → `bg-ds-surface`. Naming it `--ds-color-surface`
would not generate `bg-ds-surface`. The `ds` prefix also prevents
collisions with shadcn or any other library's `@theme` block regardless
of import order — never declare the same `@theme` variable name in two
CSS files.

## Checklist

- Raw hex / raw scale values appear only in `tokens.css`.
- Semantic tokens are `--ds-*`, intent-named, and point to primitives.
- Bridge variables are category-prefixed (`--color-ds-*`, `--spacing-ds-*`,
  `--radius-ds-*`), never `--ds-color-*`.
- No `@theme` variable name is declared in more than one file.
- Import order is tailwindcss → tokens → themes → bridge.
- A missing value becomes a new primitive mapped through a semantic token,
  never an inline literal.
