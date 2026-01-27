---
name: component-testing
description: Isolated component testing for React, Vue, and Svelte with Playwright. Use when testing UI components in isolation, testing component interactions, or building component test suites.
version: 1.0.0
tags: [testing, components, react, vue, svelte, playwright, isolation]
---

# Component Testing with Playwright

Test UI components in isolation using Playwright's experimental component testing feature. Supports React, Vue, Svelte, and Solid.

## Quick Start

```typescript
// Button.spec.tsx
import { test, expect } from '@playwright/experimental-ct-react';
import { Button } from './Button';

test('button click triggers callback', async ({ mount }) => {
  let clicked = false;

  const component = await mount(
    <Button onClick={() => clicked = true}>Click me</Button>
  );

  await component.click();
  expect(clicked).toBe(true);
});
```

## Installation

### React

```bash
npm init playwright@latest -- --ct
# Select React when prompted
```

Or manually:
```bash
npm install -D @playwright/experimental-ct-react
```

### Vue

```bash
npm install -D @playwright/experimental-ct-vue
```

### Svelte

```bash
npm install -D @playwright/experimental-ct-svelte
```

## Configuration

**playwright-ct.config.ts:**
```typescript
import { defineConfig, devices } from '@playwright/experimental-ct-react';

export default defineConfig({
  testDir: './src',
  testMatch: '**/*.spec.tsx',

  use: {
    ctPort: 3100,
    ctViteConfig: {
      // Custom Vite config for component tests
    },
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
});
```

## React Component Testing

### Basic Mount

```typescript
import { test, expect } from '@playwright/experimental-ct-react';
import { UserCard } from './UserCard';

test('displays user info', async ({ mount }) => {
  const component = await mount(
    <UserCard
      name="John Doe"
      email="john@example.com"
    />
  );

  await expect(component.getByText('John Doe')).toBeVisible();
  await expect(component.getByText('john@example.com')).toBeVisible();
});
```

### With Props

```typescript
test('button variants', async ({ mount }) => {
  // Primary variant
  const primary = await mount(<Button variant="primary">Save</Button>);
  await expect(primary).toHaveClass(/btn-primary/);

  // Secondary variant
  const secondary = await mount(<Button variant="secondary">Cancel</Button>);
  await expect(secondary).toHaveClass(/btn-secondary/);
});
```

### With Event Handlers

```typescript
test('form submission', async ({ mount }) => {
  const submittedData: any[] = [];

  const component = await mount(
    <ContactForm onSubmit={(data) => submittedData.push(data)} />
  );

  await component.getByLabel('Name').fill('John');
  await component.getByLabel('Email').fill('john@example.com');
  await component.getByRole('button', { name: 'Submit' }).click();

  expect(submittedData).toHaveLength(1);
  expect(submittedData[0]).toEqual({
    name: 'John',
    email: 'john@example.com',
  });
});
```

### With Context Providers

```typescript
// Create wrapper for providers
import { ThemeProvider } from './ThemeContext';

test('themed component', async ({ mount }) => {
  const component = await mount(
    <ThemeProvider theme="dark">
      <ThemedButton>Click</ThemedButton>
    </ThemeProvider>
  );

  await expect(component).toHaveClass(/dark-theme/);
});
```

### With Slots/Children

```typescript
test('card with custom content', async ({ mount }) => {
  const component = await mount(
    <Card>
      <CardHeader>Title</CardHeader>
      <CardBody>Content here</CardBody>
      <CardFooter>
        <Button>Action</Button>
      </CardFooter>
    </Card>
  );

  await expect(component.getByText('Title')).toBeVisible();
  await expect(component.getByText('Content here')).toBeVisible();
  await expect(component.getByRole('button')).toBeVisible();
});
```

## Vue Component Testing

```typescript
// Counter.spec.ts
import { test, expect } from '@playwright/experimental-ct-vue';
import Counter from './Counter.vue';

test('counter increments', async ({ mount }) => {
  const component = await mount(Counter, {
    props: {
      initialCount: 0,
    },
  });

  await expect(component.getByText('Count: 0')).toBeVisible();
  await component.getByRole('button', { name: '+' }).click();
  await expect(component.getByText('Count: 1')).toBeVisible();
});
```

### With Slots

```typescript
test('card with slots', async ({ mount }) => {
  const component = await mount(Card, {
    slots: {
      default: '<p>Card content</p>',
      header: '<h2>Card Title</h2>',
    },
  });

  await expect(component.getByText('Card Title')).toBeVisible();
  await expect(component.getByText('Card content')).toBeVisible();
});
```

### With Vuex/Pinia

```typescript
import { test, expect } from '@playwright/experimental-ct-vue';
import { createTestingPinia } from '@pinia/testing';
import UserProfile from './UserProfile.vue';

test('displays user from store', async ({ mount }) => {
  const component = await mount(UserProfile, {
    global: {
      plugins: [
        createTestingPinia({
          initialState: {
            user: { name: 'John', email: 'john@example.com' },
          },
        }),
      ],
    },
  });

  await expect(component.getByText('John')).toBeVisible();
});
```

## Svelte Component Testing

```typescript
// Button.spec.ts
import { test, expect } from '@playwright/experimental-ct-svelte';
import Button from './Button.svelte';

test('button emits click', async ({ mount }) => {
  let clicked = false;

  const component = await mount(Button, {
    props: {
      label: 'Click me',
    },
    on: {
      click: () => clicked = true,
    },
  });

  await component.click();
  expect(clicked).toBe(true);
});
```

## Testing Patterns

### Visual Regression

```typescript
test('button visual states', async ({ mount }) => {
  const component = await mount(<Button>Click</Button>);

  // Default state
  await expect(component).toHaveScreenshot('button-default.png');

  // Hover state
  await component.hover();
  await expect(component).toHaveScreenshot('button-hover.png');

  // Focus state
  await component.focus();
  await expect(component).toHaveScreenshot('button-focus.png');
});
```

### Accessibility

```typescript
import AxeBuilder from '@axe-core/playwright';

test('button is accessible', async ({ mount, page }) => {
  await mount(<Button>Submit</Button>);

  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});
```

### Responsive Behavior

```typescript
test('responsive navigation', async ({ mount, page }) => {
  const component = await mount(<Navigation />);

  // Desktop - horizontal nav
  await page.setViewportSize({ width: 1280, height: 720 });
  await expect(component.locator('.nav-horizontal')).toBeVisible();

  // Mobile - hamburger menu
  await page.setViewportSize({ width: 375, height: 667 });
  await expect(component.locator('.hamburger-menu')).toBeVisible();
});
```

### Loading States

```typescript
test('async component states', async ({ mount }) => {
  const component = await mount(<DataTable dataUrl="/api/data" />);

  // Loading state
  await expect(component.getByText('Loading...')).toBeVisible();

  // Wait for data
  await expect(component.getByRole('table')).toBeVisible();
  await expect(component.getByText('Loading...')).not.toBeVisible();
});
```

### Error States

```typescript
test('error handling', async ({ mount, page }) => {
  // Mock failed API
  await page.route('**/api/data', route => {
    route.fulfill({ status: 500 });
  });

  const component = await mount(<DataTable dataUrl="/api/data" />);

  await expect(component.getByText(/error/i)).toBeVisible();
  await expect(component.getByRole('button', { name: 'Retry' })).toBeVisible();
});
```

## Hooks and Fixtures

### Before Each Test

```typescript
import { test as base, expect } from '@playwright/experimental-ct-react';

const test = base.extend({
  autoMockApi: async ({ page }, use) => {
    await page.route('**/api/**', route => {
      route.fulfill({ status: 200, body: '{}' });
    });
    await use();
  },
});

test('component with mocked api', async ({ mount, autoMockApi }) => {
  const component = await mount(<ApiComponent />);
  // API calls are automatically mocked
});
```

### Custom Mount

```typescript
const test = base.extend({
  mountWithProviders: async ({ mount }, use) => {
    const wrappedMount = async (component: JSX.Element) => {
      return mount(
        <ThemeProvider>
          <AuthProvider>
            {component}
          </AuthProvider>
        </ThemeProvider>
      );
    };
    await use(wrappedMount);
  },
});

test('with providers', async ({ mountWithProviders }) => {
  const component = await mountWithProviders(<Dashboard />);
  // Component has access to theme and auth contexts
});
```

## Running Tests

```bash
# Run all component tests
npx playwright test -c playwright-ct.config.ts

# Run specific test file
npx playwright test Button.spec.tsx -c playwright-ct.config.ts

# Run with UI mode
npx playwright test -c playwright-ct.config.ts --ui

# Update snapshots
npx playwright test -c playwright-ct.config.ts --update-snapshots
```

## Best Practices

1. **Test behavior, not implementation** - Focus on user interactions
2. **Keep components isolated** - Mock external dependencies
3. **Test all states** - Default, loading, error, empty, success
4. **Use semantic queries** - `getByRole`, `getByLabel` over CSS selectors
5. **Combine with E2E** - Component tests for logic, E2E for integration

## References

- `references/react-patterns.md` - React-specific testing patterns
- `references/vue-patterns.md` - Vue-specific testing patterns
