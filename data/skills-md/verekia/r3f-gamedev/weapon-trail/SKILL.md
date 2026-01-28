---
name: weapon-trail
description: Create a ribbon trail effect that follows a weapon's movement.
---

# Weapon Trail

Create a ribbon trail effect that follows a weapon's movement.

## Technique

Build a custom `BufferGeometry` that stores a history of positions in a ring buffer. Each frame, record the current world positions of trail points and update the geometry vertices to create a ribbon connecting all historical positions.

## Key Concepts

- Define trail points (e.g., base and tip of weapon)
- Use a ring buffer to store position history efficiently
- Create geometry with proper UVs for texture mapping (gradient fade)
- Update vertex positions each frame with `positions.needsUpdate = true`
- Use `localToWorld()` to get world positions from the target object
- Support enabling/disabling with fade out animation

## Usage

```tsx
const trailPoints = [new Vector3(0, 0, 0), new Vector3(0, 1.5, 0)]

<group ref={weaponRef}>
  <mesh>{/* weapon mesh */}</mesh>
</group>
<Trail target={weaponRef} points={trailPoints} enabled={isAttacking} />
```

## Geometry Structure

- Segments: historical snapshots (oldest to newest)
- Points per segment: trail point positions at that time
- UVs: u = position along trail (0-1), v = age (0 = newest, 1 = oldest)
- Alpha map texture for gradient fade effect

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
