---
name: web-motion-design
description: Use when building CSS animations, JavaScript transitions, React/Vue motion, or any browser-based animation work.
---

# Web Motion Design

Apply Disney's 12 animation principles to CSS, JavaScript, and frontend frameworks.

## Quick Reference

| Principle | Web Implementation |
|-----------|-------------------|
| Squash & Stretch | `transform: scale()` on interaction states |
| Anticipation | Slight reverse movement before action |
| Staging | Focus user attention with motion hierarchy |
| Straight Ahead / Pose to Pose | JS frame-by-frame vs CSS keyframes |
| Follow Through / Overlapping | Staggered child animations, elastic easing |
| Slow In / Slow Out | `ease-in-out`, cubic-bezier curves |
| Arc | `motion-path` or bezier translate transforms |
| Secondary Action | Shadows, glows responding to primary motion |
| Timing | Duration: micro 100-200ms, standard 200-400ms |
| Exaggeration | Scale beyond 1.0, overshoot animations |
| Solid Drawing | Consistent transform-origin, 3D perspective |
| Appeal | Smooth 60fps, purposeful motion design |

## Principle Applications

**Squash & Stretch**: Apply `scaleY` compression on button press, `scaleX` stretch on hover. Keep volume constant—if you compress Y, expand X slightly.

**Anticipation**: Before expanding a dropdown, shrink it 2-3% first. Before sliding content left, move it 5px right.

**Staging**: Dim background elements during modal focus. Use motion to direct eye flow—animate important elements first.

**Straight Ahead vs Pose to Pose**: Use CSS `@keyframes` for predictable, repeatable animations (pose to pose). Use JavaScript/GSAP for dynamic, physics-based motion (straight ahead).

**Follow Through & Overlapping**: Child elements should complete movement after parent stops. Use `animation-delay` with decreasing values for natural stagger.

**Slow In / Slow Out**: Never use `linear` for UI motion. Standard easing: `cubic-bezier(0.4, 0, 0.2, 1)`. Enter: `cubic-bezier(0, 0, 0.2, 1)`. Exit: `cubic-bezier(0.4, 0, 1, 1)`.

**Arc**: Elements in nature move in arcs, not straight lines. Use `offset-path` or combine X/Y transforms with different easings.

**Secondary Action**: Button shadow grows/blurs on hover. Icon inside button rotates while button scales. Background particles respond to primary element.

**Timing**: Micro-interactions: 100-200ms. Standard transitions: 200-400ms. Complex sequences: 400-700ms. Page transitions: 300-500ms.

**Exaggeration**: Hover states scale to 1.05-1.1, not 1.01. Error shakes move 10-20px, not 2px. Make motion noticeable but not jarring.

**Solid Drawing**: Maintain consistent `transform-origin`. Use `perspective` for 3D depth. Avoid conflicting transforms that create visual glitches.

**Appeal**: Target 60fps—use `transform` and `opacity` only when possible. Add subtle personality through custom easing curves. Motion should feel intentional.

## Code Patterns

```css
/* Elastic button with squash/stretch */
.button:active {
  transform: scale(0.95, 1.05);
  transition: transform 100ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* Anticipation before expansion */
.dropdown-enter {
  animation: dropdown-open 300ms cubic-bezier(0.34, 1.56, 0.64, 1);
}

@keyframes dropdown-open {
  0% { transform: scaleY(0.98); opacity: 0; }
  100% { transform: scaleY(1); opacity: 1; }
}
```

## Performance Rules

1. Animate only `transform` and `opacity` for GPU acceleration
2. Use `will-change` sparingly and remove after animation
3. Prefer CSS over JavaScript when animation is predictable
4. Test on low-powered devices
