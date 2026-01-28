---
name: smooth-interpolation
description: Animate values smoothly using exponential decay instead of linear interpolation.
---

# Smooth Interpolation

Animate values smoothly using exponential decay instead of linear interpolation.

## Technique

Use exponential smoothing formulas to interpolate between current and target values. This creates a natural easing effect that's frame-rate independent.

## Key Concepts

- Exponential smoothing: `(target - current) * (1 - Math.exp(-speed * dt))`
- Exponential decay: `target + (current - target) * Math.exp(-decay * dt)`
- Both formulas produce the same result with different parameters
- Speed/decay values from 1-25 work well
- Frame-rate independent due to delta time usage

## Usage

```tsx
const addSmoothExp = (current: number, target: number, speed: number, dt: number) =>
  (target - current) * (1 - Math.exp(-speed * dt))

const expDecay = (current: number, target: number, decay: number, dt: number) =>
  target + (current - target) * Math.exp(-decay * dt)

useFrame((_, delta) => {
  mesh.position.x += addSmoothExp(mesh.position.x, targetX, 3, delta)
  // or
  mesh.position.x = expDecay(mesh.position.x, targetX, 3, delta)
})
```

## References

- [Exponential Smoothing](https://lisyarus.github.io/blog/posts/exponential-smoothing.html)
- [Lerp Smoothing is Broken](https://www.youtube.com/watch?v=LSNQuFEDOyQ)

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
