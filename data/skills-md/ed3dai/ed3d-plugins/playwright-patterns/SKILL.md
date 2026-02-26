---
name: playwright-patterns
description: Use when writing Playwright automation code, building web scrapers, or creating E2E tests - provides best practices for selector strategies, waiting patterns, and robust automation that minimizes flakiness
user-invocable: false
---

# Playwright Automation Patterns

## Overview

Reliable browser automation requires strategic selector choice, proper waiting, and defensive coding. This skill provides patterns that minimize test flakiness and maximize maintainability.

## When to Use

- Writing new Playwright scripts or tests
- Debugging flaky automation
- Refactoring unreliable selectors
- Building web scrapers that need to handle dynamic content
- Creating E2E tests that must be maintainable

**When NOT to use:**
- Simple one-time browser tasks
- When you need Playwright API documentation (use context7 MCP)

## Selector Strategy

### Priority Order

Use user-facing locators first (most resilient), then test IDs, then CSS/XPath as last resort:

1. **Role-based locators** (best - user-centric)
   ```javascript
   await page.getByRole('button', { name: 'Submit' }).click();
   await page.getByRole('textbox', { name: 'Email' }).fill('test@example.com');
   ```

2. **Other user-facing locators**
   ```javascript
   await page.getByLabel('Password').fill('secret');
   await page.getByPlaceholder('Search...').fill('query');
   await page.getByText('Submit Order').click();
   ```

3. **Test ID attributes** (explicit contract)
   ```javascript
   // Default uses data-testid
   await page.getByTestId('submit-button').click();

   // Can customize in playwright.config.ts:
   // use: { testIdAttribute: 'data-pw' }
   ```

4. **CSS/ID selectors** (fragile, avoid if possible)
   ```javascript
   await page.locator('#submit-btn').click();
   await page.locator('.btn.btn-primary.submit').click();
   ```

### Strictness and Specificity

Locators are strict by default - operations throw if multiple elements match:

```javascript
// ERROR if 2+ buttons exist
await page.getByRole('button').click();

// Solutions:
// 1. Make locator more specific
await page.getByRole('button', { name: 'Submit' }).click();

// 2. Filter to narrow down
await page.getByRole('button')
  .filter({ hasText: 'Submit' })
  .click();

// 3. Chain locators to scope
await page.locator('.product-card')
  .getByRole('button', { name: 'Add to cart' })
  .click();

// Avoid: Using first() makes tests fragile
await page.getByRole('button').first().click(); // Don't do this
```

### Locator Filtering and Chaining

```javascript
// Filter by text content
await page.getByRole('listitem')
  .filter({ hasText: 'Product 2' })
  .getByRole('button')
  .click();

// Filter by child element
await page.getByRole('listitem')
  .filter({ has: page.getByRole('heading', { name: 'Product 2' }) })
  .getByRole('button', { name: 'Buy' })
  .click();

// Filter by NOT having text
await expect(
  page.getByRole('listitem')
    .filter({ hasNot: page.getByText('Out of stock') })
).toHaveCount(5);

// Handle "either/or" scenarios
const loginOrWelcome = await page.getByRole('button', { name: 'Login' })
  .or(page.getByText('Welcome back'))
  .first();
await expect(loginOrWelcome).toBeVisible();
```

### Anti-Patterns to Avoid

❌ **Fragile CSS paths**
```javascript
// BAD: Breaks when HTML structure changes
await page.click('div.container > div:nth-child(2) > button.submit');
```

✅ **Stable semantic selectors**
```javascript
// GOOD: Survives structural changes
await page.getByRole('button', { name: 'Submit' }).click();
```

❌ **XPath with positions**
```javascript
// BAD: Brittle
await page.locator('xpath=//div[3]/button[1]').click();
```

✅ **XPath with content**
```javascript
// BETTER: More stable
await page.locator('xpath=//button[contains(text(), "Submit")]').click();
```

## Waiting Patterns

### Built-in Auto-Waiting

Playwright auto-waits before most actions. Trust it.

```javascript
// Auto-waits for element to be visible, enabled, and stable
await page.click('button');
await page.fill('input[name="email"]', 'test@example.com');
```

**What auto-waiting checks:**
- Element is attached to DOM
- Element is visible
- Element is stable (not animating)
- Element is enabled
- Element receives events (not obscured)

```javascript
// Bypass checks (use with caution)
await page.click('button', { force: true });

// Test without acting (trial run)
await page.click('button', { trial: true });
```

### Web-First Assertions

Use web-first assertions - they retry until condition is met:

```javascript
// WRONG - no retry, immediate check
expect(await page.getByText('welcome').isVisible()).toBe(true);

// CORRECT - auto-retries until timeout
await expect(page.getByText('welcome')).toBeVisible();
await expect(page.getByText('Status')).toHaveText('Complete');
await expect(page.getByRole('listitem')).toHaveCount(5);

// Soft assertions - continue test even on failure
await expect.soft(page.getByTestId('status')).toHaveText('Success');
await page.getByRole('link', { name: 'next' }).click();
// Test continues, failures reported at end
```

### Explicit Waits for Dynamic Content

```javascript
// Wait for specific element (modern - use web-first assertions)
await expect(page.locator('.results-loaded')).toBeVisible();

// Wait for network to be idle
await page.waitForLoadState('networkidle');

// Wait for custom condition
await page.waitForFunction(() =>
  document.querySelectorAll('.item').length > 10
);
```

### Handling Asynchronous Updates

```javascript
// Known count - assert exact number
await expect(page.locator('.item')).toHaveCount(5);

// Unknown count - wait for container, then extract
await expect(page.locator('.search-results')).toBeVisible();
const items = await page.locator('.item').all();

// Loading spinner - wait for absence then presence
await expect(page.locator('.loading-spinner')).not.toBeVisible();
await expect(page.locator('.results')).toBeVisible();

// Wait for text content to appear
await expect(page.locator('.status')).toHaveText('Complete');

// At least one result (reject zero results)
await expect(page.locator('.item').first()).toBeVisible();
```

## Data Extraction Patterns

### Single Element

```javascript
// textContent() - Gets all text including hidden elements
const title = await page.locator('h1').textContent();

// innerText() - Gets only visible text (respects CSS display)
const price = await page.locator('.price').innerText();

// getAttribute() - Get attribute value
const href = await page.locator('a.product').getAttribute('href');

// For assertions, prefer web-first assertions
await expect(page.locator('.price')).toHaveText('$99');
```

### Multiple Elements

```javascript
// IMPORTANT: locator.all() doesn't wait for elements
// This can be flaky if list is still loading

// Known count - assert first, then extract
await expect(page.locator('.item')).toHaveCount(5);
const items = await page.locator('.item').all();
const data = await Promise.all(
  items.map(async item => ({
    title: await item.locator('.title').textContent(),
    price: await item.locator('.price').textContent(),
  }))
);

// Unknown count - wait for container, then extract
await expect(page.locator('.results-container')).toBeVisible();
const data = await page.locator('.item').evaluateAll(items =>
  items.map(el => ({
    title: el.querySelector('.title')?.textContent?.trim(),
    price: el.querySelector('.price')?.textContent?.trim(),
  }))
);

// BEST: Use evaluateAll for batch extraction (single round-trip)
// Use when: extracting from locator-scoped elements (most common)
const data = await page.locator('.item').evaluateAll(items =>
  items.map(el => ({
    title: el.querySelector('.title')?.textContent?.trim(),
    price: el.querySelector('.price')?.textContent?.trim(),
  }))
);
```

### Complex Extraction with evaluate()

```javascript
// Use evaluate() when you need global page context
// (e.g., checking window variables, document state)
const data = await page.evaluate(() => {
  return {
    items: Array.from(document.querySelectorAll('.item')).map(el => ({
      title: el.querySelector('.title')?.textContent?.trim(),
      price: el.querySelector('.price')?.textContent?.trim(),
      url: el.querySelector('a')?.href,
      available: !el.classList.contains('out-of-stock')
    })),
    totalCount: window.productCount, // Access global variables
    filters: window.appliedFilters   // Page-level state
  };
});

// Prefer evaluateAll() for locator-scoped extraction (more focused)
const items = await page.locator('.item').evaluateAll(els =>
  els.map(el => ({ /* ... */ }))
);
```

## Error Handling

### Graceful Fallbacks

```javascript
// Check if element exists before interacting
const cookieBanner = page.locator('.cookie-banner');
if (await cookieBanner.isVisible()) {
  await cookieBanner.getByRole('button', { name: 'Accept' }).click();
}
```

### Retry Logic

```javascript
// Playwright retries automatically, but you can customize
await expect(async () => {
  const status = await page.locator('.status').textContent();
  expect(status).toBe('Complete');
}).toPass({ timeout: 10000, intervals: [1000] });
```

### Timeout Configuration

```javascript
// Set timeout for specific action
await page.click('button', { timeout: 5000 });

// Set timeout for entire test
test.setTimeout(60000);

// Set default timeout for page
page.setDefaultTimeout(10000);
```

## Navigation Patterns

### Wait for Navigation

```javascript
// Modern pattern - click auto-waits for navigation
await page.click('a.next-page');
await page.waitForLoadState('networkidle'); // Only if needed

// Using modern locator
await page.getByRole('link', { name: 'Next Page' }).click();
```

### Multi-Page Workflows

```javascript
// Open new tab
const [newPage] = await Promise.all([
  context.waitForEvent('page'),
  page.click('a[target="_blank"]')
]);

await newPage.waitForLoadState();
// Work with newPage
await newPage.close();
```

## Form Interaction Patterns

### Basic Form Filling

```javascript
// fill() - Recommended for most inputs (fast, atomic operation)
await page.fill('input[name="email"]', 'user@example.com');
await page.fill('input[name="password"]', 'secret123');

// type() - For keystroke-sensitive inputs (slower, fires each key event)
await page.locator('input.search').type('Product', { delay: 100 });

// Modern approach with role-based locators
await page.getByLabel('Email').fill('user@example.com');
await page.getByLabel('Password').fill('secret123');
await page.getByRole('combobox', { name: 'Country' }).selectOption('US');
await page.getByRole('checkbox', { name: 'I agree' }).check();
await page.getByRole('button', { name: 'Submit' }).click();
```

### File Uploads

```javascript
await page.setInputFiles('input[type="file"]', '/path/to/file.pdf');

// Multiple files
await page.setInputFiles('input[type="file"]', [
  '/path/to/file1.pdf',
  '/path/to/file2.pdf'
]);
```

### Autocomplete/Search Inputs

```javascript
// Type and wait for suggestions (modern approach)
await page.getByPlaceholder('Search products').fill('Product Name');
await expect(page.locator('.suggestions')).toBeVisible();

// Click specific suggestion using role-based locator
await page.getByRole('option', { name: 'Product Name - Premium' }).click();

// Or filter suggestions
await page.locator('.suggestions')
  .getByText('Product Name', { exact: false })
  .first()
  .click();
```

## Screenshot and Debugging

### Strategic Screenshots

```javascript
// Full page screenshot
await page.screenshot({ path: 'screenshot.png', fullPage: true });

// Element screenshot
await page.locator('.chart').screenshot({ path: 'chart.png' });

// Screenshot on failure (in test)
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== testInfo.expectedStatus) {
    await page.screenshot({
      path: `failure-${testInfo.title}.png`,
      fullPage: true
    });
  }
});
```

### Debug Mode

```javascript
// Pause execution for debugging
await page.pause();

// Slow down actions for observation
const browser = await chromium.launch({ slowMo: 1000 });
```

## Common Patterns Reference

| Task | Pattern |
|------|---------|
| Click button | `await page.getByRole('button', { name: 'Text' }).click()` |
| Fill input | `await page.getByLabel('Field').fill('value')` |
| Select option | `await page.getByRole('combobox').selectOption('value')` |
| Check checkbox | `await page.getByRole('checkbox', { name: 'Label' }).check()` |
| Wait for element | `await expect(page.locator('.el')).toBeVisible()` |
| Assert text | `await expect(page.locator('.el')).toHaveText('text')` |
| Extract text | `const text = await page.locator('.el').textContent()` |
| Extract multiple | `await expect(locator).toHaveCount(5); const els = await locator.all()` |
| Batch extract | `const data = await page.locator('.el').evaluateAll(els => ...)` |
| Run JS in page | `await page.evaluate(() => /* JS code */)` |
| Take screenshot | `await page.screenshot({ path: 'shot.png' })` |
| Handle new tab | `const newPage = await context.waitForEvent('page', () => page.click('a'))` |

## Anti-Pattern Checklist

Avoid these common mistakes:

- ❌ Using `page.waitForTimeout(5000)` instead of web-first assertions
- ❌ Using CSS class names or nth-child selectors instead of role-based locators
- ❌ Using `expect(await locator.isVisible()).toBe(true)` instead of `await expect(locator).toBeVisible()`
- ❌ Using deprecated `waitForNavigation()` - clicks auto-wait now
- ❌ Using `locator.all()` without asserting count first
- ❌ Using `first()` when locator should be more specific
- ❌ Not handling popups or cookie banners
- ❌ Hardcoding delays instead of waiting for conditions
- ❌ Taking screenshots for data extraction (use evaluate instead)

## Remember

**Robust automation priorities:**
1. **User-facing locators first** - Role, label, placeholder, text (not CSS)
2. **Web-first assertions** - `await expect(locator).toBeVisible()` not `expect(await ...)`
3. **Trust auto-waiting** - Don't add manual delays or deprecated patterns
4. **Strictness is your friend** - Fix ambiguous locators, don't use `first()`
5. **Batch extraction wisely** - Assert count before `all()`, use `evaluateAll()` for efficiency

Browser automation is inherently asynchronous and timing-dependent. Build in resilience from the start.
