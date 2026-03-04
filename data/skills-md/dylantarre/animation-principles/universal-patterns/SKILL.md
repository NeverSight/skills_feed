---
name: universal-patterns
description: Use when creating any animation type - provides foundational timing, easing, and principle application that applies to all motion in interfaces.
---

# Universal Animation Patterns

Apply Disney's 12 principles as baseline defaults for any animation.

## Core Timing Scale

| Category | Duration | Use For |
|----------|----------|---------|
| Instant | 100-150ms | Hovers, toggles, micro-states |
| Fast | 150-250ms | Feedback, small transitions |
| Standard | 250-400ms | Modals, reveals, state changes |
| Slow | 400-600ms | Page transitions, sequences |
| Deliberate | 600-1000ms | Dramatic reveals, celebrations |

## Universal Easing Library

```css
:root {
  /* Standard easings */
  --ease-out: cubic-bezier(0, 0, 0.2, 1);        /* Entrances */
  --ease-in: cubic-bezier(0.4, 0, 1, 1);         /* Exits */
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);   /* State changes */

  /* Spring easings */
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);  /* Overshoot */
  --ease-bounce: cubic-bezier(0.68, -0.55, 0.27, 1.55); /* Playful */
}
```

## The 12 Principles Quick Reference

1. **Squash & Stretch**: Scale 0.95-1.05 range for organic feel
2. **Anticipation**: 2-3px reverse movement or 50ms pause before action
3. **Staging**: Animate toward user attention, clear visual hierarchy
4. **Straight Ahead vs Pose-to-Pose**: Define keyframes, plan states
5. **Follow Through**: Overshoot by 2-5%, settle back
6. **Slow In/Slow Out**: Always ease, never linear (except spinners)
7. **Arcs**: Combine X+Y movement, natural paths
8. **Secondary Action**: Layer 2-3 properties max (opacity + transform + shadow)
9. **Timing**: Match duration to distance/importance
10. **Exaggeration**: Subtle for UI (under 10% deviation)
11. **Solid Drawing**: Maintain visual consistency during motion
12. **Appeal**: Motion should feel helpful, not performative

## Base Animation Classes

```css
/* Standard entrance */
.animate-in {
  animation: fade-in 250ms var(--ease-out) forwards;
}

/* Standard exit */
.animate-out {
  animation: fade-out 200ms var(--ease-in) forwards;
}

/* State transition */
.animate-state {
  transition: all 200ms var(--ease-in-out);
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fade-out {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(-10px); }
}
```

## Universal Rules

1. **100ms Response Time**: User actions must trigger visible change within 100ms
2. **Under 400ms for UI**: Functional animations shouldn't exceed 400ms
3. **Reduce Motion**: Always provide `prefers-reduced-motion` alternative
4. **GPU Properties**: Use only `transform` and `opacity` for smooth 60fps
5. **Exit < Enter**: Exits 20-30% faster than entrances

## Accessibility Default

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Decision Tree

1. Is element entering? → Use ease-out, 200-300ms
2. Is element exiting? → Use ease-in, 150-250ms
3. Is element changing state? → Use ease-in-out, 150-250ms
4. Is it continuous? → Use linear (rotation) or ease-in-out (pulse)
5. Is it responding to gesture? → Use ease-out with overshoot, under 200ms

When uncertain, start with: `250ms cubic-bezier(0.4, 0, 0.2, 1)`
