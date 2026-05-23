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
import type { App } from '@/types/generated'
export const vehicleIndexWithRows = {
  vehicles: [/* ... */],
  can: { createVehicle: true },
  copy: { title: 'Vehicles', emptyTitle: 'No vehicles yet' },
} satisfies Pick<App.Data.Vehicles.VehicleIndexPageData, 'vehicles' | 'can' | 'copy'>
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
