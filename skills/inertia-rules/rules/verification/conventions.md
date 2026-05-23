# Verification

Before handing off UI work, prove the change with evidence, not
assertion. Verification answers one question: *is this change backed by
enough evidence to hand off safely?* Until the `iak verify` orchestrator
exists, you run these steps by hand with the tools that do.

## Rule: run the full gate, in order, before handoff

1. **Audit self-check** — the convention catalog in
   [../audit/conventions.md](../audit/conventions.md) (roles, types,
   formatting, design-system, stories).
2. **Typecheck + lint** — the project's configured commands.
3. **Stories** — for changed reusable UI, run the stories **headlessly**
   (`@storybook/addon-vitest` via `vitest`, or `@storybook/test-runner`
   via `storybook test`): required states present, `play` interactions
   pass, and **accessibility green** (`@storybook/addon-a11y` / axe-core)
   when `parameters.a11y.test: 'error'`. Enumerate stories from the
   build's `/index.json`. ([../stories/conventions.md](../stories/conventions.md))
4. **Browser** — for route-visible changes, **Pest Browser** (preferred
   for Laravel routes) or **Playwright**, against the real route.
5. **Inspect the rendered outcome** — capture a screenshot, check the
   console for errors, run accessibility checks (axe via the browser
   executor for routes; `@storybook/addon-a11y` for stories). These
   produce **pass/fail** (exit code), not a per-violation JSON unless you
   add a custom axe reporter.
6. **Feedback** — no related feedback left unresolved
   ([../feedback/conventions.md](../feedback/conventions.md)).

**Why:** the order goes cheap-to-expensive and static-to-rendered. The
last steps — actually opening the page and reading the console — are the
ones that catch what typechecking can't, and the ones agents skip. A
"passed" claim without a rendered-outcome inspection is not verification.

## Rule: a Storybook pass is component evidence, not route evidence

A passing story proves a component's state contract. It does **not** prove
the Laravel route renders, sends the right props, authorizes, validates,
or redirects. Route-visible changes still need app-page browser evidence.

**Why:** Storybook renders the component with fixtures you control; only a
browser test against the route proves the backend actually delivers those
props. Conflating the two ships a component that works in isolation and
breaks on the page.

## Rule: browser-visible changes require artifact-backed inspection

A change to a routed page or a reusable component's visible state isn't
verified without: a screenshot of the inspected URL/story, a console
result (zero unallowlisted errors), and an accessibility result when a
runner is available.

**Why:** the screenshot and console are the difference between "I believe
it renders" and "it rendered, here's the proof." Console errors in
particular pass typecheck and fail users.

## Rule: don't fake evidence

If a step can't run (no browser runner installed, route unreachable),
record it as **skipped with a reason** — never as passed. A skipped
required step means the work isn't ready for a clean handoff.

**Why:** a skipped-as-passed step is a lie that propagates into the
handoff and the feedback resolution. An honest "skipped: no Pest Browser
configured" lets the next person decide; a false "passed" doesn't.

## Checklist

- Audit self-check, typecheck, and lint run and clean.
- Changed reusable UI verified in Storybook with required states present.
- Route-visible changes verified in the browser against the real route.
- Screenshot captured, console clean (no unallowlisted errors), a11y run
  when available.
- No related feedback left unresolved.
- Steps that couldn't run are marked skipped-with-reason, never passed.
