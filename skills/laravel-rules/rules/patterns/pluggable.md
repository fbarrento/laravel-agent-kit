# Pluggable / strategy (pattern)

> Status: stub — to be deepened (Pass 2). Per-file template with a
> **Decision** section at its heart (opt-in technique).

## Scope

An optional technique: swappable implementations selected at runtime or
via the container (strategy). Opted into per-case (`patterns/`, see
[../architecture/placement.md](../architecture/placement.md)).

## TODO (Pass 2)

- Decision: when swappable strategies earn their indirection vs a simple
  conditional.
- Contract/interface shape; how an implementation is selected and bound.
- Relationship to DI (see [../architecture/dependency-injection.md](../architecture/dependency-injection.md)).
- Good/Bad examples; testing with in-memory implementations.

## Checklist

- _(to be written)_
