---
name: accessibility-issues
description: Use when animation excludes users with vestibular disorders, cognitive disabilities, or assistive technology needs
---

# Accessibility Issues

Make animations inclusive using Disney's principles thoughtfully.

## Problem Indicators
- Motion sickness complaints
- Vestibular disorder triggers
- Screen reader confusion
- Cognitive overload
- Seizure risk (flashing)
- Keyboard focus lost during animation

## Diagnosis by Principle

### Squash and Stretch
**Issue**: Excessive distortion causes disorientation
**Fix**: Reduce or eliminate squash/stretch for users with `prefers-reduced-motion`. Use opacity changes instead.

### Secondary Action
**Issue**: Too many moving elements
**Fix**: Limit to one animated element at a time. Secondary actions should be subtle or removed.

### Exaggeration
**Issue**: Dramatic motion triggers vestibular responses
**Fix**: Reduce scale, rotation, and position changes. Keep movements small and predictable.

### Timing
**Issue**: Animations too fast or too slow
**Fix**: Provide consistent, predictable timing. Avoid sudden speed changes.

### Arcs
**Issue**: Curved motion paths cause tracking difficulty
**Fix**: Use linear motion for essential UI. Save arcs for optional decorative elements.

## Quick Fixes

1. **Respect `prefers-reduced-motion`** - Always check and honor
2. **No autoplay animation** - Let users trigger motion
3. **Keep focus visible** - Never animate focus indicator away
4. **Announce changes** - Use ARIA live regions for dynamic content
5. **Provide pause controls** - For any looping animation

## Troubleshooting Checklist

- [ ] Does animation respect `prefers-reduced-motion`?
- [ ] Is there a way to pause/stop animations?
- [ ] Are state changes announced to screen readers?
- [ ] Does keyboard focus remain visible and logical?
- [ ] Is flash rate under 3 per second?
- [ ] Can users complete tasks without animation?
- [ ] Are animations triggered by user action (not autoplay)?
- [ ] Test with screen reader enabled

## Code Pattern

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

```js
// Check preference in JS
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;
```
