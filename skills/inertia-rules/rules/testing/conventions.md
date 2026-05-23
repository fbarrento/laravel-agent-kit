# Frontend testing

Three test levels, each proving a different thing. The trap is testing the
wrong thing at the wrong level — a routed flow mocked into a component
test, or a pure helper exercised through a browser. Match the test to what
it proves. (For *when* to run these as a pre-handoff gate, see
[../verification/conventions.md](../verification/conventions.md); this file
is *how to write* them.)

| Level | Tool | Proves |
|---|---|---|
| Story interaction | Storybook play functions (`@storybook/test`) | a component's states/variants/interactions in isolation |
| Route / flow | **Pest Browser** (preferred) or Playwright | the real Inertia page: prop delivery, form submit, validation, auth, navigation |
| Unit | Vitest | pure `lib/` helpers and view-model logic |

## Rule: test rendered behavior, not implementation

Assert what the user sees and can do — rendered text, enabled/disabled
controls, what appears after an interaction — not internal state,
component names, or hook call counts.

**Why:** behavior tests survive refactors (rename a hook, restructure JSX —
the test still holds); implementation tests break on every refactor and
pass while the UI is broken. Same philosophy as the backend
(`laravel-rules` testing).

## Rule: component states are story interaction tests, not route tests

A reusable component's contract — variants, `Empty`/`Loading`/`Error`,
disabled, validation display — is proven by its story (and a `play`
function for interactions), using typed fixtures
([../stories/conventions.md](../stories/conventions.md)). Don't spin up a
Laravel route to test a component's empty state.

```tsx
export const WithValidationErrors: Story = {
  args: { errors: { name: 'The name field is required.' } },
  play: async ({ canvas }) => {
    await expect(canvas.getByText('The name field is required.')).toBeVisible()
  },
}
```

**Why:** the component doesn't need the backend to render its states — its
inputs are props. Driving it from a route is slow, flaky, and tests the
route too. The story isolates the component contract.

## Rule: routed behavior is a Pest Browser test against the real route

Inertia page rendering, prop delivery, form submission → server validation
→ redirect, authorization, and navigation are proven end-to-end with
Pest's browser testing against the real Laravel route — not mocked.

```php
it('shows validation errors when creating a vehicle', function () {
    $this->actingAs(User::factory()->create());
    $page = visit('/vehicles/create');
    $page->click('Save')
        ->assertSee('The name field is required.')
        ->assertNoJavascriptErrors();
});
```

**Why:** these behaviors *are* the Laravel↔Inertia integration — only a
real request proves the controller sends the right props and validation
flows back. A Storybook pass proves the component, never the route (see
[../verification/conventions.md](../verification/conventions.md)).

## Rule: unit-test pure logic in `lib/`, not components

Framework-free helpers and view-model computation live in `lib/` (or a
feature-local pure module) and are unit-tested directly with Vitest. If
something is hard to unit-test because it's tangled with a component,
that's a signal to extract the pure part to `lib/`.

## Rule: fixtures and doubles are typed; don't mock Inertia internals

Test data uses the same typed fixtures as stories (generated/feature
types). Don't mock `usePage`, the router, or Inertia internals to fake a
page — drive components by props, and drive routes through Pest Browser.

**Why:** mocking Inertia internals tests your mock, not Inertia. Props in
(component) or a real visit (route) are the honest seams; a typed fixture
fails to compile when the backend contract changes.

## Checklist

- Tests assert rendered behavior, not implementation details.
- Component states/interactions → story `play` tests with typed fixtures.
- Routed behavior (props, form submit, validation, auth, nav) → Pest
  Browser against the real route.
- Pure helpers/view-model logic → Vitest unit tests; extract to `lib/` if
  hard to test through a component.
- Fixtures/types are generated-backed; Inertia internals not mocked.
