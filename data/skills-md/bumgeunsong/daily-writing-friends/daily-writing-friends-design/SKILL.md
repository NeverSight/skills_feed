---
name: daily-writing-friends-design
description: Design system for Daily Writing Friends app. MUST use when doing ANY UI work including components, pages, buttons, forms, styling, Tailwind CSS, dark mode, theming, layouts, cards, inputs, or visual changes. Ensures consistent design tokens, button hierarchy, and accessibility.
---

# Daily Writing Friends Design System

Follow these guidelines for ALL UI-related work in this project.

## Design Documentation

For detailed reference, see the design docs:
- [tokens.md](../../../docs/design/tokens.md) - Colors, typography, spacing
- [buttons.md](../../../docs/design/buttons.md) - Button hierarchy and usage
- [components.md](../../../docs/design/components.md) - Cards, inputs, interactions
- [theme.md](../../../docs/design/theme.md) - Dark mode, accessibility, mobile

---

## Quick Reference

### Color System (CSS Variables)

```css
/* Light Mode */
--background: hsl(0, 0%, 100%);
--foreground: hsl(0, 0%, 9%);
--accent: hsl(210, 100%, 50%);

/* Dark Mode */
--background: hsl(180, 4%, 12%);
--foreground: hsl(180, 3%, 92%);
--accent: hsl(210, 100%, 70%);
```

### Button Hierarchy (Most to Least Important)

| Variant | Use For | Example |
|---------|---------|---------|
| `cta` | Critical conversions | Signup, Join, Main FAB |
| `default` | Main interactions | Login, Save, Submit |
| `outline` | Supporting actions | Drafts, Cancel |
| `ghost` | Subtle actions | Edit, Navigation, Logout |
| `destructive` | Dangerous actions | Delete (red ghost style) |

```tsx
// CTA - most important
<Button variant="cta">회원가입</Button>

// Primary - main action
<Button variant="default">글 저장</Button>

// Secondary - supporting
<Button variant="outline">임시 저장 글</Button>

// Ghost - subtle
<Button variant="ghost">수정</Button>

// Destructive - dangerous (ghost style with red text)
<Button variant="destructive">삭제</Button>
```

### Ghost Button Override Pattern

When ghost buttons need consistent styling on hover:
```tsx
<Button
  variant="ghost"
  className="text-foreground hover:bg-transparent hover:text-foreground"
>
```

### Component Styling

```tsx
// Card
<div className="bg-card border-border/50 reading-shadow rounded-lg p-4">

// Input
<input className="bg-input border-border reading-focus" />

// Link
<a className="text-ring hover:underline">
```

### Utility Classes

| Class | Purpose |
|-------|---------|
| `reading-shadow` | Adaptive shadow (light/dark) |
| `reading-hover` | Subtle accent highlight on hover |
| `reading-focus` | Focus ring (2px accent) |
| `text-reading` | Optimized reading (line-height 1.7) |
| `nav-selected` | Navigation selection state |
| `active-scale` | Press feedback (scale 0.99) |

### Dark Mode

- Strategy: Tailwind `darkMode: 'class'`
- Toggle: `useTheme()` hook from `@/shared/hooks/useTheme`
- Persistence: localStorage with OS preference fallback

```tsx
import { useTheme } from '@/shared/hooks/useTheme';

const { theme, toggleTheme } = useTheme();
```

### Spacing

- Major sections: `my-6` / `py-6`
- Minor sections: `my-3` / `py-3`
- Default: `space-y-4`, `p-4`
- Mobile: `px-3 md:px-4`

### Accessibility

- Touch targets: minimum 44x44px
- Color contrast: 4.5:1 for text, 3:1 for large text
- Focus visibility: use `reading-focus`
- Screen reader: use `sr-only` for hidden text

---

## Principles

1. **Premium minimal** - Less visual noise, Bear app style
2. **Content-first** - Remove decorative wrappers
3. **Consistent hierarchy** - Follow button/color hierarchy strictly
4. **Dual-mode** - All UI must work in both light and dark modes
5. **Mobile-first** - Responsive spacing and touch targets
