# Stories — operational notes (running the headless suite in CI)

> **Project CI/infra, not code-shape conventions.** Unlike the rest of this
> skill, this file records environment/CI gotchas observed running the headless
> Storybook suite ([conventions.md](conventions.md) — "stories are the headless
> check surface"). They are project-specific facts, not rules an agent applies
> while writing components — verify against the project's actual `.storybook`
> config and CI before relying on them.

## `laravel-vite-plugin` aborts the suite in CI

Storybook's vitest project `extends` the app Vite config, which loads
`laravel-vite-plugin`; its CI guard throws *"You should not run the Vite HMR
server in CI environments."* **Fix:** set `LARAVEL_BYPASS_ENV_CHECK=1` on the
Storybook CI step. No HMR server is actually served under vitest, so this matches
local behavior.

## Benign Inertia SSR-warmup noise

The same `extends` pulls in `@inertiajs/vite`, which logs *"Failed to warm up
Inertia SSR module graph"* during `test-storybook`. It is **non-fatal** (tests
pass, exit 0) — ignore it, or strip app plugins via `viteFinal` later.

## a11y runs headless and is gated as error

`parameters.a11y.test: 'error'` runs axe-core via `@storybook/addon-vitest` +
Playwright/Chromium and **fails the run** on violations
([../accessibility/conventions.md](../accessibility/conventions.md)). Practical
consequence for token docs: colored status text must clear contrast — keep it at
large sizes, with labels on `ds-surface` rather than on colored swatches.

## Theme + viewport are wired in `preview.tsx`

A `theme` toolbar global toggles `.dark` + `data-theme` on `documentElement`;
viewport presets are mobile / tablet / desktop. Stories that assert theme or
viewport behavior depend on this wiring.
