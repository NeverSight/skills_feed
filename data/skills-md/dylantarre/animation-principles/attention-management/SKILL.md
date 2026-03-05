---
name: attention-management
description: Use when wrong elements get attention, important content is missed, or visual hierarchy is broken by animation
---

# Attention Management

Direct user focus correctly using Disney's principles.

## Problem Indicators
- Users miss important content
- Decorative elements steal focus
- CTAs don't stand out
- Users look at wrong things first
- Information hierarchy is unclear

## Diagnosis by Principle

### Staging
**Issue**: Multiple elements compete for attention
**Fix**: One thing moves at a time. Animate the most important element; keep others still.

### Timing
**Issue**: Everything animates at same speed
**Fix**: Primary content: faster animation. Secondary: slower or delayed. Speed implies importance.

### Exaggeration
**Issue**: Uniform motion across hierarchy
**Fix**: Important elements get more dramatic animation. Background elements get subtle motion.

### Anticipation
**Issue**: No buildup directs eyes
**Fix**: Use anticipation to guide attention. A small movement can draw eyes before the main action.

### Appeal
**Issue**: Wrong elements are visually interesting
**Fix**: Make important elements the most visually appealing. Animation should enhance hierarchy, not fight it.

## Quick Fixes

1. **One animation at a time** - Sequence, don't parallelize
2. **Stagger by importance** - Most important animates first
3. **Reduce decorative motion** - Background should be calm
4. **Increase CTA animation contrast** - Stands out from surroundings
5. **Use motion to guide reading order** - Top-to-bottom, left-to-right

## Troubleshooting Checklist

- [ ] What do users look at first? (Eye tracking or testing)
- [ ] Does animation sequence match importance hierarchy?
- [ ] Are decorative animations subtle enough?
- [ ] Does primary CTA have strongest motion?
- [ ] Count simultaneous animations (should be 1-2)
- [ ] Test: Hide animation—does hierarchy still work?
- [ ] Is motion guiding or distracting?
- [ ] Does stillness create emphasis where needed?

## Code Pattern

```css
/* Stagger by importance */
.hero-title {
  animation: fadeInUp 400ms ease-out;
}

.hero-subtitle {
  animation: fadeInUp 400ms ease-out 100ms backwards;
}

.hero-cta {
  animation: fadeInUp 400ms ease-out 200ms backwards,
             pulse 2s ease-in-out 1s infinite;
}

/* De-emphasize background */
.background-element {
  animation: subtleDrift 20s linear infinite;
  opacity: 0.3;
}
```

## Hierarchy Through Motion

| Priority | Animation Style |
|----------|----------------|
| Primary | Fast, prominent, potentially looping |
| Secondary | Medium speed, one-time |
| Tertiary | Slow, subtle, or static |
| Background | Very slow or no animation |
