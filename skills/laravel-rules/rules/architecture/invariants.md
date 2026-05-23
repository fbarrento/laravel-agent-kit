# Domain invariants

Which layer owns domain invariants, and when to introduce one. Settled,
codebase-wide **policy** (see [placement.md](placement.md)). This is the
canonical home; `actions/` links here for the *who enforces* rule, and
`exceptions/` owns the *how to signal a violation* mechanics.

## Rule: actions enforce invariants

Domain invariants are enforced inside actions. Controllers, commands,
jobs, queries, and models do not enforce business invariants.

**Why:** an invariant is a guarantee about a state change, and state
changes live in actions (CQRS, see [cqrs.md](cqrs.md)). Enforcing
elsewhere splits the guarantee across layers and lets an unguarded path
violate it.

## Rule: signal violations with a specific business exception

When an invariant fails, throw a specific business exception — never a
generic `Exception`/`RuntimeException`, and never return `false`.
Naming and hierarchy mechanics live in [exceptions/](../exceptions/conventions.md).

```php
// Good
throw new DuplicateWaitlistSignupException($email);

// Bad
throw new RuntimeException('already signed up');
return false;
```

**Why:** a typed business exception lets callers handle the specific
domain failure and makes the invariant self-documenting. `false` and
generic exceptions erase what actually went wrong.

## Decision: when does a rule deserve to be a domain invariant?

> **TODO (Pass 2):** decision tree — distinguish a true domain invariant
> (must always hold for the model to be valid; enforced in the action)
> from input validation (form requests / data objects) and from
> database constraints. Cover where each belongs and how they layer.

## Checklist

- Invariants are enforced in actions, not other layers.
- Violations throw a specific business exception (see `exceptions/`).
- No generic exceptions or `false` returns for domain failures.
