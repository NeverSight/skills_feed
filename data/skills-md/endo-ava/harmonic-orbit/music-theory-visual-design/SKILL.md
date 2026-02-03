---
name: music-theory-visual-design
description: Visual design guidelines for the music theory application. Use this skill when creating or improving UI components, designing new features, or working on visual aspects (typography, colors, spacing, animations). Applies to component creation, UI design, and visual styling tasks.
---

# Music Theory Visual Design

## Overview

This skill provides visual design guidelines for building UI components in the music theory application. It ensures consistent typography, color usage, spacing, and animations across all components while maintaining the application's distinctive aesthetic: modern, clean, with musical sophistication.

## Design Philosophy

Create interfaces that balance professional elegance with approachability. Think "concert hall meets digital instrument." Prioritize visual clarity while incorporating subtle musical character through the custom color system.

## Typography

**Font Families:**

- Use `font-sans` (Noto Sans JP) for UI elements
- Use `font-serif` (Noto Serif JP) sparingly for decorative text

**Weight Contrast:**

- Headings: `font-bold` (700) or `font-extrabold` (800)
- Body text: `font-normal` (400) or `font-light` (300)
- Emphasis: Extreme contrast (e.g., `font-extralight` (200) paired with `font-black` (900))

**Size Hierarchy:**

- Small labels: `text-xs` (0.75rem)
- Standard text: `text-sm` (0.875rem)
- Headings: `text-base` (1rem) → `text-lg` → `text-xl`

## Color System

**Use CSS Variables (not hex codes):**

- Backgrounds: `bg-background`, `bg-card`, `bg-panel`
- Text: `text-foreground`, `text-muted-foreground`
- Borders: `border-border`
- Interactive: `bg-accent`, `text-accent-foreground`
- Selected: `bg-selected`

**Musical Color System (84 colors):**

- For pitch-specific elements: `bg-key-c-lydian`, `text-key-g-dorian`
- Pattern: `bg-key-{pitch}-{mode}` (12 pitches × 7 modes)
- Use sparingly for music-theory-specific visualizations

**Transparency for Layering:**

- Subtle overlays: `bg-white/10`, `bg-black/5`
- Hover states: `hover:bg-white/25`
- Selected states: `bg-white/50`

## Spacing & Layout

**Consistent Spacing:**

- Internal padding: `p-4` (16px) standard
- Vertical stacking: `space-y-4`
- Grid gaps: `gap-4`

**Common Patterns:**

- Card: `bg-card border border-border rounded-lg p-4 shadow-sm`
- Panel: `bg-panel space-y-4`
- Full-height content: `h-[var(--content-height-full)]`

**Responsive:**

- Mobile-first: Apply styles without prefix
- Desktop: Use `md:` prefix (768px+)

## Animation & Motion

**Framer Motion Basics:**

```tsx
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.3 }}
>
```

**Hover Effects:**

- Subtle: `hover:bg-accent hover:text-accent-foreground transition-colors`
- Scale: `hover:scale-105 transition-transform`

**State Transitions:**

- Always use `transition-colors` or `transition-transform` for smooth changes
- Keep durations short (0.2-0.3s)

## Tailwind CSS Conventions

**className Management:**

- Always use `twMerge` for component className props:
  ```tsx
  className={twMerge('bg-card border rounded p-4', className)}
  ```
- Add `clsx` only when conditional logic is needed:
  ```tsx
  className={twMerge(clsx('base', isActive && 'text-primary'), className)}
  ```

**Responsibility Separation:**

- Parent (external): Size (`w-`, `h-`), position (`m-`, `p-`), responsive (`md:`)
- Child (internal): Appearance (`bg-`, `text-`, `border-`), internal layout (`flex`, `grid`)

**Example Component:**

```tsx
interface ComponentProps {
  className?: string;
}

export const Component: React.FC<ComponentProps> = ({ className }) => {
  return <div className={twMerge('bg-card rounded-lg border p-4', className)}>{/* content */}</div>;
};
```

## Accessibility

**Color Contrast:**

- Maintain WCAG AA (4.5:1 for text)
- The defined CSS variables already meet this standard

**Focus States:**

- Visible focus: `focus:ring-2 focus:ring-primary`
- Outline alternative: `focus:outline-2 focus:outline-accent`

**Visual Feedback:**

- Hover: `hover:bg-accent`
- Active: `active:scale-95`
- Disabled: `disabled:opacity-50 disabled:cursor-not-allowed`
