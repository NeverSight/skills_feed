---
name: playwright
description: Canonical Playwright hub for E2E tests and ad-hoc browser automation. Use when the user explicitly mentions "Playwright", "@playwright/test", "npx playwright", "playwright.config.ts", "PWDEBUG", "trace viewer", or "toHaveScreenshot". Avoid using for generic browser automation unless Playwright is requested, and avoid using for pure web scraping.
---

# Playwright

## When to Use This Skill

Use this skill when the user:

### Mentions / keywords

- Mentions “Playwright”, “@playwright/test”, “playwright.config.ts”, “trace viewer”, or “PWDEBUG”
- References `*.spec.ts` / `*.test.ts` files that import `@playwright/test`

### Context

- Is trying to add or maintain E2E/smoke coverage for a web app
- Is trying to debug flaky UI tests (selectors, timing, waits)
- Needs one-off automation (screenshots, console logs, quick flow checks)

## Purpose

- Route Playwright work into the right workflow (suite vs. one-off script vs. debugging)
- Standardize patterns that prevent flaky tests (locators, assertions, waits)
- Keep artifacts in `./tmp/` for predictable cleanup

## Quick routing

- **Writing/maintaining `@playwright/test` suites** → See `references/e2e-with-playwright-test.md`
- **Auth once, reuse state (`storageState`)** → See `references/auth-and-storage-state.md`
- **CI hardening + config knobs** → See `references/ci-and-config.md`
- **Locators, assertions, POM, fixtures** → See `references/patterns.md`
- **Fixtures (worker-scoped, auto fixtures)** → See `references/fixtures.md`
- **Mocking APIs / controlling network** → See `references/api-mocking.md`
- **Visual testing (`toHaveScreenshot`)** → See `references/visual-testing.md`
- **Link checking / dead link detection** → See `references/link-checking.md`
- **Flaky tests / trace viewer / retries** → See `references/debugging.md`
- **One-off automation (screenshots/logs/check flows)** → See `references/ad-hoc-automation.md`

## Non-negotiables

- Prefer `getByRole` / `getByLabel` over CSS/XPath; add `data-testid` only when needed.
- Use web-first assertions (`await expect(locator).toBeVisible()`) instead of boolean checks.
- Never add `waitForTimeout()` to “fix” flake; if you use it temporarily while debugging, remove it before calling the work “done”.
- Don’t default to `networkidle` everywhere; use it intentionally (SPAs / known background activity can make it misleading).
- For CLI agent runs, use minimal reporters to avoid log spam; store artifacts under `./tmp/playwright/`.
- Keep tests independent; avoid cross-test shared state.

## Verification

- E2E suite changes: run `npx playwright test --reporter=line` (or `--reporter=dot`) and confirm failures reproduce.
- Flake fixes: run the previously failing test at least 5 times (ex: `--repeat-each 5`) before calling it fixed.
- CI-sensitive changes: run the suite in “CI-like” settings (ex: `CI=1 npx playwright test --reporter=line`) and confirm it still behaves.

## Provenance

- Consolidated from upstream installed skills: `playwright-best-practices`, `playwright-testing`, `playwright-expert`, `playwright-skill`, `webapp-testing`
