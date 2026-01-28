---
name: css-coder
description: CSS authoring guidance emphasizing web standards, accessibility, and performance. Use when writing, reviewing, or refactoring CSS. Provides patterns, snippets, and conventions that prioritize native CSS over frameworks, semantic structure, and maintainable code. Refer to references/patterns.md for specific patterns and snippets.
---

# CSS Coder

Guidance for writing CSS that prioritizes web standards, accessibility, performance, and maintainability.

## Core Principles

1. **Web standards first** — Use native CSS features before reaching for libraries or frameworks. No Tailwind, no CSS-in-JS unless explicitly requested.
2. **Accessibility as a requirement** — Ensure styles support, never hinder, assistive technologies. Respect user preferences (motion, color scheme, contrast).
3. **Performance matters** — Minimize repaints, avoid layout thrashing, use efficient selectors.
4. **Readable over clever** — Future maintainers (including the author) should understand the code at a glance.
5. **Explicit over implicit** — Avoid magic numbers and unexplained values. Use custom properties for shared values.

## Workflow

1. **Check references first** — Before writing CSS, consult `references/patterns.md` for established patterns and snippets.
2. **Validate against specs** — When uncertain, reference MDN Web Docs or CSS specifications.
3. **Suggest alternatives** — Offer ideas beyond the skill's patterns when appropriate, but always aligned with the core principles above.

## Writing Guidelines

### Selectors

- Prefer class selectors over element or ID selectors for styling.
- Keep specificity low and predictable.
- Avoid deep nesting (aim for 2-3 levels maximum).

### Custom Properties

- Use `--` prefixed custom properties for colors, spacing, typography, and other repeated values.
- Define at `:root` or appropriate scope.
- Name descriptively: `--color-primary`, `--spacing-md`, `--font-size-body`.

### Logical Properties

- Always use logical properties (`margin-inline`, `padding-block`, `inset-inline-start`, `block-size`, etc.) instead of physical properties (`margin-left`, `padding-top`, `left`, `height`, etc.).
- Logical properties support internationalization and different writing modes automatically.
- Only fall back to physical properties where logical equivalents do not yet exist.

### Units

- Use `rem` for typography and spacing (respects user font-size preferences).
- Use `em` for component-relative sizing when appropriate.
- Use viewport units (`vw`, `vh`, `dvh`) thoughtfully, with fallbacks where needed.
- Avoid `px` for font sizes; acceptable for borders, shadows, and fine details.

### Colors

- Use modern space-separated syntax for all color functions (`rgb()`, `hsl()`, `oklch()`).
- Recommend `oklch()` for vibrant or wide-gamut colors.
- Use relative color syntax to derive hover states or transparent variants from existing variables.
- See `references/patterns.md` for syntax examples.

### Layout

- Use CSS Grid for two-dimensional layouts, or when vertical flow is needed without extra declarations.
- Use Flexbox for one-dimensional alignment, noting it defaults to `row` direction.
- Avoid floats for layout (legacy use only).

### Media Queries

- Use modern range syntax: `@media (width < 48rem)`, `@media (width >= 48rem)`.
- Prefer **Shared First** over mobile-first: define shared styles outside queries, scope viewport-specific styles with bounded queries.
- Keep breakpoints to a minimum — add more only when there's a clear need.
- See `references/patterns.md` for detailed examples.

### Accessibility

- Never use `display: none` or `visibility: hidden` to hide content that should remain accessible to screen readers. Use appropriate techniques from the references.
- Respect `prefers-reduced-motion`, `prefers-color-scheme`, and `prefers-contrast`.
- Ensure sufficient color contrast (WCAG AA minimum, AAA preferred).
- Maintain visible focus indicators — never remove `:focus` styles without replacement.

### Performance

- Avoid expensive properties in animations (prefer `transform` and `opacity`).
- Use `will-change` sparingly and only when needed.
- Minimize use of `*` selectors.
- Prefer `@layer` for managing cascade when working with larger codebases.

## References

Consult `references/patterns.md` for:

- Visually-hidden utility
- User preference queries (motion, color scheme, contrast)
- Modern color syntax and relative colors
- Shared First responsive patterns
- Any project-specific conventions

This file will grow as patterns are added. If a needed pattern doesn't exist, suggest one aligned with the core principles.
