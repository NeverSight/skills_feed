---
name: tailwind-design-system
description:
  Builds scalable design systems with Tailwind CSS 4 using CSS-based tokens, component patterns, and
  responsive guidelines with accessibility checks. Use when creating component libraries,
  implementing design systems, or refactoring and standardizing UI patterns.
---

# Tailwind Design System

Design tokens, components, and responsive patterns for Tailwind CSS 4 with accessibility in mind.

## When to Use

- Building a new design system or component library with Tailwind CSS 4
- Refactoring UI to standardize patterns and tokens
- Auditing and improving responsive behavior and accessibility

## Inputs to Gather

- Product goals and brand constraints
- Target platforms and browsers
- Existing UI patterns or components to migrate
- Required breakpoints and density targets
- Accessibility requirements (default: best effort)

## Steps

1. **Define tokens (CSS-based config)**
   - Create a single source of truth in a CSS file using `@theme`.
   - Prefer semantic tokens (e.g., `--color-surface`, `--color-text`) mapped to primitives.
   - Keep token names stable and design-system oriented.

2. **Create component patterns**
   - Define base classes in `@layer components`.
   - Keep variants and sizes consistent and composable.
   - Use utilities directly in templates for layout decisions.

3. **Establish responsive rules**
   - Adopt a small set of breakpoints with consistent naming.
   - Use container and spacing tokens to scale layouts.
   - Prefer logical properties when possible for RTL readiness.

4. **Accessibility pass**
   - Ensure visible focus (`:focus-visible`) on interactive elements.
   - Enforce minimum touch target sizes.
   - Respect reduced motion.
   - Keep color contrast readable for text and controls.

5. **Deliverables**
   - Token file (CSS)
   - Component pattern catalog
   - Responsive usage guidelines
   - Accessibility notes and exceptions

## Templates

### Token file (CSS)

```css
@import 'tailwindcss';

@theme {
  /* Color primitives */
  --color-brand-50: #f5f7ff;
  --color-brand-500: #4f46e5;
  --color-neutral-0: #ffffff;
  --color-neutral-950: #0b0b0f;

  /* Semantic colors */
  --color-surface: var(--color-neutral-0);
  --color-surface-muted: #f6f7f9;
  --color-text: var(--color-neutral-950);
  --color-text-muted: #4b5563;
  --color-border: #e5e7eb;
  --color-ring: var(--color-brand-500);

  /* Typography */
  --font-sans: ui-sans-serif, system-ui, sans-serif;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;

  /* Spacing and radius */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-3: 0.75rem;
  --spacing-4: 1rem;
  --radius-sm: 0.375rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;

  /* Shadow */
  --shadow-card: 0 1px 2px rgba(0, 0, 0, 0.08);
}

@layer base {
  :root {
    color: var(--color-text);
    background: var(--color-surface);
  }
}
```

### Component pattern (example)

```css
@layer components {
  .btn {
    @apply inline-flex items-center justify-center gap-2 rounded-md px-4 py-2 text-sm font-medium;
    @apply bg-[var(--color-brand-500)] text-white;
    @apply focus-visible:ring-2 focus-visible:ring-[var(--color-ring)] focus-visible:outline-none;
    @apply disabled:pointer-events-none disabled:opacity-50;
  }

  .btn--ghost {
    @apply bg-transparent text-[var(--color-text)] hover:bg-[var(--color-surface-muted)];
  }

  .card {
    @apply rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] shadow-[var(--shadow-card)];
  }
}
```

### Responsive rules (example)

```md
Breakpoints:

- sm: compact layouts and stacked controls
- md: default desktop baseline
- lg: expanded content density

Layout:

- Use grid for page scaffolding with `gap` tied to spacing tokens
- Avoid fixed heights for content blocks
- Prefer `min-w-0` in flex layouts to avoid overflow
```

### Accessibility checklist (best effort)

```md
- Focus styles visible on all interactive elements
- Minimum target size 44px for touch
- Reduced motion respected (avoid forced animations)
- Text contrast readable on primary surfaces
- Form labels tied to inputs and error text announced
```

## Scripts

Use the token extractor to keep a JSON snapshot of `@theme` tokens:

```bash
node ".cursor/skills/tailwind-design-system/scripts/extract-theme-tokens.mjs" path/to/tokens.css > tokens.json
```

## Examples

### Creating a new token set

1. Create `design-tokens.css` with `@theme`.
2. Add semantic tokens that map to primitives.
3. Generate `tokens.json` using the script above.

### Refactoring a component library

1. Map existing class clusters to new component patterns.
2. Replace raw colors and spacing with tokens.
3. Document variants and states.

## Output

Provide results as:

```
Design System Output
- Tokens file: <path>
- Components added/updated: <list>
- Responsive rules: <summary>
- Accessibility notes: <bullets>
- Open questions: <bullets>
```

## Present Results to User

Return a concise report using the output template above, followed by any recommended next steps
(tests, audits, or migration plan).
