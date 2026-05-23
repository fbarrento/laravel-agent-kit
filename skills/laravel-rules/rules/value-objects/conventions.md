# Value objects

> Status: stub — to be deepened (Pass 2). Per-file template.

## Scope

Internals of domain value objects (e.g. `Money`, `Email`): immutable,
self-validating, compared by value. Distinct from data objects (which
carry command/result payloads).

## TODO (Pass 2)

- Immutability + readonly; construction/validation in the constructor.
- Equality by value; no identity.
- When to introduce a value object vs a scalar/enum/data object.
- Casting value objects on models; testing.

## Checklist

- _(to be written)_
