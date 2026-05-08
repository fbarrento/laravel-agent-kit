# Laravel Starter Kit Catalog

This catalog is intentionally small. Verify each community package on Packagist or in its repository before installing because requirements, versions, and post-install commands change.

## Official Laravel Kits

Use `laravel new <app-name>` and answer the installer prompts.

| Kit | Choose When |
| --- | --- |
| Blank Laravel | The user wants a clean Laravel app without auth scaffolding. |
| React | The user wants Inertia with React, TypeScript, Tailwind, and shadcn/ui conventions. |
| Vue | The user wants Inertia with Vue, TypeScript, Tailwind, and shadcn-vue conventions. |
| Svelte | The user wants Inertia with Svelte, TypeScript, Tailwind, and shadcn-svelte conventions. |
| Livewire | The user prefers Blade/PHP-first dynamic UI with Livewire and Flux UI conventions. |

## Curated Community Kits

Install these community kits with:

```sh
laravel new <app-name> --using=<vendor/package>
```

| Package | Choose When | Notes |
| --- | --- | --- |
| `axyr/laravel-react-starter-kit` | The user wants Laravel with a decoupled React frontend instead of Inertia. | Verify Sanctum/Fortify, CORS, and frontend setup instructions before install. |
| `ercogx/laravel-filament-starter-kit` | The user wants a Filament-powered Laravel admin application. | Check the supported Laravel and Filament versions and run its documented admin-user setup. |
| `ludo237/237-starter-kit` | The user wants an opinionated React/Inertia kit with stricter tooling. | Verify current PHP, Pest, Rector, and static-analysis requirements. |
| `modus-digital/laravel-starter-kit` | The user wants a Livewire/Filament-oriented starter with operational packages. | Verify preferred package manager and post-install commands. |

## Composer Create-Project Kits

Install these kits with their documented `composer create-project` command, then run the kit's setup command before applying app-specific customization.

| Package | Choose When | Notes |
| --- | --- | --- |
| `nunomaduro/laravel-starter-kit` | The user wants a Blade-first, ultra-strict, type-safe Laravel 13 skeleton. | Requires PHP 8.5+, Bun, and a coverage driver; run `composer setup`, then `composer dev` or `composer test`. |
| `nunomaduro/laravel-starter-kit-inertia-vue` | The user wants Nuno's strict Laravel 13 conventions with Inertia and Vue. | Requires PHP 8.5+, Bun, Inertia 3 beta, Fortify, Wayfinder, Essentials, and strict test/tooling expectations. |
| `nunomaduro/laravel-starter-kit-inertia-react` | The user wants Nuno's strict Inertia and React conventions. | Current package may target Laravel 12; do not choose while the skill's default is Laravel 13 unless Packagist confirms Laravel 13 support. |

Example:

```sh
composer create-project nunomaduro/laravel-starter-kit --prefer-dist my-app
cd my-app
composer setup
```

## Selection Rules

- Prefer official kits when the user wants the mainstream Laravel path.
- Prefer community kits only when they clearly match a requested stack or tool, such as Filament or decoupled React.
- Prefer Composer create-project kits when the package documents that install path instead of `laravel new --using`.
- Enforce Laravel 13 compatibility for every selected kit; skip or ask for a different kit when the package only supports older Laravel versions.
- For unknown community packages, ask for the Packagist package name or repository URL, then verify install instructions before running `laravel new --using`.
- Never assume a community kit supports the same installer prompts as official kits.
