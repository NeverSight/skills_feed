---
name: user-feedback-clarity
description: Use when users don't notice feedback, miss state changes, or can't tell if their action worked
---

# User Feedback Clarity

Make feedback animations unmissable using Disney's principles.

## Problem Indicators
- Users click multiple times (didn't see feedback)
- "Did it work?" questions
- Users miss success/error states
- Form submission confusion
- State changes go unnoticed

## Diagnosis by Principle

### Anticipation
**Issue**: No buildup before action completes
**Fix**: Show loading/processing state immediately. User should know their input was received.

### Follow Through
**Issue**: Feedback appears and vanishes too quickly
**Fix**: Let feedback linger. Success messages need 2-3 seconds minimum. Add settle animation.

### Staging
**Issue**: Feedback appears outside user's focus
**Fix**: Show feedback near the trigger. If button was clicked, feedback should appear on/near button.

### Exaggeration
**Issue**: Feedback is too subtle
**Fix**: Increase contrast, size change, or motion. Feedback must compete with user's task focus.

### Secondary Action
**Issue**: Only one feedback channel
**Fix**: Combine channels: visual + motion + color. Error = red + shake. Success = green + checkmark + pulse.

## Quick Fixes

1. **Immediate acknowledgment** - Show something within 100ms
2. **Animate the trigger** - Button should respond visibly
3. **Use color + motion together** - Redundant signals
4. **Keep feedback in viewport** - Near user's focus
5. **Add haptic feedback** - On supported devices

## Troubleshooting Checklist

- [ ] Does feedback appear within 100ms of action?
- [ ] Is feedback in user's current focus area?
- [ ] Would feedback be noticed peripherally?
- [ ] Are multiple senses engaged (visual, motion)?
- [ ] Does feedback last long enough to read?
- [ ] Is error feedback more prominent than success?
- [ ] Test: Can users tell if action succeeded without reading text?
- [ ] Test with users—ask "did that work?"

## Code Pattern

```css
/* Button feedback */
.button:active {
  transform: scale(0.95);
}

.button.loading {
  pointer-events: none;
}

.button.success {
  animation: successPulse 300ms ease-out;
}

@keyframes successPulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); background: var(--success); }
  100% { transform: scale(1); }
}

/* Error shake */
@keyframes errorShake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}
```
