# Loading, empty & error states

Every surface that shows a collection or async data renders three states
besides the happy path: **empty**, **loading**, and **error**. These are
the same canonical states a story must cover
([../stories/conventions.md](../stories/conventions.md)) — the story
*proves* them, production *renders* them.

## Rule: handle empty, loading, and error explicitly — never a blank render

A component that can be empty, pending, or failing must render a
deliberate state for each. Don't return `null`, a bare spinner with no
context, or a screen that silently shows nothing.

**Why:** the happy path is the rare case in practice — lists start empty,
data is in flight, requests fail. A blank or null render reads as a broken
page; an explicit state tells the user what's happening and what to do.

## Rule: loading uses the framework mechanism, not an ad-hoc spinner-on-mount

- **Deferred data** → render inside `<Deferred fallback={<Skeleton/>}>`
  ([../navigation/conventions.md](../navigation/conventions.md)); the
  fallback is the loading state.
- **Form submit** → drive busy UI from the form's `processing`
  ([../forms/conventions.md](../forms/conventions.md)).
- **Navigation** → the `<Link>` `data-loading` attribute styles in-flight
  links.

Don't hand-roll a `useState(isLoading)` + `useEffect` fetch to recreate
what deferred props / `processing` already give you.

**Why:** Inertia already knows when data is deferred or a form is
submitting. An ad-hoc loading flag is a second, hand-maintained source of
the same truth — and usually the symptom of a client fetch that shouldn't
exist ([../state/conventions.md](../state/conventions.md)).

## Rule: empty states are a real component with backend copy

An empty collection renders a dedicated empty-state component
(`features/<resource>/<resource>-empty-state.tsx`) whose heading, body,
and primary action use backend-provided copy
([../types/formatting.md](../types/formatting.md)), not hard-coded strings.

```tsx
{vehicles.length === 0
  ? <VehicleEmptyState copy={copy} can={can} />
  : <VehicleTable vehicles={vehicles} />}
```

**Why:** the empty state is often the user's first screen; treating it as
an afterthought (a bare "No results") wastes the moment that should
onboard them. A real component with backend copy makes it reviewable (a
story state) and translatable.

## Rule: catch render failures with an error boundary; surface request failures

Wrap pages/regions in an error boundary so a render error shows a recovery
UI, not a white screen. For failed requests, surface the failure (a flash
message or inline error), and let Inertia's error handling cover
unexpected server responses — don't swallow errors silently.

**Why:** an uncaught render error blanks the whole app; a swallowed
request failure leaves the user staring at stale or empty UI with no idea
it failed. Both must fail *visibly*.

## Rule: a disabled/permission-blocked state is explicit too

When `can.*` capability flags forbid an action, render the control as
disabled (or omit it) with the reason where useful — don't show an action
that errors on click. Drive it from the backend capability prop, not a
client guess. The backend-owned-authorization rule this rests on is the
canonical [../authorization/conventions.md](../authorization/conventions.md).

## Checklist

- Collection/async surfaces render explicit empty, loading, and error
  states — never blank/null.
- Loading comes from `<Deferred>` fallbacks, form `processing`, or
  `data-loading`; no ad-hoc `isLoading` + `useEffect` fetch.
- Empty state is a dedicated component using backend copy.
- Error boundary around pages/regions; request failures surfaced, not
  swallowed.
- Capability-blocked actions rendered disabled/omitted from `can.*`, not a
  client guess.
- These states match the component's required story states.
