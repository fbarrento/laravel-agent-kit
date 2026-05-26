---
name: product-vision
description: Establishes or materially revises product/vision.md — the root statement of what the product is for, who it serves, what it solves, and what it is not. Use when defining or re-defining a product's vision. Authors the vision from human intent, reconciles it against existing capabilities, and resolves bootstrap vision-links. Not triggered by a single feature idea.
license: MIT
metadata:
  author: Francisco Barrento
---

# Product Vision

## What this skill does

`product-vision` produces `product/vision.md` — the root WHY of the product.
It works in three parts: it elicits the vision from human product intent; it
reconciles that vision against any capabilities the project has already grown;
and once the vision is approved it resolves the bootstrap vision-links left on
capability stubs. It is the top of the pipeline — every capability ultimately
cites the vision this skill writes.

## Where the state tree lives

Generic skill — hard-codes no path. Resolve the state-tree root from the
project's `CLAUDE.md` (project-declared paths, DESIGN_PRODUCT_PIPELINE.md §2);
default `docs/`, and say which you used. `{state-root}` is that root, so the
vision lives at `{state-root}/product/vision.md` and capability stubs at
`{state-root}/capabilities/{slug}/README.md`.

## STOP — how this skill works

Before writing `vision.md` you MUST, in order:

1. ELICIT INTENT. The vision is authored from the human's product intent —
   what the product is for, who it serves, what it solves, what it explicitly
   is NOT. If you do not have that intent, ASK for it. You may not infer the
   vision from the codebase or from existing capability stubs.
2. RECONCILE against existing capabilities (see "Reconciliation"). Read the
   capability stubs; produce a reconciliation report of where the drafted
   vision and the built reality disagree. Findings are flagged for a human,
   never silently fixed.
3. WRITE the vision (see "What vision.md must contain").
4. SEEK HUMAN APPROVAL — the vision is the highest-stakes artifact in the
   pipeline; it gets an explicit human approval step.
5. RESOLVE BOOTSTRAP TOKENS, gated (see "Resolving bootstrap vision-links").

On approval, before writing `status: approved`, append a `## Changelog` entry
for this revision: the new `revision` number, the date, and one or two
sentences on what changed and why. Bumping `revision` without the matching
changelog entry is a defect — they are one act.

Hard rules:
- You author the vision from human intent. You never derive it from what got
  built. A vision traced from the codebase can only ratify the product; it
  must be able to judge it.
- Reconciliation surfaces drift. It never edits the vision to fit the
  capabilities, nor the capabilities to fit the vision.
- You do not approve the vision yourself. Approval is an explicit human act.

## Reconciliation

A project may already have provisional capability stubs and shipped changes
before this skill ever runs. Read them — every `capabilities/{slug}/README.md`
— and hold the drafted intent-based vision next to them. Ask the tension
questions:

- Is there a capability the vision, as drafted, does NOT justify? A real
  finding: either the vision is incomplete, or something got built that should
  not have been. Flag it; a human decides which.
- Does the vision call for something NO capability is growing toward yet? A
  gap between intent and reality. Flag it.
- Does a capability's description CONTRADICT the vision's framing? Flag it.

The output is the vision (from intent) PLUS a reconciliation report listing
these findings. You do not resolve them — widening the vision or marking a
capability misaligned is a human's call. Reconciliation is how this skill
turns "write a vision" into "discover whether the built product and the
intended product have drifted apart." Reading the stubs informs the CHECK; it
never authors the vision.

## What vision.md must contain

Write to `{state-root}/product/vision.md`.

Frontmatter:
```
---
revision: 1
status: draft
approved_by:
approved_on:
---
```
`vision.md` is the root why — it has no `why-link`.

Body — every section required:
- **Purpose** — what the product is for, in one or two plain sentences.
- **Who it serves** — the audience(s).
- **What it solves** — the problems it exists to remove.
- **What it is not** — explicit non-goals; the product's boundary.
- **Vision goals** — the named goals capabilities will cite. Each goal is a
  short, stable, citable statement. These are the citation targets for every
  capability `why-link`.
- **Reconciliation report** — the findings from "Reconciliation": capabilities
  the vision does not account for, intent no capability serves, contradictions.
  Each flagged for a human. If the project had no capabilities, say so.
- **Changelog** — per DESIGN_PRODUCT_PIPELINE.md §2b (Changelog); first entry
  `revision 1 — <date> — initial vision`.

The vision is written from intent. It contains no capability decompositions,
no technical content.

## Resolving bootstrap vision-links

`change-scope` creates capability stubs during bootstrap with the vision-link
`why-link: BOOTSTRAP — no product vision yet`, because no vision existed yet.
Once `vision.md` is approved, resolve those tokens — but GATED on
reconciliation:

- For a capability the reconciled vision JUSTIFIES — replace its `BOOTSTRAP`
  token with a real citation to the specific vision goal it serves
  (path + goal).
- For a capability FLAGGED in the reconciliation report as unaccounted-for —
  do NOT resolve its token. Leave the `BOOTSTRAP` marker, or escalate, until
  the human resolves the tension.

Resolving a `BOOTSTRAP` token is an assertion that the capability genuinely
serves the vision. Never resolve a token by inventing a vision goal to point
at — that would re-hide the very drift reconciliation just surfaced.

A re-run that changes the vision bumps `revision` and appends a `## Changelog`
entry naming the change — the same atomic act required at approval (STOP gate).

## When this skill applies

- Establishing a product's vision for the first time, or materially revising
  it — this skill.
- A single feature idea — NOT this skill; that is `change-scope` (stage 3).
- Decomposing the product into capabilities — NOT this skill; that is
  `capability-map` (stage 2), which runs after the vision exists.
- Discussion about product direction — not a trigger; answer normally.

## Precedence

`vision.md` is the root authority of the product pipeline — capabilities,
changes, specs, and issues all ultimately cite it. A project's decision
records (`docs/adr/` etc., where the project keeps them) record TECHNICAL
decisions and sit below this skill's concern; `product-vision` does not read
or write them. If product intent and a technical decision record appear to
conflict, that is a reconciliation finding for a human — flag it, do not
resolve it here.
