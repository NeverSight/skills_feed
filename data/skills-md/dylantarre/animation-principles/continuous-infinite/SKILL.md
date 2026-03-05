---
name: continuous-infinite
description: Use when building ongoing loop animations - loading states, ambient motion, background effects that run indefinitely without user fatigue
---

# Continuous Animations (Infinite)

Infinite animations run **without end state**. They indicate ongoing processes, create ambient atmosphere, or provide persistent visual interest. The challenge: avoiding fatigue.

## Disney Principles for Continuous Motion

### Sustainable Application

**Squash & Stretch**: Subtle, rhythmic - 5-10% oscillation that doesn't demand attention. Breathing, not bouncing.

**Anticipation**: Built into loop - each cycle should flow naturally into the next without visible restart.

**Staging**: Background hierarchy - continuous motion must not compete with interactive elements.

**Straight Ahead/Pose to Pose**: Pose to pose for seamless loops - endpoint must match startpoint perfectly.

**Follow Through**: Wave propagation - elements should move in sequence, creating natural flow.

**Slow In/Slow Out**: Smooth, endless curves - no sharp accelerations that call attention.

**Arcs**: Circular, orbital paths - return to origin naturally. Figure-8s, ellipses, waves.

**Secondary Action**: Layered ambient motion - multiple elements at different speeds create depth.

**Timing**: Varied cycle lengths - elements should NOT sync up. Use prime number relationships (3s, 5s, 7s).

**Exaggeration**: Minimal - subtlety prevents fatigue. Users should barely notice the motion.

**Solid Drawing**: Simple transforms preferred - complex animations drain battery and attention.

**Appeal**: Calm, not chaotic - continuous motion should soothe, not stimulate.

## Loop Duration Guidelines

- **Loading spinners**: 800-1200ms cycles
- **Breathing/pulsing**: 2000-4000ms cycles
- **Ambient background**: 5000-15000ms cycles
- **Subtle floating**: 3000-8000ms cycles

## Easing Recommendations

```css
/* Seamless breathing */
animation-timing-function: ease-in-out;

/* Perpetual smooth motion */
animation-timing-function: cubic-bezier(0.37, 0, 0.63, 1);

/* Organic, natural feeling */
animation-timing-function: cubic-bezier(0.45, 0.05, 0.55, 0.95);
```

## Best Use Cases

- Loading/progress indicators
- Ambient background effects
- Music visualizers
- Screensaver-style displays
- Status indicators (pulsing online dot)
- Attention-getters (gentle notification pulse)
- Decorative motion (floating particles)

## Implementation Pattern

```css
/* Seamless spin */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.spinner {
  animation: spin 1000ms linear infinite;
}

/* Breathing pulse */
@keyframes breathe {
  0%, 100% { transform: scale(1); opacity: 0.7; }
  50% { transform: scale(1.05); opacity: 1; }
}
.pulse {
  animation: breathe 3000ms ease-in-out infinite;
}

/* Floating ambient - use multiple with prime-number durations */
@keyframes float {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  33% { transform: translateY(-10px) rotate(2deg); }
  66% { transform: translateY(5px) rotate(-1deg); }
}
.float-a { animation: float 5000ms ease-in-out infinite; }
.float-b { animation: float 7000ms ease-in-out infinite; }
.float-c { animation: float 11000ms ease-in-out infinite; }
```

## Anti-Patterns

- Synchronizing multiple continuous animations
- High-frequency motion (causes nausea)
- Large-scale movement in peripheral vision
- Competing with primary content
- Running during user input/focus

## Key Insight

Continuous animations must be **invisible by design**. If users consciously notice them after the first few seconds, they're too aggressive. The best infinite animations are felt as atmosphere, not seen as motion.
