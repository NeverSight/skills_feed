---
name: micro-100-200ms
description: Use when building micro-interactions between 100-200ms - tooltips appearing, dropdown opens, small feedback animations that feel quick but perceptible
---

# Micro Animations (100-200ms)

The 100-200ms range is the **sweet spot for micro-interactions**. Fast enough to feel responsive, slow enough to be perceived as intentional motion.

## Disney Principles at Micro Speed

### Works Well

**Squash & Stretch**: Light application - 5-10% works for bouncy buttons, appearing elements.

**Anticipation**: Micro-anticipation possible - 20-30ms wind-up before 150ms action.

**Staging**: Single focal point - one element moving, rest static.

**Straight Ahead/Pose to Pose**: Either works - simple enough for straight ahead, controlled enough for poses.

**Follow Through**: Minimal overshoot - 2-5% past target, settle quickly.

**Slow In/Slow Out**: `ease-out` dominates - elements should arrive confidently.

**Arcs**: Slight curves possible - dropdown items can arc subtly rather than straight down.

**Secondary Action**: One secondary max - icon rotates while menu opens.

**Timing**: 6-12 frames at 60fps. Enough for smooth motion.

**Exaggeration**: Moderate - scale 0.9-1.1, rotation up to 30 degrees.

**Solid Drawing**: Simple transforms - scale, opacity, short translations.

**Appeal**: Quick animations feel modern and polished.

### Doesn't Work

- Long travel distances
- Complex choreography
- Heavy physics simulations
- Multi-stage reveals
- Elaborate anticipation sequences

## Easing Recommendations

```css
/* Standard micro-interaction */
transition: all 150ms ease-out;

/* Appearing elements - start fast, land soft */
transition: opacity 120ms ease-out, transform 150ms ease-out;

/* Bouncy micro-feedback */
transition: transform 180ms cubic-bezier(0.34, 1.56, 0.64, 1);
```

## Best Use Cases

- Tooltip appearance
- Dropdown menus opening
- Icon state changes
- Small hover animations
- Notification badges
- Tab switches
- Accordion headers

## Implementation Pattern

```css
.tooltip {
  opacity: 0;
  transform: translateY(-4px) scale(0.95);
  transition: opacity 120ms ease-out,
              transform 150ms ease-out;
}

.trigger:hover .tooltip {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.dropdown-item {
  opacity: 0;
  transform: translateY(-8px);
  transition: all 150ms ease-out;
}
```

## Key Insight

Micro-animations are **felt more than watched**. Users notice when they're missing but don't consciously observe them. This is where polish lives.
