# DESIGN — Product → Capabilities → Changes pipeline

**Status:** design contract. The per-skill handoff briefs derive from this
document; nothing here is a brief yet.
**Repo:** `fbarrento/laravel-agent-kit` — five new generic skills.
**Decisions locked:** (1) the why-link is a hard, checkable requirement;
(2) skills are generic, the state-tree paths are project-declared; (3) build
order is `change-scope` and `change-spec` first.

This document is the single source of truth for how the five skills compose.
A skill brief that contradicts it is wrong; fix the brief.

---

## 1. The two halves — never conflate them

**State** — durable artifacts on disk, in the consuming project.
**Skills** — generic processes, shipped by the kit, that read and write state.

A skill is a *transition between states*. A skill is never itself a layer.
"Manage a capability" is not a skill — it is a folder that skills act on. If a
skill and a layer become the same thing, the why has no clean place to live
and the pipeline rots. Skills are verbs; folders are nouns.

---

## 2. The state tree (project-declared paths)

Canonical default shape. The kit's skills define this *shape*; each consuming
project's `CLAUDE.md` declares the actual root path. A skill must never
hard-code `docs/` — it reads the path the project declares, exactly as the
existing skills treat `docs/adr/`.

```
docs/
  product/
    vision.md                       ← durable: what the product is, who it
                                       serves, what it solves. The root why.
  capabilities/
    {capability-slug}/
      README.md                     ← durable: what this capability IS today,
                                       from the user's perspective.
      changes/
        {NNNN-change-slug}/
          prd.md                    ← the WHY of one change.
          spec.md                   ← the HOW of one change.
          issues.md                 ← the breakdown into tasks.
```

Rules of the tree:
- A **capability** is a durable area of the product. `{capability-slug}` names
  the capability — never a release, a version, or a project (`watchlists`, not
  `q3-revamp` or `watchlists-v2`).
- A **change** is one unit of intent applied to a capability — the first build,
  an extension, a refactor are all changes. Numbered per capability
  (`0001`, `0002`), so the number is the change's place in that capability's
  history.
- `capabilities/{slug}/README.md` is the **present tense** — current state,
  updated when a change ships. `changes/NNNN/prd.md` is the **history** — why
  it became that, change by change.
- A refactor does not get its own folder. It is a change inside the
  capability's `changes/` series.

---

## 3. The why-link — hard, checkable, the spine of the system

Every artifact cites the why of the stage above it. An artifact without a
valid upward link is **invalid** — a skill that emits one has produced an
orphan, and that fails verification.

| Artifact | MUST cite |
|---|---|
| `capabilities/{slug}/README.md` | a goal in `product/vision.md` |
| `changes/{NNNN}/prd.md` | its capability's `README.md` + states its own product why |
| `changes/{NNNN}/spec.md` | its `prd.md` |
| each issue in `issues.md` | a `spec.md` section + the governing rule file(s) |

"Cite" means a **resolvable path-and-section** — a real file, a real heading —
not a remembered title or a commit reference. Reconstructing the upstream why
from a filename, a commit message, or memory does NOT satisfy the link. This
is the no-orphan check from the routing-table work, applied to the pipeline.

**Bootstrap resolution (amendment).** A PRD always cites a real, resolvable
capability `README.md` — if none exists, `change-scope` creates a provisional
capability stub to be that parent (see §5.3). The only tolerated declared-gap
token is `BOOTSTRAP — no product vision yet`, permitted **solely** on a
capability stub's vision link, at the capability→vision tier — never on any
other link. `product-vision` later resolves these tokens into real citations
(§5.1).

**Drift invariant (amendment).** Alongside the no-orphan and
resolvable-why-link checks, a third belongs to the same verification family: a
change whose implementation merged with its building blocks touched, but whose
capability `README.md` was not updated in that merge, is a source-of-truth
violation. `spec-breakdown` enforces it by drafting the README update as the
final issue, landed atomically with the implementation (§5.5).

Why this is the spine: it is what stops stage N from rationalizing stage N-1.
A skill cannot invent a why — it must cite the why above it. Remove this rule
and "product → capabilities → changes" is just three folders; with it, it is
an auditable chain of justification from a line of code up to the product
vision.

---

## 4. Three contract rules every skill obeys

1. **Why-link is mandatory** (section 3). Every output artifact carries a
   valid upward citation; producing an orphan fails.
2. **A skill is a router, not a rulebook.** When a skill references how a
   building block is built, it cites the `laravel-rules` / `inertia-rules`
   rule-file *path* — it never summarizes the rule. Summarizing rebuilds the
   cheat-sheet bug across a skill boundary, where agents read the summary
   instead of the rule.
3. **Enter at any stage; over-fire at none.** Most work enters at stage 3 or 4
   and *reads* stages 1–2 as settled state. The pipeline must run partially —
   if it only works end-to-end it becomes ceremony and gets routed around. And
   a one-line bug fix triggers none of the five skills; the classify step in
   `change-scope` must be allowed to answer "in-shape — go to the code gate."

---

## 4a. The desirability / feasibility line

Stage 0 (grilling) interrogates an idea on **desirability and strategy** — and
never on **feasibility or construction**. This line is absolute.

- In scope for a grill: the problem and who has it; whether the problem is
  real; value and why-now; market and positioning; the user experience and
  journey; deliberate non-goals; whether an idea is one capability or several.
- Out of scope, hard: anything about how it is built — architecture, data
  shapes, the stack, effort estimates, sequencing. The moment a grill asks
  "is this technically hard", it has become a feasibility review, which is
  `change-spec`'s job.

Marketing-as-strategy (positioning, audience, why-anyone-cares) is in scope.
Marketing-as-execution (campaigns, copy, channels, launch plans) is a separate
discipline and is NOT what a grill does. A grill sharpens whether and why; it
does not write the go-to-market.

---

## 5. The five skills

Each is one transition. Generic (kit-shipped). Each consumes the why above and
emits the why-link downward.

### 5.0 Stage 0 — pre-pipeline grilling (optional)

Stage 0 is two **grill** skills. A grill is a PRE-STAGE: it interrogates an
idea and hands a sharpened input to a producer skill. A grill is not a
pipeline stage — it produces no durable artifact and carries no why-link.

- **`vision-grill`** — pressure-tests a PRODUCT: strategy, positioning,
  market, the product's reason to exist. Feeds `product-vision` (stage 1).
- **`idea-grill`** — pressure-tests a single IDEA: the problem, the user
  experience, the smallest worthwhile version, one-capability-or-three. Feeds
  `change-scope` (stage 3).

Two grills, not one, because they interrogate different-sized things:
product-level strategy belongs next to the vision; change-level UX belongs
next to a change. Folding marketing/strategy into the idea grill would
re-litigate product strategy on every feature idea.

**Readied-idea handoff.** A grill ends by writing a short, structured
**readied-idea stub** — NOT a document. A handful of fields: the problem, the
audience, the why-now, the deliberate non-goals, and (for `idea-grill`) the
one-capability-or-three call. No prose narrative, no user stories, no scope
section. The stub:
- is TRANSIENT — it is scratch input, not a durable pipeline artifact;
- carries no `why-link` and no `status`;
- lives in a clearly-transient location, never in the durable state tree;
- is CONSUMED AND SUPERSEDED by the producer skill — once the PRD or vision is
  authored, the stub is spent and is deleted.

The producer skill (`change-scope` / `product-vision`) AUTHORS from the stub;
it does not copy it. The stub must never grow into a PRD or a vision — that
would re-weld idea-interrogation and why-authoring into one step, the bug the
pipeline exists to prevent.

**Stage 0 is optional.** A well-formed idea enters the pipeline directly at
stage 1 or stage 3. The grills are the front door for vague ideas, not a gate.

### 5.1 product-vision
- **Transition:** (nothing / stale vision) → `product/vision.md`.
- **Trigger:** establishing or materially revising the product's vision.
- **Input:** founder/maintainer intent.
- **Output:** `product/vision.md` — what the product is, who it serves, what
  it solves, what it explicitly is not.
- **Why-link:** none above it — this is the root why.
- **Not triggered by:** a single feature idea (that is stage 3).
- **Three parts:** (1) elicit the vision from human product intent; (2)
  reconcile it against any capabilities the project has already grown,
  producing a reconciliation report of drift flagged for a human; (3) gated
  `BOOTSTRAP`-token resolution. The vision is authored from human intent and
  NEVER derived from the codebase or the stubs — a vision traced from what got
  built can only ratify the product, never judge it.
- **Approval:** `vision.md` carries human-approval frontmatter (`status` /
  `approved_by` / `approved_on`) — the highest-stakes artifact in the
  pipeline.
- **`BOOTSTRAP`-token resolution is gated** on the reconciliation: a stub the
  reconciled vision justifies has its `BOOTSTRAP — no product vision yet`
  (§3, §5.3) replaced with a real vision-goal citation; a capability flagged
  as unaccounted-for KEEPS its token until a human resolves the tension.
- **Build order:** `product-vision` (stage 1) is built and runs before
  `capability-map` (stage 2) — `capability-map` refuses to run without
  `vision.md`.

### 5.2 capability-map
- **Transition:** `product/vision.md` → the set of
  `capabilities/{slug}/README.md`.
- **Trigger:** decomposing the product into capabilities, or adding/retiring a
  capability.
- **Input:** `product/vision.md`.
- **Output:** one `README.md` per capability — what the capability is, today.
- **Why-link:** each `README.md` cites a vision goal.
- **Owns the judgment:** "is this one capability or three." This is
  architectural reasoning, not folder scaffolding — the skill owns the
  decomposition logic, not just the `mkdir`. It promotes the **provisional
  capability stubs** `change-scope` creates during bootstrap (§5.3) into
  considered capability READMEs.
- **Refuses without a vision.** No approved `vision.md` → no criterion to
  decompose against → STOP.
- **Batch proposal, human-approved.** Produces ONE considered decomposition of
  the whole product at once — not stub-by-stub — as a PROPOSAL; nothing in the
  state tree is rewritten before a human approves it (a skill that can
  mass-break `why-link`s must not act unreviewed).
- **Reshaping a populated capability is a migration.** A merge / split /
  rename of a capability that already has a `changes/` history moves the
  affected `changes/` folders and rewrites every `why-link` / `capability:`
  field that pointed at the old capability — applied atomically so every link
  resolves again. A capability with shipped changes is reshaped, **never
  erased**; its history is real and moves with it.
- **Build order:** built and runs AFTER `product-vision` (stage 1). This is
  the last of the five pipeline skills — stages 1–5 are complete.

### 5.3 change-scope  *(build first)*
- **Transition:** a raw idea → `changes/{NNNN}/prd.md`.
- **Trigger:** a feature idea, an extension, or a refactor request for the
  product.
- **Input:** the idea + `product/vision.md` + the relevant capability
  `README.md` (read, not re-derived).
- **First action — CLASSIFY:** new capability / change to an existing
  capability / in-shape work needing no pipeline. The classification reasoning
  is stated explicitly and, for a change to an existing capability, is made
  only AFTER reading that capability's existing PRDs and decision records —
  because the prior decisions are often what make a change architectural.
- **Output:** `changes/{NNNN}/prd.md` — the problem, the user's current pain,
  the product value, user stories, scope. The PRD owns the WHY. It does NOT
  make technical decisions (no cast choices, no class shapes).
- **Why-link:** the PRD cites the capability `README.md`. When the target
  capability does not yet exist, `change-scope` creates a **provisional
  capability stub** (folder + one-paragraph README, status `provisional`) as
  the anchor the PRD cites — it must NOT write a considered capability
  description, scope, or decomposition into that stub; that is
  `capability-map`'s exclusive output.
- **Test of a good PRD:** a non-engineer can read it and disagree with it. If
  half the PRD is only meaningful to someone who has read `laravel-rules`, the
  why and the how have been welded — the pipeline ran in the wrong order.
- **Runs BEFORE any spec.** This ordering is the fix for the observed bug
  where the PRD was back-filled from an implementation plan.

### 5.4 change-spec  *(build first)*
- **Transition:** `changes/{NNNN}/prd.md` → `changes/{NNNN}/spec.md`.
- **Trigger:** producing the technical spec for a scoped change.
- **STOP-gate precondition:** an approved `prd.md` with a valid capability
  why-link must exist. No PRD → no why to implement → stop. This precondition
  is what structurally prevents jumping straight to migrations.
- **Input:** the `prd.md` + the relevant decision records (conditional — read
  bodies, see section 6).
- **Output:** `spec.md` — building-blocks table (each row: name · type ·
  `new`/`restructured`/`removed` · governing rule-file path · constraining
  decision-record IDs · deliberate deviations) + decision records consulted +
  inferences/open questions + proposed/superseded decision records.
- **Why-link:** the spec cites the `prd.md`.
- **Routes to** `laravel-rules` / `inertia-rules` by rule-file path only
  (contract rule 2). Owns the judgment of splitting a change into one spec vs
  several (e.g. a domain spec + an HTTP spec).
- **Approval:** the spec carries human-approval frontmatter (`status` /
  `approved_by` / `approved_on`), invalidated on edit — the same mechanism as
  the PRD; `spec-breakdown` consumes only an approved spec.

### 5.5 spec-breakdown
- **Transition:** `changes/{NNNN}/spec.md` → `changes/{NNNN}/issues.md`.
- **Trigger:** breaking an approved spec into implementation tasks.
- **Input:** `spec.md`.
- **Output:** ordered tasks, each naming its building block(s) and therefore
  carrying its rule file(s) and decision-record IDs forward.
- **Why-link:** each issue cites a spec section.
- **How it breaks down:** assigns each building block to one of six
  **dependency-role layers** (L1 persistence · L2a read contract · L2b write
  logic · L3 delivery surfaces · L4 UI primitives · L5 UI pages), splits each
  layer into independently mergeable issues by cohesion (the "mergeable alone
  without breaking `main`" test), and attaches a per-issue **review weight**
  and **completion contract** (no standalone "write tests" issue; checks
  sourced from the rules skills, conditional on project tooling).
- **Keeps the repo true:** drafts the capability `README.md` update, delivered
  as the final issue and landed **atomically** with the implementation. On a
  capability's first ship it de-provisionalizes the `change-scope` stub with a
  factual present-tense README (decomposition/vision relation stay
  `capability-map`'s).

**Implementation is not a sixth skill.** It is the existing code STOP gate in
`laravel-rules` / `inertia-rules`, fed by issues that already carry their
authority. The pipeline ends at issues; the gate takes over.

---

## 6. Decision records — conditional, as always

`docs/adr/`, `docs/postmortem/`, `docs/learnings/` are per-project and
optional. No pipeline skill may hard-require them. `change-scope` and
`change-spec` read them IF the project keeps them; the project's `CLAUDE.md`
declares which exist. When a change supersedes or contradicts an existing
decision record, the spec flags it for a human ruling and may propose a
superseding record — it never silently overrides one. Reading a record means
reading the document body, never its title or a commit message.

---

## 7. Build order

1. **change-scope** + **change-spec** — stages 3–4. They deliver value on the
   next feature and force the PRD→spec contract everything else inherits.
2. **product-vision** + **capability-map** — stages 1–2, once the contract is
   proven.
3. **spec-breakdown** — last.
4. **vision-grill** + **idea-grill** — stage 0, built last, once the pipeline
   they feed is complete. Each is a pre-stage producing a transient
   readied-idea stub, not a pipeline artifact.

Per-skill briefs are written in that order. Each brief: frontmatter (matching
the kit's existing SKILL.md shape — `name`, `description`, `license`,
`metadata.author`), STOP gate / trigger, input artifact, output artifact, the
why-link header it produces, the upward link it checks, cross-skill routing,
and verification (path-resolvable why-link check; `python3
scripts/lint-skills.py`).

---

## 8. Open questions

- **Numbering authority.** RESOLVED (change-scope brief). `change-scope` scans
  the capability's `changes/` and takes the next free integer, zero-padded
  (`0001`…). The number is PROVISIONAL until merge; the SLUG is the change's
  identity and every intra-change why-link cites the slug, never the bare
  number. A parallel-mint collision is a loud merge-time rename, not a bug.
- **PRD approval.** RESOLVED (change-scope brief). "Approved" = an explicit
  human act recorded in `prd.md` frontmatter (`status: approved`,
  `approved_by`, `approved_on`). The agent never sets it from its own
  judgment, and any later edit to the PRD invalidates it — resetting to
  `draft` until re-approved. `change-spec` consumes a PRD only when these
  fields are populated and current.
- **`capabilities/{slug}/README.md` update.** RESOLVED (spec-breakdown brief).
  `spec-breakdown` owns the write: it drafts the present-tense README update
  as the final issue, which lands atomically with the implementation it
  describes (and clears the `provisional` stub on first ship). The
  present-tense README cannot drift from reality because the same merge that
  touches the building blocks updates it.
