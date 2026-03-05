---
name: universal-timing
description: Use when learning animation timing fundamentals - principles that apply regardless of duration, the foundational rules that scale across all time ranges
---

# Universal Timing Principles

Some animation truths **transcend duration**. These principles work at 50ms and 5000ms. Master these to make good timing decisions at any scale.

## Disney Principles - Universal Application

### Always True

**Squash & Stretch**: Scale proportionally - 5% at 100ms, 30% at 2000ms. Never eliminate, always proportional.

**Anticipation**: Ratio stays constant - anticipation is 20-30% of main action duration, regardless of total time.

**Staging**: One clear focus - whether instant or cinematic, only one thing should demand primary attention.

**Straight Ahead/Pose to Pose**: Complexity matches duration - short = straight ahead, long = pose to pose.

**Follow Through**: Present at all durations - even 100ms can have micro-overshoot. Scale matches duration.

**Slow In/Slow Out**: Always ease - linear motion looks mechanical at every duration.

**Arcs**: Natural paths scale - short animations = subtle curves, long animations = sweeping arcs.

**Secondary Action**: Supports, never competes - true at 50ms and 5000ms.

**Timing**: Duration determines perception - same motion reads differently at different speeds.

**Exaggeration**: Match duration and importance - longer duration allows more exaggeration.

**Solid Drawing**: Transforms must match - consistency matters regardless of speed.

**Appeal**: The goal - animation should enhance, not impede, at any duration.

## Universal Ratios

### The Golden Ratio of Animation Timing

```
Anticipation : Action : Follow-through
    20%      :   50%  :     30%

Example at 500ms:
  Anticipation: 100ms
  Main action: 250ms
  Follow-through: 150ms
```

### Stagger Ratio

```
Optimal stagger delay: 10-20% of item duration

Item duration: 300ms
Stagger delay: 30-60ms between items
```

### Easing Intensity vs Duration

```
Duration < 150ms: ease-out only (no time for ease-in)
Duration 150-400ms: ease-out or custom
Duration 400ms+: full ease-in-out possible
```

## Easing That Works Everywhere

```css
/* Universal ease-out - works at any duration */
transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1);

/* Universal natural motion */
transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);

/* Universal bounce - scale amplitude with duration */
transition-timing-function: cubic-bezier(0.34, 1.56, 0.64, 1);
```

## Universal Laws

1. **Shorter distances = shorter durations** - motion should feel proportional to space.

2. **Bigger elements move slower** - perceived weight requires more time.

3. **Enter fast, exit faster** - users care about what's arriving, not leaving.

4. **Context determines tolerance** - first visit allows longer animation than repeat use.

5. **Attention is finite** - compete for it wisely, regardless of duration.

6. **Physics provides intuition** - match real-world expectations at any speed.

7. **Easing is mandatory** - linear motion looks wrong at every duration.

8. **Test at extremes** - if it works at 2x and 0.5x, it's robust.

## Duration Selection Framework

```
What should the user feel?
├── Instant (< 100ms)
│   └── Confirmation, responsiveness
├── Quick (100-300ms)
│   └── Efficiency, polish
├── Standard (300-500ms)
│   └── Clarity, communication
├── Deliberate (500-1000ms)
│   └── Importance, attention
└── Dramatic (> 1000ms)
    └── Story, emotion, memory
```

## Key Insight

Duration is a **design decision**. It communicates importance, guides attention, and shapes emotion. The Disney principles are tools - timing is how you wield them. Master the principles, then let context determine duration.
