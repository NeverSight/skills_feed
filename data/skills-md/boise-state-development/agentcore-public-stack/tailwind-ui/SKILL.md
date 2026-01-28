---
name: tailwind-ui
description: Tailwind CSS v4.1 best practices with WCAG 2.1 AA accessibility, theming, and dark mode support. Use when working with HTML, CSS, styling components, accessibility (a11y), WCAG compliance, color contrast, focus states, screen readers, theming, light mode, dark mode, or building accessible UI patterns like buttons, forms, cards, and navigation. Complements the angular-best-practices skill for Angular frontends.
---

# Tailwind UI Skill

Tailwind CSS v4.1 development with accessibility and theming baked in.

## Quick Reference

### v4.1 Critical Changes

Never use deprecated utilities — always use replacements:

| Deprecated | Replacement |
|------------|-------------|
| `bg-opacity-*` | `bg-black/50` (opacity modifier) |
| `bg-gradient-*` | `bg-linear-*` |
| `shadow-sm` | `shadow-xs` |
| `shadow` | `shadow-sm` |
| `rounded-sm` | `rounded-xs` |
| `rounded` | `rounded-sm` |
| `ring` | `ring-3` |
| `outline-none` | `outline-hidden` |
| `leading-*` | Use `text-base/7` line-height modifiers |
| `flex-shrink-*` / `flex-grow-*` | `shrink-*` / `grow-*` |
| `space-x-*` in flex/grid | Use `gap-*` instead |

### Essential Patterns

```html
<!-- Gap over space utilities -->
<div class="flex gap-4">...</div>

<!-- Opacity modifiers -->
<div class="bg-primary-500/60">...</div>

<!-- Line height modifiers -->
<p class="text-base/7">...</p>

<!-- Dynamic viewport height (mobile-safe) -->
<div class="min-h-dvh">...</div>

<!-- Size utility for equal dimensions -->
<div class="size-12">...</div>
```

## Reference Files

Load these based on the task:

- **[references/v4-migration.md](references/v4-migration.md)** — Full v4.1 breaking changes, upgrade process, new features
- **[references/accessibility.md](references/accessibility.md)** — WCAG 2.1 AA patterns: contrast, focus, screen readers
- **[references/theming.md](references/theming.md)** — @theme setup, CSS variables, light/dark mode
- **[references/components.md](references/components.md)** — Accessible component patterns (buttons, forms, cards, nav)

## Theme Asset

- **[assets/theme-starter.css](assets/theme-starter.css)** — Starter @theme with primary/secondary/tertiary color scales

## Core Principles

1. **Use Tailwind's scale** — Avoid arbitrary values like `ml-[16px]`; use `ml-4`
2. **Never use @apply** — Use CSS variables or framework components
3. **Gap over margins** — Use `gap-*` in flex/grid, not `space-*` or child margins
4. **Test both modes** — Always verify light AND dark mode appearance
5. **Accessibility first** — Every interactive element needs visible focus states and proper contrast
