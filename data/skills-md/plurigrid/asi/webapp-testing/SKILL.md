---
name: webapp-testing
description: Toolkit for interacting with and testing local web applications using
version: 1.0.0
---


# Web App Testing with Playwright

## Setup

```bash
npm init playwright@latest
```

## Basic Test Structure

```typescript
import { test, expect } from '@playwright/test';

test('homepage has title', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await expect(page).toHaveTitle(/My App/);
});

test('can navigate to about page', async ({ page }) => {
  await page.goto('http://localhost:3000');
  await page.click('text=About');
  await expect(page).toHaveURL(/.*about/);
});
```

## Common Actions

### Navigation
```typescript
await page.goto('http://localhost:3000');
await page.goBack();
await page.reload();
```

### Clicking
```typescript
await page.click('button');
await page.click('text=Submit');
await page.click('#submit-btn');
await page.click('[data-testid="submit"]');
```

### Form Input
```typescript
await page.fill('input[name="email"]', 'test@example.com');
await page.fill('#password', 'secret123');
await page.selectOption('select#country', 'USA');
await page.check('input[type="checkbox"]');
```

### Waiting
```typescript
await page.waitForSelector('.loaded');
await page.waitForURL('**/dashboard');
await page.waitForResponse('**/api/data');
await page.waitForTimeout(1000); // Avoid if possible
```

## Assertions

```typescript
await expect(page.locator('h1')).toHaveText('Welcome');
await expect(page.locator('.items')).toHaveCount(5);
await expect(page.locator('button')).toBeEnabled();
await expect(page.locator('.modal')).toBeVisible();
await expect(page.locator('input')).toHaveValue('test');
```

## Screenshots

```typescript
// Full page
await page.screenshot({ path: 'screenshot.png', fullPage: true });

// Element only
await page.locator('.chart').screenshot({ path: 'chart.png' });
```

## Console Logs

```typescript
page.on('console', msg => console.log(msg.text()));
page.on('pageerror', err => console.error(err.message));
```

## Network Interception

```typescript
await page.route('**/api/data', route => {
  route.fulfill({
    status: 200,
    body: JSON.stringify({ items: [] })
  });
});
```

## Running Tests

```bash
# Run all tests
npx playwright test

# Run specific file
npx playwright test tests/login.spec.ts

# Run in headed mode
npx playwright test --headed

# Run with UI
npx playwright test --ui
```



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 5. Evaluation

**Concepts**: eval, apply, interpreter, environment

### GF(3) Balanced Triad

```
webapp-testing (+) + SDF.Ch5 (−) + [balancer] (○) = 0
```

**Skill Trit**: 1 (PLUS - generation)


### Connection Pattern

Evaluation interprets expressions. This skill processes or generates evaluable forms.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.