# Model Rules

## Creation

Always create new models with Artisan and include the related factory, migration, and seeder:

```bash
php artisan make:model ModelName -fms --no-interaction
```

Use the concrete model name, for example:

```bash
php artisan make:model WaitlistSignup -fms --no-interaction
```

Do not manually create model, migration, factory, or seeder files when Artisan can generate the correct structure.

## Casts

Every Eloquent model must cast every persisted attribute in `casts(): array`, including:

- Primary keys and foreign keys.
- Strings, decimals, booleans, integers, enums, and nullable attributes.
- `created_at`, `updated_at`, and other date/time columns.

Do not rely on Laravel's implicit timestamp casts when editing or creating a model. Keep casts explicit and complete.

## Scopes

Never implement Eloquent scopes on models. Model scopes hide query behavior behind Laravel magic and make it harder to understand what is being called and when.

Put reusable read filters and query composition in query objects under `app/Queries` instead.

## Deletes

Never use the `SoftDeletes` trait. Deletes are hard deletes — the row is
actually removed.

Soft deletes keep "deleted" rows in the table forever, which is a GDPR /
right-to-erasure liability (personal data you believe is gone is still
stored) and a steady source of stale data and surprising query results.
They also add a global scope — the same Eloquent magic the **Scopes** rule
above rejects — and complicate unique constraints.

If you need to retain a record of what existed, use an append-only history
table ([../database/history.md](../database/history.md)), not a
`deleted_at` flag. When deleting a parent, delete its children explicitly
first, inside one transaction ([../architecture/transactions.md](../architecture/transactions.md));
constrained foreign keys ([../database/migrations.md](../database/migrations.md))
make a forgotten child throw rather than leave orphaned personal data
behind.

## Tests

Every model must have a unit test that verifies its array shape:

```php
test('to array', function (): void {
    $model = SomeModel::factory()->create()->refresh();

    expect(array_keys($model->toArray()))
        ->toBe([
            'id',
            'name',
            'created_at',
            'updated_at',
        ]);
});
```

The expected array keys should match the public serialized shape, including hidden attributes and appended values when applicable.

## Checklist

- Create new models with `php artisan make:model ModelName -fms --no-interaction`.
- Cast all persisted columns explicitly.
- Include enum casts for enum-backed columns.
- Include decimal precision in decimal casts.
- Include timestamp casts rather than relying on Laravel defaults.
- Do not add local or global model scopes.
- Do not use the `SoftDeletes` trait; deletes are hard deletes (retain
  history via an append-only table, not `deleted_at`).
- Add or update a `to array` test for every model touched.
