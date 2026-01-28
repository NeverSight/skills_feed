---
name: code-review
description: Comprehensive code review covering functionality, testing, QA, and AGENTS.md compliance. Triggers on "review code", "code review", "review this", "check my code". Validates correctness, test coverage, test quality, and guideline adherence.
---

# Code Review Skill

Reviews code through battle-tested engineering principles with comprehensive quality gates.

## Usage

Tell me what to review:
- "Review `src/auth.ts`"
- "Review the changes in `git diff HEAD~3`"
- "Review this PR for merge readiness"

## Review Process

1. **Read the code** — Understand what it does
2. **Verify functionality** — Check for bugs, edge cases, correctness
3. **Assess test coverage** — Ensure changed code has adequate tests
4. **Evaluate test quality** — Check tests follow best practices (not flaky)
5. **Check guideline compliance** — Verify AGENTS.md/CLAUDE.md adherence
6. **Apply philosophy lenses** — Check against engineering principles
7. **Run QA checks** — Execute lint, typecheck, tests (after fixes)
8. **Output structured findings** — Categorized, actionable feedback

---

## 1. Functionality Verification

### Correctness Checklist
- Does the code do what it's supposed to do?
- Are all requirements/acceptance criteria met?
- Are edge cases handled? (null, empty, boundary values, overflow)
- Are error conditions handled gracefully?
- Is the happy path tested AND working?
- Are race conditions possible? (async, concurrent access)
- Is state managed correctly? (no stale data, proper initialization)

### Bug Detection Signals
| Signal | Question |
|--------|----------|
| **Off-by-one** | Loop bounds, array indices, comparisons (< vs <=) |
| **Null/undefined** | Can any value be null when accessed? |
| **Type coercion** | Implicit conversions causing bugs? (JS: `"5" + 3`) |
| **Resource leaks** | Files, connections, memory properly closed? |
| **Infinite loops** | Can loop conditions fail to terminate? |
| **Integer overflow** | Large numbers handled safely? |
| **Security holes** | SQL injection, XSS, path traversal, secrets exposed? |

---

## 2. Test Coverage Assessment

### Coverage Requirements
- **New code**: Must have tests covering primary functionality
- **Bug fixes**: Must have regression test proving fix
- **Changed code**: Tests should cover modified behavior
- **Critical paths**: Auth, payments, data mutations require high coverage

### Coverage Analysis
```
Is the changed code tested? → NO → Block: Add tests
     ↓ YES
Are edge cases covered? → NO → Request edge case tests
     ↓ YES
Are error paths tested? → NO → Request error handling tests
     ↓ YES
Coverage adequate ✓
```

### Google's Coverage Guidelines
- **60%**: Acceptable minimum
- **75%**: Commendable
- **90%**: Exemplary
- **Per-commit**: 90%+ for changed lines is reasonable

> Focus on what's NOT covered rather than hitting arbitrary numbers.

---

## 3. Test Quality (Non-Flaky Tests)

### FIRST Principles for Good Tests
| Principle | Meaning |
|-----------|---------|
| **Fast** | Run quickly (milliseconds for unit tests) |
| **Isolated** | No dependencies on other tests or external state |
| **Repeatable** | Same result every time, any environment |
| **Self-validating** | Pass or fail, no manual interpretation |
| **Timely** | Written close to the code (ideally before - TDD) |

### Flaky Test Detection
Tests are flaky if they fail intermittently without code changes.

**Common Causes:**
- Time/date dependencies (use fixed/mocked time)
- Random data without seed control
- Shared mutable state between tests
- Network/external service calls
- Race conditions in async code
- File system dependencies
- Database state leakage
- Order-dependent tests

### Test Quality Checklist
- [ ] Tests are deterministic (same input → same output)
- [ ] Tests clean up after themselves (no side effects)
- [ ] Tests don't depend on execution order
- [ ] Async operations properly awaited
- [ ] External dependencies mocked/stubbed
- [ ] Time-sensitive tests use controlled time
- [ ] Random values use seeded generators
- [ ] Tests have meaningful assertions (not just `expect(true)`)
- [ ] Test names describe behavior being tested
- [ ] One logical assertion per test

### Red Flags in Tests
- `sleep()` or arbitrary delays
- Commented-out assertions
- Empty catch blocks swallowing failures
- Tests that pass when logic is deleted (useless tests)
- `expect(result).toBeDefined()` without checking value
- Shared state between `it()` blocks
- Network calls without mocking

---

## 4. QA Checks

### Before Approving, Verify:
1. **Lint passes**: `npm run lint`, `eslint`, etc.
2. **Types check**: `tsc --noEmit`, `npm run typecheck`, etc.
3. **Tests pass**: `npm test`, `pytest`, etc.
4. **Build succeeds**: `npm run build`, `cargo build`, etc.

### Automated QA Flow
```
Run lint → FAIL → Must fix before merge
    ↓ PASS
Run typecheck → FAIL → Must fix before merge
    ↓ PASS
Run tests → FAIL → Must fix (unless pre-existing)
    ↓ PASS
Build → FAIL → Must fix before merge
    ↓ PASS
QA Passed ✓
```

---

## 5. Guidelines Compliance

### AGENTS.md / CLAUDE.md Adherence
Check if the codebase has guidance files:
- `AGENTS.md` or `CLAUDE.md` in root or relevant directories
- Project-specific coding standards
- Architecture decisions and patterns

### Compliance Checklist
- [ ] Follows documented code style
- [ ] Uses approved libraries/patterns
- [ ] Adheres to naming conventions
- [ ] Follows directory structure guidelines
- [ ] Respects forbidden patterns (if documented)
- [ ] Matches documented architectural decisions

---

## 6. Engineering Philosophy Lenses

### Grug Brain Check (Complexity Demon Detection)
- Is this the simplest solution?
- Could a newcomer understand it in 30 seconds?
- Are there unnecessary abstractions?

### Code Smell Detection
| Smell | Question |
|-------|----------|
| **Long Method** | >50 lines? One sentence description? |
| **Long Params** | >3 parameters? Group them? |
| **Feature Envy** | Uses another class more than its own? |
| **Shotgun Surgery** | One change = many file edits? |
| **Dead Code** | Unreachable or unused? |

### Unix Philosophy Check
- Does each function do ONE thing well?
- Can components be tested in isolation?
- Are there side effects in "pure" functions?

### DRY/KISS
- Is logic duplicated?
- Is there a simpler solution?

---

## Output Format

```markdown
## Summary
[One-line verdict: APPROVE / NEEDS WORK / RETHINK]

## QA Status
- Lint: ✓/✗
- Typecheck: ✓/✗
- Tests: ✓/✗ (X passed, Y failed)
- Build: ✓/✗

## Functionality Issues
[Bugs, incorrect behavior, edge cases]

## Test Coverage Gaps
[Untested code paths, missing tests]

## Test Quality Issues
[Flaky tests, bad patterns]

## Guidelines Violations
[AGENTS.md/CLAUDE.md non-compliance]

## Code Quality
[Design issues, maintainability]

## Nitpicks
[Minor suggestions]

## What's Good
[Acknowledge solid work]
```

## Severity Levels

| Level | Meaning | Action |
|-------|---------|--------|
| 🔴 Critical | Bugs, security, data loss, broken tests | Block merge |
| 🟠 Important | Missing tests, design issues | Should fix |
| 🟡 Suggestion | Could be better | Consider |
| 🟢 Nitpick | Style, minor preference | Optional |

## Master Decision Tree

```
Does it work correctly? → NO → 🔴 Fix bugs first
     ↓ YES
Does it have tests? → NO → 🔴 Add tests
     ↓ YES
Are tests good (not flaky)? → NO → 🟠 Fix test quality
     ↓ YES
Does QA pass? → NO → 🔴 Fix QA failures
     ↓ YES
Follows guidelines? → NO → 🟠 Align with standards
     ↓ YES
Is it simple? → NO → 🟡 Consider simplifying
     ↓ YES
APPROVE ✓
```

## What NOT to Do

- Don't nitpick formatting (use formatters)
- Don't demand unnecessary abstractions
- Don't block on style preferences
- Don't rewrite working code for elegance alone
- Don't ignore test failures as "probably flaky"
