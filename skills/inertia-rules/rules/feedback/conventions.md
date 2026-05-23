# Human-in-the-loop feedback

When a human (or a test, or you) flags something about the UI, it is a
piece of feedback that must be resolved with **evidence**, not closed with
prose. This file is the discipline; the eventual `iak` feedback store and
queue are implementation that doesn't change the rule.

A feedback item carries: the surface it came from (`app`, `storybook`, or
`test`), what it points at (route/URL, story id, selector or coordinates),
a message, and any captured artifacts (screenshot, DOM, console).

## Rule: never resolve feedback with prose alone

Closing a feedback item requires a resolution that includes:

- a short summary of what changed;
- the changed files (grouped by role);
- the checks you ran and their result (typecheck, the
  [audit](../audit/conventions.md) self-check, tests);
- a **post-fix screenshot** when the feedback is about app or Storybook
  UI;
- a Storybook story result when resolving Storybook feedback, and an
  app-page result when the fix affects routed behavior.

**Why:** "fixed" without evidence is the single most common false claim in
UI work. Requiring a post-fix screenshot and a passing check makes
resolution mean "I looked at the rendered outcome and it's right," not "I
edited a file and assume it's right."

## Rule: one queue, evidence rules don't change by surface

App feedback, Storybook feedback, and test-generated feedback are the same
kind of item with the same resolution bar. The surface only changes what
the item *points at* (a route vs a story id), not how rigorously it's
closed.

**Why:** a single bar means a human, an agent, and a test runner all close
items the same way, and an app issue can be reproduced-and-fixed in a
story (then verified there) without inventing a second, looser process.

## Rule: a fix often lives in a story, even for app feedback

For app feedback about reusable UI, the cleanest resolution is often:
reproduce it in the component's story, fix the reusable component, attach
the now-passing story as evidence, then confirm the route.

**Why:** Storybook is the reusable-UI runtime ([../stories/conventions.md](../stories/conventions.md)).
Fixing at the component level (with its story as proof) fixes every page
that uses it, not just the one the feedback came from.

## Rule: unresolved feedback related to your change blocks handoff

If pending feedback touches the route, story, selector, component, or
resource you changed, resolve it (with evidence) or explicitly defer it
with a reason before handing off. Carry the unresolved count into the
[handoff](../handoff/conventions.md).

**Why:** handing off with related feedback still open silently passes a
known problem to the next agent or to production. Surfacing the count
makes the decision to defer explicit instead of accidental.

## Checklist

- Each resolved item has: summary, changed files, checks run, and a
  post-fix screenshot for app/Storybook UI.
- No item closed with prose alone.
- App-vs-Storybook-vs-test items held to the same evidence bar.
- Reusable-UI fixes verified in the component's story.
- Related unresolved feedback resolved or explicitly deferred; the count
  is in the handoff.
