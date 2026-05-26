# Archived — the product-pipeline experiment

This directory holds an exploration of an **AI-driven product-development
pipeline**: a chain of skills that took a product from a vague idea through
vision, strategy, capability mapping, roadmap, scoping, technical spec, and
issue breakdown, with a why-link spine binding every artifact up to the
product vision.

```
DESIGN_PRODUCT_PIPELINE.md   the design contract for the whole pipeline
idea-grill / vision-grill    stage 0 — pre-pipeline interrogation
product-vision               stage 1 — the root why
product-strategy             stage 1.5 — personas, positioning, monetization
capability-map               stage 2 — decompose the product into capabilities
product-roadmap              stage 2.5 — sequence value slices
change-scope                 stage 3 — a raw idea → PRD
change-spec                  stage 4 — PRD → technical spec
spec-breakdown               stage 5 — spec → implementation issues
```

## Status

**Superseded and retained for reference — not maintained.** The decision is to
use [GitHub Spec Kit](https://github.com/github/spec-kit) for spec-driven
development instead of this bespoke pipeline. These skills are kept for their
design notes and ideas, not for use; they are not installed by the kit, not
linted in CI, and will not be updated.

The maintained part of this repo is the convention-skills kit in `skills/`
(see the top-level [README](../../README.md)).
