---
name: canvas-styling-conventions
description:
  Style Canvas components with Tailwind CSS 4 theme tokens and approved utility
  patterns. Use when (1) Creating a new component, (2) Adding colors or styling
  to components, (3) Working with Tailwind theme tokens, (4) Adding or updating
  design tokens in global.css, (5) Creating color/style props, (6) Any change
  where component props are added/removed/renamed/retyped and can affect
  rendered styles. Covers @theme variables, CVA variants, and cn() utility.
---

## Technology stack

| Technology                           | Purpose            |
| ------------------------------------ | ------------------ |
| Tailwind CSS 4.1+                    | Styling            |
| class-variance-authority (CVA)       | Component variants |
| `clsx` + `tailwind-merge` via `cn()` | Class name merging |

Only use these dependencies for styling. Do not add third-party CSS libraries or
create new styling utilities.

## Styling conventions

- Use Tailwind's theme colors (`primary-*`, `gray-*`) defined in `global.css`.
- Avoid hardcoded color values; use theme tokens instead.
- Follow the existing focus, hover, and active state patterns from examples.

## The cn() utility

Use `cn()` to merge Tailwind classes. It combines `clsx` for conditional classes
with `tailwind-merge` to resolve conflicting utilities. Import from either
source:

```jsx
import { cn } from "@/lib/utils";
// or
import { cn } from "drupal-canvas";
```

Example usage:

```jsx
const Button = ({ variant, className, children }) => (
  <button
    className={cn(
      "rounded px-4 py-2",
      variant === "primary" && "bg-primary-600 text-white",
      variant === "secondary" && "bg-gray-200 text-gray-800",
      className,
    )}
  >
    {children}
  </button>
);
```

## Accept className for style customization

Every component should accept a `className` prop to allow style overrides. Pass
it to `cn()` as the last argument so consumer classes take precedence.

```jsx
const Card = ({ colorScheme, className, children }) => (
  <div className={cn(cardVariants({ colorScheme }), className)}>{children}</div>
);
```

`className` is an implementation/composition prop, not an editor prop. Do not
add `className` to `component.yml`, do not mark it as required, and do not
surface it in Canvas metadata.

## Tailwind 4 theme variables

Canvas projects use Tailwind CSS 4's `@theme` directive to define design tokens
in `global.css`. Variables defined inside `@theme { }` automatically become
available as Tailwind utility classes.

**Always check `global.css` for available design tokens.** The `@theme` block is
the source of truth for colors, fonts, breakpoints, and other design tokens.

### How theme variables map to utility classes

When you define a CSS variable in `@theme`, Tailwind 4 automatically generates
corresponding utility classes based on the variable's namespace prefix:

| CSS Variable in `@theme`    | Generated Utility Classes                                  |
| --------------------------- | ---------------------------------------------------------- |
| `--color-primary-600: #xxx` | `bg-primary-600`, `text-primary-600`, `border-primary-600` |
| `--color-gray-100: #xxx`    | `bg-gray-100`, `text-gray-100`, `border-gray-100`          |
| `--font-sans: ...`          | `font-sans`                                                |
| `--breakpoint-md: 48rem`    | `md:` responsive prefix                                    |

The pattern is: `--{namespace}-{name}` becomes `{utility}-{name}`.

### Examples

Given this definition in `global.css`:

```css
@theme {
  --color-primary-600: #1899cb;
  --color-primary-700: #1487b4;
}
```

You can use these colors with any color-accepting utility:

```jsx
// Correct
<button className="bg-primary-600 hover:bg-primary-700 text-white">
  Click me
</button>

// Wrong
<button className="bg-[#1899cb] text-white hover:bg-[#1487b4]">Click me</button>
```

Arbitrary values (e.g., `bg-[#xxx]`) are acceptable for rare, one-off cases
where adding a theme variable would be overkill. However, if a color appears in
multiple places or represents a brand/design system value, add it to `@theme`
instead.

### Semantic aliases

Theme variables can reference other variables to create semantic aliases:

```css
@theme {
  --color-primary-700: #1487b4;
  --color-primary-dark: var(--color-primary-700);
}
```

Both `bg-primary-700` and `bg-primary-dark` will work. Use semantic aliases when
they better express intent (e.g., `primary-dark` for a darker brand variant).

### Adding or updating theme variables

When a design requires a color, font, or other value not yet defined in the
theme, add it to the `@theme` block in `global.css` rather than hardcoding the
value in a component.

**When to add new theme variables:**

- A design introduces a new brand color or shade
- You need a semantic alias for an existing value (e.g., `--color-accent`)
- The design uses a specific spacing, font, or breakpoint value repeatedly

**When to update existing theme variables:**

- The brand colors change (update the hex values)
- Design tokens need adjustment across the system

**Example - adding a new color:**

```css
@theme {
  /* Existing tokens */
  --color-primary-600: #1899cb;

  /* New token for a success state */
  --color-success: #22c55e;
  --color-success-dark: #16a34a;
}
```

After adding, you can immediately use `bg-success`, `text-success-dark`, etc.

**Keep the theme organized.** Group related tokens together with comments
explaining their purpose. Follow the existing naming conventions in `global.css`
(e.g., numbered shades like `primary-100` through `primary-900`, semantic names
like `primary-dark`).

## Color props must use variants, not color codes

**Never create props that allow users to pass color codes** (hex values, RGB,
HSL, or any raw color strings). Instead, define a small set of human-readable
variants using CVA that map to the design tokens in `global.css`.

**Always check `global.css` for available design tokens.** The tokens defined
there (such as `primary-*`, `gray-*`, etc.) are the source of truth for color
values.

**Wrong - allowing raw color values:**

```yaml
# Wrong
props:
  properties:
    backgroundColor:
      title: Background Color
      type: string
      examples:
        - "#3b82f6"
```

```jsx
// Wrong
const Card = ({ backgroundColor }) => (
  <div style={{ backgroundColor }}>{/* ... */}</div>
);
```

**Correct - using CVA variants with design tokens:**

```yaml
# Correct
props:
  properties:
    colorScheme:
      title: Color Scheme
      type: string
      enum:
        - default
        - primary
        - muted
        - dark
      meta:enum:
        default: Default (White)
        primary: Primary (Blue)
        muted: Muted (Light Gray)
        dark: Dark
      examples:
        - default
```

```jsx
// Correct
import { cva } from "class-variance-authority";

const cardVariants = cva("rounded-lg p-6", {
  variants: {
    colorScheme: {
      default: "bg-white text-black",
      primary: "bg-primary-600 text-white",
      muted: "bg-gray-100 text-gray-700",
      dark: "bg-gray-900 text-white",
    },
  },
  defaultVariants: {
    colorScheme: "default",
  },
});

const Card = ({ colorScheme, children }) => (
  <div className={cardVariants({ colorScheme })}>{children}</div>
);
```

This approach ensures:

- Consistent colors across the design system
- Users select from curated, meaningful options (not arbitrary values)
- Easy theme updates by modifying `global.css` tokens
- Better accessibility through tested color combinations
