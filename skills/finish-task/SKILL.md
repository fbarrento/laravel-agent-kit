---
name: finish-task
description: Run a project's quality gates, get user review, then commit — the end-of-task counterpart to new-task. Tech-stack agnostic: discovers the project's own test, typecheck, lint, static-analysis, and format commands rather than hardcoding them. Use when a coding task is implemented and ready to commit, when the user says "finish this", "wrap up", "ready to commit", "ship it", or before any commit that concludes a task.
---

# Finish Task

End-of-task lifecycle: gates → review → commit. Counterpart to
`new-task` (which starts the branch). Commit/PR naming is owned by
`git-conventions`.

This skill owns the **gate sequence and policy**, never the commands —
those are stack-specific and get **discovered** from the project.

## Gate sequence

Run in this order; stop on first red and enter the fix-loop:

1. **Tests**
2. **Typecheck**
3. **Lint**
4. **Static analysis**
5. **Format** (apply, then re-stage)

Then: show the user the diff + gate results → **ask for review** →
commit only on explicit approval.

## Command discovery (stack-agnostic)

Do not assume tools. Detect the project's own commands, in priority order:

1. Composer scripts — `composer.json` `scripts` (e.g. `test`, `lint`, `analyse`).
2. NPM/PNPM scripts — `package.json` `scripts`.
3. `Makefile` / `justfile` targets.
4. `bin/` or `scripts/` entrypoints.
5. CI config (`.github/workflows/*`, `.gitlab-ci.yml`) — mirror what CI runs.

Map each gate to the discovered command; **skip a gate with no command**
(state which were skipped). Example resolutions (illustrative, not
hardcoded): Laravel → `pest`/`phpunit`, `phpstan`/`larastan`,
`pint`/`rector`. JS/TS → `vitest`/`jest`, `tsc --noEmit`, `eslint`,
`prettier`.

> Laravel-specific gate commands live in `laravel-rules`; this skill
> resolves "run the static-analysis command" → that project's tool.

## Fix-loop

Gate red → read failure → fix → re-run that gate. Cap at ~3 iterations
per gate; if still red, **stop and escalate to the user** with the exact
error. Never disable/skip a check to make it pass. Never `--no-verify`.

## Commit

- Only after all runnable gates green AND user approved the diff.
- Message per `git-conventions` (type vocab, subject grammar, footers).
- Push only if the user asks.

## Guardrails

- **Never commit red** — no failing or skipped-to-pass checks.
- **Never commit without showing the diff and getting approval** — the
  commit concludes the task; treat it as a confirmation gate.
- Never bypass hooks (`--no-verify`), never weaken a check to pass.
- Never commit secrets — scan the diff for tokens/keys before committing.
- If the working tree mixes unrelated changes, ask before staging.

## Checklist

- Gate commands discovered from the project, not assumed.
- Each gate run or explicitly reported as skipped (no command).
- All runnable gates green before commit.
- Diff shown + user approved.
- Commit message follows `git-conventions`.
- No hook bypass, no weakened checks, no secrets in the diff.
