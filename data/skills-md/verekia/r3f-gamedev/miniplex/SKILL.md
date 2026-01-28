---
name: miniplex
description: Use Miniplex for minimalistic Entity Component System with TypeScript support.
---

# Miniplex ECS

Use Miniplex for minimalistic Entity Component System with TypeScript support.

When setting up or undertaking important changes with Miniplex, fetch the documentations:

Core: https://raw.githubusercontent.com/hmans/miniplex/refs/heads/main/packages/core/README.md
React bindings: https://raw.githubusercontent.com/hmans/miniplex/refs/heads/main/packages/react/README.md

## Technique

Define an entity type with optional properties, create a world, and query entities based on their properties. Use `miniplex-react` for React bindings with the `Entities` component.

## Key Concepts

- Entity type defines all possible components as optional properties
- `world.with('prop1', 'prop2')` creates typed queries
- `world.add()` and `world.remove()` for entity lifecycle
- `world.addComponent()` and `world.removeComponent()` for component lifecycle
- `<Entities in={query}>{Component}</Entities>` renders entities reactively
- Entity props are passed directly to child components

## What NOT to Use

- `onEntityAdded` / `onEntityRemoved` - Prefer using data and systems to trigger things (e.g., timers, flags)
- `.where()` - Don't use predicate-based filtering

## Preferred Methods

Only use these world methods:

- `world.add(entity)` - Add a new entity
- `world.remove(entity)` - Remove an entity
- `world.addComponent(entity, 'component', value)` - Add component to existing entity
- `world.removeComponent(entity, 'component')` - Remove component from entity
- `world.with('prop1', 'prop2')` - Create queries

## Queries

Declare queries at module level and import them where needed:

```tsx
// ecs/queries.ts
export const characterQuery = world.with('position', 'isCharacter')
export const enemyQuery = world.with('position', 'isEnemy')
export const movingEntities = world.with('position', 'velocity')

// In a system file
import { movingEntities } from './ecs/queries'
```

## Usage

```tsx
type Entity = {
  position?: { x: number; y: number }
  isCharacter?: true
}

const world = new World<Entity>()
const characters = world.with('position', 'isCharacter')

// Add entity
world.add({ position: { x: 0, y: 0 }, isCharacter: true })

// Render
<Entities in={characters}>{Character}</Entities>
```

Note: Miniplex is feature-complete but no longer maintained.

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
