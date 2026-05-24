# Side effects (guardrail)

> **[Side effect](../../LANGUAGE.md)** is defined in `LANGUAGE.md` (a guardrail term); this file owns the grammar.

The frontend counterpart to **laravel-rules'** observers/events guardrail.
Same creed on both sides of the wire: **one source of truth, explicit
mutations, no hidden work.** On the backend that means no model lifecycle
hooks; here it means no `useEffect` doing work Inertia already does, no
client copy of server state, no shadow-copy optimism. This file owns the
*principle and the decision tree*; the specific patterns live in their
rule files and are linked, not restated.

## Rule: the server owns state; effects are a last resort

Domain data arrives as Inertia **props** and you render from it. Reach for
a `useEffect` (or any client-side effect) only for ephemeral, view-only
work that **no Inertia mechanism covers**. Everything else has an explicit,
visible home:

- **Fetching / refreshing server data** → Inertia: partial reloads
  (`only`), deferred props, `usePoll`, `<WhenVisible>`
  ([../navigation/conventions.md](../navigation/conventions.md),
  [../loading-states/conventions.md](../loading-states/conventions.md)).
- **Reading server state** → render from props; derive computed values
  during render, don't store them
  ([../state/conventions.md](../state/conventions.md)).
- **Optimistic mutations** → Inertia's props snapshot with automatic
  rollback, never a `useState` shadow copy
  ([../interactivity/conventions.md](../interactivity/conventions.md)).

**Why:** a `useEffect` fetch is a second data layer that duplicates what
Inertia does and parks results in client state; a `useState` copy of props
goes stale on the next visit; a shadow-copy optimistic update desyncs the
moment the real response arrives. Each is an *implicit* behavior a reader
of the component can't see — the frontend's version of a hidden observer.

## Decision: should this be a `useEffect` / client-side effect?

Default: **no.** Walk in order; the first **stop** is your answer.

1. **Is it fetching or refreshing server data?** (a list, a record, counts,
   a related slice, "load more") → **stop.** Use a partial reload, deferred
   props, `usePoll`, or `<WhenVisible>`
   ([../navigation/conventions.md](../navigation/conventions.md)).

2. **Is it copying or mirroring props into client state?** → **stop.**
   Render from props; derive computed values during render
   ([../state/conventions.md](../state/conventions.md)).

3. **Is it an optimistic mutation?** → **stop.** Apply it through Inertia's
   props snapshot (auto-rollback), not a `useState` shadow copy
   ([../interactivity/conventions.md](../interactivity/conventions.md)).

4. **Is it ephemeral, view-only work with no server data** — focusing a
   field, firing an analytics/telemetry event, subscribing to a browser API
   (resize, media query, visibility), or imperatively driving a non-React
   widget — **with cleanup on unmount?** → a `useEffect` is **acceptable**,
   and prefer wrapping it in a named, framework-bound hook in `hooks/`
   ([../architecture/roles.md](../architecture/roles.md)). Otherwise it is
   server state (gate 1/2) or derived state — don't reach for an effect.

```tsx
// Bad — a useEffect fetch: a second data layer, result parked in client state
function VehicleList() {
  const [vehicles, setVehicles] = useState([])
  useEffect(() => { fetch('/vehicles').then(r => r.json()).then(setVehicles) }, [])
  // ...
}

// Good — the server sends it as a prop; the page renders from it
function VehicleList({ vehicles }: VehicleIndexPageProps) {
  return <VehicleTable rows={vehicles} />
}

// Acceptable — ephemeral, view-only, with cleanup; wrapped in a hook
function useMediaQuery(query: string) {
  const [matches, setMatches] = useState(() => matchMedia(query).matches)
  useEffect(() => {
    const mql = matchMedia(query)
    const onChange = () => setMatches(mql.matches)
    mql.addEventListener('change', onChange)
    return () => mql.removeEventListener('change', onChange)
  }, [query])
  return matches
}
```

## Edge cases

- **Loading flags.** Don't pair a `useState(isLoading)` with a fetch —
  `processing` and deferred props already carry that truth
  ([../loading-states/conventions.md](../loading-states/conventions.md)).
- **One-off transient requests** (a typeahead, a non-navigational lookup)
  use the sanctioned `useHttp` escape hatch — its result is **not** page
  state and must not be treated as one
  ([../interactivity/conventions.md](../interactivity/conventions.md)).
- **Infinite scroll / polling.** Merge props and `usePoll`, never
  `setItems([...items, ...next])` or a hand-rolled `setInterval` + `fetch`
  ([../navigation/conventions.md](../navigation/conventions.md)).

## Checklist

- No `useEffect` fetch of server data — Inertia mechanisms only.
- No `useState` copy/mirror of props; derived values computed during render.
- Optimistic updates go through Inertia's props snapshot, not a shadow copy.
- The only effects present are ephemeral, view-only, with cleanup —
  preferably inside a named `hooks/` hook.
