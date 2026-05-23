# Data objects (DTOs, list-options, enums)

Three flavors of `Data\` class. All `final readonly`. Mirror the spec's
field names in snake_case in serialization; use camelCase in PHP.

## Output DTOs (response hydration)

For every resource the SDK reads back from the API. Implements
`JsonSerializable`, has a `static from(array $data): self` for hydration,
emits snake_case via `jsonSerialize()`.

```php
final readonly class Widget implements JsonSerializable
{
    public function __construct(
        public string $id,
        public string $name,
        public ?int $credentialId,
        public DateTimeImmutable $createdAt,
    ) {}

    public static function from(array $data): self
    {
        $id = $data['id'] ?? null;
        if (! is_string($id)) {
            throw new InvalidArgumentException('Widget data is missing the `id` field.');
        }
        $attributes = $data['attributes'] ?? null;
        if (! is_array($attributes)) {
            throw new InvalidArgumentException('Widget data is missing the `attributes` object.');
        }
        return new self(
            id: $id,
            name: self::requireString($attributes, 'name'),
            credentialId: self::optionalInt($attributes, 'credential_id'),
            createdAt: self::requireDate($attributes, 'created_at'),
        );
    }

    /** Reusable strict helpers — copy into each DTO. */
    private static function requireString(array $attributes, string $key): string { /* ... */ }
    private static function optionalString(array $attributes, string $key): ?string { /* ... */ }
    private static function requireInt(array $attributes, string $key): int { /* ... */ }
    private static function optionalInt(array $attributes, string $key): ?int { /* ... */ }
    private static function requireBool(array $attributes, string $key): bool { /* ... */ }
    private static function optionalBool(array $attributes, string $key): ?bool { /* ... */ }
    private static function requireDate(array $attributes, string $key): DateTimeImmutable { /* ... */ }

    /** @return array{id: string, name: string, credential_id: ?int, created_at: string} */
    #[Override]
    public function jsonSerialize(): array
    {
        return [
            'id' => $this->id,
            'name' => $this->name,
            'credential_id' => $this->credentialId,
            'created_at' => $this->createdAt->format(DATE_ATOM),
        ];
    }
}
```

**Be lenient where the spec is strict.** If the API actually returns
`null` for a field the spec marks required-non-null (this happens! see
[pitfalls.md](pitfalls.md)), mark it `?T` and use the `optionalX`
helper. The fixture from a real recording is the source of truth — the
spec is a hint.

**Don't enum-ify open strings.** If the spec's `slug` / `disk_type` /
`architecture` is just `"type": "string"` with no `enum:` constraint,
the DTO field stays `string`. Add an `Enums\X` constant table separately
for ergonomic comparisons (`$widget->kind === WidgetKind::Standard->value`).

## Input DTOs (request payloads)

For every endpoint that takes a JSON body. Has `toArray(): array` that
strips nulls so partial-update endpoints don't accidentally clear
fields.

```php
final readonly class UpdateWidgetData
{
    public function __construct(
        public ?string $name = null,
        public ?string $color = null,
        public ?array $tags = null,
    ) {}

    /** @return array<string, mixed> */
    public function toArray(): array
    {
        $payload = [];
        if ($this->name !== null) $payload['name'] = $this->name;
        if ($this->color !== null) $payload['color'] = $this->color;
        if ($this->tags !== null) $payload['tags'] = $this->tags;
        return $payload;
    }
}
```

For create-payloads with provider-polymorphic nested objects
(e.g. `hetzner: { region_id, size_id, network_id }`), make each
provider its own DTO (`HetznerWidgetConfig`) with its own `toArray()`,
and embed the optional config in the parent DTO:

```php
final readonly class CreateWidgetData
{
    public function __construct(
        public string $name,
        public WidgetType $type,
        public ?HetznerWidgetConfig $hetzner = null,
    ) {}

    public function toArray(): array
    {
        $payload = [
            'name' => $this->name,
            'type' => $this->type->value,
        ];
        if ($this->hetzner instanceof HetznerWidgetConfig) {
            $payload['hetzner'] = $this->hetzner->toArray();
        }
        return $payload;
    }
}
```

Add new provider configs lazily — only when the SDK needs to support
creating widgets for that provider.

## List-options DTOs (query params)

For paginated GET endpoints. Has `toQuery(): array` emitting only
non-null fields, with `page[size]` / `page[cursor]` / `sort` /
`filter[...]` keys.

```php
final readonly class ListWidgetsOptions
{
    public function __construct(
        public ?int $size = null,
        public ?string $cursor = null,
        public ?string $sort = null,
        public ?string $name = null,
    ) {}

    /** @return array<string, int|string> */
    public function toQuery(): array
    {
        $query = [];
        if ($this->size !== null) $query['page[size]'] = $this->size;
        if ($this->cursor !== null) $query['page[cursor]'] = $this->cursor;
        if ($this->sort !== null) $query['sort'] = $this->sort;
        if ($this->name !== null) $query['filter[name]'] = $this->name;
        return $query;
    }
}
```

If a filter target name collides with a pagination field
(`filter[size]` vs `page[size]`), rename the constructor param to
disambiguate (`sizeFilter` instead of `size`). Keep `size` for
pagination — that's the established precedent.

## Enums

Use only for closed sets the spec **explicitly** enumerates. Backed
string enum, kebab/snake-case values matching the wire format.

```php
enum WidgetAction: string
{
    case Reboot = 'reboot';
    case PowerCycle = 'power-cycle';
}
```

Place under `src/Enums/`. Mirror exact spec values, including any
inconsistent casing (e.g. `'php56-old'` for an old PHP build).

When in doubt — open strings, not enums. Spec ambiguity, runtime
inconsistency (display labels like `'NVMe SSD'` with spaces), and
forward compatibility all argue for lenient strings.

## Factories

Every Data class gets a factory under `tests/Factories/<X>Factory.php`,
using `fbarrento/data-factory`. See the **pest-package-tests** skill for
factory shape.

```php
final class WidgetFactory extends Factory
{
    protected string $dataObject = Widget::class;

    public function definition(): array
    {
        return [
            'id' => (string) $this->fake->numberBetween(1, 99_999),
            'name' => $this->fake->bothify('widget-##'),
            'credentialId' => $this->fake->numberBetween(1, 9_999),
            'createdAt' => new DateTimeImmutable('-1 month'),
        ];
    }
}
```
