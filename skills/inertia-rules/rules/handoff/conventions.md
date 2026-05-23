# Handoff

The handoff is the evidence-backed close-out of a UI task: what changed,
what was checked, what's left. A human summary is fine, but it must be
backed by the same evidence the future `iak.handoff.v1` artifact will
carry. This file is the discipline; no command is required to follow it.

## Rule: a complete handoff carries evidence, not claims

For completed UI work, the handoff includes:

- **Changed files grouped by role** (page / feature / primitive /
  app-component / story / type), each with its action (create/modify).
- **Audit result** — the [audit](../audit/conventions.md) self-check passed
  (or its remaining findings, explicitly).
- **Type/test result** — typecheck, lint, and tests passed.
- **Story evidence** — for reusable-UI changes, the story id(s) and status.
- **Browser evidence** — for route-visible changes, the app URL/route, a
  screenshot, the console result (error count), and an accessibility
  result when available.
- **Unresolved feedback count** — even when zero
  ([../feedback/conventions.md](../feedback/conventions.md)).
- **Brand status** — when Brand OS is enabled and the task touched
  UI/tokens/assets.

**Why:** "done" is only meaningful with proof. Each item maps to a way the
work commonly fails silently — a missing story, a console error, an
unresolved comment — so requiring it in the handoff turns "I think it's
done" into "here is the evidence it's done."

## Rule: a handoff is invalid if required evidence is missing

A handoff for completed work is **not** complete if it omits: changed
files grouped by role, audit result, test result, a story id or app URL
for visible changes, a screenshot for an inspected surface, the console
result, or the unresolved-feedback count.

**Why:** these are exactly the fields the next agent (or the verify step)
needs to trust the work without redoing it. An omission isn't a formatting
nit — it's a missing proof, which means the claim can't be trusted.

## Rule: be honest about skipped and deferred items

If a verification step was skipped (no browser runner, route unreachable)
or feedback was deferred, say so with a reason. Don't present skipped
steps as passed or hide deferred feedback.

**Why:** an honest "browser check skipped: no Pest Browser configured"
lets the reader decide whether that's acceptable; a silent omission or a
false "passed" removes their ability to. The whole point of the evidence
trail is that it can be trusted.

## Rule: keep it small — reference, don't embed

Summaries, ids, counts, and paths go in the handoff. Screenshots, DOM
dumps, console logs, generated types, and whole files are referenced by
path, not pasted.

**Why:** the handoff is for the next reader's working memory; pasting
verbose artifacts buries the signal and blows the context budget. A path
to the screenshot is as good as the screenshot and a hundredth the size.

## Checklist

- Changed files listed and grouped by role, with actions.
- Audit, typecheck, lint, and tests reported with results.
- Story id/status for reusable-UI changes; app URL + screenshot + console
  + a11y for route-visible changes.
- Unresolved feedback count included (even if zero); brand status when
  enabled.
- Skipped/deferred items stated with reasons, never disguised as passed.
- Verbose artifacts referenced by path, not embedded.
