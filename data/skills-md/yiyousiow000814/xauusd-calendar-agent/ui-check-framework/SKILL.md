---
name: ui-check-framework
description: Build or extend an extensible UI self-check framework for Web UIs (React/Vite or plain HTML) using Playwright. Use when asked to add/upgrade ui-check or ui-watch flows, enforce data-qa/data-testid discovery, add theme/contrast checks, animation verification, loading state-machine checks, layout stability/overlap checks, modal scroll rules, or to document QA tagging standards and UI testing commands.
---

# UI Check Framework

## Overview

Create or refine an automated UI self-check system that discovers UI blocks via data-qa
tags and enforces behavioral/visual contracts (themes, animations, loading, layout
stability, modal usability, error visibility). The framework must scale to new cards,
modals, toasts, and actions without writing new test cases each time.

## Workflow (use in order)

1) **Inspect existing scaffolding**
   - Prefer reusing the project's `ui-tests/` folder if it exists.
   - Read `ui-tests/docs/UI_TESTING.md` and `ui-tests/docs/QA_TAGGING.md` if present.
   - Confirm scripts in root `package.json` (`ui:test`, `ui:update-baseline`,
     `ui:report`, `ui:check`, `ui:watch`) point at Playwright flows.

2) **Enforce discovery**
   - Auto-collect all `data-qa` or `data-testid` elements that start with `qa:`.
   - Capture component screenshots (cards, modals, menus, toolbars, toasts) at
     small/medium/large sizes.
   - For modals: verify internal scroll, single close button, and header visibility
     at small window height.

3) **Enforce contracts (generic, not hardcoded)**
   - Theme contrast/readability for dark/light/system (see references).
   - Animation/motion checks for spinners, transitions, toasts.
   - Loading state machine for async actions: idle -> loading -> success/error -> idle.
   - Layout stability (no layout shift for transient status/toasts).
   - Overlap detection for action buttons and modal header/footer.
   - Error visibility and blank-page detection.

4) **Wire UI hooks for automation**
   - Add minimal `window.__ui_check__` helpers (e.g., append log, trigger toast) to
     make contracts testable without hardcoding selectors.
   - Add required `data-qa` tags to new cards/modals/actions as they appear.

5) **Artifacts and reporting**
   - Store artifacts under `artifacts/ui-check/` (snapshots, frames, video, report.html).
   - Ensure `ui:check` is interactive (open/close modal, hover/press, theme toggle, scroll).

## Project-specific anchors

- Primary UI tests live in `ui-tests/` and use Playwright.
- Use `ui-tests/scripts/ui-check.mjs` and `ui-tests/scripts/ui-watch.mjs` as the
  interactive validation entry points.
- Keep user-facing docs in `ui-tests/docs/UI_TESTING.md` and
  `ui-tests/docs/QA_TAGGING.md`.

## References

- `references/workflow.md` - extension workflow and verification checklist.
- `references/qa-tagging.md` - required QA tokens and naming conventions.
- `references/contracts.md` - required generic contracts and how to check them.
