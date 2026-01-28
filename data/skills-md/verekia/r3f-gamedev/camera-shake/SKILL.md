---
name: camera-shake
description: Shake the camera when the player takes damage or on impacts for visual feedback.
---

# Camera Shake

Shake the camera when the player takes damage or on impacts for visual feedback.

## Technique

Instantly offset the camera's rotation on X (pitch) and Z (roll) axes, then smoothly return to the base rotation using exponential decay in `useFrame`.

## Key Concepts

- Store rotation offsets in a module-level object for external triggering
- Use exponential smoothing: `(target - current) * (1 - Math.exp(-speed * dt))`
- Apply offsets to `camera.rotation.x` and `camera.rotation.z`
- Call `shake(intensity)` from anywhere to trigger the effect

## Usage

```tsx
const shake = (intensity = 0.05) => {
  rotationOffset.x = (Math.random() - 0.5) * intensity
  rotationOffset.z = (Math.random() - 0.5) * intensity
}

// In useFrame:
rotationOffset.x += addSmoothExp(rotationOffset.x, 0, 10, delta)
camera.rotation.x = rotationOffset.x
```

## Related Skills

- `smooth-interpolation` - Exponential smoothing formula details

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
