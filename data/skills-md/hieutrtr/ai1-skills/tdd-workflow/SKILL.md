---
name: tdd-workflow
description: >-
  Test-driven development workflow enforcement for Python and React projects. Use when
  the user requests TDD, test-first development, or red-green-refactor methodology.
  Enforces strict cycle: write ONE failing test -> implement minimum code to pass ->
  refactor while green -> repeat. Applies to both backend (pytest) and frontend (Testing
  Library). Changes agent behavior to write tests before code. Does NOT provide testing
  patterns (use pytest-patterns or react-testing-patterns for how to write tests).
license: MIT
compatibility: 'Python 3.12+, pytest, React 18+, Testing Library, Vitest/Jest'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: testing
allowed-tools: Read Edit Write Bash(pytest:*) Bash(npm:*)
context: fork
---

# TDD Workflow

## When to Use

Activate this skill when:
- The user explicitly requests TDD, test-first, or red-green-refactor
- Implementing new functions, methods, endpoints, or components where test-first is valuable
- Fixing bugs where a regression test should be written first
- The user says "write the test first", "TDD this", or "red-green-refactor"

Do NOT use this skill for:
- Configuration files, environment setup, or static content
- One-line fixes or trivial changes
- Exploratory prototyping or proof-of-concept code
- Code that cannot be meaningfully tested in isolation
- Testing pattern details (use `pytest-patterns` or `react-testing-patterns` for HOW to write tests)

## Instructions

### The TDD Cycle

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   ┌─────┐     ┌───────┐     ┌──────────┐          │
│   │ RED │ ──→ │ GREEN │ ──→ │ REFACTOR │ ──→ ...  │
│   └─────┘     └───────┘     └──────────┘          │
│                                                     │
│   Write ONE    Write MINIMUM   Clean up code        │
│   failing      code to make    while ALL tests      │
│   test         it pass         stay GREEN            │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Phase 1: RED — Write a Failing Test

1. Write exactly ONE test that describes the expected behavior
2. The test must be specific: test one behavior, not multiple
3. Run the test suite and confirm the new test FAILS
4. The failure message should clearly describe what is missing

**Backend (pytest):**
```bash
pytest tests/unit/test_user_service.py::test_create_user_returns_user -x
# Expected: FAILED (function/class does not exist yet)
```

**Frontend (Vitest):**
```bash
npx vitest run src/hooks/useAuth.test.ts --reporter=verbose
# Expected: FAILED (hook/component does not exist yet)
```

**Rules for RED phase:**
- Write the simplest test that expresses the requirement
- The test should fail for the RIGHT reason (missing implementation, not syntax error)
- Don't write more than one failing test at a time
- Import from the location where the code WILL live (even though it doesn't exist yet)

### Phase 2: GREEN — Make It Pass

1. Write the MINIMUM code to make the failing test pass
2. Do NOT add extra functionality, error handling, or edge cases
3. It's okay to hardcode values or use simple implementations
4. Run the test suite and confirm ALL tests pass (not just the new one)

```bash
# Backend
pytest tests/unit/test_user_service.py -x

# Frontend
npx vitest run src/hooks/useAuth.test.ts
```

**Rules for GREEN phase:**
- Minimum code means minimum — if a constant satisfies the test, use a constant
- Do not add code that no test requires
- Do not refactor during this phase
- Do not write additional tests during this phase
- If tests pass, move to REFACTOR

### Phase 3: REFACTOR — Clean Up

1. Improve code quality while keeping all tests green
2. Remove duplication (DRY)
3. Improve naming and readability
4. Extract functions or classes if needed
5. Run tests after EVERY change — they must stay green

```bash
# After each refactoring change
pytest tests/ -x    # Must pass
npx vitest run      # Must pass
```

**Rules for REFACTOR phase:**
- Every change must keep tests green
- Refactor both production code AND test code
- Do NOT add new functionality (that requires a new RED phase)
- If you break a test, undo the refactoring immediately

### Phase 4: COMMIT

After a successful REFACTOR phase:
1. Stage all changes (test + implementation)
2. Commit with a descriptive message
3. Return to Phase 1 (RED) for the next behavior

### Strict TDD Rules

These rules are non-negotiable when this skill is active:

1. **NEVER write production code without a failing test first**
2. **NEVER write more than one failing test at a time**
3. **NEVER add functionality that no test requires**
4. **ALWAYS run tests after every change**
5. **ALWAYS commit after each successful GREEN-REFACTOR cycle**
6. **ALWAYS keep the RED-GREEN-REFACTOR cycle short** (minutes, not hours)

### Backend TDD Flow (pytest)

```
1. Write test:     tests/unit/test_user_service.py::test_create_user_returns_user
2. Run:            pytest tests/unit/test_user_service.py::test_create_user_returns_user -x
3. See:            FAILED - ImportError or AssertionError
4. Implement:      app/services/user_service.py (minimum code)
5. Run:            pytest tests/unit/test_user_service.py -x
6. See:            PASSED
7. Refactor:       Clean up, run tests again
8. Commit:         "Add UserService.create_user"
9. Next test:      test_create_user_rejects_duplicate_email
```

### Frontend TDD Flow (Testing Library)

```
1. Write test:     src/components/UserCard.test.tsx::renders user name
2. Run:            npx vitest run src/components/UserCard.test.tsx
3. See:            FAILED - module not found
4. Implement:      src/components/UserCard.tsx (minimum code)
5. Run:            npx vitest run src/components/UserCard.test.tsx
6. See:            PASSED
7. Refactor:       Clean up, run tests again
8. Commit:         "Add UserCard component"
9. Next test:      calls onEdit when button clicked
```

### Bug Fix TDD Flow

When fixing a bug, always start with a failing test that reproduces the bug:

```
1. Reproduce:      Understand the bug and its trigger condition
2. Write test:     Test that exercises the exact scenario that causes the bug
3. Run:            Confirm FAILED (the test reproduces the bug)
4. Fix:            Implement the minimum fix
5. Run:            Confirm PASSED (bug is fixed)
6. Refactor:       Clean up if needed
7. Commit:         "Fix: [describe the bug]"
```

This guarantees the bug cannot regress — the test will catch it.

## Examples

### TDD: UserService.create_user (3 Cycles)

**Cycle 1 — RED:** Test that create_user returns a user
```python
async def test_create_user_returns_user(db_session):
    service = UserService(db_session)
    user = await service.create_user(UserCreate(email="a@b.com", password="12345678", display_name="A"))
    assert user.email == "a@b.com"
    assert user.id is not None
```
**GREEN:** Implement `UserService.create_user` with basic logic.
**REFACTOR:** Extract password hashing. Commit.

**Cycle 2 — RED:** Test that duplicate email raises error
```python
async def test_create_user_rejects_duplicate_email(db_session):
    service = UserService(db_session)
    await service.create_user(UserCreate(email="a@b.com", password="12345678", display_name="A"))
    with pytest.raises(ConflictError):
        await service.create_user(UserCreate(email="a@b.com", password="87654321", display_name="B"))
```
**GREEN:** Add duplicate check before insert.
**REFACTOR:** Clean up. Commit.

**Cycle 3 — RED:** Test that password is hashed
```python
async def test_create_user_hashes_password(db_session):
    service = UserService(db_session)
    user = await service.create_user(UserCreate(email="a@b.com", password="12345678", display_name="A"))
    assert user.hashed_password != "12345678"
    assert verify_password("12345678", user.hashed_password)
```
**GREEN:** Already passing from cycle 1 refactor? Then this test is a verification, not a RED. Write a test for a NEW behavior instead.

## Edge Cases

- **When to skip TDD:** Configuration files (`.env`, `tsconfig.json`), static content, auto-generated code (Alembic migrations), one-off scripts, and exploratory prototyping.

- **TDD with external dependencies:** Mock at the boundary. If testing a service that calls an external API, mock the API client, not the HTTP library. Test the service's behavior, not the mock.

- **Large features:** Break the feature into small, testable behaviors. Each behavior gets its own RED-GREEN-REFACTOR cycle. The sum of all cycles implements the full feature.

- **Refactoring existing code without tests:** First write tests for the existing behavior (characterization tests). Then refactor with those tests as a safety net. This is not strict TDD but is a valid use of the test-first mindset.

- **Pair with pattern skills:** This skill defines the WORKFLOW (when to write tests vs code). Use `pytest-patterns` or `react-testing-patterns` for the PATTERNS (how to structure tests, which assertions to use).
