# Resources

Saloon `BaseResource` subclasses. Two flavors per domain: a **collection
resource** (plural) and an **item resource** (singular). Resources are
thin glue between the connector and request classes — they don't hold
state beyond what they need to build URLs.

## Collection resource

Methods: `all()`, `iterate()`, `create()`.

```php
final class WidgetsResource extends BaseResource
{
    use ParsesPage;

    public function __construct(
        Connector $connector,
        private readonly string $organization,    // if org-scoped
        private readonly int|string $parentId,    // if nested under a parent
    ) {
        parent::__construct($connector);
    }

    /** @return Page<Widget> @throws Throwable */
    public function all(?ListWidgetsOptions $options = null): Page
    {
        return $this->parsePage(
            $this->connector->send(new GetWidgets($this->organization, $this->parentId, $options)),
            Widget::from(...),
        );
    }

    /** @return Generator<int, Widget> @throws Throwable */
    public function iterate(?ListWidgetsOptions $options = null): Generator
    {
        $options ??= new ListWidgetsOptions;
        do {
            $page = $this->all($options);
            yield from $page;                   // NOT `foreach { yield $x; }` (coverage)
            $options = new ListWidgetsOptions(  // forward EVERY filter field
                size: $options->size,
                cursor: $page->nextCursor,
                /* ... all other filters ... */
            );
        } while ($page->hasMore());
    }

    /** @throws Throwable */
    public function create(CreateWidgetData $data): Widget
    {
        $response = $this->connector->send(new CreateWidget($this->organization, $this->parentId, $data));
        /** @var array<array-key, mixed> $body */
        $body = $response->json('data');
        return Widget::from($body);
    }
}
```

## Item resource

Methods: `get()`, `update()`, `delete()`, plus action helpers.

```php
final class WidgetResource extends BaseResource
{
    public function __construct(
        Connector $connector,
        private readonly string $organization,
        private readonly int|string $id,
    ) {
        parent::__construct($connector);
    }

    /** @throws Throwable */
    public function get(): Widget {
        $response = $this->connector->send(new GetWidget($this->organization, $this->id));
        /** @var array<array-key, mixed> $data */
        $data = $response->json('data');
        return Widget::from($data);
    }

    /** @throws Throwable */
    public function update(UpdateWidgetData $data): Widget { /* same shape */ }

    /** @throws Throwable */
    public function delete(): void {
        $this->connector->send(new DeleteWidget($this->organization, $this->id));
    }

    /** @throws Throwable */
    public function reboot(): void { $this->sendAction(WidgetAction::Reboot); }

    /** @throws Throwable */
    public function powerCycle(): void { $this->sendAction(WidgetAction::PowerCycle); }

    /** @throws Throwable */
    private function sendAction(WidgetAction $action): void {
        $this->connector->send(new SendWidgetAction($this->organization, $this->id, $action));
    }
}
```

Always `@throws Throwable` (imported via `use Throwable;` — no inline
`\Throwable`). The actual exception is one of the typed subclasses, but
documenting the broad surface is honest given Saloon middleware can
inject anything.

## `ParsesPage` trait

Shared cursor-pagination parser. Lives at `src/Resources/Concerns/ParsesPage.php`.

```php
trait ParsesPage
{
    /** @return Page<T> */
    private function parsePage(Response $response, callable $hydrator): Page
    {
        $data = $response->json('data');
        $meta = $response->json('meta');
        $items = [];
        if (is_array($data)) {
            foreach ($data as $entry) {
                if (is_array($entry)) {
                    $items[] = $hydrator($entry);
                }
            }
        }
        return new Page(
            data: $items,
            nextCursor: /* read from $meta */,
            prevCursor: /* read from $meta */,
            size: /* read from $meta */,
        );
    }
}
```

Hydrator is passed as `Widget::from(...)` (first-class callable syntax)
so the trait stays generic.

## Untestable defensive guards

Don't write `if (! is_array($data)) { throw new RuntimeException(...); }`
in `get()` / `update()` etc. — there's no recordable real API response
that triggers it, so the branch is uncovered AND
`MockResponse::make()` is forbidden by [rules/testing.md](testing.md).

Instead, cast aggressively and trust the API:

```php
/** @var array<array-key, mixed> $data */
$data = $response->json('data');
return Widget::from($data);
```

If `data` is missing or non-array, PHP throws a `TypeError` at the
`Widget::from()` call. Less friendly than a custom message but rarely
triggered.

## Async / empty-body endpoints

Some Forge endpoints (POST `/ssh-keys`, server actions) return 202 with
an empty body. Resource methods for those return `void`, not a DTO:

```php
public function create(CreateSshKeyData $data): void {
    $this->connector->send(new CreateSshKey($this->organization, $this->serverId, $data));
}
```

Callers wanting the just-created resource list afterwards. Document the
behavior in the method docblock and in `docs/FINDINGS.md`.

## Wiring

Once the resource exists, expose it on the parent (connector or parent
resource):

```php
// On the Connector:
public function widgets(): WidgetsResource { return new WidgetsResource($this); }
public function widget(int|string $id): WidgetResource { return new WidgetResource($this, $id); }

// On an item resource (nested):
public function sshKeys(): SshKeysResource {
    return new SshKeysResource($this->connector, $this->organization, $this->id);
}
public function sshKey(int|string $keyId): SshKeyResource {
    return new SshKeyResource($this->connector, $this->organization, $this->id, $keyId);
}
```
