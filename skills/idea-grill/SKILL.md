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
- Grill until the idea is sharp — then stop. Do not interrogate a
  already-clear idea into the ground.

## The readied-idea stub

When the idea is sharp, write a transient readied-idea stub — NOT a document.

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

The stub is scratch input. It is consumed and superseded by `change-scope`,
which AUTHORS the PRD from it — `change-scope` does not copy it. Once the PRD
exists, the stub is spent; delete it. The stub must never grow into a PRD: no
why-link, no status, no user stories, no scope section. If you are writing
those, you have stopped grilling and started scoping — that is the wrong
skill.

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
