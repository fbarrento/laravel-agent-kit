---
name: product-roadmap
description: Produces product/roadmap.md — a deliberate sequence of intended value slices across capabilities, ordered by priority, dependency, and time-to-market. Use when establishing or revising the product's roadmap. Authored top-down from the strategy and capability map, never derived from existing changes. Advisory, not a gate. Refuses to run without an approved strategy and capability map.
license: MIT
metadata:
  author: Francisco Barrento
---

# Product Roadmap

## What this skill does

`product-roadmap` produces `product/roadmap.md` — the product's sequenced
intent: which value slices the product should ship next, across which
capabilities, in what order, and why. It is authored top-down from the
strategy and the capability map. It is advisory — a roadmap item is the
recommended starting point for a change, never a gate. It is product-level
state, a sibling of `vision.md` and `strategy.md`, and it can be re-run to
reconcile with a changed strategy or capability map.

## Where the state tree lives

This skill is generic. It hard-codes no path. Resolve the state-tree root from
the consuming project's `CLAUDE.md` (the path it declares for the
product/capabilities tree, the same way the rules skills read `docs/adr/` and
the same way the other pipeline skills resolve it). If the project declares no
root, use the default `docs/` and say so explicitly in your reply.

Throughout this skill, `{state-root}` is that declared root (default `docs/`),
so the roadmap lives at `{state-root}/product/roadmap.md`, the strategy at
`{state-root}/product/strategy.md`, the vision at
`{state-root}/product/vision.md`, and the capability map is the set of
`{state-root}/capabilities/{slug}/README.md`.

## STOP — how this skill works

Before producing a roadmap you MUST, in order:

1. CHECK INPUTS. Read `product/strategy.md` — it must exist and be
   `status: approved` (the strategy itself transitively requires an approved
   vision). Read the capability map — the set of
   `capabilities/{slug}/README.md`. If there is no approved strategy, or no
   capability map — STOP. The roadmap sequences value slices across
   capabilities to serve the strategy; without both it has nothing to sequence
   and no criterion to sequence by. Run `product-strategy` / `capability-map`
   first.
2. AUTHOR the roadmap top-down (see "Authoring the roadmap"). Do NOT read the
   `changes/` folders to assemble it.
3. If a roadmap already exists, RECONCILE (see "Re-running the roadmap").
4. PRODUCE THE PROPOSAL and SEEK HUMAN APPROVAL.

Hard rules:
- Authored from the strategy and capability map — never back-filled from
  existing changes.
- Priority, dependency, and time-to-market only. No dates, quarters, or
  deadlines.
- The roadmap is advisory. It gates nothing and rejects nothing.
- An item is a value slice, not a capability. If an item is a whole
  capability, it has not been broken down — break it into the slices that
  deliver value incrementally.
- You do not approve the roadmap yourself. Approval is an explicit human act.

## Authoring the roadmap

Hold the strategy and the capability map together and decide: what should this
product ship next, and in what order. Each roadmap item is one value slice.

A roadmap item is a VALUE SLICE, not a capability. The single most common
mistake is to make each item a whole capability and topologically sort them —
that is the capability map with numbers on it, not a roadmap.

A value slice is the smallest coherent increment that delivers real user
value. It is defined by the value it delivers, not by which capability it
belongs to. Therefore:
- a value slice may use only PART of a capability — a bare-bones version of a
  capability that delivers value before the full capability is built (e.g. a
  trade with just an entry and an exit price, before any reusable strategy
  engine exists);
- a value slice may SPAN several capabilities — the thinnest end-to-end thing
  a user can feel often cuts across two or three;
- a capability is almost never one roadmap item — it is usually delivered by
  several slices over several items.

For every item you draft, apply this test: "Is this the thinnest thing that
delivers user value — or have I just named a capability?" If it is a whole
capability, break it down: find the minimal slice that delivers value first,
make that the item, and let the rest of the capability follow as later items.
Sequence the slices by value and dependency — earliest value first, by the
shortest path, subject to what each slice genuinely depends on.

For each item, establish:
- the value slice it delivers, and which capability/capabilities it draws on;
- the strategy goal it serves — its `why-link` (tracing to a vision goal via
  the strategy);
- its priority relative to the other items — why it matters now versus later;
- its dependencies — which other roadmap items must happen first.

Order the items by priority and dependency. An item that cannot be tied to a
strategy goal is a finding — either the strategy is incomplete or the item
should not be on the roadmap; surface it, do not invent a goal to cite.

Sequence for earliest shippable value. The strategy states the product's
time-to-market urgency and why; the roadmap obeys it by ordering value slices
so the first shippable, market-testable slice reaches users as early as
dependencies allow. This is a sequencing criterion, NOT a date — the roadmap
still assigns no dates, quarters, or deadlines. "Time to market" means
"shortest path to real value in real hands", not "by when".

Do NOT read the `changes/` directories to build the roadmap. The roadmap is
intent; the changes are execution. Authoring from execution is the back-fill
bug. (Existing changes are relevant only during reconciliation — see below.)

## What roadmap.md must contain

Write to `{state-root}/product/roadmap.md`.

Frontmatter:
```
---
revision: 1
status: draft
approved_by:
approved_on:
reconciled-against: strategy.md revision N
---
```
`roadmap.md` is product-level state; its items carry why-links, the file
itself does not. `reconciled-against` records the `strategy.md` revision this
roadmap was authored against (and transitively the vision the strategy
serves) — see "Document versioning".

Body — an ORDERED list of roadmap items, sequenced by priority and dependency.
Each item carries:
- a short title — the value slice it delivers;
- the user-facing value the slice delivers, in one line — if it cannot state
  one, it is not a value slice;
- which capability/capabilities it draws on;
- its `why-link` — the strategy goal it serves (resolvable path + goal),
  tracing to a vision goal via the strategy;
- its priority rationale — why now versus later, in one or two lines;
- its dependencies — which earlier roadmap items must happen first, or `none`.

Plus a short **reconciliation notes** section when the roadmap was re-run (see
below), listing what changed and why.

The roadmap contains NO dates, quarters, or deadlines. It contains no PRDs, no
specs, no technical content — only sequenced intent.

## Re-running the roadmap

The roadmap is durable state and goes stale — the strategy shifts,
`capability-map` reshapes capabilities, priorities change. The roadmap is also
stale by definition when its `reconciled-against` strategy revision is behind
the current `strategy.md` `revision` (see "Document versioning").
`product-roadmap` is re-runnable. When a roadmap already exists, reconcile it:

- Re-read the current `strategy.md` (and the vision it serves) and capability
  map.
- For each existing roadmap item: is it still tied to a current strategy goal?
  Does the capability it names still exist (or was it merged/renamed by
  `capability-map`)? Is its priority still right?
- Items whose capability was reshaped have their capability reference and
  `why-link` updated. Items no longer tied to a strategy goal are flagged.
- During reconciliation ONLY, you may read the `changes/` folders — to see
  which roadmap items have already been delivered, so the re-proposed roadmap
  reflects what is done versus still intended. This is the one place existing
  changes inform the roadmap, and even here they inform RECONCILIATION, never
  the original authoring.

Re-running produces a new proposal with a reconciliation-notes section, bumps
`revision`, and sets `reconciled-against` to the `strategy.md` revision used.
It is human-approved like any roadmap.

## Approval

The roadmap is approved only by an explicit human act — the same rule as the
vision, the capability map, the PRD, the spec. You cannot approve it; a
sub-agent cannot; vague assent does not count.

1. Present the roadmap to the user FOR REVIEW — the item order, the priority
   rationale, the dependencies, and any item not tied to a vision goal.
   For a re-run, surface the reconciliation notes. Explicitly invite rejection
   or revision.
2. On unambiguous human approval, write `status: approved`, `approved_by`,
   `approved_on`, the current `revision`, and `reconciled-against` into the
   `roadmap.md` frontmatter.
3. Any later edit to an approved roadmap INVALIDATES the approval — reset to
   `draft`, clear the fields, seek fresh approval.

## How the roadmap feeds the pipeline

A roadmap item is the RECOMMENDED upstream of a change. When an item's turn
comes, it is the starting point handed to `idea-grill` or `change-scope` — a
prioritized, vision-linked intent rather than a raw idea.

The roadmap is advisory. A change may enter the pipeline WITHOUT a roadmap
item — `product-roadmap` gates nothing and rejects nothing. A PRD MAY cite its
roadmap item; if it does, the why-link chain extends from change to roadmap
item to strategy goal to vision goal. If it does not, nothing breaks.
`product-roadmap` never blocks `change-scope` and never requires a change to
trace to a roadmap item.

## When this skill applies

- Establishing or revising the product's roadmap — this skill.
- A single feature idea ready to scope — NOT this skill; that is `idea-grill`
  / `change-scope`.
- Decomposing the product into capabilities — NOT this skill; that is
  `capability-map`.
- Discussion about priorities — not a trigger; answer normally.

## Precedence

`strategy.md` and the capability map outrank `product-roadmap` — they are what
the roadmap sequences to serve; this skill never edits them to make an item
fit. (`strategy.md` in turn serves `vision.md`.) If the roadmap exposes that
the strategy is incomplete or a capability is missing, that is a finding for
`product-strategy` / `capability-map` and a human — surface it, do not resolve
it by bending the roadmap. `product-roadmap` reads and writes no decision
records.

## Document versioning

A human must be able to tell, by opening the roadmap, whether it is current
with the strategy it serves — without reading git history.

- `roadmap.md` carries a `revision` integer and an `approved_on` date, bumped
  on every approved change.
- It records `reconciled-against: strategy.md revision N` — the `strategy.md`
  revision it was authored against (and transitively the vision the strategy
  serves).
- Staleness is readable on the face of the file: if `strategy.md`'s `revision`
  is higher than the roadmap's `reconciled-against` value, the roadmap is
  STALE and must be re-run (see "Re-running the roadmap"). No git archaeology
  required.

This is the same scheme `product-vision` and `product-strategy` apply to their
own documents.
