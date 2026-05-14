# laravel-agent-kit

My personal kit of [Claude Code skills](https://docs.claude.com/en/docs/claude-code/skills) for Laravel and PHP work — opinionated project conventions packaged as installable skills.

These skills are small, composable, and designed to override generic Laravel guidance with the patterns I actually use across my projects. Fork them, adapt them, make them your own.

## Quickstart

Install with [skills.sh](https://skills.sh):

```bash
npx skills add fbarrento/laravel-agent-kit
```

You'll be prompted to pick which skills to install and which agents to install them on. That's it — the skills activate automatically in Claude Code when their description matches your request.

## Manual install (symlink)

If you'd rather wire the skills up by hand so `git pull` flows updates through automatically:

```bash
# 1. Clone the kit anywhere you like
git clone git@github.com:fbarrento/laravel-agent-kit.git ~/code/laravel-agent-kit

# 2. Symlink the skills you want into ~/.claude/skills/ (user-level)
mkdir -p ~/.claude/skills
ln -s ~/code/laravel-agent-kit/skills/laravel-rules ~/.claude/skills/laravel-rules

# Or install every skill at once
for skill in ~/code/laravel-agent-kit/skills/*/; do
    ln -s "$skill" "$HOME/.claude/skills/$(basename "$skill")"
done
```

For project-scoped install, symlink into `<project>/.claude/skills/` instead. To uninstall, remove the symlink — the source in the kit is untouched.

## Reference

- **[install-laravel](./skills/install-laravel/SKILL.md)** — Bootstraps Laravel 13 apps from official starter kits, curated community kits, or Composer `create-project`, optionally creating a GitHub or GitLab repo.
- **[laravel-rules](./skills/laravel-rules/SKILL.md)** — Applies my Laravel, Pest, model, and naming conventions when writing or reviewing Laravel code inside a full app. Overrides generic Laravel guidance.
- **[pest-package-tests](./skills/pest-package-tests/SKILL.md)** — Writes Pest tests for framework-agnostic PHP packages using project testing and naming conventions, with [`fbarrento/data-factory`](https://github.com/fbarrento/data-factory) as the default for data-object test data.
- **[new-task](./skills/new-task/SKILL.md)** — Creates a fresh task branch from the latest `origin/main` using conventional-commit branch naming before starting any new task.

## License

MIT
