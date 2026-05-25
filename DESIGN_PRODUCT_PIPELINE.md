# DESIGN — Product → Capabilities → Changes pipeline

**Status:** design contract. The per-skill handoff briefs derive from this
document; nothing here is a brief yet.
**Repo:** `fbarrento/laravel-agent-kit` — a family of generic pipeline skills.
**Decisions locked:** (1) the why-link is a hard, checkable requirement;
(2) skills are generic, the state-tree paths are project-declared; (3) build
order is `change-scope` and `change-spec` first.

This document is the single source of truth for how the pipeline skills
compose: stage 0 (the two grills) and stages 1, 1.5, 2, 2.5, 3, 4, 5. A skill
brief that contradicts it is wrong; fix the brief.

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
    strategy.md                     ← durable: the WHAT — personas,
                                       positioning, goals, monetization, urgency
    roadmap.md                      ← durable: the sequenced intent — which
                                       value slices, in what order, and why
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
- `roadmap.md` is product-level state — a deliberate,
  priority-and-dependency-ordered sequence of intended changes across
  capabilities. It is advisory: it guides what to build next; it gates
  nothing.

---

## 2a. The infrastructure tier

Not everything a product is built from is a capability. Below the capability
layer sits the **infrastructure tier** — substrate that capabilities consume
but that is not itself a product area.

A thing is infrastructure, not a capability, when ALL of these hold:
- a user does not experience it as a product area — it has no surface of its
  own, it is plumbing;
- it is consumed by capabilities as a dependency, typically by several;
- no vision goal names it, and naming one would be inventing a goal to satisfy
  a link.

Canonical examples: authentication and user accounts; third-party data feeds
(e.g. a market-data API); the database.

Rules of the infrastructure tier:
- Infrastructure carries **no why-link and no vision goal**. This is correct,
  not a gap: the why-link contract binds *capabilities* to vision goals, and
  infrastructure is not a capability. An infrastructure item without a goal is
  not an orphan and not a product-vision gap.
- Infrastructure is **not folded inside a capability**. Burying shared
  substrate inside one consumer creates a false dependency — other capabilities
  would reach *through* that capability for the substrate. Infrastructure sits
  *below* the capability layer, available to all consumers directly.
- The capability-vs-infrastructure call is a deliberate classification, made
  the same way the "one capability or several" call is made. If a thing a user
  genuinely experiences as a product surface is mistaken for infrastructure,
  that is a misclassification — substrate has no user-facing surface.
- A borderline case: if a thing looks like substrate but the vision implies
  users *experience* it as a product area, it is a capability and the vision
  has a gap — flag it, do not bury it as infrastructure to dodge the gap.

---

## 2b. Document versioning

A human must be able to tell, by opening a document, when it last changed and
whether what depends on it is current — without reading git history.

- Every product-level document (`vision.md`, `strategy.md`, `roadmap.md`)
  carries a `revision` integer and an `approved_on` date in its frontmatter,
  bumped on every approved change.
- Every downstream document records, in frontmatter, the `revision` of each
  upstream document it was reconciled against (`reconciled-against`).
- Staleness is then readable on the face of the document: if an upstream
  document's `revision` is higher than the `reconciled-against` value a
  downstream document records, the downstream document is STALE and must be
  re-run. No git archaeology required.

This is a readability convention, not a why-link tier — it tells a human what
is stale; it does not add an artifact to the no-orphan chain.

### Changelog

Every product-level document (`vision.md`, `strategy.md`, `roadmap.md`) and
every capability `README.md` carries a `## Changelog` section: a
reverse-chronological history, newest first, one entry per revision.

Each entry is one line:
`revision N — YYYY-MM-DD — short description of what changed and why`

Rules:
- A skill MUST NOT bump a document's `revision` without appending the matching
  changelog entry in the same act. Revision bump and changelog entry are
  atomic. A revision with no entry, or an entry with no revision bump, is a
  defect.
- The top changelog entry's revision MUST equal the frontmatter `revision`.
- Entries are decision-level and short — what changed, and why (the trigger:
  a reconciliation finding, a human decision, an upstream revision). Not a
  diff. One or two sentences.
- The changelog is append-only. Past entries are never edited or removed —
  the history is the point.

---

## 3. The why-link — hard, checkable, the spine of the system

Every artifact cites the why of the stage above it. An artifact without a
valid upward link is **invalid** — a skill that emits one has produced an
orphan, and that fails verification.

| Artifact | MUST cite |
|---|---|
| `product/strategy.md` | a goal in `product/vision.md` |
| each item in `product/roadmap.md` | a goal in `product/strategy.md` |
| `capabilities/{slug}/README.md` | a goal in `product/vision.md` |
| `changes/{NNNN}/prd.md` | its capability's `README.md` + states its own product why |
| `changes/{NNNN}/spec.md` | its `prd.md` |
| each issue in `issues.md` | a `spec.md` section + the governing rule file(s) |

"Cite" means a **resolvable path-and-section** — a real file, a real heading —
not a remembered title or a commit reference. Reconstructing the upstream why
from a filename, a commit message, or memory does NOT satisfy the link. This
is the no-orphan check from the routing-table work, applied to the pipeline.

**The full chain.** The product model is vision → strategy → roadmap, and
every artifact's mandatory citation is the table above. Two facts must be held
together, and they do not contradict:

- **The mandatory spine** a shipped line of code traces upward is
  issue → spec → PRD → capability → **vision**. A capability `README.md` cites
  a **vision goal directly** — that is its mandatory link, and it is CORRECT,
  never a chain break. A capability may additionally relate to the strategy,
  but its required citation is the vision.
- **The roadmap thread runs in parallel.** `strategy.md` cites a vision goal;
  each `roadmap.md` item cites a strategy goal (→ vision via the strategy).
  When a PRD cites its roadmap item, the change threads
  change → roadmap item → strategy → vision **alongside** the spine. Citing a
  roadmap item is optional (the roadmap is advisory, §5.2a); the spine is not.

A capability citing the vision directly while the roadmap cites the strategy is
**by design** — it is not an inconsistency, a chain break, or a gap to work
around.

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

**Changelog defect check (amendment).** A fourth check joins the same
verification family: on every product-level document and every capability
README, the top `## Changelog` entry's revision MUST equal the frontmatter
`revision` (§2b Changelog). A `revision` bumped without a matching changelog
entry — or an entry without a bump — is a defect.

Why this is the spine: it is what stops stage N from rationalizing stage N-1.
A skill cannot invent a why — it must cite the why above it. Remove this rule
and "product → capabilities → changes" is just three folders; with it, it is
an auditable chain of justification from a line of code up to the product
vision.

Infrastructure-tier items (§2a) sit outside this chain entirely: they carry no
why-link and no vision goal by definition — their absence of a goal is
correct, not an orphan.

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
   and *reads* the product-level stages (vision, strategy, capabilities,
   roadmap) as settled state. The pipeline must run partially — if it only
   works end-to-end it becomes ceremony and gets routed around. And a one-line
   bug fix triggers none of the pipeline stages; the classify step in
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

## 5. The pipeline skills

Each is one transition. Generic (kit-shipped). Each consumes the why above and
emits the why-link downward. Stage 0 (the two grills) feeds the pipeline;
stages 1, 1.5, 2, 2.5, 3, 4, 5 run it.

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

**Vision-level implications are flagged, never resolved.** Grilling sometimes
surfaces something that implies a change to the product's strategy or vision —
new monetization, a new audience, a goal the product lacks. A grill NAMES it
as a vision-level question and records it (in the readied-idea stub) for the
human to take to `product-vision`. A grill never decides it, and never loads
or argues from the vision — it grills the idea adversarially, it does not
defend or adjudicate against the existing vision.

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
- **Personas live in the strategy, not here.** A vision is short and
  aspirational; target-customer definitions and personas are a strategy
  artifact (§5.1a), not a vision section.

### 5.1a product-strategy  *(stage 1.5)*
- **Transition:** `product/vision.md` → `product/strategy.md`.
- **Trigger:** establishing or revising the product's strategy.
- **Input:** the approved `vision.md` + human intent about market, customers,
  positioning, monetization, and urgency.
- **Output:** `strategy.md` — the WHAT between the vision's why and the
  roadmap's when: target customers and **personas**, positioning, measurable
  goals, **monetization**, and **time-to-market urgency**.
- **Why-link:** `strategy.md` cites a vision goal.
- **Authored from intent**, never derived from the codebase, capabilities, or
  the readied-idea stub; reconciled against the vision with findings flagged
  for a human. Kept concise — a strategy nobody can internalize is dead.
- **Approval:** human-approved like the vision; carries `revision` /
  `reconciled-against` for visible versioning (§2b).
- **The roadmap and capabilities serve it:** `product-roadmap` sequences value
  slices to serve the strategy (and its time-to-market urgency); capabilities
  are shaped to serve it.
- **Refuses without an approved vision.** No vision → the strategy has nothing
  to serve → STOP.
- **Build order:** stage 1.5, built and runs after `product-vision`.

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
- **Build order:** runs AFTER `product-vision` (stage 1) — the vision it
  decomposes against — and is built after `product-strategy` (stage 1.5) in
  pipeline order (see §7).

### 5.2a product-roadmap  *(stage 2.5)*
- **Transition:** `product/strategy.md` + the capability map →
  `product/roadmap.md`.
- **Trigger:** establishing or revising the product's roadmap.
- **Input:** `strategy.md` (and the vision it serves) and the set of
  `capabilities/{slug}/README.md`.
- **Output:** `roadmap.md` — a sequence of value slices across capabilities,
  ordered de-risk → ROI → dependency (below). Never by dates.
- **A roadmap item is a value slice, not a capability** — the smallest
  coherent increment that delivers user value, which may use only PART of a
  capability or SPAN several. A capability is usually delivered by several
  slices over several items; an item that is a whole capability has not been
  broken down.
- **Ordering: de-risk first, then ROI, within hard dependencies.** The
  cheapest slice testing an unproven existential bet the strategy names leads,
  ahead of value-÷-effort ranking; a low-ROI enabler of a high-value slice is
  evaluated as a pair, by the value ultimately unlocked.
- **Commits to ordering; never defers it.** The roadmap decides every slice's
  position — including enabler-pairs and close calls — and justifies it; it
  never hands an ordering judgment back to the human via a flag ("promote
  if…"). Surfacing genuine findings (no why-link, missing capability, vision
  gap) remains required and is distinct from deferring an ordering decision.
- **Why-link:** each roadmap item cites a strategy goal (→ vision via the
  strategy, per §3).
- **Authored top-down.** The roadmap is authored FROM the strategy and the
  capability map — what the product should do next. It is NEVER derived
  bottom-up from the changes that already exist; a roadmap assembled from
  scoped changes reports activity instead of expressing intent.
- **Advisory, not a gate.** A roadmap item is the RECOMMENDED upstream of a
  change — when its turn comes it feeds `idea-grill` / `change-scope` as a
  prioritized starting point. But a change may enter the pipeline without a
  roadmap item. A PRD MAY cite a roadmap item (`roadmap-link`); if it does,
  the why-link thread extends upward through the strategy to the vision; if it
  does not, nothing breaks.
- **Human-approved.** The roadmap is produced as a proposal and approved by a
  human, like the vision, strategy, and capability map; it carries
  `revision` / `reconciled-against` for visible versioning (§2b).
- **Re-runnable.** The roadmap is durable state and can go stale as the
  strategy shifts or `capability-map` reshapes capabilities. `product-roadmap`
  re-runs: it reconciles the existing roadmap against the current strategy and
  capability map and re-proposes — the same review-and-reconcile pattern
  `product-vision`, `product-strategy`, and `capability-map` use.
- **No dates.** The roadmap sequences by de-risk, ROI, and dependency — never
  by dates. Dated promises slip, the roadmap lies, and a roadmap nobody trusts
  violates the source-of-truth principle louder than anything else.

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

**Implementation is not a further pipeline skill.** It is the existing code
STOP gate in `laravel-rules` / `inertia-rules`, fed by issues that already
carry their authority. The pipeline ends at issues; the gate takes over.

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
3. **spec-breakdown** — stage 5, last of the original change pipeline (the
   later items below were added by subsequent amendments).
4. **vision-grill** + **idea-grill** — stage 0, built once the pipeline they
   feed is complete. Each is a pre-stage producing a transient readied-idea
   stub, not a pipeline artifact.
5. **product-roadmap** — stage 2.5, built after `capability-map` (it sequences
   changes across capabilities, so it needs the capability map) and before
   the change pipeline. Advisory; not a gate.
6. **product-strategy** — stage 1.5, built after `product-vision` (it serves
   the vision and refuses to run without one) and before `capability-map` /
   `product-roadmap`, which it in turn governs.

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
- **Infrastructure tier.** RESOLVED (infrastructure-tier amendment). Substrate
  consumed by capabilities — authentication, third-party data feeds, the
  database — is the infrastructure tier (§2a): below the capability layer, no
  why-link, no vision goal, not folded into any capability.
- **Strategy layer.** RESOLVED (product-strategy amendment). Personas,
  positioning, measurable goals, and monetization belong to `strategy.md`
  (§5.1a, stage 1.5) — the WHAT between the vision's why and the roadmap's
  when — not to the vision or the roadmap. The roadmap sequences value slices
  to serve the strategy and its time-to-market urgency.
- **Document versioning.** RESOLVED (product-strategy amendment). Product-level
  documents carry a `revision`; downstream documents record
  `reconciled-against`; staleness is readable on the face of a document
  without git (§2b).
- **Document changelog.** RESOLVED (changelog amendment). Every product-level
  document and every capability README carries an append-only `## Changelog`;
  a `revision` bump and its changelog entry are one atomic act, enforced in
  every skill that writes these documents.
- **Roadmap ordering.** RESOLVED (de-risk amendment). The roadmap sequences
  de-risking slices first (cheapest test of each unproven existential bet the
  strategy names), then by ROI, within hard dependencies. A roadmap that ranks
  the bet-testing slice below feature slices has the wrong sort key.
- **Roadmap commits to ordering.** RESOLVED (commit amendment). The roadmap
  decides every slice's position and justifies it; it never ships an ordering
  flag ("promote if…") in place of a decision. This generalizes the
  value-slice and de-risk amendments — roadmap ordering is now complete.

---

## 9. The verification family

The invariants the skills enforce, collected for audit. This section
introduces nothing — each is defined in the section pointed to.

- **No-orphan** (§3) — every capability cites a vision goal; no artifact is
  left unaccounted for above it.
- **Resolvable why-link** (§3) — every why-link is a real, resolvable
  path-and-section; an unresolved link is invalid.
- **Drift invariant** (§3, §5.5) — a capability `README.md` matches reality
  because the same merge that changes the capability updates it.
- **Changelog defect check** (§2b, §3) — a document's top `## Changelog`
  entry's revision equals its frontmatter `revision`; a revision bump without
  a matching entry (or an entry without a bump) is a defect.
- **Staleness check** (§2b) — a downstream document whose `reconciled-against`
  upstream revision is lower than the upstream's current `revision` is stale
  and must be re-run.
- **Infrastructure tier** (§2a) — substrate carries no why-link and no vision
  goal and is not folded into a capability; this is correct, not a gap.
