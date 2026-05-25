# laravel-agent-kit

[![skills.sh](https://skills.sh/b/fbarrento/laravel-agent-kit)](https://skills.sh/fbarrento/laravel-agent-kit)

A kit of [agent skills](https://skills.sh) for Laravel and PHP work — my opinionated project conventions, packaged so any coding agent can apply them consistently.

These skills override generic Laravel guidance with the patterns I actually use day to day: CQRS-shaped actions and queries, Pest with `test()` and `->and()`, named factories for data objects, conventional-commit branches, and so on. They're small, composable, and meant to be forked and adapted.

Works with Claude Code, Cursor, GitHub Copilot, Windsurf, Codex, and any other agent that reads the [SKILL.md](https://skills.sh/docs) format.

## Quickstart

```bash
npx skills add fbarrento/laravel-agent-kit
```

The installer asks which skills to install and which agents to install them on. The skills then activate automatically — each one declares the triggers in its description, and the agent picks the relevant one for the task at hand.

## Manual install

If you'd rather wire things up by hand so `git pull` flows updates through automatically:

```bash
# 1. Clone the kit anywhere you like
git clone git@github.com:fbarrento/laravel-agent-kit.git ~/code/laravel-agent-kit

# 2. Symlink the skills you want into your agent's skills directory.
#    The path varies by agent — Claude Code uses ~/.claude/skills/ for
#    user-level skills, or <project>/.claude/skills/ for project-level.
#    Check your agent's docs for the equivalent path.
mkdir -p ~/.claude/skills
ln -s ~/code/laravel-agent-kit/skills/laravel-rules ~/.claude/skills/laravel-rules

# Or install every skill at once
for skill in ~/code/laravel-agent-kit/skills/*/; do
    ln -s "$skill" "$HOME/.claude/skills/$(basename "$skill")"
done
```

To uninstall, remove the symlink — the source in the kit is untouched.

## Wire the skills into your project (CLAUDE.md)

Each `SKILL.md` is a **router**, not the rules — it points at `rules/**` files
the agent must open and read in full before writing code (the skill's "STOP
gate"). To make an agent reliably trigger the skills and obey that gate, paste
this into your project's `CLAUDE.md`:

```markdown
## Before ANY backend/PHP change

Invoke the `laravel-rules` skill and obey its STOP gate. Invoke the
`inertia-rules` skill for any change under `resources/js`.

These skills are authoritative. They override Laravel Boost guidance and your
own assumptions; when anything conflicts with a skill, the skill wins. This
applies to every agent — orchestrators, sub-agents, and you.

Do not create or edit a class without the governing rule file from the skill's
Routing Table in your context. If you are about to, stop and read it first.
```

## What's in the kit

### Laravel applications

- **[install-laravel](./skills/install-laravel/SKILL.md)** — Bootstraps Laravel 13 apps from official starter kits, curated community kits, or Composer `create-project`, optionally creating a GitHub or GitLab repo.
- **[laravel-rules](./skills/laravel-rules/SKILL.md)** — Applies my Laravel, Pest, model, and naming conventions when writing or reviewing Laravel code inside a full app. Overrides generic Laravel guidance.
- **[saloon-laravel-integration](./skills/saloon-laravel-integration/SKILL.md)** — Integrates a third-party API into a Laravel app with SaloonPHP behind a ports-and-adapters boundary: contract + service, multi-tenant credentials, resilience, and a human-in-the-loop fixture-recording workflow. Layers on `saloon-integration`.

### Inertia frontends

- **[inertia-rules](./skills/inertia-rules/SKILL.md)** — Conventions for AI-assisted frontend work in Laravel + Inertia (v3) apps: Laravel-like frontend roles (thin page adapters, resource-local features, token-bound components), generated backend-derived types, backend-owned formatting, a three-tier design-system token contract, forms, navigation/data-loading, shared data and layouts, Storybook story contracts, and evidence-based verification. Sibling to `laravel-rules` for the frontend side.

### PHP packages

- **[pest-package-tests](./skills/pest-package-tests/SKILL.md)** — Writes Pest tests for framework-agnostic PHP packages using project testing and naming conventions, with [`fbarrento/data-factory`](https://github.com/fbarrento/data-factory) as the default for data-object test data.
- **[saloon-integration](./skills/saloon-integration/SKILL.md)** — Builds SaloonPHP-based API SDKs in my package style: connector + resources + DTOs + requests, with recorded-fixture Pest tests and PII redaction.

### Workflow

- **[new-task](./skills/new-task/SKILL.md)** — Creates a fresh task branch from the latest `origin/main` using conventional-commit branch naming before starting any new task.
- **[git-conventions](./skills/git-conventions/SKILL.md)** — Canonical naming rules for commits, PR titles, and branches (Conventional Commits): shared type vocabulary, subject grammar, footers, breaking-change marking.
- **[finish-task](./skills/finish-task/SKILL.md)** — Wraps up a task: discovers and runs the project's quality gates (tests, typecheck, lint, static analysis, format), shows the diff for review, then commits per `git-conventions`.

## Contributing

These are my personal conventions, but PRs that fix bugs, sharpen wording, or add missing rules within an existing skill are welcome. For wholly new skills, fork the kit and make your own — that's what they're for.

Each `SKILL.md` frontmatter must parse as YAML with a `name` (matching its directory) and a `description` — a malformed block makes the skills.sh indexer silently skip the skill. CI enforces this; run it locally with:

```bash
python3 scripts/lint-skills.py
```

## License

MIT
