---
name: excitement-energy
description: Use when creating animations that generate enthusiasm, build anticipation, or create high-energy experiences.
---

# Excitement & Energy Animation

Create animations that energize, excite, and create dynamic, high-impact experiences.

## Emotional Goal

Excitement builds through dynamic, escalating motion. Energy comes from fast, varied animations that create momentum and keep users engaged.

## Disney Principles for Excitement

### Squash & Stretch
Dynamic and impactful (20-35%). High-energy compression and extension. Objects feel springy and responsive.

### Anticipation
Quick, building tension (100-150ms). Like a coiled spring. The anticipation itself creates excitement.

### Staging
Dynamic compositions. Diagonal lines, asymmetric layouts. Nothing static—energy in every arrangement.

### Straight Ahead Action
Embrace for particle effects, explosions, and dynamic backgrounds. Energetic spontaneity.

### Follow Through & Overlapping Action
Bouncy, energetic overshoot. Elements don't just stop—they rebound with vitality.

### Slow In & Slow Out
Aggressive acceleration curves. Fast starts, snappy stops. `cubic-bezier(0.0, 0, 0.2, 1)` for punch.

### Arc
Dramatic, sweeping paths. High trajectories, dynamic curves. Motion that commands attention.

### Secondary Action
Abundant energy effects. Particles, trails, glows. The environment responds to exciting moments.

### Timing
Fast and punchy (100-300ms). Rapid sequences. Variety in timing creates rhythm and energy.

### Exaggeration
High (25-40%). Push movements to feel impactful. Energy requires going beyond subtle.

### Solid Drawing
Dynamic poses and forms. Lean into motion. Shapes that convey speed and force.

### Appeal
Bold, high-contrast design. Saturated colors. Dynamic angles. Visual energy.

## Timing Recommendations

| Element | Duration | Easing |
|---------|----------|--------|
| Quick hit | 100-150ms | `ease-out` |
| Bounce | 300-400ms | `spring` |
| Reveal | 200-300ms | `ease-out` |
| Sequence step | 50-100ms | `ease-out` |

## CSS Easing

```css
--energy-snap: cubic-bezier(0.0, 0, 0.2, 1);
--energy-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
--energy-punch: cubic-bezier(0.22, 1, 0.36, 1);
```

## High-Energy Patterns

```css
@keyframes energy-burst {
  0% {
    transform: scale(0.8);
    opacity: 0;
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes energy-shake {
  0%, 100% { transform: translateX(0); }
  10%, 30%, 50%, 70%, 90% { transform: translateX(-4px); }
  20%, 40%, 60%, 80% { transform: translateX(4px); }
}

@keyframes energy-pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.08); }
}
```

## Building Energy

1. Start with anticipation build
2. Quick, impactful main action
3. Energetic follow-through
4. Secondary effects cascade
5. Brief pause before next beat

## When to Use

- Sports and fitness apps
- Music and entertainment
- Gaming interfaces
- Event promotions
- Product launches
- Sales and promotions
- Streaming platforms
- Action-oriented apps
