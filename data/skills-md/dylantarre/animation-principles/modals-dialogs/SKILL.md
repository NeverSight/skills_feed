---
name: modals-dialogs
description: Use when animating modals, dialogs, popovers, or overlay content to create smooth entrances and exits
---

# Modal & Dialog Animation Principles

Apply Disney's 12 principles to modals for seamless, non-jarring transitions.

## Principles Applied to Modals

### 1. Squash & Stretch
Modal can scale from 0.9 to 1.0 on enter, creating a subtle expansion feel. Exit reverses. Keep it subtle to maintain professionalism.

### 2. Anticipation
Trigger element (button) should react before modal appears. Brief scale-down of trigger, then modal emerges from that point.

### 3. Staging
Backdrop dims (0.5-0.7 opacity) to focus attention on modal. Background content can blur slightly (4-8px). Modal is the star.

### 4. Straight Ahead & Pose to Pose
Define states: hidden, entering, visible, exiting. Clear keyframes for each. Pose-to-pose ensures predictable, controllable animation.

### 5. Follow Through & Overlapping Action
Modal container arrives first, content fades in 50-100ms after. Close button can have slight bounce at end. Stagger form fields.

### 6. Ease In & Ease Out
Enter: `ease-out` (decelerates in). Exit: `ease-in` (accelerates out). `cubic-bezier(0.16, 1, 0.3, 1)` for smooth, bouncy enter.

### 7. Arcs
If modal originates from a button, arc toward center rather than straight line. Creates more organic movement path.

### 8. Secondary Action
While modal scales in (primary), backdrop fades (secondary), content staggers (tertiary). Each supports without competing.

### 9. Timing
- Backdrop fade: 200-250ms
- Modal enter: 250-350ms
- Modal exit: 200ms (faster out)
- Content stagger: 30-50ms per item
- Shake on error: 300ms

### 10. Exaggeration
Dramatic entrance for important alerts. Slight overshoot scale (1.02) before settling at 1.0. Error modals can shake briefly.

### 11. Solid Drawing
Modal shadows should match interface light source. Maintain consistent border-radius. Content should never overflow during animation.

### 12. Appeal
Smooth entrances feel polished. Origin-point animation feels connected. Abrupt modals feel jarring. Invest in modal transitions.

## CSS Implementation

```css
.modal-backdrop {
  transition: opacity 250ms ease-out;
}

.modal {
  animation: modalEnter 300ms cubic-bezier(0.16, 1, 0.3, 1);
}

@keyframes modalEnter {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
  }
}
```

## Key Properties
- `transform`: scale, translate (origin point)
- `opacity`: fade in/out
- `backdrop-filter`: blur background
- `animation`: keyframe sequences
- `transform-origin`: source point
