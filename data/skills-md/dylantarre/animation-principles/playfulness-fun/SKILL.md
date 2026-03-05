---
name: playfulness-fun
description: Use when creating animations that entertain, engage with humor, or create lighthearted interactive experiences.
---

# Playfulness & Fun Animation

Create animations that entertain, surprise, and make interactions genuinely enjoyable.

## Emotional Goal

Playfulness invites interaction through unexpected, whimsical motion. Fun comes from animations that have personality, respond expressively, and make users smile.

## Disney Principles for Playfulness

### Squash & Stretch
Generous, exaggerated (25-40%). Rubbery, cartoon physics. Objects should feel alive and reactive. Bounce like a beach ball.

### Anticipation
Exaggerated wind-ups (150-250ms). Comic timing—big preparation for big payoff. Elements "think" before acting.

### Staging
Theatrical presentation. Clear setup and punchline. Give playful moments room to breathe and be noticed.

### Straight Ahead Action
Embrace spontaneity. Wobbly paths, unpredictable bounces. Characters and elements with minds of their own.

### Follow Through & Overlapping Action
Extensive, bouncy follow-through. Overshoots, wobbles, and settling. Like a cartoon character skidding to a stop.

### Slow In & Slow Out
Asymmetric with overshoot. Quick starts, bouncy landings. `cubic-bezier(0.68, -0.55, 0.265, 1.55)` for elastic effect.

### Arc
Exaggerated, bouncy curves. High arcs for jumps. Squiggly paths for personality. Nothing moves in straight lines.

### Secondary Action
Abundant! Wiggles, sparkles, expressions. Elements react to each other. The whole interface feels alive.

### Timing
Varied and expressive (100-500ms). Quick snaps, slow anticipation. Comic timing with beats and pauses.

### Exaggeration
High (30-50%). Push movements to cartoon levels. Impossible physics that feel emotionally true.

### Solid Drawing
Maintain appeal through deformation. Stretched elements stay charming. Volume shifts for effect.

### Appeal
Round, friendly shapes. Bright, saturated colors. Big eyes, expressive forms. Character in everything.

## Timing Recommendations

| Element | Duration | Easing |
|---------|----------|--------|
| Bounce | 400-600ms | `spring(1, 60, 8)` |
| Wiggle | 300-400ms | `ease-in-out` |
| Pop | 150-250ms | `ease-out-back` |
| Squash | 100-150ms | `ease-out` |

## CSS Easing

```css
--play-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
--play-elastic: cubic-bezier(0.34, 1.56, 0.64, 1);
--play-wobble: cubic-bezier(0.45, 0.05, 0.55, 0.95);
```

## Fun Animations

```css
@keyframes wiggle {
  0%, 100% { transform: rotate(0deg); }
  25% { transform: rotate(-5deg); }
  75% { transform: rotate(5deg); }
}

@keyframes boing {
  0% { transform: scale(1); }
  30% { transform: scale(1.25, 0.75); }
  50% { transform: scale(0.85, 1.15); }
  70% { transform: scale(1.05, 0.95); }
  100% { transform: scale(1); }
}
```

## When to Use

- Games and gamification
- Children's interfaces
- Social media reactions
- Onboarding tutorials
- Empty states
- Easter eggs
- Casual apps
- Entertainment platforms
