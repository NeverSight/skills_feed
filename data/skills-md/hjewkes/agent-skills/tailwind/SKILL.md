---
name: tailwind
description: |
  Tailwind CSS v4 with shadcn/ui — setup, configuration, component patterns, dark mode, and troubleshooting.
  Use when setting up Tailwind v4, building UI components, fixing Tailwind errors, migrating from v3, or styling with utility classes.
---

# Tailwind CSS v4

Combined from jezweb/claude-skills (tailwind-v4-shadcn + tailwind-patterns). Production-tested.

## Setup Quick Start

```bash
pnpm add tailwindcss @tailwindcss/vite
pnpm add -D @types/node tw-animate-css
pnpm dlx shadcn@latest init
rm tailwind.config.ts  # v4 doesn't use this
```

Use `@tailwindcss/vite` plugin (NOT PostCSS). Set `"config": ""` in `components.json`.

## The Four-Step CSS Architecture

Skip any step and the theme breaks. See `references/setup.md` for full details.

1. **CSS Variables at `:root`** — define colors with `hsl()` wrapper, NOT inside `@layer base`
2. **`@theme inline`** — map CSS vars to Tailwind utilities (`--color-background: var(--background)`)
3. **`@layer base`** — apply base styles using unwrapped variables
4. **Result** — `bg-background` auto-switches in dark mode, no `dark:` prefix needed

## Critical Rules

**Always**: semantic tokens (`bg-primary` not `bg-blue-500`), mobile-first (`base → sm: → md:`), `hsl()` in `:root`/`.dark`, consistent spacing (4/6/8/12/16/24 scale)

**Never**: `tailwind.config.ts` (v4 ignores it), `@apply` with `@layer` classes (use `@utility`), double-wrap `hsl(var(--color))`, raw colors, `.dark { @theme {} }`, `dark:` variants for semantic colors

## Quick Error Reference

| Symptom | Fix |
|---------|-----|
| `bg-primary` doesn't work | Add `@theme inline` block |
| Colors black/white | Remove double `hsl()` wrap |
| Dark mode stuck | Add ThemeProvider, check `.dark` on `<html>` |
| Build fails | Delete `tailwind.config.ts` |
| Animation errors | Replace `tailwindcss-animate` with `tw-animate-css` |
| `@apply` breaks | Use `@utility` directive instead |
| Base styles ignored | Don't wrap in `@layer base`, define at root |

Full error details with solutions: `references/common-errors.md`

## Component Patterns

Patterns use semantic tokens for automatic dark mode. See `references/patterns.md` for full library.

```tsx
// Container
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

// Responsive grid
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

// Card
<div className="bg-card text-card-foreground rounded-lg border border-border p-6">

// Button
<button className="bg-primary text-primary-foreground px-4 py-2 rounded-md hover:bg-primary/90 transition-colors">
```

## Reference Files

- `references/setup.md` — full 4-step architecture + vite config + components.json
- `references/common-errors.md` — 8 documented v4 errors with solutions
- `references/patterns.md` — layouts, cards, buttons, forms, nav, typography
- `references/dark-mode.md` — ThemeProvider, toggle, OKLCH colors
- `references/migration.md` — v3 → v4 checklist and gotchas
- `templates/` — index.css, components.json, theme-provider.tsx, vite.config.ts, utils.ts
