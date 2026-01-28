---
name: ui-component-builder
description: Build, convert, and optimize React/Vue/Svelte UI components with TypeScript, advanced patterns, animations, and accessibility. Updated for React 19, Next.js 16, and modern 2025 standards.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# UI Component Builder

Expert skill for building production-ready UI components for component libraries. Specializes in React 19, Vue 3.5, and Svelte 5 with TypeScript 5.9, implementing advanced patterns, animations with Motion 12, and ensuring accessibility and performance.

## Technology Stack (2025)

### Core Technologies
- **React 19.2** - Latest with React Compiler, use API, Server Components
- **Next.js 16** - Turbopack stable, Cache Components, PPR
- **TypeScript 5.9** - Latest stable with enhanced type inference
- **Tailwind CSS 4.0** - CSS-first config, cascade layers, 100x faster incremental builds
- **Motion 12** (formerly Framer Motion) - Hybrid engine, GPU-accelerated animations

### Build & Testing
- **Vitest 4.0** - Browser Mode stable, Visual Regression testing
- **Vite 6** - Lightning fast HMR
- **Storybook 9** - Component development platform

### Utilities
- **class-variance-authority (cva)** - Variant management
- **clsx/tailwind-merge** - Conditional className composition
- **Zod 4** - Runtime validation
- **React Hook Form 8** - Form state management

## Core Capabilities

### 1. Component Creation
- Create new components from scratch with TypeScript
- Implement compound components pattern
- Build components with render props
- Create custom hooks with the new `use` API (React 19)
- Support for polymorphic components (as prop pattern)
- Generic component types for maximum reusability
- Server Components support (Next.js 16)

### 2. Framework Conversion
Convert components seamlessly between frameworks:
- **React 19 → Vue 3.5**: JSX to template/composition API
- **React 19 → Svelte 5**: Hooks to runes ($state, $derived, $effect)
- **Vue 3.5 → React 19**: Template to JSX, composables to hooks
- **Svelte 5 → React 19**: Runes to useState/use

### 3. Advanced Patterns Implementation

#### Compound Components
```typescript
<Select>
  <Select.Trigger />
  <Select.Content>
    <Select.Item value="1">Option 1</Select.Item>
  </Select.Content>
</Select>
```

#### React 19 `use` API
```typescript
function Comments({ commentsPromise }: { commentsPromise: Promise<Comments[]> }) {
  const comments = use(commentsPromise)
  return comments.map(c => <Comment key={c.id} data={c} />)
}
```

#### Server Components (Next.js 16)
```typescript
// Server Component - runs on server only
async function ProductList() {
  const products = await db.products.findMany()
  return <ProductGrid products={products} />
}

// Client Component
'use client'
function AddToCart({ productId }: { productId: string }) {
  const [pending, startTransition] = useTransition()
}
```

### 4. Animation Integration (Motion 12)
```typescript
import { motion, AnimatePresence } from 'motion/react'

export function Modal({ isOpen, onClose, children }: ModalProps) {
  return (
    <AnimatePresence>
      {isOpen && (
        <>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="fixed inset-0 bg-black/50"
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: 'spring', duration: 0.3 }}
            className="fixed inset-0 flex items-center justify-center"
          >
            {children}
          </motion.div>
        </>
      )}
    </AnimatePresence>
  )
}
```

### 5. TypeScript 5.9 Excellence
- Strict type safety with proper generic constraints
- Discriminated unions for component variants
- `satisfies` operator for better inference
- `const` type parameters
- Proper typing for refs, events, and children

### 6. Accessibility (a11y) First
- Semantic HTML elements
- ARIA attributes when needed
- Keyboard navigation (Tab, Enter, Escape, Arrow keys)
- Focus management and focus trapping
- Screen reader announcements
- WCAG 2.1 AA/AAA compliance
- `prefers-reduced-motion` support

### 7. Performance Optimization
- React Compiler automatic memoization
- Server Components for zero client JS
- Virtual scrolling for large lists
- Code splitting and lazy loading
- Streaming and Suspense

## Component Patterns

### Button Component (React 19 + Tailwind 4)
```typescript
import { forwardRef, type ButtonHTMLAttributes } from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/lib/utils'

const buttonVariants = cva(
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent',
        secondary: 'bg-secondary text-secondary-foreground hover:bg-secondary/80',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
        link: 'text-primary underline-offset-4 hover:underline',
      },
      size: {
        default: 'h-10 px-4 py-2',
        sm: 'h-9 rounded-md px-3',
        lg: 'h-11 rounded-md px-8',
        icon: 'h-10 w-10',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, ...props }, ref) => {
    return (
      <button
        ref={ref}
        className={cn(buttonVariants({ variant, size, className }))}
        {...props}
      />
    )
  }
)

Button.displayName = 'Button'
export { Button, buttonVariants }
```

### Compound Component Pattern
```typescript
import { createContext, useContext, useState, type ReactNode } from 'react'

interface TabsContextValue {
  activeTab: string
  setActiveTab: (tab: string) => void
}

const TabsContext = createContext<TabsContextValue | null>(null)

function useTabs() {
  const context = useContext(TabsContext)
  if (!context) throw new Error('Tabs components must be used within Tabs')
  return context
}

export function Tabs({ defaultValue, children }: { defaultValue: string; children: ReactNode }) {
  const [activeTab, setActiveTab] = useState(defaultValue)

  return (
    <TabsContext value={{ activeTab, setActiveTab }}>
      <div className="w-full">{children}</div>
    </TabsContext>
  )
}

export function TabsTrigger({ value, children }: { value: string; children: ReactNode }) {
  const { activeTab, setActiveTab } = useTabs()
  const isActive = activeTab === value

  return (
    <button
      role="tab"
      aria-selected={isActive}
      onClick={() => setActiveTab(value)}
      className={cn(
        'px-4 py-2 font-medium transition-colors',
        isActive ? 'border-b-2 border-primary text-primary' : 'text-muted-foreground'
      )}
    >
      {children}
    </button>
  )
}

export function TabsContent({ value, children }: { value: string; children: ReactNode }) {
  const { activeTab } = useTabs()
  if (activeTab !== value) return null
  return <div role="tabpanel" className="py-4">{children}</div>
}
```

## Framework Conversion

### React 19 to Svelte 5
```typescript
// REACT 19
function Counter() {
  const [count, setCount] = useState(0)
  const doubled = useMemo(() => count * 2, [count])
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

// SVELTE 5 (Runes)
<script lang="ts">
  let count = $state(0)
  let doubled = $derived(count * 2)
</script>

<button onclick={() => count++}>{count} ({doubled})</button>
```

### React 19 to Vue 3.5
```typescript
// REACT 19
function Counter() {
  const [count, setCount] = useState(0)
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>
}

// VUE 3.5
<script setup lang="ts">
import { ref } from 'vue'
const count = ref(0)
</script>

<template>
  <button @click="count++">{{ count }}</button>
</template>
```

## Tailwind CSS 4.0 Configuration

```css
@import "tailwindcss";

@theme {
  --color-primary: oklch(0.7 0.15 250);
  --color-secondary: oklch(0.6 0.12 280);
  --font-sans: "Inter", system-ui, sans-serif;
  --radius-md: 0.5rem;
}

@media (prefers-color-scheme: dark) {
  @theme {
    --color-background: oklch(0.15 0.01 250);
    --color-foreground: oklch(0.95 0.01 250);
  }
}
```

## Best Practices (2025)

### Component Structure
```
components/
  Button/
    Button.tsx           # Main component
    Button.types.ts      # Type definitions
    Button.test.tsx      # Vitest 4 tests
    Button.stories.tsx   # Storybook 9 stories
    index.ts             # Public exports
```

### React 19 Best Practices
- Use React Compiler - no manual memoization needed
- Prefer Server Components when possible
- Use `use` API for data fetching in render
- Leverage Suspense for loading states
- Use `useOptimistic` for optimistic updates
- Use `useFormStatus` for form states

### Performance Checklist
- [ ] Server Components for static content
- [ ] React Compiler enabled (auto-memoization)
- [ ] Lazy loading for heavy components
- [ ] Virtual scrolling for large lists

### Accessibility Checklist
- [ ] Semantic HTML elements
- [ ] Keyboard navigation works
- [ ] ARIA attributes where needed
- [ ] WCAG AA color contrast (4.5:1)
- [ ] prefers-reduced-motion support

## When to Use This Skill

Activate when you need to:
- Create new UI components
- Convert components between React/Vue/Svelte
- Implement advanced component patterns
- Add animations with Motion 12
- Optimize component performance
- Improve accessibility
- Build Server Components (Next.js 16)

## Output Format

Provide:
1. **Complete Component Code**: Fully typed and production-ready
2. **Usage Example**: How to use the component
3. **Props Documentation**: All props with types
4. **Accessibility Notes**: Keyboard shortcuts and ARIA
5. **Performance Tips**: React Compiler, Server Components

Always follow React 19, Next.js 16, and TypeScript 5.9 conventions.
