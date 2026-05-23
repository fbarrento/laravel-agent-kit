# HTTP

> Status: stub — to be deepened (Pass 2). Per-file template.

## Scope

Internals of the HTTP layer: controllers, form requests, API resources,
routing. Controllers validate/prepare input, call an action or query,
then respond — they hold no business logic (see
[../architecture/cqrs.md](../architecture/cqrs.md)).

## TODO (Pass 2)

- Controller shape; thin controllers delegating to actions/queries.
- Form requests for input validation (vs invariants/data-object
  validation).
- API resources for output shaping; relationship to data objects.
- Routing conventions.
- HTTP tests live in `tests/Feature` ([../testing/conventions.md](../testing/conventions.md)).

## Checklist

- _(to be written)_
