---
name: shell-ui
description: Shell module patterns for src/app/shell, covering global UI state, layout composition, navigation, theming with Material Design 3 tokens, and zone-less signal-first presentation boundaries; use when changing app chrome or global UI concerns.
---

# Shell UI

## Intent
Own global application chrome and cross-cutting UI state (navigation, theme, notifications) without leaking business logic.

## Responsibilities
- Layout composition, global navigation, and app-level UI scaffolding.
- Global UI state stores (theme, toasts/snackbars, search UI state) when truly cross-cutting.

## Boundaries
- Shell does not own capability business logic.
- Shell consumes application-facing signals; it does not call repositories directly.

## UI Rules
- Standalone components only.
- Bind templates to signals only using Angular control flow.
- Use Material 3 tokens; avoid hardcoded CSS values for color/typography.

## Navigation
- Prefer router-driven composition and lazy loading.
- Use functional guards/resolvers with `inject()`.

## Accessibility
- Ensure keyboard navigation, focus visibility, semantic landmarks, and skip links for global layout.
