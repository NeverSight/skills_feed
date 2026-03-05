---
name: icons-badges
description: Use when animating icons, badges, avatars, status indicators, or small visual elements to add personality and feedback
---

# Icon & Badge Animation Principles

Apply Disney's 12 principles to small UI elements for personality and meaningful feedback.

## Principles Applied to Icons

### 1. Squash & Stretch
Heart icons can squash/stretch on "like" tap. Notification badges can bounce with squash on arrival. Adds life to small elements.

### 2. Anticipation
Before icon action, brief scale down (0.9) for 50ms. Bell can tilt back before ringing forward. Prepares for action.

### 3. Staging
Active/important icons should be visually prominent: color, size, or animation. Badges use contrasting colors to stand out.

### 4. Straight Ahead & Pose to Pose
Simple icons use pose-to-pose (two states). Complex icon animations (morphing) can use straight-ahead for organic transitions.

### 5. Follow Through & Overlapping Action
Bell ring continues after user interaction stops. Badge number updates before badge bounce settles. Multi-part icons offset timing.

### 6. Ease In & Ease Out
Icon hover: `ease-out`. Icon click: `ease-in-out`. Bounce: `cubic-bezier(0.68, -0.55, 0.27, 1.55)` for overshoot.

### 7. Arcs
Bell swinging follows pendulum arc. Refresh icons spin in true circular arcs. Arrows can arc during state changes.

### 8. Secondary Action
While icon scales (primary), color changes (secondary), glow pulses (tertiary). Badge count changes while badge bounces.

### 9. Timing
- Hover scale: 100-150ms
- Click feedback: 50-100ms
- Badge bounce: 300-400ms
- Bell ring: 400-600ms
- Status pulse: 1500-2500ms
- Morph transition: 250-350ms

### 10. Exaggeration
Celebratory icons (confetti, hearts) can be very animated. Functional icons (menu, close) should be subtle. Match purpose.

### 11. Solid Drawing
Icons must remain crisp at all animation frames. Maintain stroke consistency. Badge numbers should be legible during motion.

### 12. Appeal
Animated icons add personality. A bouncing notification feels alive. A pulsing status feels responsive. Small touches matter greatly.

## CSS Implementation

```css
.icon-btn:hover .icon {
  transform: scale(1.15);
  transition: transform 150ms ease-out;
}

.icon-btn:active .icon {
  transform: scale(0.9);
  transition: transform 50ms ease-in;
}

.badge {
  animation: badgeBounce 400ms cubic-bezier(0.68, -0.55, 0.27, 1.55);
}

@keyframes badgeBounce {
  0% { transform: scale(0); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

.status-indicator {
  animation: pulse 2000ms ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.6; transform: scale(1.1); }
}

.bell-icon:hover {
  animation: ring 500ms ease-in-out;
}

@keyframes ring {
  0%, 100% { transform: rotate(0); }
  20%, 60% { transform: rotate(15deg); }
  40%, 80% { transform: rotate(-15deg); }
}
```

## Key Properties
- `transform`: scale, rotate
- `opacity`: pulse effects
- `animation`: complex sequences
- `fill`/`stroke`: SVG color changes
- `filter`: glow effects
