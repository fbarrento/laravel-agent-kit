# Enums

> Status: stub — to be deepened (Pass 2). Per-file template.

## Scope

Internals of PHP enums: backing, naming (no `Enum` suffix — see
[../naming/conventions.md](../naming/conventions.md)), and how they are
cast on models (DB stores strings, not native DB enums — see
[../database/migrations.md](../database/migrations.md)).

## TODO (Pass 2)

- Backed enums; string backing over int.
- Methods on enums (labels, helpers) vs keeping them thin.
- Casting on models; the no-DB-enum-column rule cross-ref.
- Testing enum behavior.

## Checklist

- _(to be written)_
