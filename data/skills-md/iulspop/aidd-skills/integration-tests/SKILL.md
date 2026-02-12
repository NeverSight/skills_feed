---
name: integration-tests
description: Generates integration tests for server actions, database operations, and API routes using Vitest with the "given/should" prose format. Use when testing infrastructure facades, route actions, session management, or multi-service interactions.
---

# Integration Tests

Act as a top-tier software engineer with serious testing skills.

Write integration tests for: $ARGUMENTS

Each test must answer these 5 questions:

1. What is the unit under test? (test should be in a named describe block)
2. What is the expected behavior? ($given and $should arguments are adequate)
3. What preconditions exist? (database state, authenticated user, form data)
4. What is the expected outcome? (response status, database state, redirects, toasts)
5. How can we find the bug? (implicitly answered if the above questions are answered correctly)

## Rules

- Use Vitest with describe, expect, and test. Test files use the `.spec.ts` extension.
- Tests must use the "given: ..., should: ..." prose format.
- Colocate test files next to the action or model they test.
- Test against the real database — never mock Prisma or database calls.
- Use `onTestFinished` for automatic cleanup: delete created users, organizations, and related data after each test.
- Use infrastructure factories (`*-factories.server.ts`) to create test data with sensible defaults. Override only what the test needs.
- Use `createAuthenticatedRequest` to build requests with auth cookies for route action tests.
- Use context providers (`createAuthTestContextProvider`, `createOrganizationMembershipTestContextProvider`) to satisfy middleware requirements.
- Use `toFormData` to convert objects to FormData for action submissions.
- Use `setupMockServerLifecycle` with MSW handlers for external service mocks (Stripe, Supabase, email).
- Use `server.events.on("response:mocked", listener)` to verify external API calls were made. Clean up listeners with `onTestFinished`.
- Verify database state after mutations using model facade functions from the infrastructure layer.
- Verify redirects: `expect(response.status).toEqual(302)` and `expect(response.headers.get("Location")).toEqual("/path")`.
- Verify toast messages by extracting from `Set-Cookie` header and reading with `getToast`.
- Verify validation errors by checking `response.data.result.error.fieldErrors`.
- Use `test.each` for parametrized validation tests when multiple inputs produce similar error responses.
- Use response helpers (`badRequest`, `forbidden`, `notFound`, `conflict`) to build expected response shapes.
- Create helper functions like `sendAuthenticatedRequest` to reduce boilerplate when testing multiple intents on the same route.
- Group tests by intent when an action handles multiple form intents via `test.describe`.
- Catch thrown `Response` objects for redirect assertions in middleware tests.
- Capture `actual` and `expected` values in variables before asserting with `toEqual`.

## When NOT to use this skill

- For pure function tests (`.test.ts`), use `/unit-tests` instead.
- For React component render tests (`.test.tsx`), use `/happy-dom-tests` instead.
- For browser-level user flow tests (`.e2e.ts`), use `/e2e-tests` instead.
- This skill is for server action, database, and API route tests (`.spec.ts`) only.
