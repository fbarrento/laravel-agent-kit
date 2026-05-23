# Mass assignment

> Status: stub — to be deepened (Pass 2). Per-file template.

## Scope

Guarding Eloquent writes against unintended attribute assignment.
Cross-cutting security concern.

## TODO (Pass 2)

- `fillable`/`guarded` policy; never `Model::create($request->all())`.
- Prefer typed data objects as the write contract
  ([../data-objects/conventions.md](../data-objects/conventions.md)) over
  raw request arrays — actions receive a data object, not request input.
- Route-model-binding + over-posting risks.
- Testing that extra fields are rejected.

## Checklist

- _(to be written)_
