---
name: spec-breakdown
description: Turns an approved spec into ordered, independently mergeable implementation issues, and drafts the capability README update that keeps the repo the source of truth. Use after a change has been specced and its spec approved. Refuses to run without an approved spec. The last skill in the product pipeline.
license: MIT
metadata:
  author: Francisco Barrento
---

# Spec Breakdown

## What this skill does

`spec-breakdown` produces `issues.md` — the ordered implementation issues for
one change — from an approved spec. It assigns each of the spec's building
blocks to a dependency-role layer, splits each layer into independently
mergeable issues, attaches a completion contract and a review weight to each,
and drafts the capability `README.md` update the change makes true. It is the
last pipeline skill: after it, implementation is the code STOP gate in
`laravel-rules` / `inertia-rules`.

## Where the state tree lives

This skill is generic. It hard-codes no path. Resolve the state-tree root from
the consuming project's `CLAUDE.md` (the path it declares for the
product/capabilities tree, the same way the rules skills read `docs/adr/` and
the same way `change-scope` / `change-spec` resolve it). If the project
declares no root, use the default `docs/` and say so explicitly in your reply.

Throughout this skill, `{capabilities-root}` means
`{declared-root}/capabilities` (default `docs/capabilities`).

## STOP — how this skill works

Before producing issues you MUST, in order:

1. LOCATE THE SPEC and check approval. Read the change's `spec.md` (or
   `spec-{n}-{slug}.md` files if split). Usable ONLY if frontmatter has
   `status: approved` with `approved_by` and `approved_on` populated. If
   `draft`, unapproved, or invalidated by a later edit — STOP; the spec needs
   (re-)approval via `change-spec` first.
2. READ THE SPEC IN FULL. You turn its building blocks into issues; you do not
   add blocks, change their types, or re-decide anything. If the spec is wrong
   or incomplete, STOP — that is a `change-spec` problem.
3. ASSIGN each building block to a layer (see "Dependency-role layers").
4. CLUSTER each layer into issues (see "Splitting a layer into issues").
5. ATTACH a completion contract and a review weight to each issue.
6. ORDER the issues; draft the README update; write `issues.md`.
7. SEEK HUMAN APPROVAL of the issues.

Hard rules:
- You make no technical decisions. The spec made them. You sequence and
  package.
- You are a router. Issues cite spec sections and the rule-file paths the
  spec named. You never copy rule content into an issue.
- An issue's completion contract is part of the issue, never a separate
  issue. There is no standalone "write tests" task.

## Dependency-role layers

Every building block belongs to exactly one of six layers. Layers are defined
by DEPENDENCY ROLE — what a block depends on and what depends on it — not by
the block's type name. This is why the layer set never needs extending: a new
kind of building block lands in a layer by its role.

- **L1 — persistence:** the data that exists before anything reads it —
  schema/migrations, models, factories, seeders, relations.
- **L2a — read contract:** what produces the typed shapes — data objects,
  value objects, queries.
- **L2b — write logic:** what mutates state — actions, and anything that IS or
  WRAPS write logic (write-side jobs, CQRS commands, the events/listeners/
  observers those writes fire).
- **L3 — delivery surfaces:** thin entry points that call L2a/L2b — HTTP
  controllers, form requests, routes, the page-data contract, console
  commands, middleware.
- **L4 — UI primitives:** capability-agnostic components and their stories.
- **L5 — UI pages:** capability-specific UI wiring primitives to the change's
  data.

Placement rule: a building block joins the layer of its dependency role. To
map a specific block type to a layer, consult the rules skills —
`laravel-rules` for backend blocks, `inertia-rules` for `resources/js` blocks:
they own what a "job", a "console command", an "observer", a "primitive" is in
this stack. `spec-breakdown` owns the six layers and the rule; the rules
skills own the type→layer mapping. Examples that follow from the rule: a
queued job that wraps an action → L2b; a console command (a CLI entry point) →
L3; an observer reacting to model writes → L2b.

## Splitting a layer into issues

A layer is a taxonomy, not an issue. One issue per layer is wrong for any
non-trivial change — it produces unreviewable, all-or-nothing merges.

Within each layer, split into issues by COHESION:
- Two building blocks belong in the SAME issue only if they are cohesive —
  one is non-functional without the other (a model with its migration and
  factory; an action with the job that wraps it).
- Independent blocks in the same layer — unrelated actions, unrelated models —
  go in SEPARATE issues. A large layer always splits.
- A single cohesive cluster that is itself large but truly indivisible
  (everything in it is mutually non-functional) STAYS one issue. Cohesion may
  force a big issue; that is acceptable. Layer KIND never forces a big issue.

The legitimacy test for every issue: **could it be reviewed and merged on its
own without leaving `main` in a broken state?** If yes, it is a valid issue.
If splitting it would strand a model from its migration, it was never two
issues — it is one cohesive cluster.

A cohesive cluster NEVER crosses a layer boundary. A model (L1) and an action
that uses it (L2b) are dependency-related but not one cluster — L1 must merge
and be sound before L2b builds on it. Layering overrides cohesion across
boundaries.

Order: layers run L1 → L2a → L2b → L3 → L4 → L5; within a layer, clusters are
ordered so a cluster's dependencies precede it.

## Review intensity

Each issue carries a review weight, inherited from its layer. The weight tells
the reviewer where human attention pays off — it is driven by how much PRODUCT
JUDGEMENT versus pure CONVENTION the layer carries.

- L1 persistence — MODERATE. Convention-heavy, but the schema is a durable,
  expensive-to-change decision; review the schema shape.
- L2a read contract — HIGH. This is the contract every downstream layer
  trusts; a wrong shape propagates.
- L2b write logic — MODERATE. Business logic, bounded by the L2a contract.
- L3 delivery surfaces — MODERATE. Mostly mechanical wiring; the page-data
  contract within it is HIGH.
- L4 UI primitives — LOW. Convention-bound; trust `inertia-rules`; review
  design-system conformance only.
- L5 UI pages — HIGH. Where the PRD's user stories are satisfied or not.

Review weight and the completion contract are inverse: a LOW-review issue is
only safe because its completion contract (see "The completion contract") is
strong enough to stand in for the human. Where automated checks cannot assert
correctness (L5: "does this satisfy the user stories"), the issue stays HIGH
review.

## The completion contract

Every issue carries a completion contract — the tests and quality checks that
define when it is DONE. The contract is PART of the issue, never a separate
issue. There is no standalone "write tests" task. An issue may not be merged
until its contract passes.

`spec-breakdown` does not invent what verification a layer needs — it asks the
rules skills. For each issue, source its checks from the skill that governs
its layer: `laravel-rules` for L1–L3 (e.g. Pest tests for the building blocks,
the `arch()` suite, Pint, static analysis), `inertia-rules` for L4–L5 (e.g.
lint, type-check, the Storybook build, an a11y gate). Carry those onto the
issue as its contract.

A contract can only require checks the consuming project actually has — the
same conditional rule the rules skills' own enforcement sections use. Name the
automated checks the project's tooling supports; for anything valuable that is
not tool-backed, write it as a MANDATORY MANUAL review item in the contract,
never as a hallucinated command. A contract is never empty: automated where
tooled, explicit-manual where not.

Layer ordering with contracts: a layer's issues must have PASSING completion
contracts before the next layer's issues build on them. The boundary between
layers is a passed contract, not a checkbox — this is what stops an unverified
foundation propagating upward.

## What issues.md must contain

Write to
`{capabilities-root}/{capability-slug}/changes/{NNNN}-{slug}/issues.md`.

Frontmatter:
```
---
change: {NNNN}-{slug}
capability: {capability-slug}
why-link: changes/{NNNN}-{slug}/spec.md
status: draft
approved_by:
approved_on:
---
```
The `why-link` cites the spec by change SLUG path, never a bare number.

Body — issues grouped by layer (L1 → L5), clusters ordered within each layer.
Each issue MUST carry:
- a short imperative title;
- its layer (L1–L5) and review weight;
- the building block(s) it implements, named exactly as the spec's
  building-blocks table names them, with each block's `new` / `restructured` /
  `removed` change type;
- the governing rule-file path(s) — copied from the spec, not re-derived;
- the constraining decision-record IDs — copied from the spec, or `none`;
- its dependencies — which earlier issue(s) must merge first;
- its completion contract — the tests and quality checks.

`restructured` and `removed` blocks: name the existing callers/consumers each
affects.

The FINAL issue is the README update (see "Keeping the repo true"). It is a
real issue, depends on every implementation issue before it, and carries its
own completion contract.

Issues contain no rule content and no product re-litigation — only spec
sections, rule-file paths, decision-record IDs, and completion contracts.

## Keeping the repo true

The capability `README.md` is the PRESENT TENSE — what the capability does
today. The repo is the source of truth, so a merged change must leave that
README matching reality.

1. **Draft, do not yet write.** From the approved spec, draft the updated
   `capabilities/{capability-slug}/README.md` content — the new factual
   present-tense description. Deliver it as the final issue's payload. Do NOT
   write it to the README at breakdown time; that would make the repo claim
   something not yet true.
2. **Land atomically with the code.** The README update is applied in the
   SAME commit / PR / merge as the implementation it describes. Before that
   merge the repo truthfully describes the old capability; after it, the new
   one. There is never a window where the README and `main` disagree.

First ship of a capability: if the README is still a `provisional` stub left
by `change-scope`, the drafted update is the real present-tense README and
CLEARS the `provisional` marker. Write only what the capability factually does
now. Do NOT write a considered decomposition, scope boundaries, or any vision
relation — that is `capability-map`'s exclusive output.

Drift invariant: a change whose implementation merged with its building blocks
touched, but whose capability `README.md` was not updated in that merge, is a
source-of-truth violation.

When the capability `README.md` is updated as part of a shipped change, bump
its `revision` and append a `## Changelog` entry in the same act — one line:
the new revision, the date, and what the change altered about the capability.
The README update, the revision bump, and the changelog entry all land
together in the implementation merge. A revision bumped without a changelog
entry is a defect.

## Approval

`issues.md` is approved only by an explicit human act — the same rule as the
PRD and the spec. You cannot approve it; a sub-agent cannot; vague assent does
not count.

1. Present the issue list to the user FOR REVIEW — surface the layer order,
   the clusters, the dependencies, the review weights, the higher-risk
   `restructured`/`removed` issues, and the final README-update issue.
   Explicitly invite rejection or revision.
2. On unambiguous human approval, write `status: approved`, `approved_by`,
   `approved_on` into the `issues.md` frontmatter.
3. Any later edit to an approved `issues.md` INVALIDATES the approval — reset
   to `draft`, clear the fields, seek fresh approval.

Approved issues feed implementation: each issue re-enters the code STOP gate
of `laravel-rules` / `inertia-rules` with its rule-file paths, decision
records, and completion contract already in hand.

## When this skill applies

- Breaking an approved spec into implementation issues — this skill.
- No approved spec yet — not this skill; the change needs `change-spec` first.
- A small in-shape modification that never produced a spec — not this skill;
  it goes straight to the code STOP gate, no issues file.
- Discussion or estimation talk about a spec — not a trigger; answer normally.
