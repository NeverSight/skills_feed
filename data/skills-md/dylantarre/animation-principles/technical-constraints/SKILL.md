---
name: technical-constraints
description: Use when animation is limited by browser support, platform capabilities, or technical requirements
---

# Technical Constraints

Work within platform limitations while preserving animation intent.

## Problem Indicators
- Animation doesn't work on target browsers
- Mobile devices can't handle animation
- Framework limitations block implementation
- File size constraints (Lottie, sprites)
- Email/constrained environment needs

## Diagnosis by Principle

### Straight Ahead vs Pose-to-Pose
**Issue**: Runtime calculations too expensive
**Fix**: Pre-calculate animations. Use CSS keyframes (pose-to-pose) over JS frame-by-frame (straight ahead).

### Solid Drawing
**Issue**: Complex shapes cause rendering issues
**Fix**: Simplify geometry. Use CSS shapes over SVG paths. Reduce polygon counts in 3D.

### Timing
**Issue**: Consistent timing across devices
**Fix**: Use relative units. Test on slowest target device. Consider `requestAnimationFrame` for JS.

### Secondary Action
**Issue**: Budget only allows essential animation
**Fix**: Prioritize primary actions. Cut secondary animations first when constrained.

### Staging
**Issue**: Limited screen real estate
**Fix**: Animate in place. Use transforms that don't affect layout. Consider reduce-motion as default on constrained platforms.

## Quick Fixes

1. **Use CSS over JavaScript** - Better browser optimization
2. **Progressive enhancement** - Core function works without animation
3. **Feature detection** - Check capability before animating
4. **Fallback states** - Static alternative for unsupported browsers
5. **Lazy load animation libraries** - Don't block initial render

## Troubleshooting Checklist

- [ ] List target browsers/devices
- [ ] Check caniuse.com for feature support
- [ ] Test on oldest supported browser
- [ ] Measure animation impact on bundle size
- [ ] Verify fallback experience is acceptable
- [ ] Test with animation disabled
- [ ] Check framework animation capabilities
- [ ] Consider server-rendered alternatives (GIF, video)

## Code Pattern

```js
// Feature detection
const supportsAnimation =
  'animate' in Element.prototype &&
  CSS.supports('transform', 'translateZ(0)');

if (supportsAnimation) {
  element.animate(keyframes, options);
} else {
  element.classList.add('final-state');
}

// Progressive enhancement
@supports (animation: name) {
  .element {
    animation: fadeIn 200ms ease-out;
  }
}
```

## Platform-Specific Tips

- **Email**: Use GIF or static images
- **iOS Safari**: Test `-webkit-` prefixes
- **Older Android**: Reduce animation complexity
- **Low-end devices**: Use `prefers-reduced-motion` as proxy
