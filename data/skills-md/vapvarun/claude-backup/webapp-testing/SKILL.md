---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using Playwright. Supports verifying frontend functionality, debugging UI behavior, capturing browser screenshots, and viewing browser logs.
---

# Web Application Testing with Playwright

Comprehensive E2E testing patterns for web applications.

## Quick Start

### Python Setup

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://localhost:3000')
    page.wait_for_load_state('networkidle')
    # ... test logic
    browser.close()
```

### JavaScript/TypeScript Setup

```typescript
import { test, expect } from '@playwright/test';

test('example test', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page.locator('h1')).toContainText('Welcome');
});
```

## Server Management

### Using Helper Scripts

**Single server:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_test.py
```

**Multiple servers:**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_test.py
```

### Playwright Config (playwright.config.ts)

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
    screenshot: 'only-on-failure',
  },

  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'Mobile Chrome', use: { ...devices['Pixel 5'] } },
    { name: 'Mobile Safari', use: { ...devices['iPhone 12'] } },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
```

## Selectors

### Best Practices

```typescript
// BEST: Test IDs (most reliable)
page.locator('[data-testid="submit-button"]')
page.getByTestId('submit-button')

// GOOD: Role-based (accessible)
page.getByRole('button', { name: 'Submit' })
page.getByRole('heading', { level: 1 })
page.getByRole('link', { name: 'Learn more' })

// GOOD: Label-based (forms)
page.getByLabel('Email address')
page.getByPlaceholder('Enter your email')

// GOOD: Text content
page.getByText('Welcome back')
page.getByText(/welcome/i) // Case-insensitive regex

// AVOID: CSS selectors (brittle)
page.locator('.btn-primary') // Class might change
page.locator('#submit') // ID might change
```

### Selector Chaining

```typescript
// Find within a container
const form = page.locator('form[data-testid="login-form"]');
await form.getByLabel('Email').fill('user@example.com');
await form.getByRole('button', { name: 'Log in' }).click();

// Filter results
await page.getByRole('listitem')
  .filter({ hasText: 'Product 1' })
  .getByRole('button', { name: 'Add to cart' })
  .click();
```

## Common Test Patterns

### Authentication Flow

```typescript
import { test, expect } from '@playwright/test';

test.describe('Authentication', () => {
  test('successful login', async ({ page }) => {
    await page.goto('/login');

    await page.getByLabel('Email').fill('user@example.com');
    await page.getByLabel('Password').fill('password123');
    await page.getByRole('button', { name: 'Log in' }).click();

    // Verify redirect to dashboard
    await expect(page).toHaveURL('/dashboard');
    await expect(page.getByText('Welcome back')).toBeVisible();
  });

  test('invalid credentials show error', async ({ page }) => {
    await page.goto('/login');

    await page.getByLabel('Email').fill('wrong@example.com');
    await page.getByLabel('Password').fill('wrongpassword');
    await page.getByRole('button', { name: 'Log in' }).click();

    await expect(page.getByText('Invalid credentials')).toBeVisible();
    await expect(page).toHaveURL('/login'); // Still on login page
  });

  test('logout', async ({ page }) => {
    // Login first (or use authenticated state)
    await page.goto('/dashboard');
    await page.getByRole('button', { name: 'Logout' }).click();

    await expect(page).toHaveURL('/login');
  });
});
```

### Form Submission

```typescript
test.describe('Contact Form', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/contact');
  });

  test('submits form with valid data', async ({ page }) => {
    await page.getByLabel('Name').fill('John Doe');
    await page.getByLabel('Email').fill('john@example.com');
    await page.getByLabel('Message').fill('This is a test message');
    await page.getByRole('button', { name: 'Send' }).click();

    await expect(page.getByText('Message sent successfully')).toBeVisible();
  });

  test('shows validation errors for empty fields', async ({ page }) => {
    await page.getByRole('button', { name: 'Send' }).click();

    await expect(page.getByText('Name is required')).toBeVisible();
    await expect(page.getByText('Email is required')).toBeVisible();
  });

  test('validates email format', async ({ page }) => {
    await page.getByLabel('Name').fill('John');
    await page.getByLabel('Email').fill('invalid-email');
    await page.getByRole('button', { name: 'Send' }).click();

    await expect(page.getByText('Invalid email address')).toBeVisible();
  });
});
```

### Navigation Testing

```typescript
test.describe('Navigation', () => {
  test('main menu links work', async ({ page }) => {
    await page.goto('/');

    // Test each navigation link
    const navLinks = [
      { name: 'Home', url: '/' },
      { name: 'About', url: '/about' },
      { name: 'Products', url: '/products' },
      { name: 'Contact', url: '/contact' },
    ];

    for (const link of navLinks) {
      await page.getByRole('link', { name: link.name }).click();
      await expect(page).toHaveURL(link.url);
    }
  });

  test('breadcrumbs show correct path', async ({ page }) => {
    await page.goto('/products/category/item-1');

    const breadcrumbs = page.getByRole('navigation', { name: 'Breadcrumb' });
    await expect(breadcrumbs.getByText('Home')).toBeVisible();
    await expect(breadcrumbs.getByText('Products')).toBeVisible();
    await expect(breadcrumbs.getByText('Category')).toBeVisible();
  });
});
```

### CRUD Operations

```typescript
test.describe('Product Management', () => {
  test('creates new product', async ({ page }) => {
    await page.goto('/admin/products');
    await page.getByRole('button', { name: 'Add Product' }).click();

    await page.getByLabel('Name').fill('New Product');
    await page.getByLabel('Price').fill('29.99');
    await page.getByLabel('Description').fill('Product description');
    await page.getByRole('button', { name: 'Save' }).click();

    await expect(page.getByText('Product created')).toBeVisible();
    await expect(page.getByText('New Product')).toBeVisible();
  });

  test('edits existing product', async ({ page }) => {
    await page.goto('/admin/products');

    // Find product row and click edit
    await page.getByRole('row', { name: /Existing Product/ })
      .getByRole('button', { name: 'Edit' })
      .click();

    await page.getByLabel('Name').fill('Updated Product');
    await page.getByRole('button', { name: 'Save' }).click();

    await expect(page.getByText('Product updated')).toBeVisible();
    await expect(page.getByText('Updated Product')).toBeVisible();
  });

  test('deletes product with confirmation', async ({ page }) => {
    await page.goto('/admin/products');

    // Click delete button
    await page.getByRole('row', { name: /Product to Delete/ })
      .getByRole('button', { name: 'Delete' })
      .click();

    // Handle confirmation dialog
    await page.getByRole('button', { name: 'Confirm' }).click();

    await expect(page.getByText('Product deleted')).toBeVisible();
    await expect(page.getByText('Product to Delete')).not.toBeVisible();
  });
});
```

### Modal/Dialog Testing

```typescript
test.describe('Modal Dialogs', () => {
  test('opens and closes modal', async ({ page }) => {
    await page.goto('/');

    // Open modal
    await page.getByRole('button', { name: 'Open Modal' }).click();
    await expect(page.getByRole('dialog')).toBeVisible();

    // Close with X button
    await page.getByRole('button', { name: 'Close' }).click();
    await expect(page.getByRole('dialog')).not.toBeVisible();
  });

  test('closes modal on escape key', async ({ page }) => {
    await page.goto('/');

    await page.getByRole('button', { name: 'Open Modal' }).click();
    await expect(page.getByRole('dialog')).toBeVisible();

    await page.keyboard.press('Escape');
    await expect(page.getByRole('dialog')).not.toBeVisible();
  });

  test('closes modal on backdrop click', async ({ page }) => {
    await page.goto('/');

    await page.getByRole('button', { name: 'Open Modal' }).click();
    await expect(page.getByRole('dialog')).toBeVisible();

    // Click outside modal
    await page.locator('.modal-backdrop').click({ position: { x: 10, y: 10 } });
    await expect(page.getByRole('dialog')).not.toBeVisible();
  });
});
```

## Waiting Strategies

### Explicit Waits

```typescript
// Wait for element
await page.waitForSelector('[data-testid="content"]');

// Wait for element state
await page.getByRole('button').waitFor({ state: 'visible' });
await page.getByRole('button').waitFor({ state: 'hidden' });

// Wait for navigation
await page.waitForURL('/dashboard');
await page.waitForURL(/\/user\/\d+/);

// Wait for network
await page.waitForResponse('/api/users');
await page.waitForResponse(response =>
  response.url().includes('/api/') && response.status() === 200
);

// Wait for load state
await page.waitForLoadState('networkidle');
await page.waitForLoadState('domcontentloaded');
```

### Auto-Waiting

```typescript
// Playwright auto-waits for these
await page.click('button'); // Waits for button to be actionable
await page.fill('input', 'text'); // Waits for input to be editable
await expect(locator).toBeVisible(); // Waits up to timeout
```

## Assertions

### Common Assertions

```typescript
// Visibility
await expect(locator).toBeVisible();
await expect(locator).toBeHidden();
await expect(locator).not.toBeVisible();

// Text content
await expect(locator).toHaveText('exact text');
await expect(locator).toContainText('partial');
await expect(locator).toHaveText(/regex/i);

// Attributes
await expect(locator).toHaveAttribute('href', '/about');
await expect(locator).toHaveClass(/active/);
await expect(locator).toHaveId('main-content');

// Input values
await expect(locator).toHaveValue('input value');
await expect(locator).toBeChecked();
await expect(locator).toBeDisabled();
await expect(locator).toBeEditable();

// Count
await expect(locator).toHaveCount(5);

// Page assertions
await expect(page).toHaveURL('/dashboard');
await expect(page).toHaveTitle('Dashboard | My App');
```

### Soft Assertions

```typescript
// Continue test even if assertion fails
await expect.soft(locator).toHaveText('text');
await expect.soft(locator).toBeVisible();

// Check all soft assertions at end
expect(test.info().errors).toHaveLength(0);
```

## API Testing Integration

### Mock API Responses

```typescript
test('shows loading and data states', async ({ page }) => {
  // Intercept API request
  await page.route('/api/users', async route => {
    await route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify([
        { id: 1, name: 'John' },
        { id: 2, name: 'Jane' },
      ]),
    });
  });

  await page.goto('/users');
  await expect(page.getByText('John')).toBeVisible();
  await expect(page.getByText('Jane')).toBeVisible();
});

test('handles API errors gracefully', async ({ page }) => {
  await page.route('/api/users', route =>
    route.fulfill({ status: 500 })
  );

  await page.goto('/users');
  await expect(page.getByText('Failed to load users')).toBeVisible();
});
```

### Wait for API Calls

```typescript
test('submits form and waits for API', async ({ page }) => {
  await page.goto('/contact');

  // Start waiting for API response before triggering it
  const responsePromise = page.waitForResponse('/api/contact');

  await page.getByLabel('Email').fill('test@example.com');
  await page.getByRole('button', { name: 'Submit' }).click();

  const response = await responsePromise;
  expect(response.status()).toBe(200);
});
```

## Visual Testing

### Screenshots

```typescript
test('homepage visual test', async ({ page }) => {
  await page.goto('/');

  // Full page screenshot
  await expect(page).toHaveScreenshot('homepage.png', {
    fullPage: true,
  });
});

test('component visual test', async ({ page }) => {
  await page.goto('/');

  // Element screenshot
  await expect(page.getByTestId('header')).toHaveScreenshot('header.png');
});
```

### Screenshot Options

```typescript
await page.screenshot({
  path: 'screenshots/test.png',
  fullPage: true,
  animations: 'disabled', // Reduce flakiness
  mask: [page.locator('.dynamic-content')], // Hide changing content
});
```

## Authentication Reuse

### Save Auth State

```typescript
// auth.setup.ts
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill('user@example.com');
  await page.getByLabel('Password').fill('password');
  await page.getByRole('button', { name: 'Sign in' }).click();

  await page.waitForURL('/dashboard');

  // Save signed-in state
  await page.context().storageState({ path: authFile });
});
```

### Use Auth State

```typescript
// playwright.config.ts
export default defineConfig({
  projects: [
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'tests',
      dependencies: ['setup'],
      use: {
        storageState: 'playwright/.auth/user.json',
      },
    },
  ],
});
```

## Accessibility Testing

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test.describe('Accessibility', () => {
  test('homepage has no a11y violations', async ({ page }) => {
    await page.goto('/');

    const results = await new AxeBuilder({ page }).analyze();

    expect(results.violations).toEqual([]);
  });

  test('form is accessible', async ({ page }) => {
    await page.goto('/contact');

    const results = await new AxeBuilder({ page })
      .include('form')
      .analyze();

    expect(results.violations).toEqual([]);
  });
});
```

## Performance Testing

```typescript
test('page loads within performance budget', async ({ page }) => {
  await page.goto('/');

  const metrics = await page.evaluate(() =>
    JSON.stringify(window.performance.timing)
  );
  const timing = JSON.parse(metrics);

  const loadTime = timing.loadEventEnd - timing.navigationStart;
  expect(loadTime).toBeLessThan(3000); // 3 seconds
});

test('tracks Core Web Vitals', async ({ page }) => {
  await page.goto('/');

  const lcp = await page.evaluate(() => {
    return new Promise(resolve => {
      new PerformanceObserver(list => {
        const entries = list.getEntries();
        resolve(entries[entries.length - 1].startTime);
      }).observe({ type: 'largest-contentful-paint', buffered: true });
    });
  });

  expect(lcp).toBeLessThan(2500); // Good LCP is < 2.5s
});
```

## Debug Helpers

### Debugging Commands

```bash
# Run with headed browser
npx playwright test --headed

# Run with debugging UI
npx playwright test --debug

# Run specific test
npx playwright test -g "test name"

# Show report
npx playwright show-report
```

### In-Test Debugging

```typescript
test('debug example', async ({ page }) => {
  await page.goto('/');

  // Pause execution
  await page.pause();

  // Take screenshot
  await page.screenshot({ path: 'debug.png' });

  // Log to console
  console.log(await page.content());

  // Slow down
  await page.setDefaultTimeout(30000);
});
```

### Console Logs

```python
# Python: Capture browser console
page.on('console', lambda msg: print(f'Browser log: {msg.text}'))
page.on('pageerror', lambda err: print(f'Browser error: {err}'))
```

```typescript
// TypeScript: Capture browser console
page.on('console', msg => console.log('Browser:', msg.text()));
page.on('pageerror', err => console.log('Error:', err));
```

## Test Organization

### File Structure

```
tests/
├── e2e/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   └── logout.spec.ts
│   ├── products/
│   │   ├── listing.spec.ts
│   │   └── details.spec.ts
│   └── checkout/
│       └── flow.spec.ts
├── fixtures/
│   └── test-data.ts
└── utils/
    └── helpers.ts
```

### Custom Fixtures

```typescript
// fixtures/test-fixtures.ts
import { test as base } from '@playwright/test';

type Fixtures = {
  authenticatedPage: Page;
};

export const test = base.extend<Fixtures>({
  authenticatedPage: async ({ page }, use) => {
    await page.goto('/login');
    await page.fill('[name="email"]', 'test@example.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');
    await page.waitForURL('/dashboard');
    await use(page);
  },
});

// Usage
test('authenticated test', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/profile');
  // Already logged in
});
```

## Common Pitfalls

| Pitfall | Problem | Solution |
|---------|---------|----------|
| Race conditions | Test checks before page updates | Use `waitFor` or `expect` with retries |
| Flaky selectors | CSS classes change | Use `data-testid` or role selectors |
| Hard-coded waits | `page.waitForTimeout(3000)` | Wait for specific conditions |
| Not waiting for hydration | JS not executed | `waitForLoadState('networkidle')` |
| Shared state | Tests affect each other | Use isolated storage/auth per test |
| Ignoring errors | Uncaught exceptions | Check `page.on('pageerror')` |

## Checklist

- [ ] Use stable selectors (test IDs, roles, labels)
- [ ] Wait for appropriate conditions (not arbitrary timeouts)
- [ ] Test both happy path and error states
- [ ] Include accessibility checks
- [ ] Test responsive breakpoints
- [ ] Mock external API dependencies
- [ ] Capture screenshots on failure
- [ ] Run tests in CI/CD
- [ ] Keep tests independent
- [ ] Organize tests by feature
