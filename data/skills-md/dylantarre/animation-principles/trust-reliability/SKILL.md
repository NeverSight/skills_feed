---
name: trust-reliability
description: Use when creating animations that build user confidence, establish credibility, and communicate dependability.
---

# Trust & Reliability Animation

Create animations that establish confidence, consistency, and dependable user experiences.

## Emotional Goal

Trust develops through predictable, controlled movements that respect user expectations. Reliability means animations behave consistently and never surprise negatively.

## Disney Principles for Trust

### Squash & Stretch
Minimal stretch (5-10% maximum). Controlled deformation shows stability. Elements should feel solid and grounded, not rubbery.

### Anticipation
Subtle but present (50-100ms). Brief preparation signals what's coming without surprises. Users should always know what to expect next.

### Staging
Clear, unambiguous presentation. One action at a time. Important elements are obvious. No hidden or confusing movements.

### Straight Ahead Action
Avoid for trust-building. Prefer pose-to-pose for predictable, controlled results. Every frame should be intentional.

### Follow Through & Overlapping Action
Restrained follow-through. Elements settle quickly without excessive bouncing. Professional, controlled completion of movements.

### Slow In & Slow Out
Smooth, symmetrical easing. `ease-in-out` creates predictable, professional motion. No sudden accelerations or jarring stops.

### Arc
Gentle, predictable curves. Consistent arc patterns across similar interactions. Avoid erratic or unexpected paths.

### Secondary Action
Minimal and purposeful. Supporting animations should reinforce, not distract. Loading indicators should be calm and steady.

### Timing
Moderate, consistent timing (250-400ms). Never too fast (feels rushed) or too slow (feels broken). Same elements should always animate at same speed.

### Exaggeration
Very minimal (5-10%). Near-realistic movements feel professional and trustworthy. Subtle refinement over dramatic effect.

### Solid Drawing
Maintain perfect proportions. No warping or distortion. Elements should feel stable and well-constructed.

### Appeal
Clean, balanced designs. Symmetry suggests stability. Professional aesthetics over playful charm.

## Timing Recommendations

| Element | Duration | Easing |
|---------|----------|--------|
| Transitions | 250-350ms | `ease-in-out` |
| Feedback | 150-200ms | `ease-out` |
| Loading | Continuous | `linear` |
| Modals | 200-300ms | `ease-out` |

## CSS Easing

```css
--trust-smooth: cubic-bezier(0.4, 0, 0.2, 1);
--trust-enter: cubic-bezier(0, 0, 0.2, 1);
--trust-exit: cubic-bezier(0.4, 0, 1, 1);
```

## Consistency Rules

1. Same action = same animation, always
2. Duration variance: maximum ±50ms
3. No random or variable timing
4. Respect system motion preferences
5. Graceful degradation when disabled

## When to Use

- Financial transactions and payments
- Form submissions and data entry
- Authentication flows
- Settings and configuration
- Progress indicators
- Confirmation dialogs
- Enterprise applications
