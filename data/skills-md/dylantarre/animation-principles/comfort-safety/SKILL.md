---
name: comfort-safety
description: Use when creating animations that reassure users, reduce anxiety, or communicate protection and security.
---

# Comfort & Safety Animation

Create animations that reassure, protect, and make users feel secure.

## Emotional Goal

Comfort comes from predictable, gentle motion that never startles. Safety means animations that communicate protection, stability, and user control.

## Disney Principles for Comfort

### Squash & Stretch
Minimal, soft (5-10%). Gentle give without instability. Like a cushion—absorbs impact, maintains structure.

### Anticipation
Clear, reassuring preparation (150-200ms). Users always know what's coming. No surprises, no hidden actions.

### Staging
Enclosed, protected compositions. Clear boundaries. Safe spaces. Visual hierarchy that guides without overwhelming.

### Straight Ahead Action
Avoid. Safety requires predictability. Every movement should be controlled and expected.

### Follow Through & Overlapping Action
Gentle, cushioned settling. Soft landings. Elements ease into place like being tucked in.

### Slow In & Slow Out
Smooth, gentle curves throughout. No sudden changes. `ease-in-out` for predictable, comfortable motion.

### Arc
Soft, natural curves. Cradling, embracing paths. Motion that wraps around rather than cuts through.

### Secondary Action
Reassuring cues only. Checkmarks, shields, locks. Visual confirmation of safety and completion.

### Timing
Moderate, unhurried (300-450ms). Time to process and feel safe. Never rushed or abrupt.

### Exaggeration
None to minimal. Realistic, grounded movements. Comfort requires believability.

### Solid Drawing
Stable, balanced forms. Low center of gravity. Shapes that feel grounded and secure.

### Appeal
Warm, muted colors. Soft edges. Familiar, comfortable aesthetics. Nothing aggressive or sharp.

## Timing Recommendations

| Element | Duration | Easing |
|---------|----------|--------|
| Transitions | 300-400ms | `ease-in-out` |
| Feedback | 200-250ms | `ease-out` |
| Confirmation | 350-450ms | `ease-out` |
| Protection reveal | 400-500ms | `ease-in-out` |

## CSS Easing

```css
--comfort-smooth: cubic-bezier(0.4, 0, 0.2, 1);
--comfort-gentle: cubic-bezier(0.45, 0, 0.55, 1);
--comfort-settle: cubic-bezier(0.25, 0.1, 0.25, 1);
```

## Reassuring Patterns

```css
@keyframes comfort-embrace {
  from {
    opacity: 0;
    transform: scale(0.98);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@keyframes comfort-check {
  0% {
    stroke-dashoffset: 24;
    opacity: 0;
  }
  50% { opacity: 1; }
  100% {
    stroke-dashoffset: 0;
    opacity: 1;
  }
}

.safe-element {
  animation: comfort-embrace 400ms ease-in-out forwards;
}
```

## Safety Signals

- Clear, visible feedback for all actions
- Undo animations that show reversibility
- Progress that never goes backward unexpectedly
- Transitions that maintain orientation
- Consistent patterns users can rely on

## When to Use

- Banking and finance
- Healthcare applications
- Password and security flows
- Data privacy controls
- Insurance platforms
- Backup and recovery
- Parental controls
- Sensitive data handling
