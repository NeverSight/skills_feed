---
name: controller-testing
description: "Writes Pest feature tests for Laravel HTTP controllers with repeatable patterns for web/session and API/JSON flows. Activates for controller-focused feature tests (especially under tests/Feature/Http/Controllers/**), CRUD action matrices, nested route binding checks, authorization outcomes (403 vs 404), validation datasets, and persistence assertions."
license: MIT
metadata:
  author: Hosmel Quintana
---

# Controller Testing

## When to Apply

Activate this skill when the task is about **Laravel controller feature tests** and includes signals like:

- Paths such as `tests/Feature/Http/Controllers/**` (including `tests/Feature/Http/Controllers/Api/**`).
- Pest action blocks like `describe('create' | 'destroy' | 'edit' | 'index' | 'show' | 'store' | 'update')`.
- Controller route assertions using `route(...)`, nested parameters, and route-model binding scope checks.
- Auth/authorization outcomes and controller transport assertions:
  - web/session (`get`, `post`, `patch`, `delete`, `assertInertia`, redirects), or
  - API/JSON (`getJson`, `postJson`, `patchJson`, `deleteJson`, JSON assertions).

Do **not** use this skill for model/unit tests, service-layer tests, console commands, or non-HTTP behavior.

## Quick Start

```bash
# Create file only when needed
php artisan make:test --pest Http/Controllers/<Name>ControllerTest --no-interaction

# Run only the affected file
php artisan test --compact tests/Feature/Http/Controllers/<Name>ControllerTest.php

# Optional focused rerun
php artisan test --compact --filter="<test name>"
```

## Decision Workflow

1. Inspect sibling controller tests first to match naming, helpers, and transport style.
2. Choose transport mode: web/session or API/JSON.
3. Determine route shape (flat vs nested) and parameter keys.
4. For each action under test, apply this baseline in order (as applicable):
   - requires authentication
   - policy denial (`403`)
   - binding mismatch (`404`)
   - validation datasets (`store`/`update`)
   - success response + persistence assertions
5. Load only the reference files needed for the action/rule pattern.

## Canonical `403` vs `404` Rule

Use this as the source of truth:

- If route bindings resolve correctly and authorization denies access, assert `assertForbidden()` (`403`).
- If route-model binding fails (wrong parent/child chain, scoped binding mismatch), assert `assertNotFound()` (`404`).

Actor context to keep outcomes deterministic:

- `403` tests: authenticate an **in-scope actor** that can resolve bindings but lacks permission.
- Validation and success-path tests: authenticate an **authorized in-scope actor**.
- `404` binding-mismatch tests: any authenticated actor is acceptable because binding fails first.

## Reference Map

Load only what you need:

- API/JSON adaptation guide and full examples:
  - `references/modes/api-json.md`
- Nested route naming and parameter composition:
  - `references/route-patterns.md`
- Per-action templates (web/session-first):
  - `references/actions/create.md`
  - `references/actions/destroy.md`
  - `references/actions/edit.md`
  - `references/actions/index.md`
  - `references/actions/show.md`
  - `references/actions/store.md`
  - `references/actions/update.md`
- Validation catalogs (merge only required rules):
  - `references/validation/store-validates-fields.md`
  - `references/validation/update-validates-fields.md`
- Focused validation patterns (prefer first when matching rules exist):
  - `references/validation/required-with-and-array.md`
  - `references/validation/scoped-exists-and-unique.md`
  - `references/validation/prepare-for-validation.md`
  - `references/validation/api-login-validation.md`

Action references are web/session-first templates. For API/JSON controllers, keep the same action structure and adapt assertions with `references/modes/api-json.md` plus sibling API tests.

## Baseline Assertions by Transport

Web/session mode:

- `requires authentication` -> redirect to login route.
- Validation failures -> `assertRedirectBackWithErrors(...)`.
- Page actions -> `assertOk()` + `assertInertia(...)`.
- Mutation actions -> redirect + persistence assertions.
- Toast/flash assertions are optional and app-specific.

API/JSON mode:

- Protected endpoints: `requires authentication` -> `assertUnauthorized()`.
- Public endpoints: skip auth-required test unless the endpoint is protected.
- Validation failures -> `assertUnprocessable()` + `assertJsonValidationErrors(...)`.
- Success actions -> `assertOk()` / `assertCreated()` / `assertNoContent()` + JSON + persistence assertions.
- Prefer asserting validation keys for stability; assert full messages when project conventions expect them.

## Notes

- One-level, two-level, and three-level examples are patterns, not limits.
- For `destroy`, choose persistence assertions by model behavior:
  - `assertSoftDeleted(...)` for soft-deleting models.
  - `assertModelMissing(...)` otherwise.
- Use the app's identifier shape in assertions (`id`, `public_id`, slug, route key).
