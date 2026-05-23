# Exceptions

> Status: stub — to be deepened (Pass 2). Per-file template.

## Scope

Internals of business exceptions: naming, hierarchy, and throw-vs-return.
*When* an invariant violation is thrown is governed by
[../architecture/invariants.md](../architecture/invariants.md); this
folder owns *how* the exception is shaped.

## TODO (Pass 2)

- Specific business exceptions over generic ones; naming
  (`DuplicateWaitlistSignupException`).
- Base exception/hierarchy per domain; carrying context.
- Throw vs return-null/false (tie to the invariant rule).
- Rendering/handling at the HTTP boundary (cross-ref `http/`).
- Testing thrown exceptions in Pest.

## Checklist

- _(to be written)_
