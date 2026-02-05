---
name: run-tests
description: Run the test suite for the Cartridge Controller monorepo. Use when validating changes, before committing, or when asked to run tests.
---

# Run Tests

## Quick Reference

| Command | Purpose | Duration |
|---------|---------|----------|
| `pnpm lint:check` | Lint + format check | ~30s |
| `pnpm test` | Unit tests | ~1-2min |
| `pnpm test:ci` | Unit tests with coverage | ~2-3min |
| `pnpm test:storybook` | Visual regression tests | ~5-10min |
| `pnpm build` | Full build (includes type check) | ~2-3min |
| `pnpm e2e` | End-to-end tests | ~5-10min |

## Test Types

### 1. Linting and Formatting

Fastest check - always run before committing:

```bash
pnpm lint:check
```

This runs:
- ESLint for code quality
- Prettier for formatting

To auto-fix issues:
```bash
pnpm format  # Fix formatting + lint
```

### 2. Unit Tests

Tests the keychain package:

```bash
# Standard run
pnpm test

# With coverage report
pnpm test:ci

# Run specific test file
pnpm keychain test -- --testPathPattern="connection"
```

Test files are located in:
- `packages/keychain/src/**/*.test.ts`
- `packages/controller/src/__tests__/`

### 3. Storybook Visual Regression Tests

Tests UI components for visual changes:

```bash
# Run visual tests (compares against baseline)
pnpm test:storybook

# Update baseline snapshots after intentional changes
pnpm test:storybook:update
```

Snapshots are stored in:
- `packages/keychain/__image_snapshots__/`

### 4. Build (Type Checking)

TypeScript compilation catches type errors:

```bash
pnpm build
```

This also validates that all packages compile correctly.

### 5. End-to-End Tests

Full integration tests with Playwright:

```bash
# Run headless
pnpm e2e

# Run with UI for debugging
pnpm e2e:ui
```

E2E tests are in:
- `examples/next/tests/`

## CI Equivalence

To mirror what CI runs, execute in order:

```bash
# 1. Quality checks (quality.yml)
pnpm lint:check

# 2. Build and test (test.yml)
pnpm build
pnpm test:ci

# 3. Visual regression (test.yml - storybook job)
pnpm test:storybook
```

## Interpreting Results

### Test Failures

```bash
# Re-run failed test with more details
pnpm keychain test -- --verbose --testNamePattern="failing test name"
```

### Snapshot Failures

If Storybook tests fail with visual differences:
1. Review the diff images in `packages/keychain/__image_snapshots__/__diff_output__/`
2. If changes are intentional: `pnpm test:storybook:update`
3. If changes are unintentional: fix the component

### Type Errors

```bash
# Check specific package
pnpm controller build
pnpm keychain build
```

## Package-Specific Testing

```bash
# Controller SDK tests
pnpm controller test

# Keychain tests
pnpm keychain test

# Run test in watch mode for development
pnpm keychain test -- --watch
```

## Common Issues

### "Cannot find module" errors
```bash
pnpm clean && pnpm i && pnpm build:deps
```

### Storybook tests timeout
Ensure the Storybook server is not already running on port 6006.

### E2E tests fail to start
Ensure dev servers are running:
```bash
pnpm dev  # In one terminal
pnpm e2e  # In another
```

## Pre-Commit Verification

The git pre-commit hook automatically runs:
```bash
pnpm run format --ui stream
pnpm run lint:check --ui stream
```

This ensures basic quality before every commit.
