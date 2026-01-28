---
name: tailwind-react
description: >
  Patterns for using Tailwind CSS with React components.
  Trigger: When using Tailwind CSS with React components.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with tailwind react"

## When to Use

Use this skill when:
- Building React components with Tailwind
- Creating reusable styled components
- Managing component variants
- Using utility libraries like clsx/cva

---

## Critical Patterns

### Class Merging (REQUIRED)

```typescript
import { clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

// ✅ ALWAYS: Use cn() utility for class merging
function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

// Usage
<div className={cn(
  "base-classes",
  condition && "conditional-classes",
  className
)} />
```

### Component Variants (REQUIRED)

```typescript
import { cva, type VariantProps } from 'class-variance-authority';

// ✅ Use CVA for variant management
const buttonVariants = cva(
  "inline-flex items-center rounded-md font-medium transition-colors",
  {
    variants: {
      variant: {
        primary: "bg-blue-600 text-white hover:bg-blue-700",
        secondary: "bg-gray-100 text-gray-900 hover:bg-gray-200",
        ghost: "hover:bg-gray-100",
      },
      size: {
        sm: "h-8 px-3 text-sm",
        md: "h-10 px-4 text-base",
        lg: "h-12 px-6 text-lg",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

interface ButtonProps extends VariantProps<typeof buttonVariants> {
  children: React.ReactNode;
}

function Button({ variant, size, children }: ButtonProps) {
  return (
    <button className={buttonVariants({ variant, size })}>
      {children}
    </button>
  );
}
```

---

## Decision Tree

```
Need dynamic classes?      → Use clsx/cn utility
Need variants?             → Use CVA
Need conditional?          → Use clsx with conditions
Need to override?          → Use tailwind-merge
```

---

## Code Examples

### Conditional Classes

```tsx
<button
  className={cn(
    "px-4 py-2 rounded",
    isActive ? "bg-blue-600 text-white" : "bg-gray-200",
    disabled && "opacity-50 cursor-not-allowed"
  )}
>
  Click me
</button>
```
