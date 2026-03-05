---
name: orchestrated-sequences
description: Use when building multi-part animation sequences - staggered reveals, choreographed UI, coordinated motion where multiple elements work together
---

# Orchestrated Sequences

Orchestrated sequences coordinate **multiple elements across time**. Like a conductor directing an orchestra, you control when each element enters, how it moves, and how elements relate.

## Disney Principles for Orchestration

### Ensemble Coordination

**Squash & Stretch**: Unified style - all elements should share consistent elasticity. Mix bouncy and stiff looks chaotic.

**Anticipation**: Staggered preparation - lead element anticipates first, others follow in sequence.

**Staging**: Clear hierarchy - primary action leads, secondary elements support but don't compete.

**Straight Ahead/Pose to Pose**: Pose to pose mandatory - choreography requires precise timing control.

**Follow Through**: Cascading settle - elements land in sequence with overlapping follow-through.

**Slow In/Slow Out**: Shared easing family - use variations of same curve for cohesion.

**Arcs**: Coordinated paths - elements should move in complementary directions, not randomly.

**Secondary Action**: Intentional support - every element has a role in the composition.

**Timing**: The heart of orchestration - stagger delays, duration variations, tempo changes.

**Exaggeration**: Proportional emphasis - primary elements more exaggerated, supporting less.

**Solid Drawing**: Consistent dimensional logic - shared perspective, depth, scale relationships.

**Appeal**: Unified performance - the sequence should feel like one composed moment.

## Timing Strategies

```css
/* Linear stagger - equal delays */
.item:nth-child(n) {
  transition-delay: calc(var(--index) * 50ms);
}

/* Accelerating stagger - getting faster */
.item:nth-child(1) { transition-delay: 0ms; }
.item:nth-child(2) { transition-delay: 80ms; }
.item:nth-child(3) { transition-delay: 140ms; }
.item:nth-child(4) { transition-delay: 180ms; }

/* Decelerating stagger - slowing down */
.item:nth-child(1) { transition-delay: 0ms; }
.item:nth-child(2) { transition-delay: 40ms; }
.item:nth-child(3) { transition-delay: 100ms; }
.item:nth-child(4) { transition-delay: 180ms; }
```

## Easing Recommendations

```css
/* Cohesive family - same curve, different durations */
.primary { transition: all 400ms cubic-bezier(0.16, 1, 0.3, 1); }
.secondary { transition: all 350ms cubic-bezier(0.16, 1, 0.3, 1); }
.tertiary { transition: all 300ms cubic-bezier(0.16, 1, 0.3, 1); }

/* Sequence curve - smooth start, confident end */
animation-timing-function: cubic-bezier(0.22, 1, 0.36, 1);
```

## Best Use Cases

- Page load sequences
- Dashboard reveals
- Card grid animations
- Navigation menu opens
- Feature section reveals
- Data visualization builds
- Onboarding step sequences
- List population animations

## Implementation Pattern

```css
/* Staggered reveal system */
.orchestrated-item {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 300ms ease-out,
              transform 400ms cubic-bezier(0.16, 1, 0.3, 1);
}

.orchestrated-item.visible {
  opacity: 1;
  transform: translateY(0);
}

/* Apply delays via CSS custom properties or nth-child */
.orchestrated-item:nth-child(1) { transition-delay: 0ms; }
.orchestrated-item:nth-child(2) { transition-delay: 75ms; }
.orchestrated-item:nth-child(3) { transition-delay: 150ms; }
.orchestrated-item:nth-child(4) { transition-delay: 225ms; }
```

```javascript
// JS orchestration for complex sequences
const sequence = [
  { el: '.hero', delay: 0, duration: 500 },
  { el: '.title', delay: 100, duration: 400 },
  { el: '.subtitle', delay: 200, duration: 350 },
  { el: '.cta', delay: 350, duration: 400 },
];
```

## Key Insight

Orchestration is **composition in time**. Just as visual design arranges elements in space, animation orchestration arranges motion in time. The goal is a single, coherent performance, not a collection of individual animations.
