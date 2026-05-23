# Forms (Inertia v3)

Forms are where the frontend touches the most backend contracts at once:
the route/action (Wayfinder), the input shape (`*FormData`), and the
validation rules + messages (Laravel). The rules keep all three on the
backend's side of the line. Forms live in feature components
(`features/<resource>/<resource>-form.tsx`), never in pages.

Inertia v3 gives two tools: the **`<Form>` component** (declarative) and
the **`useForm` helper** (programmatic). Server-side validation flows back
automatically through Inertia's redirect cycle into `errors` — you never
read a `422` or hand-build messages.

## Decision: `<Form>` component or `useForm`?

- **`<Form>` (default).** A straightforward create/edit form. Declarative,
  exposes `errors`, `processing`, `wasSuccessful`, `reset`, etc. via its
  render prop. Reach for it first.
- **`useForm` (when you need programmatic control).** Multi-step wizards,
  computed/`transform`ed payloads, conditional submit, sharing form state
  across components, or form history (`useForm('Key', {...})`).

**Why:** most forms are a declarative submit-and-show-errors, which is
exactly what `<Form>` removes boilerplate for. `useForm` is the escape
hatch for the genuinely stateful cases — using it everywhere reintroduces
the boilerplate `<Form>` exists to delete.

```tsx
// Good — <Form>: Wayfinder action, server-owned errors, processing state
import { Form } from '@inertiajs/react'
import { store } from '@/actions/generated/App/Http/Controllers/VehicleController'

export function VehicleForm() {
  return (
    <Form action={store()} disableWhileProcessing>
      {({ errors, processing }) => (
        <>
          <input name="name" />
          {errors.name && <p data-part="field-error">{errors.name}</p>}
          <button type="submit" disabled={processing}>Save</button>
        </>
      )}
    </Form>
  )
}
```

## Rule: the action comes from Wayfinder; never handwrite URL or method

Pass the Wayfinder action object to `action` (the `<Form>` infers method
and URL) or to `useForm(store(), {...})`. Never write a literal URL or
`method="post"` string for a Laravel route.

**Why:** a handwritten endpoint is an untyped backend-derived string that
breaks silently on a route rename — the same rule as
[../types/generated.md](../types/generated.md), at the form boundary.
Wayfinder makes the method/URL a typed, generated contract.

## Rule: validation is the server's; render `errors`, never invent messages

Display the `errors` the form exposes (populated automatically when
Laravel throws `ValidationException` via `$request->validate()`). Do not
hard-code validation messages, regex checks, or required-field copy in the
component.

**Why:** validation rules and their wording live in Laravel
([../types/formatting.md](../types/formatting.md)). A client-side message
is a second source of truth that drifts from the server rule and skips
translation. For *real-time* client validation, use the built-in
**Precognition** (`validate()` on the form) — it still runs the server's
rules, so there's one source of truth.

## Rule: typed initial values from the generated form shape

A `useForm` initial-data object is typed by the generated `*FormData`
(aliased `VehicleFormValues` — see [../naming/conventions.md](../naming/conventions.md)),
not a handwritten shape or `any`.

```tsx
import { useForm } from '@inertiajs/react'
import { update } from '@/actions/generated/App/Http/Controllers/VehicleController'
import type { VehicleFormValues } from '@/features/vehicles/vehicle.types'

const form = useForm<VehicleFormValues>({ name: '', tier: 'standard' })
form.transform(d => ({ ...d })).submit(update(vehicleId), {
  preserveScroll: true,
  onSuccess: () => form.reset(),
})
```

## Rule: reflect submit state and reset on success

Disable the submit control while `processing` (or use the `<Form>`
`disableWhileProcessing` prop), and `reset()` / `resetOnSuccess` after a
successful create. Use `preserveScroll` so validation errors don't jump
the page.

**Why:** without a disabled state, users double-submit; without a reset, a
create form keeps stale values. These are the defaults a hand-rolled
fetch would miss and the form helpers give you.

## Rule: file inputs use the form helpers (auto-multipart)

A `<input type="file">` inside `<Form>` / a file field in `useForm` is
sent as `FormData` automatically; track `progress.percentage` for upload
UI. Don't hand-build `FormData` or a manual `fetch`.

## Checklist

- Form is a feature component, not page-owned; `<Form>` by default,
  `useForm` only for programmatic needs (Decision above).
- `action`/submit target is a Wayfinder object — no handwritten URL/method.
- Errors rendered from the form's `errors`; no client-side validation
  messages (Precognition for real-time, which uses server rules).
- `useForm` initial data typed by the generated `*FormData` alias, not
  `any`.
- Submit disabled while `processing`; form resets on successful create;
  `preserveScroll` on submit.
- File uploads go through the form helpers, not manual `FormData`/`fetch`.
