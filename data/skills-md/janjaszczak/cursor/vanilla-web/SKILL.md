---
name: vanilla-web
description: Build or modify plain HTML/CSS/JavaScript (no framework) using modular ES modules (ESM), SRP, minimal global state, and shippable runnable files with lightweight verification. Use for static pages, small UI widgets, vanilla JS refactors, and quick prototypes without React/Vue/Angular.
compatibility: >
  Cursor Agent Skills (Nightly). Project skill location: .cursor/skills/vanilla-web/SKILL.md.
  Assumes a browser-run environment; optional local server via python3 for manual verification.
metadata:
  author: janjaszczak
  version: "1.0"
---

# Vanilla Web (HTML/CSS/JS)

## Baseline constraints (from the rule)
Use these as non-negotiables:
- "HTML/CSS/JS only (no framework)."
- "Keep JS modular (ESM), split responsibilities (SRP)."
- "Prefer small, focused functions and pure utilities; avoid global state."
- "Ship complete runnable files and minimal tests before marking done."

## When to activate this skill
Activate when the user asks for:
- vanilla JS / plain HTML/CSS/JS / static page
- “no framework”, “no React/Vue/Angular”
- small UI components (modal, tabs, dropdown, form validation) built directly in the DOM
- refactors to remove framework dependencies or reduce JS complexity

## Output expectations
1) Deliver **complete runnable** files (no missing imports/paths, no TODO placeholders).
2) Keep changes **small, testable, and incremental**.
3) Provide a short **runbook**: how to run/verify locally + what to check in DevTools.

## Implementation workflow
### 1) Clarify only what blocks correctness
Ask up to 3 questions *only* if requirements are ambiguous in a way that changes implementation.
Otherwise proceed with explicit assumptions.

### 2) Structure & responsibilities
- Prefer this split:
  - `index.html` (semantic markup)
  - `styles.css` (or `css/…`)
  - `js/main.js` as an ESM entrypoint + `js/modules/*.js` for components/utilities
- SRP: each module does one thing (DOM wiring, state, rendering, API, utilities).
- Avoid global mutable state. If state is needed, encapsulate it in a module and expose minimal functions.

### 3) HTML guidelines
- Use semantic tags (`header`, `main`, `nav`, `button`, `dialog` where applicable).
- Accessibility baseline: keyboard navigation, focus states, ARIA only when needed (don’t ARIA-overuse).

### 4) CSS guidelines
- Prefer simple, predictable naming (BEM-like optional).
- Use CSS variables for theme primitives.
- Keep layout responsive by default (flex/grid + relative units).

### 5) JavaScript guidelines (ESM)
- Use `type="module"` and explicit imports/exports.
- Prefer pure utilities and small functions.
- Use event delegation for lists/dynamic UIs.
- Handle errors explicitly (network failures, missing DOM nodes, invalid inputs).

## Verification checklist
Use the detailed checklist in:
- `references/checklist.md`

When finishing work, ensure:
- No console errors/warnings caused by the change
- All referenced assets resolve (paths/imports)
- Feature works with keyboard and without requiring a framework runtime

## Progressive disclosure
Keep this SKILL.md lean; store deeper examples and checklists under `references/`.
Do not paste large style guides into SKILL.md—link to repo examples instead.

## Suggested companion scripts (optional)
- `scripts/serve.sh` for quick static serving (manual verification)

See:
- `scripts/serve.sh`
