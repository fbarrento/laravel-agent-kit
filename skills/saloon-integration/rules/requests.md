# Requests

Saloon `Request` subclasses, one per endpoint. They own the HTTP method,
URL composition, and (for write methods) the JSON body. They DON'T
hydrate responses — that's the resource layer's job.

## GET requests (no body)

```php
final class GetWidget extends Request
{
    protected Method $method = Method::GET;

    public function __construct(
        private readonly string $organization,
        private readonly int|string $id,
    ) {}

    #[Override]
    public function resolveEndpoint(): string
    {
        return sprintf('/orgs/%s/widgets/%s', $this->organization, $this->id);
    }
}
```

## GET with query params (paginated list)

Take an optional `List<X>Options` DTO; emit via `defaultQuery()`.

```php
final class GetWidgets extends Request
{
    protected Method $method = Method::GET;

    public function __construct(
        private readonly string $organization,
        private readonly ?ListWidgetsOptions $options = null,
    ) {}

    #[Override]
    public function resolveEndpoint(): string
    {
        return sprintf('/orgs/%s/widgets', $this->organization);
    }

    /** @return array<string, int|string> */
    #[Override]
    protected function defaultQuery(): array
    {
        return $this->options?->toQuery() ?? [];
    }
}
```

## POST / PUT with JSON body

`implements HasBody` + `use HasJsonBody` trait + `defaultBody()` method.

**`defaultBody()` does NOT get `#[Override]`** — `HasJsonBody` is a
trait, not a parent class, and the trait doesn't declare `defaultBody()`
as an abstract method. Adding `#[Override]` throws a fatal at class load
time.

```php
final class CreateWidget extends Request implements HasBody
{
    use HasJsonBody;

    protected Method $method = Method::POST;

    public function __construct(
        private readonly string $organization,
        private readonly CreateWidgetData $data,
    ) {}

    #[Override]
    public function resolveEndpoint(): string
    {
        return sprintf('/orgs/%s/widgets', $this->organization);
    }

    /** @return array<string, mixed> */
    protected function defaultBody(): array       // <-- NO #[Override] here
    {
        return $this->data->toArray();
    }
}
```

PUT is the same shape with `Method::PUT` + the resource id in the path
+ an `UpdateWidgetData` input DTO.

## DELETE

```php
final class DeleteWidget extends Request
{
    protected Method $method = Method::DELETE;

    public function __construct(
        private readonly string $organization,
        private readonly int|string $id,
    ) {}

    #[Override]
    public function resolveEndpoint(): string
    {
        return sprintf('/orgs/%s/widgets/%s', $this->organization, $this->id);
    }
}
```

## Action endpoints (`POST /resource/{id}/actions`)

Body is `{ "action": "reboot" }`. Take an enum for the action.

```php
final class SendWidgetAction extends Request implements HasBody
{
    use HasJsonBody;

    protected Method $method = Method::POST;

    public function __construct(
        private readonly string $organization,
        private readonly int|string $id,
        private readonly WidgetAction $action,
    ) {}

    #[Override]
    public function resolveEndpoint(): string
    {
        return sprintf('/orgs/%s/widgets/%s/actions', $this->organization, $this->id);
    }

    /** @return array{action: string} */
    protected function defaultBody(): array
    {
        return ['action' => $this->action->value];
    }
}
```

## File layout

Under `src/Requests/<Domain>/` matching the resource. Server-scoped
endpoints (including nested ones like `/servers/{id}/ssh-keys`) stay
flat under `src/Requests/Servers/`:

```
src/Requests/Servers/
├── GetServers.php
├── GetServer.php
├── CreateServer.php
├── UpdateServer.php
├── DeleteServer.php
├── SendServerAction.php
├── GetSshKeys.php          # nested under /servers/{id}/ssh-keys
├── GetSshKey.php
├── CreateSshKey.php
└── DeleteSshKey.php
```

The class name disambiguates the operation; the folder marks the
domain. Don't add another nesting level for sub-resources.

## Path-param typing

URL path parameters that are ids should be typed `int|string`. The
upstream API may accept either (numeric server ids vs string slugs);
let callers pass what they have.

```php
public function __construct(
    private readonly string $organization,  // slugs are always strings
    private readonly int|string $serverId,  // numeric id OR slug — accept both
) {}
```

## Imports

Always FQCN via `use` imports — no inline `\Foo\Bar` references. Each
test file gets explicit namespaces. Tests typing `@throws Throwable`
must `use Throwable;` at the top, not `@throws \Throwable`.
