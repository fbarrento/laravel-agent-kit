---
name: git-conventions
description: Canonical naming + message rules for commits, pull request titles, and branch names using Conventional Commits. Defines the shared type vocabulary (feat, fix, refactor, chore, docs, test, perf, build, ci, style, revert), subject grammar, body/footer format, co-author trailer, breaking-change marking, and issue references. Use when writing or reviewing a commit message, naming a PR, or naming a branch. Framework-agnostic — applies to any repo.
---

# Git Conventions

Canonical home for VCS naming. The `new-task` skill *creates* branches;
this skill owns the *naming rules* it (and you) apply. Same type
vocabulary spans branch, commit, and PR title.

## Type vocabulary (shared by branch / commit / PR)

| Type | Use for |
|------|---------|
| `feat` | new user-facing capability |
| `fix` | bug fix |
| `refactor` | behavior-preserving restructuring |
| `perf` | performance improvement |
| `docs` | documentation only |
| `test` | tests only |
| `chore` | maintenance, deps, tooling, workflow |
| `build` | build system / packaging |
| `ci` | CI config / pipelines |
| `style` | formatting only, no logic change |
| `revert` | reverts a prior commit |

Pick the type by **intent**, not by which files changed.

## Commit messages

```
type(scope): subject

body — what + why, wrapped ~72 cols. optional.

Refs: #123
Co-Authored-By: Name <email>
```

Rules:
- Subject: imperative mood, lowercase start, no trailing period, ≤ ~72 chars.
- `scope` optional, lowercase noun (`auth`, `laravel-rules`). `type(scope):` or bare `type:`.
- Body explains *why*, not a diff restatement. Blank line after subject.
- Issue refs in subject `(#1)` for the headline issue, or a `Refs:`/`Closes:` footer.

**Breaking change:** add `!` before the colon AND a footer.
```
feat(api)!: drop v1 token endpoint

BREAKING CHANGE: clients must use /v2/tokens.
```

## PR titles

PR title = a Conventional Commit subject. Same grammar, same vocabulary.

- Good: `feat(quotes): add FinnHub symbol quote service`
- Good: `refactor: restructure laravel-rules into topic folders`
- Bad: `Update stuff`, `WIP`, `Fixes`.

Squash-merge → the PR title becomes the commit subject, so it must obey
the commit rules above.

## Branch names

`type/kebab-description` — same type vocabulary, lowercase kebab-case,
short + specific. Creation workflow + guardrails → `new-task` skill.

- Good: `fix/waitlist-validation`, `chore/upgrade-laravel-12`.
- Bad: `patch-1`, `franciscos-branch`.

## Checklist

- Type chosen by intent from the shared vocabulary.
- Commit subject: imperative, lowercase, no period, ≤ ~72.
- Body says why (when non-trivial); blank line after subject.
- Breaking change marked with `!` + `BREAKING CHANGE:` footer.
- Issue referenced (`(#1)` or footer) when one exists.
- PR title obeys commit-subject rules.
- Branch is `type/kebab-description`.
