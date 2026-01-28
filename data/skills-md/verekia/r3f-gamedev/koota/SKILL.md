---
name: koota
description: Use Koota for data-oriented Entity Component System architecture with React bindings.
---

# Koota ECS

Use Koota for data-oriented Entity Component System architecture with React bindings.

When setting up or undertaking important changes with Koota, fetch the documentations:

https://raw.githubusercontent.com/pmndrs/koota/refs/heads/main/README.md

## Technique

Define traits (components) with `trait()`, create a world, spawn entities with traits, and query entities in systems. Use `useQuery` to reactively render entities and `useTraitEffect` to respond to trait changes.

## Key Concepts

- `trait()` defines component schemas with default values
- `world.spawn()` creates entities with traits
- `world.query()` finds entities matching traits
- `useQuery()` hook for reactive entity lists in React
- `useTraitEffect()` for responding to trait changes without re-rendering
- Systems are React components that use `useFrame` to update entities (they return `null`, not views)

## Usage

```tsx
const Position = trait({ x: 0, y: 0 })
const IsCharacter = trait()

const world = createWorld()

// Spawn
world.spawn(Position({ x: 1, y: 2 }), IsCharacter)

// Query in system
world.query(Position).updateEach(([position]) => {
  position.x += 0.01
})

// React component
const characters = useQuery(Position, IsCharacter)
```

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
