---
name: idea-grill
description: Pressure-tests a half-formed product or feature idea on desirability, strategy, and user experience — never on feasibility or implementation — until it is sharp enough to scope. Use when an idea is vague and needs interrogating before it enters the pipeline. Produces a transient readied-idea stub that change-scope consumes. Optional front door; a well-formed idea can go straight to change-scope.
license: MIT
metadata:
  author: Francisco Barrento
---

# Idea Grill

## What this skill does

`idea-grill` takes a vague product or feature idea and interrogates it —
adversarially, on desirability and strategy — until it is sharp enough to
scope. It produces a transient readied-idea stub that `change-scope` consumes.
It is a pre-stage, not a pipeline stage: it writes no PRD, no durable artifact,
no why-link. It grills the idea; `change-scope` authors the PRD from the
sharpened result.

## When this skill applies

- A vague, half-formed feature or product idea that needs sharpening before it
  can be scoped — this skill.
- A well-formed idea whose problem, value, and shape are already clear — NOT
  this skill; go straight to `change-scope`. Grilling is the front door for
  vague ideas, never a mandatory gate.
- A product-level question (strategy, positioning, the product's reason to
  exist) — NOT this skill; that is `vision-grill`.
- Anything about how an idea would be built — NOT this skill; feasibility is
  `change-spec`'s job.

## The grill

Interrogate the idea adversarially. Your job is to find the holes, not to be
agreeable. Pursue, in no fixed order, until each has a real answer:

- **The problem.** What can the user not do today? Is the problem real, or
  assumed? Who actually has it — and how do you know?
- **The value.** What is shipping this worth, and to whom? Why now?
- **The user experience.** What is the user's journey through this? Where is
  it awkward? What is the experience if it goes wrong, or if data is missing?
- **The smallest worthwhile version.** What is the least that could ship and
  still be worth shipping? What is gold-plating?
- **The shape.** Is this one capability, or several? Does it extend an
  existing capability, or create a new one? (You classify loosely — a sharper
  classification is `change-scope`'s job.)
- **The non-goals.** What is this idea deliberately NOT? Name the boundary.

Rules of the grill:
- Stay on desirability and strategy. Never ask whether something is
  technically hard, what the data model is, or how it is built. If the idea's
  owner raises implementation, note it as out of scope for this grill and
  return to the product question.
- Push back. A grill that only agrees has failed. If an answer is thin, say
  so and ask again.
- Surface, do not resolve. When you find a contradiction or a weak point,
  NAME it and put it back to the idea's owner to resolve — do not hand them a
  reworded, cleaned-up version of their idea. Exposing the hole is your job;
  deciding how to close it is theirs. A grill that rewrites the idea into a
  more defensible shape has authored the product for the owner, however
  gently. Ask the sharp question and hold.
- Flag vision-level implications; do not resolve them. If grilling surfaces
  something that implies a change to the product's strategy or vision — a new
  way to make money, a new audience, a goal the product does not currently
  have — NAME it as a vision-level question and record it as an open item for
  the human to take to the vision. Do NOT decide it, and do NOT load or argue
  from the product's vision: your job is to grill the idea adversarially, not
  to defend the existing vision or adjudicate against it. Grilling may reveal
  the vision itself is wrong or incomplete — that is a finding, surfaced to
  the human, never settled inside the grill.
- Grill until the idea is sharp — then stop. Do not interrogate a
  already-clear idea into the ground.

## The readied-idea stub

The readied-idea stub is defined in DESIGN_PRODUCT_PIPELINE.md §5.0. When the
idea is sharp, write one — NOT a document.

Location: a clearly-transient path — `{declared-scratch-path}` if the project
declares one, else `docs/.scratch/` — never the durable state tree.
Filename: `readied-idea-{short-slug}.md`.

Content — a handful of fields, no prose narrative, no user stories, no scope
section:
- **Idea** — one line.
- **Problem** — the real problem, and who has it.
- **Value / why now** — one or two lines.
- **Smallest worthwhile version** — what the least shippable version is.
- **Shape** — one capability or several; new capability or extends an
  existing one (loose — `change-scope` classifies properly).
- **Deliberate non-goals** — the boundary.
- **Open product questions** — anything the grill could not resolve.
- **Vision-level implications** — anything the grill surfaced that implies a
  change to the product's strategy or vision (new monetization, new audience,
  a goal the product lacks). Recorded for the human to take to `product-vision`
  — not resolved here.

`change-scope` authors the PRD from this stub and does not copy it (§5.0);
once the PRD exists, delete the stub. It must never grow into a PRD — no
why-link, no status, no user stories, no scope section. If you are writing
those, you have stopped grilling and started scoping — the wrong skill.

## Handoff

End by telling the idea's owner the grill is done and the next step is
`change-scope`, which will classify the change and author its PRD from the
readied-idea stub. Do not invoke `change-scope` yourself and do not pre-empt
its work — classification and PRD authoring are its job. Your deliverable is
the sharpened idea and the stub, nothing more.

## Precedence

`idea-grill` writes nothing durable and overrides nothing. It reads no
decision records and no rule files. If the grill surfaces a question that is
really about feasibility or implementation, it does not answer it — it records
it under "Open product questions" in the stub and leaves it for `change-spec`,
downstream. The grill's authority is over the SHARPNESS of an idea, never over
what the project builds or how.
