---
name: change-spec
description: Turns an approved PRD into a technical spec — the HOW of one change to a capability. Use after a change has been scoped and its PRD approved, to decompose it into building blocks and route each to its governing rule file. Refuses to run without an approved PRD. Cites rule-file paths; never restates rule content.
license: MIT
metadata:
  author: Francisco Barrento
---

# Change Spec

## What this skill does

`change-spec` produces a spec — the HOW of one change: the building blocks it
introduces, restructures, or removes, each routed to its governing rule file,
plus the decision records that constrain it. It consumes an approved PRD as
input and never re-derives the product why. It is a router: it points at the
rule files in `laravel-rules` / `inertia-rules`, it never copies what those
rules say. The spec it produces, once human-approved, is the input to
`spec-breakdown`.

## Where the state tree lives

Generic skill — hard-codes no path. Resolve the state-tree root from the
project's `CLAUDE.md` (project-declared paths, DESIGN_PRODUCT_PIPELINE.md §2);
default `docs/`, and say which you used. `{capabilities-root}` means
`{declared-root}/capabilities` (default `docs/capabilities`).

## STOP — how this skill works

Before producing a spec you MUST, in order:

1. LOCATE THE PRD and check its approval. Read the target change's `prd.md`.
   It is usable ONLY if its frontmatter has `status: approved` with
   `approved_by` and `approved_on` populated. If it is `draft`, unapproved, or
   the approval was invalidated by a later edit — STOP. Tell the user the PRD
   needs (re-)approval via `change-scope` first. You may not spec an
   unapproved PRD.
2. READ THE PRD IN FULL as your input. The spec implements the PRD's intent;
   it does not reinterpret or expand it. If the PRD's product intent looks
   wrong, STOP — that is a `change-scope` problem, not something to fix here.
3. READ THE RELEVANT DECISION RECORDS (see Precedence) — bodies, not titles.
4. DECOMPOSE into building blocks and route each to its governing rule file
   (see "Routing to the rules skills").
5. DECIDE one spec or several (see "One spec or several").
6. WRITE THE SPEC (see "What a spec must contain").
7. SEEK HUMAN APPROVAL (see "Approval").

Hard rules:
- You are a router, not a rulebook. You cite rule-file paths. You never copy,
  summarize, or paraphrase what a rule says into the spec.
- Every technical claim about how the project does something is labelled by
  Provenance (see below). No inference may be load-bearing.
- You do not approve your own spec. Approval is an explicit human act.

## Routing to the rules skills

For every building block in the spec, name its governing rule file by looking
it up in the relevant skill's Routing Table:
- backend / PHP building blocks → the `laravel-rules` Routing Table;
- anything under `resources/js` → the `inertia-rules` Routing Table.

Cite the rule file by PATH (e.g. `rules/data-objects/conventions.md`). Do not
invent paths — use the Routing Table. You may open a rule file to confirm a
building block is being specced correctly, but you MUST NOT copy its content
into the spec. The spec tells the implementer WHICH rule file governs each
block; the implementer opens it at the code STOP gate. A spec that paraphrases
a rule has rebuilt the cheat-sheet the rules skills exist to prevent.

## What a spec must contain

Write the spec to
`{capabilities-root}/{capability-slug}/changes/{NNNN}-{slug}/spec.md`.

Frontmatter:
```
---
change: {NNNN}-{slug}
capability: {capability-slug}
why-link: changes/{NNNN}-{slug}/prd.md
status: draft
approved_by:
approved_on:
---
```
The `why-link` cites the PRD by change SLUG path, never a bare number.

Body — every section required; sections collapse for a small change, never
absent:

- **Summary** — in prose, what this change builds, traced to the PRD's intent.
- **Building blocks** — a table, one row per block, columns:
  `name` · `type` · `change` · `rule file` · `decision records` · `deviation`
  where `change` is `new` / `restructured` / `removed`, `rule file` is the
  path from the rules-skill Routing Table, `decision records` is the
  constraining record IDs or `none`, and `deviation` names any rule this block
  deliberately departs from, with justification, or `none`.
- **Decision records consulted** — which records were read in full, and the
  precedence applied.
- **Inferences & open questions** — every Provenance `inference`, and any
  unresolved technical question. Nothing load-bearing left silent.
- **Proposed decision records** — stubs for technical decisions nothing
  governed (see Precedence).
- **Superseded decision records** — any existing record this change
  contradicts or invalidates, flagged for a human ruling.

The spec contains no product re-litigation. It contains no rule content —
only rule-file paths.

## Precedence

A project's documented decisions outrank the rules skills. Read them if the
project keeps them — `change-spec` never requires them and never hard-codes
their location; the project's `CLAUDE.md` declares which exist (commonly
`docs/adr/`, `docs/postmortem/`, `docs/learnings/`). Read the document body,
never the title or a commit message.

Three moves, all recorded in the spec:
- **Cite** — a record that still constrains this change → its ID in the
  building-blocks table and in "Decision records consulted".
- **Propose** — a technical decision this change forces that nothing governs →
  a stub in "Proposed decision records". `change-spec` proposes; a human
  decides. This is the only thing `change-spec` may suggest writing to a
  decision-record folder.
- **Supersede** — a record this change contradicts or invalidates → flagged in
  "Superseded decision records" for a human ruling. `change-spec` never
  silently overrides a decision record.

## Provenance

Every claim in the spec about how the project does something is labelled:
- authority — from a rule file or decision record actually read;
- general-knowledge — true of the framework/library regardless of this
  project;
- inference — your reasoning, not yet verified here.

No inference may be load-bearing in the spec. Every `inference` appears in
"Inferences & open questions". When implementation begins, each inference must
be resolved against the rule file or decision record before the building-block
code is written.

## One spec or several

A change may need more than one spec — e.g. a domain spec and an HTTP/Inertia
spec, delivered as separate tasks. Splitting is a judgment you own: split when
the parts have distinct building blocks, distinct rule skills, or a clean
dependency boundary (one unblocks the other). When you split, each spec file
is `spec-{n}-{slug}.md` in the change folder, each carries its own frontmatter
and approval, and each cites the same PRD. Do not split a small change for the
sake of it; do not cram a genuinely two-layered change into one spec.

## Approval

A spec is approved only by an explicit human act — the same rule as a PRD. You
cannot approve it; a sub-agent cannot; vague assent does not count.

1. Present the finished spec to the user FOR REVIEW — surface the building
   blocks, the change types, the deviations, and especially any superseded
   decision records. Explicitly invite rejection or revision.
2. On unambiguous human approval, write `status: approved`, `approved_by`,
   `approved_on` into the spec frontmatter.
3. Any later edit to an approved spec INVALIDATES the approval — reset to
   `draft`, clear the fields, seek fresh approval.

`spec-breakdown` (stage 5) consumes a spec only if it is `status: approved`
with current approval fields.
