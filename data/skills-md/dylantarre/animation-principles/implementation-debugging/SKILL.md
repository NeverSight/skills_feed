---
name: implementation-debugging
description: Use when animation doesn't work as expected, has bugs, or behaves inconsistently
---

# Implementation Debugging

Debug animation issues using Disney's principles as diagnostic framework.

## Problem Indicators
- Animation doesn't play at all
- Animation plays but looks wrong
- Works in dev, broken in production
- Inconsistent across browsers
- Animation triggers at wrong time
- Flickering or visual glitches

## Diagnosis by Principle

### Timing
**Issue**: Animation timing is off
**Debug**: Check duration values. Verify units (ms vs s). Check if CSS transition is being overridden. Inspect computed styles.

### Straight Ahead vs Pose-to-Pose
**Issue**: Keyframes not hitting
**Debug**: Verify all keyframe percentages. Check for typos in property names. Ensure values are animatable.

### Staging
**Issue**: Animation hidden or clipped
**Debug**: Check z-index, overflow, opacity. Verify element is in viewport. Check for `visibility: hidden`.

### Solid Drawing
**Issue**: Visual glitches during animation
**Debug**: Look for subpixel rendering issues. Add `transform: translateZ(0)` for GPU layer. Check for layout thrashing.

### Follow Through
**Issue**: Animation ends abruptly or wrong state
**Debug**: Check `animation-fill-mode`. Verify end state matches CSS. Check for competing animations.

## Common Bugs

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| No animation | Property not animatable | Use transform instead of changing property directly |
| Flicker at start | No initial state | Set initial values explicitly |
| Wrong end state | Fill mode | Add `forwards` to animation |
| Choppy motion | Layout thrashing | Animate only transform/opacity |
| Works once only | Animation not reset | Remove and re-add class, or use JS |

## Quick Fixes

1. **Check DevTools Animation panel** - See timeline
2. **Verify animatable properties** - Not all CSS animates
3. **Add `animation-fill-mode: forwards`** - Keep end state
4. **Force GPU layer** - `will-change: transform`
5. **Check for `!important`** - May override animation

## Troubleshooting Checklist

- [ ] Is animation class/trigger being applied? (DevTools Elements)
- [ ] Are properties animatable? (`display` is not, `opacity` is)
- [ ] Check computed styles for overrides
- [ ] Is element visible? (opacity, visibility, display, z-index)
- [ ] Any JavaScript errors blocking execution?
- [ ] Check Animation panel in DevTools
- [ ] Test in incognito (no extensions)
- [ ] Compare working vs broken environment

## Code Pattern

```js
// Debug: Log animation events
element.addEventListener('animationstart', (e) => {
  console.log('Animation started:', e.animationName);
});

element.addEventListener('animationend', (e) => {
  console.log('Animation ended:', e.animationName);
});

// Debug: Check computed animation
const styles = getComputedStyle(element);
console.log('Animation:', styles.animation);
console.log('Transition:', styles.transition);

// Reset animation
element.classList.remove('animate');
void element.offsetWidth; // Trigger reflow
element.classList.add('animate');
```

## DevTools Tips

1. **Elements > Styles**: Check computed animation values
2. **Performance tab**: Record and analyze frames
3. **Animations panel**: Slow down, replay, inspect
4. **Console**: Log animation events
