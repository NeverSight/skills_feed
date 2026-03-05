---
name: large-500-800ms
description: Use when building larger movement animations between 500-800ms - hero transitions, complex reveals, animations that tell a story and deserve attention
---

# Large Animations (500-800ms)

At 500-800ms, animations become **events**. Users stop and watch. Reserve this duration for significant moments that deserve attention and communicate importance.

## Disney Principles at Large Scale

### Full Expression of All Principles

**Squash & Stretch**: Dramatic deformation - 20-30% stretch visible and characterful. Objects feel elastic and alive.

**Anticipation**: Extended wind-up - 150-200ms anticipation sells the action. Clear "about to happen" signal.

**Staging**: Sophisticated choreography - multiple elements with clear hierarchy and timing offsets.

**Straight Ahead/Pose to Pose**: Definitely pose to pose - complex motion needs keyframe control.

**Follow Through**: Extended settling - elements continue moving 100-200ms after main action completes.

**Slow In/Slow Out**: Dramatic easing - strong deceleration creates impact at endpoints.

**Arcs**: Essential - all movement should follow natural curved paths.

**Secondary Action**: Rich layering - primary, secondary, and tertiary actions possible.

**Timing**: 30-48 frames at 60fps. Full cinematic range.

**Exaggeration**: Go bold - this duration supports theatrical expression.

**Solid Drawing**: Full 3D transforms - depth, perspective, complex rotations.

**Appeal**: Memorable moments - users will recall these animations.

## Easing Recommendations

```css
/* Dramatic entrance */
transition: all 600ms cubic-bezier(0.16, 1, 0.3, 1);

/* Powerful deceleration */
transition: all 700ms cubic-bezier(0, 0.55, 0.45, 1);

/* Elastic landing */
transition: transform 650ms cubic-bezier(0.68, -0.55, 0.265, 1.55);

/* Smooth, cinematic */
transition: all 800ms cubic-bezier(0.25, 0.1, 0.25, 1);
```

## Best Use Cases

- Hero image/section reveals
- Major feature introductions
- Success/completion celebrations
- Onboarding sequences
- Dashboard data loads
- Portfolio piece reveals
- First-time user experiences
- Important state changes

## Implementation Pattern

```css
.hero-reveal {
  opacity: 0;
  transform: translateY(60px) scale(0.9);
  transition: opacity 500ms ease-out,
              transform 700ms cubic-bezier(0.16, 1, 0.3, 1);
}

.hero-reveal.visible {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* Staggered reveal with follow-through */
.hero-title { transition-delay: 0ms; }
.hero-subtitle { transition-delay: 100ms; }
.hero-cta { transition-delay: 200ms; }
```

## Warning Signs

- If users seem impatient, duration is too long
- If used for common actions, flow suffers
- If multiple large animations compete, staging fails

## Key Insight

Large animations are **moments of theater**. They punctuate the experience and create memory. Use sparingly - every large animation should earn its duration.
