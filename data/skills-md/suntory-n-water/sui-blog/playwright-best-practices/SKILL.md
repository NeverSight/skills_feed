---
name: playwright-best-practices
description: Playwright automation best practices for web scraping and testing. Use when writing or reviewing Playwright code, especially for element operations (click, fill, select), waiting strategies (waitForSelector, waitForURL, waitForLoadState), navigation patterns, and locator usage. Apply when encountering unstable tests, race conditions, or needing guidance on avoiding deprecated patterns like waitForNavigation or networkidle.
---

# Playwright Best Practices

## Overview

This skill provides guidance on writing reliable, maintainable Playwright automation code based on official best practices. It covers element operations, waiting strategies, navigation patterns, and common anti-patterns to avoid.

## Core Principles

### 1. Always Use Locators with Auto-waiting

Playwright Locators automatically wait and retry until elements are actionable:

```typescript
// ✅ Recommended: Locator with auto-waiting
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByLabel('Username').fill('john');

// ❌ Avoid: Direct DOM manipulation
await page.evaluate(() => document.querySelector('button').click());
```

### 2. Prefer User-Facing Attributes

Prioritize locators based on how users perceive the page:

```typescript
// Priority order:
// 1. Role-based (best for accessibility)
await page.getByRole('button', { name: 'Sign in' });

// 2. Label-based (best for forms)
await page.getByLabel('Email address');

// 3. Text-based
await page.getByText('Submit');

// 4. Test ID
await page.getByTestId('submit-button');

// 5. CSS/XPath (last resort)
await page.locator('.btn-primary');
```

### 3. Trust Auto-waiting, Minimize Explicit Waits

Locators automatically check actionability before operations:

```typescript
// ✅ Recommended: Action includes waiting
await page.getByRole('button').click();

// ⚠️ Usually unnecessary
await page.waitForSelector('button');
await page.locator('button').click();
```

## Common Workflows

### Element Operations

**Click:**
```typescript
await page.getByRole('button', { name: 'Next' }).click();
```

**Fill text:**
```typescript
await page.getByLabel('Email').fill('user@example.com');
```

**Select option:**
```typescript
await page.getByLabel('Country').selectOption({ label: 'Japan' });
```

**Check/uncheck:**
```typescript
await page.getByLabel('I agree').check();
```

### Navigation Patterns

**Same-page navigation:**
```typescript
// ✅ Recommended: Click and wait for next page element
await page.getByRole('link', { name: 'Next' }).click();
await page.waitForSelector('#next-page-element', { timeout: 30 * 1000 }); // example wait time

// Or use conditional selector for different destination pages
const waitSelector = condition === 'A'
  ? '#page-a-element'
  : '#page-b-element';
await page.waitForSelector(waitSelector, { timeout: 30 * 1000 }); // example wait time

// Or use waitForURL if URL pattern is predictable
await page.click('button');
await page.waitForURL('**/next-page');
```

**New tab/window:**
```typescript
const [newPage] = await Promise.all([
  page.context().waitForEvent('page'),
  page.getByRole('link', { name: 'Open in new tab' }).click()
]);
await newPage.waitForLoadState();
```

### Form Interactions

```typescript
// Complete form workflow
await page.getByLabel('Username').fill('john');
await page.getByLabel('Password').fill('secret');
await page.getByRole('checkbox', { name: 'Remember me' }).check();
await page.getByLabel('Country').selectOption('Japan');
await page.getByRole('button', { name: 'Submit' }).click();

// Verify submission
await expect(page.getByText('Success')).toBeVisible();
```

## Anti-Patterns to Avoid

### ❌ waitForNavigation (Deprecated)
```typescript
// ❌ Avoid: Deprecated API
const navigationPromise = page.waitForNavigation();
await page.click('button');
await navigationPromise;

// ✅ Use instead: waitForURL or waitForSelector
await page.click('button');
await page.waitForURL('**/next-page');
// or
await page.waitForSelector('#next-page-element');
```

### ❌ networkidle (Unreliable)
```typescript
// ❌ Avoid: Can complete before page is ready
await page.waitForLoadState('networkidle');

// ✅ Use instead: Wait for specific elements
await page.waitForSelector('#content-loaded');
// or
await page.waitForLoadState('load');
```

### ❌ page.evaluate() for Clicks
```typescript
// ❌ Avoid: Bypasses actionability checks
await page.evaluate(() => document.querySelector('button').click());

// ✅ Use instead: Locator click
await page.locator('button').click();
```

### ❌ Unnecessary Promise.all
```typescript
// ❌ Unnecessary: Playwright auto-waits for navigation
await Promise.all([
  page.waitForNavigation(),
  page.click('button')
]);

// ✅ Simpler: Just click
await page.click('button');
```

## Actionability Checks

Playwright automatically verifies these conditions before actions:

| Action | Visible | Stable | Receives Events | Enabled | Editable |
|--------|---------|--------|----------------|---------|----------|
| click() | ✓ | ✓ | ✓ | ✓ | - |
| fill() | ✓ | - | - | ✓ | ✓ |
| check() | ✓ | ✓ | ✓ | ✓ | - |
| selectOption() | ✓ | - | - | ✓ | - |
| hover() | ✓ | ✓ | ✓ | - | - |

**Definitions:**
- **Visible**: Has bounding box, not `visibility:hidden`
- **Stable**: Same position for 2+ frames (animation complete)
- **Receives Events**: Not covered by other elements
- **Enabled**: No `disabled` attribute
- **Editable**: Enabled and not `readonly`

## When to Use Explicit Waits

Explicit waits are needed in these cases:

```typescript
// 1. Before using locator.all() (doesn't auto-wait)
await page.getByRole('listitem').first().waitFor();
const items = await page.getByRole('listitem').all();

// 2. Waiting for element to disappear
await page.locator('.loading').waitFor({ state: 'hidden' });

// 3. Waiting for element to detach
await page.locator('.modal').waitFor({ state: 'detached' });

// 4. Conditional page destinations
const waitSelector = condition ? '#page-a' : '#page-b';
await page.waitForSelector(waitSelector, { timeout: 30 * 1000 }); // example wait time
```

## Advanced References

For detailed information on specific topics, see:

- **[anti-patterns.md](references/anti-patterns.md)**: Detailed explanation of deprecated patterns and why to avoid them
- **[locators.md](references/locators.md)**: Comprehensive guide to locator strategies and selection
- **[actions.md](references/actions.md)**: Detailed action methods and their behavior


## Official Documentation

- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Actionability](https://playwright.dev/docs/actionability)
- [Locators](https://playwright.dev/docs/locators)
- [Navigations](https://playwright.dev/docs/navigations)
