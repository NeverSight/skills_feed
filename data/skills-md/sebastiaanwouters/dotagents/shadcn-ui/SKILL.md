---
name: shadcn-ui
description: Build UIs with shadcn/ui components. Covers CLI commands, component installation, theming with CSS variables, OKLCH colors, and customization patterns. Triggers on shadcn, shadcn-ui, add component, or theming questions.
---

# shadcn/ui

Copy-paste component library built on Radix UI + Tailwind CSS. Components are NOT imported from a package—they're copied into your project for full ownership.

## Quick Reference

```bash
# Initialize project
npx shadcn@latest init

# Add components
npx shadcn@latest add button card dialog

# Add all components
npx shadcn@latest add -a

# View component source before adding
npx shadcn@latest view button
```

## CLI Commands

### init
```bash
npx shadcn@latest init [options]

Options:
  -t, --template <template>    # next, vite, start, next-monorepo
  -b, --base-color <color>     # neutral, gray, zinc, stone, slate
  --css-variables              # Use CSS variables (default)
  --no-css-variables           # Inline Tailwind classes
  -y, --yes                    # Skip prompts
```

### add
```bash
npx shadcn@latest add [components...]

Options:
  -y, --yes          # Skip confirmation
  -o, --overwrite    # Overwrite existing
  -a, --all          # Add all components
  -p, --path <path>  # Custom install path
```

## Theming System

shadcn/ui uses CSS variables with OKLCH color format for perceptual uniformity.

### CSS Variables Structure

```css
/* app/globals.css */
:root {
  --radius: 0.625rem;
  
  /* Semantic colors */
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
}

.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --primary: oklch(0.985 0 0);
  --primary-foreground: oklch(0.205 0 0);
  /* ... inverted values */
}

/* Map to Tailwind */
@theme inline {
  --color-background: var(--background);
  --color-foreground: var(--foreground);
  --color-primary: var(--primary);
  --color-primary-foreground: var(--primary-foreground);
  /* ... all semantic colors */
}
```

### OKLCH Format

```
oklch(lightness chroma hue)
     0-1       0-0.4   0-360°
```

- **Lightness**: 0 = black, 1 = white
- **Chroma**: 0 = gray, higher = more saturated
- **Hue**: Color angle (0=red, 120=green, 240=blue)

### Adding Custom Colors

```css
:root {
  --warning: oklch(0.84 0.16 84);
  --warning-foreground: oklch(0.28 0.07 46);
}

.dark {
  --warning: oklch(0.41 0.11 46);
  --warning-foreground: oklch(0.99 0.02 95);
}

@theme inline {
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
}
```

Usage: `className="bg-warning text-warning-foreground"`

### Base Color Palettes

Choose in `components.json`:
- **neutral**: Pure achromatic
- **stone**: Warm grayscale
- **zinc**: Cool grayscale  
- **gray**: Balanced with slight tint
- **slate**: Blue-tinted gray

## Configuration

### components.json

```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "",
    "css": "app/globals.css",
    "baseColor": "neutral",
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

## Component Patterns

### CVA Variants

Components use class-variance-authority for variant management:

```tsx
import { cva, type VariantProps } from "class-variance-authority"

const buttonVariants = cva(
  "inline-flex items-center justify-center rounded-md text-sm font-medium transition-all disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-white hover:bg-destructive/90",
        outline: "border bg-background hover:bg-accent",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 px-3 text-xs",
        lg: "h-10 px-6",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)
```

### cn Utility

Merges classes intelligently, resolving Tailwind conflicts:

```tsx
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

### Compound Components

```tsx
<Card>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content here</CardContent>
  <CardFooter>Footer actions</CardFooter>
</Card>
```

### Data Attributes

Components include `data-slot` for semantic styling:

```tsx
<div data-slot="card" className={cn(...)}>
<button data-slot="button" data-variant="default">
```

## Customization

### Override Component Styles

```tsx
// The className prop merges with defaults
<Button className="w-full rounded-full" />
```

### Extend Variants

Edit the component file directly:

```tsx
const buttonVariants = cva(baseClasses, {
  variants: {
    variant: {
      // existing...
      success: "bg-green-600 text-white hover:bg-green-700",
    },
  },
})
```

### Dark Mode

Uses class strategy. Toggle `.dark` on html/body:

```tsx
// Toggle dark mode
document.documentElement.classList.toggle('dark')
```

## Dependencies

Required packages (installed by init):
- `class-variance-authority` - Variant management
- `clsx` - Class concatenation
- `tailwind-merge` - Conflict resolution
- `lucide-react` - Icons
- `tw-animate-css` - Animations
- `@radix-ui/*` - Accessible primitives (per component)

## Common Tasks

### Change Theme Colors

1. Edit CSS variables in `globals.css`
2. Both `:root` (light) and `.dark` (dark) selectors
3. Use OKLCH values for best results

### Add New Semantic Color

1. Define CSS variable in `:root` and `.dark`
2. Map in `@theme inline` block
3. Use with Tailwind: `bg-{name} text-{name}-foreground`

### Switch Base Palette

Update `components.json`:
```json
"tailwind": {
  "baseColor": "zinc"
}
```

Then re-run `npx shadcn@latest init` or manually update CSS variables.

## Attribution

Based on [shadcn/ui](https://github.com/shadcn-ui/ui) by shadcn.
