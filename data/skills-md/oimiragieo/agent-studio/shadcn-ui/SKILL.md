---
name: shadcn-ui
description: Deep expertise on shadcn/ui component library including installation, customization, theming, and accessibility patterns. Use when building UI with shadcn/ui components, integrating Radix UI primitives, configuring Tailwind CSS v4 themes, or implementing dark mode. Covers Next.js App Router, Pages Router, and Vite setups.
license: MIT
metadata:
  author: google-labs-code
  version: '1.0.0'
  source: google-labs-code/stitch-skills
verified: true
lastVerifiedAt: 2026-02-22T00:00:00.000Z
version: 1.0.0
tools: []
---

# shadcn/ui Expert

Comprehensive guide to building UIs with shadcn/ui -- the copy-paste component library built on Radix UI primitives and Tailwind CSS. Components are not installed as a dependency; they are copied into your project for full ownership and customization.

## When to Apply

Use this skill when:

- Adding shadcn/ui components to a React or Next.js project
- Customizing component styles, variants, or behavior
- Setting up Tailwind CSS v4 theming with CSS variables
- Implementing dark mode with shadcn/ui
- Building accessible forms, dialogs, or data tables
- Choosing between shadcn/ui components and custom implementations

## Core Concepts

### shadcn/ui is NOT a Component Library

shadcn/ui is a collection of reusable components that you copy into your project. Key differences from traditional libraries:

- **No npm package dependency** -- components live in your codebase
- **Full ownership** -- modify any component freely
- **Radix UI primitives** -- accessible, unstyled headless components under the hood
- **Tailwind CSS** -- all styling via utility classes and CSS variables
- **CLI-driven** -- `npx shadcn@latest add button` copies component code

### Architecture

```
Your Project
  components/
    ui/              <- shadcn/ui components live here
      button.tsx
      dialog.tsx
      input.tsx
      ...
  lib/
    utils.ts         <- cn() utility (clsx + tailwind-merge)
```

## Setup

### Next.js App Router (Recommended)

```bash
# Initialize shadcn/ui in existing Next.js project
npx shadcn@latest init

# This creates:
# - components.json (configuration)
# - lib/utils.ts (cn utility)
# - Tailwind CSS variable theme in globals.css
```

**components.json Configuration:**

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "zinc",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  }
}
```

### Vite + React

```bash
# Initialize
npx shadcn@latest init

# Vite requires path aliases in vite.config.ts:
import path from 'path';

export default defineConfig({
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
```

### Next.js Pages Router

Same as App Router but set `rsc: false` in components.json since Pages Router does not support React Server Components.

## Adding Components

```bash
# Add a single component
npx shadcn@latest add button

# Add multiple components
npx shadcn@latest add button card input label

# Add all components
npx shadcn@latest add --all

# View available components
npx shadcn@latest add --list
```

### The cn() Utility

Every shadcn/ui component uses `cn()` for conditional class merging:

```typescript
// lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

`cn()` combines `clsx` (conditional classes) with `tailwind-merge` (resolves Tailwind conflicts):

```tsx
<Button
  className={cn(
    'bg-primary text-white',
    isDisabled && 'opacity-50 cursor-not-allowed',
    size === 'lg' && 'px-8 py-4 text-lg'
  )}
>
  Submit
</Button>
```

## Theming with CSS Variables

### Tailwind CSS v4 Theme Setup

shadcn/ui uses CSS custom properties for theming, enabling runtime theme switching:

```css
/* globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 240 10% 3.9%;
    --card: 0 0% 100%;
    --card-foreground: 240 10% 3.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 240 10% 3.9%;
    --primary: 240 5.9% 10%;
    --primary-foreground: 0 0% 98%;
    --secondary: 240 4.8% 95.9%;
    --secondary-foreground: 240 5.9% 10%;
    --muted: 240 4.8% 95.9%;
    --muted-foreground: 240 3.8% 46.1%;
    --accent: 240 4.8% 95.9%;
    --accent-foreground: 240 5.9% 10%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 5.9% 90%;
    --input: 240 5.9% 90%;
    --ring: 240 5.9% 10%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 240 10% 3.9%;
    --foreground: 0 0% 98%;
    --card: 240 10% 3.9%;
    --card-foreground: 0 0% 98%;
    --popover: 240 10% 3.9%;
    --popover-foreground: 0 0% 98%;
    --primary: 0 0% 98%;
    --primary-foreground: 240 5.9% 10%;
    --secondary: 240 3.7% 15.9%;
    --secondary-foreground: 0 0% 98%;
    --muted: 240 3.7% 15.9%;
    --muted-foreground: 240 5% 64.9%;
    --accent: 240 3.7% 15.9%;
    --accent-foreground: 0 0% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 0 0% 98%;
    --border: 240 3.7% 15.9%;
    --input: 240 3.7% 15.9%;
    --ring: 240 4.9% 83.9%;
  }
}
```

### Dark Mode Implementation

Use `next-themes` for Next.js dark mode:

```tsx
// app/providers.tsx
'use client';

import { ThemeProvider } from 'next-themes';

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  );
}

// app/layout.tsx
import { Providers } from './providers';

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
```

Toggle component:

```tsx
'use client';

import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/button';
import { Moon, Sun } from 'lucide-react';

export function ThemeToggle() {
  const { setTheme, theme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
```

## Common Component Patterns

### Forms with React Hook Form + Zod

```tsx
'use client';

import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';

const formSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

export function LoginForm() {
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: { email: '', password: '' },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values);
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input placeholder="name@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          control={form.control}
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Password</FormLabel>
              <FormControl>
                <Input type="password" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit">Sign In</Button>
      </form>
    </Form>
  );
}
```

### Data Tables with TanStack Table

```tsx
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { ColumnDef, flexRender, getCoreRowModel, useReactTable } from '@tanstack/react-table';

interface DataTableProps<TData, TValue> {
  columns: ColumnDef<TData, TValue>[];
  data: TData[];
}

export function DataTable<TData, TValue>({ columns, data }: DataTableProps<TData, TValue>) {
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          {table.getHeaderGroups().map(headerGroup => (
            <TableRow key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                <TableHead key={header.id}>
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </TableHead>
              ))}
            </TableRow>
          ))}
        </TableHeader>
        <TableBody>
          {table.getRowModel().rows.map(row => (
            <TableRow key={row.id}>
              {row.getVisibleCells().map(cell => (
                <TableCell key={cell.id}>
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
```

### Responsive Dialog / Drawer Pattern

Use Dialog on desktop and Drawer on mobile:

```tsx
'use client';

import { useMediaQuery } from '@/hooks/use-media-query';
import { Dialog, DialogContent, DialogTrigger } from '@/components/ui/dialog';
import { Drawer, DrawerContent, DrawerTrigger } from '@/components/ui/drawer';
import { Button } from '@/components/ui/button';

export function ResponsiveModal({ children }: { children: React.ReactNode }) {
  const isDesktop = useMediaQuery('(min-width: 768px)');

  if (isDesktop) {
    return (
      <Dialog>
        <DialogTrigger asChild>
          <Button>Open</Button>
        </DialogTrigger>
        <DialogContent>{children}</DialogContent>
      </Dialog>
    );
  }

  return (
    <Drawer>
      <DrawerTrigger asChild>
        <Button>Open</Button>
      </DrawerTrigger>
      <DrawerContent>{children}</DrawerContent>
    </Drawer>
  );
}
```

## Accessibility Patterns

shadcn/ui components are built on Radix UI, which provides:

- Full keyboard navigation (Tab, Arrow keys, Enter, Escape)
- ARIA attributes (roles, states, properties)
- Focus management (trapping, restoration)
- Screen reader announcements

### Key Accessibility Features by Component

| Component     | Keyboard                | ARIA                          | Focus Trap |
| ------------- | ----------------------- | ----------------------------- | ---------- |
| Button        | Enter/Space to activate | role="button"                 | No         |
| Dialog        | Escape to close         | role="dialog", aria-modal     | Yes        |
| Dropdown Menu | Arrow keys to navigate  | role="menu", role="menuitem"  | Yes        |
| Select        | Arrow keys, type-ahead  | role="listbox", role="option" | Yes        |
| Tabs          | Arrow keys between tabs | role="tablist", role="tab"    | No         |
| Toast         | Auto-announce           | role="status", aria-live      | No         |
| Tooltip       | Focus/hover to show     | role="tooltip"                | No         |

### Custom Accessibility Enhancements

```tsx
// Always provide labels for interactive elements
<Button aria-label="Close dialog">
  <X className="h-4 w-4" />
</Button>

// Use sr-only for visual-only content
<span className="sr-only">Loading...</span>

// Announce dynamic content
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>
```

## Anti-Patterns

- Do NOT install shadcn/ui as an npm package -- use the CLI to copy components
- Do NOT modify Radix primitives directly -- extend via the shadcn wrapper component
- Do NOT use hardcoded colors -- always use CSS variable theme tokens
- Do NOT skip the `cn()` utility -- it prevents Tailwind class conflicts
- Do NOT forget `suppressHydrationWarning` on `<html>` when using next-themes
- Do NOT nest interactive elements (button inside button, link inside button)

## Iron Laws

1. **NEVER** install shadcn/ui as a package dependency — components must be copied into the project for full ownership
2. **ALWAYS** use the `cn()` utility for conditional class names to prevent Tailwind class conflicts
3. **NEVER** hardcode colors — always use CSS variable theme tokens for theming consistency
4. **ALWAYS** use Radix UI primitives through the shadcn/ui abstraction, not directly
5. **NEVER** nest interactive elements (button inside button, link inside button) — violates accessibility standards

## Anti-Patterns

| Anti-Pattern                       | Why It Fails                                          | Correct Approach                                                      |
| ---------------------------------- | ----------------------------------------------------- | --------------------------------------------------------------------- |
| Installing as a package            | Component source is locked; no customization possible | Use `npx shadcn@latest add` to copy components into your project      |
| Hardcoding color values            | Theme switching breaks; dark mode fails               | Use CSS variable tokens (`bg-background`, `text-foreground`, etc.)    |
| Skipping `cn()` utility            | Tailwind class conflicts produce unpredictable styles | Always merge classes with `cn()` from `@/lib/utils`                   |
| Direct Radix UI primitive use      | Missing shadcn styling and accessibility wiring       | Use shadcn components that wrap Radix primitives with correct classes |
| Missing `suppressHydrationWarning` | Hydration mismatch errors with next-themes dark mode  | Add `suppressHydrationWarning` to `<html>` when using next-themes     |

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.

## References

- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Radix UI Primitives](https://www.radix-ui.com/primitives)
- [Tailwind CSS v4](https://tailwindcss.com/docs)
- [next-themes](https://github.com/pacocoursey/next-themes)
