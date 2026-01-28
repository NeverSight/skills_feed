---
name: tailwind4-expert
id: tailwind4-expert
version: 1.2.0
description: "Senior expert in Tailwind CSS 4.0+, CSS-First architecture, and modern Design Systems. Use when configuring themes, migrating from v3, or implementing native container queries."
---

# 🎨 Skill: tailwind4-expert

## Description
Senior specialist in Tailwind CSS 4.0+, focused on the high-performance "Oxide" engine and CSS-first configuration. This skill guides the elimination of JavaScript-heavy build steps in favor of native CSS variables and lightning-fast compilation.

## Core Priorities
1.  **CSS-First Configuration**: Moving all tokens to `@theme` and abandoning `tailwind.config.js`.
2.  **Performance Optimization**: Leveraging the Rust-based engine for sub-10ms incremental builds.
3.  **Modern CSS Features**: Utilizing native Container Queries, 3D transforms, and `@utility` without plugins.
4.  **Design System Integrity**: Enforcing a strict token-based workflow using CSS variables.

## 🚀 Top 5 Gains in Tailwind 4.0

1.  **Zero-JS Config**: The configuration *is* the CSS. No more context-switching between JS and CSS files.
2.  **Built-in Container Queries**: Native support for `@container` and variants like `@md:grid-cols-2`.
3.  **Dynamic Utilities**: Automatic generation of complex utilities like `grid-cols-(--my-grid-count)`.
4.  **Native 3D Transforms**: Utilities like `rotate-x-45` and `perspective-1000` work out of the box.
5.  **Composability by Default**: Every utility is designed to be composed without conflict using the new Oxide engine logic.

## 🛠️ Implementation Example: The Modern Layout (2026)

Combining Container Queries, 3D Transforms, and `@theme` variables for a cutting-edge UI.

```tsx
// 1. Define tokens in globals.css
// @theme { --color-neon: #00f0ff; --perspective-deep: 1200px; }

export function ModernCard() {
  return (
    <div className="@container perspective-(--perspective-deep) p-8">
      <div className="
        group relative transform-3d transition-all duration-500
        hover:rotate-y-12 hover:rotate-x-6
        bg-zinc-900 border border-white/10 rounded-2xl
        p-4 @md:p-8 @lg:p-12
      ">
        <div className="text-zinc-400 @md:text-lg @lg:text-2xl font-medium">
          Responsive to Parent
        </div>
        
        <div className="mt-4 h-1 bg-neon shadow-[0_0_15px_var(--color-neon)]" />
        
        <div className="mt-8 grid grid-cols-1 @md:grid-cols-3 gap-4">
          <div className="aspect-square bg-white/5 rounded-lg" />
          <div className="aspect-square bg-white/5 rounded-lg" />
          <div className="aspect-square bg-white/5 rounded-lg" />
        </div>
      </div>
    </div>
  )
}
```

## Table of Contents & Detailed Guides

### 1. [Migration from v3 to v4](./references/1-migration.md) — **CRITICAL**
- Automated upgrade tool (`npx @tailwindcss/upgrade`)
- Manual migration: Removing `tailwind.config.js`
- PostCSS vs. Lightning CSS integration

### 2. [The @theme Block & Design Systems](./references/2-design-system.md) — **CRITICAL**
- Defining colors, fonts, and spacing tokens
- Overriding vs. Extending the default theme
- Using CSS variables (`var(--color-*)`) instead of `theme()`

### 3. [Advanced Layout & Container Queries](./references/3-layout-and-containers.md) — **HIGH**
- Native Container Query variants (`@md:`, `@lg:`)
- Complex Grid configurations with dynamic variables
- 3D Transforms and Perspective

### 4. [Custom Utilities & @utility](./references/4-custom-utilities.md) — **MEDIUM**
- The new `@utility` directive syntax
- Handling functional/dynamic values in custom classes
- Avoiding arbitrary values with local theme variables

## Quick Reference: The "Do's" and "Don'ts"

| **Don't** | **Do** |
| :--- | :--- |
| `tailwind.config.js` | `@theme { ... }` in CSS |
| `@tailwind base; @tailwind components;` | `@import "tailwindcss";` |
| `theme('colors.brand')` | `var(--color-brand)` |
| `arbitrary-vals-[123px]` | Define in `@theme` or local `--variable` |
| `npm install @tailwindcss/container-queries` | Use native `@md:` variants |
| `import { ... } from 'tailwind-merge'` | Trust the Oxide engine for composition |

---
*Optimized for Tailwind CSS 4.0+ and Lightning CSS.*
*Updated: January 22, 2026 - 14:59*
