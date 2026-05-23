# State ownership

Where state lives. The default answer is "the server, delivered as Inertia
props." Client state is the exception, reserved for ephemeral UI. This is
the canonical home for the server-state rule that
[../navigation/conventions.md](../navigation/conventions.md) refers to.

## Rule: server state comes from props — don't copy it into client state

Domain data (the list, the record, capability flags, counts) lives on the
server and arrives as Inertia props. Render directly from props. Refresh
it through Inertia (partial reloads, deferred props, polling, prefetch —
[../navigation/conventions.md](../navigation/conventions.md)), never by
copying props into `useState`/`useReducer`/a store.

**Why:** props *are* server state delivered to the page. Copying them into
client state creates a stale second copy — a mutation updates the server
and the next props, but not your copy, so the UI desyncs. Reading props
directly means the page is always as fresh as the last visit.

```tsx
// Good — render from props
function VehicleTable({ vehicles }: { vehicles: VehicleListItem[] }) {
  return <Table rows={vehicles} />
}

// Bad — props copied into state; goes stale after the next partial reload
const [rows, setRows] = useState(vehicles)   // now there are two truths
```

## Rule: no client store for server data

Do not introduce Redux/Zustand/a context cache to hold server data, and
do not add React Query/SWR alongside Inertia. Inertia is the data layer.

**Why:** a client store mirroring server data is a parallel source of
truth that must be manually kept in sync with every visit and mutation —
the exact bug class Inertia removes. (Same rule, stated from the
navigation side.)

## Rule: local state is for ephemeral UI only

`useState` is for UI that has no server meaning: open/closed, hover,
current tab, an in-progress (unsubmitted) selection, a controlled input
before submit. Once it matters to the domain, it goes to the server via an
action, not a client store.

**Why:** ephemeral UI state is genuinely client-only — the server doesn't
care whether a menu is open. Keeping local state to that category is what
makes "render from props" hold for everything that *does* matter.

## Rule: derive, don't store, what you can compute from props

Compute view values from props during render (filtered/sorted views,
totals, derived flags). Reach for `useMemo` only for a measured cost, not
by default. Don't snapshot a derived value into state.

**Why:** a derived value stored in state is a cache that goes stale when
props change. Computing during render is always correct and usually cheap.

## Rule: view-model state is typed and feature-local

When a feature needs genuine client state (multi-select, a wizard step),
type it in the feature's `*.types.ts` and keep it in the feature
([../types/generated.md](../types/generated.md)). Persist it across an
Inertia visit with `preserveState` when needed
([../navigation/conventions.md](../navigation/conventions.md)).

```ts
export type VehicleSelectionState = { selectedIds: number[]; lastSelectedId: number | null }
```

## Checklist

- Server/domain data rendered from props; never copied into
  `useState`/store.
- No Redux/Zustand/React-Query/SWR holding server data.
- Local state limited to ephemeral UI; domain changes go to the server via
  an action.
- Computed values derived during render, not snapshotted into state.
- Genuine client state is typed in the feature's `*.types.ts`;
  `preserveState` used when it must survive a visit.
