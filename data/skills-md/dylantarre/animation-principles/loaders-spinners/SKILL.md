---
name: loaders-spinners
description: Use when creating loading indicators, spinners, progress bars, or skeleton screens to communicate system status
---

# Loader & Spinner Animation Principles

Apply Disney's 12 principles to loading indicators for engaging, informative wait experiences.

## Principles Applied to Loaders

### 1. Squash & Stretch
Bouncing dot loaders should squash on landing, stretch while rising. Creates life-like, playful motion.

### 2. Anticipation
Before progress completes, bar can briefly pause or slow. Spinners can decelerate before stopping. Signals completion coming.

### 3. Staging
Loader should be clearly visible but not block content unnecessarily. Skeleton screens stage where real content will appear.

### 4. Straight Ahead & Pose to Pose
Organic loaders (bouncing dots) benefit from straight-ahead. Progress bars use pose-to-pose (0% to 100% keyframes).

### 5. Follow Through & Overlapping Action
Multi-part loaders should have elements offset in timing. Dot 1 bounces, dot 2 follows 100ms later. Creates rhythm.

### 6. Ease In & Ease Out
Spinning: use `ease-in-out` per rotation cycle or `linear` for continuous. Bouncing: `ease-in` up, `ease-out` down.

### 7. Arcs
Orbital loaders should follow true circular arcs. Bouncing elements follow parabolic arcs like real physics.

### 8. Secondary Action
While spinner rotates (primary), glow pulses (secondary). Skeleton shimmer is secondary to skeleton shape.

### 9. Timing
- Spinner full rotation: 800-1200ms
- Bounce cycle: 500-800ms
- Skeleton shimmer: 1500-2500ms
- Progress bar smooth updates: 200ms
- Dot stagger: 100-150ms
- Pulse: 1000-2000ms

### 10. Exaggeration
Playful brands can use bouncy, elastic loaders. Professional contexts need subtle, smooth spinners. Match brand energy.

### 11. Solid Drawing
Maintain consistent stroke widths. Circular paths should be true circles. Progress bars should fill evenly.

### 12. Appeal
Engaging loaders reduce perceived wait time. Boring spinners feel slower. A delightful loader can turn frustration into momentary joy.

## CSS Implementation

```css
.spinner {
  animation: spin 1000ms linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.bounce-dot {
  animation: bounce 600ms ease-in-out infinite alternate;
}

.bounce-dot:nth-child(2) { animation-delay: 100ms; }
.bounce-dot:nth-child(3) { animation-delay: 200ms; }

@keyframes bounce {
  from { transform: translateY(0) scaleY(1); }
  to { transform: translateY(-20px) scaleY(0.9); }
}

.skeleton {
  background: linear-gradient(90deg, #eee 25%, #f5f5f5 50%, #eee 75%);
  background-size: 200% 100%;
  animation: shimmer 2000ms infinite;
}

@keyframes shimmer {
  to { background-position: -200% 0; }
}
```

## Key Properties
- `transform`: rotate, translateY, scale
- `animation`: infinite loops
- `background-position`: shimmer effects
- `stroke-dashoffset`: SVG spinners
- `opacity`: pulsing effects
