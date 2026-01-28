---
name: tailwind-best-practices
description: Tailwind CSS patterns and conventions. Use when writing responsive designs, implementing dark mode, creating reusable component styles, or configuring Tailwind. Triggers on tasks involving Tailwind classes, responsive design, dark mode, or CSS styling.
version: 4.0.0
framework: Tailwind CSS
minimumVersion: 3.4.0
license: MIT
---

# Tailwind CSS Best Practices

Comprehensive patterns for building consistent, maintainable interfaces with Tailwind CSS v4. Contains 26+ rules covering responsive design, dark mode, component patterns, and configuration best practices.

## Metadata

- **Version:** 4.0.0
- **Framework:** Tailwind CSS v3.4+ / v4.0+
- **Rule Count:** 26 rules across 7 categories
- **License:** MIT
- **Documentation:** [tailwindcss.com/docs](https://tailwindcss.com/docs)

## When to Apply

Reference these guidelines when:
- Writing responsive layouts
- Implementing dark mode
- Creating reusable component styles
- Configuring Tailwind
- Optimizing CSS output

## Rule Categories by Priority

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | Responsive Design | CRITICAL | `resp-` |
| 2 | Dark Mode | CRITICAL | `dark-` |
| 3 | Component Patterns | HIGH | `comp-` |
| 4 | Custom Configuration | HIGH | `config-` |
| 5 | Spacing & Typography | MEDIUM | `space-` |
| 6 | Animation | MEDIUM | `anim-` |
| 7 | Performance | LOW | `perf-` |

## Quick Reference

### 1. Responsive Design (CRITICAL)

- `resp-mobile-first` - Mobile-first approach
- `resp-breakpoints` - Use breakpoints correctly
- `resp-container` - Container patterns
- `resp-grid-flex` - Grid vs Flexbox decisions
- `resp-hidden-shown` - Conditional display

### 2. Dark Mode (CRITICAL)

- `dark-setup` - Configure dark mode
- `dark-classes` - Apply dark mode classes
- `dark-toggle` - Implement dark mode toggle
- `dark-system-preference` - Respect system preference
- `dark-colors` - Design for both modes

### 3. Component Patterns (HIGH)

- `comp-clsx-cn` - Conditional classes utility
- `comp-variants` - Component variants pattern
- `comp-slots` - Slot-based components
- `comp-composition` - Composing utilities

### 4. Custom Configuration (HIGH)

- `config-extend` - Extend vs override theme
- `config-colors` - Custom color palette
- `config-fonts` - Custom fonts
- `config-screens` - Custom breakpoints
- `config-plugins` - Using plugins

### 5. Spacing & Typography (MEDIUM)

- `space-consistent` - Consistent spacing scale
- `space-margins` - Margin patterns
- `space-padding` - Padding patterns
- `typo-scale` - Typography scale
- `typo-line-height` - Line height

### 6. Animation (MEDIUM)

- `anim-transitions` - Transition utilities
- `anim-keyframes` - Custom keyframes
- `anim-reduced-motion` - Respect motion preferences

### 7. Performance (LOW)

- `perf-purge` - Content configuration
- `perf-jit` - JIT mode benefits
- `perf-arbitrary` - Arbitrary values usage

## Essential Patterns

### Mobile-First Responsive Design

```tsx
// ✅ Mobile-first: start with mobile, add larger breakpoints
<div className="
  w-full           // Mobile: full width
  md:w-1/2         // Tablet: half width
  lg:w-1/3         // Desktop: third width
">
  <p className="
    text-sm          // Mobile: small text
    md:text-base     // Tablet: base text
    lg:text-lg       // Desktop: large text
  ">
    Content
  </p>
</div>

// ❌ Don't think desktop-first
<div className="w-1/3 md:w-1/2 sm:w-full">  // Confusing
```

### Dark Mode Implementation

```tsx
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media' for system preference
  // ...
}

// Component
<div className="
  bg-white dark:bg-gray-900
  text-gray-900 dark:text-white
  border border-gray-200 dark:border-gray-700
">
  <h2 className="text-gray-900 dark:text-white">Title</h2>
  <p className="text-gray-600 dark:text-gray-400">Description</p>
</div>

// Toggle with JavaScript
function toggleDarkMode() {
  document.documentElement.classList.toggle('dark')
}
```

### Conditional Classes with clsx/cn

```tsx
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

// cn utility - merges Tailwind classes intelligently
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Usage
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger'
  size?: 'sm' | 'md' | 'lg'
  className?: string
  children: React.ReactNode
}

function Button({ variant = 'primary', size = 'md', className, children }: ButtonProps) {
  return (
    <button
      className={cn(
        // Base styles
        'inline-flex items-center justify-center rounded-md font-medium transition-colors',
        'focus:outline-none focus:ring-2 focus:ring-offset-2',

        // Variants
        {
          'bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500':
            variant === 'primary',
          'bg-gray-100 text-gray-900 hover:bg-gray-200 focus:ring-gray-500':
            variant === 'secondary',
          'bg-red-600 text-white hover:bg-red-700 focus:ring-red-500':
            variant === 'danger',
        },

        // Sizes
        {
          'px-3 py-1.5 text-sm': size === 'sm',
          'px-4 py-2 text-base': size === 'md',
          'px-6 py-3 text-lg': size === 'lg',
        },

        // Allow override
        className
      )}
    >
      {children}
    </button>
  )
}
```

### Tailwind Configuration

```js
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './resources/**/*.blade.php',
    './resources/**/*.{js,ts,jsx,tsx}',
  ],
  darkMode: 'class',
  theme: {
    // Override defaults
    screens: {
      sm: '640px',
      md: '768px',
      lg: '1024px',
      xl: '1280px',
      '2xl': '1536px',
    },

    // Extend (recommended - keeps defaults)
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
        secondary: {
          // ...
        },
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
      },
      borderRadius: {
        '4xl': '2rem',
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

### Responsive Grid Layout

```tsx
// Product grid - responsive columns
<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
  {products.map(product => (
    <ProductCard key={product.id} product={product} />
  ))}
</div>

// Dashboard layout - sidebar + main
<div className="flex flex-col lg:flex-row min-h-screen">
  <aside className="
    w-full lg:w-64
    bg-gray-900
    lg:min-h-screen
  ">
    <nav>...</nav>
  </aside>
  <main className="flex-1 p-4 lg:p-8">
    <div className="max-w-7xl mx-auto">
      {children}
    </div>
  </main>
</div>
```

### Form Styling

```tsx
<form className="space-y-6">
  <div>
    <label htmlFor="email" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
      Email
    </label>
    <input
      type="email"
      id="email"
      className="
        mt-1 block w-full rounded-md
        border-gray-300 dark:border-gray-600
        bg-white dark:bg-gray-800
        text-gray-900 dark:text-white
        shadow-sm
        focus:border-blue-500 focus:ring-blue-500
        disabled:bg-gray-100 disabled:cursor-not-allowed
      "
    />
  </div>

  <button
    type="submit"
    className="
      w-full flex justify-center
      py-2 px-4
      border border-transparent rounded-md
      shadow-sm text-sm font-medium
      text-white bg-blue-600
      hover:bg-blue-700
      focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500
      disabled:opacity-50 disabled:cursor-not-allowed
    "
  >
    Submit
  </button>
</form>
```

### Animations with Reduced Motion

```tsx
// Respect user's motion preferences
<div className="
  transition-transform duration-300
  hover:scale-105
  motion-reduce:transition-none
  motion-reduce:hover:transform-none
">
  Card content
</div>

// Custom animation
<div className="animate-fade-in motion-reduce:animate-none">
  Content
</div>
```

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      keyframes: {
        'fade-in': {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
      },
      animation: {
        'fade-in': 'fade-in 0.3s ease-out',
      },
    },
  },
}
```

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/resp-mobile-first.md
rules/dark-setup.md
rules/comp-clsx-cn.md
```

## References

- [Tailwind CSS Documentation](https://tailwindcss.com/docs) - Official documentation
- [Responsive Design Guide](https://tailwindcss.com/docs/responsive-design) - Mobile-first patterns
- [Dark Mode Guide](https://tailwindcss.com/docs/dark-mode) - Theme implementation
- [Configuration Guide](https://tailwindcss.com/docs/configuration) - Customization
- [Tailwind UI](https://tailwindui.com) - Official component library
- [Headless UI](https://headlessui.com) - Accessible components
- [Heroicons](https://heroicons.com) - Icon library

## Ecosystem Tools

- **Tailwind CSS IntelliSense** - VS Code autocomplete and linting
- **Prettier Plugin** - Automatic class sorting
- **tailwind-merge** - Conflict-free class merging
- **clsx** - Conditional class utility
- **CVA** - Component variant system

## License

MIT License - See repository for full license text.

This skill is part of the Agent Skills collection, providing AI-powered development assistance with industry best practices.
