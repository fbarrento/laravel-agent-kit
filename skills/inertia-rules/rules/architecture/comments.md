# Comments

Settled, codebase-wide policy for when a comment earns its place in
`resources/js`. The default is none: names, TypeScript types, the generated
backend-derived types, and design tokens carry the meaning.

## Rule: comment the non-obvious WHY, never restate the code

Make the code say what it does — through component and variable names, the
prop types, the backend-derived types, and the design-system tokens. A comment
is justified only when it records a **why** the code cannot express: a
workaround for a browser/library bug, a non-obvious UX trade-off, a deliberate
deviation from a rule file, a link to a decision record. A comment that
restates what the JSX, the type, or the token already says is noise — delete
it and let the code speak.

**Why:** a comment that paraphrases the line beside it is a second source of
truth that drifts the moment the component changes, and a reader who catches
one stale comment stops trusting all of them. The prop type already states the
shape; the token name already states the intent; the component name already
states the role. Narrating them in prose adds nothing and rots.

```tsx
// Bad — restates what the type, the name, and the token already say
interface Props {
  // The optional buy-target: the price the user intends to buy at,
  // formatted by the backend as a money string. Undefined means no
  // target is set, a distinct state, so the prop is optional.
  buyTarget?: string
}

// the wrapper div uses the surface token for the card background
<div className="bg-[--ds-surface]">

// Good — the optional type, the field name, and the token carry all of it
interface Props {
  buyTarget?: string
}

<div className="bg-[--ds-surface]">
```

`buyTarget?: string` already says "optional, formatted string"; `--ds-surface`
already says "surface background". The narration adds a maintenance liability,
not information.

## Edge cases

- **A genuine non-obvious why** — a workaround for a browser quirk, a
  deliberate a11y or UX trade-off, a deviation from a rule file — keep a short
  comment stating the why and linking its source. This is the comment that
  earns its place.
- **The "why" is really a missing name** — extract a named component, hook, or
  `const` instead of commenting. A `<BuyTargetField>` or a `useBuyTarget()`
  beats a paragraph explaining a block of JSX.
- **JSDoc the type system cannot express** — a generic component's contract, a
  non-obvious prop unit — keep; it is type/contract information, not narration.
- **Shared `components/ui` / `components/app` public props** other features
  consume — a short docblock documenting the contract is allowed; internals
  are not.

## Checklist

- No comment restates what a name, type, prop, or token already says.
- Every surviving comment records a *why* the code cannot express, not a
  *what*.
- A comment that exists only because a name is unclear is replaced by a better
  name, extracted component, or hook — not kept.
- JSDoc is limited to contract/type information the type system cannot carry.
