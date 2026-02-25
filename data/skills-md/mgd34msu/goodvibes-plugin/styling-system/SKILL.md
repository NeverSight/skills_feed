---
name: styling-system
description: "Load PROACTIVELY when task involves CSS architecture, theming, or visual design systems. Use when user says \"set up Tailwind\", \"add dark mode\", \"create a design system\", \"make it responsive\", or \"configure the theme\". Covers Tailwind configuration and custom plugins, design token systems, responsive breakpoint strategies, dark mode implementation, component variant patterns (CVA/class-variance-authority), CSS-in-JS alternatives, and animation patterns."
metadata:
  version: 1.0.0
  category: outcome
  tags: [css, tailwind, styling, theme, dark-mode, responsive, design-tokens]
---

## Resources
```
scripts/
  validate-styling.sh
references/
  styling-comparison.md
```

# Styling System

This skill guides you through CSS architecture decisions and implementation using GoodVibes precision tools. Use this workflow when setting up styling infrastructure, creating design systems, or implementing theming and responsive patterns.

## When to Use This Skill

Load this skill when:
- Setting up a new project's styling infrastructure
- Choosing between Tailwind, CSS Modules, CSS-in-JS, or vanilla CSS
- Implementing a design token system
- Adding dark mode support
- Creating responsive layouts and breakpoint strategies
- Migrating between styling approaches
- Building component variant systems
- Setting up animation patterns

Trigger phrases: "setup styling", "add Tailwind", "implement dark mode", "design tokens", "responsive design", "CSS architecture", "theme system".

## Core Workflow

### Phase 1: Discovery

Before making styling decisions, understand the project's current state.

#### Step 1.1: Detect Existing Styling Approach

Use `discover` to find styling patterns across the codebase.

```yaml
discover:
  queries:
    - id: tailwind_usage
      type: grep
      pattern: "(className=|class=).*\".*\\b(flex|grid|text-|bg-|p-|m-)"
      glob: "**/*.{tsx,jsx,vue,svelte}"
    - id: css_modules
      type: glob
      patterns: ["**/*.module.css", "**/*.module.scss"]
    - id: css_in_js
      type: grep
      pattern: "(styled\\.|styled\\(|css`|makeStyles|createStyles)"
      glob: "**/*.{ts,tsx,js,jsx}"
    - id: design_tokens
      type: glob
      patterns: ["**/tokens.{ts,js,json}", "**/design-tokens.{ts,js,json}", "**/theme.{ts,js}"]
    - id: dark_mode
      type: grep
      pattern: "(dark:|data-theme|ThemeProvider|useTheme|darkMode)"
      glob: "**/*.{ts,tsx,js,jsx,css,scss}"
  verbosity: count_only
```

**What this reveals:**
- Primary styling approach (Tailwind, CSS Modules, CSS-in-JS, vanilla)
- Whether design tokens exist
- Dark mode implementation status
- Consistency across the codebase

#### Step 1.2: Check Configuration Files

Read existing config to understand the setup.

```yaml
precision_read:
  files:
    - path: "tailwind.config.js"
      extract: content
    - path: "tailwind.config.ts"
      extract: content
    - path: "postcss.config.js"
      extract: content
    - path: "src/styles/globals.css"
      extract: outline
  verbosity: minimal
```

#### Step 1.3: Analyze Component Styling Patterns

Read representative components to understand conventions.

```yaml
precision_read:
  files:
    - path: "src/components/Button.tsx"  # or discovered component
      extract: content
    - path: "src/components/Card.tsx"
      extract: content
  output:
    max_per_item: 100
  verbosity: standard
```

### Phase 2: Decision Making

Choose the styling approach that fits your project needs. See `references/styling-comparison.md` for the complete decision tree.

#### Quick Decision Guide

**Use Tailwind CSS when:**
- You want rapid prototyping with utility classes
- Consistency across team is a priority
- You prefer design constraints over complete freedom
- You're building component-based UIs (React, Vue, Svelte)

**Use CSS Modules when:**
- You want scoped styles without build complexity
- You prefer writing traditional CSS
- You need coexistence with existing global styles
- Bundle size is a major concern (smaller than Tailwind)

**Use CSS-in-JS when:**
- You need runtime dynamic theming
- You want TypeScript types for style props
- Component-scoped styles with JS logic are required
- You're using styled-components or Emotion

**Use Vanilla CSS when:**
- You're building simple sites with minimal interactivity
- You want maximum control and minimal dependencies
- Progressive enhancement is critical
- You prefer cascade and inheritance patterns

For detailed framework-specific patterns, see `references/styling-comparison.md`.

### Phase 3: Configuration Setup

#### Step 3.1: Install Dependencies

Based on your chosen approach, install required packages.

**Tailwind CSS:**
```yaml
precision_exec:
  commands:
    - cmd: "npm install -D tailwindcss postcss autoprefixer"
      expect:
        exit_code: 0
    - cmd: "npx tailwindcss init -p"
      expect:
        exit_code: 0
  verbosity: minimal
```

**CSS-in-JS (styled-components):**
```yaml
precision_exec:
  commands:
    - cmd: "npm install styled-components"
    - cmd: "npm install -D @types/styled-components"
  verbosity: minimal
```

#### Step 3.2: Create Configuration

Write config files following best practices.

**Tailwind Config Example:**
```typescript
import type { Config } from 'tailwindcss';

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class', // or 'media' for system preference
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          // ... full scale
          900: '#0c4a6e',
        },
      },
      fontFamily: {
        sans: ['var(--font-inter)', 'system-ui', 'sans-serif'],
      },
      spacing: {
        '18': '4.5rem',
      },
    },
  },
  plugins: [],
};

export default config;
```

**Best Practices:**
- Use TypeScript for config files (type safety)
- Extend theme, don't replace defaults
- Use CSS variables for dynamic values
- Keep content paths specific to avoid slow builds
- Use the `class` strategy for dark mode (more control)

#### Step 3.3: Write Configuration Files

```yaml
precision_write:
  files:
    - path: "tailwind.config.ts"
      content: |
        import type { Config } from 'tailwindcss';
        // ... [full config]
    - path: "src/styles/globals.css"
      content: |
        @tailwind base;
        @tailwind components;
        @tailwind utilities;
        
        @layer base {
          :root {
            --background: 0 0% 100%;
            --foreground: 222.2 84% 4.9%;
            /* ... design tokens */
          }
          
          .dark {
            --background: 222.2 84% 4.9%;
            --foreground: 210 40% 98%;
          }
        }
  verbosity: count_only
```

### Phase 4: Design Token System

#### Step 4.1: Define Token Structure

Create a centralized token system for consistency.

**Token Categories:**
- **Colors**: Primary, secondary, neutral, semantic (success, error, warning)
- **Typography**: Font families, sizes, weights, line heights
- **Spacing**: Consistent scale (4px base, 8px increments)
- **Shadows**: Elevation system
- **Borders**: Radii, widths
- **Breakpoints**: Responsive design system
- **Animation**: Duration, easing functions

**Implementation Pattern:**
```typescript
// src/styles/tokens.ts
export const tokens = {
  colors: {
    primary: {
      light: '#3b82f6',
      DEFAULT: '#2563eb',
      dark: '#1d4ed8',
    },
    semantic: {
      success: '#10b981',
      error: '#ef4444',
      warning: '#f59e0b',
    },
  },
  spacing: {
    xs: '0.25rem',   // 4px
    sm: '0.5rem',    // 8px
    md: '1rem',      // 16px
    lg: '1.5rem',    // 24px
    xl: '2rem',      // 32px
  },
  typography: {
    fontFamily: {
      sans: ['Inter', 'system-ui', 'sans-serif'],
      mono: ['Fira Code', 'monospace'],
    },
    fontSize: {
      xs: ['0.75rem', { lineHeight: '1rem' }],
      sm: ['0.875rem', { lineHeight: '1.25rem' }],
      base: ['1rem', { lineHeight: '1.5rem' }],
      lg: ['1.125rem', { lineHeight: '1.75rem' }],
      xl: ['1.25rem', { lineHeight: '1.75rem' }],
    },
  },
} as const;

export type Tokens = typeof tokens;

// Integration with ThemeProvider (React Context)
type Theme = {
  tokens: Tokens;
  mode: 'light' | 'dark';
};

// Integration with styled-components
import 'styled-components';
declare module 'styled-components' {
  export interface DefaultTheme extends Tokens {
    mode: 'light' | 'dark';
  }
}

// Usage in components
import { useTheme } from 'styled-components';
const Button = styled.button`
  background: ${props => props.theme.colors.primary};
  padding: ${props => props.theme.spacing[4]};
`;
```

#### Step 4.2: Integrate Tokens with Tailwind

```typescript
// tailwind.config.ts
import { tokens } from './src/styles/tokens';

const config: Config = {
  theme: {
    extend: {
      colors: tokens.colors,
      spacing: tokens.spacing,
      fontFamily: tokens.typography.fontFamily,
      fontSize: tokens.typography.fontSize,
    },
  },
};
```

### Phase 5: Dark Mode Implementation

#### Step 5.1: Choose Dark Mode Strategy

**Class-based (Recommended):**
- More control over toggle behavior
- Can persist user preference
- Works with next-themes or similar libraries

**Media query-based:**
- Respects system preference only
- No JS required
- Less flexibility

#### Step 5.2: Setup next-themes (React/Next.js)

```typescript
// src/components/ThemeProvider.tsx
import { ThemeProvider as NextThemesProvider } from 'next-themes';
import type { ReactNode } from 'react';

interface ThemeProviderProps {
  children: ReactNode;
}

export function ThemeProvider({ children }: ThemeProviderProps) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      {children}
    </NextThemesProvider>
  );
}
```

#### Step 5.3: Define Dark Mode Color Scales

Use CSS variables for seamless theme switching.

```css
/* globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
  }
  
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
  }
}
```

**Best Practices:**
- Use HSL values for easier manipulation
- Keep semantic naming (background, foreground, primary)
- Test contrast ratios for accessibility (WCAG AA: 4.5:1)
- Avoid pure black (#000) in dark mode (use dark grays)

### Phase 6: Responsive Design Patterns

#### Step 6.1: Define Breakpoint Strategy

**Mobile-First Approach (Recommended):**
```css
/* Base styles for mobile */
.container {
  padding: 1rem;
}

/* Tablet and up */
@media (min-width: 768px) {
  .container {
    padding: 2rem;
  }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .container {
    padding: 3rem;
  }
}
```

**Tailwind Breakpoints:**
```tsx
<div className="p-4 md:p-8 lg:p-12">
  {/* padding increases with screen size */}
</div>
```

#### Step 6.2: Container Queries (Modern)

Use container queries for component-level responsiveness.

```css
.card-container {
  container-type: inline-size;
}

@container (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 1fr 2fr;
  }
}
```

**Tailwind Container Queries:**
```typescript
// tailwind.config.ts
plugins: [require('@tailwindcss/container-queries')]
```

```tsx
<div className="@container">
  <div className="@md:grid @md:grid-cols-2">
    {/* Responsive to container, not viewport */}
  </div>
</div>
```

### Phase 7: Component Variant Systems

#### Step 7.1: Install class-variance-authority (CVA)

```yaml
precision_exec:
  commands:
    - cmd: "npm install class-variance-authority clsx tailwind-merge"
  verbosity: minimal
```

#### Step 7.2: Create cn Utility

```typescript
// src/lib/utils.ts
import { type ClassValue, clsx } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

#### Step 7.3: Build Variant Components

```typescript
// src/components/Button.tsx
import { cva, type VariantProps } from 'class-variance-authority';
import { cn } from '@/lib/utils';
import type { ButtonHTMLAttributes } from 'react';

const buttonVariants = cva(
  // Base styles
  'inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 disabled:pointer-events-none disabled:opacity-50',
  {
    variants: {
      variant: {
        default: 'bg-primary text-primary-foreground hover:bg-primary/90',
        destructive: 'bg-destructive text-destructive-foreground hover:bg-destructive/90',
        outline: 'border border-input bg-background hover:bg-accent',
        ghost: 'hover:bg-accent hover:text-accent-foreground',
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
);

interface ButtonProps
  extends ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
}

export function Button({
  className,
  variant,
  size,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}
```

**Benefits:**
- Type-safe variant props
- Automatic Tailwind class merging
- Consistent component API
- Easy to extend with new variants

### Phase 8: Error State Styling

#### Step 8.1: Form Validation States

```typescript
// src/components/Input.tsx
import { cva } from 'class-variance-authority';
import { cn } from '@/lib/utils';

const inputVariants = cva(
  'w-full rounded-md border px-3 py-2 text-sm transition-colors',
  {
    variants: {
      state: {
        default: 'border-input focus:border-primary focus:ring-2 focus:ring-primary/20',
        error: 'border-destructive focus:border-destructive focus:ring-2 focus:ring-destructive/20',
        success: 'border-green-500 focus:border-green-500 focus:ring-2 focus:ring-green-500/20',
      },
    },
    defaultVariants: {
      state: 'default',
    },
  }
);

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  error?: string;
  success?: boolean;
}

export function Input({ error, success, className, ...props }: InputProps) {
  const state = error ? 'error' : success ? 'success' : 'default';
  
  return (
    <div className="space-y-1">
      <input
        className={cn(inputVariants({ state }), className)}
        aria-invalid={!!error}
        aria-describedby={error ? 'input-error' : undefined}
        {...props}
      />
      {error && (
        <p id="input-error" className="text-sm text-destructive" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
```

#### Step 8.2: Toast Notifications

```typescript
// src/components/Toast.tsx
import { cva } from 'class-variance-authority';

const toastVariants = cva(
  'rounded-lg border p-4 shadow-lg',
  {
    variants: {
      variant: {
        default: 'bg-background border-border',
        success: 'bg-green-50 border-green-200 text-green-900 dark:bg-green-950 dark:border-green-800 dark:text-green-100',
        error: 'bg-red-50 border-red-200 text-red-900 dark:bg-red-950 dark:border-red-800 dark:text-red-100',
        warning: 'bg-yellow-50 border-yellow-200 text-yellow-900 dark:bg-yellow-950 dark:border-yellow-800 dark:text-yellow-100',
      },
    },
  }
);
```

#### Step 8.3: Loading/Skeleton States

```css
/* Skeleton pulse animation */
@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.skeleton {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
  background-color: hsl(var(--muted));
  border-radius: 0.375rem;
}
```

```typescript
// src/components/Skeleton.tsx
export function Skeleton({ className, ...props }: React.HTMLAttributes<HTMLDivElement>) {
  return <div className={cn('skeleton', className)} {...props} />;
}

// Usage in loading states
export function CardSkeleton() {
  return (
    <div className="space-y-3">
      <Skeleton className="h-4 w-full" />
      <Skeleton className="h-4 w-3/4" />
      <Skeleton className="h-20 w-full" />
    </div>
  );
}
```

### Phase 9: Animation Patterns

#### Step 9.1: CSS Transitions (Lightweight)

```css
.button {
  transition: background-color 200ms ease-in-out;
}

.button:hover {
  background-color: var(--primary-hover);
}
```

**Tailwind:**
```tsx
<button className="transition-colors duration-200 hover:bg-primary-hover">
  Click me
</button>
```

#### Step 9.2: Framer Motion (Advanced)

For complex animations and gestures.

```typescript
// src/components/AnimatedCard.tsx
import { motion } from 'framer-motion';

export function AnimatedCard() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <div className="card">Content</div>
    </motion.div>
  );
}
```

**Best Practices:**
- Keep animations under 300ms for UI feedback
- Use easing functions (ease-in-out, ease-out)
- Respect `prefers-reduced-motion`
- Avoid animating layout-triggering properties (width, height)
- Prefer transform and opacity (GPU-accelerated)

### Phase 10: Validation

#### Step 10.1: Run Styling Validation Script

```bash
bash scripts/validate-styling.sh .
```

See `scripts/validate-styling.sh` for the complete validation suite.

#### Step 10.2: Check Build Output

Verify CSS bundle size and ensure no unused styles.

```yaml
precision_exec:
  commands:
    - cmd: "npm run build"
      expect:
        exit_code: 0
  verbosity: standard
```

**Check for:**
- CSS bundle size (<50KB gzipped for Tailwind is good)
- No duplicate utility classes
- Proper tree-shaking
- Dark mode classes generated correctly

#### Step 10.3: Accessibility Check

Ensure color contrast meets WCAG standards.

```yaml
precision_exec:
  commands:
    - cmd: "npx @axe-core/cli http://localhost:3000"
  verbosity: standard
```

#### Step 10.4: Visual Regression Testing

Catch unintended visual changes with automated screenshot comparison.

**Playwright with Visual Testing:**
```typescript
// tests/visual.spec.ts
import { test, expect } from '@playwright/test';

test('button variants match snapshots', async ({ page }) => {
  await page.goto('/components/button');
  
  // Take screenshot and compare
  await expect(page).toHaveScreenshot('button-variants.png', {
    maxDiffPixels: 100,
  });
});

test('dark mode toggle', async ({ page }) => {
  await page.goto('/');
  
  // Light mode
  await expect(page).toHaveScreenshot('home-light.png');
  
  // Toggle to dark
  await page.click('[data-testid="theme-toggle"]');
  await expect(page).toHaveScreenshot('home-dark.png');
});
```

**Chromatic (for Storybook):**
```bash
# Install and setup
npm install --save-dev chromatic

# Run visual tests
npx chromatic --project-token=<token>
```

**Percy (cross-browser):**
```typescript
import percySnapshot from '@percy/playwright';

test('responsive layout', async ({ page }) => {
  await page.goto('/dashboard');
  await percySnapshot(page, 'Dashboard - Desktop');
  
  await page.setViewportSize({ width: 375, height: 667 });
  await percySnapshot(page, 'Dashboard - Mobile');
});
```

#### Step 10.5: CSS Purging Configuration

**Tailwind v3+ with JIT:**
The `content` paths in `tailwind.config.ts` serve as the purge configuration. Tailwind automatically removes unused classes in production builds.

```typescript
// tailwind.config.ts
export default {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx}',
    './src/components/**/*.{js,ts,jsx,tsx}',
    './src/app/**/*.{js,ts,jsx,tsx}',
  ],
  // JIT mode is default in v3+
};
```

**Production Build Optimization:**
```bash
# Build with minification
npx tailwindcss -i ./src/styles/globals.css -o ./dist/output.css --minify

# Check final size
du -h dist/output.css
```

**Safelist Dynamic Classes:**
```typescript
// tailwind.config.ts
export default {
  content: ['./src/**/*.{js,ts,jsx,tsx}'],
  safelist: [
    // Dynamic classes that can't be detected statically
    'bg-red-500',
    'bg-green-500',
    'bg-blue-500',
    // Or use patterns
    {
      pattern: /bg-(red|green|blue)-(400|500|600)/,
    },
  ],
};
```

**Monitor Bundle Size:**
```yaml
precision_exec:
  commands:
    - cmd: "npm run build"
    - cmd: "ls -lh dist/**/*.css"
  verbosity: standard
```

Target: <50KB gzipped for typical Tailwind projects after purging.

## Common Anti-Patterns

**DON'T:**
- Mix styling approaches (Tailwind + CSS-in-JS in same components)
- Use inline styles for static values
- Hardcode colors/spacing (use design tokens)
- Ignore dark mode contrast ratios
- Use `!important` to override Tailwind (fix specificity instead)
- Animate width/height (causes layout thrashing)
- Skip mobile-first responsive design
- Use pixel values everywhere (prefer rem for accessibility)

**DO:**
- Choose one primary styling approach and be consistent
- Use CSS variables for dynamic values
- Implement design tokens from the start
- Test dark mode for contrast and readability
- Follow Tailwind's utility-first philosophy
- Animate transform and opacity for performance
- Design mobile-first, enhance for larger screens
- Use relative units (rem, em, %) for scalability

## Security Considerations

**CSP (Content Security Policy) and Styling:**

**Safe by Default (Build-time):**
- Tailwind CSS - Compiled at build time, no runtime injection
- CSS Modules - Compiled at build time, CSP-safe
- Vanilla CSS / SCSS - Served as static files

**Requires CSP Configuration (Runtime):**
- styled-components - Injects `<style>` tags at runtime
- Emotion - Injects styles at runtime
- Inline styles - May require `unsafe-inline` or nonce

**CSP Best Practices:**
```typescript
// Next.js example with CSP for styled-components
import { getCspNonce } from './lib/csp';

export default function RootLayout({ children }) {
  const nonce = getCspNonce();
  return (
    <html>
      <head>
        <meta
          httpEquiv="Content-Security-Policy"
          content={`style-src 'self' 'nonce-${nonce}';`}
        />
      </head>
      <body>
        <StyleSheetManager nonce={nonce}>
          {children}
        </StyleSheetManager>
      </body>
    </html>
  );
}
```

**CSS Injection Prevention:**
- Never interpolate unsanitized user input into CSS values
- Use allowlists for user-configurable colors/themes
- Validate color values before applying

```typescript
// DON'T: Unsafe user input interpolation
const BadButton = ({ userColor }) => (
  <div style={{ backgroundColor: userColor }} /> // CSS injection risk!
);

// DO: Validate against allowlist
const ALLOWED_COLORS = ['primary', 'secondary', 'accent'] as const;
type AllowedColor = typeof ALLOWED_COLORS[number];

const SafeButton = ({ color }: { color: AllowedColor }) => (
  <div className={`bg-${color}`} />
);

// DO: Validate hex colors
function isValidHexColor(color: string): boolean {
  return /^#[0-9A-Fa-f]{6}$/.test(color);
}
```

## Quick Reference

**Discovery Phase:**
```yaml
discover: { queries: [tailwind, css_modules, css_in_js, tokens, dark_mode], verbosity: count_only }
precision_read: { files: [tailwind.config.ts, globals.css], verbosity: minimal }
```

**Configuration Phase:**
```yaml
precision_exec: { commands: [{ cmd: "npm install -D tailwindcss postcss autoprefixer" }] }
precision_write: { files: [tailwind.config.ts, globals.css, tokens.ts], verbosity: count_only }
```

**Validation Phase:**
```bash
bash scripts/validate-styling.sh .
npm run build
```

For detailed decision trees, token examples, and framework-specific patterns, see `references/styling-comparison.md`.
