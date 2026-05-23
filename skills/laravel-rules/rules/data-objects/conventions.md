# Data objects

> Status: stub — to be deepened (Pass 2). Per-file template: Rule → Why →
> Good/Bad → Edge cases → Checklist.

## Scope

Internals of Spatie Laravel Data objects: command inputs, results, and
nested data. Casts and transformers nest under `app/Data/Casts` and
`app/Data/Transformers` — the only sanctioned nesting (see the registry
in [../architecture/structure.md](../architecture/structure.md)).

## TODO (Pass 2)

- Input vs result data objects; immutability/readonly.
- `app/Data/Casts` and `app/Data/Transformers` usage and when to write
  each.
- Validation boundary: what belongs in a data object vs a form request
  vs an action invariant ([../architecture/invariants.md](../architecture/invariants.md)).
- Null-stripping / serialization conventions; to-array tests.

## Checklist

- _(to be written)_
