---
name: playwright-e2e-init
description: Initialize Playwright end-to-end testing for Next.js and React projects. Sets up configuration, creates example tests, and integrates with existing CI/CD. Use when adding E2E tests to a frontend project.
---

# Playwright E2E Testing Initialization

Sets up Playwright for end-to-end testing in Next.js and React applications.

## When to Use

This skill should be used when:

- Adding E2E tests to a Next.js project
- Setting up browser automation testing
- Creating user flow tests for critical paths
- Integrating E2E tests with CI/CD pipeline

## What It Does

1. **Installs Playwright** and browsers
2. **Creates configuration** (playwright.config.ts)
3. **Sets up test directory** (e2e/)
4. **Creates example tests** for common flows
5. **Adds npm scripts** for running tests
6. **Updates CI/CD** to run E2E tests

## Quick Start

Ask Claude to:

```
Add Playwright E2E tests to this project
```

Or be specific:

```
Set up E2E tests for the authentication flow
```

## Installation

```bash
bun add -D @playwright/test
bunx playwright install chromium
```

## Configuration

### playwright.config.ts

```typescript
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [["html", { open: "never" }], ["list"]],
  use: {
    baseURL: "http://localhost:3000",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    { name: "chromium", use: { ...devices["Desktop Chrome"] } },
  ],
  webServer: {
    command: "bun run dev",
    url: "http://localhost:3000",
    reuseExistingServer: !process.env.CI,
    timeout: 120 * 1000,
  },
});
```

## Test Structure

```
e2e/
├── home.spec.ts          # Homepage tests
├── auth.spec.ts          # Authentication flow
├── navigation.spec.ts    # Navigation tests
└── fixtures/
    └── test-data.ts      # Shared test data
```

## Example Tests

### Basic Navigation Test

```typescript
import { test, expect } from "@playwright/test";

test.describe("Homepage", () => {
  test("should load successfully", async ({ page }) => {
    await page.goto("/");
    await expect(page).toHaveTitle(/My App/);
  });

  test("should navigate to about page", async ({ page }) => {
    await page.goto("/");
    await page.click('a[href="/about"]');
    await expect(page).toHaveURL("/about");
  });
});
```

### Authentication Flow Test

```typescript
import { test, expect } from "@playwright/test";

test.describe("Authentication", () => {
  test("should login successfully", async ({ page }) => {
    await page.goto("/login");

    await page.fill('input[name="email"]', "test@example.com");
    await page.fill('input[name="password"]', "password123");
    await page.click('button[type="submit"]');

    await expect(page).toHaveURL("/dashboard");
    await expect(page.locator("text=Welcome")).toBeVisible();
  });

  test("should show error for invalid credentials", async ({ page }) => {
    await page.goto("/login");

    await page.fill('input[name="email"]', "wrong@example.com");
    await page.fill('input[name="password"]', "wrongpassword");
    await page.click('button[type="submit"]');

    await expect(page.locator("text=Invalid credentials")).toBeVisible();
  });
});
```

### Form Submission Test

```typescript
import { test, expect } from "@playwright/test";

test.describe("Contact Form", () => {
  test("should submit form successfully", async ({ page }) => {
    await page.goto("/contact");

    await page.fill('input[name="name"]', "John Doe");
    await page.fill('input[name="email"]', "john@example.com");
    await page.fill('textarea[name="message"]', "Hello, this is a test message");
    await page.click('button[type="submit"]');

    await expect(page.locator("text=Thank you")).toBeVisible();
  });
});
```

## NPM Scripts

Add to package.json:

```json
{
  "scripts": {
    "e2e": "playwright test",
    "e2e:ui": "playwright test --ui",
    "e2e:headed": "playwright test --headed",
    "e2e:debug": "playwright test --debug",
    "e2e:report": "playwright show-report"
  }
}
```

## CI/CD Integration

### GitHub Actions

Add to your CI workflow:

```yaml
- name: Install Playwright Browsers
  run: bunx playwright install --with-deps chromium

- name: Run E2E tests
  run: bun run e2e
  env:
    CI: true

- name: Upload Playwright Report
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: playwright-report
    path: playwright-report/
    retention-days: 7
```

## Best Practices

### 1. Test Critical User Flows

Focus on:

- Authentication (login, logout, signup)
- Core features (main value proposition)
- Payment/checkout flows
- Error handling

### 2. Use Page Object Model

```typescript
// e2e/pages/login.page.ts
import { Page } from "@playwright/test";

export class LoginPage {
  constructor(private page: Page) {}

  async goto() {
    await this.page.goto("/login");
  }

  async login(email: string, password: string) {
    await this.page.fill('input[name="email"]', email);
    await this.page.fill('input[name="password"]', password);
    await this.page.click('button[type="submit"]');
  }
}
```

### 3. Use Data Attributes for Selectors

```html
<button data-testid="submit-button">Submit</button>
```

```typescript
await page.click('[data-testid="submit-button"]');
```

### 4. Keep Tests Independent

Each test should:

- Set up its own state
- Not depend on other tests
- Clean up after itself

### 5. Use Fixtures for Common Setup

```typescript
import { test as base } from "@playwright/test";

const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    await page.goto("/login");
    await page.fill('input[name="email"]', "test@example.com");
    await page.fill('input[name="password"]', "password");
    await page.click('button[type="submit"]');
    await use(page);
  },
});
```

## Troubleshooting

### Tests timing out

Increase timeout in config:

```typescript
timeout: 60000, // 60 seconds
```

### Elements not found

Use `waitFor`:

```typescript
await page.waitForSelector('[data-testid="element"]');
```

### Flaky tests

Add retries and use `toPass`:

```typescript
await expect(async () => {
  await expect(page.locator("text=Success")).toBeVisible();
}).toPass({ timeout: 10000 });
```

## Integration with Other Skills

| Skill | Integration |
|-------|-------------|
| `testing-cicd-init` | Sets up unit tests first |
| `testing-expert` | Provides testing patterns |
| `webapp-testing` | Alternative automation skill |

---

**When this skill is active**, Claude will:

1. Install Playwright and browsers
2. Create configuration file
3. Set up e2e/ directory
4. Create example tests for existing pages
5. Add npm scripts
6. Update CI/CD workflow
