---
name: motion-sickness
description: Use when animation causes dizziness, nausea, disorientation, or vestibular discomfort
---

# Motion Sickness Prevention

Eliminate vestibular triggers using Disney's principles safely.

## Problem Indicators
- Users report dizziness or nausea
- Disorientation during navigation
- Users avoid certain features
- Complaints increase with larger screens
- Parallax or zoom effects cause issues

## Dangerous Patterns

These trigger vestibular responses:
- Large-scale zoom animations
- Parallax scrolling (especially multi-layer)
- Full-screen rotations
- Rapid direction changes
- Continuous/looping background motion
- Scroll-jacking

## Diagnosis by Principle

### Exaggeration
**Issue**: Over-dramatic motion
**Fix**: Reduce scale of transforms. Max 10-20% size change. Avoid full-screen zooms.

### Arcs
**Issue**: Curved paths cause tracking strain
**Fix**: Use linear motion for functional UI. Save arcs for small, optional elements only.

### Follow Through
**Issue**: Overshooting creates whiplash effect
**Fix**: Remove bounce/overshoot from navigation. Use critically damped springs or ease-out.

### Secondary Action
**Issue**: Multiple moving elements cause confusion
**Fix**: Limit to one primary motion. Remove parallax layers.

### Slow In and Slow Out
**Issue**: Acceleration patterns cause disorientation
**Fix**: Use consistent, predictable easing. Avoid sudden speed changes.

## Quick Fixes

1. **Respect `prefers-reduced-motion`** - Non-negotiable
2. **Remove parallax effects** - Common trigger
3. **Avoid zoom transitions** - Use fades instead
4. **Keep motion small** - Under 100px movement
5. **No scroll-jacking** - Let scroll be scroll

## Troubleshooting Checklist

- [ ] Does animation respect `prefers-reduced-motion`?
- [ ] Is any element moving more than 100px?
- [ ] Are there any zoom effects?
- [ ] Is parallax present? Remove it.
- [ ] Are there continuous/looping animations?
- [ ] Can users pause or disable motion?
- [ ] Test on large display (motion amplified)
- [ ] Test for 5+ minutes continuously

## Safe Alternatives

| Triggering | Safe Alternative |
|------------|------------------|
| Zoom transition | Fade + slight scale (max 5%) |
| Parallax scroll | Static or single-layer |
| Rotation | Fade or slide |
| Bounce/spring | Ease-out (no overshoot) |
| Full-page slide | Crossfade |

## Code Pattern

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }

  .parallax {
    transform: none !important;
  }
}

/* Safe default motion */
.safe-transition {
  transition: opacity 200ms ease-out;
  /* Avoid: transform with large values */
}
```
