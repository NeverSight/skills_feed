---
name: elegance-sophistication
description: Use when creating animations that convey luxury, refinement, or premium brand experiences.
---

# Elegance & Sophistication Animation

Create animations that convey refinement, luxury, and understated excellence.

## Emotional Goal

Elegance emerges from restrained, perfectly timed motion. Sophistication means animations that are noticed for their quality, not their quantity—subtle excellence over obvious effort.

## Disney Principles for Elegance

### Squash & Stretch
Extremely minimal (0-5%). Refined objects don't deform—they glide. Preserve perfect proportions throughout motion.

### Anticipation
Subtle, refined preparation (100-150ms). A gentle weight shift, not a wind-up. Elegant motion begins smoothly.

### Staging
Negative space and restraint. Let elements breathe. Single focal point with generous margins. Less is more.

### Straight Ahead Action
Avoid. Elegance requires control and precision. Every frame should be intentional and refined.

### Follow Through & Overlapping Action
Graceful, extended settling. Like silk falling. Long, smooth deceleration without bounce or wobble.

### Slow In & Slow Out
Extended easing on both ends. Gradual, flowing motion. `cubic-bezier(0.4, 0, 0.2, 1)` for refined transitions.

### Arc
Sweeping, graceful curves. Like a conductor's baton or a dancer's arm. Beautiful paths, not just endpoints.

### Secondary Action
Minimal, purposeful accents. A subtle shadow shift, a gentle highlight. Supporting motion that elevates, not distracts.

### Timing
Unhurried but not slow (300-500ms). Time to appreciate the motion. Luxury doesn't rush.

### Exaggeration
Almost none (0-10%). Realistic, refined movements. Perfection in subtlety.

### Solid Drawing
Impeccable proportions maintained. No distortion. Geometric precision and balance.

### Appeal
Clean lines, perfect proportions. Monochromatic or limited palette. Timeless aesthetics.

## Timing Recommendations

| Element | Duration | Easing |
|---------|----------|--------|
| Fade | 300-400ms | `ease-in-out` |
| Slide | 400-500ms | `ease-out` |
| Scale | 350-450ms | `ease-in-out` |
| Reveal | 500-700ms | `ease-out` |

## CSS Easing

```css
--elegant-smooth: cubic-bezier(0.4, 0, 0.2, 1);
--elegant-enter: cubic-bezier(0.0, 0, 0.2, 1);
--elegant-flow: cubic-bezier(0.45, 0, 0.55, 1);
```

## Refined Transitions

```css
@keyframes elegant-reveal {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.elegant-element {
  animation: elegant-reveal 500ms cubic-bezier(0.4, 0, 0.2, 1) forwards;
}
```

## Design Principles

- White space is active, not empty
- Motion reveals content, doesn't decorate it
- Timing shows confidence and quality
- Every animation earns its place
- Restraint demonstrates mastery

## When to Use

- Luxury brand sites
- Fashion and jewelry
- High-end real estate
- Premium subscriptions
- Art galleries and museums
- Fine dining
- Boutique hotels
- Executive dashboards
