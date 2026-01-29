---
name: writing-tests
description: Write behavior-focused tests following Testing Trophy model with real dependencies, avoiding common anti-patterns like testing mocks and polluting production code. Use when writing new tests, reviewing test quality, or improving test coverage.
---

# Writing Tests

**Core Philosophy:** Test user-observable behavior with real dependencies. Tests should survive refactoring when behavior is unchanged.

**Iron Laws:**

<IMPORTANT>
1. Test real behavior, not mock behavior
2. Never add test-only methods to production code
3. Never mock without understanding dependencies
</IMPORTANT>

## Testing Trophy Model

Write tests in this priority order:

1. **Integration Tests (PRIMARY)** - Multiple units with real dependencies
2. **E2E Tests (SECONDARY)** - Complete workflows across the stack
3. **Unit Tests (RARE)** - Pure functions only (no dependencies)

**Default to integration tests.** Only drop to unit tests for pure utility functions.

## Pre-Test Workflow

BEFORE writing any tests, copy this checklist and track your progress:

```
Test Writing Progress:
- [ ] Step 1: Review project standards (check existing tests)
- [ ] Step 2: Understand behavior (what should it do? what can fail?)
- [ ] Step 3: Choose test type (Integration/E2E/Unit)
- [ ] Step 4: Identify dependencies (real vs mocked)
- [ ] Step 5: Write failing test first (TDD)
- [ ] Step 6: Implement minimal code to pass
- [ ] Step 7: Verify coverage (happy path, errors, edge cases)
```

**Before writing any tests:**

1. **Review project standards** - Check existing test files, testing docs, or project conventions
2. **Understand behavior** - What should this do? What can go wrong?
3. **Choose test type** - Integration (default), E2E (critical workflows), or Unit (pure functions)
4. **Identify dependencies** - What needs to be real vs mocked?

## Test Type Decision

```
Is this a complete user workflow?
  → YES: E2E test

Is this a pure function (no side effects/dependencies)?
  → YES: Unit test

Everything else:
  → Integration test (with real dependencies)
```

## Mocking Guidelines

**Default: Don't mock. Use real dependencies.**

### Only Mock These

- External HTTP/API calls
- Time-dependent operations (timers, dates)
- Randomness (random numbers, UUIDs)
- File system I/O
- Third-party services (payments, analytics, email)
- Network boundaries

### Never Mock These

- Internal modules/packages
- Database queries (use test database)
- Business logic
- Data transformations
- Your own code calling your own code

**Why:** Mocking internal dependencies creates brittle tests that break during refactoring.

### Before Mocking, Ask:

1. "What side effects does this method have?"
2. "Does my test depend on those side effects?"
3. If yes → Mock at lower level (the slow/external operation, not the method test needs)
4. Unsure? → Run with real implementation first, observe what's needed, THEN add minimal mocking

### Mock Red Flags

- "I'll mock this to be safe"
- "This might be slow, better mock it"
- Can't explain why mock is needed
- Mock setup longer than test logic
- Test fails when removing mock

## Integration Test Pattern

```
describe("Feature Name", () => {
  setup(initialState)

  test("should produce expected output when action is performed", () => {
    // Arrange: Set up preconditions
    // Act: Perform the action being tested
    // Assert: Verify observable output
  })
})
```

**Key principles:**

- Use real state/data, not mocks
- Assert on outputs users/callers can observe
- Test the behavior, not the implementation

For language-specific patterns, see the Language-Specific Patterns section.

## Async Waiting Patterns

When tests involve async operations, avoid arbitrary timeouts:

```
// BAD: Guessing at timing
sleep(500)
assert result == expected

// GOOD: Wait for the actual condition
wait_for(lambda: result == expected)
```

**When to use condition-based waiting:**

- Tests use `sleep`, `setTimeout`, or arbitrary delays
- Tests are flaky (pass locally, fail in CI)
- Tests timeout when run in parallel
- Waiting for async operations to complete

**Delegate to skill:** When you encounter these patterns, invoke `Skill(ce:condition-based-waiting)` for detailed guidance on implementing proper condition polling and fixing flaky tests.

## Assertion Strategy

**Principle:** Assert on observable outputs, not internal state.

| Context | Assert On                                             | Avoid                                 |
| ------- | ----------------------------------------------------- | ------------------------------------- |
| UI      | Visible text, accessibility roles, user-visible state | CSS classes, internal state, test IDs |
| API     | Response body, status code, headers                   | Internal DB state directly            |
| CLI     | stdout/stderr, exit code                              | Internal variables                    |
| Library | Return values, documented side effects                | Private methods, internal state       |

**Why:** Tests that assert on implementation details break when you refactor, even if behavior is unchanged.

## Test Data Management

**Use source constants and fixtures, not hard-coded values:**

```
// Good - References actual constant or fixture
expected_message = APP_MESSAGES.SUCCESS
assert response.message == expected_message

// Bad - Hard-coded, breaks when copy changes
assert response.message == "Action completed successfully!"
```

**Why:** When product copy changes, you want one place to update, not every test file.

## Anti-Patterns to Avoid

### Testing Mock Behavior

```
// BAD: Testing that the mock was called, not real behavior
mock_service.assert_called_once()

// GOOD: Test the actual outcome
assert user.is_active == True
assert len(sent_emails) == 1
```

**Gate:** Before asserting on mock calls, ask "Am I testing real behavior or mock interactions?" If testing mocks → Stop, test the actual outcome instead.

### Test-Only Methods in Production

```
// BAD: destroy() only used in tests - pollutes production code
class Session:
    def destroy(self):  # Only exists for test cleanup
        ...

// GOOD: Test utilities handle cleanup
# In test_utils.py
def cleanup_session(session):
    # Access internals here, not in production code
    ...
```

**Gate:** Before adding methods to production code, ask "Is this only for tests?" Yes → Put in test utilities.

### Mocking Without Understanding

```
// BAD: Mock prevents side effect test actually needs
mock(database.save)  # Now duplicate detection won't work!

add_item(item)
add_item(item)  # Should fail as duplicate, but won't

// GOOD: Mock at correct level
mock(external_api.validate)  # Mock slow external call only

add_item(item)  # DB save works, duplicate detected
add_item(item)  # Fails correctly
```

### Incomplete Mocks

```
// BAD: Partial mock - missing fields downstream code needs
mock_response = {
    status: "success",
    data: {...}
    // Missing: metadata.request_id that downstream code uses
}

// GOOD: Mirror real API completely
mock_response = {
    status: "success",
    data: {...},
    metadata: {request_id: "...", timestamp: ...}
}
```

**Gate:** Before creating mocks, check "What does the real thing return?" Include ALL fields.

## TDD Prevents Anti-Patterns

1. **Write test first** → Think about what you're testing (not mocks)
2. **Watch it fail** → Confirms test tests real behavior
3. **Minimal implementation** → No test-only methods creep in
4. **Real dependencies first** → See what test needs before mocking

**If testing mock behavior, you violated TDD** - you added mocks without watching test fail against real code.

## Language-Specific Patterns

For detailed framework and language-specific patterns:

- **JavaScript/React**: See `references/javascript-react.md` for React Testing Library queries, Jest/Vitest setup, Playwright E2E, and component testing patterns
- **Python**: See `references/python.md` for pytest fixtures, polyfactory, respx mocking, testcontainers, and FastAPI testing
- **Go**: See `references/go.md` for table-driven tests, testify/go-cmp assertions, testcontainers-go, and interface fakes

## Quality Checklist

Before completing tests, verify:

- [ ] Happy path covered
- [ ] Error conditions handled
- [ ] Edge cases considered
- [ ] Real dependencies used (minimal mocking)
- [ ] Async waiting uses conditions, not arbitrary timeouts
- [ ] Tests survive refactoring (no implementation details)
- [ ] No test-only methods added to production code
- [ ] No assertions on mock existence or call counts
- [ ] Test names describe behavior, not implementation

## What NOT to Test

- Internal state
- Private methods
- Function call counts
- Implementation details
- Mock existence
- Framework internals

**Test behavior users/callers observe, not code structure.**

## Quick Reference

| Test Type   | When                    | Dependencies                 |
| ----------- | ----------------------- | ---------------------------- |
| Integration | Default choice          | Real (test DB, real modules) |
| E2E         | Critical user workflows | Real (full stack)            |
| Unit        | Pure functions only     | None                         |

| Anti-Pattern                    | Fix                                     |
| ------------------------------- | --------------------------------------- |
| Testing mock existence          | Test actual outcome instead             |
| Test-only methods in production | Move to test utilities                  |
| Mocking without understanding   | Understand dependencies, mock minimally |
| Incomplete mocks                | Mirror real API completely              |
| Tests as afterthought           | TDD - write tests first                 |
| Arbitrary timeouts/sleeps       | Use condition-based waiting             |

<IMPORTANT>
**Remember:** Behavior over implementation. Real over mocked. Outputs over internals.
</IMPORTANT>
