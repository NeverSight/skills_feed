---
name: design-systems
description: Design tokens, spacing scales, color systems, and typography for building consistent UIs. Use when creating design systems, theming, or establishing UI foundations.
version: 1.0.0
---

# Design Systems

This skill covers the foundational elements of design systems — design tokens, spacing scales, color systems, typography, and naming conventions that enable consistent user experiences.

## Use-When

This skill activates when:
- Agent creates or maintains a design system
- Agent establishes theming or CSS variables
- Agent builds reusable components
- Agent needs consistent spacing/color/typography
- Agent configures Tailwind or similar CSS frameworks

## Core Rules

- ALWAYS use design tokens (variables) instead of hardcoded values
- ALWAYS use a consistent spacing scale (4px or 8px base)
- ALWAYS use semantic color roles (primary, secondary, destructive) over color names
- ALWAYS use a typography scale with limited font sizes
- ALWAYS name tokens semantically (background-primary, not background-blue-500)

## Common Agent Mistakes

- Using arbitrary values (margin-6, color-red-500) instead of tokens
- Creating new colors instead of reusing system colors
- Using too many font sizes (stick to 3-4)
- Hardcoding values that should be tokens

## Examples

### ✅ Correct

```tsx
// Using design tokens/variables
<div className="p-4 gap-4">
  <span className="text-primary text-sm font-medium">
    Consistent spacing and semantic colors
  </span>
</div>

// CSS variables (design tokens)
:root {
  --spacing-1: 0.25rem;  // 4px base
  --spacing-2: 0.5rem;   // 8px
  --spacing-4: 1rem;     // 16px
  --color-primary: #0f172a;
  --color-secondary: #64748b;
}
```

### ❌ Wrong

```tsx
// Arbitrary values
<div className="p-6 gap-5">
  <span className="text-blue-600 text-[15px]">
    Magic numbers and hardcoded colors
  </span>
</div>
```

## References

- [Design Tokens W3C Spec](https://designtokens.org/)
- [Tailwind Theme Configuration](https://tailwindcss.com/docs/theme)
- [Design Systems for Developers](https://www.designsystems.com/)
