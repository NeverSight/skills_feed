---
name: test
description: Run tests for the Pitfal Solutions project. Supports unit tests, E2E tests, and coverage reporting.
allowed-tools: Bash, Read
---

# Run Tests

Execute the test suite for the Pitfal Solutions website.

## Arguments
- `$ARGUMENTS` - Optional mode: `unit`, `e2e`, `coverage`, `watch`, `changed`, or empty for all tests

## Test Modes

### Run All Tests (Default)
```bash
pnpm test
```

### Unit/Component Tests Only
```bash
pnpm test
```

### E2E Tests (Playwright)
```bash
pnpm test:e2e
```

### E2E Tests with UI
```bash
pnpm test:e2e:ui
```

### Watch Mode (Development)
```bash
pnpm test:watch
```

### Changed Files Only (For Pre-Commit)
```bash
pnpm test:changed
```

### Coverage Report
```bash
pnpm test:coverage
```

## Coverage Thresholds

The project enforces 80% coverage thresholds for:
- Lines
- Functions
- Branches
- Statements

If coverage drops below 80%, the `test:coverage` command will fail.

## Test Categories

| Category | Location | Framework |
|----------|----------|-----------|
| Unit Tests | `src/**/*.test.ts` | Vitest |
| Component Tests | `src/**/*.test.tsx` | Vitest + Testing Library |
| API Tests | `lambda/**/*.test.ts` | Vitest |
| E2E Tests | `tests/e2e/*.spec.ts` | Playwright |

## Pre-Commit Workflow

Before committing code:
```bash
pnpm test:changed   # Tests for changed files only
pnpm lint           # Lint check
pnpm type-check     # TypeScript check
```

## CI Workflow

Full test suite for CI/CD:
```bash
pnpm test           # Full test suite
pnpm test:coverage  # Coverage report
pnpm test:e2e       # E2E tests
```

## Output

Report:
- Test results (pass/fail counts)
- Failed test details with stack traces
- Coverage summary (when using `coverage` mode)
- Recommendations for next steps
