---
name: playwright
description: >
  Playwright E2E testing patterns.
  Trigger: When writing Playwright E2E tests (Page Object Model, selectors, MCP exploration workflow).
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root, ui]
  auto_invoke: "Writing Playwright E2E tests"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## When to Use

Use this skill when:
- Writing E2E tests with Playwright
- Creating Page Object Models
- Setting up selectors and assertions
- Using MCP for test exploration

---

## MCP Workflow (MANDATORY If Available)

**⚠️ If you have Playwright MCP tools, ALWAYS use them BEFORE creating any test:**

1. **Navigate** to target page
2. **Take snapshot** to see page structure and elements
3. **Interact** with forms/elements to verify exact user flow
4. **Take screenshots** to document expected states
5. **Verify page transitions** through complete flow
6. **Document actual selectors** from snapshots
7. **Only after exploring** create test code with verified selectors

**Why This Matters:**
- ✅ Precise tests - exact steps needed, no assumptions
- ✅ Accurate selectors - real DOM structure
- ✅ Real flow validation
- ✅ Avoid over-engineering
- ✅ Prevent flaky tests

---

## Critical Patterns

### File Structure (REQUIRED)

```
tests/
├── base-page.ts              # Parent class for ALL pages
├── helpers.ts                # Shared utilities
└── {page-name}/
    ├── {page-name}-page.ts   # Page Object Model
    ├── {page-name}.spec.ts   # ALL tests here (NO separate files!)
    └── {page-name}.md        # Test documentation
```

**File Naming:**
- ✅ `sign-up.spec.ts` (all sign-up tests)
- ❌ `sign-up-critical-path.spec.ts` (WRONG - no separate files)

### Selector Priority (REQUIRED)

```typescript
// 1. BEST - getByRole for interactive elements
this.submitButton = page.getByRole("button", { name: "Submit" });
this.navLink = page.getByRole("link", { name: "Dashboard" });

// 2. BEST - getByLabel for form controls
this.emailInput = page.getByLabel("Email");
this.passwordInput = page.getByLabel("Password");

// 3. SPARINGLY - getByText for static content only
this.errorMessage = page.getByText("Invalid credentials");

// 4. LAST RESORT - getByTestId when above fail
this.customWidget = page.getByTestId("date-picker");

// ❌ AVOID fragile selectors
this.button = page.locator(".btn-primary");  // NO
this.input = page.locator("#email");         // NO
```

### Page Object Pattern (REQUIRED)

```typescript
import { Page, Locator, expect } from "@playwright/test";

// BasePage - ALL pages extend this
export class BasePage {
  constructor(protected page: Page) {}

  async goto(path: string): Promise<void> {
    await this.page.goto(path);
    await this.page.waitForLoadState("networkidle");
  }

  async waitForNotification(): Promise<void> {
    await this.page.waitForSelector('[role="status"]');
  }
}

// Page-specific implementation
export interface LoginData {
  email: string;
  password: string;
}

export class LoginPage extends BasePage {
  readonly emailInput: Locator;
  readonly passwordInput: Locator;
  readonly submitButton: Locator;

  constructor(page: Page) {
    super(page);
    this.emailInput = page.getByLabel("Email");
    this.passwordInput = page.getByLabel("Password");
    this.submitButton = page.getByRole("button", { name: "Sign in" });
  }

  async goto(): Promise<void> {
    await super.goto("/login");
  }

  async login(data: LoginData): Promise<void> {
    await this.emailInput.fill(data.email);
    await this.passwordInput.fill(data.password);
    await this.submitButton.click();
  }
}
```

---

## Decision Tree

```
Need to click?             → Use getByRole or getByTestId
Need to type?              → Use getByLabel + fill()
Need to assert?            → Use expect() with locator
Need to wait?              → Auto-wait is built-in
Need reusable logic?       → Create Page Object
Need shared utilities?     → Add to helpers.ts
```

---

## Scope Detection (ASK IF AMBIGUOUS)

| User Says | Action |
|-----------|--------|
| "a test", "one test", "new test" | Create ONE test() in existing spec |
| "comprehensive tests", "all tests", "test suite" | Create full suite |

---

## Code Examples

### Test Pattern with Tags

```typescript
import { test, expect } from "@playwright/test";
import { LoginPage } from "./login-page";

test.describe("Login", () => {
  test("User can login successfully",
    { tag: ["@critical", "@e2e", "@login", "@LOGIN-E2E-001"] },
    async ({ page }) => {
      const loginPage = new LoginPage(page);
      await loginPage.goto();
      await loginPage.login({ email: "user@test.com", password: "pass123" });
      await expect(page).toHaveURL("/dashboard");
    }
  );
});
```

### Page Object Reuse

```typescript
// ✅ GOOD: Reuse existing page objects
import { SignInPage } from "../sign-in/sign-in-page";
import { HomePage } from "../home/home-page";

test("User can sign up and login", async ({ page }) => {
  const signUpPage = new SignUpPage(page);
  const signInPage = new SignInPage(page);  // REUSE
  const homePage = new HomePage(page);      // REUSE

  await signUpPage.signUp(userData);
  await homePage.signOut();
  await signInPage.login(credentials);
});
```

### Refactoring to BasePage

```typescript
// Move to BasePage when used by multiple pages:
export class BasePage {
  async waitForNotification(): Promise<void> {
    await this.page.waitForSelector('[role="status"]');
  }
}

// Move to helpers.ts for test data:
export function generateUniqueEmail(): string {
  return `test.${Date.now()}@example.com`;
}
```

---

## Commands

```bash
npx playwright test                    # Run all
npx playwright test --grep "login"     # Filter by name
npx playwright test --ui               # Interactive UI
npx playwright test --debug            # Debug mode
npx playwright codegen                 # Generate tests
npx playwright show-report             # View report
```

---

## Test Documentation Format

```markdown
### E2E Tests: {Feature Name}

**Suite ID:** `{SUITE-ID}`
**Priority:** `{critical|high|medium|low}`

**Tags:** @e2e, @{feature-name}

**Preconditions:**
- {Prerequisites}

### Flow Steps:
1. {Step 1}
2. {Step 2}

### Expected Result:
- {Expected outcome}
```

---

## Resources

- **Best Practices**: [best-practices.md](best-practices.md)
