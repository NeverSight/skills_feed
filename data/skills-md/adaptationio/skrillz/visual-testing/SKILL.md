---
name: visual-testing
description: Visual regression testing with Chromatic, Lost Pixel, and Playwright snapshots. Use when detecting UI changes, maintaining visual consistency, reviewing design changes, or setting up screenshot comparison in CI/CD.
---

# Visual Testing

## Overview

Visual regression testing catches unintended UI changes by comparing screenshots. This skill covers three approaches:

1. **Chromatic** - Cloud-based, unlimited parallelization (recommended)
2. **Lost Pixel** - Self-hosted, open source alternative
3. **Playwright Built-in** - Simple snapshot testing

---

## Quick Start: Chromatic (5 Minutes)

### 1. Install Chromatic

```bash
npm install --save-dev chromatic
```

### 2. Get Project Token

1. Go to [chromatic.com](https://chromatic.com)
2. Sign up with GitHub (free tier: 5000 snapshots/month)
3. Create project → Copy project token

### 3. Run First Build

```bash
# Set token
export CHROMATIC_PROJECT_TOKEN=your_token_here

# Run visual tests with Playwright
npx chromatic --playwright
```

### 4. Review Changes

- Chromatic UI shows visual diffs
- Approve or reject changes
- Approved changes become new baselines

---

## Chromatic with Playwright

### Configuration

```typescript
// playwright.config.ts
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests/visual',
  use: {
    screenshot: 'on',
  },
  reporter: [
    ['html'],
    ['chromatic', { projectToken: process.env.CHROMATIC_PROJECT_TOKEN }],
  ],
});
```

### Visual Test Example

```typescript
// tests/visual/homepage.spec.ts
import { test, expect } from '@playwright/test';

test('homepage visual', async ({ page }) => {
  await page.goto('/');

  // Full page screenshot
  await expect(page).toHaveScreenshot('homepage.png');
});

test('dashboard visual', async ({ page }) => {
  await page.goto('/dashboard');

  // Wait for data to load
  await page.waitForSelector('.dashboard-loaded');

  // Component screenshot
  const chart = page.locator('.revenue-chart');
  await expect(chart).toHaveScreenshot('revenue-chart.png');
});
```

### CI Integration (GitHub Actions)

```yaml
# .github/workflows/visual.yml
name: Visual Tests
on: [push, pull_request]

jobs:
  visual:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Required for Chromatic
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx chromatic --playwright
        env:
          CHROMATIC_PROJECT_TOKEN: ${{ secrets.CHROMATIC_PROJECT_TOKEN }}
```

### Chromatic Features (Free Tier)

| Feature | Free Tier |
|---------|-----------|
| Snapshots | 5000/month |
| Parallelization | Unlimited |
| Browsers | Chrome, Firefox, Safari |
| Review UI | Yes |
| GitHub Integration | Yes |

---

## Lost Pixel (Self-Hosted)

For confidential projects that can't use cloud services.

### Installation

```bash
npm install --save-dev lost-pixel
```

### Configuration

```typescript
// lostpixel.config.ts
import { CustomProjectConfig } from 'lost-pixel';

export const config: CustomProjectConfig = {
  pageShots: {
    pages: [
      { path: '/', name: 'home' },
      { path: '/login', name: 'login' },
      { path: '/dashboard', name: 'dashboard' },
    ],
    baseUrl: 'http://localhost:3000',
  },
  // Store baselines locally
  imagePathBaseline: '.lostpixel/baseline',
  imagePathCurrent: '.lostpixel/current',
  imagePathDifference: '.lostpixel/difference',

  // Fail on difference
  generateOnly: false,
  failOnDifference: true,

  // Comparison settings
  threshold: 0.1,  // 0.1% pixel difference allowed
};
```

### Run Lost Pixel

```bash
# Generate baselines (first run)
npx lost-pixel update

# Run comparison
npx lost-pixel

# View differences in .lostpixel/difference/
```

### Docker Setup (for CI)

```dockerfile
# Dockerfile.lostpixel
FROM mcr.microsoft.com/playwright:v1.40.0-focal

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .

CMD ["npx", "lost-pixel"]
```

```yaml
# .github/workflows/visual-selfhosted.yml
jobs:
  visual:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -f Dockerfile.lostpixel -t visual-tests .
      - run: docker run visual-tests
```

---

## Playwright Built-in Snapshots

Simplest approach, no external services.

### Basic Usage

```typescript
// tests/visual/basic.spec.ts
import { test, expect } from '@playwright/test';

test('visual regression', async ({ page }) => {
  await page.goto('/');

  // Full page
  await expect(page).toHaveScreenshot('homepage.png');

  // With options
  await expect(page).toHaveScreenshot('homepage-full.png', {
    fullPage: true,
    maxDiffPixels: 100,  // Allow 100 pixel difference
  });

  // Specific element
  const header = page.locator('header');
  await expect(header).toHaveScreenshot('header.png');
});
```

### Update Baselines

```bash
# Update all baselines
npx playwright test --update-snapshots

# Update specific test
npx playwright test tests/visual/homepage.spec.ts --update-snapshots
```

### Configuration

```typescript
// playwright.config.ts
export default defineConfig({
  expect: {
    toHaveScreenshot: {
      maxDiffPixels: 100,
      maxDiffPixelRatio: 0.01,  // 1%
      threshold: 0.2,  // Color difference threshold
    },
  },
  snapshotPathTemplate: '{testDir}/__screenshots__/{testFilePath}/{arg}{ext}',
});
```

### Cross-Platform Issues

**Problem**: Screenshots differ between Mac/Linux/Windows.

**Solutions**:

1. **Use Docker** (recommended):
```bash
# Run tests in consistent environment
docker run --rm -v $(pwd):/app mcr.microsoft.com/playwright:v1.40.0 \
  npx playwright test --update-snapshots
```

2. **Platform-specific baselines**:
```typescript
// playwright.config.ts
export default defineConfig({
  snapshotPathTemplate: '{testDir}/__screenshots__/{platform}/{testFilePath}/{arg}{ext}',
});
```

3. **Increase threshold**:
```typescript
await expect(page).toHaveScreenshot('page.png', {
  maxDiffPixelRatio: 0.05,  // 5% tolerance
});
```

---

## Comparison Matrix

| Feature | Chromatic | Lost Pixel | Playwright |
|---------|-----------|------------|------------|
| **Free Tier** | 5000 snapshots | Unlimited | Unlimited |
| **Self-Hosted** | No | Yes | Yes |
| **Parallelization** | Unlimited | Manual | Manual |
| **Review UI** | Yes (web) | No (local files) | No (local files) |
| **Cross-Browser** | Yes | Yes | Yes |
| **AI Detection** | Yes | No | No |
| **Setup Time** | 5 min | 15 min | 5 min |
| **Best For** | Teams, CI/CD | Confidential | Simple projects |

---

## Best Practices

### 1. Stable Selectors

```typescript
// Wait for dynamic content
await page.waitForSelector('[data-loaded="true"]');
await page.waitForLoadState('networkidle');

// Hide dynamic elements
await page.evaluate(() => {
  document.querySelectorAll('.timestamp').forEach(el => el.style.visibility = 'hidden');
});

await expect(page).toHaveScreenshot('page.png');
```

### 2. Consistent Viewport

```typescript
// playwright.config.ts
export default defineConfig({
  use: {
    viewport: { width: 1280, height: 720 },
  },
});

// Or per-test
test('mobile view', async ({ page }) => {
  await page.setViewportSize({ width: 375, height: 667 });
  await expect(page).toHaveScreenshot('mobile.png');
});
```

### 3. Mock Time/Data

```typescript
// Freeze time
await page.addInitScript(() => {
  Date.now = () => new Date('2024-01-15T10:00:00').getTime();
});

// Mock API responses
await page.route('**/api/user', route => {
  route.fulfill({
    json: { name: 'Test User', avatar: '/default-avatar.png' },
  });
});

await expect(page).toHaveScreenshot('profile.png');
```

### 4. Component-Level Testing

```typescript
// Test individual components
test('button states', async ({ page }) => {
  await page.goto('/storybook/button');

  const button = page.locator('.button');

  // Default state
  await expect(button).toHaveScreenshot('button-default.png');

  // Hover state
  await button.hover();
  await expect(button).toHaveScreenshot('button-hover.png');

  // Active state
  await button.click({ force: true });
  await expect(button).toHaveScreenshot('button-active.png');
});
```

---

## Workflow: Visual Testing in CI

### PR Workflow

```
1. Developer pushes code
   ↓
2. CI runs visual tests
   ↓
3. Chromatic detects changes
   ↓
4. Review visual diff in Chromatic UI
   ↓
5. Approve → New baseline
   Reject → Fix and re-push
   ↓
6. Merge PR
```

### Baseline Management

```bash
# Update baselines locally
npx playwright test --update-snapshots

# Commit baselines to git
git add tests/__screenshots__/
git commit -m "Update visual baselines"

# Or use Chromatic (baselines stored in cloud)
npx chromatic --auto-accept-changes  # Accept all changes
```

---

## References

- `references/chromatic-setup.md` - Complete Chromatic configuration
- `references/lost-pixel-self-hosted.md` - Self-hosted setup guide
- `references/playwright-snapshots.md` - Built-in snapshot testing

---

**Visual testing catches UI regressions before users do - choose Chromatic for teams, Lost Pixel for confidential projects.**
