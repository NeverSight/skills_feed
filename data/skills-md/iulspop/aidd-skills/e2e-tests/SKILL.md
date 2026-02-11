---
name: e2e-tests
description: Generates end-to-end tests using Playwright with the "given/should" prose format. Use when writing e2e tests for user flows, page interactions, or integration scenarios that exercise the full application stack.
---

# E2E Tests

Act as a top-tier software engineer with serious testing skills.

Write e2e tests for: $ARGUMENTS

Each test must answer these 5 questions:

1. What is the user flow under test? (test should be in a named describe block)
2. What is the expected behavior? ($given and $should arguments are adequate)
3. What actions does the user perform? (navigations, clicks, form fills, etc.)
4. What is the expected outcome? (visible elements, URLs, toasts, database state)
5. How can we find the bug? (implicitly answered if the above questions are answered correctly)

## Rules

- Use Playwright with test, expect, and test.describe.
- Tests must use the "given: ..., should: ..." prose format.
- Test files live in `playwright/` directory, organized by feature subdirectories.
- Test files use the `.e2e.ts` extension.
- Prefer accessible locators: `getByRole`, `getByLabel`, `getByText` over CSS selectors.
- Use `getByRole` with name option as the primary locator strategy.
- When accessible locators are insufficient, use `data-testid` attributes via `getByTestId`.
- Never use CSS class selectors for test locators — classes are for styling, not testing.
- Define `data-testid` values as named exports in a shared constants file (e.g. `app/test/test-ids.ts`) and import them in both the component and the test.
- Use regex with case-insensitive flag for text matching: `{ name: /submit/i }`.
- Await all Playwright actions and assertions.
- Use `toBeVisible()` and `toBeHidden()` for element presence checks.
- Use `toHaveURL()` or a `getPath(page)` helper for URL assertions.
- Handle auth setup in helper functions, not inline in every test.
- Clean up test data in teardown — don't leave state for the next test.
- Each test should be independent and not depend on other tests' state.
- Use `test.step("description", async () => { ... })` to organize logical phases within a test — never use inline comments like `// Open notifications panel` as step separators.
- Block images in performance-sensitive tests via `page.route`.
- Use `test.describe` blocks to group related scenarios.
- Assert toast notifications via `getByRole("region", { name: /notifications/i })`.
- For forms, use `getByRole("textbox", { name: /label/i })` and `.fill()`.
- For dropdowns, use `getByRole("combobox")` then `getByRole("option")`.
- For accessibility checks, use `@axe-core/playwright` with `expect(results.violations).toEqual([])`.
- Create reusable setup/teardown helpers for common flows (login, org creation, etc.).
- Use factories from the codebase to create test data — never hardcode full objects.
- Verify database state after mutations using model functions from infrastructure layer.

## When NOT to use this skill

- For pure function tests (`.test.ts`), use `/unit-tests` instead.
- For React component render tests (`.test.tsx`), use `/happy-dom-tests` instead.
- For server action or database tests (`.spec.ts`), use `/integration-tests` instead.
- This skill is for Playwright browser tests (`.e2e.ts`) only.
