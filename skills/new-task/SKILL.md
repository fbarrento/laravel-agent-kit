---
name: new-task
description: Creates a fresh task branch from the latest remote main branch using conventional-commit branch naming. Use when starting any new coding task, bug fix, refactor, feature, chore, documentation change, or user request that will modify repository files.
---

# Fresh Task Branch

## Quick Start

Before modifying repository files for a new task, start from a fresh branch based on `origin/main`:

```bash
git fetch origin
git switch --create feat/short-description origin/main
```

## Workflow

1. Check the current branch and working tree with `git status --short --branch`.
2. If there are uncommitted changes, do not switch branches or modify them without asking the user how to proceed.
3. Fetch the latest remote refs with `git fetch origin`.
4. Create the task branch from `origin/main`, not local `main`.
5. Use a branch name aligned with conventional commits.
6. Continue with the requested implementation only after the fresh branch is active.

## Branch Naming

Format: `type/kebab-description`. The type vocabulary (`feat`, `fix`,
`refactor`, `chore`, `docs`, `test`, …) and naming rules are owned by the
**git-conventions** skill — use it as the canonical source so branch,
commit, and PR names stay aligned. This skill does not restate the vocab.

Lowercase kebab-case after the prefix, short and specific, for example
`fix/waitlist-validation` or `chore/upgrade-laravel-12`.

## Guardrails

- Never overwrite, reset, delete, stash, or commit user work without explicit approval.
- If the requested task continues existing branch work, ask whether to stay on the current branch instead of creating a new one.
- If `origin/main` is unavailable, inspect remotes and ask before choosing another base branch.
- Do not create a new branch for purely informational questions, reviews, or planning unless the user asks for file changes.
