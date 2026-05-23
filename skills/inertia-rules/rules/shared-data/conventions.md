# Shared data & page meta (Inertia v3)

Ambient page context: the data every page needs (auth user, flash, app
config) and the document head (title, meta). Both come from the backend —
shared data through the `HandleInertiaRequests` middleware, head tags
through `<Head>`.

## Rule: ambient data is shared from the middleware, not prop-drilled

Cross-cutting data (auth user, flash messages, app name, feature flags)
is shared once in `HandleInertiaRequests::share()` and read where needed
via `usePage().props`. Don't pass it down as a prop through every page and
component.

```php
// app/Http/Middleware/HandleInertiaRequests.php
public function share(Request $request): array
{
    return array_merge(parent::share($request), [
        'auth' => ['user' => fn () => $request->user()?->only('id', 'name', 'email')],
        'flash' => ['success' => fn () => $request->session()->get('success')],
    ]);
}
```
```tsx
import { usePage } from '@inertiajs/react'
const { auth } = usePage().props
```

**Why:** auth/flash are needed everywhere; threading them through props
pollutes every page signature and every intermediate component. Sharing +
`usePage` makes them ambient, read only where used (typically a layout).

## Rule: shared props are typed too

Type `usePage().props` against generated shared types — don't read
`usePage().props` as `any`. The shared shape (auth, flash) is backend-owned
truth like any other prop ([../types/generated.md](../types/generated.md));
generate it (Spatie Data) and import it.

**Why:** `usePage().props.auth.user.naem` should fail at compile time. An
untyped `usePage()` is the same drift hole as a handwritten DTO, just in
the ambient layer.

## Rule: surface flash and validation errors in one place

Read the shared `flash` prop in a layout (or a top-level toast region) and
render it once. Inertia auto-shares validation `errors`; prefer the
**form-scoped** `errors` (from `<Form>`/`useForm`) for field messages, and
reserve the shared `errors` prop for cross-cutting cases.

**Why:** a single flash region means every page gets notifications for
free without each page wiring its own. Field errors belong with their
form (where the user is looking), not in a global banner.

## Rule: set the page title and meta with `<Head>`

Inertia apps render in `<body>`, so document head tags go through the
`<Head>` component — never by reaching for `document.title`. Use the
`title` shorthand per page; set a global suffix once via the
`createInertiaApp` `title` callback; dedupe shared tags with `head-key`.

```tsx
import { Head } from '@inertiajs/react'
<Head title="Vehicles" />
```
```js
createInertiaApp({ title: (title) => `${title} — Fleet`, /* ... */ })
```

**Why:** `<Head>` is how Inertia manages head tags across client-side
visits; a manual `document.title` write isn't tracked and gets clobbered
on the next navigation. The global callback keeps the app-name suffix in
one place instead of every page.

## Rule: page copy still comes from the backend, not shared dictionaries

Shared data is for *state* (who's logged in, a flash message), not for a
frontend copy/translation dictionary. User-facing strings come from page
props ([../types/formatting.md](../types/formatting.md)); titles that are
domain copy come from the backend too.

## Checklist

- Auth/flash/app-config shared via `HandleInertiaRequests::share()` and
  read via `usePage().props`, not prop-drilled.
- `usePage().props` typed against generated shared types — never `any`.
- Flash surfaced once (layout/toast); field errors come from the form, not
  the global `errors` prop.
- Title/meta set via `<Head>` (+ global `title` callback, `head-key`
  dedup); no `document.title` writes.
- Shared data carries state, not a frontend copy/translation dictionary.
