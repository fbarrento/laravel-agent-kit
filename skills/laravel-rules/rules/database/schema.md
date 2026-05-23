# Database — schema

> Status: stub — to be deepened (Pass 2). Per-file template. Sibling to
> [migrations.md](migrations.md) (which owns migration mechanics).

## Scope

Schema design: column types, nullability, indexing strategy, keys, and
relationships at the table level. Migration *mechanics* (UUID PK,
forward-only, no cascades/defaults/DB-enums) live in
[migrations.md](migrations.md).

## TODO (Pass 2)

- Column type selection; nullability defaults.
- Indexing strategy (and its overlap with [performance.md](performance.md)).
- Keys/relationships; portable types over engine-specific.
- Engine-specific notes defer to [mysql.md](mysql.md) / [postgres.md](postgres.md).

## Checklist

- _(to be written)_
