---
name: shadcn-setup
description: Set up shadcn/ui component library with Tailwind CSS v4 configuration. Handles installation, initialization, theme configuration, and common component setup. Use when starting a new Next.js/React project that needs a component library.
version: 1.0.0
tags:
  - shadcn
  - ui
  - components
  - tailwind
  - react
  - nextjs
---

# shadcn/ui Setup

Sets up shadcn/ui with proper Tailwind CSS v4 configuration. This skill ensures you get the modern CSS-first setup, not the deprecated v3 approach.

## Purpose

**IMPORTANT**: shadcn/ui CLI and AI assistants often generate Tailwind v3 configs by default. This skill ensures:

- Tailwind v4 CSS-first configuration
- Proper `@theme` block with shadcn color tokens
- No deprecated `tailwind.config.js` files
- Correct dependency versions

## When to Use

- Setting up a new Next.js project with shadcn/ui
- Adding shadcn/ui to an existing project
- Migrating from shadcn + Tailwind v3 to v4
- Resetting a broken shadcn configuration

## Quick Start

```bash
# Full setup (recommended)
python3 ~/.claude/skills/shadcn-setup/scripts/setup.py --root .

# With specific theme
python3 ~/.claude/skills/shadcn-setup/scripts/setup.py --root . --theme zinc

# Install specific components
python3 ~/.claude/skills/shadcn-setup/scripts/setup.py --root . --components button,card,input,dialog

# Next.js App Router (default)
python3 ~/.claude/skills/shadcn-setup/scripts/setup.py --root . --app-router

# Next.js Pages Router
python3 ~/.claude/skills/shadcn-setup/scripts/setup.py --root . --pages-router
```

## What Gets Installed

### Dependencies

```json
{
  "dependencies": {
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "lucide-react": "^0.400.0"
  },
  "devDependencies": {
    "tailwindcss": "^4.0.0",
    "@tailwindcss/postcss": "^4.0.0"
  }
}
```

### File Structure

```
project/
├── src/
│   ├── app/
│   │   └── globals.css           # Tailwind v4 + shadcn theme
│   ├── components/
│   │   └── ui/                   # shadcn components
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       └── ...
│   └── lib/
│       └── utils.ts              # cn() utility
├── components.json               # shadcn config
└── postcss.config.mjs            # PostCSS with @tailwindcss/postcss
```

## Tailwind v4 + shadcn CSS Configuration

The skill generates a CSS-first configuration:

```css
/* src/app/globals.css */
@import "tailwindcss";

@theme {
  /* Base colors */
  --color-background: hsl(0 0% 100%);
  --color-foreground: hsl(222.2 84% 4.9%);

  /* Card */
  --color-card: hsl(0 0% 100%);
  --color-card-foreground: hsl(222.2 84% 4.9%);

  /* Popover */
  --color-popover: hsl(0 0% 100%);
  --color-popover-foreground: hsl(222.2 84% 4.9%);

  /* Primary */
  --color-primary: hsl(222.2 47.4% 11.2%);
  --color-primary-foreground: hsl(210 40% 98%);

  /* Secondary */
  --color-secondary: hsl(210 40% 96.1%);
  --color-secondary-foreground: hsl(222.2 47.4% 11.2%);

  /* Muted */
  --color-muted: hsl(210 40% 96.1%);
  --color-muted-foreground: hsl(215.4 16.3% 46.9%);

  /* Accent */
  --color-accent: hsl(210 40% 96.1%);
  --color-accent-foreground: hsl(222.2 47.4% 11.2%);

  /* Destructive */
  --color-destructive: hsl(0 84.2% 60.2%);
  --color-destructive-foreground: hsl(210 40% 98%);

  /* Border & Input */
  --color-border: hsl(214.3 31.8% 91.4%);
  --color-input: hsl(214.3 31.8% 91.4%);
  --color-ring: hsl(222.2 84% 4.9%);

  /* Chart colors */
  --color-chart-1: hsl(12 76% 61%);
  --color-chart-2: hsl(173 58% 39%);
  --color-chart-3: hsl(197 37% 24%);
  --color-chart-4: hsl(43 74% 66%);
  --color-chart-5: hsl(27 87% 67%);

  /* Border radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-full: 9999px;

  /* Sidebar (if using sidebar component) */
  --color-sidebar: hsl(0 0% 98%);
  --color-sidebar-foreground: hsl(240 5.3% 26.1%);
  --color-sidebar-primary: hsl(240 5.9% 10%);
  --color-sidebar-primary-foreground: hsl(0 0% 98%);
  --color-sidebar-accent: hsl(240 4.8% 95.9%);
  --color-sidebar-accent-foreground: hsl(240 5.9% 10%);
  --color-sidebar-border: hsl(220 13% 91%);
  --color-sidebar-ring: hsl(217.2 91.2% 59.8%);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  @theme {
    --color-background: hsl(222.2 84% 4.9%);
    --color-foreground: hsl(210 40% 98%);
    --color-card: hsl(222.2 84% 4.9%);
    --color-card-foreground: hsl(210 40% 98%);
    --color-popover: hsl(222.2 84% 4.9%);
    --color-popover-foreground: hsl(210 40% 98%);
    --color-primary: hsl(210 40% 98%);
    --color-primary-foreground: hsl(222.2 47.4% 11.2%);
    --color-secondary: hsl(217.2 32.6% 17.5%);
    --color-secondary-foreground: hsl(210 40% 98%);
    --color-muted: hsl(217.2 32.6% 17.5%);
    --color-muted-foreground: hsl(215 20.2% 65.1%);
    --color-accent: hsl(217.2 32.6% 17.5%);
    --color-accent-foreground: hsl(210 40% 98%);
    --color-destructive: hsl(0 62.8% 30.6%);
    --color-destructive-foreground: hsl(210 40% 98%);
    --color-border: hsl(217.2 32.6% 17.5%);
    --color-input: hsl(217.2 32.6% 17.5%);
    --color-ring: hsl(212.7 26.8% 83.9%);
    --color-sidebar: hsl(240 5.9% 10%);
    --color-sidebar-foreground: hsl(240 4.8% 95.9%);
    --color-sidebar-primary: hsl(224.3 76.3% 48%);
    --color-sidebar-primary-foreground: hsl(0 0% 100%);
    --color-sidebar-accent: hsl(240 3.7% 15.9%);
    --color-sidebar-accent-foreground: hsl(240 4.8% 95.9%);
    --color-sidebar-border: hsl(240 3.7% 15.9%);
  }
}

/* Base styles */
* {
  border-color: var(--color-border);
}

body {
  background-color: var(--color-background);
  color: var(--color-foreground);
}
```

## Available Themes

| Theme | Description |
|-------|-------------|
| `default` | shadcn default (neutral grays) |
| `zinc` | Zinc-based neutral |
| `slate` | Slate-based cool neutral |
| `stone` | Stone-based warm neutral |
| `gray` | Pure gray |
| `neutral` | True neutral |
| `red` | Red primary |
| `rose` | Rose primary |
| `orange` | Orange primary |
| `green` | Green primary |
| `blue` | Blue primary |
| `yellow` | Yellow primary |
| `violet` | Violet primary |

## Common Components

Install commonly used components:

```bash
# Essential set
python3 ~/.claude/skills/shadcn-setup/scripts/setup.py --root . \
  --components button,card,input,label,dialog,dropdown-menu,toast

# Form-focused
python3 ~/.claude/skills/shadcn-setup/scripts/setup.py --root . \
  --components form,input,label,select,checkbox,radio-group,switch,textarea

# Dashboard
python3 ~/.claude/skills/shadcn-setup/scripts/setup.py --root . \
  --components card,table,tabs,badge,avatar,dropdown-menu,sheet,sidebar
```

## components.json Configuration

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "src/app/globals.css",
    "baseColor": "zinc",
    "cssVariables": true,
    "prefix": ""
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils",
    "ui": "@/components/ui",
    "lib": "@/lib",
    "hooks": "@/hooks"
  },
  "iconLibrary": "lucide"
}
```

**Note**: The `tailwind.config` is empty because we use CSS-first configuration in v4.

## Utils File

```typescript
// src/lib/utils.ts
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Usage After Setup

### Adding Components

```bash
# Using bunx (recommended with bun)
bunx shadcn@latest add button

# Multiple components
bunx shadcn@latest add card dialog dropdown-menu
```

### Using Components

```tsx
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export function MyComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Welcome</CardTitle>
      </CardHeader>
      <CardContent>
        <Button>Click me</Button>
      </CardContent>
    </Card>
  );
}
```

## Dark Mode Support

The CSS uses `prefers-color-scheme` by default. For manual toggle:

```tsx
// Add to layout.tsx or a theme provider
'use client';

import { useEffect, useState } from 'react';

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    document.documentElement.classList.toggle('dark', theme === 'dark');
  }, [theme]);

  return (
    <ThemeContext.Provider value={{ theme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
}
```

Update CSS to use class-based dark mode:

```css
/* Replace @media (prefers-color-scheme: dark) with: */
.dark {
  --color-background: hsl(222.2 84% 4.9%);
  /* ... rest of dark theme variables */
}
```

## Troubleshooting

### "tailwind.config.js created by shadcn CLI"

Delete it. The CLI sometimes generates v3 configs. Run:

```bash
rm tailwind.config.js tailwind.config.ts
```

### Components not styled correctly

1. Check that `globals.css` is imported in your layout
2. Verify `@import "tailwindcss"` is at the top
3. Ensure `@theme` block contains all required variables

### Type errors with components

Run:

```bash
bun add -D @types/react @types/react-dom
```

### cn() utility not found

Create `src/lib/utils.ts`:

```typescript
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

## Validation

After setup, run the Tailwind v4 validator:

```bash
python3 ~/.claude/skills/tailwind4-validator/scripts/validate.py --root . --verbose
```

This ensures no v3 patterns were accidentally introduced.
