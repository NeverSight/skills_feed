---
name: web-components
description: Create or modify vanilla HTML/CSS/JavaScript (without a framework) using modular ES modules (ESM), vanilla technologies, clean and readable code, ready for production (no transpiling). Useful for lightweight, high-performance pages, dependency-free UI widgets, standard JavaScript refactoring, and rapid prototyping without using frameworks like React, Angular or Vue.
compatibility: opencode
metadata:
  author: manzdev
  version: "1.0"
---

# Vanilla Web (HTML/CSS/JS)

## Required constraints (non-negotiables)

- HTML/CSS/JS only (no framework)
- Use modular JS (ESM)
- Prefer small, focused functions and pure utilities
- Avoid global state

## When to activate this skill (user asks for)

- Vanilla JS / plain HTML/CSS/JS / static page / efficient
- no framework, no React/Angular/Vue
- small UI components (modals, tabs, dropdown, form validation) built directly in the DOM
- refactors to remove framework dependencies or reduce JS complexity

## Output expectations

- Avoid missing imports or paths
- Avoid TODO placeholders
- Keep changes small, testable, and incremental

## Implementation workflow

### 1) Structure

- Prefer this structure:
  - `src/` source code
  - `public/` static files (fonts, images, etc...)
  - `index.html` main entrypoint
  - `main.js` main JS entrypoint
  - `src/css/global.css` global styles
  - `src/components/` webcomponents folder
  - `src/modules/` reusable and utilities modules JS
- Each module does one thing (DOM wiring, module state, rendering, API, utilities...)
- Avoid global mutable state. If state is needed, encapsulate it in a module and expose minimal functions.

- Use always this name convention for filenames:
  - `src/components/` components should use PascalCase. Class name should match with filename. Same with css files.
  - `src/modules/` modules should use camelCase. Function names should match with filename.

### 2) HTML guidelines

- Use semantic tags (`<header>`, `<footer>`, `<article>`, `<main>`, `<nav>`, `<button>`, `<dialog>`, etc... where applicable)
- Avoid soup of divs (reduce to essential elements)

### 3) DOM guidelines

- Use `CSSStyleSheet` API for create styles instead string templates.
- Prefer `import` attributes `with` over `new CSSStyleSheet()`. Prefer `new CSSStyleSheet()` over plain string templates.
- Use `querySelector*()` API instead `getElement*()` API.
- Use `setHTMLUnsafe()` / `getHTML()` instead `innerHTML`.
- Prefer modern DOM API for add elements: `append()`, `prepend()`, `before()`, `after()`. Else, `insertAdjacent*()` over old API `appendChild()`.

### 4) CSS guidelines

- Prefer simple, predictable naming
- Prefer `@scope` rules instead BEM naming
- Use CSS variables for theme primitives and very common reusable data
- Keep layout responsive by default (flex/grid)
- Prefer `:where()` low specificity over `!important`
- Use CSS nesting for group related-block classes

### 5) Javascript guidelines

- Use `type="module"` and explicit imports/exports
- Prefer naming imports over default imports
- Prefer pure utilities and small functions
- Use event delegation for lists/dynamics UIs
- Handle errors explicity (network failures, missing DOM nodes, invalid inputs)
- Create small class methods for split logic
- Prefix code string template with `/* html */`, `/* css */` or `/* svg */`

## Verification checklist

When finishing work, ensure:

- No console errors/warnings caused by changes
- All referenced assets resolve (paths/imports)
- Review the imported items to check if they are being used
- Feature works with keyboard and without requiring a framework runtime

## Suggested scripts

- Add a `npm run dev` using `servor` local server development
