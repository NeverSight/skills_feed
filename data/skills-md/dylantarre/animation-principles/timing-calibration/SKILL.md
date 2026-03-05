---
name: timing-calibration
description: Use when animation speed feels wrong—too fast, too slow, or inconsistent
---

# Timing Calibration

Get animation speed right using Disney's timing principles.

## Problem Indicators
- "Too slow" or "too fast" feedback
- Animations feel inconsistent
- Similar actions have different speeds
- Users wait for animations
- Motion feels robotic or unnatural

## Diagnosis by Principle

### Timing
**Issue**: Duration doesn't match action type
**Fix**: Micro-interactions: 100-150ms. Transitions: 200-400ms. Complex reveals: 400-600ms. Never exceed 1s for UI.

### Slow In and Slow Out
**Issue**: Linear timing feels mechanical
**Fix**: Use easing. Ease-out for entrances (fast start, soft landing). Ease-in for exits (soft start, quick finish).

### Arcs
**Issue**: Straight-line motion at wrong speed
**Fix**: Curved paths need more time than straight paths. Increase duration for arc motion.

### Staging
**Issue**: Multiple speeds compete
**Fix**: Similar elements should animate at similar speeds. Create timing harmony.

### Secondary Action
**Issue**: Secondary animations at wrong relative speed
**Fix**: Secondary actions should be slightly slower than primary. Creates natural hierarchy.

## Timing Scale

| Category | Duration | Use For |
|----------|----------|---------|
| Instant | 0-100ms | Hover states, micro-feedback |
| Fast | 100-200ms | Buttons, toggles, small elements |
| Normal | 200-300ms | Cards, modals, most transitions |
| Slow | 300-400ms | Page transitions, large elements |
| Deliberate | 400-600ms | Complex reveals, onboarding |

## Quick Fixes

1. **Start with 200ms** - Adjust from there
2. **Larger elements = longer duration** - Size affects perceived speed
3. **Distance affects timing** - Longer travel = longer duration
4. **Create a timing scale** - Use 3-4 consistent values
5. **Test at 2x speed** - If too slow works, use it

## Troubleshooting Checklist

- [ ] Is duration under 400ms for most UI?
- [ ] Do similar elements have similar timing?
- [ ] Is easing applied (not linear)?
- [ ] Does larger movement have longer duration?
- [ ] Test: Speed up by 30%—still readable?
- [ ] Test: Slow down by 30%—feels sluggish?
- [ ] Are users waiting for animations?
- [ ] Compare to platform conventions (iOS/Android/Web)

## Code Pattern

```css
:root {
  /* Timing scale */
  --duration-instant: 50ms;
  --duration-fast: 150ms;
  --duration-normal: 250ms;
  --duration-slow: 350ms;
  --duration-deliberate: 500ms;

  /* Easing */
  --ease-out: cubic-bezier(0, 0, 0.2, 1);
  --ease-in: cubic-bezier(0.4, 0, 1, 1);
  --ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
}

/* Size-aware timing */
.small-element { transition-duration: var(--duration-fast); }
.medium-element { transition-duration: var(--duration-normal); }
.large-element { transition-duration: var(--duration-slow); }
```
