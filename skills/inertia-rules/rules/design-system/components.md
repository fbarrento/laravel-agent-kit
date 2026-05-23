# Component roles

Three component roles, each with a different contract. The role decides
what a component may know and what it must ship with.

| Role | Path | Knows about | Story |
|---|---|---|---|
| Primitive | `components/ui/*` | nothing domain-specific | required |
| App component | `components/app/*` | generic app concepts | required |
| Feature component | `features/<resource>/*` | one resource | when reusable/stateful |

## Rule: primitives are domain-free and token-bound

`components/ui/*` are low-level, reusable, domain-free, token-bound
building blocks (Button, Input, Badge). Requirements:

- colocated story (required);
- small typed public API; finite variant/size sets, all represented in
  the story;
- styling via `ds-` semantic utilities only;
- state expressed through props and useful `data-*` attributes;
- **no** backend, resource, or domain concepts; **no** raw colors,
  arbitrary values, inline hex, or primitive variables.

**Why:** a primitive is shared by the whole app, so any domain concept or
raw value in it contaminates everything downstream. Domain-free +
token-bound is what makes it safe to reuse and to reskin.

```txt
components/ui/button.tsx
components/ui/button.stories.tsx
```

## Rule: app components are reusable and generic

`components/app/*` are reusable product components above primitive level
(PageHeader, EmptyState, DataTable, FilterBar). They may compose
primitives and accept generic data. Requirements:

- colocated story (required);
- generic across resources — **no** resource-specific names or
  backend-specific assumptions;
- generic generated/shared types allowed; resource-specific types belong
  in `features/<resource>`.

**Why:** the value of an app component is reuse across resources; the
moment it says "vehicle" it's a feature component in the wrong folder.

## Rule: feature components own one resource's UI

`features/<resource>/*` own resource-specific workflow UI (VehicleTable,
VehicleForm, VehicleFilters). Requirements:

- use generated backend-derived types ([../types/generated.md](../types/generated.md));
- use typed local fixtures for stories
  ([../stories/conventions.md](../stories/conventions.md));
- get a story when reusable, stateful, visually important, exported, or
  likely to be edited by agents;
- if a feature component becomes generic across resources, **promote** it
  to `components/app/*` and update imports.

**Why:** resource UI is where domain knowledge legitimately lives; keeping
it in the feature folder (not in a primitive or app component) preserves
the reusability of the lower roles and keeps the resource's surface
together.

## Decision: which role does this component belong to?

- Domain-free, low-level, token-bound? → **primitive** (`components/ui`).
- Reusable across resources, generic data, above primitive level? →
  **app component** (`components/app`).
- Specific to one resource's workflow/data? → **feature**
  (`features/<resource>`).

If you're unsure between app and feature: does it name or assume a
resource? Yes → feature. No, and ≥2 resources would use it → app.

## Checklist

- Primitives: domain-free, token-bound, finite typed API, colocated story,
  no raw styling.
- App components: generic, reusable, no resource names, colocated story.
- Feature components: generated types, typed fixtures, story when
  reusable/stateful; promoted to `components/app` if they go generic.
- Role chosen via the Decision above, not by where the file was first
  dropped.
