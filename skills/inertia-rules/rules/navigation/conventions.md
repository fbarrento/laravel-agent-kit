# Navigation & data loading (Inertia v3)

How users move between pages and how data arrives beyond the first render.
The throughline: **the server owns state; the frontend requests slices of
it.** Don't build a parallel client data layer — Inertia's visits, partial
reloads, and deferred props are the data-fetching mechanism.

## Rule: navigate with `<Link>`, not raw anchors or manual visits

Use `<Link>` for navigation. For a non-GET link (logout, destroy) set
`method` and `as="button"`; pass `data` for a payload. Use
`router.visit`/`router.post` only for programmatic navigation that isn't a
clickable element.

**Why:** `<Link>` intercepts the click, does an XHR visit, and swaps page
props without a full reload — the whole point of Inertia. A raw `<a>` to a
Laravel route triggers a full document load and loses the SPA flow.

```tsx
import { Link } from '@inertiajs/react'
import { destroy } from '@/actions/generated/App/Http/Controllers/VehicleController'

<Link href={show(vehicle.id)}>View</Link>
<Link href={destroy(vehicle.id)} method="delete" as="button">Delete</Link>
```

Use the Wayfinder route/action object for `href` — never a handwritten URL
([../types/generated.md](../types/generated.md)).

## Rule: refresh only what changed with partial reloads

When re-fetching after an interaction (filter, sort, paginate), request
**only** the props that change with `only` (or `except`), and back it with
server-side lazy props so the rest isn't recomputed.

```tsx
router.reload({ only: ['vehicles'] })          // client: fetch just this prop
```
```php
// server: closures are evaluated only when that prop is requested
'vehicles'  => fn () => $this->query->paginate(),
'filters'   => Inertia::optional(fn () => /* only on demand */),
'appConfig' => Inertia::always(/* sent even in partial reloads */),
```

**Why:** a default visit re-evaluates and re-sends every prop — extra
queries and payload for data that didn't change. `only` + lazy closures
make a filter change cost one query, not the whole page.

## Rule: defer expensive, below-the-fold data — don't block first paint

Wrap slow or non-critical props in `Inertia::defer()` on the server and
render them inside `<Deferred>` with a `fallback`. Group related deferred
props so they load in parallel.

```php
'vehicles'    => fn () => $this->query->paginate(),          // initial render
'stats'       => Inertia::defer(fn () => $this->expensiveStats()),
```
```tsx
import { Deferred } from '@inertiajs/react'

<Deferred data="stats" fallback={<StatsSkeleton />}>
  <VehicleStats />
</Deferred>
```

**Why:** the page renders immediately with its essential props while
expensive aggregates stream in after — instead of one slow request
blocking the whole view. This is the v3-sanctioned loading pattern; don't
hand-roll a client `useEffect` fetch for it.

## Rule: prefetch likely-next navigations

For links a user is likely to follow, add `prefetch` (hover by default;
`prefetch="mount"` for always-visible primary nav). Tune freshness with
`cacheFor`.

```tsx
<Link href={index()} prefetch cacheFor="1m">Vehicles</Link>
```

**Why:** prefetch-on-hover makes the next page feel instant for near-zero
cost, using Inertia's own cache — no client query library needed. To also
render the target *immediately* on click, see instant visits
([../interactivity/conventions.md](../interactivity/conventions.md)).

## Rule: poll live data with `usePoll`, scoped by `only`

For data that changes server-side while the page is open (a job's status, a
queue depth), refresh it with `usePoll` — a timed partial reload — fetching
**only** the prop that changes. Drive conditional polling with the returned
`start`/`stop` and `{ autoStart: false }`, and stop once the work is done.

```tsx
import { usePoll } from '@inertiajs/react'

usePoll(5000, { only: ['queueDepth'] })            // refresh one prop every 5s
const { start, stop } = usePoll(5000, { only: ['job'] }, { autoStart: false })
```

**Why:** `usePoll` is a partial reload on a timer — the polled prop refreshes
from the server into page props and throttles automatically when the tab is
backgrounded. A hand-rolled `setInterval` + `fetch` (or a `router.reload`
without `only`) re-fetches more than changed and parks the result in client
state — the two anti-patterns this layer bans
([../state/conventions.md](../state/conventions.md)).

## Rule: load below-the-fold props on scroll with `<WhenVisible>`

For a prop that's expensive and off-screen at first paint, mark it
deferred/optional on the server and load it when its element nears the
viewport with `<WhenVisible>` (tune the lead distance with `buffer`).

```tsx
import { WhenVisible } from '@inertiajs/react'

<WhenVisible data="activity" buffer={300} fallback={<ActivitySkeleton />}>
  <ActivityFeed activity={activity} />
</WhenVisible>
```

**Why:** `<WhenVisible>` is `<Deferred>` triggered by visibility instead of
immediately — same contract: the server owns the prop, it lands in page
props, the fallback is the loading state. Wiring an IntersectionObserver to
a manual `fetch` rebuilds that by hand and lands the data in client state.

## Rule: paginate endlessly with `<InfiniteScroll>` + server merge props

For infinite lists, accumulate pages **into the prop** with
`Inertia::scroll()` (or `Inertia::merge()`/`deepMerge()` with `matchOn`) on
the server and render with `<InfiniteScroll>`. Reset the accumulation with
`router.reload({ reset: ['vehicles'] })` when filters change.

```tsx
import { InfiniteScroll } from '@inertiajs/react'

<InfiniteScroll data="vehicles">
  {vehicles.data.map((v) => <VehicleRow key={v.id} vehicle={v} />)}
</InfiniteScroll>
```
```php
'vehicles' => Inertia::scroll(fn () => $this->query->paginate()),
```

**Why:** merge props make each page *append to the same prop* server-side,
and Inertia merges successive responses into page props automatically — so
the growing list is still server state in props. The React-state version,
`setItems([...items, ...next])`, is the parallel client copy this layer
forbids ([../state/conventions.md](../state/conventions.md)).

## Rule: don't duplicate server state in a client cache

Page data comes from Inertia props and is refreshed via the mechanisms
above (partial reloads, deferred props, polling, prefetch) — never a
parallel client cache (React Query, SWR, Redux) mirroring props. The
canonical rule and rationale live in
[../state/conventions.md](../state/conventions.md); this is a link-stub.

## Rule: use `preserveScroll` / `preserveState` deliberately

Set `preserveScroll` when a visit shouldn't jump to the top (in-place
filter, validation error); `preserveState` to keep local component state
across a visit (a form mid-edit). Don't set them blanket — they change
perceived behavior.

## Checklist

- Navigation uses `<Link>` (with `method`/`as="button"` for non-GET); raw
  `<a>` to app routes avoided. `href` is a Wayfinder object.
- Re-fetches use `only`/`except` + server lazy/`optional`/`always` props,
  not full visits.
- Expensive/non-critical data is `Inertia::defer()` + `<Deferred>` with a
  fallback, not a client `useEffect` fetch.
- Likely-next links use `prefetch` where it pays off; instant rendering on
  click uses `instant` ([../interactivity/conventions.md](../interactivity/conventions.md)).
- Live data polled with `usePoll` scoped by `only`; no `setInterval`+fetch.
- Below-fold props loaded via `<WhenVisible>` (server-deferred), not an
  observer + manual fetch.
- Infinite lists use `<InfiniteScroll>` + `Inertia::scroll()`/merge props;
  pages accumulate in props, never `setItems`.
- No parallel client data cache duplicating Inertia props.
- `preserveScroll`/`preserveState` set deliberately, not by default.
