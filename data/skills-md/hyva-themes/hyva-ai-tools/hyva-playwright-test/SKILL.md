---
name: hyva-playwright-test
description: Write Playwright tests for Hyvä themes with Alpine.js components. This skill should be used when writing e2e tests, creating page objects, or debugging selector issues in Playwright tests for Hyvä Magento storefronts. Trigger phrases include "write playwright test", "playwright alpine", "test hyva page", "e2e test", "playwright selector".
---

# Writing Playwright Tests for Hyvä + Alpine.js

## Overview

Hyvä replaces Luma's KnockoutJS/RequireJS/jQuery with Alpine.js + Tailwind CSS. Playwright's strict mode (rejects locators matching multiple elements) conflicts with Alpine.js DOM patterns where hidden elements exist throughout the page. This skill documents pitfalls and solutions discovered while writing Playwright tests for Hyvä storefronts.

## The #1 Rule: Hidden Alpine Elements

Hyvä templates scatter elements like `<div x-show="displayErrorMessage" class="message error">` throughout the DOM. These are **invisible but present**, so a bare selector like `.message.error` matches both hidden and visible instances, causing Playwright strict mode violations.

**Always scope page-level messages to the `#messages` container:**

```typescript
// WRONG — matches hidden Alpine x-show elements throughout DOM
await expect(page.locator('.message.success')).toContainText('Added to cart');
await expect(page.locator('.message-error')).toContainText('Error');

// RIGHT — scoped to the visible messages container
await expect(page.locator('#messages .message.success')).toContainText('Added to cart');
await expect(page.locator('#messages .message-error, #messages .message.error')).toContainText('Error');
```

**Never use:** bare `.message`, `.message.error`, `.message.success`, or `div.message` as selectors.

**Exception — inline page messages:** Not all `.message` elements are flash messages. The search results "no results" notice (`.message.notice`) renders as static inline content inside `#maincontent`, not inside the `#messages` container. For these inline messages, the bare class selector is correct.

## Selector Strategy

Follow [Playwright's recommended locator priority](https://playwright.dev/docs/locators):

1. **`getByRole()`** — always prefer — closest to how users perceive the page. Avoids text ambiguity where the same text appears in headings, links, breadcrumbs, and `sr-only` spans.
2. **`getByLabel()`** — for form controls (checkboxes, inputs with associated labels).
3. **`getByText()`** — for non-interactive elements, **scoped to a container** (e.g., `page.locator('#maincontent').getByText(...)`).
4. **`getByPlaceholder()`**, **`getByAltText()`** — for inputs and images respectively.
5. **`getByTestId()`** — when Hyvä provides `data-testid` attributes or when adding custom test IDs.
6. **CSS selectors** — last resort, only when user-facing locators aren't available. Prefer `aria-*` attribute selectors (e.g., `[aria-label="pagination"]`, `[aria-current="page"]`) over class-based selectors. When CSS is necessary, scope to a unique container (e.g., `#messages .message.success`).

**Avoid:** `:visible` pseudo-selector — per Playwright docs, "it's usually better to find a more reliable way to uniquely identify the element." Scope to a container or use role/attribute selectors instead. Only use `:visible` as an absolute last resort when the DOM provides no other way to distinguish elements.

## Alpine.js Interaction Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| `x-show` hidden elements | Strict mode: multiple matches | Scope to unique container (`#messages`), use role/attribute selectors |
| `x-defer="intersect"` | Element not initialized until visible | `scrollIntoViewIfNeeded()` before interacting |
| `x-if` (template) | Elements don't exist in DOM until condition true | Click the trigger first, then query children |
| `x-model` on inputs | Alpine clears value after form submit | Don't assert input value post-submit; verify via success message |
| `x-text` / `x-html` async | Cart badge updates asynchronously | Use web-first assertions with timeout: `not.toHaveText('0', { timeout: 15_000 })` |
| `x-show` submenus | Hidden until hover | `hover()` on parent before clicking child |
| Alpine form reveal | Fields hidden until checkbox checked | `waitFor({ state: 'visible' })` after checking the checkbox |
| `press('Enter')` on input | May submit Alpine-bound form unexpectedly | Prefer explicit `.click()` on submit button |

## Assertions

Always use [web-first assertions](https://playwright.dev/docs/best-practices#use-web-first-assertions) that auto-wait and retry:

```typescript
// DO — auto-retries             // DON'T — no retry
await expect(loc).toBeVisible(); // expect(await loc.isVisible()).toBe(true);
await expect(loc).toContainText('X'); // expect(await loc.textContent()).toContain('X');
```

For async Alpine.js updates (cart counts, prices), use extended timeouts on the assertion — never `waitForTimeout()`:

```typescript
// Cart count updates asynchronously via Alpine x-text
await expect(page.locator('#menu-cart-icon span[x-text="summaryCount"]'))
  .not.toHaveText('0', { timeout: 15_000 });
```

## Hyvä vs Luma Selector Differences

| Element | Hyvä Selector | Luma Selector |
|---------|---------------|---------------|
| Pagination nav | `getByRole('navigation', { name: 'pagination' })` | `ul.pages-items` |
| Page link | `getByRole('link', { name: 'Page 2' })` | `.pages-items li a` |
| Active page | `[aria-current="page"]` | `<strong>` element |
| Filter button | `getByRole('button', { name: 'Color filter' })` | `.filter-options-title` |
| Cart icon badge | `#menu-cart-icon > span[x-text="summaryCount"]` | `.counter-number` |
| Account menu | `#customer-menu + nav` | `.customer-menu` |
| Success message | `#messages .message.success` | `.message-success` |
| Error message | `#messages .message-error, #messages .message.error` | `.message-error` |
| Main menu | `getByRole('navigation', { name: 'Main menu' })` | `nav.navigation` |
| Footer nav | `getByRole('navigation', { name: 'Company Menu' }).getByRole('link', { name })` | `nav ul li:nth-child(N) a` |
| Product image | `#gallery img[itemprop="image"]` | `#gallery img:visible` |
| Add to Cart (card) | `getByRole('button', { name: /Add to Cart/ }).first()` | `button.btn-primary:visible` |

## References

See `references/` for code examples. Load files relevant to the current task:

**Always useful:**
- **[page-object-patterns.md](references/page-object-patterns.md)** — Page object structure, navigation, form submits, redirects
- **[selector-patterns.md](references/selector-patterns.md)** — Before/after selector fixes (messages, text ambiguity, forms)


**Page-specific (load when testing that page):**
- **[cart-patterns.md](references/cart-patterns.md)** — Cart spinner wait, quantity changes, mini cart
- **[product-patterns.md](references/product-patterns.md)** — Bundle quantities, gallery images
- **[account-patterns.md](references/account-patterns.md)** — Password change (Alpine checkbox reveal)
- **[category-patterns.md](references/category-patterns.md)** — Filters (x-defer scroll), pagination (ARIA)

<!-- Copyright © Hyvä Themes https://hyva.io. All rights reserved. Licensed under OSL 3.0 -->

