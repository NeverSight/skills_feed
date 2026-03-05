---
name: medium-300-500ms
description: Use when building standard animations between 300-500ms - page transitions, significant UI changes, animated illustrations that need clear communication
---

# Medium Animations (300-500ms)

The 300-500ms range is **standard animation territory**. Long enough to be watched, short enough to not impede flow. The workhorse duration for meaningful motion.

## Disney Principles at Medium Duration

### All 12 Principles Applicable

**Squash & Stretch**: Full expression - visible deformation for bouncing, elastic elements. 15-25% stretch feels natural.

**Anticipation**: Clear preparation - 80-120ms anticipation before main action. Pull back before push forward.

**Staging**: Multi-element choreography possible - primary action leads, supporting elements follow.

**Straight Ahead/Pose to Pose**: Pose to pose recommended - define key positions, let easing handle in-betweens.

**Follow Through**: Essential - overlapping action where parts settle at different rates.

**Slow In/Slow Out**: Critical for naturalism - both directions need proper easing.

**Arcs**: Natural motion paths - elements should travel on curves matching real physics.

**Secondary Action**: Multiple secondary actions - hair follows head, shadow follows object.

**Timing**: 18-30 frames at 60fps. Enough frames for nuanced motion.

**Exaggeration**: Full range available - match to brand personality and context.

**Solid Drawing**: Complex transforms work - 3D rotations, perspective shifts.

**Appeal**: Character-defining animations - this is where brand personality lives.

## Easing Recommendations

```css
/* Smooth, natural motion */
transition: all 400ms cubic-bezier(0.4, 0, 0.2, 1);

/* Expressive entrance */
transition: all 450ms cubic-bezier(0.16, 1, 0.3, 1);

/* Bouncy, playful */
transition: transform 400ms cubic-bezier(0.34, 1.56, 0.64, 1);

/* Dramatic deceleration */
transition: all 350ms cubic-bezier(0, 0.55, 0.45, 1);
```

## Best Use Cases

- Page/view transitions
- Complex modal sequences
- Animated illustrations
- Data visualization changes
- Onboarding animations
- Feature reveals
- State machine transitions
- Loading completion celebrations

## Implementation Pattern

```css
.page-enter {
  opacity: 0;
  transform: translateX(30px);
}

.page-enter-active {
  opacity: 1;
  transform: translateX(0);
  transition: opacity 350ms ease-out,
              transform 400ms cubic-bezier(0.16, 1, 0.3, 1);
}

/* Staggered children */
.list-item {
  transition: all 400ms cubic-bezier(0.4, 0, 0.2, 1);
}
.list-item:nth-child(1) { transition-delay: 0ms; }
.list-item:nth-child(2) { transition-delay: 50ms; }
.list-item:nth-child(3) { transition-delay: 100ms; }
```

## Key Insight

Medium duration is where animation becomes **storytelling**. Users watch, understand, and remember these animations. Invest in polish here - it defines perceived quality.
