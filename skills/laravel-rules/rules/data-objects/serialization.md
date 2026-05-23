# Data objects across a queue boundary

What happens when a data object is carried by a queued job, and how to
keep it lean and correct. Read alongside [conventions.md](conventions.md)
and [../jobs/conventions.md](../jobs/conventions.md). The Spatie-version
specifics below should be confirmed with `search-docs` / the app's
`composer.lock` before relying on them.

## Rule: a queued data object carries IDs and scalars, never Eloquent models

Laravel serializes a job's properties with PHP `serialize()`. The
`SerializesModels` trait only re-queries Eloquent models that are
**top-level job properties** — a model **nested inside a data object** is
serialized whole, ships stale, and bloats the payload.

So a data object that crosses a queue holds primitives,
[value objects](../value-objects/conventions.md), enums, and IDs (the
same rule the anchor states for *all* data objects). The job passes the
ID; the action re-fetches inside `handle()`.

**Why:** the database is the source of truth. A serialized model snapshot
captured at dispatch time may be out of date — or reference a row that
changed or was deleted — by the time the job runs.

```php
// Good — job carries a lean data object of scalars/IDs; action re-fetches
ProcessSignup::dispatch(new ProcessSignupData(
    waitlistSignupId: $signup->id,
    locale: $signup->locale,
));

// Bad — a model embedded in the queued payload: heavy and stale on run
ProcessSignup::dispatch(new ProcessSignupData(signup: $signup));
```

## Rule: do not hand-roll `__serialize` / `__unserialize` to paper over Spatie

A Spatie `Data` object is a plain PHP object and serializes natively in
the simple case. The pain shows up around `Lazy` / `Optional` / partial
state and nested models — and reconstructing `readonly` promoted
properties in a custom `__unserialize` is awkward and fragile.

When a Spatie Data object does not round-trip cleanly through the queue,
**sidestep rather than patch**: keep models out (rule above), avoid
`Lazy` on queued objects, and if it still fights you, drop to a plain DTO
(next rule). Do not scatter custom magic-method serialization across data
objects.

**Why:** a hand-rolled `__unserialize` couples your payload to Spatie's
internal state representation, which changes between versions — exactly
the kind of drift the queue will surface in production, not in tests.

## Decision: Spatie `Data` or a plain readonly DTO?

Both are valid; choose by what the object needs at its boundary:

- **Spatie `Data`** — use at the edges that need its powers: request
  hydration, validation, casting/transforming, response mapping (HTTP and
  API). See [spatie-laravel-data.md](spatie-laravel-data.md).
- **Plain readonly DTO implementing `Arrayable` + `JsonSerializable`** —
  use for internal, serialization-sensitive payloads (queued jobs,
  internal carriers) where you need none of Spatie's machinery. No
  package magic means nothing surprising to serialize.

```php
// Plain DTO escape hatch — no Spatie, trivially serializable
final readonly class ProcessSignupData implements Arrayable, JsonSerializable
{
    public function __construct(
        public string $waitlistSignupId,
        public string $locale,
    ) {}

    /** @return array{waitlistSignupId: string, locale: string} */
    public function toArray(): array
    {
        return ['waitlistSignupId' => $this->waitlistSignupId, 'locale' => $this->locale];
    }

    public function jsonSerialize(): array
    {
        return $this->toArray();
    }
}
```

**Why:** because [jobs already carry IDs](../jobs/conventions.md), *most*
data objects never touch a queue — so the everyday object stays Spatie
`Data`. The plain DTO is the lean exception for the narrow case that does
cross the wire and needs no boundary powers.

## Edge cases

- **`Optional` on a queued object.** Prefer a concrete nullable type over
  `Optional` for fields that ride a queue, so there is no partial-state
  ambiguity to serialize.
- **Encrypted/sensitive fields.** Do not put secrets in a queued payload;
  carry an ID and load/decrypt inside the job.

## Checklist

- Queued data objects carry IDs, scalars, value objects, enums — no
  Eloquent models.
- The job's action re-fetches models by ID inside `handle()`.
- No bespoke `__serialize`/`__unserialize` added to dodge Spatie quirks.
- Object type chosen via the Decision: Spatie `Data` at boundaries needing
  its powers, plain `Arrayable`/`JsonSerializable` DTO for lean queued
  payloads.
- No secrets in queued payloads.
