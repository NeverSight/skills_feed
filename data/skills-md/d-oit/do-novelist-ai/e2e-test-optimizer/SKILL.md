---
name: e2e-test-optimizer
description:
  Optimizes Playwright E2E tests by removing waitForTimeout anti-patterns,
  implementing smart waits, and enabling test sharding for parallel execution.
  Use when tests timeout, CI execution exceeds limits, or test reliability
  issues occur.
---

# E2E Test Optimizer

## Quick Start

This skill helps fix three critical E2E test issues:

1. **Anti-pattern removal**: Replace arbitrary `waitForTimeout` with smart waits
2. **Test sharding**: Enable parallel test execution in CI
3. **Mock optimization**: Reduce mock setup overhead

### When to Use

- E2E tests timing out or failing due to arbitrary waits
- CI execution time exceeds 10 minutes
- Need test parallelization for faster feedback
- Test flakiness from race conditions

## Smart Wait Patterns

### Navigation Waits

```typescript
// ❌ Arbitrary wait
await page.click('[data-testid="nav-dashboard"]');
await page.waitForTimeout(1000);

// ✅ Wait for specific element
await page.click('[data-testid="nav-dashboard"]');
await expect(page.getByTestId('dashboard-content')).toBeVisible({
  timeout: 5000,
});
```

### State Transition Waits

```typescript
// ❌ Arbitrary wait after action
await page.getByRole('button', { name: 'Generate' }).click();
await page.waitForTimeout(2000);

// ✅ Wait for loading state completion
await page.getByRole('button', { name: 'Generate' }).click();
await expect(page.getByTestId('loading-spinner')).not.toBeVisible();
await expect(page.getByTestId('result')).toBeVisible();
```

### Network Waits

```typescript
// ❌ Arbitrary wait after submit
await page.getByRole('button', { name: 'Save' }).click();
await page.waitForTimeout(1500);

// ✅ Wait for network idle or success message
await page.getByRole('button', { name: 'Save' }).click();
await page.waitForLoadState('networkidle');
// OR
await expect(page.getByText('Saved successfully')).toBeVisible();
```

## Test Sharding Setup

Add to `.github/workflows/ci.yml`:

```yaml
e2e-tests:
  name: 🧪 E2E Tests [Shard ${{ matrix.shard }}/3]
  runs-on: ubuntu-latest
  timeout-minutes: 30
  needs: build-and-test
  strategy:
    fail-fast: false
    matrix:
      shard: [1, 2, 3]
  steps:
    - name: Run Playwright tests
      run: pnpm exec playwright test --shard=${{ matrix.shard }}/3
      env:
        CI: true
```

**Expected improvement**: 60-65% faster (27 minutes → 9-10 minutes)

## Detection Commands

```bash
# Find all waitForTimeout usage
grep -r "waitForTimeout" tests/specs/*.spec.ts

# Count per file
grep -c "waitForTimeout" tests/specs/*.spec.ts
```

## Standard Test Structure

```typescript
import { test, expect } from '@playwright/test';
import { setupGeminiMock } from '../utils/mock-ai-gateway';

test.describe('Feature Name', () => {
  test.beforeEach(async ({ page }) => {
    await setupGeminiMock(page);
    await page.goto('/');
    await page.waitForLoadState('networkidle');
  });

  test('should perform action', async ({ page }) => {
    // Navigate
    await page.getByTestId('nav-target').click();
    await expect(page.getByTestId('target-page')).toBeVisible();

    // Interact
    await page.getByRole('button', { name: 'Action' }).click();
    await expect(page.getByTestId('loading')).not.toBeVisible();

    // Assert
    await expect(page.getByTestId('result')).toBeVisible();
  });
});
```

## Element Selection Priority

```typescript
// ✅ Best: data-testid (stable, explicit)
await page.getByTestId('project-card');

// ✅ Good: role + name (semantic, accessible)
await page.getByRole('button', { name: 'Create' });

// ⚠️ OK: text (can break with i18n)
await page.getByText('Dashboard');

// ❌ Avoid: CSS selectors (brittle)
await page.locator('.project-card > div.title');
```

## Optimization Workflow

### Phase 1: Analysis

1. Scan test files for `waitForTimeout`
2. Count occurrences per file
3. Prioritize files by occurrence count

### Phase 2: Fix Anti-Patterns

1. Start with highest-priority file
2. Replace each `waitForTimeout` with smart wait
3. Run tests after each file: `playwright test path/to/file.spec.ts`
4. Commit per-file changes

### Phase 3: Implement Sharding

1. Update CI workflow with matrix strategy
2. Test locally: `playwright test --shard=1/3`
3. Push and monitor all 3 shards in CI

### Phase 4: Validation

1. Verify all tests pass
2. Confirm execution time < 10 minutes
3. Check shard balance (±2 min variance acceptable)

## Common Issues

**Tests still timing out after fix**

- Increase timeout on slow operations:
  `expect(...).toBeVisible({ timeout: 10000 })`

**Unbalanced shards (one takes much longer)**

- Use `--grep` to manually distribute heavy tests across shards

**Mock setup still slow**

- Implement global browser warm-up (see MOCK-OPTIMIZATION-GUIDE.md in
  tests/docs)

## Success Criteria

- Zero `waitForTimeout` calls in active tests
- CI execution time < 10 minutes
- All shards complete within ±2 minutes of each other
- 100% test pass rate (no flaky tests)

## References

See tests/docs/ for detailed guides:

- MOCK-OPTIMIZATION-GUIDE.md - Mock performance patterns
- MOCK-PERFORMANCE-ANALYSIS.md - Optimization results

External documentation:

- Playwright Best Practices: https://playwright.dev/docs/best-practices
- Test Sharding: https://playwright.dev/docs/test-sharding
