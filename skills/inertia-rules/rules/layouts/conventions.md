# Layouts (Inertia v3)

Layouts are the app chrome (nav, sidebar, flash region) that wraps page
content. Use **persistent** layouts so that chrome — and its state —
survives client-side navigation instead of being torn down and rebuilt on
every visit. Layouts live in `layouts/`.

## Rule: use persistent layouts, not page-wrapping

Assign a layout via the page's `layout` property (or a default in
`createInertiaApp`). Do **not** wrap each page's JSX in `<AppLayout>…
</AppLayout>` — that destroys and recreates the layout on every visit.

```tsx
// Good — persistent: Inertia keeps the layout instance alive across visits
function VehiclesIndex(props: ...) { /* page content only */ }
VehiclesIndex.layout = (page: React.ReactNode) => <AppLayout>{page}</AppLayout>
export default VehiclesIndex

// Bad — wrapping rebuilds the layout (and loses its state) on every navigation
export default function VehiclesIndex() {
  return <AppLayout>{/* ... */}</AppLayout>
}
```

**Why:** a persistent layout instance preserves state across navigations —
sidebar scroll, an open menu, a playing media element, the flash/toast
region — and avoids re-mounting the whole chrome on each visit. Wrapping
re-creates it every time, dropping that state and flickering.

## Rule: set a default layout in `createInertiaApp`; exclude public pages

Apply the app layout once as a default, and opt specific pages out
(auth/marketing screens) rather than assigning the layout on every page.

```js
createInertiaApp({
  layout: (name) => (name.startsWith('Public/') ? null : AppLayout),
  // ...
})
```

**Why:** most pages share one shell; a global default removes the
per-page `layout` line and the risk of forgetting it. Per-page assignment
then becomes the *exception* (a different shell), which is where it earns
its keep.

## Rule: nest layouts by composing, not by deep page trees

Stack layouts with an array (`layout: [AppLayout, SettingsLayout]`) when a
section needs an inner shell. This is layout composition — it is unrelated
to page folders, which stay flat ([../architecture/roles.md](../architecture/roles.md)).

**Why:** nested layouts express "settings pages share a sub-shell" without
nesting the `pages/` tree. Composition at the layout level keeps the page
folder flat and the shared chrome in one place.

## Rule: layouts hold chrome; pages hold content

A layout owns app-wide chrome: navigation, sidebar, header, the flash/
toast region, and reading shared data via `usePage()`
([../shared-data/conventions.md](../shared-data/conventions.md)). A page
owns only its content and composes features. Keep resource/domain UI out
of layouts.

**Why:** the layout is shared by every page it wraps, so a resource
concept in it (a "vehicles" menu hard-coded with vehicle logic) couples
unrelated pages to that resource — the same contamination rule as
primitives. Chrome is generic; content is the page's job.

## Rule: pass dynamic layout data through layout props, not globals

When a layout needs page-derived data (a title, a section flag), pass it
via layout props (static `layout: [AppLayout, { section: 'fleet' }]`,
callback from page props, or runtime `setLayoutProps`) — not a module
global or context hack.

## Checklist

- Layouts are persistent (page `layout` property / `createInertiaApp`
  default), never per-page `<Layout>` wrapping.
- A default layout is set app-wide; public/auth pages opt out.
- Section shells use nested layout arrays; `pages/` stays flat.
- Layouts hold only generic chrome + shared-data reads; no resource/domain
  UI or content.
- Layout-specific data passed via layout props, not globals.
