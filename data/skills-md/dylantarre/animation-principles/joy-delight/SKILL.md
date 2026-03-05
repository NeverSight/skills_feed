---
name: joy-delight
description: Use when creating animations that evoke happiness, surprise, or delightful moments in the user experience.
---

# Joy & Delight Animation

Create animations that spark happiness, pleasant surprise, and memorable delight.

## Emotional Goal

Joy emerges from unexpected pleasures, playful movements, and moments that exceed expectations. Delight comes from animations that feel alive, responsive, and genuinely fun.

## Disney Principles for Joy

### Squash & Stretch
Exaggerate bouncy, elastic movements. Objects that squash 30-40% on impact feel alive and playful. Use for success states, rewards, and celebrations.

### Anticipation
Build excitement before reveals. A slight pullback (100-150ms) before a pop-in creates satisfying payoff. Perfect for notifications and achievements.

### Staging
Draw focus to joyful moments. Clear visual hierarchy ensures the delightful element gets full attention. Dim surroundings during celebration animations.

### Straight Ahead Action
Create spontaneous, organic movements for confetti, particles, and celebration effects. Randomized paths feel natural and exciting.

### Follow Through & Overlapping Action
Let elements overshoot and settle with bouncy secondary motion. Hair, ribbons, and decorative elements should continue moving after main action.

### Slow In & Slow Out
Use asymmetric easing—quick starts with slow, satisfying landings. `cubic-bezier(0.34, 1.56, 0.64, 1)` creates playful overshoot.

### Arc
Bouncing, curved trajectories feel more joyful than linear paths. Elements should travel in parabolic arcs during celebrations.

### Secondary Action
Add sparkles, particles, or wobbles to primary animations. A "like" heart that radiates small hearts amplifies joy.

### Timing
Fast, snappy timing (150-250ms) feels energetic. Quick bursts with micro-pauses create rhythm. Success animations: 200-400ms.

### Exaggeration
Push proportions and movements 20-30% beyond realistic. Oversized bounces, stretched smiles, and amplified reactions.

### Solid Drawing
Maintain volume during stretchy movements. Squashed elements should expand horizontally to preserve mass—this reads as physicality.

### Appeal
Round shapes, bright colors, and smooth curves. Asymmetry in timing and position adds character and charm.

## Timing Recommendations

| Element | Duration | Easing |
|---------|----------|--------|
| Pop-in | 200-300ms | `ease-out-back` |
| Bounce | 300-500ms | `spring(1, 80, 10)` |
| Confetti | 800-1200ms | `ease-out` |
| Celebration | 400-600ms | `ease-out-elastic` |

## CSS Easing

```css
--joy-bounce: cubic-bezier(0.34, 1.56, 0.64, 1);
--joy-pop: cubic-bezier(0.175, 0.885, 0.32, 1.275);
--joy-elastic: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

## When to Use

- Success confirmations and completions
- Achievement unlocks and rewards
- Onboarding celebrations
- Easter eggs and surprises
- Positive feedback states
- Welcome animations
