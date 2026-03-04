---
name: continuous-loops
description: Use when creating ongoing animations - loading spinners, pulsing indicators, ambient motion, background effects, or any animation that repeats indefinitely.
---

# Continuous Loop Animations

Apply Disney's 12 principles to animations that never stop.

## Principle Application

**Squash & Stretch**: Subtle scale oscillation (0.98-1.02) creates organic breathing. Avoid rigid mechanical loops.

**Anticipation**: Build anticipation into the loop cycle. Brief pause at extremes before reversing.

**Staging**: Loops should support, not dominate. Keep amplitude subtle for background elements.

**Straight Ahead vs Pose-to-Pose**: Design keyframe poses that loop seamlessly. End frame must flow into start frame.

**Follow Through & Overlapping**: Multi-part loops have elements at different phases. Three dots pulse with 120° phase offset.

**Slow In/Slow Out**: Use ease-in-out for smooth oscillations. Linear motion looks mechanical.

**Arcs**: Circular motion follows true arcs. Spinners rotate, pendulums swing, orbits circle.

**Secondary Action**: Primary rotation + secondary wobble. Spinner spins while slightly bouncing.

**Timing**:
- Fast loops: 500-800ms (spinners, urgent indicators)
- Medium loops: 1000-2000ms (pulsing, breathing)
- Slow loops: 2000-4000ms (ambient, background)

**Exaggeration**: Minimal for loops - they're already attention-grabbing through repetition.

**Solid Drawing**: Loops must be seamless. Any jump between end and start destroys the illusion.

**Appeal**: Loops should be hypnotic, not annoying. Test at 30 seconds - still pleasant?

## Timing Recommendations

| Loop Type | Duration | Easing | Iterations |
|-----------|----------|--------|------------|
| Spinner | 600-800ms | linear (rotation) | infinite |
| Pulse | 1500-2000ms | ease-in-out | infinite |
| Skeleton Shimmer | 1500ms | ease-in-out | infinite |
| Typing Dots | 1400ms | ease-in-out | infinite |
| Breathing | 3000-4000ms | ease-in-out | infinite |
| Floating | 3000-5000ms | ease-in-out | infinite |

## Implementation Patterns

```css
/* Smooth spinner */
.spinner {
  animation: spin 700ms linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Organic pulse */
.pulse {
  animation: pulse 2000ms ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.05); opacity: 0.8; }
}

/* Staggered dots */
.dot {
  animation: bounce 1400ms ease-in-out infinite;
}
.dot:nth-child(2) { animation-delay: 160ms; }
.dot:nth-child(3) { animation-delay: 320ms; }
```

## Performance Rules

1. Use `transform` and `opacity` only - no layout properties
2. Add `will-change: transform` for loops over 1 second
3. Pause off-screen loops with Intersection Observer
4. Respect `prefers-reduced-motion` - reduce or stop loops

## Seamless Loop Formula

For breathing/pulsing: `0%, 100%` keyframes must be identical. Use `alternate` direction for simpler ping-pong effects.
