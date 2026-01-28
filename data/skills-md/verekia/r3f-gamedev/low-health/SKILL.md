---
name: low-health
description: Display a pulsing red vignette overlay when the player's health is low.
---

# Low Health

Display a pulsing red vignette overlay when the player's health is low.

## Technique

Use a full-screen fixed div with `box-shadow: inset` to create a red vignette effect. Animate the opacity with CSS keyframes for a pulsing effect.

## Key Concepts

- Fixed positioning with `inset-0` to cover the entire screen
- `pointer-events-none` to allow clicking through the overlay
- Inset box shadow creates the vignette: `inset 0 0 160px 40px red`
- CSS animation for pulsing: `animate-[low-health-opacity_0.5s_ease-in-out_infinite_alternate]`

## Usage

```tsx
<div
  className="pointer-events-none fixed inset-0 animate-[low-health-opacity_0.5s_ease-in-out_infinite_alternate]"
  style={{ boxShadow: 'inset 0 0 160px 40px red' }}
/>
```

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
