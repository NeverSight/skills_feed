---
name: e2e-testing-expert
description: Senior End-to-End (E2E) Test Architect for 2026. Specialized in Playwright orchestration, visual regression testing, and high-performance CI/CD sharding. Expert in building resilient, auto-waiting test suites using the Page Object Model (POM), automated accessibility auditing (Axe-core), and deep-trace forensic debugging.
---

# 🧪 Skill: e2e-testing-expert (v1.0.0)

## Executive Summary
Senior End-to-End (E2E) Test Architect for 2026. Specialized in Playwright orchestration, visual regression testing, and high-performance CI/CD sharding. Expert in building resilient, auto-waiting test suites using the Page Object Model (POM), automated accessibility auditing (Axe-core), and deep-trace forensic debugging.

---

## 📋 The Conductor's Protocol

1.  **Test Surface Mapping**: Identify critical user flows (Happy Path, Edge Cases, Auth) that require E2E coverage.
2.  **Environment Sync**: Ensure the test environment (Staging/Preview) is seeded with predictable data and mocks.
3.  **Sequential Activation**:
    `activate_skill(name="e2e-testing-expert")` → `activate_skill(name="github-actions-pro")` → `activate_skill(name="ui-ux-pro")`.
4.  **Verification**: Execute `bun x playwright test` and verify results via the Trace Viewer for any flaky failures.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. User-Visible Locators First
As of 2026, CSS/XPath selectors are considered legacy and fragile.
- **Rule**: Always use `getByRole`, `getByText`, or `getByLabel`.
- **Protocol**: If an element is not reachable via a standard role, work with `ui-ux-pro` to fix the accessibility tree instead of adding `data-testid`.

### 2. Page Object Model (POM) Architecture
- **Rule**: Never write raw locators in test files.
- **Protocol**: Encapsulate all page-specific logic and selectors in POM classes under `tests/models/`.

### 3. Visual Regression & Masking
- **Rule**: Use `expect(page).toHaveScreenshot()` for critical UI components.
- **Protocol**: Mask dynamic content (dates, usernames, ads) using the `mask` property to prevent false positives.

### 4. Forensic Debugging (Tracing)
- **Rule**: Never debug via screenshots/videos in CI. Use Playwright Traces.
- **Protocol**: Configure `trace: 'on-first-retry'` in CI to capture full DOM snapshots and network logs for every failure.

### 5. Continuous Accessibility (Axe-core)
- **Rule**: Every E2E test must include an accessibility audit.
- **Protocol**: Use `@axe-core/playwright` to run `injectAxe` and `checkA11y` during key user flows.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Page Object Model (POM) Example
`tests/models/LoginPage.ts`:
```typescript
import { Page, Locator, expect } from "@playwright/test";

export class LoginPage {
  readonly page: Page;
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.emailInput = page.getByLabel("Email address");
    this.passwordInput = page.getByLabel("Password");
    this.loginButton = page.getByRole("button", { name: "Sign in" });
  }

  async goto() {
    await this.page.goto("/auth/login");
  }

  async login(email: string, pass: string) {
    await this.emailInput.fill(email);
    await this.passwordInput.fill(pass);
    await this.loginButton.click();
  }
}
```

### Visual Testing & Accessibility
```typescript
test("homepage looks correct and is accessible", async ({ page }) => {
  await page.goto("/");
  
  // 1. Accessibility Check
  await injectAxe(page);
  await checkA11y(page);

  // 2. Visual Regression
  await expect(page).toHaveScreenshot("homepage.png", {
    mask: [page.getByTestId("current-date")],
    maxDiffPixels: 100
  });
});
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** use `page.waitForTimeout()`. Use web-first assertions like `expect().toBeVisible()`.
2.  **DO NOT** test 3rd party APIs (Stripe, Auth0) directly. Use `page.route()` to mock them.
3.  **DO NOT** share state between tests. Use a fresh `BrowserContext` for every test.
4.  **DO NOT** run all tests in one job. Use Playwright Sharding (`--shard=1/3`) for large suites.
5.  **DO NOT** ignore console errors or warnings during tests. Fail the test if unexpected errors occur.

---

## 📂 Progressive Disclosure (Deep Dives)

- **[Advanced Locators & Auto-Waiting](./references/locators.md)**: Role-based vs. Text-based strategy.
- **[Network Mocking & Interception](./references/mocking.md)**: Using `page.route()` for stable tests.
- **[Sharding & Parallelism in CI](./references/ci-sharding.md)**: Running 1,000 tests in under 2 minutes.
- **[Visual Regression Strategies](./references/visual-testing.md)**: Tolerance, Masking, and Baseline management.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/analyze-traces.sh`: A wrapper to open the Trace Viewer for the latest CI failures.
- `scripts/generate-pom.ts`: Scaffolds a POM class based on a URL's accessibility tree.

---

## 🎓 Learning Resources
- [Playwright Official Documentation](https://playwright.dev/)
- [Axe-core Accessibility Testing](https://github.com/dequelabs/axe-core-playwright)
- [Modern E2E Testing Patterns 2026](https://example.com/e2e-2026)

---
*Updated: January 23, 2026 - 20:50*
