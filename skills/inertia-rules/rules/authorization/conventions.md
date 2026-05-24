# Authorization & capability-gated UI

Who may do what is decided by Laravel policies/gates and delivered to the
frontend as capability booleans. The frontend **renders** those decisions;
it never **makes** them. Same boundary as backend-owned copy and types — the
frontend never owns what Laravel owns.

## Rule: gate UI from backend `can.*` capability props — never reimplement authorization

The backend computes capability booleans (from policies/gates) and ships
them as typed props ([../types/generated.md](../types/generated.md)). The
frontend reads them — `can.update`, `can.delete` — to decide what to show or
enable. Never re-derive a permission in JS from role strings, ownership
comparisons (`user.id === vehicle.ownerId`), or feature flags.

```tsx
// Good — render from the backend capability
{can.delete && <DeleteVehicleButton vehicle={vehicle} />}

// Bad — authorization logic reimplemented on the client
{user.role === 'admin' || user.id === vehicle.ownerId
  ? <DeleteVehicleButton vehicle={vehicle} />
  : null}
```

**Why:** the policy is the single source of authorization truth. Re-deriving
it on the client duplicates rules that drift the moment the policy changes,
and ships business logic (who owns what, which roles may act) to a place the
user controls. Reading a `can.*` boolean keeps the decision in one place —
the backend — and the frontend honest about only displaying it.

## Rule: capability fields are outcome-named — `can.createTeam`, not `can.canCreateTeam`

The `can` field is the **outcome**, so it doesn't stutter against the `can`
accessor: read `can.createTeam`, never `can.canCreateTeam`. The backing object is
the page's `*PageAuthorizationData` (exposed as the `can` prop), with one boolean
per action outcome. The naming and backend shape are owned by laravel-rules
`data-objects/inertia-page-data`; the frontend only reads the field.

```tsx
{can.createTeam && <CreateTeamButton />}      // Good — reads as a sentence
{can.canCreateTeam && <CreateTeamButton />}   // Bad — stutters
```

## Rule: hide or disable the control from the capability, at the right granularity

When `can.x` is false, omit the control or render it disabled (with a reason
where useful) — driven by the prop, never a control that 403s on click. Gate
at the granularity of the action: a single button by its own `can.*`, a whole
section by the capability that governs it. This is the permission-blocked
case of the explicit-state rule
([../loading-states/conventions.md](../loading-states/conventions.md)).

**Why:** showing an action the user can't perform invites a dead-end click
and a server rejection; hiding or disabling it from the same boolean the
server uses keeps the UI truthful. Gating at the wrong level — a whole page
off one button's flag, or every button re-checking a page-level flag — either
hides too much or scatters the check.

## Rule: gating is UX, not security — the server still authorizes

A hidden button is not protection. The action's route is still guarded by the
policy server-side (laravel-rules `security/authorization`); the frontend gate
only spares the user actions that would be rejected. Never treat `can.*` as
the enforcement boundary.

**Why:** capability props travel to the client, where anything can be edited
or replayed. Authorization that isn't enforced on the server isn't
enforcement — the frontend gate is a courtesy to the user, not a lock.

## Checklist

- Visible/enabled actions are gated by backend `can.*` props, never by
  client-side role/ownership/flag logic.
- Forbidden actions are hidden or disabled from the capability prop, not
  rendered as controls that 403.
- Capability props are typed from generated backend contracts
  ([../types/generated.md](../types/generated.md)).
- Capability fields are outcome-named (`can.createTeam`), not `can.can*`; backed
  by the page's `*PageAuthorizationData` (laravel-rules `data-objects/inertia-page-data`).
- Server-side policy enforcement is assumed in place — the UI gate is UX,
  not the security boundary.
