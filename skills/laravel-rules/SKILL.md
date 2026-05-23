---
name: laravel-rules
description: Applies Francisco Barrento's Laravel, Pest, model, and naming conventions that override generic Laravel guidance. Use when writing, editing, reviewing, or refactoring Laravel PHP code in this project — actions, queries, models, data/value objects, migrations, jobs, events, HTTP, and Pest tests.
license: MIT
metadata:
  author: Francisco Barrento
---

# FBarrento Laravel Rules

Higher priority than `.agents/skills/laravel-best-practices` when both
apply. Use Laravel and Pest documentation for API syntax; use these
files for project code shape.

## Placement test (read before adding a rule)

Each rule has one canonical home, decided by
[rules/architecture/placement.md](rules/architecture/placement.md):

1. **Internals of one class type?** → that building-block folder.
2. **A settled global rule the whole codebase obeys?** → `architecture/`.
3. **An optional technique chosen per case?** → `patterns/`.

"It's a pattern" is never a placement reason — CQRS is a pattern but is
mandatory policy (`architecture/`); pipeline is a pattern you opt into
(`patterns/`). Cross-cutting rules live in one home; other folders
link-stub to it, never restate.

Each rule file follows: **Rule → Why → Good/Bad → Edge cases →
Checklist**, with a **Decision** section where a rule is a choice.

## Rule index

**Architecture** (mandatory, codebase-wide policy)
- [architecture/placement.md](rules/architecture/placement.md) — what goes where.
- [architecture/structure.md](rules/architecture/structure.md) — flat folders + nesting-exception registry.
- [architecture/cqrs.md](rules/architecture/cqrs.md) — actions write, queries read, services for external.
- [architecture/dependency-injection.md](rules/architecture/dependency-injection.md) — inject over facades; contextual attributes.
- [architecture/transactions.md](rules/architecture/transactions.md) — transaction boundaries; after-commit; dispatch jobs only from actions.
- [architecture/invariants.md](rules/architecture/invariants.md) — actions enforce invariants; throw specific business exceptions.

**Patterns** (optional techniques)
- [patterns/pipeline.md](rules/patterns/pipeline.md) — staged, swappable workflows; stages wrap actions.
- [patterns/pluggable.md](rules/patterns/pluggable.md) — strategy / swappable impls; one interface, bound selection.

**Building blocks** (internals of one class type)
- [actions/conventions.md](rules/actions/conventions.md) — `handle()`, data-object inputs, simple-vs-orchestrator.
- [queries/conventions.md](rules/queries/conventions.md) — fluent read-only query objects.
- [models/conventions.md](rules/models/conventions.md) — explicit casts, no scopes, to-array test.
- [data-objects/conventions.md](rules/data-objects/conventions.md) — immutable typed payloads; create/update/response roles.
  - [data-objects/spatie-laravel-data.md](rules/data-objects/spatie-laravel-data.md) — `Optional`, mapping, casts/transformers, `toArray()` in actions.
  - [data-objects/serialization.md](rules/data-objects/serialization.md) — queue boundary; IDs not models; plain-DTO escape hatch.
- [value-objects/conventions.md](rules/value-objects/conventions.md) — immutable, value equality. _(stub)_
- [enums/conventions.md](rules/enums/conventions.md) — backing, casting. _(stub)_
- [exceptions/conventions.md](rules/exceptions/conventions.md) — business-exception shape. _(stub)_
- [jobs/conventions.md](rules/jobs/conventions.md) — no business logic; inject actions.
- [events/conventions.md](rules/events/conventions.md) — event/listener shape. _(stub)_
- [observers/conventions.md](rules/observers/conventions.md) — guardrail: prefer actions/events. _(stub)_
- [http/conventions.md](rules/http/conventions.md) — thin controllers, form requests, resources. _(stub)_

**Infrastructure / runtime**
- [database/migrations.md](rules/database/migrations.md) — UUID PK, forward-only, no cascades/defaults/DB-enums.
- [database/schema.md](rules/database/schema.md) — schema design. _(stub)_
- [database/performance.md](rules/database/performance.md) — indexing, N+1. _(stub)_
- [database/mysql.md](rules/database/mysql.md) · [database/postgres.md](rules/database/postgres.md) — engine specifics. _(stubs)_
- [queues/conventions.md](rules/queues/conventions.md) — retries, failed jobs, Horizon. _(stub)_
- [logs/conventions.md](rules/logs/conventions.md) — structured logging. _(stub)_

**Cross-cutting**
- [naming/conventions.md](rules/naming/conventions.md) — class + variable naming.
- [packages/policy.md](rules/packages/policy.md) — when to add a dependency. _(stub)_
- [packages/catalog.md](rules/packages/catalog.md) — approved packages. _(stub)_

**Discipline**
- [testing/conventions.md](rules/testing/conventions.md) — Pest `test()`, `->and()`, structure mirror, in-memory services.

## How to apply

1. Identify the touched area and read the matching leaf file before editing.
2. Run the placement test before adding a *new* rule; put it in one home.
3. When rules conflict, this skill wins over `.agents/skills/laravel-best-practices`.
4. Check nearby files for current patterns, but do not copy ones that violate these rules.
5. Verify Laravel API syntax with `search-docs` before using framework APIs or attributes.

> Files marked _(stub)_ are scaffolded for an upcoming deepening pass and
> contain scope + TODOs, not yet full rules.
