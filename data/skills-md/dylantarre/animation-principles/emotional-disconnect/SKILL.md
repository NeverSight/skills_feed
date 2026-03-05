---
name: emotional-disconnect
description: Use when animation feels wrong, creates unintended emotional response, or mismatches context
---

# Emotional Disconnect

Align animation emotion with context using Disney's principles.

## Problem Indicators
- Animation feels "off" but hard to articulate
- Playful motion on serious content
- Sterile motion on warm content
- Users describe UI as cold/robotic or chaotic/annoying
- Mismatch between animation and message

## Diagnosis by Principle

### Appeal
**Issue**: Animation lacks emotional resonance
**Fix**: Define the emotional goal. Warm = soft easing, overshoot. Professional = crisp, linear. Match motion to message.

### Exaggeration
**Issue**: Wrong intensity for emotional context
**Fix**: Serious contexts need restraint. Joyful contexts can be bouncy. Match exaggeration to emotional stakes.

### Timing
**Issue**: Speed conflicts with emotional tone
**Fix**: Calm emotions = slower. Excitement = faster. Tension = variable speed. Timing IS emotion.

### Squash and Stretch
**Issue**: Elastic effects on rigid contexts
**Fix**: Squash/stretch implies playfulness and life. Remove for serious, clinical, or professional contexts.

### Follow Through
**Issue**: Endings don't match emotional intent
**Fix**: Abrupt endings feel harsh. Soft landings feel gentle. Bouncy endings feel playful. Choose consciously.

## Quick Fixes

1. **Name the target emotion** - "This should feel calm"
2. **Match easing to emotion** - Bouncy = playful, smooth = calm
3. **Adjust timing to context** - Slow down serious moments
4. **Remove mismatch sources** - Cut animations that fight the tone
5. **Test with emotional vocabulary** - Ask users "how does this feel?"

## Troubleshooting Checklist

- [ ] What emotion should this moment evoke?
- [ ] Does animation easing match that emotion?
- [ ] Is timing appropriate for emotional context?
- [ ] Would removing animation feel better?
- [ ] Do similar products use different motion here?
- [ ] Ask users: "What 3 words describe this animation?"
- [ ] Does animation match content gravity?
- [ ] Test: Cover content, does motion emotion match?

## Emotion-to-Motion Map

| Emotion | Easing | Timing | Effects |
|---------|--------|--------|---------|
| Joy | Bouncy overshoot | Fast | Squash/stretch, scale up |
| Calm | Gentle ease-out | Slow | Fade, subtle slide |
| Trust | Smooth, predictable | Medium | Minimal, consistent |
| Urgency | Sharp ease-in | Fast | Direct, no overshoot |
| Playful | Spring physics | Variable | Rotation, bounce |
| Serious | Linear or subtle ease | Slow | Minimal movement |

## Code Pattern

```css
/* Calm/trustworthy */
--ease-calm: cubic-bezier(0.4, 0, 0.2, 1);

/* Playful/joyful */
--ease-playful: cubic-bezier(0.34, 1.56, 0.64, 1);

/* Urgent/serious */
--ease-urgent: cubic-bezier(0.4, 0, 1, 1);
```
