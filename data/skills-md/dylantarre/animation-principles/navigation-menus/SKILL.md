---
name: navigation-menus
description: Use when animating navigation bars, menus, sidebars, or wayfinding elements to create smooth, intuitive transitions
---

# Navigation & Menu Animation Principles

Apply Disney's 12 principles to navigation for fluid, intuitive wayfinding.

## Principles Applied to Navigation

### 1. Squash & Stretch
Menu items can compress slightly on click. Mobile hamburger icon lines should squash during transformation to X.

### 2. Anticipation
Before dropdown opens, trigger item can lift or highlight. Sidebar toggle icon rotates slightly before panel slides.

### 3. Staging
Active nav item should be clearly distinguished. Dropdown menus appear above other content via z-index and shadow. Focus hierarchy matters.

### 4. Straight Ahead & Pose to Pose
Define clear states: closed, opening, open, closing. Each menu item has default, hover, active, selected poses.

### 5. Follow Through & Overlapping Action
Dropdown items stagger in (20-30ms delay each). Submenu arrows rotate after text settles. Active indicator slides with slight overshoot.

### 6. Ease In & Ease Out
Menu open: `ease-out`. Menu close: `ease-in`. Hover transitions: `ease-in-out`. `cubic-bezier(0.4, 0, 0.2, 1)` for Material-style.

### 7. Arcs
Mobile nav sliding in from side should have slight arc. Menu indicator sliding between items can follow subtle curve path.

### 8. Secondary Action
While dropdown expands (primary), shadow grows (secondary), parent item stays highlighted (tertiary). Chevron rotates.

### 9. Timing
- Dropdown open: 200-250ms
- Dropdown close: 150-200ms
- Hover highlight: 100-150ms
- Active indicator slide: 200-300ms
- Stagger per item: 20-40ms
- Hamburger morph: 300ms

### 10. Exaggeration
Active indicator can overshoot and bounce back. Important nav items can pulse briefly for attention. Mega menus deserve bold entrances.

### 11. Solid Drawing
Maintain consistent spacing during animations. Shadows should be consistent. Icons should stay crisp at all animation frames.

### 12. Appeal
Smooth nav feels professional. Snappy responses build confidence. Navigation is used constantly, so invest in these micro-interactions.

## CSS Implementation

```css
.nav-dropdown {
  transform-origin: top;
  transition: transform 200ms ease-out,
              opacity 200ms ease-out;
}

.nav-dropdown.open {
  transform: scaleY(1);
  opacity: 1;
}

.nav-indicator {
  transition: transform 250ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

## Key Properties
- `transform`: translateX/Y, scaleY, rotate
- `opacity`: fade menus
- `height`/`max-height`: accordion menus
- `clip-path`: reveal effects
- `transform-origin`: dropdown direction
