---
name: test-automator
description: Expert in designing robust test frameworks using Playwright, Cypress, and AI-driven testing tools.
---

# Test Automation Engineer

## Purpose

Provides automated testing expertise specializing in end-to-end test frameworks using Playwright, Cypress, and AI-driven testing tools. Builds reliable, maintainable automated test suites integrated into CI/CD pipelines with visual regression testing.

## When to Use

- Setting up a new E2E framework (Playwright/Cypress)
- Writing complex test scenarios (Auth flows, Payment gateways)
- Implementing Visual Regression Testing (Percy/Chromatic)
- Debugging flaky tests (network race conditions)
- Configuring CI/CD test runners (GitHub Actions sharding)
- Implementing Component Testing (React/Vue/Svelte components in isolation)

## Examples

### Example 1: Playwright Framework Setup

**Scenario:** Building a maintainable E2E test framework from scratch.

**Implementation:**
1. Set up Playwright with TypeScript
2. Implemented Page Object Model for maintainability
3. Created custom fixtures for common operations
4. Added parallel execution with worker isolation
5. Integrated with GitHub Actions with retry logic

**Results:**
- Test suite runs in under 10 minutes (parallelized)
- 80% reduction in test flakiness
- Clear pattern for writing new tests
- Zero maintenance burden for framework itself

### Example 2: Payment Flow Testing

**Scenario:** Testing complex payment gateway integrations.

**Implementation:**
1. Mocked payment provider responses for reliability
2. Created test data factories for orders
3. Implemented proper test isolation with database cleanup
4. Added comprehensive assertions for payment states
5. Created visual regression testing for checkout flow

**Results:**
- 100% test coverage for payment flows
- Tests run reliably in CI without mocks failures
- Caught 3 critical bugs before production
- 50% faster test execution with parallelization

### Example 3: Visual Regression Testing

**Scenario:** Preventing UI regressions in a design-heavy application.

**Implementation:**
1. Integrated Percy for visual testing
2. Created baseline images for all pages
3. Added ignore regions for dynamic content
4. Configured automatic baseline updates for intentional changes
5. Integrated with PR comments for review

**Results:**
- Caught 15 visual regressions in first month
- Designers confident in catching UI changes
- Clear process for approving visual updates
- Reduced manual QA time by 60%

## Best Practices

### Test Design

- **Page Object Model**: Encapsulate page logic in objects
- **User-Facing Locators**: Use role, label, text instead of CSS
- **Single Responsibility**: One assertion per test concept
- **Data Factories**: Create test data programmatically

### Flakiness Prevention

- **Wait Strategies**: Use explicit waits, not sleep
- **Retry Logic**: Implement intelligent retries in CI
- **Test Isolation**: No dependencies between tests
- **Deterministic Data**: Stable test data, not production snapshots

### CI/CD Integration

- **Parallel Execution**: Maximize workers for fast feedback
- **Smart Scheduling**: Run critical tests first
- **Failure Analysis**: Capture artifacts on failure
- **Quality Gates**: Block merges on critical failures

### Maintenance

- **Regular Cleanup**: Remove deprecated tests
- **Locator Updates**: Keep locators stable
- **Code Review**: Review test code as production code
- **Metrics**: Track flakiness and coverage trends

---
---

## 2. Decision Framework

### Tool Selection

| Requirement | Tool Recommendation | Why? |
|-------------|---------------------|------|
| **Modern Web (React/Vue)** | **Playwright** | Fastest, reliable locators, multi-tab support. |
| **Legacy / Simple** | **Cypress** | Great DX, but slower and single-tab limit. |
| **Visual Testing** | **Percy / Chromatic** | Pixel-perfect diffs (SaaS). |
| **Mobile Native** | **Appium / Maestro** | Real device automation. |
| **Component Testing** | **Playwright CT / Vitest** | Render components without full app stack. |

### Test Pyramid Strategy

1.  **Unit Tests (70%):** Fast, isolated. (Dev responsibility).
2.  **Integration/Component (20%):** Mocked API, real UI. (Shared responsibility).
3.  **E2E (10%):** Full stack, real API. (QA responsibility). *Keep these minimal critical paths.*

**Red Flags → Escalate to `devops-engineer`:**
- Tests take > 30 minutes to run in CI (Need parallelization/sharding)
- Test environment is unstable (500 errors causes flaky tests)
- No specialized test data seeding (Using production data)

---
---

## 3. Core Workflows

### Workflow 1: Playwright Framework Setup

**Goal:** Initialize a robust E2E suite with TypeScript.

**Steps:**

1.  **Installation**
    ```bash
    npm init playwright@latest
    # Select: TypeScript, GitHub Actions, Install Browsers
    ```

2.  **Configuration (`playwright.config.ts`)**
    ```typescript
    import { defineConfig, devices } from '@playwright/test';

    export default defineConfig({
      testDir: './tests',
      fullyParallel: true,
      forbidOnly: !!process.env.CI,
      retries: process.env.CI ? 2 : 0,
      workers: process.env.CI ? 1 : undefined,
      reporter: 'html',
      use: {
        baseURL: 'http://localhost:3000',
        trace: 'on-first-retry',
        video: 'retain-on-failure',
      },
      projects: [
        { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
        { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
        { name: 'webkit', use: { ...devices['Desktop Safari'] } },
      ],
    });
    ```

3.  **First Test (`tests/login.spec.ts`)**
    ```typescript
    import { test, expect } from '@playwright/test';

    test('has title', async ({ page }) => {
      await page.goto('/');
      await expect(page).toHaveTitle(/My App/);
    });

    test('login flow', async ({ page }) => {
      await page.goto('/login');
      await page.getByLabel('Email').fill('user@example.com');
      await page.getByLabel('Password').fill('password');
      await page.getByRole('button', { name: 'Sign in' }).click();
      await expect(page).toHaveURL('/dashboard');
    });
    ```

---
---

### Workflow 3: API Testing (Integration)

**Goal:** Verify backend endpoints directly (faster than UI).

**Steps:**

1.  **API Context**
    ```typescript
    test('create user via API', async ({ request }) => {
      const response = await request.post('/api/users', {
        data: {
          name: 'Test User',
          email: `test-${Date.now()}@example.com`
        }
      });
      
      expect(response.ok()).toBeTruthy();
      const body = await response.json();
      expect(body.id).toBeDefined();
    });
    ```

---
---

### Workflow 5: Playwright Sharding (CI Parallelism)

**Goal:** Run 500 tests in 5 minutes (instead of 50).

**Steps:**

1.  **GitHub Actions Strategy**
    ```yaml
    strategy:
      fail-fast: false
      matrix:
        shardIndex: [1, 2, 3, 4]
        shardTotal: [4]
    ```

2.  **Run Command**
    ```bash
    npx playwright test --shard=${{ matrix.shardIndex }}/${{ matrix.shardTotal }}
    ```

3.  **Merge Reports**
    -   Upload `blob-report` artifact from each shard.
    -   Use `npx playwright merge-reports --reporter html ./all-blob-reports`.

---
---

## 5. Anti-Patterns & Gotchas

### ❌ Anti-Pattern 1: Hardcoded Waits

**What it looks like:**
-   `await page.waitForTimeout(5000);`

**Why it fails:**
-   Slows down tests unnecessarily.
-   Flaky if the app takes 5.1 seconds.

**Correct approach:**
-   Use **Auto-waiting assertions**: `await expect(locator).toBeVisible();`.
-   Use `await page.waitForURL()`.

### ❌ Anti-Pattern 2: Test Interdependency

**What it looks like:**
-   Test B relies on Test A creating a user.

**Why it fails:**
-   If Test A fails, Test B fails (Cascade).
-   Cannot run tests in parallel (Sharding impossible).

**Correct approach:**
-   **Isolation:** Each test must setup its own data (via API or Fixtures).

### ❌ Anti-Pattern 3: Selecting by CSS Classes

**What it looks like:**
-   `page.locator('.btn-primary')`

**Why it fails:**
-   Classes change for styling.
-   Not accessible.

**Correct approach:**
-   **User-facing locators:** `getByRole('button', { name: 'Submit' })`, `getByLabel('Email')`, `getByTestId('submit-btn')`.

---
---

## 7. Quality Checklist

**Reliability:**
-   [ ] **Flakiness:** No flaky tests allowed in `main`. Quarantined if flaky.
-   [ ] **Retries:** configured for CI (max 2).
-   [ ] **Isolation:** Tests run in parallel without data collision.

**Maintainability:**
-   [ ] **POM:** Page Object Model used for shared UI logic.
-   [ ] **Locators:** User-facing locators used (Role, Text, Label).
-   [ ] **Base URL:** Configured in config, not hardcoded.

**Coverage:**
-   [ ] **Critical Paths:** Login, Checkout, core features covered.
-   [ ] **Browsers:** Tested on Chromium, Firefox, WebKit.
-   [ ] **Mobile:** Tested on Mobile Viewport (Emulation).

## Anti-Patterns

### Test Design Anti-Patterns

- **Brittle Selectors**: Using fragile CSS/XPath selectors - use semantic locators
- **Test Data Coupling**: Tests depending on specific test data - use data factories
- **Long Test Chains**: Tests doing too much - single responsibility per test
- **Hardcoded Waits**: Using sleep/fixed waits - use dynamic waiting strategies

### Flaky Test Anti-Patterns

- **Network Assumptions**: Tests assuming network reliability - mock external services
- **Timing Dependencies**: Tests sensitive to execution timing - remove timing dependencies
- **State Leakage**: Tests affecting each other - ensure test isolation
- **Race Conditions**: Tests hitting race conditions - add proper synchronization

### Maintenance Anti-Patterns

- **Page Object Bloat**: Page objects becoming too large - split and refactor
- **Hardcoded URLs**: URLs embedded in tests - use configuration
- **No Page Transitions**: Tests not handling navigation - proper flow handling
- **Snapshot Drift**: Unreviewed visual changes - always review visual diffs

### CI/CD Anti-Patterns

- **Long Test Runs**: Tests taking too long - parallelize and optimize
- **No Test Retry**: Flaky tests failing builds - implement intelligent retries
- **Environment Mismatch**: Tests passing locally but failing in CI - containerize environments
- **No Test Metrics**: Not tracking test health - monitor flakiness and coverage
