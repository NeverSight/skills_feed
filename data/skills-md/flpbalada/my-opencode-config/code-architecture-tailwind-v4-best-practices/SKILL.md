---
name: code-architecture-tailwind-v4-best-practices
description: Guides Tailwind CSS v4 patterns for buttons and components. Use this skill when creating components with variants, choosing between CVA/tailwind-variants, or configuring Tailwind v4's CSS-first approach.
---

# Tailwind CSS v4: Best Practices

## Core Principle

**Use utilities directly in markup as the primary approach. Abstract with CVA/tailwind-variants only when you have 3+ variants.**

Tailwind v4's CSS-first configuration eliminates `tailwind.config.js` entirely. All configuration happens in CSS via `@theme` directive.

## The CSS-First Setup

```css
@import "tailwindcss";

@theme {
  --color-brand-primary: oklch(0.65 0.24 354.31);
  --color-brand-secondary: oklch(0.72 0.11 178);
  --font-sans: "Inter", sans-serif;
  --radius-button: 0.5rem;
}
```

Key v4 changes:
- Single `@import "tailwindcss"` replaces three `@tailwind` directives
- `--color-*` generates color utilities AND exposes as CSS variables
- Automatic template discovery (respects `.gitignore`)
- Oxide engine: 3.5x faster full builds, 8x faster incremental

## When to Abstract

### ✅ Use Pure Utilities When

- Component has 1-2 variants
- Prototyping or simple components
- Bundle size is critical (0KB overhead)

```tsx
// ✅ Simple button - no abstraction needed
<button className="
  inline-flex items-center justify-center gap-2
  px-4 py-2
  bg-blue-500 hover:bg-blue-600 active:bg-blue-700
  text-white text-sm font-medium
  rounded-md transition-colors
  focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-500
  disabled:opacity-50 disabled:pointer-events-none
">
  Save Changes
</button>
```

### ✅ Use CVA When

- 3+ variants needed
- Type safety required
- Building component library
- ~1KB bundle cost acceptable

```typescript
import { cva, type VariantProps } from 'class-variance-authority';

const buttonVariants = cva(
  // Base classes
  "inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        primary: "bg-blue-500 text-white hover:bg-blue-600",
        secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300",
        outline: "border-2 border-blue-500 text-blue-500 hover:bg-blue-50",
        ghost: "text-blue-500 hover:bg-blue-50"
      },
      size: {
        sm: "h-8 px-3 text-xs",
        md: "h-10 px-4 text-sm",
        lg: "h-12 px-6 text-base"
      }
    },
    defaultVariants: {
      variant: "primary",
      size: "md"
    }
  }
);

export type ButtonProps = VariantProps<typeof buttonVariants>;
```

### ✅ Use Tailwind-Variants When

- Responsive variants needed
- Multi-part/slot components (cards, accordions)
- Component composition via `extend`
- ~4KB bundle cost acceptable

```typescript
import { tv, type VariantProps } from 'tailwind-variants';

const card = tv({
  slots: {
    base: 'rounded-lg border bg-card shadow-sm',
    header: 'flex flex-col space-y-1.5 p-6',
    title: 'text-2xl font-semibold',
    content: 'p-6 pt-0',
    footer: 'flex items-center p-6 pt-0'
  },
  variants: {
    variant: {
      elevated: { base: 'shadow-xl' },
      flat: { base: 'shadow-none border' }
    }
  }
});

const { base, header, title, content, footer } = card({ variant: 'elevated' });
```

### ❌ Don't Use @apply

The Tailwind team discourages `@apply` except in narrow circumstances. Use component abstractions instead.

```css
/* ❌ Avoid - hides styling decisions, breaks variant support */
.btn-primary {
  @apply bg-blue-500 text-white px-4 py-2 rounded;
}

/* ✅ Use @utility for custom utilities if absolutely needed */
@utility btn-base {
  display: inline-flex;
  align-items: center;
  padding: 0.5rem 1rem;
  border-radius: 0.5rem;
}
```

## Decision Matrix

| Approach | Bundle | Type Safe | Use Case |
|----------|--------|-----------|----------|
| Pure Tailwind | 0KB | ❌ | Simple, 1-2 variants, prototyping |
| CVA | ~1KB | ✅ | Component libraries, most projects |
| Tailwind-variants | ~4KB | ✅ | Complex design systems, slots |

## State Management with Data Attributes

V4 supports native data attributes for clean state management:

```tsx
export function Button({ isLoading, isDisabled, children }: ButtonProps) {
  return (
    <button
      data-loading={isLoading ?? ""}
      data-disabled={isDisabled ?? ""}
      className="
        bg-blue-500 text-white px-4 py-2 rounded
        hover:bg-blue-600
        data-loading:opacity-50 data-loading:cursor-wait
        data-disabled:opacity-50 data-disabled:pointer-events-none
      "
    >
      {isLoading && <Spinner className="mr-2" />}
      {children}
    </button>
  );
}
```

Custom variants via `@custom-variant`:

```css
@custom-variant selected-not-disabled (&[data-selected]:not([data-disabled]));
```

## Modern React Pattern (shadcn/ui style)

```tsx
import { tv, type VariantProps } from 'tailwind-variants';

const buttonStyles = tv({
  base: "inline-flex items-center justify-center rounded-md font-medium transition-colors",
  variants: {
    variant: {
      primary: "bg-blue-500 text-white hover:bg-blue-600",
      secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300"
    },
    size: {
      sm: "h-8 px-3 text-xs",
      md: "h-10 px-4 text-sm"
    }
  }
});

type ButtonProps = React.ComponentProps<"button"> &
  VariantProps<typeof buttonStyles>;

export function Button({ variant, size, className, ...props }: ButtonProps) {
  return (
    <button
      data-slot="button"
      className={cn(buttonStyles({ variant, size }), className)}
      {...props}
    />
  );
}
```

## Accessibility Checklist

```tsx
<button
  type="button"
  disabled={disabled || loading}
  aria-disabled={disabled || loading}
  aria-busy={loading}
  aria-label={ariaLabel}
  className={buttonStyles({ variant, size })}
>
  {loading && <Spinner aria-hidden="true" />}
  {leftIcon && <span data-slot="icon">{leftIcon}</span>}
  <span data-slot="label">{children}</span>
</button>
```

## Breaking Changes from v3

| v3 | v4 |
|----|-----|
| `shadow-sm` | `shadow-xs` |
| `rounded-sm` | `rounded-xs` |
| `bg-opacity-50` | `bg-black/50` |
| `bg-gradient-to-r` | `bg-linear-to-r` |
| `border` (gray-200 default) | `border` (currentColor) |
| `ring` (3px blue-500) | `ring-3` (currentColor) |

Automated migration: `npx @tailwindcss/upgrade`

## Quick Reference

### DO

- Use utilities directly for simple components
- Wait for **3+ variants** before using CVA/tailwind-variants
- Use **data attributes** for state management
- Follow **shadcn/ui patterns** for React components
- Use **@theme** for design tokens (generates utilities + CSS vars)

### DON'T

- Use `@apply` for component styles
- Abstract prematurely (same rule as code abstractions)
- Mix approaches inconsistently within a project
- Forget accessibility attributes on interactive elements

## Recommended Stack (2025)

- **React**: Next.js 15 + shadcn/ui + CVA + Tailwind v4
- **Vue**: Vue 3 + shadcn/vue + Tailwind v4
- **Bundle**: CVA (~1KB) + clsx (~0.2KB) + tailwind-merge (~7KB) ≈ 8KB total

## References

- [Tailwind CSS v4 Docs](https://tailwindcss.com/docs)
- [CVA (class-variance-authority)](https://cva.style/docs)
- [Tailwind Variants](https://www.tailwind-variants.org/)
- [shadcn/ui](https://ui.shadcn.com/)
