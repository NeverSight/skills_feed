---
name: state-changes
description: Use when elements transform in place - toggle switches, expanding accordions, checkbox animations, button states, or any transformation without entering/exiting.
---

# State Change Animations

Apply Disney's 12 principles when elements transform without leaving.

## Principle Application

**Squash & Stretch**: Elements compress before expanding. A toggle switch squashes 5% before sliding.

**Anticipation**: Wind up before the change. Slight reverse movement (2-3px) before expanding.

**Staging**: Keep transformations centered on user focus. Don't let state changes distract from the interaction point.

**Straight Ahead vs Pose-to-Pose**: Define exact states. Button has rest, hover, active, disabled - each precisely designed.

**Follow Through & Overlapping**: Parts transform at different rates. Icon rotates before label fades in.

**Slow In/Slow Out**: Use ease-in-out for bidirectional changes: `cubic-bezier(0.4, 0, 0.2, 1)`.

**Arcs**: Rotating elements follow natural arcs. Chevrons rotate on their center point, not linearly.

**Secondary Action**: Pair the primary change with supporting motion. Toggle sliding + color shift + icon swap.

**Timing**:
- Micro-states: 100-150ms (checkbox tick, radio fill)
- Standard states: 150-250ms (toggles, accordions)
- Complex states: 250-400ms (multi-part transformations)

**Exaggeration**: Overshoot slightly on state changes. Toggle goes 2px past, then settles.

**Solid Drawing**: Maintain element integrity during transformation. No distortion that breaks visual consistency.

**Appeal**: State changes should feel satisfying. Users clicked with intent - reward that intent.

## Timing Recommendations

| State Change | Duration | Easing | Notes |
|-------------|----------|--------|-------|
| Checkbox | 150ms | ease-out | Tick draws in |
| Toggle Switch | 200ms | ease-in-out | Overshoot slightly |
| Radio Button | 150ms | ease-out | Scale in from center |
| Accordion | 250ms | ease-in-out | Height + rotation |
| Tab Switch | 200ms | ease-in-out | Indicator slides |
| Button Active | 100ms | ease-out | Scale to 0.97 |
| Card Expand | 300ms | ease-in-out | All properties together |

## Implementation Pattern

```css
.toggle {
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

.toggle-knob {
  transition: transform 200ms cubic-bezier(0.34, 1.56, 0.64, 1); /* Overshoot */
}

.toggle.active .toggle-knob {
  transform: translateX(20px);
}
```

## Accordion Pattern

```css
.accordion-content {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows 250ms ease-in-out;
}

.accordion.open .accordion-content {
  grid-template-rows: 1fr;
}
```

## Key Rule

State changes are reversible. The animation to state B should be the inverse of animation to state A. Test both directions.
