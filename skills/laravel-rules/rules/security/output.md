# Output safety

> Status: stub — to be deepened (Pass 2). Per-file template.

## Scope

Preventing sensitive or unsafe data from leaving the app: response
shaping, escaping, and hidden attributes. Cross-cutting security concern.

## TODO (Pass 2)

- Never expose secrets/internal fields in API responses; use response
  data objects ([../data-objects/conventions.md](../data-objects/conventions.md)),
  not raw models.
- Model `$hidden`/serialization for secret-bearing columns (ties to
  [secrets.md](secrets.md)).
- Output escaping for rendered content.
- Testing response shape excludes sensitive fields.

## Checklist

- _(to be written)_
