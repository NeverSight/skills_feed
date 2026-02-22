---
name: write-tests
description: >-
  Add test coverage to existing code with correct mock patterns. Use when adding
  tests to untested modules, writing regression tests for bugs, or user asks to
  test a specific file. Handles mockReset:true, vi.hoisted(), forwarding
  pattern, and test app builder utilities.
---

# Write Tests for Existing Code

## Before Writing, Ask Yourself

- **Module type?** Route handler, repository, plugin, utility, or service — each has a different mock strategy
- **Blast radius?** Does this module have side effects (DB writes, API calls) that need isolation?
- **Nearest test file?** Find the closest `*.test.ts` and match its structure exactly

## Mock Strategy by Module Type

| Module Type      | Strategy                                               |
| ---------------- | ------------------------------------------------------ |
| Route handler    | Test app builder + session simulation + `app.inject()` |
| Repository       | Mock DB connection + counter-based `execute`           |
| Framework plugin | Real framework instance + selective dependency mocks   |
| Pure utility     | No mocks — test inputs/outputs directly                |
| Service w/ DI    | Mock injected deps via forwarding pattern              |

## Mock Setup (mockReset: true)

If your test runner uses `mockReset: true`, most examples from the internet will **silently fail**.

```typescript
const { mockFn } = vi.hoisted(() => ({
  mockFn: vi.fn(),
}));

vi.mock("./dependency", () => ({
  dependency: (...args: unknown[]) => mockFn(...args),
}));

beforeEach(() => {
  // MUST reconfigure here — mockReset clears return values between tests
  mockFn.mockResolvedValue(defaultResult);
});
```

For complex TDZ cases (multiple interdependent mocks), use the **globalThis registry pattern**.

## NEVER

- **NEVER chain `mockResolvedValueOnce`** — `mockReset` clears the chain between tests. Use counter-based `mockImplementation` instead.
- **NEVER define mock variables at module scope then reference in `vi.mock()` factories** — hoisting creates a temporal dead zone. Use `vi.hoisted()` or globalThis.
- **NEVER `vi.importActual()` for modules with side effects** — use selective re-exports.
- **NEVER test implementation details** (private state, internal call order) — test behavior through the public API.
- **NEVER copy mock patterns from other projects** — check YOUR test runner config first.
- **NEVER modify source code** — this skill writes tests only.

## Metacognitive Rule

**If >3 tests fail on first run**: STOP. The root cause is almost certainly a mock wiring issue affecting all tests, not individual test logic errors. Re-examine the mock setup strategy holistically before fixing tests one by one.

## Run

```bash
npx vitest run <test-file> --reporter=verbose
```

## Arguments

- `$ARGUMENTS`: Path to the source file or module to cover
  - Example: `/write-tests src/routes/admin/settings.ts`
  - If empty, ask the user which file needs test coverage
