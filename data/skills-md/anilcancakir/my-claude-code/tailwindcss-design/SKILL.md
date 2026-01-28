---
name: tailwindcss-design
description: "TailwindCSS implementation patterns for Refactoring UI principles. COMPANION skill for web-design-mastery. ALWAYS activate for: TailwindCSS, Tailwind classes, utility classes, Tailwind config, Tailwind components, Tailwind dark mode, Tailwind responsive, Tailwind spacing, Tailwind typography, Tailwind colors, Tailwind shadows. Provides class recipes, component patterns, dark mode implementation, responsive patterns. Turkish: Tailwind kullanımı, Tailwind class, utility CSS, Tailwind config. English: Tailwind patterns, utility-first CSS, Tailwind best practices."
---

# TailwindCSS Design Patterns

TailwindCSS implementation companion for **web-design-mastery** skill. Translates Refactoring UI principles into Tailwind utility classes.

> **Prerequisite:** This skill provides Tailwind-specific syntax. For design theory and decision-making, reference `web-design-mastery` skill.

---

## ⚠️ CRITICAL: Project Brand Colors First

**ALWAYS check `tailwind.config.js` for custom colors before using generic colors.**

If the project defines `primary`, `secondary`, `brand`, or similar custom colors, **USE THEM**:

```js
// tailwind.config.js
colors: {
  primary: { 50: '...', 500: '...', 900: '...' },
  secondary: { ... },
  brand: { ... }
}
```

**Priority order:**

1. **Project-defined colors** (`primary`, `secondary`, `brand`, `accent`)
2. **Generic Tailwind colors** (`zinc`, `gray`, `slate`) as fallback only

**Usage examples with project colors:**

```html
<!-- ✅ CORRECT: Use project colors -->
<button class="bg-primary-600 hover:bg-primary-700 text-white">
<a class="text-primary-600 hover:text-primary-700">
<div class="border-primary-500 bg-primary-50">
<input class="focus:border-primary-500 focus:ring-primary-500">

<!-- Active/selected states -->
<nav class="bg-primary-50 text-primary-700">

<!-- ❌ AVOID when project colors exist -->
<button class="bg-blue-600">  <!-- Generic, ignores brand -->
<button class="bg-zinc-900">  <!-- Only if no primary defined -->
```

**Rules:**

- Primary = main CTAs, active states, links, focus rings
- Secondary = alternative actions, supporting elements
- Brand/Accent = highlights, decorative elements
- Neutral (zinc/gray) = structure, text, borders only

---

## Spacing Classes (4px Grid)

| Token | Size | Classes | Use Case |
|-------|------|---------|----------|
| 1 | 4px | `gap-1`, `p-1`, `m-1` | Micro gaps |
| 2 | 8px | `gap-2`, `p-2`, `m-2` | Tight, within components |
| 3 | 12px | `gap-3`, `p-3`, `m-3` | Related elements |
| 4 | 16px | `gap-4`, `p-4`, `m-4` | Standard padding |
| 6 | 24px | `gap-6`, `p-6`, `m-6` | Between sections |
| 8 | 32px | `gap-8`, `p-8`, `m-8` | Major separation |
| 12 | 48px | `gap-12`, `p-12` | Large gaps |
| 16 | 64px | `gap-16`, `py-16` | Hero spacing |

**Rule:** Symmetric padding by default. `p-4` not `pt-6 pb-2 pl-4 pr-8`.

---

## Typography Classes

| Size | Class | Use Case |
|------|-------|----------|
| 12px | `text-xs` | Labels, meta, fine print |
| 14px | `text-sm` | Body text, default |
| 16px | `text-base` | Emphasis |
| 18px | `text-lg` | Subheadings |
| 20px | `text-xl` | Card titles |
| 24px | `text-2xl` | Page titles |
| 30px | `text-3xl` | Hero subheading |
| 36px+ | `text-4xl`, `text-5xl` | Hero heading |

**Weight Classes:**

| Role | Class |
|------|-------|
| Body | `font-normal` |
| Labels | `font-medium` |
| Headings | `font-semibold` |

**Tracking (Letter-spacing):**

```html
<!-- Headlines: tighter -->
<h1 class="text-3xl font-semibold tracking-tight">

<!-- All-caps: wider -->
<span class="text-xs font-medium uppercase tracking-wide">
```

---

## Color Hierarchy

### Text Colors (4-Level System)

```html
<!-- Light mode -->
<span class="text-zinc-900">Primary</span>
<span class="text-zinc-600">Secondary</span>
<span class="text-zinc-400">Muted</span>
<span class="text-zinc-300">Faint</span>

<!-- Dark mode -->
<span class="dark:text-zinc-100">Primary</span>
<span class="dark:text-zinc-400">Secondary</span>
<span class="dark:text-zinc-500">Muted</span>
<span class="dark:text-zinc-600">Faint</span>
```

### Status Colors

```html
<span class="text-emerald-600 dark:text-emerald-400">Success</span>
<span class="text-amber-600 dark:text-amber-400">Warning</span>
<span class="text-red-600 dark:text-red-400">Error</span>
<span class="text-blue-600 dark:text-blue-400">Info</span>
```

### Brand Colors (Priority)

Check `tailwind.config.js` first. If `primary`/`secondary` defined, use them:

```html
<button class="bg-primary-600 hover:bg-primary-700">
<a class="text-primary-600 hover:text-primary-700">
<div class="border-primary-500 bg-primary-50">
```

---

## Shadow & Depth Strategies

**Pick ONE per project:**

### Strategy A: Flat (Borders)

```html
<div class="border border-zinc-200 dark:border-zinc-800">
```

### Strategy B: Subtle Lift

```html
<div class="shadow-sm border border-zinc-200/50">
```

### Strategy C: Layered (Premium)

```html
<div class="shadow-sm ring-1 ring-black/5">
```

### Strategy D: Surface Shift

```html
<div class="bg-zinc-50"> <!-- page -->
  <div class="bg-white"> <!-- elevated -->
```

**Shadow Scale:**

| Level | Class | Use Case |
|-------|-------|----------|
| 1 | `shadow-sm` | Cards, buttons |
| 2 | `shadow` | Dropdowns |
| 3 | `shadow-md` | Popovers |
| 4 | `shadow-lg` | Modals |
| 5 | `shadow-xl` | Full-screen overlays |

---

## Component Recipes

### Cards

```html
<!-- Flat -->
<div class="rounded-lg border border-zinc-200 bg-white p-4 dark:border-zinc-800 dark:bg-zinc-900">

<!-- Elevated -->
<div class="rounded-lg bg-white p-4 shadow-sm ring-1 ring-black/5 dark:bg-zinc-900">
```

### Buttons

```html
<!-- Primary -->
<button class="rounded-md bg-zinc-900 px-3 py-1.5 text-sm font-medium text-white hover:bg-zinc-800 dark:bg-zinc-100 dark:text-zinc-900 dark:hover:bg-zinc-200">

<!-- Secondary -->
<button class="rounded-md border border-zinc-300 bg-white px-3 py-1.5 text-sm font-medium text-zinc-700 hover:bg-zinc-50 dark:border-zinc-700 dark:bg-zinc-800 dark:text-zinc-300">

<!-- Ghost -->
<button class="rounded-md px-3 py-1.5 text-sm font-medium text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-zinc-100">
```

### Inputs

```html
<input class="w-full rounded-md border border-zinc-300 bg-white px-3 py-2 text-sm text-zinc-900 placeholder:text-zinc-400 focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-100" />
```

### Navigation Item

```html
<!-- Default -->
<a class="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-zinc-600 hover:bg-zinc-100 hover:text-zinc-900 dark:text-zinc-400 dark:hover:bg-zinc-800 dark:hover:text-zinc-100">

<!-- Active -->
<a class="flex items-center gap-2 rounded-md bg-zinc-100 px-3 py-2 text-sm font-medium text-zinc-900 dark:bg-zinc-800 dark:text-zinc-100">
```

---

## Animation Classes

| Duration | Class | Use Case |
|----------|-------|----------|
| 150ms | `duration-150` | Hovers, toggles |
| 200ms | `duration-200` | Standard transitions |
| 300ms | `duration-300` | Page transitions |

```html
<div class="transition-all duration-200 ease-out">
<div class="transition-colors duration-150">
```

**Staggered Animation:**

```html
<div class="animate-fade-in [animation-delay:0ms]">
<div class="animate-fade-in [animation-delay:50ms]">
<div class="animate-fade-in [animation-delay:100ms]">
```

---

## Dark Mode Pattern

```html
<div class="bg-white dark:bg-zinc-950">
  <h1 class="text-zinc-900 dark:text-zinc-100">
  <p class="text-zinc-600 dark:text-zinc-400">
  <div class="border-zinc-200 dark:border-zinc-800">
```

**Dark mode adjustments:**

- Borders > shadows (shadows less visible)
- Desaturate status colors slightly
- Reduce contrast on secondary elements

---

## Anti-Patterns

```html
<!-- ❌ NEVER -->
<div class="shadow-2xl">           <!-- Too dramatic -->
<button class="rounded-2xl px-3">  <!-- Radius too large for size -->
<div class="pt-8 pb-2 pl-6 pr-3">  <!-- Asymmetric without reason -->
<div class="border-4 border-purple-500"> <!-- Thick decorative -->
<div class="animate-bounce">       <!-- Bouncy in enterprise UI -->

<!-- ✅ INSTEAD -->
<div class="shadow-sm">
<button class="rounded-md px-3">
<div class="p-4">
<div class="border border-zinc-200">
<div class="transition-all duration-200">
```

---

## Reference Files

| Topic | File |
|-------|------|
| Component depth patterns | [depth-strategies.md](references/depth-strategies.md) |
| Complete component library | [components.md](references/components.md) |
| Responsive patterns | [responsive.md](references/responsive.md) |
