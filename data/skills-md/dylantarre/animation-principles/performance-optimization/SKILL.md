---
name: performance-optimization
description: Use when animation runs slow, janky, or causes frame drops
---

# Performance Optimization

Diagnose and fix slow or janky animations using Disney's 12 principles.

## Problem Indicators
- Frame rate drops below 60fps
- Stuttering or choppy motion
- UI feels sluggish
- Battery drain on mobile
- Layout thrashing

## Diagnosis by Principle

### Straight Ahead vs Pose-to-Pose
**Issue**: Calculating every frame in real-time
**Fix**: Use pose-to-pose (keyframe) animation. Let the browser interpolate between states using CSS transitions or `will-change`.

### Timing
**Issue**: Too many simultaneous animations
**Fix**: Stagger animations. Offset start times by 50-100ms to reduce concurrent calculations.

### Secondary Action
**Issue**: Too many secondary effects
**Fix**: Remove non-essential secondary animations on low-power devices. Use `prefers-reduced-motion` query.

### Solid Drawing
**Issue**: Animating expensive properties (width, height, top, left)
**Fix**: Only animate `transform` and `opacity`. These are GPU-accelerated and skip layout/paint.

### Staging
**Issue**: Animating off-screen elements
**Fix**: Only animate what's visible. Use Intersection Observer to pause off-screen animations.

## Quick Fixes

1. **Replace JS animations with CSS** - Browser-optimized
2. **Use `transform` instead of position properties** - GPU layer
3. **Add `will-change` sparingly** - Hints to browser
4. **Reduce simultaneous animations** - Stagger or sequence
5. **Lower animation complexity on mobile** - Detect device capability

## Troubleshooting Checklist

- [ ] Check DevTools Performance tab for long frames
- [ ] Verify animations use transform/opacity only
- [ ] Count simultaneous animations (keep under 3-4)
- [ ] Test on lowest-spec target device
- [ ] Check for layout thrashing (forced reflows)
- [ ] Verify `will-change` isn't overused
- [ ] Test with CPU throttling enabled
- [ ] Check if animations pause when tab is hidden

## Code Pattern

```css
/* Fast */
.element {
  will-change: transform;
  transition: transform 200ms ease-out;
}
.element:hover {
  transform: translateY(-4px);
}

/* Slow - avoid */
.element:hover {
  top: -4px; /* Triggers layout */
}
```
