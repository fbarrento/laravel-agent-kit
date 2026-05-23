# Migration Rules

## IDs And Timestamps

Always use UUID primary keys, and they must be **time-ordered** UUIDs
(Laravel's `HasUuids` generates ordered UUIDs; use the UUIDv7 trait where
available — verify the exact trait with `search-docs`), generated
app-side:

```php
$table->uuid('id')->primary();
```

Never use a random UUIDv4 PK. A random PK lands inserts at random points
in the B-tree on large tables — page splits, poor cache locality, write
amplification — which hurts exactly the tens-of-millions-row tables. A
time-ordered UUID inserts near-sequentially and makes `ORDER BY id`
chronological, so `latest('id')` is a valid recency order (see
[history.md](history.md) and [large-tables.md](large-tables.md)). The
trade-off: an ordered/v7 UUID embeds its creation time — acceptable for
internal identifiers.

Always place timestamps immediately after the primary key:

```php
$table->uuid('id')->primary();
$table->timestamps();
```

## Foreign Keys

Always use `foreignIdFor()` for foreign keys and always constrain them:

```php
$table->foreignIdFor(User::class)->constrained();
```

Never use cascading deletes or cascading updates in migrations. Domain behavior should be explicit in actions, not hidden in database cascade rules.

## Defaults And Enums

Never define database defaults in migrations. Set defaults explicitly in application code or data objects.

Never use database enum columns. Use strings or other portable column types and cast to PHP enums in Eloquent models.

## Down Methods

Never define a `down()` method. Migrations are forward-only in this project.

## Checklist

- UUID primary key via `$table->uuid('id')->primary()`, generated
  app-side and **time-ordered** (never random UUIDv4).
- `$table->timestamps()` appears immediately after the primary key.
- Foreign keys use `foreignIdFor(...)->constrained()`.
- No `cascadeOnDelete()`, `cascadeOnUpdate()`, or equivalent cascade behavior.
- No column defaults.
- No database enum columns.
- No `down()` method.
