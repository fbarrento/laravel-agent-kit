# Handoff — laravel-rules v2, Pass 2 deepening

## Mission

Deepen `skills/laravel-rules` rule files to full content. PRD = GitHub
issue #1 (`fbarrento/laravel-agent-kit`). Pass 1 (reorg) done + pushed.

## State (done, on `main`)

- `e436072` — saloon-integration + saloon-laravel-integration skills.
- `a73036f` — Pass 1 reorg of laravel-rules (#1).
- `17bf291` — vendored mattpocock/skills into `.agents/skills`.
- Uncommitted: `README.md` (pre-existing edit, not mine, leave alone).

## Pass 1 result

`skills/laravel-rules/` = `SKILL.md` (thin map) + `rules/` 18 folders, 30 leaves.

Written full (NOT stubs):
- `architecture/placement.md` — placement test (canonical).
- `architecture/structure.md` — flat folders + nesting-exception registry.
- `architecture/cqrs.md`, `architecture/dependency-injection.md`.
- `architecture/transactions.md` — tx boundaries + after-commit + dispatch-from-actions.
- `architecture/invariants.md` — invariant ownership (when-to-use tree = TODO).
- `actions/conventions.md`, `jobs/conventions.md` — hoisted out, link-stubs left.
- Verbatim moves: `naming/`, `database/migrations.md`, `models/`, `queries/`, `testing/`.

Stubs (scope + TODO + empty checklist, marked `_(stub)_` in SKILL.md):
`patterns/{pipeline,pluggable}`, `packages/{policy,catalog}`, `data-objects`,
`value-objects`, `enums`, `exceptions`, `events`, `observers`, `http`,
`queues`, `logs`, `database/{schema,performance,mysql,postgres}`.

## Pass 2 order (priority)

1. `architecture/` finish (invariants when-to-use tree) + `patterns/{pipeline,pluggable}` — linchpins, everything links here.
2. `actions/`, `data-objects/`, `value-objects/`.
3. Rest: enums, exceptions, events, observers, http, queues, logs, database/*, packages/*.

Each leaf = its own commit. Reference #1.

## Hard rules (from grill — do NOT violate)

- **Placement test** decides every rule home: (1) internals of one class type -> block folder; (2) settled global rule -> `architecture/`; (3) optional per-case technique -> `patterns/`. "Is it a pattern?" NOT a reason. See `architecture/placement.md`.
- **One canonical home** per cross-cutting rule. Other folders = one-line link-stub, never restate. Drift = bug.
- **Per-file template**: Rule -> Why (mandatory) -> Good/Bad pair -> Edge cases -> Checklist. **Decision** section where rule is a choice (decision tree/criteria).
- **Uniform folders**: every domain = folder, `conventions.md` anchor (or obvious anchor like `migrations.md`). Stable paths.
- Laravel APP structure stays flat. Only exception = nesting registry (`app/Data/Casts`, `app/Data/Transformers`). This skill reorganizes DOCS, not apps.
- Pipeline + pluggable = patterns (opt-in), 2 files. CQRS = policy (mandatory) -> architecture, despite pattern lineage.
- Action kinds = simple vs orchestrator (Decision in `actions/conventions.md`). Pipeline NOT an action kind.

## Content seeds for stubs (from grill, already in TODO blocks)

- `invariants` tree: true domain invariant (action) vs input validation (form request/data obj) vs DB constraint.
- `data-objects`: input vs result DTOs, Casts/Transformers, validation boundary, to-array tests.
- `value-objects`: immutable, value-equality, when vs scalar/enum/data-obj.
- `observers`: guardrail — prefer actions/events, narrow acceptable cases.
- `packages/policy`: health/scope/lock-in/security/"is it core domain". `catalog`: spatie/laravel-data, saloonphp (-> saloon-laravel-integration skill).
- `database` split: portable rules in schema/migrations/performance; engine quirks in mysql/postgres.

## Testing decision (PRD)

Only validation = **link/reference integrity** check: all cross-refs + link-stubs resolve, SKILL.md indexes every leaf. No template-lint, no code-compile. Could be small CI/pre-commit script (none in repo yet).

## Gotchas

- Bash cwd persists between calls — earlier `cd` drifted. Use abs paths.
- `git mv` for moves to keep history; big content rewrites show delete+add (fine).
- Commit msg footer: `Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>`. Commit/push only when user asks.
- `.claude/skills/*` = symlinks (mode 120000) -> break on Windows checkout. Known, not blocking.
