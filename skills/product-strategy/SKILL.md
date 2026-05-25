---
name: product-strategy
description: Produces product/strategy.md — the WHAT between the vision's why and the roadmap's when. Use when defining or revising the product's strategy — target customers and personas, positioning, measurable goals, monetization, and time-to-market urgency. Authored from human intent, reconciled against the vision. Refuses to run without an approved vision.
license: MIT
metadata:
  author: Francisco Barrento
---

# Product Strategy

## What this skill does

`product-strategy` produces `product/strategy.md` — the strategy layer of the
product, between the vision (why) and the roadmap (when/how). It defines who
the product is for (personas), how it is positioned, the measurable goals,
the monetization model, and the time-to-market urgency. It is authored from
human intent and reconciled against the approved vision. The roadmap and the
capabilities are sequenced and shaped to serve it.

## Where the state tree lives

Generic skill — hard-codes no path. Resolve the state-tree root from the
project's `CLAUDE.md` (project-declared paths, DESIGN_PRODUCT_PIPELINE.md §2);
default `docs/`, and say which you used. `{state-root}` is that root, so the
strategy lives at `{state-root}/product/strategy.md` and the vision at
`{state-root}/product/vision.md`.

## STOP — how this skill works

Before writing `strategy.md` you MUST, in order:

1. CHECK THE VISION. Read `product/vision.md` — it must exist and be
   `status: approved`. No approved vision → STOP; the strategy serves the
   vision and cannot precede it.
2. ELICIT INTENT. The strategy is authored from the human's intent about
   market, customers, positioning, monetization, and urgency. If you do not
   have that intent, ASK. Do NOT derive the strategy from the codebase, the
   capabilities, or the readied-idea stub.
3. RECONCILE against the vision (see "Reconciliation").
4. WRITE the strategy (see "What strategy.md must contain").
5. SEEK HUMAN APPROVAL — the strategy is a high-stakes artifact; explicit
   human approval, like the vision.

Hard rules:
- Authored from human intent, never derived from what exists.
- Concise. A strategy nobody can internalize and reference in daily decisions
  is dead. No 50-page documents.
- It is the WHAT, not the WHY (that is the vision) and not the WHEN (the
  roadmap). It does not restate the vision or pre-empt the roadmap.
- You do not approve the strategy yourself. Approval is an explicit human act.

## Reconciliation

Hold the drafted strategy against the approved vision. The strategy must serve
the vision, not contradict it. Surface, as findings flagged for a human:
- a strategy element (a persona, a monetization model, a goal) that the vision
  does not support — either the vision needs revisiting or the element is
  wrong;
- a vision goal the strategy does nothing to advance — a gap in the strategy.

Do not resolve these by bending the strategy or the vision. Flag them. If the
strategy genuinely requires the vision to change, that goes back to
`product-vision` — the strategy does not edit the vision.

## What strategy.md must contain

Write to `{state-root}/product/strategy.md`.

Frontmatter:
```
---
revision: 1
status: draft
approved_by:
approved_on:
why-link: product/vision.md
reconciled-against: vision.md revision N
---
```

Body — every section required; concise throughout:
- **Target customers & personas** — the specific segments the product serves,
  as personas: their context, needs, behaviours, what they do today. This is
  the home of personas — they belong here, not in the vision.
- **Positioning** — how the product is different from the alternatives, in a
  sentence or two; who it is explicitly NOT for.
- **Measurable goals** — the concrete, trackable objectives for the product
  (the vision's goals are aspirational; these are measurable). Each should
  serve a vision goal.
- **Monetization** — how, or whether, the product makes money. If the product
  is to be paid, this is where that decision lives — not in the vision and not
  in the roadmap.
- **Time-to-market urgency** — how fast the product needs to reach users, and
  WHY (competitive window, runway, the need to test an unproven bet). This is
  the input the roadmap uses to sequence for earliest shippable value.
- **Reconciliation report** — the findings from "Reconciliation".
- **Changelog** — per DESIGN_PRODUCT_PIPELINE.md §2b (Changelog); first entry
  `revision 1 — <date> — initial strategy`.

The strategy is the WHAT. It names no capabilities, no roadmap items, no
implementation. It is concise enough to be internalized.

## Re-running the strategy

`strategy.md` is durable state and can go stale as the vision changes.
`product-strategy` is re-runnable: re-read the current vision, reconcile, and
re-propose. On every run, bump `revision`, set `reconciled-against` to the
vision revision used, and append a `## Changelog` entry naming the change. A
re-run produces a reconciliation report of what changed and is human-approved
like any strategy.

## Approval

`strategy.md` is approved only by an explicit human act — the same rule as the
vision. You cannot approve it; a sub-agent cannot; vague assent does not count.

1. Present the strategy to the user FOR REVIEW — the personas, the
   positioning, the goals, the monetization decision, the time-to-market
   urgency, and any reconciliation findings. Explicitly invite rejection or
   revision.
2. On unambiguous human approval, write `status: approved`, `approved_by`,
   `approved_on`, and the current `revision`.
3. Any later edit to an approved strategy INVALIDATES the approval — reset to
   `draft`, clear the fields, seek fresh approval.

On approval, before writing `status: approved`, append a `## Changelog` entry
for this revision: the new `revision` number, the date, and one or two
sentences on what changed and why. Bumping `revision` without the matching
changelog entry is a defect — they are one act.

## When this skill applies

- Defining or revising the product's strategy — this skill.
- Setting the product's vision — NOT this skill; that is `product-vision`.
- Sequencing what to build next — NOT this skill; that is `product-roadmap`.
- A single feature idea — NOT this skill; that is `idea-grill` / `change-scope`.

## Precedence

`vision.md` outranks `strategy.md` — the strategy serves the vision and never
edits it. The strategy in turn outranks the roadmap and the capability map:
the roadmap sequences to serve the strategy, capabilities are shaped to serve
it. If the strategy exposes that the vision is wrong, that is a finding for
`product-vision` and a human — flag it, do not resolve it by bending the
strategy.

## Document versioning

Per DESIGN_PRODUCT_PIPELINE.md §2b. `product-strategy` sets its own `revision`
and `reconciled-against: vision.md revision N`; a vision whose `revision`
exceeds that value means this strategy is STALE and must be re-run.
