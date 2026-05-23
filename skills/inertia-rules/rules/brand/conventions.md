# Brand OS boundary

Brand OS is upstream and separate. It *creates* the brand contract
(strategy, voice, logo, color/type/spacing rationale, neutral tokens). This
app *consumes* that contract: adapt its tokens into the `ds-` tier, render
through semantic utilities, and never let brand values or brand copy leak
into frontend code.

```txt
Brand OS  = defines the brand
this app  = consumes, adapts, and applies it behind ds- tokens
```

## Rule: never edit the upstream Brand OS project

Treat the Brand OS source as read-only. Copy, cache, or adapt its
consumable artifacts (`brand.json`, token JSON, theme CSS, approved
assets) into the app; do not modify the source.

**Why:** the brand is owned and versioned upstream. Editing it from a
consumer app forks the brand and breaks every other app that consumes it.

## Rule: adapt brand tokens into the `ds-` tiers — app never reads brand tokens directly

Brand OS raw values become app **primitive** tokens (`tokens.css`); brand
theme intent becomes **semantic** `--ds-*` tokens (`themes.css`); the app
generates the Tailwind **bridge**. App code consumes `bg-ds-surface`,
`text-ds-muted`, etc.

App code must **not**: import brand token JSON directly, hard-code brand
colors/fonts/radii/shadows, or reference raw brand token paths.

**Why:** routing the brand through the three-tier model
([../design-system/tokens.md](../design-system/tokens.md)) is what lets the
brand change values behind stable utilities — components and pages don't
change class names when the active brand changes. A direct brand-token
import re-couples components to a specific brand.

## Rule: Laravel still owns brand-influenced copy

Brand OS informs voice and messaging, but production copy, translation,
and locale-sensitive formatting still come from Laravel lang files and
backend Data DTOs ([../types/formatting.md](../types/formatting.md)).

Frontend code must not import Brand OS markdown/copy or construct
translation keys from brand terms. Brand voice rules may appear as review
references (in feedback), never as a frontend runtime dictionary.

**Why:** the brand guides *tone*; the backend still *delivers* the words.
A frontend brand-copy dictionary reintroduces exactly the formatting/
translation leak the backend-owned rule prevents — now with a brand label
on it.

## Rule: stories render with the active adapted brand

Storybook loads the same adapted `ds-` token layer and approved brand
assets the app uses, importing assets through app paths (not upstream
Brand OS paths).

**Why:** brand state is part of visual verification. A story rendered with
unbranded or stale tokens proves a component that doesn't match the
shipping brand.

## Checklist

- Brand OS source treated as read-only; only consumable artifacts copied
  in.
- Brand values reach the app only through the `ds-` token tiers; no direct
  brand-token imports or hard-coded brand values.
- Production copy/translation comes from Laravel, not Brand OS markdown;
  no frontend brand-copy dictionary.
- Stories render with the active adapted brand tokens and app-path assets.
