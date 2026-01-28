---
name: design-system-manager
description: Create and manage design systems with Tailwind CSS 4, design tokens, theming, and component documentation
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
---

# Design System Manager

Expert skill for creating and maintaining scalable design systems. Specializes in Tailwind CSS 4, design tokens, theming systems, color palettes, and typography scales.

## Technology Stack (2025)

### Styling
- **Tailwind CSS 4.0** - CSS-first config, cascade layers, @theme
- **CSS Variables** - Runtime theming
- **oklch()** - Perceptually uniform colors
- **@property** - Registered custom properties

### Tools
- **Style Dictionary 4** - Token transformation
- **Radix Colors** - Accessible color system
- **colord** - Color manipulation
- **Figma Tokens** - Design-to-code sync

## Tailwind CSS 4.0 Configuration

### CSS-First Configuration
```css
/* app.css */
@import "tailwindcss";

@theme {
  /* Colors using oklch for better interpolation */
  --color-primary: oklch(0.7 0.15 250);
  --color-primary-hover: oklch(0.6 0.15 250);
  --color-secondary: oklch(0.65 0.12 280);

  --color-background: oklch(0.99 0.005 250);
  --color-foreground: oklch(0.15 0.01 250);

  --color-muted: oklch(0.95 0.01 250);
  --color-muted-foreground: oklch(0.45 0.02 250);

  --color-accent: oklch(0.92 0.02 250);
  --color-accent-foreground: oklch(0.15 0.01 250);

  --color-destructive: oklch(0.55 0.2 25);
  --color-destructive-foreground: oklch(0.98 0.01 250);

  --color-success: oklch(0.6 0.18 145);
  --color-warning: oklch(0.75 0.18 85);

  /* Typography */
  --font-sans: "Inter Variable", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 1.875rem;
  --text-4xl: 2.25rem;

  /* Spacing (4px grid) */
  --spacing-0: 0;
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-3: 0.75rem;
  --spacing-4: 1rem;
  --spacing-5: 1.25rem;
  --spacing-6: 1.5rem;
  --spacing-8: 2rem;
  --spacing-10: 2.5rem;
  --spacing-12: 3rem;
  --spacing-16: 4rem;

  /* Border Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;
  --radius-2xl: 1rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px 0 oklch(0 0 0 / 0.05);
  --shadow-md: 0 4px 6px -1px oklch(0 0 0 / 0.1), 0 2px 4px -2px oklch(0 0 0 / 0.1);
  --shadow-lg: 0 10px 15px -3px oklch(0 0 0 / 0.1), 0 4px 6px -4px oklch(0 0 0 / 0.1);

  /* Transitions */
  --duration-fast: 150ms;
  --duration-normal: 200ms;
  --duration-slow: 300ms;
  --easing-default: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Dark Mode */
@media (prefers-color-scheme: dark) {
  @theme {
    --color-background: oklch(0.15 0.01 250);
    --color-foreground: oklch(0.95 0.01 250);
    --color-muted: oklch(0.25 0.01 250);
    --color-muted-foreground: oklch(0.65 0.02 250);
    --color-accent: oklch(0.25 0.02 250);
    --color-accent-foreground: oklch(0.95 0.01 250);
  }
}

/* Class-based dark mode */
.dark {
  @theme {
    --color-background: oklch(0.15 0.01 250);
    --color-foreground: oklch(0.95 0.01 250);
  }
}
```

## Theme Provider (React 19)

```typescript
// theme-provider.tsx
'use client'

import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'

type Theme = 'light' | 'dark' | 'system'

interface ThemeContextValue {
  theme: Theme
  setTheme: (theme: Theme) => void
  resolvedTheme: 'light' | 'dark'
}

const ThemeContext = createContext<ThemeContextValue | null>(null)

export function useTheme() {
  const context = useContext(ThemeContext)
  if (!context) throw new Error('useTheme must be used within ThemeProvider')
  return context
}

interface ThemeProviderProps {
  children: ReactNode
  defaultTheme?: Theme
  storageKey?: string
}

export function ThemeProvider({
  children,
  defaultTheme = 'system',
  storageKey = 'ui-theme',
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(defaultTheme)
  const [resolvedTheme, setResolvedTheme] = useState<'light' | 'dark'>('light')

  useEffect(() => {
    const stored = localStorage.getItem(storageKey) as Theme | null
    if (stored) setTheme(stored)
  }, [storageKey])

  useEffect(() => {
    const root = document.documentElement

    const applyTheme = (t: 'light' | 'dark') => {
      root.classList.remove('light', 'dark')
      root.classList.add(t)
      setResolvedTheme(t)
    }

    if (theme === 'system') {
      const media = window.matchMedia('(prefers-color-scheme: dark)')
      applyTheme(media.matches ? 'dark' : 'light')

      const handler = (e: MediaQueryListEvent) => applyTheme(e.matches ? 'dark' : 'light')
      media.addEventListener('change', handler)
      return () => media.removeEventListener('change', handler)
    } else {
      applyTheme(theme)
    }
  }, [theme])

  const handleSetTheme = (newTheme: Theme) => {
    setTheme(newTheme)
    localStorage.setItem(storageKey, newTheme)
  }

  return (
    <ThemeContext value={{ theme, setTheme: handleSetTheme, resolvedTheme }}>
      {children}
    </ThemeContext>
  )
}
```

## Color System

### Color Palette Generator
```typescript
// color-utils.ts
import { colord, extend } from 'colord'
import a11yPlugin from 'colord/plugins/a11y'

extend([a11yPlugin])

export function generateColorScale(baseColor: string) {
  const base = colord(baseColor)

  return {
    50: base.lighten(0.45).toHex(),
    100: base.lighten(0.4).toHex(),
    200: base.lighten(0.3).toHex(),
    300: base.lighten(0.2).toHex(),
    400: base.lighten(0.1).toHex(),
    500: baseColor,
    600: base.darken(0.1).toHex(),
    700: base.darken(0.2).toHex(),
    800: base.darken(0.3).toHex(),
    900: base.darken(0.4).toHex(),
    950: base.darken(0.45).toHex(),
  }
}

export function checkContrast(foreground: string, background: string) {
  const contrast = colord(foreground).contrast(background)

  return {
    ratio: contrast.toFixed(2),
    passesAA: contrast >= 4.5,
    passesAAA: contrast >= 7,
    passesAALarge: contrast >= 3,
  }
}
```

### OKLCH Color Utilities
```typescript
// oklch-utils.ts
export function oklch(l: number, c: number, h: number, a = 1) {
  return `oklch(${l} ${c} ${h}${a < 1 ? ` / ${a}` : ''})`
}

export const colors = {
  primary: {
    DEFAULT: 'var(--color-primary)',
    hover: 'var(--color-primary-hover)',
  },
  background: 'var(--color-background)',
  foreground: 'var(--color-foreground)',
  muted: {
    DEFAULT: 'var(--color-muted)',
    foreground: 'var(--color-muted-foreground)',
  },
}
```

## Typography System

### Fluid Typography with clamp()
```css
@theme {
  /* Fluid type scale */
  --text-fluid-xs: clamp(0.69rem, 0.66rem + 0.16vw, 0.75rem);
  --text-fluid-sm: clamp(0.83rem, 0.78rem + 0.24vw, 0.94rem);
  --text-fluid-base: clamp(1rem, 0.93rem + 0.36vw, 1.19rem);
  --text-fluid-lg: clamp(1.2rem, 1.09rem + 0.53vw, 1.48rem);
  --text-fluid-xl: clamp(1.44rem, 1.29rem + 0.75vw, 1.86rem);
  --text-fluid-2xl: clamp(1.73rem, 1.52rem + 1.05vw, 2.33rem);
  --text-fluid-3xl: clamp(2.07rem, 1.78rem + 1.47vw, 2.91rem);
}
```

### Text Styles
```typescript
// text-styles.ts
export const textStyles = {
  h1: 'text-4xl font-bold tracking-tight',
  h2: 'text-3xl font-semibold tracking-tight',
  h3: 'text-2xl font-semibold',
  h4: 'text-xl font-semibold',
  body: 'text-base',
  small: 'text-sm text-muted-foreground',
  code: 'font-mono text-sm',
}
```

## Spacing System

### 4px Grid System
```css
@theme {
  --spacing-px: 1px;
  --spacing-0: 0;
  --spacing-0.5: 0.125rem;  /* 2px */
  --spacing-1: 0.25rem;     /* 4px */
  --spacing-1.5: 0.375rem;  /* 6px */
  --spacing-2: 0.5rem;      /* 8px */
  --spacing-2.5: 0.625rem;  /* 10px */
  --spacing-3: 0.75rem;     /* 12px */
  --spacing-3.5: 0.875rem;  /* 14px */
  --spacing-4: 1rem;        /* 16px */
  --spacing-5: 1.25rem;     /* 20px */
  --spacing-6: 1.5rem;      /* 24px */
  --spacing-7: 1.75rem;     /* 28px */
  --spacing-8: 2rem;        /* 32px */
  --spacing-9: 2.25rem;     /* 36px */
  --spacing-10: 2.5rem;     /* 40px */
  --spacing-12: 3rem;       /* 48px */
  --spacing-14: 3.5rem;     /* 56px */
  --spacing-16: 4rem;       /* 64px */
  --spacing-20: 5rem;       /* 80px */
  --spacing-24: 6rem;       /* 96px */
}
```

## Component Tokens

```typescript
// component-tokens.ts
export const componentTokens = {
  button: {
    sm: 'h-9 px-3 text-sm',
    md: 'h-10 px-4',
    lg: 'h-11 px-8',
    icon: 'h-10 w-10',
  },
  input: {
    height: 'h-10',
    padding: 'px-3 py-2',
    border: 'border border-input',
    focus: 'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring',
  },
  card: {
    padding: 'p-6',
    border: 'border rounded-lg',
    shadow: 'shadow-sm',
  },
}
```

## Best Practices

### Design Tokens
1. **Three-Tier System**: Primitive → Semantic → Component
2. **Meaningful Names**: `color-primary` not `color-blue`
3. **Single Source of Truth**: Define once, use everywhere
4. **CSS Variables**: For runtime theming

### Tailwind CSS 4
1. **CSS-First Config**: Use @theme directive
2. **OKLCH Colors**: Better color interpolation
3. **Cascade Layers**: Proper specificity control
4. **Container Queries**: Component-level responsive

### Accessibility
1. **Color Contrast**: WCAG AA minimum (4.5:1)
2. **Focus States**: Visible focus indicators
3. **Motion**: Respect prefers-reduced-motion
4. **Font Size**: Minimum 16px for body

## When to Use This Skill

Activate when you need to:
- Set up design system
- Create design tokens
- Implement theming
- Define color palettes
- Create typography system
- Set up spacing system
- Ensure design consistency
- Improve accessibility

## Output Format

Provide:
1. **Token Files**: Complete token definitions
2. **Theme Configuration**: CSS variables and theme provider
3. **Usage Examples**: How to use tokens
4. **Accessibility Report**: WCAG compliance
5. **Documentation**: Usage guidelines
