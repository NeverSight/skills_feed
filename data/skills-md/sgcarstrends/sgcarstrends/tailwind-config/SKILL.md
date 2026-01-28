---
name: tailwind-config
description: Update Tailwind CSS configuration, custom themes, and design tokens across packages. Use when adding new colors, spacing scales, or customizing the design system.
allowed-tools: Read, Edit, Grep, Glob
---

# Tailwind CSS Configuration Skill

This skill helps you configure and customize Tailwind CSS across the monorepo.

## When to Use This Skill

- Adding custom colors to the design system
- Configuring typography scales
- Customizing spacing and sizing
- Setting up design tokens
- Configuring Tailwind plugins
- Debugging Tailwind configuration issues
- Creating reusable theme presets

## Tailwind Configuration Structure

```
├── packages/ui/
│   ├── tailwind.config.ts       # UI package Tailwind config
│   └── src/styles/globals.css   # Global styles and CSS variables
└── apps/web/
    ├── tailwind.config.ts       # Web app Tailwind config
    └── src/app/globals.css      # App-specific global styles
```

## Base Tailwind Configuration

### UI Package Configuration

```typescript
// packages/ui/tailwind.config.ts
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: [
    "./src/**/*.{ts,tsx}",
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      keyframes: {
        "accordion-down": {
          from: { height: "0" },
          to: { height: "var(--radix-accordion-content-height)" },
        },
        "accordion-up": {
          from: { height: "var(--radix-accordion-content-height)" },
          to: { height: "0" },
        },
      },
      animation: {
        "accordion-down": "accordion-down 0.2s ease-out",
        "accordion-up": "accordion-up 0.2s ease-out",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};

export default config;
```

### App Configuration (Extending UI)

```typescript
// apps/web/tailwind.config.ts
import type { Config } from "tailwindcss";
import baseConfig from "@sgcarstrends/ui/tailwind.config";

const config: Config = {
  ...baseConfig,
  content: [
    "./src/**/*.{ts,tsx}",
    "../../packages/ui/src/**/*.{ts,tsx}", // Include UI package components
  ],
  theme: {
    ...baseConfig.theme,
    extend: {
      ...(baseConfig.theme?.extend || {}),
      // App-specific extensions
      colors: {
        ...(baseConfig.theme?.extend?.colors || {}),
        brand: {
          50: "#f0f9ff",
          100: "#e0f2fe",
          200: "#bae6fd",
          300: "#7dd3fc",
          400: "#38bdf8",
          500: "#0ea5e9",
          600: "#0284c7",
          700: "#0369a1",
          800: "#075985",
          900: "#0c4a6e",
        },
      },
    },
  },
};

export default config;
```

## CSS Variables

### Global Styles with CSS Variables

```css
/* packages/ui/src/styles/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;

    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;

    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;

    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;

    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;

    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;

    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;

    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;

    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;

    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;

    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;

    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;

    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;

    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;

    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;

    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;

    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;

    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
```

## Common Customizations

### Adding Brand Colors

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        brand: {
          primary: "#0070F3",
          secondary: "#7928CA",
          accent: "#FF0080",
        },
        // Singapore-themed colors
        sg: {
          red: "#ED2939",
          white: "#FFFFFF",
        },
      },
    },
  },
};
```

Usage:

```tsx
<div className="bg-brand-primary text-white">
  <h1 className="text-brand-accent">SG Cars Trends</h1>
</div>
```

### Custom Typography

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["Fira Code", "monospace"],
      },
      fontSize: {
        "2xs": "0.625rem",     // 10px
        xs: "0.75rem",          // 12px
        sm: "0.875rem",         // 14px
        base: "1rem",           // 16px
        lg: "1.125rem",         // 18px
        xl: "1.25rem",          // 20px
        "2xl": "1.5rem",        // 24px
        "3xl": "1.875rem",      // 30px
        "4xl": "2.25rem",       // 36px
        "5xl": "3rem",          // 48px
      },
      lineHeight: {
        tight: "1.2",
        normal: "1.5",
        relaxed: "1.75",
      },
    },
  },
};
```

### Custom Spacing

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      spacing: {
        "4.5": "1.125rem",    // 18px
        "13": "3.25rem",      // 52px
        "15": "3.75rem",      // 60px
        "128": "32rem",       // 512px
        "144": "36rem",       // 576px
      },
    },
  },
};
```

### Custom Breakpoints

```typescript
// tailwind.config.ts
export default {
  theme: {
    screens: {
      xs: "475px",
      sm: "640px",
      md: "768px",
      lg: "1024px",
      xl: "1280px",
      "2xl": "1536px",
      "3xl": "1920px",
    },
  },
};
```

### Custom Animations

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      keyframes: {
        shimmer: {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideUp: {
          "0%": { transform: "translateY(10px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
      },
      animation: {
        shimmer: "shimmer 2s linear infinite",
        fadeIn: "fadeIn 0.3s ease-out",
        slideUp: "slideUp 0.4s ease-out",
      },
    },
  },
};
```

Usage:

```tsx
<div className="animate-shimmer bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200">
  Loading...
</div>
```

## Tailwind Plugins

### Typography Plugin

```bash
pnpm add -D @tailwindcss/typography
```

```typescript
// tailwind.config.ts
export default {
  plugins: [
    require("@tailwindcss/typography"),
  ],
};
```

Usage:

```tsx
<article className="prose lg:prose-xl dark:prose-invert">
  <h1>Blog Post Title</h1>
  <p>Content goes here...</p>
</article>
```

### Forms Plugin

```bash
pnpm add -D @tailwindcss/forms
```

```typescript
// tailwind.config.ts
export default {
  plugins: [
    require("@tailwindcss/forms"),
  ],
};
```

### Container Queries Plugin

```bash
pnpm add -D @tailwindcss/container-queries
```

```typescript
// tailwind.config.ts
export default {
  plugins: [
    require("@tailwindcss/container-queries"),
  ],
};
```

Usage:

```tsx
<div className="@container">
  <div className="@sm:grid @sm:grid-cols-2 @lg:grid-cols-3">
    {/* Content */}
  </div>
</div>
```

## Custom Utilities

### Adding Custom Utilities

```css
/* packages/ui/src/styles/globals.css */
@layer utilities {
  .text-balance {
    text-wrap: balance;
  }

  .scrollbar-hide {
    -ms-overflow-style: none;
    scrollbar-width: none;
  }

  .scrollbar-hide::-webkit-scrollbar {
    display: none;
  }

  .glass {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
  }
}
```

### Plugin-Based Custom Utilities

```typescript
// tailwind.config.ts
import plugin from "tailwindcss/plugin";

export default {
  plugins: [
    plugin(function ({ addUtilities }) {
      addUtilities({
        ".no-scrollbar": {
          "-ms-overflow-style": "none",
          "scrollbar-width": "none",
          "&::-webkit-scrollbar": {
            display: "none",
          },
        },
        ".scrollbar-thin": {
          "scrollbar-width": "thin",
        },
      });
    }),
  ],
};
```

## Design Tokens

### Creating a Shared Preset

```typescript
// packages/ui/tailwind-preset.ts
import type { Config } from "tailwindcss";

const preset: Partial<Config> = {
  darkMode: ["class"],
  theme: {
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
};

export default preset;
```

Use in apps:

```typescript
// apps/web/tailwind.config.ts
import preset from "@sgcarstrends/ui/tailwind-preset";

export default {
  presets: [preset],
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      // App-specific extensions
    },
  },
};
```

## Dark Mode Configuration

### Class-Based Dark Mode

```typescript
// tailwind.config.ts
export default {
  darkMode: ["class"],
};
```

### Theme Toggle Implementation

```tsx
"use client";

import { useTheme } from "next-themes";
import { Button } from "@sgcarstrends/ui";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      {theme === "dark" ? "🌙" : "☀️"}
    </Button>
  );
}
```

### Provider Setup

```bash
pnpm add next-themes
```

```tsx
// app/providers.tsx
"use client";

import { ThemeProvider } from "next-themes";

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      {children}
    </ThemeProvider>
  );
}
```

## Responsive Design Patterns

### Mobile-First Approach

```tsx
// Default (mobile)
<div className="text-sm p-4">
  {/* Mobile styles */}
</div>

// Tablet and up
<div className="text-sm md:text-base p-4 md:p-6">
  {/* Tablet styles */}
</div>

// Desktop and up
<div className="text-sm md:text-base lg:text-lg p-4 md:p-6 lg:p-8">
  {/* Desktop styles */}
</div>
```

### Container Queries

```tsx
<div className="@container">
  <div className="grid grid-cols-1 @md:grid-cols-2 @lg:grid-cols-3 gap-4">
    {/* Responsive grid based on container */}
  </div>
</div>
```

## Performance Optimization

### Content Configuration

```typescript
// tailwind.config.ts
export default {
  content: [
    "./src/**/*.{ts,tsx}",
    // Only include what's needed
    "../../packages/ui/src/**/*.{ts,tsx}",
  ],
  // Safelist classes that are generated dynamically
  safelist: [
    "bg-red-500",
    "bg-green-500",
    "bg-blue-500",
  ],
};
```

### Purge Unused Styles

Tailwind automatically purges unused styles in production. For dynamic classes:

```typescript
// ❌ Bad - Won't be detected
<div className={`bg-${color}-500`}>

// ✅ Good - Use safelist or full class names
<div className={color === 'red' ? 'bg-red-500' : 'bg-blue-500'}>
```

## Debugging

### Enable JIT Debug Mode

```bash
# See which classes are being generated
TAILWIND_MODE=watch npx tailwindcss -i ./src/styles/globals.css -o ./dist/output.css --watch
```

### Check Configuration

```bash
# Inspect resolved config
npx tailwindcss config
```

### Common Issues

**Classes not applying:**
1. Check content paths include all component files
2. Verify CSS is imported in app
3. Check for typos in class names
4. Ensure build process is running

**Dark mode not working:**
1. Verify `darkMode: ["class"]` in config
2. Check ThemeProvider is set up
3. Ensure dark mode classes are in CSS

**Purge removing needed classes:**
1. Add to safelist
2. Use complete class names (not dynamic)
3. Check content paths

## Testing Tailwind Classes

```typescript
// __tests__/components/button.test.tsx
import { render } from "@testing-library/react";
import { Button } from "@sgcarstrends/ui";

describe("Button Tailwind Classes", () => {
  it("applies variant classes correctly", () => {
    const { container } = render(<Button variant="destructive">Delete</Button>);
    const button = container.querySelector("button");

    // Check if destructive variant classes are applied
    expect(button?.className).toContain("bg-destructive");
  });

  it("applies size classes correctly", () => {
    const { container } = render(<Button size="lg">Large</Button>);
    const button = container.querySelector("button");

    expect(button?.className).toContain("h-11");
  });
});
```

## References

- Tailwind CSS Documentation: https://tailwindcss.com
- Related files:
  - `packages/ui/tailwind.config.ts` - UI package config
  - `apps/web/tailwind.config.ts` - Web app config
  - `packages/ui/src/styles/globals.css` - Global styles
  - `packages/ui/CLAUDE.md` - UI package documentation

## Best Practices

1. **Mobile-First**: Design for mobile, then add larger breakpoints
2. **CSS Variables**: Use CSS variables for theming
3. **Reusable Presets**: Share configuration via presets
4. **Content Paths**: Include all component paths
5. **Safelist Sparingly**: Only safelist when absolutely necessary
6. **Semantic Names**: Use meaningful color names (brand, accent, not blue-500)
7. **Dark Mode**: Support dark mode from the start
8. **Performance**: Minimize custom utilities, use Tailwind defaults
9. **Size Utility**: Use `size-*` instead of `h-* w-*` when dimensions are equal (Tailwind v3.4+)

### Size Utility Convention

When an element needs equal height and width, use the `size-*` utility instead of separate `h-*` and `w-*` classes:

```tsx
// ✅ Good - Use size-* for equal dimensions
<div className="size-4">Icon</div>
<div className="size-8">Avatar</div>
<button className="size-10">Icon Button</button>

// ❌ Avoid - Redundant h-* and w-*
<div className="h-4 w-4">Icon</div>
<div className="h-8 w-8">Avatar</div>
<button className="h-10 w-10">Icon Button</button>

// ✅ Good - Different dimensions still use h-* and w-*
<div className="h-4 w-6">Rectangle</div>
<div className="h-full w-32">Sidebar</div>
```

**Common Use Cases:**
- Icons: `size-4`, `size-5`, `size-6`
- Avatars: `size-8`, `size-10`, `size-12`
- Icon buttons: `size-8`, `size-10`, `size-12`
- Loading spinners: `size-4`, `size-6`, `size-8`
- Square containers: `size-16`, `size-24`, `size-32`
