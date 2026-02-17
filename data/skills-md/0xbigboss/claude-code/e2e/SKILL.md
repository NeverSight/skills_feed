---
name: e2e
description: Run e2e tests, fix flake and outdated tests, identify bugs against spec. Use when running e2e tests, debugging test failures, or fixing flaky tests. Never changes source code logic or API without spec backing.
---

# E2E Testing

## Principles (Always Active)

These apply whenever working with e2e tests, test failures, or test flakiness:

### Failure Taxonomy

Every e2e failure is exactly one of:

**A. Flaky** (test infrastructure issue)
- Race conditions, timing-dependent assertions
- Stale selectors after UI changes
- Missing waits, incorrect wait targets
- Network timing, mock setup ordering
- Symptom: passes on retry, fails intermittently

**B. Outdated** (test no longer matches implementation)
- Test asserts old behavior that was intentionally changed
- Selectors reference removed/renamed elements
- API contract changed, test wasn't updated
- Symptom: consistent failure, app works correctly

**C. Bug** (implementation doesn't match spec)
- Test correctly asserts spec'd behavior, code is wrong
- **Only classify as bug when a spec exists to validate against**
- If no spec exists, classify as "unverified failure" and report to the user

### Fix Rules by Category

**Flaky fixes:**
- Replace `waitForTimeout` with auto-waiting locators
- Replace brittle CSS selectors with `getByRole`/`getByLabel`/`getByTestId`
- Fix race conditions with `expect()` web-first assertions
- Fix mock/route setup ordering (before navigation)
- **Never add arbitrary delays** - fix the underlying wait
- **Never weaken assertions** to make flaky tests pass
- **Never add retry loops around assertions** - use the framework's built-in retry

**Outdated fixes:**
- Update test assertions to match current (correct) behavior
- Update selectors to match current DOM/API
- **Never change source code** - the implementation is correct, the test is stale

**Bug fixes:**
- Quote the spec section that defines expected behavior
- Fix the source code to match the spec
- **Unit tests MUST exist** before the fix is complete
  - If unit tests exist, run them to confirm
  - If unit tests don't exist, write them first (TDD)
- **Never change e2e assertions** to match buggy code
- **Never change API contracts or interfaces** without spec backing
- If no spec exists, ask the user: bug or outdated test?

### Source Code Boundary

E2e test fixes must not change:
- Application logic or business rules
- API contracts, request/response shapes
- Database schemas or migrations
- Configuration defaults

The only exception: bug fixes where a spec explicitly defines the correct behavior and unit tests cover the fix.

## Workflow (When Explicitly Running E2E)

### Step 1: Discover Test Infrastructure

1. Find e2e config: `playwright.config.ts`, `vitest.config.ts`, or project-specific setup
2. Read `package.json` for the canonical e2e command
3. Check if dev server or Tilt environment is required and running
4. Find spec files: `*.spec.md`, `docs/*.spec.md` - source of truth for bug decisions

### Step 2: Run Tests

Run with minimal reporter to avoid context overflow:

```bash
# Playwright
yarn playwright test --reporter=line

# Or project-specific
yarn test:e2e
```

If a filter is specified, apply it:
```bash
yarn playwright test --reporter=line -g "transfer"
yarn test:e2e -- --grep "transfer"
```

Parse failures into:

| Test | File | Error | Category |
|---|---|---|---|
| `login flow` | `auth.spec.ts:42` | timeout waiting for selector | TBD |

### Step 3: Categorize

For each failure:
1. Read the test file
2. Read the source code it exercises
3. Check for a corresponding spec file
4. Assign category: flaky, outdated, bug, or unverified

### Step 4: Fix by Category

Apply fixes following the Principles above, in order:
1. **Flaky** - fix test infrastructure issues first (unblocks other tests)
2. **Outdated** - update stale assertions
3. **Bug** - fix with spec + unit test gate

### Step 5: Re-run and Report

After all fixes, re-run the suite:

```
## E2E Results

**Run**: `yarn test:e2e` on <date>
**Result**: X/Y passed

### Fixed
- FLAKY: `auth.spec.ts:42` - replaced waitForTimeout with getByRole wait
- OUTDATED: `profile.spec.ts:88` - updated selector after header redesign
- BUG: `transfer.spec.ts:120` - fixed amount validation per SPEC.md#transfers

### Remaining Failures
- UNVERIFIED: `settings.spec.ts:55` - no spec, needs user decision

### Unit Tests Added
- `src/transfer.test.ts` - amount validation edge cases (covers BUG fix)
```
