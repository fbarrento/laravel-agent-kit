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

## 5. The five skills

Each is one transition. Generic (kit-shipped). Each consumes the why above and
emits the why-link downward.

### 5.1 product-vision
- **Transition:** (nothing / stale vision) → `product/vision.md`.
- **Trigger:** establishing or materially revising the product's vision.
- **Input:** founder/maintainer intent.
- **Output:** `product/vision.md` — what the product is, who it serves, what
  it solves, what it explicitly is not.
- **Why-link:** none above it — this is the root why.
- **Not triggered by:** a single feature idea (that is stage 3).
- **Future responsibility:** resolve `BOOTSTRAP — no product vision yet`
  tokens left on capability stubs (§3, §5.3) into real citations to vision
  goals.

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
  decomposition logic, not just the `mkdir`.
- **Future responsibility:** review and promote the **provisional capability
  stubs** that `change-scope` creates during bootstrap (§5.3) into considered
  capability READMEs.

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
- **`capabilities/{slug}/README.md` update.** STILL OPEN. When a change ships, the
  capability's current-state README must be updated. Decide which skill owns
  that write — `spec-breakdown`, or a closing step — so the present-tense
  README does not drift from reality.
