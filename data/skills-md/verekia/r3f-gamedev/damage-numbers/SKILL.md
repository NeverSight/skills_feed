---
name: damage-numbers
description: Display floating damage numbers that animate upward and fade out, with support for critical hits.
---

# Damage Numbers

Display floating damage numbers that animate upward and fade out, with support for critical hits.

## Technique

Use Drei's `Html` component to render DOM elements in 3D space. Manage damage numbers in React state, spawn them with random positions, and use CSS animations for the floating/fading effect.

## Key Concepts

- `Html` from `@react-three/drei` for DOM-in-3D rendering
- Track damages in state with unique IDs for keying
- Use `setTimeout` to remove damages after animation completes
- CSS keyframe animations for movement and opacity
- Critical hits can have different styling (larger text, "CRIT" label)

## Usage

```tsx
<Html center position={[damage.x, damage.y, 0]}>
  <div style={{ animation: 'damageNumber 1.3s ease-out forwards' }}>{damage.value}</div>
</Html>
```

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
