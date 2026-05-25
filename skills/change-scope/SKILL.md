---
name: change-scope
description: Turns a raw product or feature idea into an approved PRD — the product WHY of one change to a capability. Use when a feature, extension, or refactor is being proposed and needs scoping before any technical spec. Classifies the idea (new capability / change to an existing capability / in-shape work needing no pipeline). Does NOT make technical decisions and does NOT produce technical specs.
license: MIT
metadata:
  author: Francisco Barrento
---

# Change Scope

## What this skill does

`change-scope` produces a PRD — the WHY of one change to a capability: the
problem, the user's current pain, the product value, user stories, and scope.
It runs BEFORE any technical spec. It owns the product reasoning and makes no
technical decisions. The PRD it produces is the required input to
`change-spec`, and `change-spec` will refuse a PRD that a human has not
approved.

## Where the state tree lives

This skill is generic. It hard-codes no path. Resolve the state-tree root from
the consuming project's `CLAUDE.md` (the path it declares for the
product/capabilities tree, the same way the rules skills read `docs/adr/`). If
the project declares no root, use the default `docs/` and say so explicitly in
your reply.

Throughout this skill, `{capabilities-root}` means
`{declared-root}/capabilities` (default `docs/capabilities`), and
`product/vision.md` means `{declared-root}/product/vision.md`.

## STOP — how this skill works

Before producing a PRD you MUST, in order:

1. CLASSIFY the idea. State the classification and the reasoning out loud:
   - New capability — the product has no existing area for this.
   - Change to an existing capability — name the capability. Make this call
     ONLY after reading that capability's existing PRDs and decision records
     (see Precedence); prior decisions are often what make a change
     architectural.
   - In-shape work — a small modification needing no PRD and no spec. Say so
     and STOP: direct the work to the relevant rules skill's code gate. Do not
     manufacture a PRD for a one-line change.
2. RESOLVE THE CAPABILITY ANCHOR.
   - The capability already exists → the PRD will cite its `README.md`.
   - The capability does NOT exist → create a provisional capability stub
     (Task 5) so the PRD has a real parent to cite. The stub is an anchor, not
     a capability description.
3. ALLOCATE THE CHANGE NUMBER (Task 6).
4. WRITE THE PRD (Task 7).
5. SEEK HUMAN APPROVAL (Task 8). Until a human approves, the PRD is not
   approved and `change-spec` may not consume it.

Hard rules:
- You make no technical decisions. No class shapes, casts, schema, or
  framework specifics appear in a PRD. If you are writing one, stop — that is
  `change-spec`'s job.
- A good PRD passes this test: a non-engineer can read it and disagree with
  it. If half of it is only meaningful to someone who has read the code
  conventions, the why and the how have been welded — start over.
- You do not approve your own PRD. Approval is an explicit human act (Task 8).

## Creating a provisional capability stub

When the target capability does not yet exist, create — and nothing more:

- the folder `{capabilities-root}/{capability-slug}/`
- a `README.md` containing ONLY: the capability name, a one-line
  description, and this status block:

  ```
  status: provisional — established by change-scope, pending capability-map
  why-link: BOOTSTRAP — no product vision yet
  ```

  If `product/vision.md` already exists, replace the `why-link` line with a
  real citation to the relevant vision goal (path + section) instead of the
  BOOTSTRAP token.

This stub is a coat hook: it exists so the PRD has a resolvable parent. You
MUST NOT write a considered capability description, scope, boundaries, or
decomposition into it — that is `capability-map`'s exclusive output, produced
later, which will review and promote this stub. Creating the stub does not
make `change-scope` a two-transition skill: the stub is the PRD's parent
coming into existence as a side effect, explicitly marked provisional.

## Numbering a change

Scan the capability's `changes/` directory and take the next free integer,
zero-padded to four digits (`0001`, `0002`, …). This number is PROVISIONAL
until merge — tell the user plainly: "scoped as NNNN — provisional; if NNNN
already exists when this merges, renumber."

The change's identity is its SLUG, not its number. The change folder is
`changes/{NNNN}-{change-slug}/`; the slug is what is unique and meaningful.
Two developers minting the same number in parallel is a loud, merge-time
naming conflict resolved by a rename — it is expected and acceptable.

Because the number is provisional, every why-link that references THIS change
(the spec citing this PRD, issues citing this change) MUST cite the change
SLUG, never the bare number. A renumber must never break a why-link.

## What a PRD must contain

Write the PRD to `{capabilities-root}/{capability-slug}/changes/{NNNN}-{slug}/prd.md`.

Frontmatter:
```
---
change: {NNNN}-{slug}
capability: {capability-slug}
why-link: {resolvable path + section of the capability README.md}
status: draft
approved_by:
approved_on:
---
```

Body — every section is required; sections collapse for a small change but are
never absent:
- **Problem** — what the user cannot do today, and the pain it causes. In
  product terms, no implementation language.
- **Why now / value** — what shipping this is worth, to whom.
- **User stories** — real user-facing stories. "As a developer, I want a typed
  data contract" is NOT a user story — it is a technical decision; it does not
  belong here.
- **Scope** — what this change includes.
- **Out of scope** — what it explicitly does not, and why.
- **Open product questions** — unresolved product (not technical) questions.

The PRD describes intent and value only. It names no classes, tables, casts,
routes, or framework mechanics.

## Approval

A PRD is approved only by an explicit human act. You cannot approve it; a
sub-agent cannot; ambiguous assent ("looks good", "sure") does not count — if
the response is vague, ask again.

Steps:
1. Present the finished PRD to the user FOR REVIEW. Surface what it commits to
   — the problem framing, the scope, the out-of-scope calls — and explicitly
   invite rejection or revision. Do not present it as a fait accompli; an
   approval step that can only produce "yes" is theatre.
2. On unambiguous human approval, write into the PRD frontmatter:
   `status: approved`, `approved_by: {who}`, `approved_on: {date}`.
3. Any later edit to an approved PRD INVALIDATES the approval: reset
   `status` to `draft` and clear `approved_by`/`approved_on`. The edited PRD
   needs fresh human approval. "Approved" must always mean "approved as it now
   reads."

`change-spec`'s STOP gate checks exactly this: it consumes a PRD only if
`status: approved` and the approval fields are populated and current.

## Precedence

A project's documented decisions outrank this skill. Read them if the project
keeps them — `change-scope` never requires them and never hard-codes their
location; the project's `CLAUDE.md` declares which exist (commonly
`docs/adr/`, `docs/postmortem/`, `docs/learnings/`).

When classifying a change to an existing capability (STOP step 1), read the
capability's existing PRDs AND any relevant decision records — read the
document body, never the title or a commit message. Prior decisions are often
what make an otherwise-small change architectural, and that classification is
the difference between scoping it properly and routing it to the code gate.

`change-scope` proposes no decision records and overrides none. A change that
contradicts an existing decision is surfaced for a human ruling in the PRD's
**Open product questions**; the technical resolution belongs to `change-spec`.
