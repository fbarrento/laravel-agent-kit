# Boost boundary & the agent loop

Laravel **Boost** is the generic Laravel agent substrate. This skill is
the Inertia/frontend discipline layer on top. Knowing which side owns
what stops you from guessing Laravel facts and stops this skill from
duplicating Boost.

## Rule: use Boost for live Laravel facts; never guess them

When you need a fact about the running app, ask Boost rather than
inferring it from source. Use Boost for:

- Laravel/package versions and app info;
- routes and absolute URLs;
- database schema and safe read queries;
- logs, last error, browser logs;
- Laravel / Inertia / Tailwind / Pest documentation search.

**Why:** these are runtime truths that drift from the source you can see.
Guessing a route name, a column, or a package version produces code that
typechecks and still breaks. Boost reads the actual app.

## Rule: use this skill for Inertia/frontend discipline

This skill (not Boost) owns:

- the frontend role graph and page/resource conventions;
- generated backend-derived type ownership;
- backend-owned formatting/translation rules;
- the design-system token and component contract;
- story contracts and typed fixtures;
- verification, feedback, and handoff evidence discipline.

Do not expect Boost to enforce any of these — they are conventions you
apply by hand.

## The required agent loop

For any task that changes Inertia UI:

1. **Establish context.** Use Boost for versions, routes, schema, logs,
   and docs you need.
2. **Identify the surface.** Find the route, controller/action, page
   component, props, validation contract, and redirect/flash behavior.
   Confirm the backend contract exists (generated types via Spatie Data;
   routes/actions via Wayfinder). If it doesn't, that's a backend task
   first — do not handwrite the shapes (see
   [../types/generated.md](../types/generated.md)).
3. **Make the smallest coherent change** inside the app-owned surface,
   respecting the role graph ([roles.md](roles.md)).
4. **Verify the flow.** Run the [verification](../verification/conventions.md)
   checklist: typecheck/lint, the [audit](../audit/conventions.md)
   self-check, Storybook for reusable UI, Pest Browser / Playwright for
   route-visible changes; inspect screenshot + console.
5. **Report with evidence.** Assemble the [handoff](../handoff/conventions.md):
   changed files by role, checks run, blockers, remaining risk, and any
   unresolved [feedback](../feedback/conventions.md).

**Why:** the loop front-loads the two things agents skip — confirming the
backend contract before writing UI, and inspecting the rendered outcome
before claiming done. Skipping from route discovery straight to edits is
how you get a page that compiles against an invented prop shape and was
never opened in a browser.

## Checklist

- Live Laravel facts came from Boost, not inference.
- The backend contract (generated types + Wayfinder routes) was confirmed
  to exist before frontend code was written.
- The change stayed inside the app-owned frontend surface and the role
  graph.
- The flow was verified with the rendered outcome inspected, not just
  typechecked.
- The handoff reports changed files, checks, blockers, and risk.
