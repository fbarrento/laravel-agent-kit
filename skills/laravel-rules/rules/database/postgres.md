# Database — PostgreSQL

> Status: stub — to be deepened (Pass 2). Per-file template. Engine-specific
> notes only; portable rules live in [schema.md](schema.md) /
> [migrations.md](migrations.md) / [performance.md](performance.md).

## Scope

PostgreSQL-specific concerns that differ from the portable defaults:
JSONB, partial/expression indexes, native types, sequences/UUID
generation, transaction/locking quirks.

## TODO (Pass 2)

- JSONB vs JSON; indexing JSONB.
- Partial and expression indexes.
- UUID generation strategy (with the UUID-PK rule in [migrations.md](migrations.md)).
- Locking/isolation quirks relevant to actions/transactions.

## Checklist

- _(to be written)_
