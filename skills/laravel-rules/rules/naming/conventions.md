# Naming Rules

This file owns the *grammar* of names — suffixes, verb-first order,
variable naming. The **class types** being named (Action, Query, Service,
Model, …) are defined in [../../LANGUAGE.md](../../LANGUAGE.md); the rules
below say how to spell them.

## Domain names come from `CONTEXT.md`

`LANGUAGE.md` names the **architecture** (Action, Query, Data object); the
project's `CONTEXT.md` names the **domain** (Signup, Invoice, Vehicle). A
class name is one of each — `CreateSignup` is the `Create` verb + the
`Signup` domain term.

- If the repo has a `CONTEXT.md` / `CONTEXT-MAP.md`, name every domain
  concept with **its** term, and never with a term that glossary lists
  under `_Avoid_`. Read the relevant context before naming
  (`CONTEXT-MAP.md` points at per-context glossaries in multi-context
  repos).
- If the concept you need to name **isn't in the glossary**, that is a
  signal — either you are inventing language the project doesn't use
  (reconsider the name) or there's a real gap. Surface it, and suggest
  `/grill-with-docs` to resolve the term rather than coining it silently.
- If there is **no `CONTEXT.md` at all**, proceed silently — do not nag to
  create one. The glossary is produced by `/grill-with-docs`, not by this
  skill.

## Class Names

- Actions do not use the `Action` suffix.
- Action names start with the verb and then the affected subject or subjects.
- Services use the `Service` suffix.
- Queries use the `Query` suffix.
- Models do not use the `Model` suffix.
- Enums do not use the `Enum` suffix.
- Tests use the `Test` suffix.

Query names should describe the read operation, not just the aggregate. Prefer `ListUsersQuery`, `FindUserByEmailQuery`, or `ListStatisticsObservationsQuery` over broad names like `UserQuery`.

Action names must describe what the action does using a verb-first name. Put the subject or subjects after the verb.

- Orchestrator example: `RegisterOrganization`.
- Single-responsibility example: `CreateOrganization`.
- Single-responsibility example: `AttachUserToOrganization`.
- Avoid noun-only names like `OrganizationRegistration`.
- Avoid vague verbs like `HandleOrganization` or `ProcessUser`.

## Variables And Properties

Name variables and `$this` properties for the value they contain, not for how the value was obtained.

- Good: `$this->createWaitlistSignup = resolve(CreateWaitlistSignup::class);`
- Good: `$waitlistSignup = $this->createWaitlistSignup->handle($data);`
- Avoid: `$service`, `$result`, `$resolved`, `$action`, `$model` when a precise domain name is available.

For return values, use the concrete domain concept returned by the call. For actions named with verbs, the setup property may match the action class, while the handle result should match the returned model or result object.

## Examples

```php
beforeEach(function (): void {
    $this->createWaitlistSignup = resolve(CreateWaitlistSignup::class);
});

$waitlistSignup = $this->createWaitlistSignup->handle($createWaitlistSignupData);
```

Prefer domain-specific names over generic names:

- Use `$waitlistSignup`, not `$model`.
- Use `$indicatorDiscoveryResult`, not `$result`.
- Use `$ineIndicatorDataSource`, not `$service`.
