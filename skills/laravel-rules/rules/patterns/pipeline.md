# Pipeline (pattern)

> Status: stub — to be deepened (Pass 2). Per-file template: Rule → Why →
> Good/Bad → Edge cases → Checklist, with a **Decision** section (this is
> an opt-in technique, so the Decision is the heart of the file).

## Scope

An optional composition technique: a workflow expressed as ordered,
swappable stages threading a payload through. Opted into per-case
(`patterns/`, see [../architecture/placement.md](../architecture/placement.md)),
not mandatory. Often applied inside an orchestrator action.

## TODO (Pass 2)

- Decision: when a pipeline beats inline steps (conditional, reorderable,
  independently testable/swappable stages) vs when it is over-engineering.
- Stage contract: shape of a stage, how the payload threads through.
- Registration/ordering of stages.
- Good/Bad examples; testing a pipeline and its stages.
- Cross-ref from [../actions/conventions.md](../actions/conventions.md).

## Checklist

- _(to be written)_
