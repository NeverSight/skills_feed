---
name: pushback
description: Make enemies flash white and rock back and forth when receiving damage.
---

# Pushback

Make enemies flash white and rock back and forth when receiving damage.

## Technique

Track pushback state with a direction vector and progress value. In `useFrame`, interpolate the position along the pushback direction using a back-and-forth curve, and change the material color to white during the effect.

## Key Concepts

- Store pushback direction (`dx`, `dy`) and progress (0 to 1)
- Use a triangle wave for back-and-forth motion: `t < 0.5 ? t * 2 : (1 - t) * 2`
- Flash material color to white during pushback
- Reset to original position and color when complete
- Direction should be opposite to the damage source (player position)

## Usage

```tsx
const pushbackRef = useRef<{ dx: number; dy: number } | null>(null)
const pushbackProgress = useRef(0)

useFrame((_, delta) => {
  if (pushbackRef.current) {
    pushbackProgress.current += delta * 8
    material.color.set('white')

    const t = pushbackProgress.current
    const offset = t < 0.5 ? t * 2 : (1 - t) * 2
    mesh.position.x = baseX + pushbackRef.current.dx * offset
  }
})
```

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
