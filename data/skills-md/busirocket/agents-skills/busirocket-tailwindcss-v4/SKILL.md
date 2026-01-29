---
name: busirocket-tailwindcss-v4
description:
  Tailwind CSS v4 setup and styling strategy. Use when configuring Tailwind v4,
  writing component styles, deciding between utility classes and custom CSS, and
  avoiding style drift.
metadata:
  author: cristiandeluxe
  version: "1.0.0"
---

# Tailwind CSS v4 Best Practices

Setup and styling patterns for Tailwind CSS v4 projects.

## When to Use

Use this skill when:

- Setting up Tailwind CSS v4 in a project
- Writing component styles with Tailwind utilities
- Deciding when to extract custom CSS vs using utilities
- Avoiding style drift and maintaining consistency

## Non-Negotiables (MUST)

- Import Tailwind via a single global CSS entry: `@import 'tailwindcss';`
- Keep that global CSS imported from the root layout.
- Prefer Tailwind utilities in `className` for most styling.
- Avoid large custom CSS files; keep custom CSS truly global (resets, tokens).
- Avoid heavy use of arbitrary values unless necessary; prefer consistent
  tokens.

## Class Strategy

- If class strings become hard to read:
  - Extract a small presentational component.
  - Or extract a `components/<area>/...` wrapper rather than inventing large
    custom CSS.

## Rules

### Setup

- `tailwind-setup` - Tailwind CSS v4 setup (single global CSS import)

### Class Strategy

- `tailwind-class-strategy` - Prefer utilities, extract components when needed
- `tailwind-avoid-drift` - Avoid style drift (keep custom CSS global, prefer
  tokens)

### Ordering

- `tailwind-css-ordering` - CSS order depends on import order

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/tailwind-setup.md
rules/tailwind-class-strategy.md
rules/tailwind-avoid-drift.md
```

Each rule file contains:

- Brief explanation of why it matters
- Code examples (correct and incorrect patterns)
- Additional context and best practices
