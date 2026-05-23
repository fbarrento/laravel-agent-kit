# Events

> Status: stub — to be deepened (Pass 2). Per-file template.

## Scope

Internals of event classes and listeners. Emission timing/origin
(after-commit, dispatched from actions) is governed by
[../architecture/transactions.md](../architecture/transactions.md) — this
folder does not restate it.

## TODO (Pass 2)

- Event class shape; immutable payloads.
- Listener shape; sync vs queued listeners.
- When an event is the right tool vs a direct action call.
- Testing with `Event::fake()`.

## Checklist

- _(to be written)_
