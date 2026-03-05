---
name: power-confidence
description: Use when creating animations that convey strength, authority, or bold confidence in brand and product.
---

# Power & Confidence Animation

Create animations that convey strength, authority, and commanding presence.

## Emotional Goal

Power comes from deliberate, controlled, weighty motion. Confidence means animations that know exactly where they're going and arrive with certainty.

## Disney Principles for Power

### Squash & Stretch
Minimal stretch, impactful squash. Heavy objects don't stretch—they compress on impact (10-15%). Weight and solidity over flexibility.

### Anticipation
Deliberate, confident preparation (100-200ms). Not hesitation—gathering power. Like a predator before striking.

### Staging
Dominant positioning. Large scale, center stage. Powerful elements command attention through presence, not motion.

### Straight Ahead Action
Avoid. Power requires intention and control. Every movement should be deliberate, not spontaneous.

### Follow Through & Overlapping Action
Controlled deceleration. Heavy elements don't bounce—they settle with authority. Short, decisive follow-through.

### Slow In & Slow Out
Strong ease-out with sudden stops. Fast acceleration, decisive landing. `cubic-bezier(0.0, 0, 0.2, 1)` for powerful arrivals.

### Arc
Direct paths preferred. Power takes the straightest route. When arced, low and driving—like a charging bull.

### Secondary Action
Impactful ripples or shockwaves. When power lands, the environment responds. Subtle screen shake, radiating force.

### Timing
Medium-fast with decisive endpoints (150-300ms). Not rushed, not leisurely. Purposeful velocity.

### Exaggeration
Moderate (15-25%). Amplify impact, not movement. The landing matters more than the journey.

### Solid Drawing
Heavy, grounded forms. Strong geometric shapes. Stability and mass in every frame.

### Appeal
Bold, angular design. High contrast. Dark, saturated colors. Commanding presence.

## Timing Recommendations

| Element | Duration | Easing |
|---------|----------|--------|
| Entrance | 200-300ms | `ease-out` |
| Impact | 100-150ms | `ease-out` |
| Settle | 150-200ms | `ease-out` |
| Transition | 250-350ms | `ease-in-out` |

## CSS Easing

```css
--power-strike: cubic-bezier(0.0, 0, 0.2, 1);
--power-land: cubic-bezier(0.16, 1, 0.3, 1);
--power-drive: cubic-bezier(0.25, 0.1, 0.25, 1);
```

## Impact Animation

```css
@keyframes power-land {
  0% {
    transform: translateY(-20px) scale(1.05);
    opacity: 0;
  }
  60% {
    transform: translateY(2px) scale(0.98);
  }
  100% {
    transform: translateY(0) scale(1);
    opacity: 1;
  }
}
```

## Weight Simulation

- Larger elements animate slower
- Powerful elements affect surroundings
- Impacts create brief compression
- Recovery is quick and controlled

## When to Use

- Hero sections and headlines
- Premium product showcases
- Brand statements
- Achievement displays
- Dashboard key metrics
- Executive presentations
- Automotive and luxury brands
- Sports and fitness apps
