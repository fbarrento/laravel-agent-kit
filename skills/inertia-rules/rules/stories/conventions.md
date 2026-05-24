# Stories

Storybook is the runtime contract for **reusable UI** — primitives, app
components, and eligible feature components. Stories are executable
component contracts, not a marketing doc site, and not a replacement for
app-page browser tests (those still own routed Inertia behavior).

## Rule: colocated stories are required for reusable UI

- Every `components/ui/*` primitive: colocated story required.
- Every `components/app/*` reusable component: colocated story required.
- A `features/<resource>/*` component: story required when it is
  reusable, stateful, visually important, exported outside its file, or
  likely to be edited by agents.
- Pages usually get **no** story — browser tests cover them. Add a page
  story only for a screen state worth reviewing in isolation, and it never
  satisfies the route's browser-test requirement.

The story file shares the component's basename
(`vehicle-table.tsx` → `vehicle-table.stories.tsx`).

**Why:** a story is the only place a reusable component's states can be
reviewed and verified in isolation. No story means no contract — the
component's variants and edge states are unverified and invisible to the
next agent.

## Rule: required states, represented directly

`Default` is always required. Add the others when the component can
express them:

| State | Required when |
|---|---|
| `Default` | always |
| `Empty` | renders a collection/slot that can be empty |
| `Loading` | accepts loading/pending/skeleton state |
| `Error` | renders an error/retry/failed state |
| `Disabled` | exposes disabled/read-only/permission-blocked controls |
| `WithValidationErrors` | renders a form/field group |

State exports are PascalCase and stable, and must represent the state
**directly via fixtures/args** — never by mutating `Default` at runtime.

**Why:** the canonical states are exactly the ones that break in
production and rarely get manually exercised. Pinning each to its own
fixture makes the contract reproducible and reviewable; mutating `Default`
hides which state actually rendered.

## Rule: typed fixtures, never inline backend-shaped blobs

Stories use typed fixtures that import generated/shared/feature-owned
types. Feature fixtures live in
`features/<resource>/<resource>.fixtures.ts`.

Fixtures must not: use `any`/broad records; hand-copy Spatie Data /
Wayfinder / enum / form / page-prop shapes; or call `Intl`/date
libraries/label maps to fake user-facing output.

```ts
import type { VehicleIndexPageData } from '@/types/generated'
export const vehicleIndexWithRows = {
  vehicles: [/* ... */],
  can: { createVehicle: true },
  copy: { title: 'Vehicles', emptyTitle: 'No vehicles yet' },
} satisfies Pick<VehicleIndexPageData, 'vehicles' | 'can' | 'copy'>
```

**Why:** an inline blob is an untyped, drifting copy of a backend shape —
the same anti-pattern as a handwritten type ([../types/generated.md](../types/generated.md)),
just hidden in a story. `satisfies` a generated type makes the fixture
fail to compile when the contract changes.

## Rule: stories render with the real token/theme CSS

Stories load the same token/theme CSS the app uses, so screenshots reflect
the runtime. Story-only raw colors, arbitrary spacing, or primitive
variables are violations ([../design-system/styling.md](../design-system/styling.md)).

**Why:** a story styled differently from production verifies nothing — it
proves a component that won't exist. Same CSS = the story is a faithful
contract.

## Rule: responsive components are reviewed across viewports

A component whose layout changes across breakpoints — a table that becomes
cards, a sidebar that collapses, a multi-column grid — must be reviewable across
the wired viewport presets, **mobile / tablet / desktop** (set in
`.storybook/preview.tsx`, [operations.md](operations.md)). Viewport is a render
*condition* like theme, not a fixture state: exercise it via the viewport
toolbar/global, never by hardcoding widths into a story. A non-responsive
primitive needs none.

**Why:** reviewing a responsive component only at desktop hides exactly the
breakage responsive design exists to prevent. Verified across breakpoints, the
story stays a faithful contract — and it's where mobile reflow and the a11y
200%-zoom concern ([../accessibility/conventions.md](../accessibility/conventions.md))
get caught.

## Rule: stories are the headless check surface for components

A story isn't just a manual preview — it's the surface CI/an agent runs.
Run stories headlessly with `@storybook/addon-vitest` (`vitest`) or
`@storybook/test-runner` (`storybook test`): `play` functions become
**interaction tests** ([../testing/conventions.md](../testing/conventions.md)),
and `@storybook/addon-a11y` (axe-core) runs an **accessibility** check per
story, gated by `parameters.a11y.test: 'error'`
([../accessibility/conventions.md](../accessibility/conventions.md)).
Stories are enumerable from the build's `/index.json`.

**Why:** writing a story already buys the component's interaction and a11y
checks for free in CI — so a missing story isn't just missing
documentation, it's a component with no automated contract at all. (Note:
the a11y run yields pass/fail, not per-violation JSON, and covers DOM-level
WCAG only — a backstop, not full a11y.)

## Rule: the sidebar taxonomy comes from the `meta.title` path, not file moves

Storybook's sidebar grouping is driven entirely by the `meta.title`
lowercase-path scheme ([../naming/conventions.md](../naming/conventions.md)) — no
parallel folder structure, no file moves. Top-level groups, in order:
`Introduction`, `brand/*`, `design-system/*`, `components/*` (`ui` then `app`),
`features/<resource>/*`. The order is enforced once in `.storybook/preview.tsx`
via `storySort` (this project's instance):

```ts
storySort: { order: ['Introduction', 'brand', 'design-system', 'components', ['ui', 'app'], 'features', '*'] }
```

**Storybook-only documentation** (MDX) lives under `.storybook/docs/**/*.mdx`
(added to the `stories` glob in `.storybook/main.ts`) — deliberately **outside
`resources/js`**, because docs are not shipped app code and so stay out of the
role graph ([../architecture/roles.md](../architecture/roles.md)). Foundation
token pages, by contrast, *are* `*.stories.tsx` under
`resources/js/design-system/` (they render real components).

**Why:** deriving groups from the title path means one naming rule controls both
the story id and the sidebar — no second taxonomy to maintain. Keeping MDX docs
in `.storybook/` keeps non-shipped prose out of the app the role graph governs.

## Rule: reusable-component metas opt into autodocs

Every reusable-component and foundation meta sets `tags: ['autodocs']` and a
`parameters.docs.description.component` string; autodocs then generates the Docs
tab (description + args table + source) from the meta.

**Why:** the component's API table and description should come from the same
typed meta that drives the stories, not a hand-written doc that drifts — one
source of truth for both the runtime contract and its docs.

## Rule: foundation (`design-system/*`) pages show live values, meaning, and application

A token/foundation page must do three things — never a static swatch dump:

1. **Live resolved values** — read the computed token off the rendered element
   (`getComputedStyle`); never hardcode a primitive (`oklch(...)`). Drift-proof
   and theme-aware ([../design-system/styling.md](../design-system/styling.md)
   bans raw values; this is its docs corollary).
2. **Product meaning** — state the semantic intent, not just the value (status:
   `emerald=gain`, `rose=loss`, `amber=alert`, `blue=brand`).
3. **An "Applying …" story** — the token in real UI, across surfaces
   (`surface` / `surface-muted` / `surface-raised`) and light + dark.

Shared doc helpers (presentational, `ds-`-only, not matched by the `*.stories`
glob) live in `resources/js/design-system/token-docs.tsx`. Colored status text on
these pages must clear contrast ([../accessibility/conventions.md](../accessibility/conventions.md)).

**Why:** a hardcoded swatch lies the moment the theme changes; a value with no
meaning doesn't tell an agent *when* to use it; a token shown only in isolation
hides that it must survive every surface and theme. Live + meaning + application
is what makes the page a contract, not decoration.

> Gotchas for running the headless story/docs suite in CI (vite-plugin guard, SSR
> warmup noise, a11y gating, theme/viewport wiring) are project-ops, recorded
> separately in [operations.md](operations.md).

## Checklist

- Reusable UI (ui/app + eligible feature components) has a colocated
  story; pages generally do not.
- Stories run headlessly (test-runner / addon-vitest); `play` interactions
  and `addon-a11y` checks pass with `parameters.a11y.test: 'error'`.
- `Default` present; applicable canonical states present and backed by
  fixtures/args, not runtime mutation.
- Fixtures are typed against generated/shared/feature types — no `any`, no
  inline backend shapes, no faked formatting.
- Stories render with the app's token/theme CSS; no raw styling.
- Responsive components (breakpoint-dependent layout) are reviewable across the
  mobile/tablet/desktop viewport presets; non-responsive ones need none.
- Sidebar groups derive from the `meta.title` path; `storySort` order set once in
  `.storybook/preview.tsx`; Storybook-only MDX docs in `.storybook/docs/` (outside
  `resources/js`).
- Reusable/foundation metas set `tags: ['autodocs']` + a
  `docs.description.component`.
- Foundation (`design-system/*`) pages show live resolved token values (no
  hardcoded primitives), product meaning, and an "Applying …" story across
  surfaces + light/dark.
- CI/ops gotchas for the headless suite live in [operations.md](operations.md).
