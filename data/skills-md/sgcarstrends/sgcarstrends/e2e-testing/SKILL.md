---
name: e2e-testing
description: Write and run end-to-end tests with Playwright for user flows, page interactions, and visual regression. Use when testing user journeys, ensuring UI functionality works correctly.
allowed-tools: Read, Edit, Write, Bash, Grep, Glob
---

# End-to-End Testing Skill

This skill helps you write and run comprehensive end-to-end tests using Playwright.

## When to Use This Skill

- Testing complete user flows
- Verifying page interactions and navigation
- Testing form submissions
- Checking API integrations from the UI
- Visual regression testing
- Cross-browser compatibility testing
- Mobile responsiveness testing
- Before production deployments

## Playwright Overview

Playwright is a modern E2E testing framework that provides:
- **Cross-browser**: Chromium, Firefox, WebKit
- **Auto-waiting**: Intelligent element waiting
- **Network interception**: Mock API responses
- **Screenshots & videos**: Visual debugging
- **Parallel execution**: Fast test runs
- **TypeScript support**: Type-safe tests

## Project Configuration

### Installation

```bash
# Install Playwright (if not already installed)
pnpm add -D -w @playwright/test

# Install browsers
pnpm exec playwright install
```

### Configuration File

```typescript
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

export default defineConfig({
  testDir: "./apps/web/__tests__/e2e",
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ["html"],
    ["junit", { outputFile: "test-results/junit.xml" }],
  ],
  use: {
    baseURL: process.env.BASE_URL || "http://localhost:3001",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  projects: [
    {
      name: "chromium",
      use: { ...devices["Desktop Chrome"] },
    },
    {
      name: "firefox",
      use: { ...devices["Desktop Firefox"] },
    },
    {
      name: "webkit",
      use: { ...devices["Desktop Safari"] },
    },
    {
      name: "Mobile Chrome",
      use: { ...devices["Pixel 5"] },
    },
    {
      name: "Mobile Safari",
      use: { ...devices["iPhone 12"] },
    },
  ],
  webServer: {
    command: "pnpm -F @sgcarstrends/web dev",
    url: "http://localhost:3001",
    reuseExistingServer: !process.env.CI,
  },
});
```

## Test Structure

### File Organization

```
apps/web/
├── __tests__/
│   └── e2e/
│       ├── home.spec.ts              # Homepage tests
│       ├── cars/
│       │   ├── makes.spec.ts         # Car makes listing
│       │   └── models.spec.ts        # Car models listing
│       ├── coe/
│       │   └── bidding.spec.ts       # COE bidding results
│       ├── blog/
│       │   ├── list.spec.ts          # Blog listing
│       │   └── post.spec.ts          # Blog post detail
│       └── fixtures/
│           ├── mock-data.ts          # Test data
│           └── page-objects.ts       # Page object models
```

### Basic Test Example

```typescript
// apps/web/__tests__/e2e/home.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Homepage", () => {
  test("should load successfully", async ({ page }) => {
    await page.goto("/");

    // Check page title
    await expect(page).toHaveTitle(/SG Cars Trends/);

    // Check main heading
    const heading = page.getByRole("heading", { name: /SG Cars Trends/ });
    await expect(heading).toBeVisible();
  });

  test("should display navigation menu", async ({ page }) => {
    await page.goto("/");

    // Check nav links
    await expect(page.getByRole("link", { name: "Cars" })).toBeVisible();
    await expect(page.getByRole("link", { name: "COE" })).toBeVisible();
    await expect(page.getByRole("link", { name: "Blog" })).toBeVisible();
  });

  test("should navigate to cars page", async ({ page }) => {
    await page.goto("/");

    // Click cars link
    await page.getByRole("link", { name: "Cars" }).click();

    // Verify URL
    await expect(page).toHaveURL(/\/cars/);

    // Verify page content
    await expect(page.getByRole("heading", { name: /Cars/ })).toBeVisible();
  });
});
```

## Page Object Pattern

### Create Page Objects

```typescript
// apps/web/__tests__/e2e/fixtures/page-objects.ts
import { Page, Locator } from "@playwright/test";

export class HomePage {
  readonly page: Page;
  readonly heading: Locator;
  readonly carsLink: Locator;
  readonly coeLink: Locator;
  readonly blogLink: Locator;

  constructor(page: Page) {
    this.page = page;
    this.heading = page.getByRole("heading", { name: /SG Cars Trends/ });
    this.carsLink = page.getByRole("link", { name: "Cars" });
    this.coeLink = page.getByRole("link", { name: "COE" });
    this.blogLink = page.getByRole("link", { name: "Blog" });
  }

  async goto() {
    await this.page.goto("/");
  }

  async navigateToCars() {
    await this.carsLink.click();
  }

  async navigateToCOE() {
    await this.coeLink.click();
  }

  async navigateToBlog() {
    await this.blogLink.click();
  }
}

export class CarsPage {
  readonly page: Page;
  readonly heading: Locator;
  readonly makeSelect: Locator;
  readonly modelSelect: Locator;
  readonly resultsTable: Locator;

  constructor(page: Page) {
    this.page = page;
    this.heading = page.getByRole("heading", { name: /Cars/ });
    this.makeSelect = page.getByLabel("Make");
    this.modelSelect = page.getByLabel("Model");
    this.resultsTable = page.getByRole("table");
  }

  async goto() {
    await this.page.goto("/cars");
  }

  async selectMake(make: string) {
    await this.makeSelect.click();
    await this.page.getByRole("option", { name: make }).click();
  }

  async selectModel(model: string) {
    await this.modelSelect.click();
    await this.page.getByRole("option", { name: model }).click();
  }

  async getResultsCount(): Promise<number> {
    const rows = await this.resultsTable.locator("tbody tr").count();
    return rows;
  }
}
```

### Use Page Objects

```typescript
// apps/web/__tests__/e2e/cars/makes.spec.ts
import { test, expect } from "@playwright/test";
import { HomePage, CarsPage } from "../fixtures/page-objects";

test.describe("Cars Page", () => {
  test("should filter by make", async ({ page }) => {
    const homePage = new HomePage(page);
    const carsPage = new CarsPage(page);

    // Navigate to cars page
    await homePage.goto();
    await homePage.navigateToCars();

    // Select Toyota
    await carsPage.selectMake("Toyota");

    // Wait for results
    await expect(carsPage.resultsTable).toBeVisible();

    // Verify results contain Toyota
    const firstRow = page.locator("tbody tr").first();
    await expect(firstRow).toContainText("Toyota");
  });

  test("should filter by make and model", async ({ page }) => {
    const carsPage = new CarsPage(page);

    await carsPage.goto();
    await carsPage.selectMake("Toyota");
    await carsPage.selectModel("Corolla");

    // Verify results
    const count = await carsPage.getResultsCount();
    expect(count).toBeGreaterThan(0);
  });
});
```

## API Mocking

### Mock API Responses

```typescript
// apps/web/__tests__/e2e/cars/mocked.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Cars Page with Mocked API", () => {
  test("should display mocked car data", async ({ page }) => {
    // Mock API response
    await page.route("**/api/v1/cars/makes", async (route) => {
      await route.fulfill({
        status: 200,
        contentType: "application/json",
        body: JSON.stringify([
          { make: "Toyota", count: 1000 },
          { make: "Honda", count: 800 },
          { make: "BMW", count: 600 },
        ]),
      });
    });

    await page.goto("/cars");

    // Verify mocked data is displayed
    await expect(page.getByText("Toyota")).toBeVisible();
    await expect(page.getByText("1000")).toBeVisible();
  });

  test("should handle API errors gracefully", async ({ page }) => {
    // Mock API error
    await page.route("**/api/v1/cars/makes", async (route) => {
      await route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ error: "Internal server error" }),
      });
    });

    await page.goto("/cars");

    // Verify error message is displayed
    await expect(page.getByText(/error|failed/i)).toBeVisible();
  });
});
```

## Form Testing

### Test Form Submissions

```typescript
// apps/web/__tests__/e2e/blog/comment.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Blog Comment Form", () => {
  test("should submit comment successfully", async ({ page }) => {
    await page.goto("/blog/test-post");

    // Fill form
    await page.getByLabel("Name").fill("John Doe");
    await page.getByLabel("Email").fill("john@example.com");
    await page.getByLabel("Comment").fill("Great article!");

    // Submit
    await page.getByRole("button", { name: "Submit" }).click();

    // Verify success message
    await expect(page.getByText(/comment submitted/i)).toBeVisible();
  });

  test("should validate required fields", async ({ page }) => {
    await page.goto("/blog/test-post");

    // Submit empty form
    await page.getByRole("button", { name: "Submit" }).click();

    // Verify validation errors
    await expect(page.getByText(/name is required/i)).toBeVisible();
    await expect(page.getByText(/email is required/i)).toBeVisible();
  });

  test("should validate email format", async ({ page }) => {
    await page.goto("/blog/test-post");

    await page.getByLabel("Email").fill("invalid-email");
    await page.getByRole("button", { name: "Submit" }).click();

    await expect(page.getByText(/invalid email/i)).toBeVisible();
  });
});
```

## Visual Testing

### Screenshot Comparison

```typescript
// apps/web/__tests__/e2e/visual/homepage.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Visual Regression", () => {
  test("homepage should match snapshot", async ({ page }) => {
    await page.goto("/");

    // Wait for page to be fully loaded
    await page.waitForLoadState("networkidle");

    // Take screenshot and compare
    await expect(page).toHaveScreenshot("homepage.png", {
      fullPage: true,
      maxDiffPixels: 100,
    });
  });

  test("cars page should match snapshot", async ({ page }) => {
    await page.goto("/cars");
    await page.waitForLoadState("networkidle");

    await expect(page).toHaveScreenshot("cars-page.png", {
      fullPage: true,
    });
  });

  test("mobile homepage should match snapshot", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto("/");
    await page.waitForLoadState("networkidle");

    await expect(page).toHaveScreenshot("homepage-mobile.png", {
      fullPage: true,
    });
  });
});
```

## Accessibility Testing

### Test Accessibility

```typescript
// apps/web/__tests__/e2e/a11y/homepage.spec.ts
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test.describe("Accessibility", () => {
  test("homepage should not have accessibility violations", async ({ page }) => {
    await page.goto("/");

    const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

    expect(accessibilityScanResults.violations).toEqual([]);
  });

  test("should have proper heading hierarchy", async ({ page }) => {
    await page.goto("/");

    // Check h1 exists and is unique
    const h1Count = await page.locator("h1").count();
    expect(h1Count).toBe(1);

    // Check heading order
    const headings = await page.locator("h1, h2, h3, h4, h5, h6").all();
    const headingLevels = await Promise.all(
      headings.map((h) => h.evaluate((el) => el.tagName))
    );

    // H1 should come first
    expect(headingLevels[0]).toBe("H1");
  });

  test("should have alt text on images", async ({ page }) => {
    await page.goto("/");

    const images = await page.locator("img").all();

    for (const img of images) {
      const alt = await img.getAttribute("alt");
      expect(alt).toBeTruthy();
    }
  });
});
```

## Running Tests

### Common Commands

```bash
# Run all tests
pnpm exec playwright test

# Run specific test file
pnpm exec playwright test home.spec.ts

# Run tests in headed mode
pnpm exec playwright test --headed

# Run tests in specific browser
pnpm exec playwright test --project=chromium
pnpm exec playwright test --project=firefox

# Run tests in debug mode
pnpm exec playwright test --debug

# Run tests with UI
pnpm exec playwright test --ui

# Generate test report
pnpm exec playwright show-report

# Update screenshots
pnpm exec playwright test --update-snapshots
```

### Package.json Scripts

```json
{
  "scripts": {
    "test:e2e": "playwright test",
    "test:e2e:headed": "playwright test --headed",
    "test:e2e:debug": "playwright test --debug",
    "test:e2e:ui": "playwright test --ui",
    "test:e2e:report": "playwright show-report"
  }
}
```

## CI Configuration

### GitHub Actions

```yaml
# .github/workflows/e2e.yml
name: E2E Tests

on: [push, pull_request]

jobs:
  e2e:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install
      - run: pnpm exec playwright install --with-deps

      - run: pnpm test:e2e
        env:
          BASE_URL: http://localhost:3001

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30
```

## Best Practices

### 1. Use Locators Wisely

```typescript
// ❌ Fragile CSS selectors
await page.locator(".btn-primary").click();

// ✅ Semantic selectors
await page.getByRole("button", { name: "Submit" }).click();

// ✅ Text content
await page.getByText("Welcome").click();

// ✅ Label
await page.getByLabel("Email").fill("test@example.com");
```

### 2. Auto-waiting

```typescript
// ❌ Manual waiting
await page.waitForTimeout(1000);
await page.click("button");

// ✅ Auto-waiting
await page.getByRole("button").click();

// ✅ Wait for specific state
await page.getByRole("button").waitFor({ state: "visible" });
```

### 3. Isolate Tests

```typescript
// ❌ Tests depend on each other
test("create user", async ({ page }) => {
  // Creates user
});

test("login user", async ({ page }) => {
  // Assumes user from previous test exists
});

// ✅ Independent tests
test("create user", async ({ page }) => {
  // Creates user and cleans up
});

test("login user", async ({ page }) => {
  // Creates its own user, logs in, cleans up
});
```

### 4. Use Fixtures

```typescript
// apps/web/__tests__/e2e/fixtures/test.ts
import { test as base } from "@playwright/test";
import { HomePage, CarsPage } from "./page-objects";

type Fixtures = {
  homePage: HomePage;
  carsPage: CarsPage;
};

export const test = base.extend<Fixtures>({
  homePage: async ({ page }, use) => {
    await use(new HomePage(page));
  },
  carsPage: async ({ page }, use) => {
    await use(new CarsPage(page));
  },
});

export { expect } from "@playwright/test";

// Use in tests
import { test, expect } from "./fixtures/test";

test("test with fixtures", async ({ homePage, carsPage }) => {
  await homePage.goto();
  await homePage.navigateToCars();
  // ...
});
```

## Debugging

### Debug Mode

```bash
# Run with debugger
pnpm exec playwright test --debug

# Debug specific test
pnpm exec playwright test home.spec.ts --debug
```

### Inspector

```typescript
// Add breakpoint
await page.pause();

// Log to console
console.log(await page.title());

// Take screenshot
await page.screenshot({ path: "debug.png" });
```

### Trace Viewer

```bash
# Generate trace
pnpm exec playwright test --trace on

# View trace
pnpm exec playwright show-trace trace.zip
```

## Troubleshooting

### Tests Timing Out

```typescript
// Increase timeout
test("slow test", async ({ page }) => {
  test.setTimeout(60000); // 60 seconds

  await page.goto("/slow-page");
});

// Or in config
export default defineConfig({
  timeout: 30000, // 30 seconds
});
```

### Flaky Tests

```typescript
// Use waitForLoadState
await page.goto("/");
await page.waitForLoadState("networkidle");

// Wait for specific elements
await page.getByRole("button").waitFor({ state: "visible" });

// Retry assertions
await expect(page.getByText("Welcome")).toBeVisible({ timeout: 10000 });
```

### Selector Not Found

```typescript
// Check element exists
const button = page.getByRole("button", { name: "Submit" });
console.log(await button.count()); // 0 if not found

// Use has
await expect(page.getByRole("button")).toHaveCount(1);

// Debug selectors
await page.pause(); // Open inspector
```

## References

- Playwright Documentation: https://playwright.dev
- Best Practices: https://playwright.dev/docs/best-practices
- Accessibility Testing: https://playwright.dev/docs/accessibility-testing
- Related files:
  - `playwright.config.ts` - Playwright configuration
  - Root CLAUDE.md - Testing guidelines

## Best Practices Summary

1. **Use Semantic Selectors**: Prefer role, text, label over CSS selectors
2. **Isolate Tests**: Each test should be independent
3. **Auto-waiting**: Let Playwright wait for elements
4. **Page Objects**: Encapsulate page logic
5. **Mock APIs**: Use route mocking for predictable tests
6. **Visual Testing**: Compare screenshots for UI changes
7. **Accessibility**: Test with axe-core
8. **CI Integration**: Run tests in continuous integration
