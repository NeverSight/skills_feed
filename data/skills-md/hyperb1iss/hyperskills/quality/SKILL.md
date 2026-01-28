---
name: quality
description: Use this skill when writing tests, fixing test failures, improving code quality, doing accessibility audits, or optimizing performance. Activates on mentions of testing, unit test, integration test, e2e test, Playwright, Vitest, Jest, pytest, test coverage, accessibility, WCAG, a11y, axe-core, screen reader, Core Web Vitals, performance, lighthouse, or code review.
---

# Quality Engineering

Ship reliable, accessible, performant software.

## Quick Reference

### Testing Stack (2026)

| Type        | Tool               | Purpose               |
| ----------- | ------------------ | --------------------- |
| Unit        | Vitest             | Fast, Vite-native     |
| Component   | Testing Library    | User-centric          |
| E2E         | Playwright         | Cross-browser         |
| API         | Playwright API     | Request testing       |
| Visual      | Playwright + Percy | Screenshot comparison |
| A11y        | Axe-core           | WCAG compliance       |
| Performance | Lighthouse CI      | Core Web Vitals       |

### Vitest Setup

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    globals: true,
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: ["node_modules", "tests"],
    },
  },
});
```

**Writing Tests:**

```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { UserProfile } from './UserProfile';

describe('UserProfile', () => {
  it('displays user name', () => {
    render(<UserProfile user={{ name: 'Alice' }} />);
    expect(screen.getByText('Alice')).toBeInTheDocument();
  });

  it('calls onEdit when button clicked', async () => {
    const onEdit = vi.fn();
    render(<UserProfile user={{ name: 'Alice' }} onEdit={onEdit} />);
    await userEvent.click(screen.getByRole('button', { name: /edit/i }));
    expect(onEdit).toHaveBeenCalledTimes(1);
  });
});
```

### Playwright E2E

```typescript
// tests/auth.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Authentication", () => {
  test("user can log in", async ({ page }) => {
    await page.goto("/login");
    await page.getByLabel("Email").fill("user@example.com");
    await page.getByLabel("Password").fill("password123");
    await page.getByRole("button", { name: "Log in" }).click();

    await expect(page).toHaveURL("/dashboard");
    await expect(page.getByText("Welcome back")).toBeVisible();
  });
});
```

**Page Object Pattern:**

```typescript
// pages/LoginPage.ts
export class LoginPage {
  constructor(private page: Page) {}

  async login(email: string, password: string) {
    await this.page.goto("/login");
    await this.page.getByLabel("Email").fill(email);
    await this.page.getByLabel("Password").fill(password);
    await this.page.getByRole("button", { name: "Log in" }).click();
  }
}
```

### Accessibility Testing

**Automated (catches ~50% of issues):**

```typescript
import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("page should be accessible", async ({ page }) => {
  await page.goto("/");

  const results = await new AxeBuilder({ page }).withTags(["wcag2a", "wcag2aa", "wcag21a", "wcag21aa"]).analyze();

  expect(results.violations).toEqual([]);
});
```

**WCAG Checklist:**

```markdown
## Perceivable

- [ ] All images have alt text
- [ ] Color is not the only indicator
- [ ] Contrast ratio ≥ 4.5:1 (text), ≥ 3:1 (large)
- [ ] Text can be resized to 200%

## Operable

- [ ] All functionality via keyboard
- [ ] No keyboard traps
- [ ] Skip links for navigation
- [ ] Focus indicators visible

## Understandable

- [ ] Language declared
- [ ] Error messages clear
- [ ] Labels on form inputs

## Robust

- [ ] Valid HTML
- [ ] ARIA used correctly
- [ ] Works with assistive tech
```

### Core Web Vitals

**Targets:**

- **LCP** < 2.5s (Largest Contentful Paint)
- **INP** < 200ms (Interaction to Next Paint)
- **CLS** < 0.1 (Cumulative Layout Shift)

**Lighthouse CI:**

```yaml
# lighthouserc.js
module.exports = {
  ci: {
    collect: {
      url: ['http://localhost:3000/', 'http://localhost:3000/about'],
      numberOfRuns: 3,
    },
    assert: {
      assertions: {
        'categories:performance': ['error', { minScore: 0.9 }],
        'categories:accessibility': ['error', { minScore: 0.9 }],
        'first-contentful-paint': ['warn', { maxNumericValue: 2000 }],
        'interactive': ['error', { maxNumericValue: 3500 }],
      },
    },
    upload: {
      target: 'temporary-public-storage',
    },
  },
};
```

### CI Integration

```yaml
# .github/workflows/quality.yml
name: Quality Gates
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4

      - name: Install
        run: pnpm install

      - name: Lint
        run: pnpm lint

      - name: Type Check
        run: pnpm typecheck

      - name: Unit Tests
        run: pnpm test:unit --coverage

      - name: E2E Tests
        run: pnpm test:e2e

      - name: Accessibility
        run: pnpm test:a11y

      - name: Upload Coverage
        uses: codecov/codecov-action@v4
```

### Test Organization

```
tests/
├── unit/           # Fast, isolated
│   └── utils.test.ts
├── integration/    # Multiple units
│   └── api.test.ts
├── e2e/           # Full user flows
│   └── checkout.spec.ts
├── a11y/          # Accessibility
│   └── pages.a11y.ts
└── fixtures/      # Test data
    └── users.json
```

### Code Review Checklist

```markdown
## Functionality

- [ ] Code does what it's supposed to
- [ ] Edge cases handled
- [ ] Error handling appropriate

## Security

- [ ] No secrets in code
- [ ] Input validated
- [ ] Output escaped

## Performance

- [ ] No N+1 queries
- [ ] Expensive operations cached
- [ ] Bundle size acceptable

## Maintainability

- [ ] Code is readable
- [ ] Tests included
- [ ] Types correct
```

## Agents

- **test-writer-fixer** - Test creation, maintenance, CI integration
- **accessibility-specialist** - WCAG compliance, inclusive design

## Deep Dives

- [references/testing-patterns.md](references/testing-patterns.md)
- [references/playwright-guide.md](references/playwright-guide.md)
- [references/accessibility-testing.md](references/accessibility-testing.md)
- [references/performance-optimization.md](references/performance-optimization.md)

## Examples

- [examples/vitest-setup/](examples/vitest-setup/)
- [examples/playwright-suite/](examples/playwright-suite/)
- [examples/a11y-testing/](examples/a11y-testing/)
