---
name: instant-0-100ms
description: Use when building instantaneous UI feedback under 100ms - button presses, toggles, state changes that feel immediate and responsive
---

# Instant Animations (0-100ms)

Animations under 100ms feel **instantaneous** to users. This duration is for immediate feedback that confirms actions without perceived delay.

## Disney Principles at Instant Speed

### Works Well

**Squash & Stretch**: Subtle - 2-5% compression on button press creates tactile feel without visible deformation.

**Anticipation**: Skip entirely - no time for preparation at this speed.

**Staging**: Minimal - rely on position/color change, not movement.

**Straight Ahead/Pose to Pose**: Straight ahead only - too fast for keyframe complexity.

**Follow Through**: None - motion completes before follow-through registers.

**Slow In/Slow Out**: Use `ease-out` only - starts at full speed, slight deceleration.

**Arcs**: Linear paths only - curves don't register at this speed.

**Secondary Action**: Skip - brain can't process multiple simultaneous instant changes.

**Timing**: 1-3 frames maximum. 60fps = 16.67ms per frame.

**Exaggeration**: Minimal - subtle scale (0.95-1.05) or opacity changes.

**Solid Drawing**: Focus on color/opacity shifts, not spatial transformation.

**Appeal**: Crisp, immediate response builds trust and perceived performance.

### Doesn't Work

- Complex multi-step sequences
- Visible travel distance
- Rotation beyond 15 degrees
- Multiple property changes
- Staged reveals

## Easing Recommendations

```css
/* Primary choice - immediate start, soft landing */
transition: all 50ms ease-out;

/* Alternative - completely linear for state toggles */
transition: opacity 80ms linear;

/* Button press feedback */
transition: transform 50ms ease-out;
```

## Best Use Cases

- Button active/pressed states
- Toggle switches
- Checkbox/radio selections
- Focus ring appearance
- Hover color shifts
- Touch ripple initiation

## Implementation Pattern

```css
.button:active {
  transform: scale(0.97);
  transition: transform 50ms ease-out;
}

.toggle-on {
  background: var(--active);
  transition: background 80ms ease-out;
}
```

## Key Insight

At instant speeds, animation serves **confirmation**, not **communication**. Users shouldn't consciously perceive the animation - they should feel the interface responding.
