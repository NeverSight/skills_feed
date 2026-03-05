---
name: notifications-toasts
description: Use when animating notifications, toasts, alerts, snackbars, or system messages to grab attention appropriately
---

# Notification & Toast Animation Principles

Apply Disney's 12 principles to notifications for attention-grabbing yet non-disruptive alerts.

## Principles Applied to Notifications

### 1. Squash & Stretch
Toast can compress slightly on entrance impact, then stretch back. Creates a "landing" feel as if it arrived from off-screen.

### 2. Anticipation
Before auto-dismiss, toast can contract slightly (95% scale) for 100ms. Signals imminent departure to user.

### 3. Staging
Notifications should appear in consistent locations. Use color and icons to stage importance: info, success, warning, error.

### 4. Straight Ahead & Pose to Pose
Define states: entering, visible, exiting, stacked. Clear keyframes for entrance, attention (if needed), and exit.

### 5. Follow Through & Overlapping Action
Icon animates after container arrives (checkmark draws, bell wobbles). Progress bar for auto-dismiss follows toast entrance.

### 6. Ease In & Ease Out
Enter: `ease-out` (fast in, slow settle). Exit: `ease-in` (slow start, fast out). `cubic-bezier(0.68, -0.55, 0.27, 1.55)` for bounce.

### 7. Arcs
Toasts sliding from corners can follow slight arc. Bell icons should swing in arc, not rotate rigidly.

### 8. Secondary Action
While toast slides in (primary), shadow appears (secondary), icon animates (tertiary), progress bar starts (quaternary).

### 9. Timing
- Toast enter: 200-300ms
- Toast exit: 150-250ms
- Auto-dismiss delay: 3000-5000ms
- Attention pulse: 1000ms loop
- Success checkmark draw: 300ms
- Stack reorder: 200ms

### 10. Exaggeration
Error notifications can shake or pulse red. Critical alerts can be larger, bolder animations. Match urgency to importance.

### 11. Solid Drawing
Maintain consistent toast sizing. Icons should be crisp. Progress bars should be smooth (use transforms, not width).

### 12. Appeal
Smooth notifications feel polished. Jarring popups annoy users. A well-animated toast conveys professionalism.

## CSS Implementation

```css
.toast {
  animation: toastEnter 300ms cubic-bezier(0.68, -0.55, 0.27, 1.55);
}

.toast.exiting {
  animation: toastExit 200ms ease-in forwards;
}

@keyframes toastEnter {
  from {
    opacity: 0;
    transform: translateY(-100%) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes toastExit {
  to {
    opacity: 0;
    transform: translateX(100%);
  }
}

.toast-progress {
  transform-origin: left;
  animation: progress 4000ms linear forwards;
}
```

## Key Properties
- `transform`: translate, scale
- `opacity`: fade
- `animation`: entrance/exit sequences
- `transform-origin`: progress bars
- `box-shadow`: depth
