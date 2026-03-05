---
name: responsive-adaptive
description: Use when building context-dependent animations - duration that changes based on device, distance, user preference, or interaction context
---

# Responsive & Adaptive Timing

Responsive timing adapts duration to **context**: device capability, travel distance, user preferences, and interaction type. One duration doesn't fit all situations.

## Disney Principles for Adaptive Motion

### Context-Aware Application

**Squash & Stretch**: Scale with device - more subtle on mobile (less screen real estate for deformation).

**Anticipation**: Shorter on touch devices - touch users expect faster response than mouse users.

**Staging**: Adapt to viewport - smaller screens need more focused staging, less simultaneous motion.

**Straight Ahead/Pose to Pose**: Same approach, scaled duration - poses stay, timing adjusts.

**Follow Through**: Proportional to distance - longer travel = more follow-through time.

**Slow In/Slow Out**: Adjust curve intensity - faster animations need sharper easing.

**Arcs**: Same paths, different speeds - arc shape remains, traversal time changes.

**Secondary Action**: Reduce on mobile - fewer simultaneous animations for performance.

**Timing**: THE adaptive variable - timing changes, principles stay.

**Exaggeration**: Less on smaller screens - proportional to viewport/element size.

**Solid Drawing**: Performance-aware - reduce 3D transforms on weaker devices.

**Appeal**: Context-appropriate - what feels right on desktop may feel slow on mobile.

## Adaptive Strategies

### Distance-Based Duration

```css
/* Base duration for reference distance */
--base-duration: 300ms;
--base-distance: 100px;

/* Duration scales with distance */
/* 50px travel = 200ms, 200px travel = 450ms */
```

```javascript
function getDuration(distance) {
  const baseDuration = 300;
  const baseDistance = 100;
  return Math.min(600, baseDuration * Math.sqrt(distance / baseDistance));
}
```

### Device-Based Duration

```css
/* Desktop - full duration */
.transition { transition-duration: 400ms; }

/* Tablet - slightly faster */
@media (max-width: 1024px) {
  .transition { transition-duration: 350ms; }
}

/* Mobile - faster for perceived responsiveness */
@media (max-width: 768px) {
  .transition { transition-duration: 250ms; }
}
```

### Preference-Based Duration

```css
/* Respect reduced motion preference */
@media (prefers-reduced-motion: reduce) {
  .transition {
    transition-duration: 0.01ms !important;
    animation-duration: 0.01ms !important;
  }
}

/* Reduce motion, don't eliminate */
@media (prefers-reduced-motion: reduce) {
  .transition {
    transition-duration: 100ms;
    transform: none; /* Only opacity fades */
  }
}
```

## Context Rules

| Context | Duration Adjustment |
|---------|---------------------|
| Touch device | -25% from desktop |
| Small viewport | -20% from desktop |
| Large travel distance | +50% base |
| Small travel distance | -30% base |
| User prefers reduced | Instant or minimal |
| Low power mode | -50% or disabled |
| High-frequency action | Use minimum duration |
| First-time view | Full duration |
| Repeat interaction | Reduced duration |

## Implementation Pattern

```css
:root {
  --duration-instant: 50ms;
  --duration-fast: 150ms;
  --duration-normal: 300ms;
  --duration-slow: 500ms;
}

@media (max-width: 768px) {
  :root {
    --duration-fast: 100ms;
    --duration-normal: 200ms;
    --duration-slow: 350ms;
  }
}

@media (prefers-reduced-motion: reduce) {
  :root {
    --duration-instant: 0ms;
    --duration-fast: 0ms;
    --duration-normal: 100ms;
    --duration-slow: 150ms;
  }
}
```

## Key Insight

Great animation adapts like typography adapts - what works at one size/context may not work at another. Build **systems**, not fixed values. Test across contexts. Duration is a variable, not a constant.
