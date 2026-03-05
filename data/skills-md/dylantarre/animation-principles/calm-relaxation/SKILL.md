---
name: calm-relaxation
description: Use when creating animations that soothe users, reduce anxiety, or create peaceful, meditative experiences.
---

# Calm & Relaxation Animation

Create animations that soothe, settle, and create peaceful user experiences.

## Emotional Goal

Calm emerges from slow, gentle, predictable motion. Relaxation comes from animations that breathe, flow naturally, and never demand attention or create tension.

## Disney Principles for Calm

### Squash & Stretch
Very subtle (2-5%). Gentle breathing or pulsing rather than bouncing. Soft, organic deformation like clouds or water.

### Anticipation
Long, gradual preparation (200-400ms). Slow builds create no surprises. Everything telegraphed well in advance.

### Staging
Soft focus, ambient positioning. No aggressive attention-grabbing. Elements share space harmoniously without competition.

### Straight Ahead Action
Gentle, organic flow for ambient animations. Drifting clouds, floating particles, subtle gradients—natural randomness.

### Follow Through & Overlapping Action
Extended, graceful follow-through. Long settling times (500ms+). Elements drift to rest like leaves on water.

### Slow In & Slow Out
Heavy easing on both ends. Very gradual acceleration and deceleration. `cubic-bezier(0.4, 0, 0.6, 1)` for smooth, gentle motion.

### Arc
Wide, sweeping curves. Gentle parabolas. Motion should flow like water or wind—never angular or abrupt.

### Secondary Action
Ambient, background motion. Subtle parallax, gentle floating elements. Supporting motion that doesn't demand attention.

### Timing
Slow and deliberate (400-800ms+). Long durations feel meditative. No quick movements. Breathing rhythm: 4-6 seconds per cycle.

### Exaggeration
Minimal to none. Realistic, natural movements. Subtlety is calming; exaggeration creates tension.

### Solid Drawing
Soft edges, rounded forms. No sharp angles. Organic shapes that feel natural and comfortable.

### Appeal
Soft colors, low contrast. Gentle gradients. Rounded shapes. Natural, organic aesthetics.

## Timing Recommendations

| Element | Duration | Easing |
|---------|----------|--------|
| Fade transitions | 400-600ms | `ease-in-out` |
| Floating elements | 3000-5000ms | `ease-in-out` |
| Breathing pulse | 4000-6000ms | `ease-in-out` |
| Parallax drift | 800-1200ms | `ease-out` |

## CSS Easing

```css
--calm-gentle: cubic-bezier(0.4, 0, 0.6, 1);
--calm-float: cubic-bezier(0.37, 0, 0.63, 1);
--calm-breathe: cubic-bezier(0.45, 0, 0.55, 1);
```

## Breathing Animation

```css
@keyframes calm-breathe {
  0%, 100% {
    transform: scale(1);
    opacity: 0.8;
  }
  50% {
    transform: scale(1.02);
    opacity: 1;
  }
}

.breathing-element {
  animation: calm-breathe 5s ease-in-out infinite;
}
```

## When to Use

- Meditation and wellness apps
- Loading states for long processes
- Ambient backgrounds
- Reading experiences
- Night mode transitions
- Healthcare interfaces
- Onboarding welcome screens
- Success states that don't need celebration
