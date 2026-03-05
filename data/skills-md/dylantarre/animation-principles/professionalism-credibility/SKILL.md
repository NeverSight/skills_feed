---
name: professionalism-credibility
description: Use when creating animations for business contexts that require seriousness, competence, and trustworthy presentation.
---

# Professionalism & Credibility Animation

Create animations that convey competence, seriousness, and business-appropriate polish.

## Emotional Goal

Professionalism means motion that respects users' time and context. Credibility comes from animations that demonstrate technical competence without showing off.

## Disney Principles for Professionalism

### Squash & Stretch
None to minimal (0-5%). Professional interfaces use rigid, precise motion. Objects maintain exact proportions.

### Anticipation
Brief and functional (50-100ms). Just enough to prevent surprise. No theatrical preparation—get to the point.

### Staging
Clear hierarchy and purpose. Business-appropriate layouts. Every element in its proper place with clear function.

### Straight Ahead Action
Avoid entirely. Professional motion is controlled and predictable. No spontaneity or variation.

### Follow Through & Overlapping Action
Minimal, controlled settling. Quick stabilization. No bouncing or playfulness—immediate completion.

### Slow In & Slow Out
Smooth, professional curves. Standard easing that feels polished but not decorative. `ease-out` for efficiency.

### Arc
Minimal curves, direct paths preferred. Professional motion is efficient. Straight lines communicate directness.

### Secondary Action
Functional only. Loading states, progress indicators. No decorative animation—everything serves a purpose.

### Timing
Efficient and consistent (150-250ms). Quick enough to feel responsive, slow enough to track. No wasted time.

### Exaggeration
None. Realistic, proportional movements. Professional means grounded and believable.

### Solid Drawing
Precise, consistent geometry. Perfect alignment. Technical accuracy in every detail.

### Appeal
Clean, systematic design. Grid-based layouts. Neutral colors. Function-first aesthetics.

## Timing Recommendations

| Element | Duration | Easing |
|---------|----------|--------|
| Transitions | 150-250ms | `ease-out` |
| Feedback | 100-150ms | `ease-out` |
| Modals | 200-250ms | `ease-out` |
| Data updates | 150-200ms | `ease-in-out` |

## CSS Easing

```css
--pro-standard: cubic-bezier(0.4, 0, 0.2, 1);
--pro-enter: cubic-bezier(0.0, 0, 0.2, 1);
--pro-exit: cubic-bezier(0.4, 0, 1, 1);
```

## Professional Patterns

```css
@keyframes pro-fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes pro-slide-up {
  from {
    opacity: 0;
    transform: translateY(8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.professional-element {
  animation: pro-slide-up 200ms ease-out forwards;
}
```

## Credibility Guidelines

- Consistent timing builds trust
- Smooth motion signals competence
- No animation is better than bad animation
- Match platform conventions
- Respect prefers-reduced-motion
- Test across devices for consistency

## When to Use

- B2B software
- Financial dashboards
- Legal and compliance tools
- Healthcare administration
- Government services
- Enterprise applications
- Professional portfolios
- Corporate websites
