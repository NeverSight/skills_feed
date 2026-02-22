---
name: tdd
description: "Test-driven development workflow — write failing tests first, implement minimum code, run full suite, commit. Use when implementing features, fixing bugs, or adding test coverage. Includes mock bootstrap phase for projects with mockReset:true."
---

# TDD Implementation Skill

Enforce a strict test-driven development cycle: Red → Green → Refactor → Commit.

## Steps

### 1. Understand the Requirement

Read the task description carefully. Identify:

- **What** behavior needs to exist (inputs, outputs, side effects)
- **Where** it belongs in the codebase (which workspace, which module)
- **Acceptance criteria** (what "done" looks like)

If the requirement is ambiguous, ask the user for clarification before writing any code.

### 2. Find the Right Test File

Locate or create the test file following project conventions:

- **Colocated tests**: `src/foo.ts` → `src/foo.test.ts`
- **Test directory**: `src/routes/bar.ts` → `src/tests/routes/bar.test.ts`
- **Monorepo**: Check each workspace's vitest/jest config for test file patterns

If no test file exists, create one with proper imports and `describe()` block.

### 3. Verify Mock Setup (Bootstrap Phase)

Before writing any tests, validate that your mocks will work correctly:

1. **Check test runner config** for `mockReset`/`mockClear`/`restoreMocks` settings:

```bash
grep -rn 'mockReset\|mockClear\|restoreMocks' vitest.config.* jest.config.*
```

If `mockReset: true` is set, mocks are reset between tests — you MUST reconfigure return values in `beforeEach`, not at module scope.

2. **Write ONE minimal test** that imports the module under test and verifies mocks resolve correctly:

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";

const mocks = vi.hoisted(() => ({
  myDep: vi.fn(),
}));

vi.mock("../path/to/dependency", () => ({
  myDep: (...args: unknown[]) => mocks.myDep(...args),
}));

describe("bootstrap", () => {
  beforeEach(() => {
    mocks.myDep.mockResolvedValue({ ok: true });
  });

  it("mock resolves correctly", async () => {
    const { myDep } = await import("../path/to/dependency");
    expect(await myDep()).toEqual({ ok: true });
  });
});
```

3. **Run it** and confirm it passes:

```bash
npx vitest run <test-file> --reporter=verbose
```

4. **Only then** proceed to write the full test suite following that proven mock pattern.

**Why this matters**: `vi.hoisted()` moves mock declarations above `vi.mock()` hoisting, avoiding temporal dead zone issues. Validating one mock round-trip before writing 20 tests saves significant debugging time.

### 4. Write Failing Tests FIRST (Red Phase)

> Remove the bootstrap test once you've confirmed the mock pattern works.

Write test cases that describe the expected behavior. Include:

- **Happy path**: Normal operation with valid inputs
- **Edge cases**: Empty inputs, boundary values, missing optional fields
- **Error cases**: Invalid inputs, unauthorized access, missing resources

```bash
npx vitest run <test-file> --reporter=verbose
```

**Checkpoint**: All new tests MUST fail. If any pass, the tests are not testing new behavior — revise them.

### 5. Implement Minimum Code (Green Phase)

Write the **minimum** code to make all tests pass. Do NOT:

- Add features not covered by tests
- Optimize prematurely
- Add error handling for untested scenarios
- Refactor existing code (that's the next step)

```bash
npx vitest run <test-file> --reporter=verbose
```

**Checkpoint**: All tests (new and existing) MUST pass.

### 6. Run the FULL Test Suite

Never skip this step:

```bash
npx vitest run --reporter=verbose
```

If any tests outside your file fail:

1. Determine if your change caused the regression
2. If yes → fix it before proceeding
3. If no (pre-existing failure) → note it but continue

### 7. Refactor (Optional)

If the implementation can be cleaner, refactor now while tests are green:

- Extract helpers for repeated logic
- Improve naming
- Simplify conditionals

Re-run the full suite after any refactor.

### 8. Quality Gates

Run lint and type checks on affected workspaces:

```bash
npx eslint <changed-files>
npx tsc --noEmit
```

Fix any issues before committing.

### 9. Commit

Stage only the files you changed and commit:

```
type(scope): description

Co-Authored-By: Claude <noreply@anthropic.com>
```

## Arguments

- `$ARGUMENTS`: Optional description of what to implement via TDD
  - Example: `/tdd add rate limiting to the search endpoint`
  - If empty, ask the user what to implement

## Key Rules

1. **Never write implementation before tests** — this is the whole point of TDD
2. **Never skip step 3** — validate your mock pattern with ONE test before writing 20
3. **Never skip step 6** — the full suite must pass, not just your file
4. **Tests should fail for the RIGHT reason** — a test that fails because of a missing import isn't a valid "red" test
5. **One logical change per cycle** — don't batch multiple features into one TDD cycle
6. **When tests fail after refactor, question the TESTS first** — they may have bad assumptions

## Mock Patterns Reference

### Forwarding Pattern (survives mockReset)

```typescript
const mockFn = vi.fn();
vi.mock("./dep", () => ({
  dep: (...args: unknown[]) => mockFn(...args),
}));
beforeEach(() => {
  mockFn.mockResolvedValue(defaultResult);
});
```

### Counter-Based Sequencing (multi-query operations)

```typescript
let callCount = 0;
mockExecute.mockImplementation(async () => {
  callCount++;
  if (callCount === 1) return insertResult;
  if (callCount === 2) return selectResult;
});
```

### globalThis Registry (TDZ workaround)

```typescript
vi.mock("./dep", () => {
  if (!(globalThis as any).__mocks) (globalThis as any).__mocks = {};
  const m = { dep: vi.fn() };
  (globalThis as any).__mocks.dep = m;
  return { dep: (...a: unknown[]) => m.dep(...a) };
});
// In tests: const mocks = (globalThis as any).__mocks;
```
