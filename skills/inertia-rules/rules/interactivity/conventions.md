# Interactivity & the non-Inertia boundary (Inertia v3)

Making interactions feel instant **without** leaving the props model — and
the one sanctioned way to make a request that isn't a page visit. The
throughline from [../navigation/conventions.md](../navigation/conventions.md)
holds: page data is server state delivered as props. These features change
*when* the user sees a result, not *where* the truth lives.

## Rule: make navigations feel instant with `instant`, not a hand-built shell

For a likely navigation, render the target immediately with an instant
visit: the `instant` prop on a Wayfinder `<Link>` (or `component` on a
manual `router.visit`) renders the destination component now while the
server request finishes in the background. Pair it with `prefetch`
([../navigation/conventions.md](../navigation/conventions.md)) so cached
props fill the intermediate frame.

```tsx
import { Link } from '@inertiajs/react'
import { show } from '@/actions/generated/App/Http/Controllers/VehicleController'

<Link href={show(vehicle.id)} prefetch instant>View</Link>
```

**Why:** instant visits keep Inertia as the router — the page still comes
from a real server response and lands in props. Faking instantness with a
client-side route plus a skeleton you swap on `fetch` resolve reintroduces
the parallel client router and data layer Inertia exists to remove
([../state/conventions.md](../state/conventions.md)). Reserve `instant` for
navigations whose target is predictable (a row → its detail page), not for
every link.

## Rule: optimistic updates mutate page props and roll back — never a shadow copy in state

When a mutation's result is predictable, apply it optimistically through
Inertia so it writes to **page props** and snapshots the changed keys,
auto-reverting them if the request fails (422 / server error / interrupted
visit). Use `useForm(...).optimistic()`, `<Form optimistic>`, or
`router.optimistic()` — never a second copy of the data in `useState`.

```tsx
const { optimistic, patch } = useForm({ done: false })

function toggle() {
  optimistic((props) => ({ task: { ...props.task, done: true } }))
  patch(update(task.id))           // reverts the snapshot on failure
}
```

**Why:** the optimistic value lives in props, so the page has one source of
truth before *and* after the server confirms — and rollback is automatic.
Hand-rolling optimism by mutating a `useState` copy of the list desyncs the
moment the real response arrives and is exactly the parallel-state bug this
skill bans ([../state/conventions.md](../state/conventions.md)). Keep the
callback pure and return only the keys that change. Use optimism for
high-confidence, low-stakes mutations (a toggle, a reorder, a like) — not
for creates whose server result you can't predict (generated ids,
timestamps, derived counts).

## Rule: leave the Inertia data layer only via `useHttp`, for genuinely non-page requests

Some requests aren't page visits: a call to a third-party API, a typeahead
hitting a plain JSON endpoint. For those, `useHttp` gives the `useForm`
developer experience (`data`/`setData`/`processing`/`errors`/`onSuccess`)
but returns parsed JSON outside Inertia's page lifecycle. This is the
**only** sanctioned escape hatch from props-as-data.

```tsx
import { useHttp } from '@inertiajs/react'

const { data, setData, get, processing } = useHttp({ q: '' })

// typeahead against a non-Inertia search endpoint; results are ephemeral UI
function onChange(e: React.ChangeEvent<HTMLInputElement>) {
  setData('q', e.target.value)
  get('/api/search', { onSuccess: (r) => setSuggestions(r.results) })
}
```

**Why:** a `useHttp` response is **not** page state — it doesn't flow
through props, so it must not be used to fetch-and-hold data that a partial
reload or deferred prop should deliver
([../navigation/conventions.md](../navigation/conventions.md)). Confine it
to (a) non-Inertia / external endpoints and (b) transient lookups whose
result is ephemeral UI, not domain state you render the page from (search
suggestions, an availability check). If the data belongs on the page, it's
a backend prop — not a `useHttp` call. Type the response and keep it
narrow; `useHttp` quietly growing into a general fetch layer *is* the React
Query / SWR this skill already forbids ([../state/conventions.md](../state/conventions.md)).

## Checklist

- Instant navigation uses `instant` + `prefetch` on a Wayfinder `<Link>`,
  not a client router or a hand-built loading shell.
- Optimistic updates go through `useForm().optimistic` / `<Form optimistic>`
  / `router.optimistic` (props snapshot + auto-rollback); no shadow copy in
  `useState`. Used only for predictable, low-stakes mutations.
- Non-page requests use `useHttp`, typed and narrow; confined to
  non-Inertia endpoints or transient ephemeral-UI lookups — never a stand-in
  for props or a parallel client cache.
