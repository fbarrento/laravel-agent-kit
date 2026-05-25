---
name: vision-grill
description: Pressure-tests a product on strategy, positioning, market, and reason to exist — never on feasibility or implementation — until it is sharp enough to set a vision from. Use when a product idea is vague and needs interrogating before product-vision runs. Produces a transient readied-idea stub that product-vision consumes. Optional front door; a clear product idea can go straight to product-vision.
license: MIT
metadata:
  author: Francisco Barrento
---

# Vision Grill

## What this skill does

`vision-grill` takes a vague product idea and interrogates it — adversarially,
on strategy, positioning, market, and the product's reason to exist — until it
is sharp enough to set a vision from. It produces a transient readied-idea
stub that `product-vision` consumes. It is a pre-stage, not a pipeline stage:
it writes no `vision.md`, no durable artifact, no why-link. It grills the
product idea; `product-vision` authors the vision from the sharpened result.

## When this skill applies

- A vague product idea that needs sharpening before a vision can be set — this
  skill.
- A product whose purpose, audience, and positioning are already clear — NOT
  this skill; go straight to `product-vision`. Grilling is the front door for
  vague product ideas, never a mandatory gate.
- A single feature idea — NOT this skill; that is `idea-grill`.
- Anything about how the product would be built, or marketing execution
  (campaigns, channels, copy) — NOT this skill.

## The grill

Interrogate the product idea adversarially. Find the holes; do not be
agreeable. Pursue, until each has a real answer:

- **The problem space.** What problem does this product exist to remove? Is it
  real and felt, or assumed? What do people do today instead?
- **The audience.** Who is this for — specifically? Who is it NOT for?
- **Reason to exist.** Why should this product exist at all? What changes for
  its users if it does? Why now?
- **Positioning.** How is this different from what people already use? What is
  the one-sentence statement of what it is?
- **The boundary.** What is this product deliberately NOT? Name the non-goals
  — the things it will refuse to become.
- **Coherence.** Do the answers above hang together as one product, or do they
  describe two?

Rules of the grill:
- Stay on strategy and desirability. Never ask about tech stack, architecture,
  or build effort. Never drift into marketing execution — campaigns, copy,
  channels are not this grill's concern; positioning and audience are.
- Push back. A grill that only agrees has failed. If an answer is thin, say so
  and ask again.
- Grill until the product idea is sharp — then stop.

## The readied-idea stub

When the product idea is sharp, write a transient readied-idea stub — NOT a
document, and NOT a vision.

Location: a clearly-transient path — `{declared-scratch-path}` if the project
declares one, else `docs/.scratch/` — never the durable state tree.
Filename: `readied-product-{short-slug}.md`.

Content — a handful of fields, no prose narrative, no vision goals:
- **Product** — one line: what it is.
- **Problem space** — the problem it removes, and for whom.
- **Audience** — who it is for, and who it is not.
- **Reason to exist / why now** — one or two lines.
- **Positioning** — how it differs from what exists.
- **Deliberate non-goals** — what the product refuses to be.
- **Open strategy questions** — anything the grill could not resolve.

The stub is scratch input. It is consumed and superseded by `product-vision`,
which AUTHORS `vision.md` from it — `product-vision` does not copy it. Once the
vision exists, the stub is spent; delete it. The stub must never grow into a
vision: no vision goals, no why-link, no status. If you are writing vision
goals, you have stopped grilling and started authoring — the wrong skill.

## Handoff

End by telling the product owner the grill is done and the next step is
`product-vision`, which will author `vision.md` from the readied-idea stub —
eliciting any remaining intent, reconciling against existing capabilities, and
resolving bootstrap tokens. Do not invoke `product-vision` yourself and do not
pre-empt its work. Your deliverable is the sharpened product idea and the
stub, nothing more.

## Precedence

`vision-grill` writes nothing durable and overrides nothing. It reads no
decision records and no rule files. If the grill surfaces a question about
feasibility, implementation, or marketing execution, it does not answer it —
it records strategy questions under "Open strategy questions" in the stub and
drops the rest. The grill's authority is over the SHARPNESS of a product idea,
never over what gets built or how it is taken to market.
