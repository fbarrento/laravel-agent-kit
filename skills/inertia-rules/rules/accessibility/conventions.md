# Accessibility

Accessibility is a build-time convention, not a verify-time afterthought.
Most of it is free if the markup is semantic and primitives carry the
right affordances; the audit/verify a11y check
([../verification/conventions.md](../verification/conventions.md)) is the
backstop, not the strategy.

## The conformance target: WCAG 2.2 AA

These rules sum to **WCAG 2.2 AA** — treat that as the bar they aim at (2.1 AA
is the floor most laws still cite). Where a legal obligation applies — the **EU
Accessibility Act** (Directive 2019/882, via `EN 301 549`), the **ADA** or
**Section 508** (US) — it sets, and can raise, the required level. **Confirm the
project's jurisdiction and target level**; default to 2.2 AA when unspecified.

**"Compliance" is not something the agent certifies.** WCAG conformance is not
machine-verifiable: you *build to* the standard via the rules below, and the
automated axe gate ("Running the automated check") is a **partial backstop** —
DOM-level only (~57% of criteria). Keyboard operability, focus order,
screen-reader semantics, and cognitive criteria are covered by the build-time
rules plus **human testing** (a real screen reader, keyboard-only, 200% zoom). An
agent reports "built to WCAG 2.2 AA; axe gate green; manual checks {done/skipped}"
— never a bare "WCAG compliant."

## Rule: semantic HTML first

Use the element that means what you intend: `<button>` for actions,
`<Link>`/`<a>` for navigation, `<label>` bound to inputs, real headings in
order, `<ul>/<table>` for lists/tables. Don't build interactive controls
from `<div>`/`<span>` + click handlers.

**Why:** native elements come with focusability, keyboard behavior, and
the right role/announcement for free; a `<div onClick>` has none and must
re-implement all of it (and usually doesn't). Semantic markup is the
cheapest accessibility you'll ever get. (A click-handler `<div>` is also a
navigation/role smell — actions are `<button>`, navigation is `<Link>`,
[../navigation/conventions.md](../navigation/conventions.md).)

## Rule: form fields are labelled and errors are associated

Every input has an associated `<label>`; each field's error message is
linked with `aria-describedby` and the field marked `aria-invalid` when it
has an error. On a failed submit, move focus to the first invalid field.

**Why:** an unlabelled field is unusable with a screen reader, and an
error that's only a red line near the input is invisible to assistive tech
and to colorblind users. Associating the error and focusing it is what
makes the server-owned validation ([../forms/conventions.md](../forms/conventions.md))
actually reach everyone.

## Rule: everything operable by keyboard; manage focus on navigation

All interactive elements are reachable and operable by keyboard in a
sensible order. Move focus deliberately when context changes: into an
opened dialog (and trap it), back to the trigger on close, and to a
sensible target after an Inertia visit.

**Why:** keyboard operability is the foundation most other a11y depends
on, and SPA-style visits don't reset focus the way full page loads do — so
without explicit focus management, keyboard and screen-reader users get
stranded after navigation.

## Rule: primitives own their a11y affordances

Accessibility behavior — focus-visible rings (via `ds-` focus tokens),
`aria-*` state, disabled semantics, roles — lives in the
`components/ui/*` primitive, exposed through props/state
([../design-system/components.md](../design-system/components.md)). Feature
and page code shouldn't re-implement it.

**Why:** putting a11y in the primitive means every use of `Button`/`Input`
is accessible by construction; scattering it across call sites guarantees
some get it wrong. Same leverage as token-bound styling.

## Rule: never rely on color alone; respect contrast and motion

Convey state with text/icon/shape in addition to color (semantic `ds-`
tokens should meet contrast). Honor `prefers-reduced-motion` for
animation. **Colored status text** (gain/loss/alert) is especially
contrast-sensitive: keep it at large sizes and on a neutral `ds-surface`,
never small or set on a colored swatch — a constraint the foundation token
pages must meet ([../stories/conventions.md](../stories/conventions.md)),
and one the headless a11y gate will fail.

**Why:** color-only state excludes colorblind and low-vision users, and
unbounded motion harms users with vestibular sensitivity. Both are common
and cheap to respect.

## Running the automated check (Storybook)

The concrete CI gate an agent can run: **`@storybook/addon-a11y`**
(axe-core) executed headlessly through **`@storybook/addon-vitest`**
(`vitest`) or **`@storybook/test-runner`** (`storybook test`). Set
`parameters.a11y.test: 'error'` so violations **fail the run**; stories
are enumerable from the build's `/index.json`.

```ts
// .storybook/preview.ts (or per-story parameters)
export const parameters = { a11y: { test: 'error' } }
```

Two limits to remember:
- It returns **pass/fail (exit code)**, not a per-violation JSON — the
  detailed breakdown is in the Storybook a11y panel. For structured output
  in CI, add a custom test-runner `postVisit` axe hook.
- axe is **DOM auditing (~57% of WCAG)** — it catches labels/contrast/ARIA
  but **not** keyboard operability, focus order, or screen-reader
  semantics. So this gate is a **backstop**; the rules above are the
  strategy. (Routes use axe via the browser executor instead — see
  [../verification/conventions.md](../verification/conventions.md).)

## Checklist

- Semantic elements for actions/navigation/labels/headings/lists; no
  `<div onClick>` controls.
- Inputs labelled; errors associated (`aria-describedby`, `aria-invalid`);
  focus moves to the first invalid field on submit.
- Full keyboard operability; focus managed into/out of dialogs and after
  visits.
- A11y affordances (focus ring, `aria-*`, roles) live in primitives.
- State not conveyed by color alone; contrast met; reduced-motion
  respected. Colored status text kept large and on `ds-surface`, not on a
  colored swatch.
- The verify a11y check is a backstop, not the only line of defense.
- Built to the **WCAG 2.2 AA** bar; project's legal level/jurisdiction (EAA/ADA/
  508) confirmed. "Compliance" = build-to-standard + axe backstop + human testing,
  never an agent certification.
