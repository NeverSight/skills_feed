---
name: ux-friction
description: Use when animation causes user confusion, delays task completion, or creates frustration
---

# UX Friction

Diagnose animations that block, confuse, or frustrate users.

## Problem Indicators
- Users wait for animations to finish
- Confusion about what happened
- Repeated clicks/taps during animation
- Users skip or abandon tasks
- "Where did that go?" moments

## Diagnosis by Principle

### Timing
**Issue**: Animation too slow for the context
**Fix**: Match duration to user intent. Micro-interactions: 100-200ms. Transitions: 200-400ms. Never block input.

### Anticipation
**Issue**: Action happens without warning
**Fix**: Add subtle anticipation cues before significant changes. A button press should show feedback before the result.

### Follow Through
**Issue**: Animation ends abruptly
**Fix**: Let elements settle naturally. Sudden stops feel broken. Add slight overshoot and settle.

### Staging
**Issue**: Important changes happen outside focus
**Fix**: Draw attention to where change occurs. If content moves, guide the eye with motion.

### Appeal
**Issue**: Animation feels arbitrary
**Fix**: Every animation should have clear purpose. If users question "why does this bounce?", remove it.

## Quick Fixes

1. **Make animations skippable** - Click/tap should complete or skip
2. **Reduce duration by 30%** - Most animations are too slow
3. **Add progress indicators** - For anything over 400ms
4. **Animate in user's focus area** - Don't move things peripherally
5. **Remove decorative animations** - If it doesn't help, it hurts

## Troubleshooting Checklist

- [ ] Can users interact during animation?
- [ ] Is duration under 400ms for transitions?
- [ ] Does animation communicate state change?
- [ ] Is the animation skippable if lengthy?
- [ ] Does motion guide attention correctly?
- [ ] Is there feedback for user input?
- [ ] Would removing animation hurt understanding?
- [ ] Test with impatient users (click rapidly)

## Pattern

```js
// Allow interaction during animation
element.style.pointerEvents = 'auto';

// Make animation skippable
element.addEventListener('click', () => {
  element.getAnimations().forEach(a => a.finish());
});
```
