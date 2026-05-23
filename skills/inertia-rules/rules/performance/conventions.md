# Performance & code splitting (Inertia v3)

Keep the app fast by **not fighting Inertia's defaults**: pages are already
code-split, assets are already versioned. Optimize deliberately, against a
measured cost — never preemptively.

## Rule: keep page components lazily code-split — don't make the glob eager

Inertia resolves pages with `import.meta.glob` inside `resolvePageComponent`,
which is **lazy by default**: each page is its own chunk, loaded on visit.
Keep it that way — don't pass `{ eager: true }`, which bundles every page
into the initial download.

```ts
// Good — lazy (default): one chunk per page, loaded on visit
resolve: (name) =>
  resolvePageComponent(`./pages/${name}.tsx`, import.meta.glob('./pages/**/*.tsx')),

// Bad — eager: every page ships in the initial bundle
import.meta.glob('./pages/**/*.tsx', { eager: true })
```

**Why:** lazy pages keep the initial bundle small — the user downloads the
page they asked for, not all of them. The one cost (a request per new page)
is exactly what `prefetch`
([../navigation/conventions.md](../navigation/conventions.md)) hides:
prefetch the likely-next link and its chunk arrives before the click. Going
eager trades a fast first paint for a cost you've already solved.

## Rule: split heavy, rarely-rendered feature components with `React.lazy`

For a large component not needed at first paint — a charting dashboard, a
rich-text editor, a heavy modal body — load it with `React.lazy` +
`<Suspense>`, with a fallback that matches the loading-states contract
([../loading-states/conventions.md](../loading-states/conventions.md)). Do
**not** split small or above-the-fold components.

```tsx
const VehicleAnalytics = lazy(() => import('@/features/vehicles/vehicle-analytics'))

<Suspense fallback={<AnalyticsSkeleton />}>
  {showAnalytics && <VehicleAnalytics vehicleId={vehicle.id} />}
</Suspense>
```

**Why:** page-level splitting is automatic, but one heavy widget inside an
otherwise light page still bloats that page's chunk; lazy-loading it defers
the cost until the user reveals it. Splitting *everything*, though, trades
bytes for round-trips and jank — reserve it for genuinely heavy, deferred UI.

## Rule: let Vite version assets — never disable the mechanism

Laravel's Vite integration sets Inertia's asset version from the build
manifest hash automatically. On deploy the hash changes, the client's cached
version mismatches, and Inertia does **one** full page load to pull the new
assets, then resumes XHR visits. Don't return `null` from `version()` or
hand-roll versioning.

**Why:** the version is what stops a user on a stale tab from running old JS
against a new backend. Disabling it reintroduces the "hard-refresh to fix it"
bug class Inertia handles for free. The wiring lives in `HandleInertiaRequests`
([../shared-data/conventions.md](../shared-data/conventions.md)); leave it on
the Vite default.

## Checklist

- Page glob stays lazy (`import.meta.glob` without `{ eager: true }`);
  likely-next pages use `prefetch`, not eager loading.
- Heavy, below-the-fold/conditional components use `React.lazy` + `<Suspense>`
  with a contract-matching fallback; small/above-fold components are not split.
- Asset versioning left to Laravel's Vite integration; `version()` not
  disabled or hand-rolled.
- Splitting and memoization are done against a measured cost, not
  preemptively ([../state/conventions.md](../state/conventions.md)).
