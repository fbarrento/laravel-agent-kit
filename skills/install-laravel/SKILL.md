---
name: install-laravel
description: Guides Laravel 13 application installs using official Laravel starter kits, curated community kits, or Composer create-project kits, then optionally creates a GitHub or GitLab repository. Use when the user wants to create, install, scaffold, or bootstrap a Laravel app, Laravel starter kit, Laravel repo, GitHub repo, GitLab repo, organization, or group.
---

# Install Laravel

Create Laravel 13 applications from official starter kits, curated community kits, or Composer create-project kits. Keep the flow guided: inspect the environment, ask only for missing decisions, then run the smallest command set.

## Quick Start

1. Confirm the app name and target path. Refuse to install into a non-empty unrelated directory unless explicitly confirmed.
2. Check prerequisites: `php -v`, `composer --version`, `laravel --version`, Herd/Herd MCP availability, and either `node`/`npm` or `bun`.
3. Install/update the Laravel installer when missing or stale: `composer global require laravel/installer`.
4. Create only Laravel 13 projects; after install, verify `composer.json` requires `laravel/framework` `^13`.
5. If the selected database is not SQLite, create both `<app_database>` and `<app_database>_testing` before running any installer command; prefer Herd MCP when Herd is installed.
6. For official kits, run `laravel new <app-name>` and answer the installer prompts from the user's choices.
7. For community kits, run `laravel new <app-name> --using=<vendor/package>` only after confirming Laravel 13 support.
8. For Composer kits, run the documented `composer create-project ...` command and setup command.
9. Install Laravel Boost, update app metadata, run matching frontend build commands, then optionally create the remote repo.

## Guided Decisions

Ask for these only when missing:

- App name, path, starter kit, auth option, teams support, database, package manager, migrations, and dev server startup.
- Whether to install `nunomaduro/essentials` and `nunomaduro/pao` by default for this app.
- Whether to create a remote repository; if yes, ask for GitHub or GitLab, owner namespace, repo visibility, and whether a new org/group is needed.

For non-SQLite databases, derive a safe database name from the app name unless the user provides one. If Herd and its MCP server are available, use Herd MCP; otherwise follow [references/databases.md](references/databases.md) before installer prompts or migrations can run.

## Starter Kits

- Official kits: blank Laravel, React, Vue, Svelte, and Livewire via `laravel new <app-name>`.
- Community kits: Packagist projects via `laravel new <app-name> --using=<vendor/package>`.
- Composer kits: packages that document `composer create-project`, including Nuno Maduro's strict starter kits.
- See [references/starter-kits.md](references/starter-kits.md) for the curated catalog, selection rules, and Nuno kit notes.

## Post-Install Standardization

Always install Laravel Boost:

```sh
composer require laravel/boost --dev
php artisan boost:install
```

If the user opts in, install Nuno packages:

```sh
composer require nunomaduro/essentials
composer require nunomaduro/pao --dev
```

Update `composer.json` and `README.md` to match the app: project name, description, stack, setup commands, dev commands, test commands, repository URL when known, and chosen optional packages. Do not stage secrets.

## Repository Creation

Repository creation is optional and only happens after the app exists.

- Default to an existing personal account, GitHub organization, or GitLab group.
- GitHub organizations must already be created before repo creation; stop and tell the user to create it first if it does not exist.
- Create a new GitLab group only when explicitly requested and supported by the environment.
- Default visibility to private unless public or internal is requested.
- Run `git status --short` before staging and create the initial commit after install artifacts exist.

GitHub:

```sh
gh repo create <owner>/<repo> --private --source=. --remote=origin --push
```

Before using an org owner, confirm the GitHub organization already exists and the user has permission to create repos in it.

GitLab:

```sh
glab repo create <group-or-user>/<repo> --private --remoteName origin
```

Use a full namespace path or `--group <group>` for existing groups. On GitLab.com, top-level groups must be created in the UI; self-managed instances may allow the Groups API.

## References

- Laravel 13 installation: https://laravel.com/docs/13.x/installation
- Laravel 13 starter kits: https://laravel.com/docs/13.x/starter-kits
- Laravel Boost: https://laravel.com/docs/13.x/boost
- Database fallbacks: [references/databases.md](references/databases.md)
- GitHub CLI repo creation: https://cli.github.com/manual/gh_repo_create
- GitLab CLI repo creation: https://docs.gitlab.com/cli/repo/create/
- GitLab Groups API: https://docs.gitlab.com/api/groups/
