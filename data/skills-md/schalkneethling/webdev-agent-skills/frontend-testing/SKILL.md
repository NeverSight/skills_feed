---
name: frontend-testing
description: Write tests that start with acceptance criteria, then add implementation tests for robustness. Use when writing unit tests (Vitest), end-to-end tests (Playwright), visual regression tests, or accessibility tests. Emphasizes user-centric testing, semantic locators, accessibility validation, and the balance between acceptance and implementation testing.
---

# Frontend Testing

Start by writing tests that validate acceptance criteria. Then add implementation tests where they provide value.

## Core Principle

> "The more your tests resemble the way your software is used, the more confidence they can give you." — Kent C. Dodds

This principle guides testing decisions, but isn't the whole picture:

- **Acceptance criteria tests** verify the system does what users/stakeholders need. These should be stable across refactors.
- **Implementation tests** verify the pieces are robust — edge cases, error handling, complex logic. These may change when you refactor.

Both have value. The anti-pattern to avoid is tests that *only* mirror implementation without validating meaningful behavior.

## When to Load References

Load reference files based on test type:

- **Unit tests with DOM**: `references/locator-strategies.md`
- **E2E tests**: `references/locator-strategies.md`, `references/aria-snapshots.md`
- **Visual regression tests**: `references/visual-regression.md`
- **Accessibility audits**: `references/accessibility-testing.md`
- **Structure validation**: `references/aria-snapshots.md` — consolidate multiple assertions into one
- **All tests**: Start with this file for core workflow

## Workflow

### Step 1: Start with Acceptance Criteria

Before writing any test, identify what the code should do from the user's perspective.

Ask for or extract criteria from:
- Ticket description or user story
- Figma annotations
- Functional requirements
- Product owner clarification

Document criteria as a checklist. These become your first tests.

**Write acceptance tests before reading implementation.** This prevents circular validation where tests just confirm "code does what code does."

### Step 2: Map Criteria to Test Cases

For each criterion, identify:
- **Happy path**: Normal expected behavior
- **Edge cases**: Boundary conditions
- **Error cases**: Invalid inputs, failures

Example mapping:
```
Criterion: "User can filter products by category"
├─ Happy path: Select category, products filter correctly
├─ Edge case: No products match filter, show empty state
├─ Edge case: Clear filter, all products show again
├─ Error case: Filter API fails, show error message
└─ Accessibility: Filter controls are keyboard accessible
```

### Step 3: Add Implementation Tests (Unit Tests)

After acceptance tests pass, add unit tests for implementation robustness:

- **Edge cases** the criteria don't cover (null, undefined, empty arrays, boundary values)
- **Algorithm correctness** for complex calculations
- **Error handling paths** (exceptions, network failures, parse errors)
- **Complex branching logic** hard to exercise through integration tests
- **Performance-sensitive code** that needs specific validation

```
Function: filterProducts(products, category)
├─ Acceptance: Returns matching products (from criteria)
├─ Implementation: Returns empty array when products is null
├─ Implementation: Returns all products when category is empty string
├─ Implementation: Handles case-insensitive category matching
└─ Implementation: Does not mutate original array
```

The distinction: acceptance tests should rarely change on refactor; implementation tests may need updates when internals change.

### Step 4: Choose Test Type

| Scenario | Test Type | Tool |
|----------|-----------|------|
| Pure logic (no DOM) | Unit test | Vitest |
| Component behavior | Unit test with DOM | Vitest + Testing Library |
| User flows, real browser | E2E test | Playwright |
| Semantic structure validation | ARIA snapshot | Playwright `toMatchAriaSnapshot` |
| Visual appearance | VRT | Playwright screenshots |
| Accessibility compliance | A11y test | Playwright + axe-core |

**ARIA snapshots** are particularly valuable for E2E tests. A single snapshot can replace multiple individual assertions while validating the accessibility tree structure.

**DOM Environment for Unit Tests:** Prefer happy-dom over jsdom. It's faster, and its API limitations serve as a useful signal — if happy-dom doesn't support what you're testing, consider whether it belongs in an E2E test instead.

### Step 5: Write Tests Before/Alongside Code

- **Ideal**: Write test first, then implementation (TDD)
- **Acceptable**: Write test immediately after implementing each criterion
- **Avoid**: Write all tests after implementation is "done"

## Test Structure

### Unit Tests (Vitest)

```javascript
describe("calculateDiscount", () => {
  describe("when customer has premium membership", () => {
    it("applies 20% discount to order total", () => {
      // Arrange - Set up test data matching criterion
      const order = { total: 100, membership: "premium" };
      
      // Act - Call the function
      const result = calculateDiscount(order);
      
      // Assert - Verify expected outcome from requirements
      expect(result).toBe(80);
    });
  });
});
```

### Component Tests (Vitest + Testing Library)

```javascript
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

describe("LoginForm", () => {
  describe("when credentials are invalid", () => {
    it("displays error message to user", async () => {
      const user = userEvent.setup();
      render(<LoginForm />);
      
      // Interact using accessible queries
      await user.type(
        screen.getByLabelText(/email/i),
        "invalid@test.com"
      );
      await user.type(
        screen.getByLabelText(/password/i),
        "wrong"
      );
      await user.click(
        screen.getByRole("button", { name: /sign in/i })
      );
      
      // Assert on user-visible outcome
      expect(
        await screen.findByRole("alert")
      ).toHaveTextContent(/invalid credentials/i);
    });
  });
});
```

### E2E Tests (Playwright)

```javascript
import { test, expect } from "@playwright/test";

test.describe("Product Catalog", () => {
  test.describe("filtering by category", () => {
    test("shows only matching products", async ({ page }) => {
      await page.goto("/products");
      
      // Use semantic locators
      await page.getByRole("combobox", { name: /category/i }).selectOption("Electronics");
      
      // Assert count, then spot-check first/last
      const products = page.getByRole("article");
      await expect(products).toHaveCount(5);
      await expect(products.first()).toContainText(/electronics/i);
      await expect(products.last()).toContainText(/electronics/i);
    });
  });
});
```

When you need to verify all items, use `Promise.all` for parallel assertions:

```javascript
test("all products match filter", async ({ page }) => {
  await page.goto("/products");
  await page.getByRole("combobox", { name: /category/i }).selectOption("Electronics");
  
  const products = await page.getByRole("article").all();
  
  // Parallel assertions — faster than sequential await in a loop
  await Promise.all(
    products.map(product =>
      expect(product.getByText(/electronics/i)).toBeVisible()
    )
  );
});
```

### E2E Tests with ARIA Snapshots

ARIA snapshots consolidate multiple assertions into one, validating semantic structure:

```javascript
test.describe("Login Page", () => {
  test("has correct form structure", async ({ page }) => {
    await page.goto("/login");
    
    // One snapshot replaces 5+ individual assertions
    await expect(page.getByRole("main")).toMatchAriaSnapshot(`
      - heading "Sign In" [level=1]
      - textbox "Email"
      - textbox "Password"
      - button "Sign In"
      - link "Forgot password?"
    `);
  });
  
  test("shows validation errors on empty submit", async ({ page }) => {
    await page.goto("/login");
    await page.getByRole("button", { name: /sign in/i }).click();
    
    await expect(page.getByRole("form")).toMatchAriaSnapshot(`
      - textbox "Email"
      - text "Email is required"
      - textbox "Password"
      - text "Password is required"
      - button "Sign In"
    `);
  });
});
```

## Locator Priority

Use locators that reflect how users and assistive technologies find elements:

1. **`getByRole`** — First choice. Queries accessibility tree.
2. **`getByLabelText`** — Best for form fields. Users find inputs by labels.
3. **`getByPlaceholderText`** — When no label exists (not ideal).
4. **`getByText`** — For non-interactive elements.
5. **`getByAltText`** — For images.
6. **`getByTestId`** — Last resort escape hatch.

If you can't find an element with semantic queries, the UI may have accessibility issues.

## Anti-Patterns

### Testing Only Implementation Details

Tests that only verify internals without validating meaningful behavior:

```javascript
// BAD: Tests internal method exists, provides no behavior guarantee
it("has a validateFields method", () => {
  expect(form.#validateFields).toBeDefined();
});

// BAD: Asserts implementation without verifying outcome
it("calls the validator", () => {
  expect(mockValidator).toHaveBeenCalledWith(data);
});

// GOOD: Tests observable behavior (acceptance)
it("prevents submission with invalid email", async () => {
  await user.type(emailInput, "not-an-email");
  await user.click(submitButton);
  expect(screen.getByRole("alert")).toHaveTextContent(/valid email/i);
});

// ALSO GOOD: Tests implementation robustness (unit)
it("returns validation errors for malformed email", () => {
  const result = validateEmail("not-an-email");
  expect(result.valid).toBe(false);
  expect(result.error).toBe("Invalid email format");
});
```

The key distinction: implementation tests should verify *meaningful* behavior of units, not just that code paths execute.

### Circular Validation

```javascript
// BAD: Test data derived from implementation
const expected = formatPrice(100); // Don't compute expected from code!
expect(formatPrice(100)).toBe(expected);

// GOOD: Expected value from requirements
expect(formatPrice(100)).toBe("$100.00");
```

### Over-Mocking

```javascript
// BAD: Mock everything, test nothing real
jest.mock("./api");
jest.mock("./utils");
jest.mock("./formatter");
// Now just testing mocks talk to each other

// GOOD: Mock only external boundaries
// Mock: APIs, databases, time, file system
// Real: Business logic, components, formatters
```

### Brittle Selectors

```javascript
// BAD: Implementation-dependent selectors
page.locator(".btn-primary.submit-form");
page.locator("#root > div > form > button:nth-child(3)");

// GOOD: Semantic locators
page.getByRole("button", { name: /submit order/i });
```

## Failing Tests Mean Bugs (Usually)

When a test fails, the investigation depends on the test type:

**Acceptance test fails:**
1. Check the code under test first — likely a real bug
2. Verify the test still matches current requirements — requirements may have changed
3. Only update the test after confirming the new behavior is correct

**Implementation test fails:**
1. If you're refactoring, the test may legitimately need updating
2. If you're not refactoring, check the code — likely a bug
3. Consider whether the test is too tightly coupled to implementation

Don't reflexively update tests to pass. Investigate why they fail.

## Checklist Before Submitting Tests

- [ ] Each acceptance criterion has at least one test
- [ ] Edge cases from criteria are covered
- [ ] Implementation tests added for complex logic, error handling, boundary conditions
- [ ] Tests are named descriptively (criteria-based or behavior-based)
- [ ] Using semantic locators (getByRole, getByLabelText)
- [ ] No tests that only verify "code runs" without validating meaningful behavior
- [ ] Failing tests investigated appropriately (acceptance vs implementation)
- [ ] Accessibility checks included for interactive components
- [ ] Consider ARIA snapshots for structure validation (consolidates multiple assertions)

## References

Load these files for detailed guidance:

- `references/locator-strategies.md` — Complete locator hierarchy with examples
- `references/aria-snapshots.md` — Structure validation, consolidating assertions
- `references/accessibility-testing.md` — axe-core integration, WCAG targeting
- `references/visual-regression.md` — Screenshot testing, baseline management
