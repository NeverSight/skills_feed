---
name: slow-800-1200ms
description: Use when building deliberate motion between 800-1200ms - dramatic reveals, loading sequences, storytelling moments where users should pause and absorb
---

# Slow Animations (800-1200ms)

At 800-1200ms, animation approaches **cinematic territory**. This is deliberate, intentional motion for moments that matter. Users are expected to stop and watch.

## Disney Principles at Slow Speed

### Cinematic Application

**Squash & Stretch**: Pronounced and characterful - 25-35% deformation tells stories. Objects have weight and personality.

**Anticipation**: Full theatrical wind-up - 200-300ms preparation. The audience knows something is coming.

**Staging**: Scene composition - think in terms of camera and stage. Clear visual hierarchy with entrance order.

**Straight Ahead/Pose to Pose**: Pose to pose essential - 4-6 key poses for 1 second of motion.

**Follow Through**: Extended overlap - different elements settle at clearly different times, 200-300ms of settling.

**Slow In/Slow Out**: Dramatic curves - strong ease-in creates weight, strong ease-out creates impact.

**Arcs**: Sweeping curves - motion paths are clearly curved, visible trajectories.

**Secondary Action**: Complex layering - multiple levels of supporting action enhance primary motion.

**Timing**: 48-72 frames at 60fps. Near-film quality frame counts.

**Exaggeration**: Theatrical - push proportions and motion for emotional impact.

**Solid Drawing**: Full dimensional transforms - parallax, depth, 3D rotation.

**Appeal**: Emotional connection - slow motion creates intimacy with the interface.

## Easing Recommendations

```css
/* Dramatic, weighted motion */
transition: all 1000ms cubic-bezier(0.16, 1, 0.3, 1);

/* Graceful entrance */
transition: all 900ms cubic-bezier(0.22, 1, 0.36, 1);

/* Heavy, impactful landing */
transition: transform 1100ms cubic-bezier(0.33, 1, 0.68, 1);

/* Elastic, memorable */
transition: all 1000ms cubic-bezier(0.68, -0.6, 0.32, 1.6);
```

## Best Use Cases

- App launch sequences
- Major feature reveals
- Storytelling moments
- Error recovery animations
- Achievement unlocks
- Tutorial sequences
- First-run experiences
- Section transitions in presentations
- Loading state to content reveals

## Implementation Pattern

```css
@keyframes slowReveal {
  0% {
    opacity: 0;
    transform: translateY(100px) scale(0.8);
  }
  60% {
    opacity: 1;
  }
  100% {
    transform: translateY(0) scale(1);
  }
}

.slow-reveal {
  animation: slowReveal 1000ms cubic-bezier(0.16, 1, 0.3, 1) forwards;
}

/* Staggered sequence */
.sequence-item {
  animation: slowReveal 900ms cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
.sequence-item:nth-child(n) {
  animation-delay: calc(var(--index) * 150ms);
}
```

## When NOT to Use

- Navigation between views (too slow)
- Repeated interactions (users get impatient)
- High-frequency actions
- Data-heavy interfaces
- Productivity tools

## Key Insight

Slow animations demand **attention as payment**. Only use when the moment is worth the user's time. These animations create memories, not just feedback.
