# Observers (guardrail)

> Status: stub — to be deepened (Pass 2). Per-file template, framed as a
> guardrail: prefer actions/events; document when an observer is ever
> acceptable.

## Scope

Model observers. Consistent with the no-model-magic stance (no scopes,
explicit reads), observers are discouraged: they hide side effects
behind Eloquent lifecycle hooks. This folder documents what to do
instead and the narrow cases where an observer is acceptable.

## TODO (Pass 2)

- Why observers are discouraged (hidden side effects, ordering, testing).
- Prefer: side effects in actions; reactions via events
  ([../events/conventions.md](../events/conventions.md)).
- The narrow acceptable cases (if any) and their constraints.
- After-commit/dispatch rules still apply
  ([../architecture/transactions.md](../architecture/transactions.md)).

## Checklist

- _(to be written)_
