---
name: buttons-ctas
description: Use when animating buttons, CTAs, or clickable action elements to create satisfying, responsive interactions
---

# Button & CTA Animation Principles

Apply Disney's 12 principles to create buttons that feel alive and responsive.

## Principles Applied to Buttons

### 1. Squash & Stretch
Scale buttons slightly on press: `transform: scale(0.95)` on `:active`, return to `scale(1)` on release. Creates tactile feedback.

### 2. Anticipation
Subtle hover lift before click: `transform: translateY(-2px)` prepares users for the action.

### 3. Staging
Primary CTAs should be visually prominent. Use size, color contrast, and whitespace. Animate primary buttons more boldly than secondary.

### 4. Straight Ahead & Pose to Pose
Use pose-to-pose for button states: define clear keyframes for default, hover, active, and disabled states.

### 5. Follow Through & Overlapping Action
After click, let shadows or glows settle slightly after the button returns. Icon inside can lag 20-50ms behind button movement.

### 6. Ease In & Ease Out
Never use linear timing. Use `ease-out` for hover-in (fast start), `ease-in` for hover-out (gentle exit). `cubic-bezier(0.4, 0, 0.2, 1)` works well.

### 7. Arcs
Floating action buttons should move in arcs when repositioning. Use `transform` with easing rather than straight-line movement.

### 8. Secondary Action
Ripple effects, icon rotations, or shadow changes accompany the primary scale/color change. Don't let secondary actions overpower.

### 9. Timing
- Hover: 150-200ms
- Active/press: 50-100ms (snappy)
- Focus ring: 150ms
- Loading state transition: 200-300ms

### 10. Exaggeration
Success buttons can briefly scale to 1.05 before settling. Error states can include subtle shake (3-5px, 2-3 cycles).

### 11. Solid Drawing
Maintain consistent border-radius and proportions across states. Shadows should respect light source direction throughout.

### 12. Appeal
Round corners feel friendly, sharp corners feel professional. Match button personality to brand. Satisfying click feedback increases conversions.

## CSS Implementation

```css
.btn {
  transition: transform 150ms ease-out,
              box-shadow 150ms ease-out,
              background-color 150ms ease-out;
}

.btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.btn:active {
  transform: scale(0.97) translateY(0);
  transition-duration: 50ms;
}
```

## Key Properties
- `transform`: scale, translate
- `box-shadow`: depth changes
- `background-color`: state indication
- `opacity`: disabled states
- `filter`: brightness on hover
