# CLAUDE.md — laravel-agent-kit

This repo holds agent **skills** (`skills/<name>/SKILL.md` + `rules/<topic>/*.md`),
published via skills.sh and vendored by projects into `.agents/skills/`. This
file is the operating manual for agents that **maintain** these skills.

## Edit skills from the main checkout only

**Never edit `skills/**` (or a project's `.agents/skills/**`) from a git
worktree.** `.claude/skills/*` are symlinks into `.agents/skills/`, and a
worktree's edits to that symlinked target resolve back to the **main
checkout** — so worktree isolation silently does **not** hold for skill files,
and changes leak into `main`. Edit skills from the main checkout.

If you must work in a worktree, after any skill edit verify with
`git -C <worktree> status`; if a change leaked, revert it in `main`
(`git checkout -- <path>`) and re-apply inside the worktree via patch. A
root-cause fix for the symlink resolution is a tracked follow-up; until then
this rule is the guard.

## Source of truth & precedence

This repo is the **canonical** source for the skills; a consuming project
vendors a pinned copy. Precedence for an agent working *in a project*,
highest first:

1. the project's `docs/adr/*` and `docs/postmortem/*` — a documented decision
   overrides a skill rule **for that project**;
2. these skills — the canonical, cross-project defaults;
3. generic framework guidance (Boost, `laravel-best-practices`).

A project ADR / postmortem / handoff is **delivered to the skills maintainer
and grilled** before any *canonical* change — the canonical skill never
auto-updates from a project doc. (An ADR overrides locally the moment it
lands; the canonical skill changes only after that review.)

## Skill examples mirror real code (path-form anchors)

When a skill cites a **real** symbol, it introduces that symbol by its repo
path — `app/Queries/Concerns/TransformsToData.php` — at least once in its home
rule file. **Illustrative** symbols stay bare names (`StripeGateway`,
`VehicleData`) and are never written in path-form. A drift guard in the
consuming app's `tests/Arch` verifies every `app/**` / `resources/**` /
`tests/**` path a skill references still exists; the path-vs-bare-name
convention is what lets it check real anchors without flagging illustrations.

The code is the source of truth: a skill example's symbol name follows a
**code** change, never a doc-only rename.

## Frontmatter lint

Every `skills/*/SKILL.md` frontmatter must parse as YAML with `name` +
`description`. Run `python3 scripts/lint-skills.py` (also enforced in CI) —
a malformed block makes the skills.sh indexer silently skip the skill.
