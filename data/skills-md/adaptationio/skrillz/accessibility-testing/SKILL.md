---
name: accessibility-testing
description: Accessibility testing with axe-core and Playwright. Use when checking WCAG compliance, finding a11y issues, ensuring keyboard navigation, or testing screen reader compatibility.
version: 1.0.0
tags: [testing, accessibility, a11y, wcag, axe-core, playwright]
---

# Accessibility Testing with axe-core

Automated accessibility testing for WCAG 2.1 AA/AAA compliance using axe-core integrated with Playwright.

## Quick Start

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('homepage has no accessibility violations', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page }).analyze();

  expect(results.violations).toEqual([]);
});
```

## Installation

```bash
npm install -D @axe-core/playwright
```

## Basic Usage

### Full Page Scan

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('check entire page', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');

  const accessibilityScanResults = await new AxeBuilder({ page }).analyze();

  expect(accessibilityScanResults.violations).toEqual([]);
});
```

### Specific Element Scan

```typescript
test('check navigation accessibility', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .include('nav')
    .analyze();

  expect(results.violations).toEqual([]);
});
```

### Exclude Dynamic Content

```typescript
test('check page excluding ads', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .exclude('.advertisement')
    .exclude('#third-party-widget')
    .analyze();

  expect(results.violations).toEqual([]);
});
```

## WCAG Compliance Levels

### WCAG 2.1 Level A

```typescript
test('WCAG 2.1 Level A compliance', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag21a'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

### WCAG 2.1 Level AA (Most Common Requirement)

```typescript
test('WCAG 2.1 Level AA compliance', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

### WCAG 2.1 Level AAA

```typescript
test('WCAG 2.1 Level AAA compliance', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag2aaa', 'wcag21a', 'wcag21aa', 'wcag21aaa'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

## Common Rule Categories

### Best Practice Rules

```typescript
test('accessibility best practices', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['best-practice'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

### Specific Rules Only

```typescript
test('check specific rules', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withRules(['color-contrast', 'image-alt', 'label', 'link-name'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

### Disable Specific Rules

```typescript
test('check except known issues', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .disableRules(['color-contrast'])  // Known issue, tracked separately
    .analyze();

  expect(results.violations).toEqual([]);
});
```

## Keyboard Navigation Testing

### Tab Order

```typescript
test('verify tab order', async ({ page }) => {
  await page.goto('/');

  const expectedOrder = ['#search', '#nav-home', '#nav-about', '#nav-contact', '#main-content'];

  for (const selector of expectedOrder) {
    await page.keyboard.press('Tab');
    const focused = await page.evaluate(() => document.activeElement?.id || document.activeElement?.className);
    expect(`#${focused}`).toBe(selector);
  }
});
```

### Focus Visibility

```typescript
test('focus indicators are visible', async ({ page }) => {
  await page.goto('/');

  await page.keyboard.press('Tab');

  const focusedElement = page.locator(':focus');
  const outline = await focusedElement.evaluate(el => {
    const styles = window.getComputedStyle(el);
    return styles.outline || styles.boxShadow;
  });

  expect(outline).not.toBe('none');
});
```

### Skip Links

```typescript
test('skip link works', async ({ page }) => {
  await page.goto('/');

  // First tab should focus skip link
  await page.keyboard.press('Tab');
  await expect(page.locator(':focus')).toHaveText(/skip to/i);

  // Enter should jump to main content
  await page.keyboard.press('Enter');
  await expect(page.locator(':focus')).toHaveAttribute('id', 'main-content');
});
```

## Color Contrast Testing

```typescript
test('color contrast meets WCAG AA', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withRules(['color-contrast'])
    .analyze();

  if (results.violations.length > 0) {
    console.log('Contrast violations:');
    results.violations[0].nodes.forEach(node => {
      console.log(`  - ${node.html}`);
      console.log(`    ${node.failureSummary}`);
    });
  }

  expect(results.violations).toEqual([]);
});
```

## Form Accessibility

```typescript
test('form is accessible', async ({ page }) => {
  await page.goto('/contact');

  // Check labels
  const inputs = page.locator('input:not([type="hidden"])');
  const count = await inputs.count();

  for (let i = 0; i < count; i++) {
    const input = inputs.nth(i);
    const id = await input.getAttribute('id');
    const ariaLabel = await input.getAttribute('aria-label');
    const ariaLabelledBy = await input.getAttribute('aria-labelledby');
    const label = page.locator(`label[for="${id}"]`);

    const hasLabel = await label.count() > 0 || ariaLabel || ariaLabelledBy;
    expect(hasLabel).toBeTruthy();
  }

  // Run axe on form
  const results = await new AxeBuilder({ page })
    .include('form')
    .analyze();

  expect(results.violations).toEqual([]);
});
```

## Image Accessibility

```typescript
test('all images have alt text', async ({ page }) => {
  await page.goto('/');

  const images = page.locator('img');
  const count = await images.count();

  for (let i = 0; i < count; i++) {
    const img = images.nth(i);
    const alt = await img.getAttribute('alt');
    const role = await img.getAttribute('role');

    // Images must have alt OR be decorative (role="presentation")
    const isAccessible = alt !== null || role === 'presentation' || role === 'none';
    expect(isAccessible).toBeTruthy();
  }
});
```

## ARIA Testing

```typescript
test('ARIA attributes are valid', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page })
    .withTags(['cat.aria'])
    .analyze();

  expect(results.violations).toEqual([]);
});
```

## Reporting

### Detailed Violation Report

```typescript
import { test, expect } from '@playwright/test';
import AxeBuilder from '@axe-core/playwright';

test('accessibility audit', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page }).analyze();

  // Generate detailed report
  if (results.violations.length > 0) {
    console.log('\n=== Accessibility Violations ===\n');

    results.violations.forEach(violation => {
      console.log(`Rule: ${violation.id}`);
      console.log(`Impact: ${violation.impact}`);
      console.log(`Description: ${violation.description}`);
      console.log(`Help: ${violation.helpUrl}`);
      console.log(`Affected elements:`);

      violation.nodes.forEach(node => {
        console.log(`  - ${node.html}`);
        console.log(`    ${node.failureSummary}`);
      });
      console.log('');
    });
  }

  expect(results.violations).toEqual([]);
});
```

### Save Report to File

```typescript
import fs from 'fs';

test('save accessibility report', async ({ page }) => {
  await page.goto('/');

  const results = await new AxeBuilder({ page }).analyze();

  // Save JSON report
  fs.writeFileSync(
    'accessibility-report.json',
    JSON.stringify(results, null, 2)
  );

  // Save HTML report
  const htmlReport = generateHtmlReport(results);
  fs.writeFileSync('accessibility-report.html', htmlReport);
});

function generateHtmlReport(results: any): string {
  return `
    <!DOCTYPE html>
    <html>
    <head><title>Accessibility Report</title></head>
    <body>
      <h1>Accessibility Report</h1>
      <p>Violations: ${results.violations.length}</p>
      <p>Passes: ${results.passes.length}</p>
      ${results.violations.map(v => `
        <div style="border:1px solid red;padding:10px;margin:10px 0">
          <h3>${v.id}</h3>
          <p><strong>Impact:</strong> ${v.impact}</p>
          <p>${v.description}</p>
          <p><a href="${v.helpUrl}">More info</a></p>
        </div>
      `).join('')}
    </body>
    </html>
  `;
}
```

## CI Integration

### GitHub Actions

```yaml
- name: Run accessibility tests
  run: npx playwright test --grep @a11y

- name: Upload a11y report
  if: failure()
  uses: actions/upload-artifact@v4
  with:
    name: accessibility-report
    path: accessibility-report.html
```

## Best Practices

1. **Test early and often** - Include a11y tests in CI
2. **Start with WCAG 2.1 AA** - Most common legal requirement
3. **Test with real users** - Automated tests catch ~30% of issues
4. **Test keyboard navigation** - Essential for motor disabilities
5. **Test with screen readers** - NVDA (Windows), VoiceOver (Mac)
6. **Fix critical issues first** - Impact: critical > serious > moderate > minor

## References

- `references/wcag-checklist.md` - WCAG 2.1 compliance checklist
- `references/common-issues.md` - Most common a11y issues and fixes
