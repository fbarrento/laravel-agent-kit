---
name: capability-map
description: Decomposes the product into a considered set of capabilities — turning product/vision.md into capability READMEs. Use when mapping or re-mapping a product's capabilities, or promoting provisional capability stubs into considered capabilities. Refuses to run without an approved product vision. Produces the map as a proposal for human approval; reshaping a populated capability is migrated, never edited.
license: MIT
metadata:
  author: Francisco Barrento
---

# Capability Map

## What this skill does

`capability-map` produces the product's considered capability set — one
`README.md` per capability — by decomposing `product/vision.md`. It owns the
"is this one capability or three" judgment, and it promotes the provisional
capability stubs `change-scope` created during bootstrap into considered
capabilities. It produces the decomposition as a PROPOSAL for human approval;
on approval it applies the map, migrating the change history of any capability
it reshapes. It is the last pipeline skill.

## Where the state tree lives

This skill is generic. It hard-codes no path. Resolve the state-tree root from
the consuming project's `CLAUDE.md` (the path it declares for the
product/capabilities tree, the same way the rules skills read `docs/adr/` and
the same way the other pipeline skills resolve it). If the project declares no
root, use the default `docs/` and say so explicitly in your reply.

Throughout this skill, `{capabilities-root}` means
`{declared-root}/capabilities` (default `docs/capabilities`), and
`product/vision.md` means `{declared-root}/product/vision.md`.

## STOP — how this skill works

Before producing a capability map you MUST, in order:

1. CHECK THE VISION. Read `product/vision.md`. It must exist and be
   `status: approved`. If there is no vision, or it is unapproved — STOP. You
   cannot decompose a product that has not been defined; run `product-vision`
   first.
2. READ THE CURRENT STATE. Read `vision.md` in full and every existing
   capability `README.md` (provisional and considered) with its `changes/`
   history.
3. DECOMPOSE the product into a considered capability set (see "The
   decomposition").
4. PRODUCE THE PROPOSAL — the considered map plus every merge / split / rename
   it implies against the current capabilities (see "The proposal").
5. SEEK HUMAN APPROVAL of the proposal. Nothing is rewritten before approval.
6. APPLY the approved map (see "Applying the map"), migrating reshaped
   capabilities.

Hard rules:
- No vision, no run. The vision is the criterion you decompose against.
- You never rewrite a README or a `why-link` before the proposal is approved.
- A capability with shipped changes may be reshaped, never erased. Its history
  is real.

## The decomposition

Decompose the product — defined by `vision.md` — into capabilities. A
capability is a durable area of the product, named for what it is
(`watchlists`), never for a release or version.

This is a BATCH judgment over the whole product at once, not a stub-by-stub
promotion. Holding the vision and the current capabilities together, decide
the considered set. You may conclude:
- a provisional stub is sound → promote it as-is;
- two provisional capabilities are really one → merge;
- one stub should be several → split;
- the vision implies a capability nothing has grown toward yet → a new,
  empty considered capability.

Each considered capability cites a vision goal — the goal it serves — as its
`why-link`. A capability you cannot tie to a vision goal is a finding: either
the vision is incomplete or the capability is misaligned. Surface it in the
proposal; do not invent a goal to cite.

Most runs the provisional set will be broadly sound and the decomposition
mostly confirms it with light edits. Reserve merges and splits for where the
decomposition genuinely changes shape.

Not every thing in the product is a capability. Some are infrastructure —
substrate that capabilities consume but that is not a product area:
authentication and user accounts, third-party data feeds, the database (see
`DESIGN_PRODUCT_PIPELINE.md` §2a). When decomposing, classify each such thing
explicitly as infrastructure: it is NOT a capability, it carries no why-link
and no vision goal, and it is NOT folded inside a capability — it sits below
the capability layer, consumed by capabilities directly. Do not invent a
vision goal to give an infrastructure item a why-link, and do not bury shared
substrate inside one capability. If a thing looks like infrastructure but the
vision implies users experience it as a product surface, it is a capability
and the vision has a gap — flag it, do not misclassify it as infrastructure.

## The proposal

Produce the decomposition as a PROPOSAL before changing anything. The proposal
states:
- the considered capability set, each with its one-line description and the
  vision goal it cites;
- for each existing capability, what happens to it — `confirmed`, `merged
  into {x}`, `split into {x, y}`, `renamed to {x}`, or `unchanged`;
- for every merge / split / rename of a capability that HAS a `changes/`
  history, the migration it entails — which `changes/` folders move and which
  `why-link`s must be rewritten;
- any capability that cannot be tied to a vision goal, flagged for a human.
- any thing classified as infrastructure rather than a capability — listed
  separately, with no why-link, noted as below the capability layer.

Present the proposal for review and explicitly invite rejection or revision. A
skill that can mass-break `why-link`s must not act unreviewed. Nothing in the
state tree is rewritten until a human approves the proposal.

## Applying the map

Only after the proposal is human-approved, apply it:

- **Confirmed / unchanged capability** — write or update its considered
  `README.md`: what the capability is, the vision goal it cites, its
  boundary. Clear any `provisional` marker. This is the considered
  description — `capability-map`'s exclusive output.
- **Reshaped capability (merge / split / rename) WITH a `changes/` history** —
  this is a MIGRATION, applied atomically:
  1. move the affected `changes/{NNNN}-{slug}/` folders to their new
     capability;
  2. rewrite every `why-link` and `capability:` frontmatter field in every
     PRD / spec / issues file that referenced the old capability;
  3. write the considered README for the resulting capability(ies).
  A reshape that skips the migration leaves the tree with broken `why-link`s —
  it is not done until every link resolves again.
- **A capability with shipped changes is never erased.** If the decomposition
  removes a capability as a standalone, its changes are folded into whichever
  capability absorbs them — the history moves, it is never dropped. Erasing
  shipped history would make the repo lie about what was built.
- **Infrastructure-tier items** — record each in the capability-map output as
  infrastructure: below the capability layer, consumed by named capabilities,
  no why-link, no vision goal. Do NOT create a `capabilities/{slug}/` folder
  or a considered README for it — it is not a capability.

After applying, every `why-link` in the tree must resolve. Verify it.

## When this skill applies

- Mapping a product's capabilities for the first time, or re-mapping them —
  this skill.
- Promoting provisional capability stubs into considered capabilities — this
  skill.
- No approved `vision.md` exists — NOT this skill; run `product-vision` first.
- A single feature idea — NOT this skill; that is `change-scope` (stage 3).
- Updating one capability's present-tense README because a change shipped —
  NOT this skill; that is `spec-breakdown`.
- Discussion about product structure — not a trigger; answer normally.

## Precedence

`vision.md` outranks `capability-map` — the vision is the criterion the
decomposition serves; this skill never edits the vision to make a capability
fit. If the decomposition exposes that the vision is incomplete, that is a
finding for `product-vision` and a human, surfaced in the proposal — not
something to resolve by bending the map.

`capability-map` reads and writes no decision records; technical decisions are
below its concern.

## What a capability README must contain

A considered `capabilities/{slug}/README.md` (this skill's exclusive output):

Frontmatter:
```
---
capability: {slug}
why-link: {resolvable path + goal in product/vision.md}
status: considered
---
```

Body:
- **What this capability is** — the durable area of the product it covers,
  in present tense.
- **Why it exists** — the vision goal it serves.
- **Boundary** — what falls inside this capability and what belongs to a
  neighbouring one.

The README is the considered description. The per-change present-tense detail
of what the capability currently does is maintained by `spec-breakdown` on
each ship; `capability-map` owns the considered framing, not the change-by-
change present tense.
