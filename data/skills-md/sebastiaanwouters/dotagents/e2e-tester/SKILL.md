---
name: e2e-tester
description: >
  Explores UI via agent-browser, generates CI-ready tests (Playwright or Pest).
  Triggers on "e2e test", "write e2e tests", "test the UI", "/e2e-tester".
---

# E2E Tester

Two-phase workflow: **explore interactively** via agent-browser, then **generate CI-ready** test code.

**Runtime:** agent-browser CLI (exploration)  
**Output:** Playwright Test files (JS/TS) or Pest Browser tests (Laravel/PHP)  
**Constraint:** Never commit `@ref` selectors—exploration-only

## Prerequisites

1. Load agent-browser skill: `use agent browser`
2. App running at accessible URL
3. Verify: `agent-browser open <url>` then `agent-browser snapshot -i`

## Two Modes

### 🔍 Exploration (agent-browser)

Use for discovery—DO NOT commit these selectors:

```bash
# Navigate and inspect
agent-browser open https://myapp.local
agent-browser snapshot -i              # Get interactive elements with @refs

# Interact using refs from snapshot
agent-browser click @e1
agent-browser fill @e2 "test@example.com"
agent-browser fill @e3 "password123"
agent-browser click @e4
agent-browser wait --load networkidle
agent-browser snapshot -i              # Check result
```

### ✅ Committed Test (CI-ready)

Generate this for test files—NO @refs, use stable locators:

**For Playwright (JS/TS):**
```ts
import { test, expect } from '@playwright/test';

test('user can log in', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('test@example.com');
  await page.getByLabel('Password').fill('password123');
  await page.getByRole('button', { name: /sign in/i }).click();
  
  await expect(page).toHaveURL(/\/dashboard/);
  await expect(page.getByRole('heading', { name: /welcome/i })).toBeVisible();
});
```

**For Pest Browser (Laravel):** See `reference/pest-browser.md`

## Locator Strategy (CI-safe)

Use in order of preference:

```ts
// 1. Test IDs (most stable)
page.getByTestId('sign-in-btn')

// 2. Role + name (semantic, accessible)
page.getByRole('button', { name: /submit/i })

// 3. Label (for form inputs)
page.getByLabel('Email')

// 4. CSS only if stable (data attributes)
page.locator('[data-action="save"]')
```

### Anti-patterns
- ❌ `@ref` selectors (exploration only)
- ❌ `.nth()` unless unavoidable
- ❌ CSS utility classes (`bg-blue-500`, `flex`)
- ❌ Dynamic/generated selectors
- ❌ `waitForTimeout` (use native waits)

## Canonical Playwright Template

```ts
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/login');
  });

  test('shows validation error for empty form', async ({ page }) => {
    await page.getByRole('button', { name: /sign in/i }).click();
    await expect(page.getByRole('alert')).toContainText('required');
  });

  test('logs in with valid credentials', async ({ page }) => {
    await page.getByLabel('Email').fill('user@test.com');
    await page.getByLabel('Password').fill('secure123');
    await page.getByRole('button', { name: /sign in/i }).click();
    await expect(page).toHaveURL(/\/dashboard/);
  });
});
```

## Wait Strategies

### In agent-browser (exploration)
```bash
agent-browser wait @e1                     # Wait for element
agent-browser wait --text "Success"        # Wait for text
agent-browser wait --url "**/dashboard"    # Wait for URL
agent-browser wait --load networkidle      # Network idle
```

### In CI tests (Playwright)
```ts
// ✅ Good: Playwright's built-in waits
await expect(page).toHaveURL(/\/dashboard/);
await expect(locator).toBeVisible();
await page.waitForResponse(res => res.url().includes('/api/users'));

// ❌ Avoid
await page.waitForTimeout(1000);
```

## Auth: storageState Pattern

Login once, reuse session:

```ts
// global-setup.ts
import { chromium } from '@playwright/test';

export default async function globalSetup() {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  await page.goto('/login');
  await page.getByLabel('Email').fill(process.env.TEST_USER_EMAIL!);
  await page.getByLabel('Password').fill(process.env.TEST_USER_PASSWORD!);
  await page.getByRole('button', { name: /sign in/i }).click();
  await page.waitForURL(/\/dashboard/);
  
  await page.context().storageState({ path: '.auth/user.json' });
  await browser.close();
}
```

```ts
// playwright.config.ts
export default defineConfig({
  globalSetup: './global-setup.ts',
  use: { storageState: '.auth/user.json' },
});
```

## agent-browser Quick Reference

| Task | Command |
|------|---------|
| Navigate | `agent-browser open <url>` |
| Inspect | `agent-browser snapshot -i` |
| Click | `agent-browser click @e1` |
| Fill | `agent-browser fill @e1 "text"` |
| Screenshot | `agent-browser screenshot` |
| Wait | `agent-browser wait --text "Done"` |
| Check state | `agent-browser is visible @e1` |

## Rules

### In agent-browser (exploration)
- Use `@ref` from snapshot to interact
- Re-snapshot after navigation/DOM changes
- Use `--headed` for visual debugging

### In CI tests (committed)
- Use `expect` assertions
- Use CI-safe locators: `getByTestId`, `getByRole`, `getByLabel`
- Never use `@ref` selectors
- Add `data-testid` to interactive elements when needed

## Reference Files

- `reference/pest-browser.md` - Laravel/Pest v4 browser testing
- `reference/advanced-patterns.md` - Page objects, dynamic content
- `reference/ci-cd.md` - GitHub Actions, Docker config
