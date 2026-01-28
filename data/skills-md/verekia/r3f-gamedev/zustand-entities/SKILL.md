---
name: zustand-entities
description: Use Zustand as a simple state store for entity management (not a true ECS).
---

# Zustand Entities

Use Zustand as a simple state store for entity management.

## Technique

Store entities in a Zustand store array. Systems read from the store directly (non-reactively) in `useFrame`, while React components subscribe to the store for re-rendering when entities are added or removed.

## Key Concepts

- Not a true ECS, but simple and effective for many cases
- Store entities in an array with `create()`
- Use `getState()` in systems for non-reactive access (no re-renders)
- Use `useStore(selector)` in components for reactive updates
- Memoize entity components to prevent unnecessary re-renders
- Re-renders happen when entities are added/removed from the array

## Usage

```tsx
const useWorldStore = create(() => ({
  characters: [] as CharacterEntity[],
}))

// In systems (non-reactive)
useFrame(() => {
  for (const char of useWorldStore.getState().characters) {
    char.position.x += 0.01
  }
})

// In React (reactive)
const characters = useWorldStore(s => s.characters)
return characters.map(c => <Character key={c.id} entity={c} />)
```

## Trade-offs

- Simple to understand and implement
- No automatic querying - must manually specify which entities to iterate
- Good for smaller games or prototypes

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
