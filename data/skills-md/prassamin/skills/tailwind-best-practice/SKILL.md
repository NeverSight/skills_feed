---
name: tailwind-best-practice
description: Tailwind CSS v4 best practices for theming, design tokens, dark mode, gradients, responsive design, and animations. Use when writing, reviewing, or refactoring Tailwind CSS code. Triggers on tasks involving styling, CSS, colors, theming, dark mode, responsive design, gradients, animations, transitions, layout, or UI styling decisions. Also use when setting up a new project's design system or reviewing CSS/Tailwind code quality.
---

# Tailwind CSS v4 Best Practices

Team standard for styling with Tailwind CSS v4 — CSS-first config, design tokens via CSS variables, class-based dark mode.

## No Hardcoded Colors (MANDATORY)

**Never use raw color values in components.** All colors must come from the design token system defined in `globals.css`.

```tsx
// BAD: Hardcoded colors
<div className="bg-blue-500 text-white border-gray-200" />
<div className="bg-[#1a73e8] text-[#ffffff]" />

// GOOD: Semantic token colors
<div className="bg-primary text-primary-foreground border-border" />
```

**Before writing any styles:** Confirm the color theme with the user. Register all colors in `globals.css` as CSS variables, then use them everywhere.

## No Arbitrary Brackets (MANDATORY)

Tailwind v4 dynamically generates values — **stop using `[brackets]` for things Tailwind already supports natively.**

```tsx
// BAD: Arbitrary brackets
<div className="w-[400px] h-[200px] p-[32px] z-[999] bg-primary/[0.08]" />

// GOOD: Native Tailwind v4 values
<div className="w-100 h-50 p-8 z-999 bg-primary/8" />
```

**How it works in v4:**

| Type | Formula | Example |
|------|---------|---------|
| Spacing (w, h, p, m, gap...) | `value × 4px` | `w-100` = 400px, `p-8` = 32px, `w-2500` = 10000px |
| Opacity | Integer = percent | `bg-primary/4` = 4% opacity, `bg-primary/80` = 80% |
| Z-index | Any integer | `z-999`, `z-6969` — no brackets needed |

**Rule:** Only use `[brackets]` when there is truly no Tailwind equivalent (e.g., `grid-cols-[1fr_2fr]`).

## Gradients — Use v4 Syntax (MANDATORY)

Tailwind v4 renamed gradients and added radial/conic support. **Stop using v3 `bg-gradient-to-*`.**

```tsx
// BAD: v3 syntax (no longer valid)
<div className="bg-gradient-to-r from-primary to-secondary" />

// GOOD: v4 syntax
<div className="bg-linear-to-r from-primary to-secondary" />
<div className="bg-linear-45 from-primary via-accent to-secondary" />
<div className="bg-radial from-primary to-transparent" />
<div className="bg-conic-180 from-primary via-accent to-secondary" />
```

| v3 (old) | v4 (new) |
|----------|----------|
| `bg-gradient-to-r` | `bg-linear-to-r` |
| `bg-gradient-to-br` | `bg-linear-to-br` |
| Not available | `bg-linear-45` (any angle) |
| Not available | `bg-radial` |
| Not available | `bg-conic-180` (any angle) |

Gradient stops support positions: `from-primary from-20% via-accent via-60% to-secondary to-100%`

## Theming Setup (MANDATORY)

**First ask the user:** Do you need one theme or two (light + dark)?

Every project must define its color system in `globals.css` using CSS variables + Tailwind's `@theme` directive.

### Single theme (light only)

If the user only needs one theme, define everything in `:root`. No `.dark`, no `@custom-variant`.

```css
/* globals.css */
@import "tailwindcss";

@theme {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  /* ... register all tokens */
}

:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.15 0 0);
  --primary: oklch(0.55 0.2 250);
  --primary-foreground: oklch(1 0 0);
  /* ... see references/theming.md for full token list */
}
```

### Two themes (light + dark)

If the user needs both themes, `:root` = light, `.dark` = dark, plus enable class-based toggle.

```css
@import "tailwindcss";

@theme {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  /* ... register all tokens */
}

/* Light mode */
:root {
  --background: oklch(1 0 0);
  --foreground: oklch(0.15 0 0);
  --primary: oklch(0.55 0.2 250);
  --primary-foreground: oklch(1 0 0);
  /* ... */
}

/* Dark mode */
.dark {
  --background: oklch(0.12 0 0);
  --foreground: oklch(0.95 0 0);
  --primary: oklch(0.65 0.2 250);
  --primary-foreground: oklch(0.1 0 0);
  /* ... */
}

/* Enable class-based dark mode */
@custom-variant dark (&:where(.dark, .dark *));
```

Then use semantic classes everywhere:

```html
<button class="bg-primary text-primary-foreground hover:bg-primary/90">Save</button>
```

For full theming guide, see [references/theming.md](references/theming.md).

## Dark Mode (only when two themes are used)

Class-based toggle via `.dark` on `<html>`. Semantic tokens handle it automatically.

```tsx
// Components automatically adapt — no extra work
<div className="bg-background text-foreground" />  {/* Works in light AND dark */}
```

**Never use `dark:` with hardcoded colors:**

```tsx
// BAD
<div className="bg-white dark:bg-gray-900 text-black dark:text-white" />

// GOOD — tokens handle it
<div className="bg-background text-foreground" />
```

## Component Styling

| Pattern | When to Use |
|---------|-------------|
| Utility classes | Default — most styling |
| `cn()` utility | Conditional/merged classes |
| CSS variables + @theme | Design tokens, theme colors |
| `@variant` | Custom CSS needing Tailwind variants |
| `@apply` | **Rarely** — only base element resets |

## Responsive Design

Mobile-first. Use breakpoint prefixes to scale up:

```tsx
<div className="px-4 md:px-8 lg:px-12" />
<h1 className="text-2xl md:text-4xl lg:text-5xl" />
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3" />
```

Always ascending order: `base → sm: → md: → lg: → xl: → 2xl:`

Tailwind v4 also provides `max-*` and `not-*` variants:

```html
<div class="max-lg:p-8">Below lg only</div>
<div class="not-lg:bg-red-500">When NOT at lg or above</div>
<div class="md:max-xl:flex">Range: md to xl only</div>
```

## Animation

Define custom animations in globals.css via `@theme` + `@keyframes`:

```css
@theme {
  --animate-fade-in: fade-in 0.3s ease-out;
  --animate-slide-up: slide-up 0.3s ease-out;
}
```

```html
<div class="animate-fade-in">Fades in</div>
```

Always respect reduced motion: `motion-safe:animate-fade-in`

For full responsive + animation guide, see [references/responsive-animation.md](references/responsive-animation.md).

## Code Review

Quick checks for Tailwind code:

1. No hardcoded colors? (`bg-blue-500`, `text-[#fff]`)
2. Semantic tokens used? (`bg-primary`, `text-foreground`)
3. `cn()` for conditional classes?
4. Focus styles on all interactive elements?
5. Mobile-first responsive? Breakpoints ascending?
6. Reduced motion respected?

For full checklist, see [references/code-review-checklist.md](references/code-review-checklist.md).
