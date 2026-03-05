---
name: brand-consistency
description: Use when animation doesn't match brand personality, feels generic, or clashes with design language
---

# Brand Consistency

Align animation style with brand identity using Disney's principles.

## Problem Indicators
- Animation feels "off-brand"
- Generic motion that could be any product
- Inconsistent animation styles across features
- Motion conflicts with brand voice
- Users don't recognize the product's personality

## Diagnosis by Principle

### Appeal
**Issue**: Animation lacks distinctive character
**Fix**: Define brand motion attributes. Is your brand playful (bouncy easing), professional (smooth, minimal), energetic (quick, snappy)?

### Exaggeration
**Issue**: Wrong level of drama for brand
**Fix**: Match exaggeration to brand personality. Luxury = subtle. Playful = bouncy. Corporate = restrained.

### Timing
**Issue**: Speed doesn't match brand energy
**Fix**: Fast brands: 100-200ms. Calm brands: 300-500ms. Define a timing scale and use consistently.

### Squash and Stretch
**Issue**: Elastic effects conflict with serious brand
**Fix**: Reserve squash/stretch for playful brands. Use scale transforms for professional brands.

### Secondary Action
**Issue**: Details don't reinforce brand
**Fix**: Secondary actions should amplify brand personality. A fun brand might have playful ripples; a serious brand uses subtle fades.

## Quick Fixes

1. **Create a motion style guide** - Document easing, duration, principles used
2. **Define 3-5 brand motion words** - "Swift, precise, confident"
3. **Build reusable animation tokens** - Consistent timing/easing variables
4. **Audit existing animations** - Find outliers
5. **Create animation components** - Enforce consistency through code

## Troubleshooting Checklist

- [ ] Can you describe animation in 3 brand words?
- [ ] Does motion match brand voice guidelines?
- [ ] Are easing curves consistent across features?
- [ ] Is timing scale documented and followed?
- [ ] Would a competitor use identical animation?
- [ ] Do animations feel like the same product?
- [ ] Test: Show animation without UI—recognizable as your brand?
- [ ] Review with brand/design team

## Code Pattern

```css
:root {
  /* Brand motion tokens */
  --brand-ease-default: cubic-bezier(0.4, 0, 0.2, 1);
  --brand-ease-enter: cubic-bezier(0, 0, 0.2, 1);
  --brand-ease-exit: cubic-bezier(0.4, 0, 1, 1);
  --brand-duration-fast: 150ms;
  --brand-duration-normal: 250ms;
  --brand-duration-slow: 400ms;
}
```
