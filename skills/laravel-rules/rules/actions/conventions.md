# Action Rules

## Purpose

Actions encapsulate all business logic and state mutation workflows. Controllers, console commands, and jobs may depend on actions, but they must not implement business logic themselves.

Every action exposes a `handle()` method:

```php
final class CreateOrganization
{
    public function handle(CreateOrganizationData $createOrganizationData): Organization
    {
        // ...
    }
}
```

Name actions with a verb first, then the affected subject or subjects. Use names like `RegisterOrganization`, `CreateOrganization`, and `AttachUserToOrganization`.

## Inputs

Avoid passing Eloquent models directly into actions. Pass purpose-built data objects instead so the action receives an explicit command-shaped input.

- Good: `CreateWaitlistSignupData $createWaitlistSignupData`
- Avoid: `User $user` when a data object can describe the operation.

Use names that describe the input value, not generic names like `$data` when a precise data object name exists.

## Decision: single-responsibility vs orchestrator

Two action shapes. Choose by responsibility and number of writes:

- **Single-responsibility** — one focused operation. Reach for this by
  default.
- **Orchestrator** — coordinates a workflow, usually injecting other
  actions. Reach for this when the operation composes ≥2 actions or
  spans multiple writes.

When an orchestrator's steps are conditional, reorderable, or
independently swappable, consider structuring it with the
[pipeline pattern](../patterns/pipeline.md) rather than inline calls.

Transaction timing for multi-write workflows is governed by
[architecture/transactions.md](../architecture/transactions.md) — single
writes need no transaction; orchestrators wrap multiple writes in one.

## Dependencies

Actions may be dependencies of controllers, console commands, jobs, and
other orchestrator actions.

Services must not contain internal business logic. Use services only for
external systems; actions may depend on services when they need to call
third-party APIs or remote systems.

Controllers, console commands, and jobs validate or prepare input, call
an action, then return/output/dispatch. They must not enforce domain
workflows directly.

## Domain invariants

Actions are the enforcer of domain invariants, and they signal a
violation with a specific business exception. The *who/when/how* is
governed by [architecture/invariants.md](../architecture/invariants.md)
and [exceptions/](../exceptions/conventions.md) — this folder does not
restate it.

## Checklist

- Action has a `handle()` method.
- Action input is a data object where operation input is needed.
- Action shape chosen via the Decision above (single vs orchestrator).
- Transaction + invariant rules deferred to their canonical homes
  (linked above), not re-decided here.
- Controllers, commands, and jobs delegate business logic to actions.
