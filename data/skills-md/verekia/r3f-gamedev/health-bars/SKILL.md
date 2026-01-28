---
name: health-bars
description: Display health bars above characters using CSS styling.
---

# Health Bars

Display health bars above characters using CSS styling.

## Technique

Use Drei's `Html` component to render styled health bars in 3D space. Update the health bar width by manipulating the DOM element's `transform: scaleX()` via a ref in `useFrame`.

## Key Concepts

- `Html` from `@react-three/drei` with `center` and `distanceFactor` props
- Use refs to directly manipulate DOM styles for performance
- `scaleX` transform for smooth width changes with CSS transitions
- Style with CSS (gradients, borders, skew transforms)

## Usage

```tsx
const healthRef = useRef<HTMLDivElement>(null)

useFrame(() => {
  healthRef.current.style.transform = `scaleX(${healthPercent})`
}, { fps: 1 })

<Html center position-y={1.5} distanceFactor={5}>
  <div className="bg-red-500">
    <div ref={healthRef} className="bg-green-500 origin-left transition-transform" />
  </div>
</Html>
```

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
