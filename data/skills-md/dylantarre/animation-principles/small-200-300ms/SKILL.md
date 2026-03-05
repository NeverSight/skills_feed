---
name: small-200-300ms
description: Use when building small transitions between 200-300ms - modal appearances, card expansions, navigation transitions that users consciously perceive
---

# Small Transitions (200-300ms)

At 200-300ms, users **consciously perceive motion**. This duration bridges micro-interactions and full animations - ideal for UI state changes.

## Disney Principles at Small Duration

### Works Well

**Squash & Stretch**: Visible but restrained - 10-15% for playful interfaces, 5% for professional.

**Anticipation**: Brief wind-up works - 40-60ms preparation enhances 200ms main action.

**Staging**: Clear hierarchy - primary element leads, secondary follows by 50-100ms.

**Straight Ahead/Pose to Pose**: Pose to pose preferred - keyframes create polished motion.

**Follow Through**: Noticeable overshoot - 5-10% past target adds life.

**Slow In/Slow Out**: Full easing curves - both ease-in-out and custom beziers shine.

**Arcs**: Natural curves enhance - elements can travel on arcs rather than straight lines.

**Secondary Action**: One or two secondary actions - fade + scale, move + rotate.

**Timing**: 12-18 frames at 60fps. Smooth, deliberate motion.

**Exaggeration**: Moderate to pronounced - depends on brand personality.

**Solid Drawing**: Full transform combinations - translate, scale, rotate together.

**Appeal**: Conscious animation that builds brand character.

### Doesn't Work

- Feeling instant (too slow)
- Complex character animation
- Long travel distances
- Multiple sequential stages

## Easing Recommendations

```css
/* Standard smooth transition */
transition: all 250ms ease-out;

/* Modal/card appearance - confident arrival */
transition: all 250ms cubic-bezier(0.16, 1, 0.3, 1);

/* Bouncy personality */
transition: transform 280ms cubic-bezier(0.34, 1.56, 0.64, 1);

/* Professional, subtle */
transition: all 220ms cubic-bezier(0.4, 0, 0.2, 1);
```

## Best Use Cases

- Modal dialogs appearing
- Card expand/collapse
- Navigation drawer slides
- Tab content transitions
- Filter panel toggles
- Image thumbnails expanding
- Alert/notification slides

## Implementation Pattern

```css
.modal {
  opacity: 0;
  transform: translateY(20px) scale(0.95);
  transition: opacity 200ms ease-out,
              transform 250ms cubic-bezier(0.16, 1, 0.3, 1);
}

.modal.open {
  opacity: 1;
  transform: translateY(0) scale(1);
}

.card-expand {
  transition: all 280ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

## Key Insight

Small transitions are **seen and understood**. Users track the motion and their brain processes the spatial relationship. Use this to guide attention and communicate hierarchy.
