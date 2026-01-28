---
name: visual-regression-testing
description: Comprehensive visual regression testing using Playwright and jest-image-snapshot. Implements screenshot comparison, baseline management, CI/CD integration, and visual diff reporting following Ant Design best practices. Use for preventing visual bugs, ensuring UI consistency, and automating visual QA. (project)
license: Complete terms in LICENSE.txt
---

# Visual Regression Testing

This skill provides comprehensive visual regression testing capabilities to detect unintended visual changes in UI components and prevent visual bugs from being merged into production.

## Overview

Visual regression testing works by:
1. Taking screenshots of components/pages in a known-good state (baselines)
2. Taking new screenshots after code changes
3. Comparing new screenshots with baselines pixel-by-pixel
4. Flagging differences for human review

**Framework**: Playwright + jest-image-snapshot
**Approach**: Based on Ant Design's visual regression testing methodology

## Core Capabilities

### 1. Screenshot Baseline Management

Create and update baseline screenshots that serve as the source of truth for visual comparison.

**Implementation**: `tests/shared/imageTest.tsx`

Key features:
- Automated baseline capture for all component demos
- Version-controlled baseline storage
- Easy baseline updates when intentional changes occur
- Support for multiple viewport sizes and themes

### 2. Visual Comparison Testing

**Implementation**: `scripts/visual-regression/`

Core testing workflow:
```typescript
// Example structure from tests/shared/imageTest.tsx
import { test, expect } from '@playwright/test';

test('component visual regression', async ({ page }) => {
  await page.goto('http://localhost:5173/component-demo');
  await page.waitForLoadState('networkidle');

  // Take screenshot and compare with baseline
  const screenshot = await page.screenshot();
  expect(screenshot).toMatchImageSnapshot({
    customSnapshotsDir: '__image_snapshots__',
    customDiffDir: '__image_snapshots__/diff',
    threshold: 0.1, // 0.1% pixel difference tolerance
  });
});
```

### 3. CI/CD Integration

**Implementation**: `.github/workflows/visual-regression-*.yml`

Workflow files:
- `visual-regression-pr.yml` - Runs on pull requests
- `visual-regression-baseline.yml` - Updates baselines on main branch
- `visual-regression-report.yml` - Generates and uploads diff reports

**PR Workflow**:
1. Checkout code and install dependencies
2. Start local server
3. Run visual regression tests
4. If differences found:
   - Generate diff screenshots
   - Upload artifacts to GitHub
   - Post comment on PR with visual diff preview
   - Mark check as failed
5. If no differences, mark check as passed

**Baseline Update Workflow**:
1. Runs on main branch after merge
2. Regenerates all baseline screenshots
3. Commits updated baselines back to repo

## File Structure

```
.github/workflows/
  ├── visual-regression-pr.yml          # PR visual checks
  ├── visual-regression-baseline.yml    # Baseline updates
  └── visual-regression-report.yml      # Diff reporting

tests/shared/
  └── imageTest.tsx                     # Baseline screenshot utilities

scripts/visual-regression/
  ├── capture-baselines.ts              # Generate baseline screenshots
  ├── compare-screenshots.ts            # Compare current vs baseline
  ├── generate-report.ts                # Create HTML diff report
  └── upload-to-storage.ts              # Upload to OSS/S3

__image_snapshots__/
  ├── baseline/                         # Baseline screenshots
  ├── current/                          # Latest test screenshots
  └── diff/                             # Difference highlights
```

## Usage Patterns

### For Component Development

When developing a new component:
```bash
# 1. Create component and demos
npm run dev

# 2. Generate initial baseline
npm run visual:baseline

# 3. Make changes
# ... edit component code ...

# 4. Run visual regression test
npm run visual:test

# 5. Review diffs (if any)
npm run visual:report

# 6. Update baseline if changes are intentional
npm run visual:update-baseline
```

### For PR Reviews

Reviewers can:
1. Check CI status for visual regression failures
2. Click artifact link in PR comment
3. Review visual diff report
4. Approve/request changes based on visual impact

### For CI/CD Pipeline

```yaml
# Example from .github/workflows/visual-regression-pr.yml
name: Visual Regression Testing

on:
  pull_request:
    branches: [main, develop]

jobs:
  visual-regression:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright
        run: npx playwright install --with-deps chromium

      - name: Start dev server
        run: npm run dev &

      - name: Wait for server
        run: npx wait-on http://localhost:5173

      - name: Run visual regression tests
        run: npm run visual:test

      - name: Upload diff artifacts
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: visual-diffs
          path: __image_snapshots__/diff/

      - name: Generate report
        if: failure()
        run: npm run visual:report

      - name: Comment PR with results
        if: failure()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('visual-report.md', 'utf8');
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            });
```

## Best Practices

### 1. Baseline Management

- **Version control baselines**: Commit baseline screenshots to git
- **Update selectively**: Only update baselines for intentional visual changes
- **Document updates**: Include baseline updates in PR descriptions
- **Platform consistency**: Generate baselines in CI environment, not locally

### 2. Test Writing

- **Wait for stability**: Always use `page.waitForLoadState('networkidle')`
- **Hide dynamic content**: Mask timestamps, animations, random data
- **Test critical paths**: Focus on user-facing components
- **Multiple viewports**: Test responsive breakpoints
- **Theme variants**: Test light/dark modes if applicable

### 3. Threshold Configuration

```typescript
// Strict comparison for critical UI
expect(screenshot).toMatchImageSnapshot({ threshold: 0.01 });

// Relaxed for minor anti-aliasing differences
expect(screenshot).toMatchImageSnapshot({ threshold: 0.1 });

// Very relaxed for charts/animations
expect(screenshot).toMatchImageSnapshot({ threshold: 0.5 });
```

### 4. Performance Optimization

- **Parallel execution**: Run tests in parallel across multiple workers
- **Selective testing**: Only test affected components in PR
- **Incremental baselines**: Cache and reuse unchanged baselines
- **Headless mode**: Always run in headless mode in CI

### 5. False Positive Reduction

Common causes of false positives:
- Font rendering differences across OS
- Anti-aliasing variations
- Animation timing
- Browser version differences
- System fonts

Solutions:
- Use Docker for consistent environment
- Freeze animations with CSS
- Use consistent browser versions
- Increase threshold for minor differences

## Integration with Existing Testing

Visual regression testing complements existing testing strategies:

```
Unit Tests (Jest)
  ↓
Component Tests (React Testing Library)
  ↓
Visual Regression (Playwright + jest-image-snapshot)
  ↓
E2E Tests (Playwright)
  ↓
Manual QA
```

## Troubleshooting

### "Screenshots don't match but look identical"

**Cause**: Platform-specific rendering differences
**Solution**:
```typescript
expect(screenshot).toMatchImageSnapshot({
  failureThreshold: 0.01,
  failureThresholdType: 'percent'
});
```

### "Baselines outdated after dependency update"

**Cause**: Library update changed component styling
**Solution**:
```bash
# Review changes first
npm run visual:test

# Update all baselines if changes are expected
npm run visual:update-baseline
```

### "CI fails but local tests pass"

**Cause**: Different environments (fonts, OS, browser version)
**Solution**: Use Docker or GitHub Actions locally
```bash
# Run in Docker matching CI environment
docker run -v $(pwd):/app -w /app mcr.microsoft.com/playwright:v1.40.0 npm run visual:test
```

## References

### Implementation Files

- `.github/workflows/visual-regression-*.yml` - CI/CD workflows
- `tests/shared/imageTest.tsx` - Baseline screenshot implementation
- `scripts/visual-regression/` - Test code and utilities

### External Resources

- [Ant Design Visual Regression](https://ant.design/docs/blog/visual-regression/) - Original methodology
- [Playwright Screenshots](https://playwright.dev/docs/screenshots) - Screenshot API docs
- [jest-image-snapshot](https://github.com/americanexpress/jest-image-snapshot) - Snapshot matcher
- [Argos CI](https://argos-ci.com/) - Visual testing platform (used by Ant Design)

## Advanced Features

### Multi-Browser Testing

```typescript
// Test across Chromium, Firefox, and WebKit
import { devices } from '@playwright/test';

const browsers = ['chromium', 'firefox', 'webkit'];
for (const browser of browsers) {
  test(`visual regression on ${browser}`, async ({ playwright }) => {
    const browserInstance = await playwright[browser].launch();
    const page = await browserInstance.newPage();
    // ... test logic
  });
}
```

### Responsive Testing

```typescript
// Test multiple viewports
const viewports = [
  { width: 375, height: 667, name: 'mobile' },
  { width: 768, height: 1024, name: 'tablet' },
  { width: 1920, height: 1080, name: 'desktop' },
];

for (const viewport of viewports) {
  test(`visual regression ${viewport.name}`, async ({ page }) => {
    await page.setViewportSize(viewport);
    // ... test logic
  });
}
```

### Component Isolation

```typescript
// Test individual component variants
const variants = ['default', 'primary', 'danger', 'disabled'];

for (const variant of variants) {
  test(`button ${variant} variant`, async ({ page }) => {
    await page.goto(`http://localhost:5173/button/${variant}`);
    await page.waitForLoadState('networkidle');
    const screenshot = await page.locator('[data-testid="button"]').screenshot();
    expect(screenshot).toMatchImageSnapshot({
      customSnapshotIdentifier: `button-${variant}`
    });
  });
}
```

## Agent Capabilities

When users request visual regression testing, the agent should:

1. **Setup Infrastructure**
   - Create GitHub Actions workflows
   - Configure Playwright with jest-image-snapshot
   - Set up baseline directory structure
   - Add npm scripts for common operations

2. **Generate Tests**
   - Create test files for each component
   - Configure appropriate thresholds
   - Handle dynamic content masking
   - Set up multi-viewport testing

3. **Integrate with CI/CD**
   - Configure PR checks
   - Set up baseline update workflows
   - Configure artifact uploads
   - Add PR commenting with diff previews

4. **Provide Documentation**
   - Document baseline update process
   - Create troubleshooting guides
   - Add examples for common scenarios
   - Document threshold configuration

## Example: Full Implementation

See the following files for complete implementation examples:
- `.github/workflows/visual-regression-pr.yml:1` - Full PR workflow
- `tests/shared/imageTest.tsx:1` - Baseline screenshot utilities
- `scripts/visual-regression/compare-screenshots.ts:1` - Comparison logic

This skill enables comprehensive visual regression testing that catches visual bugs before they reach production, maintaining UI consistency across the entire application.
