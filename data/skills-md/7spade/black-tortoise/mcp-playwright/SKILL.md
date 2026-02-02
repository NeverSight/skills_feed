---
name: mcp-playwright
description: Use the Playwright MCP server (@playwright/mcp) for browser-driven verification, screenshots, console logs, and UI flow validation; use when debugging or validating Angular UI behavior beyond unit tests.
---

# MCP Skill: Playwright MCP (UI Verification)

## Scope
Use the MCP server configured as `microsoft/playwright-mcp` in `.vscode/mcp.json` to run browser automation tasks (navigation, screenshots, DOM checks) during debugging and validation.

## Preconditions
- Ensure `.vscode/mcp.json` contains `microsoft/playwright-mcp`.
- Ensure the app is running (typically `pnpm run start`) if you are testing locally.

## Operating Rules
- Prefer resilient selectors: `data-testid`, ARIA roles/labels.
- Avoid brittle CSS selectors and deep DOM coupling.
- Capture evidence for regressions: screenshots + console errors.

## Typical Workflows
1. Smoke check a route
- Navigate to a URL and assert primary heading/landmark is visible.

2. Regression capture
- Take before/after screenshots for a single screen change.

3. Console hygiene
- Collect browser console errors/warnings for a page.

4. Accessibility spot-check
- Verify keyboard focus order for critical controls.

## Prompt Templates
- "Open <url> and verify <expected UI>. Collect console errors and take a full-page screenshot."
- "Run a quick flow: <steps>. Use role-based selectors and fail fast with screenshots on error."

## Related Repo Guidance
- See `.github/skills/e2e-playwright` for test organization and selector rules.
