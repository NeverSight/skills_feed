---
name: testing-guide
description: Defines Seagull testing strategy, tradeoffs, and required coverage. Use when adding or updating tests, implementing features that touch backend/frontend, introducing concurrency/locks, or when asked how to structure/run tests in this repo.
---

# Seagull Testing Guide

## Quick start (default approach)

When implementing a feature that touches backend/frontend:

1. **Classify behavior**:
   - **service semantics** (pure rules): put tests near the service
   - **cross-layer behavior** (tRPC + react-query + cache invalidation + timers): use `packages/test-integration`
   - **deployment-shape behavior** (real Postgres + pooling + true concurrency): run strict smoke tests pre-release

2. **Prefer real integrations over hook mocks**:
   - Do **not** mock `useMutation` when the goal is react-query/tRPC integration.
   - Only mock/alias **platform-only deps** (Expo/RN modules that break node/jsdom).

3. **Use header-injected identity for multi-user tests**:
   - Client: set `httpBatchLink({ headers: () => ({ 'x-test-user-id': userId }) })`
   - Server: in `createContext({ headers })`, read `headers.get('x-test-user-id')`

4. **Test DB schema is schema-driven (no hand-written DDL)**:
   - `packages/test-integration/src/db/pglite.ts` applies a generated `packages/test-integration/src/db/schema.sql` (single file)
   - Generate it from current Drizzle schema before running tests:
     - `pnpm -F @acme/test-integration db:schema`
   - `pnpm -F @acme/test-integration test` should run `db:schema` first (so forgetting to regenerate only breaks tests, not production).
   - PGlite compatibility: we polyfill `gen_random_uuid()` used by Drizzle schema/DDL.
   - This prevents schema drift and avoids migration ordering/duplication issues in tests.

## Where tests live

- **Cross-layer**: `packages/test-integration/src/**`
  - in-memory tRPC fetch: `packages/test-integration/src/trpc/inMemoryFetch.ts`
  - PGlite DB harness: `packages/test-integration/src/db/pglite.ts`
  - Test schema SQL (generated): `packages/test-integration/src/db/schema.sql`
  - Generator script: `packages/test-integration/scripts/generate-schema-sql.mjs`
  - example tests:
    - expiry: `packages/test-integration/src/trpc/tripLock.expiry.test.ts`
    - concurrency smoke: `packages/test-integration/src/trpc/tripLock.concurrent.test.ts`
  - Expo business examples:
    - trip/edit: `packages/test-integration/src/expo/trip/edit/**`
    - wishlist: `packages/test-integration/src/expo/wishlist/**`
- **Backend package tests**: `packages/api/src/**/*.test.ts`

## How to run

```bash
pnpm test
pnpm -F @acme/test-integration test
pnpm -F @acme/test-integration typecheck
pnpm -F @acme/api test
pnpm -F @acme/api typecheck
```

## When DB schema changes

After changing `packages/db/src/schema.ts` (or schema modules), regenerate test schema SQL so PGlite tests stay in sync:

```bash
pnpm -F @acme/test-integration db:schema
```

## Test case style rules

- **One behavior per test**: a test name should read like a requirement.
- **Assert the contract**:
  - success payload shape
  - error code (`CONFLICT`, `UNAUTHORIZED`, etc.)
  - cache behavior (invalidate/refetch) where relevant
- **Avoid flakiness**:
  - prefer deterministic triggers over “sleep”
  - if time is essential, isolate it (DB state manipulation or controlled timers)

## FK/seed policy (important after migrations reuse)

- PGlite applies real FK/unique constraints from Drizzle migrations.
- If you insert rows directly, **seed required parents first** (notably `"user"`).
- Prefer seed helpers in `packages/test-integration/src/trpc/api/seed.ts`:
  - `seedUser/seedTrip/seedWishlistJar/...` (helpers ensure required parents exist).
- For router/hook tests that use `createApiTestServer()`, authenticated requests (via header or cookie `x-test-user-id`) will **auto-upsert `"user"`** to keep tests concise.

## Concurrency policy (locks/idempotency)

### Implementation guidance

For lock acquisition, prefer **DB-atomic** statements (e.g. `onConflictDoUpdate + where + returning`) so correctness does not depend on JS scheduling.

### Testing guidance

Use two stages:
- **CI/PR smoke (fast)**: multi-user `Promise.allSettled` concurrency test verifying:
  - exactly one success, rest `CONFLICT`
  - no raw DB errors leak to the client
- **Pre-release strict smoke**: run the same scenario against **real Postgres** to cover pooling/isolation/scheduler differences.

## Definition of Done (mandatory coverage)

When a feature is “done”, tests must cover **all necessary scenarios** (not “at least one test”).

### Backend (packages/api)
- **Service rules**: cover all branches and boundary cases (expiry edges, ownership checks, conflict mapping, empty-return defenses).
- **tRPC route changes**: cover:
  - happy path
  - key failure path(s) with correct error codes/shape
  - at least one invalid input path

### Frontend (Expo business layer)
- **Effects/polling/side effects**: cover:
  - trigger conditions and call counts
  - success and failure behavior (invalidate/refetch, error handling)
  - cleanup (intervals/subscriptions released)

### Cross-layer (default required)
- Any feature that touches backend interaction (query/mutation/errors/cache/timers/concurrency) must add `packages/test-integration` tests covering all necessary scenarios.

## Reference

For the full written guide, see `docs/testing.md`.

