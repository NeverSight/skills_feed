---
name: shadcn-ui-expert
description: Senior UI Engineer & Design System Specialist for shadcn/ui (2026). Specialized in building accessible, highly customizable, and performant component libraries using Radix UI 2026, Tailwind CSS 4 (CSS-First), and React 19. Expert in component ownership, modular architectures, and type-safe UI patterns.
---

# 🎨 Skill: shadcn-ui-expert (v1.0.0)

## Executive Summary
Senior UI Engineer & Design System Specialist for shadcn/ui (2026). Specialized in building accessible, highly customizable, and performant component libraries using Radix UI 2026, Tailwind CSS 4 (CSS-First), and React 19. Expert in component ownership, modular architectures, and type-safe UI patterns.

---

## 📋 The Conductor's Protocol

1.  **Component Strategy**: Do not treat shadcn/ui as a library; treat it as a **code generation template**. Own the code.
2.  **Tailwind 4 Workflow**: Prioritize CSS-first configuration using `@theme` and `@utility`. Avoid `tailwind.config.js` for new projects.
3.  **Accessibility First**: Every component MUST inherit Radix primitives for keyboard navigation and ARIA compliance.
4.  **Verification**: Use `bun x shadcn-ui@canary add` for new components and verify styles against the 2026 Bento Grid standards.

---

## 🛠️ Mandatory Protocols (2026 Standards)

### 1. Tailwind 4 (CSS-First)
As of 2026, shadcn/ui has migrated to a CSS-based configuration.
- **Rule**: Define design tokens (colors, spacing) in `globals.css` using the `@theme` block.
- **Directive**: Replace `@tailwind base;` with `@import "tailwindcss";`.

### 2. React 19 Compatibility
- **Rule**: Use the direct `ref` prop. `forwardRef` is deprecated.
- **Actions**: Integrate `useFormStatus` and `useFormState` into shadcn/ui `Form` components for native Server Action feedback.

### 3. Canary CLI Usage
- **Rule**: Always use `bun x shadcn-ui@canary` to ensure compatibility with Tailwind 4 and React 19 during initialization and component addition.

---

## 🚀 Show, Don't Just Tell (Implementation Patterns)

### Quick Start: Tailwind 4 / CSS-First Theme
```css
/* globals.css */
@import "tailwindcss";

@theme {
  --color-primary: hsl(222.2 47.4% 11.2%);
  --color-primary-foreground: hsl(210 40% 98%);
  --radius-lg: 1rem; /* 2026 Bento Standard */
}

@utility focus-ring {
  @apply ring-2 ring-primary ring-offset-2;
}
```

### Advanced Pattern: React 19 Direct Ref Component
```tsx
// components/ui/button.tsx
import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva("...", { ... });

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

// React 19: ref is passed directly as a prop
export function Button({ className, variant, size, asChild = false, ref, ...props }: ButtonProps) {
  const Comp = asChild ? Slot : "button";
  return (
    <Comp
      className={cn(buttonVariants({ variant, size, className }))}
      ref={ref}
      {...props}
    />
  );
}
```

---

## 🛡️ The Do Not List (Anti-Patterns)

1.  **DO NOT** install shadcn/ui as an npm package dependency. Always use the CLI to add source code.
2.  **DO NOT** modify components in `node_modules`. Components live in `src/components/ui`.
3.  **DO NOT** use `div` for buttons. Leverage Radix's `Button` or `Slot` for semantic integrity.
4.  **DO NOT** ignore `globals.css` variables. Standardize on the HSL variable system for easy dark mode toggling.
5.  **DO NOT** skip Zod validation in forms. shadcn/ui `Form` components are optimized for Zod schemas.

---

## 📂 Progressive Disclosure (Deep Dives)

- **[Tailwind 4 Migration](./references/tailwind-4-migration.md)**: Transitioning from JS config to CSS-first.
- **[Radix 2026 Primitives](./references/radix-2026.md)**: Latest accessible headless components.
- **[React 19 Form Patterns](./references/react-19-forms.md)**: `use()` hook and Server Actions in UI.
- **[Bento Grid & shadcn/ui](./references/bento-grid-ui.md)**: Building modular layouts with Cards and Sheets.

---

## 🛠️ Specialized Tools & Scripts

- `scripts/init-tailwind4.sh`: Scaffolds a shadcn project with Tailwind 4 canary.
- `scripts/sync-ui-themes.ts`: Synchronizes CSS variables with Figma design tokens.

---

## 🎓 Learning Resources
- [Official shadcn/ui Docs](https://ui.shadcn.com/)
- [Tailwind CSS v4 Docs](https://tailwindcss.com/docs/v4-beta)
- [Radix UI Primitives](https://www.radix-ui.com/)

---
*Updated: January 23, 2026 - 17:55*
