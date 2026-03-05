---
name: universal-elements
description: Use when animating any UI element not covered by specific skills, or when applying general animation principles across multiple element types
---

# Universal Element Animation Principles

Apply Disney's 12 principles to any UI element for consistent, professional motion design.

## Universal Application of Principles

### 1. Squash & Stretch
Any element that responds to interaction can squash (compress on impact/press) and stretch (extend on release). Keep it subtle: 2-5% maximum for UI.

### 2. Anticipation
Before any significant action, a brief preparatory motion signals what's coming. Scale down before scale up, pull back before push forward. 50-100ms duration.

### 3. Staging
Direct attention to the most important element. Use contrast in motion, size, color, z-index, and blur to create clear visual hierarchy.

### 4. Straight Ahead & Pose to Pose
Pose-to-pose for most UI: define start and end states clearly. Straight-ahead for organic, flowing animations like particles or organic shapes.

### 5. Follow Through & Overlapping Action
Nothing stops all at once. Child elements lag behind parents. Shadows settle after objects. Stagger related elements 20-50ms apart.

### 6. Ease In & Ease Out
The golden rule: never use `linear` for UI motion. Enter with `ease-out`, exit with `ease-in`, transition with `ease-in-out`.

### 7. Arcs
Natural motion follows curved paths. Add subtle vertical movement to horizontal transitions. Rotate while translating. Avoid robotic straight lines.

### 8. Secondary Action
Every primary action deserves supporting animation. Shadow changes, color shifts, icon rotations, glow effects reinforce without competing.

### 9. Timing
| Element Type | Fast | Normal | Slow |
|--------------|------|--------|------|
| Micro (icons, buttons) | 50-100ms | 100-200ms | 200-300ms |
| Small (cards, inputs) | 150-200ms | 200-300ms | 300-400ms |
| Medium (modals, menus) | 200-250ms | 250-350ms | 350-500ms |
| Large (pages, overlays) | 300-400ms | 400-600ms | 600-800ms |

### 10. Exaggeration
Match animation intensity to context. Celebratory moments allow 20-30% exaggeration. Professional contexts keep it under 10%. Error states can be more dramatic.

### 11. Solid Drawing
Maintain visual consistency: border-radius ratios, shadow directions, spacing rhythms, typography scale. Nothing should distort or break during animation.

### 12. Appeal
The goal is delight without distraction. Smooth animations build trust. Snappy feedback feels responsive. The best animation is felt, not noticed.

## CSS Foundation

```css
/* Universal transition base */
* {
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Standard durations as custom properties */
:root {
  --duration-fast: 100ms;
  --duration-normal: 200ms;
  --duration-slow: 350ms;
  --ease-out: cubic-bezier(0.0, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-standard: cubic-bezier(0.4, 0, 0.2, 1);
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.27, 1.55);
}

/* Apply to any interactive element */
.interactive {
  transition: transform var(--duration-normal) var(--ease-standard),
              opacity var(--duration-normal) var(--ease-standard),
              box-shadow var(--duration-normal) var(--ease-standard);
}
```

## Key Properties (Any Element)
- `transform`: universal positioning and scaling
- `opacity`: visibility transitions
- `transition`: state changes
- `animation`: complex sequences
- `box-shadow`: depth and emphasis
