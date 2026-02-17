---
name: ui-design-system
description: >-
  Generates consistent UI components, layouts, and design tokens following a design system.
  Enforces spacing, color, typography, and accessibility standards across React/TypeScript
  projects. Use when creating new UI components, building page layouts, choosing colors or
  typography, setting up design tokens, or reviewing UI code for design consistency. Covers
  8pt spacing grid, Tailwind CSS token usage, shadcn/ui primitives, WCAG 2.1 AA compliance,
  responsive breakpoints, semantic HTML structure, and TypeScript component interfaces.
  Does NOT cover backend implementation (use python-backend-expert), testing (use
  react-testing-patterns), or deployment (use deployment-pipeline).
license: MIT
compatibility: 'React 18+, TypeScript 5+, Tailwind CSS 3+, shadcn/ui'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: implementation
allowed-tools: Read Edit Write Bash(npm:*) Bash(npx:*)
context: fork
---

# UI Design System

## When to Use

Activate this skill when:
- Creating new UI components that must follow a design system
- Building page layouts with consistent spacing and structure
- Setting up or extending design tokens (colors, typography, spacing)
- Choosing colors, fonts, or spacing values for a project
- Reviewing UI code for design consistency and accessibility
- Integrating shadcn/ui components into existing layouts

Do NOT use this skill for:
- Backend API implementation (use `python-backend-expert`)
- Component or hook testing (use `react-testing-patterns`)
- E2E browser testing (use `e2e-testing`)
- General React patterns unrelated to design system (use `react-frontend-expert`)
- Deployment or CI/CD (use `deployment-pipeline`)

## Instructions

### Step 0: Read Existing Design Tokens

Before generating any UI code, check the project for existing tokens:

1. Read `tailwind.config.ts` (or `.js`) for custom theme extensions
2. Read `src/styles/globals.css` or `app/globals.css` for CSS custom properties
3. Read `components.json` if shadcn/ui is configured

If no design tokens exist, generate a starter set and ask the user to confirm before proceeding (see Edge Cases).

### Design Tokens

#### Color Tokens

Define colors as CSS custom properties consumed by Tailwind. Never use hardcoded hex/rgb values in components.

**CSS custom properties (HSL format for shadcn/ui compatibility):**

```css
/* globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222 47% 11%;
    --primary: 221 83% 53%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96%;
    --secondary-foreground: 222 47% 11%;
    --muted: 210 40% 96%;
    --muted-foreground: 215 16% 47%;
    --accent: 210 40% 96%;
    --accent-foreground: 222 47% 11%;
    --destructive: 0 84% 60%;
    --destructive-foreground: 210 40% 98%;
    --border: 214 32% 91%;
    --input: 214 32% 91%;
    --ring: 221 83% 53%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222 47% 11%;
    --foreground: 210 40% 98%;
    --primary: 217 91% 60%;
    --primary-foreground: 222 47% 11%;
    --secondary: 217 33% 17%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217 33% 17%;
    --muted-foreground: 215 20% 65%;
    --accent: 217 33% 17%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 63% 31%;
    --destructive-foreground: 210 40% 98%;
    --border: 217 33% 17%;
    --input: 217 33% 17%;
    --ring: 224 76% 48%;
  }
}
```

**Tailwind config mapping:**

```ts
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
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
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
      },
    },
  },
} satisfies Config;
```

**Color usage rules:**
- Always use semantic token classes: `bg-primary`, `text-foreground`, `border-border`
- Never use raw Tailwind palette colors (`bg-blue-500`) in component code
- Every color must have a dark mode variant defined
- Use `foreground` variants for text on colored backgrounds

#### Typography Scale

Define a typographic scale using Tailwind's font-size utilities:

| Token | Size | Line Height | Usage |
|-------|------|-------------|-------|
| `text-xs` | 12px | 16px | Captions, helper text |
| `text-sm` | 14px | 20px | Secondary text, labels |
| `text-base` | 16px | 24px | Body text (default) |
| `text-lg` | 18px | 28px | Subheadings |
| `text-xl` | 20px | 28px | Section headings |
| `text-2xl` | 24px | 32px | Page headings |
| `text-3xl` | 30px | 36px | Hero headings |

**Typography rules:**
- Set a base font in `tailwind.config.ts`: `fontFamily: { sans: ["Inter", "system-ui", "sans-serif"] }`
- Use `font-medium` (500) for headings and labels, `font-normal` (400) for body
- Use `tracking-tight` for headings `text-2xl` and above
- Limit line length with `max-w-prose` (65ch) for readability

#### Spacing (8pt Grid)

All spacing values follow an 8pt base grid:

| Tailwind Class | Value | Use Case |
|---------------|-------|----------|
| `p-1` / `gap-1` | 4px | Inline icon padding, tight gaps |
| `p-2` / `gap-2` | 8px | Compact element spacing |
| `p-3` / `gap-3` | 12px | Input padding, small card padding |
| `p-4` / `gap-4` | 16px | Standard component padding |
| `p-6` / `gap-6` | 24px | Card padding, section gaps |
| `p-8` / `gap-8` | 32px | Section padding |
| `p-12` / `gap-12` | 48px | Page section spacing |
| `p-16` / `gap-16` | 64px | Major layout spacing |

**Spacing rules:**
- Use `gap-*` for flex/grid children instead of individual margins
- Prefer `space-y-*` for vertical stacking of sibling elements
- Cards: `p-6` padding with `gap-4` between internal elements
- Page sections: `py-12` or `py-16` vertical padding
- Never mix spacing systems (no `margin: 13px`)

### Component Structure

#### Hierarchy: Container > Layout > Content

Every component follows a three-layer structure:

```tsx
// Container: outer wrapper with spacing, background, border
<Card className="p-6">
  {/* Layout: flex/grid arrangement */}
  <div className="flex items-center gap-4">
    {/* Content: actual UI elements */}
    <Avatar src={user.avatar} alt={user.name} />
    <div className="space-y-1">
      <h3 className="text-sm font-medium">{user.name}</h3>
      <p className="text-sm text-muted-foreground">{user.role}</p>
    </div>
  </div>
</Card>
```

#### Semantic HTML

Use the correct HTML element for every purpose:

| Element | Use For | Not |
|---------|---------|-----|
| `<button>` | Clickable actions | `<div onClick>` |
| `<a>` | Navigation links | `<button>` for links |
| `<nav>` | Navigation regions | `<div>` |
| `<main>` | Primary page content | `<div>` |
| `<article>` | Self-contained content (card, post) | `<div>` |
| `<section>` | Thematic grouping with heading | `<div>` |
| `<aside>` | Sidebar or tangential content | `<div>` |
| `<header>` | Introductory content for a section | `<div>` |
| `<footer>` | Footer content for a section | `<div>` |
| `<ul>` / `<ol>` | Lists of items | `<div>` for each item |

#### shadcn/ui Primitives

Prefer shadcn/ui components over custom implementations:

| Need | Use | Not |
|------|-----|-----|
| Buttons | `<Button>` | Custom `<button>` with styles |
| Modals | `<Dialog>` | Custom modal with portal |
| Dropdowns | `<DropdownMenu>` | Custom dropdown |
| Cards | `<Card>` | Styled `<div>` |
| Inputs | `<Input>` | Styled `<input>` |
| Selects | `<Select>` | Native `<select>` |
| Tooltips | `<Tooltip>` | Custom tooltip |
| Tabs | `<Tabs>` | Custom tab component |
| Tables | `<Table>` | Plain `<table>` |
| Alerts | `<Alert>` | Custom banner div |

If shadcn/ui is not installed, fall back to plain Tailwind with equivalent patterns and consistent class ordering.

### TypeScript Component Interfaces

Export props as TypeScript interfaces with JSDoc descriptions:

```tsx
/** Props for the UserProfileCard component. */
interface UserProfileCardProps {
  /** User data to display. */
  user: User;
  /** Called when the edit button is clicked. */
  onEdit?: (userId: string) => void;
  /** Visual variant of the card. */
  variant?: "default" | "compact";
  /** Additional CSS classes applied to the root element. */
  className?: string;
}

export function UserProfileCard({
  user,
  onEdit,
  variant = "default",
  className,
}: UserProfileCardProps) {
  // ...
}
```

**Props rules:**
- Name interface `{ComponentName}Props`
- Include `className?: string` on every component for composition
- Use `variant` prop for visual variations, not separate components
- Default optional props in destructuring, not in interface
- Use union types for constrained string values: `"sm" | "md" | "lg"`

### Responsive Design

#### Breakpoints

Use Tailwind's mobile-first breakpoints:

| Prefix | Min Width | Target |
|--------|-----------|--------|
| (none) | 0px | Mobile (default) |
| `sm:` | 640px | Large phones / small tablets |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Desktops |
| `xl:` | 1280px | Large desktops |

**Responsive rules:**
- Design mobile-first: base styles for mobile, then add breakpoint overrides
- Use `grid-cols-1 md:grid-cols-2 lg:grid-cols-3` for responsive grids
- Stack navigation vertically on mobile: `flex-col md:flex-row`
- Hide non-essential elements on mobile: `hidden md:block`
- Set max container width: `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`

#### Responsive Layout Pattern

```tsx
<div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    {items.map((item) => (
      <ItemCard key={item.id} item={item} />
    ))}
  </div>
</div>
```

### Accessibility (WCAG 2.1 AA)

#### Contrast Ratios

- Normal text (< 18px or < 14px bold): minimum 4.5:1 contrast ratio
- Large text (>= 18px or >= 14px bold): minimum 3:1 contrast ratio
- UI components and graphical objects: minimum 3:1 contrast ratio

#### Interactive Element Requirements

Every interactive element must have:

1. **Visible label or aria-label:** `<Button aria-label="Close dialog">X</Button>`
2. **Focus indicator:** Tailwind's `ring` utilities: `focus-visible:ring-2 focus-visible:ring-ring`
3. **Keyboard access:** Reachable via Tab, activatable via Enter/Space
4. **Disabled state:** Both visual and `aria-disabled` or `disabled` attribute

#### ARIA Patterns

- Icon-only buttons: `aria-label="Delete item"`
- Loading states: `aria-busy="true"` on the loading container
- Dynamic content updates: `aria-live="polite"` on the container
- Form errors: `aria-invalid="true"` on the input, `role="alert"` on the message
- Modals: `aria-modal="true"`, focus trap, Escape to close
- Navigation landmarks: `<nav aria-label="Main navigation">`

## Examples

### User Profile Card

```tsx
interface UserProfileCardProps {
  user: { id: string; name: string; role: string; avatarUrl: string };
  onEdit?: (userId: string) => void;
  className?: string;
}

export function UserProfileCard({ user, onEdit, className }: UserProfileCardProps) {
  return (
    <Card className={cn("p-6", className)}>
      <div className="flex items-center gap-4">
        <Avatar className="h-12 w-12">
          <AvatarImage src={user.avatarUrl} alt={user.name} />
          <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
        </Avatar>
        <div className="space-y-1">
          <h3 className="text-sm font-medium leading-none">{user.name}</h3>
          <p className="text-sm text-muted-foreground">{user.role}</p>
        </div>
      </div>
      {onEdit && (
        <div className="mt-4">
          <Button
            variant="outline"
            size="sm"
            onClick={() => onEdit(user.id)}
            aria-label={`Edit ${user.name}'s profile`}
          >
            Edit Profile
          </Button>
        </div>
      )}
    </Card>
  );
}
```

### SaaS Dashboard Design Tokens Setup

**Tailwind config extension:**

```ts
// tailwind.config.ts
import type { Config } from "tailwindcss";

export default {
  theme: {
    extend: {
      colors: {
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
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
} satisfies Config;
```

### Responsive Dashboard Layout

```tsx
export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b border-border" aria-label="Main navigation">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center">
          {/* nav content */}
        </div>
      </nav>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-[240px_1fr] gap-8">
          <aside className="hidden lg:block" aria-label="Sidebar">
            {/* sidebar content */}
          </aside>
          <main>{children}</main>
        </div>
      </div>
    </div>
  );
}
```

## Edge Cases

- **No existing design tokens:** Generate a starter token set (see `references/design-tokens-reference.md`) and present it to the user for confirmation before writing any component code. Ask: "No design tokens found. Here's a starter set — should I apply these?"

- **shadcn/ui not installed:** Fall back to plain Tailwind with equivalent patterns. Use `<button className="...">` instead of `<Button>`, styled `<div>` instead of `<Card>`. Maintain the same spacing and color token approach.

- **Component overlap:** If a requested component duplicates an existing one, flag it: "A similar `UserCard` component exists at `src/components/UserCard.tsx`. Should I extend it or create a separate component?"

- **Dark mode tokens missing:** If `:root` tokens exist but `.dark` variants are absent, generate matching dark variants before proceeding. Every semantic color token must have both light and dark values.

- **Custom brand colors:** When the user provides specific brand hex values, convert them to HSL and integrate into the token system. Never use the hex values directly in components.

- **Inconsistent spacing in existing code:** Flag the inconsistency, suggest the closest 8pt grid values, and ask whether to normalize existing components or only apply the grid to new code.

See `references/design-tokens-reference.md` for starter token sets, color palette guide, and typography scales.
