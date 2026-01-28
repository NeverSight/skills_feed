---
name: testing-e2e
description: Expert guidance for writing resilient end-to-end tests that span multiple processes and components. Use this skill when reviewing, writing, or refactoring system-wide e2e tests. Covers user-facing scenarios, helper functions, data factories, ARIA-based selectors, and auto-retriable assertions. NOT for unit/integration tests - use testing-unit-integration skill instead. See references/playwright-resilience.md for detailed selector patterns.
---

# End-to-End Testing Best Practices

Expert guidance for system-wide e2e tests spanning multiple processes.

**Scope:** System-wide end-to-end tests only. NOT for unit, integration, or component tests with mocked backends - use `testing-unit-integration` skill instead.

**Note:** E2E tests are complex, slow, and limited in quantity - relaxed readability standards and less stringent best practices are acceptable compared to unit tests.

## Core Rules

### Self-Contained Tests (Critical)

- **A.8** Each test is self-contained, never relies on other tests' state or artifacts
- **A.11** Start with fresh dedicated data created in beforeEach or during test
- **A.14** Test real user scenarios, simulate actual user behavior
- **A.35** Implement comprehensive test data management with automatic cleanup

### User-Facing Locators (Critical)

- **A.17** Only ARIA-based locators: `getByRole`, `getByLabel`, `getByText`
- **A.17** NO CSS selectors, test IDs, xpath, $, or implementation-specific locators
- **A.40** No positional selectors: nth(i), first(), last()

### Boundaries

- **A.23** Only visit and test within application boundaries
- **A.48** Don't approach or assert on external systems - assert navigation happened

### Structure

- **A.5** Title summarizes flow with stakeholder, action, expectations
- **A.26** Max 15 statements - encapsulate multi-step operations in helper functions

## Helper Functions Pattern

Each helper represents a meaningful part of user's journey, not low-level interactions:

```typescript
// ✅ GOOD - Semantic helpers
async function loginAsAdmin(page: Page): Promise<void>
async function addProductToCart(page: Page, product: Product): Promise<void>
async function completeCheckout(page: Page): Promise<OrderDetails>
async function verifyOrderConfirmationEmailSent(email: string, order: OrderDetails): Promise<void>

// ❌ BAD - Low-level interactions exposed
async function clickButton(page: Page, name: string): Promise<void>
async function fillInput(page: Page, selector: string, value: string): Promise<void>
```

## Waiting Strategies

- **A.44** No time-based waiting: `setTimeout`, `page.waitForTimeout()`
- **A.44** No `waitForSelector` - couples test to implementation
- **A.20** Use auto-retriable assertions (web-first assertions):

```typescript
// ❌ BAD
await page.waitForTimeout(3000)
await page.waitForSelector('.form-loaded')

// ✅ GOOD - Auto-retriable assertions
await expect(page.getByText(/success/i)).toBeVisible()
await expect(page).toHaveURL(/\/dashboard/)
```

## Data Factories

- **A.52** Data from factory files with `buildEntity()` functions
- **A.52** Factories return defaults but allow field overrides
- **A.55** Use meaningful domain data with faker, not dummy values

```typescript
import { faker } from "@faker-js/faker";
import { Customer } from "../types";

export function buildCustomer(overrides: Partial<Customer> = {}): Customer {
  return {
    email: faker.internet.email(),
    name: faker.person.fullName(),
    address: faker.location.streetAddress(),
    ...overrides,
  };
}
```

## Assertions

- **A.58** No custom coding, loops, Array.prototype - use built-in expect APIs
- **A.62** Minimal assertions - one strong assertion catches all issues
- **A.65** Use matchers that show full diff on failure

### Strong Assertions

```typescript
// ❌ WEAK - Multiple redundant assertions
expect(response).not.toBeNull()
expect(Array.isArray(response)).toBe(true)
expect(response.length).toBe(2)

// ✅ STRONG - Single assertion catches all
expect(response).toEqual([{id: '123'}, {id: '456'}])
```

## Navigation Testing

E2E tests catch navigation bugs that mocked unit/integration tests miss.

- **A.50** Assert navigation OUTCOME (destination page renders), not that navigate() was called
- **A.52** Test router config must match production router - use real routes, not mocked
- **A.54** Use route constants, not hardcoded path strings - prevents typos and drift
- **A.56** Verify URL changed to expected value after navigation actions
- **A.58** E2E tests are the safety net - they catch contract and navigation bugs that mocked tests miss

```typescript
// ❌ BAD - Testing that navigate function was called (implementation detail)
expect(mockNavigate).toHaveBeenCalledWith('/users/123');

// ❌ BAD - Hardcoded path string (typos won't be caught)
await page.goto('/usres/123');  // Typo! Would fail silently in unit test

// ✅ GOOD - Assert the OUTCOME (user sees the page)
await expect(page.getByRole('heading', { name: /user profile/i })).toBeVisible();

// ✅ GOOD - Verify URL changed
await expect(page).toHaveURL(/\/users\/\d+/);

// ✅ GOOD - Use route constants (from shared constants file)
import { ROUTES } from '@/constants/routes';
await page.goto(ROUTES.USER_PROFILE.replace(':id', '123'));
```

### Why E2E Catches What Unit Tests Miss

| Bug Type | Unit Test (Mocked) | E2E Test |
|----------|-------------------|----------|
| Route typo in navigate('/usres') | ❌ Passes (mock doesn't validate) | ✅ Fails (404 page) |
| Route param mismatch (email vs id) | ❌ Passes (mock accepts anything) | ✅ Fails (wrong page loads) |
| Missing route in router config | ❌ Passes (mock doesn't use router) | ✅ Fails (404 or error) |
| Backend contract change | ❌ Passes (mock returns fantasy data) | ✅ Fails (real API different) |

## Maximum Coverage, Minimal Tests

E2E tests are expensive - maximize value per test:
- Each test covers a complete user journey
- Combine verification steps that belong to same flow
- Focus on critical paths and high-risk scenarios
- Use helper functions to keep tests readable despite complexity

## BAD E2E Test Example

```typescript
test('Should purchase item', async ({ page }) => { // ❌ A.5 - vague title
  await page.goto('/products') // ❌ A.8, A.11 - assumes existing session

  await page.getByText('iPhone 15 Pro').click() // ❌ A.8 - assumes specific product
  await page.locator('#add-to-cart-btn').click() // ❌ A.17 - CSS selector
  await page.goto('/checkout')

  await page.waitForSelector('.form-loaded') // ❌ A.44 - implementation detail
  await page.locator('#email').fill('foo@test.com') // ❌ A.17, A.55 - CSS + dummy data
  await page.locator('button').last().click() // ❌ A.17, A.40 - positional

  const cartItems = await page.locator('.cart-item').all() // ❌ A.58 - custom loop
  for (const item of cartItems) expect(await item.isVisible()).toBe(true) // ❌ A.58

  await page.goto('https://stripe.com/confirm') // ❌ A.23 - external system
  expect(await page.evaluate(() => localStorage.getItem('orderId'))).toBeTruthy() // ❌ A.14 - implementation
})
```

## GOOD E2E Test Example

```typescript
test('The user can purchase an item and post-purchase experience is valid', async ({ page }) => {
  // Arrange - Create fresh test data
  const customer = await saveNewCustomer(buildCustomer())
  const product = await saveNewProduct(buildProduct())

  // Act - User journey through semantic helpers
  await navigateToProductsPage(page)
  await selectProduct(page, product)
  await goToCheckout(page)
  await fillCustomerDetails(page, customer)
  await fillPaymentDetails(page, buildCreditCard())

  // Assert - Verify outcomes
  const orderDetails = await submitOrderAndVerifySuccessPage(page)
  await verifyOrderConfirmationEmailSent(customer.email, orderDetails)
  await verifySupplyRequestWasCreated(customer.email, orderDetails)
})
```

## Selector Reference

For detailed selector patterns, page object best practices, and resilience strategies, see:

**`references/playwright-resilience.md`** - Comprehensive guide including:
- Selector priority table (getByRole > getByLabel > getByPlaceholder...)
- Bad vs Good patterns for forms, buttons, headings, waiting
- When to use data-testid (error messages, toasts, loading indicators)
- Page Object best practices
- Text matching strategies (regex, partial, exact)
- Quick reference for all element types

## Rule Violation Reporting

When reviewing e2e tests, report violations as:
```
Line X: Violates [RULE_NUMBER] - [Brief explanation]
```

Example:
```
Line 8: Violates A.17 - Uses CSS selector '#email', should use getByLabel('Email')
Line 12: Violates A.44 - Uses waitForTimeout, should use auto-retriable assertion
Line 15: Violates A.23 - Navigates to external domain stripe.com
```
