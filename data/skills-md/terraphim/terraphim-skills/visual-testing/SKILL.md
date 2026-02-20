---
name: visual-testing
description: |
  Design and implement visual regression testing for UI changes. Defines
  screenshot coverage, rendering stabilization, baseline management, and CI
  integration (e.g., Playwright screenshots, Percy/Chromatic). Use when
  UI/styling/layout changes need protection against regressions, or when adding
  screenshot-based tests to a web/WASM/desktop UI.
license: Apache-2.0
---

# Visual Testing

## Overview

You are a visual QA engineer. Prevent unintended UI changes by establishing
repeatable visual baselines and diff-based tests.

## Inputs (Ask If Missing)

- UI type: Web/WASM, component library, desktop (e.g., GPUI)
- Existing test runner: Playwright/Cypress/Webdriver/Storybook/etc.
- CI environment constraints: fonts, GPU/renderer, headless support
- The specific UI changes (screens, components, states)

## Core Principles

1. **Determinism beats coverage**: a stable test is better than a broad flaky one.
2. **Smallest stable surface**: snapshot components/states, not entire apps, when possible.
3. **Interaction ≠ pixels**: keep e2e interaction assertions separate from pixel diffs.
4. **Baselines are reviewed artifacts**: never update blindly.

## Workflow

### 1) Select Visual Surfaces

Prioritize:
- Critical user flows and top-level pages
- Components with frequent styling changes
- Error/empty/loading states
- Responsive breakpoints and themes (light/dark) if applicable

### 2) Stabilize Rendering

- Fixed viewport and device scale
- Disable animations, transitions, blinking caret
- Deterministic data (fixtures/mocks, seeded DB)
- Stable fonts (bundle or ensure CI installs the same fonts)

### 3) Implement Visual Tests

Default choice for web/WASM UIs: **Playwright** (if present).

Example snippet (adapt to repo conventions):

```ts
// @playwright/test
await page.setViewportSize({ width: 1280, height: 720 });
await page.goto("/settings");
await expect(page.getByRole("main")).toHaveScreenshot("settings.png");
```

If the project already uses another tool (Cypress, Storybook snapshots, Percy,
Chromatic), extend that instead of introducing a new framework.

### 4) Baseline & Review Policy

- Store baselines in-repo (or via a review service) and review diffs in PRs.
- Require explicit “baseline update” notes in the PR when changes are expected.

### 5) CI Integration

- Run visual tests on PRs that touch UI code.
- Upload diff artifacts on failure (screenshots, HTML report).

## Visual Regression Plan Output

```markdown
# Visual Regression Plan: {change}

## Coverage
- Pages/components:
- States:

## Determinism Controls
- Viewport:
- Animations:
- Data:
- Fonts:

## Baseline Policy
- Where stored:
- When to update:
- Review requirements:

## Execution
- Local command:
- CI job:
```

## Constraints

- Avoid pixel diffs for highly dynamic surfaces unless you can stabilize them.
- Do not introduce a new framework if one already exists; extend the current stack.
