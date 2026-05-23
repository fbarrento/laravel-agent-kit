# Database — performance

> Status: stub — to be deepened (Pass 2). Per-file template.

## Scope

Query and schema performance: indexing for real access patterns, N+1
avoidance, eager loading, pagination, and chunking. Read-composition
shape lives in [../queries/conventions.md](../queries/conventions.md);
this file is the performance lens.

## TODO (Pass 2)

- Indexing for actual query patterns.
- N+1 detection; eager loading conventions.
- Pagination and chunking for large reads.
- Engine-specific tuning defers to [mysql.md](mysql.md) / [postgres.md](postgres.md).

## Checklist

- _(to be written)_
