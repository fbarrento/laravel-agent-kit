# Accessibility

Accessibility is a build-time convention, not a verify-time afterthought.
Most of it is free if the markup is semantic and primitives carry the
right affordances; the audit/verify a11y check
([../verification/conventions.md](../verification/conventions.md)) is the
backstop, not the strategy.

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
animation.

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
  respected.
- The verify a11y check is a backstop, not the only line of defense.
