---
name: mobile-app-ux
description: Mobile app UX/UI best practices for smartphone interfaces. Use for designing touch-friendly interfaces, mobile navigation patterns, gesture handling, and optimizing user experience on small screens. Triggers on requests for mobile UX, app design, touch interfaces, mobile patterns, or smartphone UI best practices.
---

# Mobile App UX Best Practices

## Touch Target Guidelines

| Element | Minimum Size | Recommended | Spacing |
|---------|-------------|-------------|---------|
| Buttons | 44×44px | 48×48px | 8px between |
| Icons | 24×24px | 24×24px + 44px touch area | 12px between |
| List items | 44px height | 48-56px height | No gap needed |
| Form inputs | 44px height | 48px height | 16px between |

```css
.touch-target {
  min-height: 44px;
  min-width: 44px;
  padding: var(--space-3);
}

/* Expand touch area without visual change */
.icon-button {
  position: relative;
}
.icon-button::after {
  content: '';
  position: absolute;
  inset: -8px;
}
```

## ✅ Do's

### Navigation
- Bottom navigation for 3-5 primary actions
- Keep most important actions within thumb reach
- Use clear, recognizable icons with labels
- Provide visual feedback on active state
- Support swipe gestures for natural navigation

### Content
- Prioritize content over chrome (UI elements)
- Use progressive disclosure - show essentials first
- Lazy load content below the fold
- Provide pull-to-refresh for dynamic content
- Show skeleton screens, not spinners

### Forms
- Use appropriate keyboard types (email, tel, number)
- Show inline validation, not after submit
- Provide autocomplete where possible
- Group related fields visually
- Save form progress automatically

### Feedback
- Immediate visual response to all touches
- Haptic feedback for important actions
- Clear loading states with progress indication
- Confirmation for destructive actions
- Undo option instead of "Are you sure?"

## ❌ Don'ts

### Navigation
- ❌ Hamburger menus for primary navigation
- ❌ Deep navigation hierarchies (>3 levels)
- ❌ Small, closely spaced tap targets
- ❌ Gestures without visual affordances
- ❌ Hiding essential actions in menus

### Content
- ❌ Horizontal scrolling for content
- ❌ Tiny text (<16px for body copy)
- ❌ Low contrast text on images
- ❌ Auto-playing video with sound
- ❌ Interstitials blocking content

### Forms
- ❌ Required fields without indication
- ❌ Generic error messages
- ❌ Disabling zoom on inputs
- ❌ Dropdowns for <5 options (use radio)
- ❌ Multi-step forms without progress indicator

### Interaction
- ❌ Double-tap to activate
- ❌ Hover-dependent interactions
- ❌ Precise targeting requirements
- ❌ Long press without alternative
- ❌ Blocking the UI during operations

## Thumb Zone Design

```
┌─────────────────────┐
│    Hard to reach    │  ← Secondary actions, menu
│                     │
├─────────────────────┤
│   Natural reach     │  ← Content, scrollable area
│                     │
├─────────────────────┤
│    Easy reach       │  ← Primary actions, nav
└─────────────────────┘
```

```css
/* Bottom-anchored primary actions */
.primary-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  padding: var(--space-4);
  padding-bottom: env(safe-area-inset-bottom, var(--space-4));
}
```

## Component Patterns

### Bottom Sheet

```tsx
interface BottomSheetProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
}

export const BottomSheet: FC<BottomSheetProps> = ({ isOpen, onClose, children }) => (
  <>
    {isOpen && <div className="overlay" onClick={onClose} />}
    <div className={cn('bottom-sheet', isOpen && 'bottom-sheet--open')}>
      <div className="bottom-sheet__handle" />
      {children}
    </div>
  </>
);
```

### Swipeable Card

```tsx
export const SwipeableCard: FC<Props> = ({ onSwipeLeft, onSwipeRight, children }) => {
  const handlers = useSwipeable({
    onSwipedLeft: onSwipeLeft,
    onSwipedRight: onSwipeRight,
    trackMouse: false,
  });
  
  return <div {...handlers}>{children}</div>;
};
```

## Performance Checklist

- [ ] First Contentful Paint < 1.8s
- [ ] Time to Interactive < 3.8s
- [ ] Images optimized and lazy-loaded
- [ ] Animations at 60fps
- [ ] No layout shifts during load
- [ ] Works offline (PWA)

## Accessibility

- Use semantic HTML (`<button>`, `<nav>`, `<main>`)
- Support screen readers (aria-labels)
- Ensure 4.5:1 color contrast minimum
- Support text scaling up to 200%
- Never disable pinch-to-zoom
