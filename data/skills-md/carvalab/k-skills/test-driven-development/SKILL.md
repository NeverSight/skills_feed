---
name: test-driven-development
description: TDD workflow guide. Use PROACTIVELY when writing new features or fixing bugs. Enforces Red-Green-Refactor cycle and prevents testing anti-patterns.
tools: Read, Edit, Bash, Grep, Glob
model: opus
---

# Test-Driven Development

Write tests before code. The test is the specification. If you can't write a test, you don't understand the requirement.

## Quick Start

```bash
# 1. Write failing test first
# 2. Run to see it fail (RED)
# 3. Write minimal code to pass (GREEN)
# 4. Refactor while tests pass (REFACTOR)
# 5. Repeat
```

**Test commands by language:**
| Language | Run Tests | Watch Mode |
|----------|-----------|------------|
| Go | `go test ./...` | `go test ./... -v` |
| Node/TS | `npm test` | `npm test -- --watch` |
| Python | `pytest` | `pytest-watch` |
| Java | `./mvnw test` | `./mvnw test -Dtest=*` |

## The Red-Green-Refactor Cycle

### 1. RED: Write Failing Test

```
- Write ONE test for the next piece of behavior
- Test must fail for the RIGHT reason
- Use descriptive names: should_calculate_total_with_tax
- Follow Arrange-Act-Assert structure
```

### 2. GREEN: Make It Pass

```
- Write MINIMAL code to pass the test
- Don't optimize, don't refactor, don't add features
- "Fake it till you make it" is valid
- The goal is GREEN, not perfect
```

### 3. REFACTOR: Improve Design

```
- Clean up code while tests stay green
- Remove duplication
- Improve names
- Extract methods/functions
- Run tests after EVERY change
```

## Common Rationalizations (Resist Them)

| Rationalization | Counter |
|-----------------|---------|
| "Let me just write one more method" | Stop. Test what exists first |
| "I'll add tests after" | You won't. Tests written after verify nothing |
| "It's too simple to test" | Simple now, complex later. Test it |
| "I'll refactor tests later" | Refactor production code, not test structure |
| "This is just scaffolding" | Scaffolding becomes foundation. Test it |

## Anti-Patterns (What NOT to Do)

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| **The Liar** | Test passes but tests nothing | Assert actual behavior |
| **The Mockery** | Over-mocking hides real bugs | Mock boundaries only |
| **Excessive Setup** | 50 lines setup, 2 lines test | Simplify SUT or use builders |
| **The Slow Poke** | Tests take minutes | Isolate, mock I/O |
| **The Local Hero** | Passes locally, fails in CI | No env dependencies |
| **Test-per-Method** | 1:1 test-to-method | Test behaviors, not methods |

## Verification Checklist

Before committing, verify your tests:

```markdown
[ ] Test fails when behavior is removed?
[ ] Test name describes the behavior?
[ ] Arrange-Act-Assert structure clear?
[ ] No test-only code in production?
[ ] Mocks verify behavior, not implementation?
[ ] Edge cases covered?
```

## When TDD Is Mandatory

- New features (write test first)
- Bug fixes (write failing test that reproduces bug)
- Refactoring (tests protect behavior)
- API changes (contract tests first)

## When to Adapt TDD

- Exploratory/spike work (delete code after, then TDD)
- UI prototyping (test logic, not layout)
- Legacy code (add tests before changing)

## Test Naming Convention

```
should_[expected_behavior]_when_[condition]

Examples:
- should_return_zero_when_cart_is_empty
- should_throw_error_when_user_not_found
- should_apply_discount_when_coupon_valid
```

## References

| Reference | Purpose |
|-----------|---------|
| `references/red-green-refactor.md` | Detailed cycle walkthrough |
| `references/anti-patterns.md` | Full anti-pattern catalog |
| `references/examples-go.md` | Go TDD examples |
| `references/examples-node.md` | Node/TypeScript TDD examples |
| `references/examples-python.md` | Python TDD examples |
| `references/examples-java.md` | Java TDD examples |
| `references/verification-checklist.md` | Pre-commit verification |
| `references/testing-boundaries.md` | What to mock, what not to mock |

## Best Practices

1. **One assertion per test** - Multiple assertions hide failures
2. **Test behavior, not implementation** - Tests survive refactoring
3. **Isolated tests** - No shared state between tests
4. **Fast tests** - Under 100ms per unit test
5. **Deterministic** - Same result every run
6. **Self-documenting** - Test name = specification

---

**Principle**: If you can't write a test for it, you don't understand what it should do. The test IS the specification.
