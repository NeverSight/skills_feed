---
name: verekia-architecture
description: Day-to-day coding style and patterns for R3F game development with Miniplex ECS.
---

# Architecture

The core principle of R3F game development is separating game logic from rendering. React components are views, not the source of truth.

## Systems vs Views

**Systems** contain all game logic:

- Movement, physics, collision detection
- Spawning and destroying entities
- State mutations (health, score, timers)
- AI and behavior
- Syncing Three.js objects with entity state

**Views** (React components) only render:

- `<PlayerEntity>`, `<EnemyEntity>` wrap models with `ModelContainer`, process any data needed and pass it as props to the model
- `<PlayerModel>`, `<EnemyModel>` are dumb and only render meshes via props
- They don't contain core game logic, just visuals logic
- No `useFrame` in view components unless it is purely visual and should not be part of the core logic

## Headless-First Mindset

Games should be capable of running entirely without a renderer:

```
┌─────────────────────────────────────────┐
│            Game Logic Layer             │
│  (Systems, ECS, World State, Entities)  │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│            View Layer (optional)        │
│   React Three Fiber / DOM / Headless    │
└─────────────────────────────────────────┘
```

This means:

- All state lives in the world/ECS, not in React components
- Systems iterate over entities and mutate state
- Views subscribe to state and render accordingly
- You could swap R3F for DOM elements or run tests headlessly

## Miniplex: What NOT to Use

**From miniplex-react:**

- `ECS.Entity` - Don't use this component
- `ECS.Component` - Don't use this component
- `ECS.world` - Don't access world through ECS, use direct import
- `useEntities` hook - Don't use this
- Render props pattern - Don't use this

**From miniplex core:**

- `onEntityAdded` / `onEntityRemoved` - Prefer using data and systems to trigger things (e.g., timers, flags)
- `.where()` - Don't use predicate-based filtering, prefer iterating over all entities that have the component no matter its value. For example iterate over all entities that have health and filter out entities that have health < 0 in the system rather than querying entities where health < 0 (which would require reindexing).

## Miniplex: Preferred Methods

Only use these:

- `world.add(entity)` - Add a new entity
- `world.remove(entity)` - Remove an entity
- `world.addComponent(entity, 'component', value)` - Add component to existing entity
- `world.removeComponent(entity, 'component')` - Remove component from entity
- `world.with('prop1', 'prop2')` - Create queries
- `createReactAPI(world)` - Get `Entities` component for rendering

## Entity Types and Queries

```tsx
// lib/ecs.ts
import { World } from 'miniplex'
import createReactAPI from 'miniplex-react'

type Entity = {
  position?: { x: number; y: number; z: number }
  velocity?: { x: number; y: number; z: number }
  isCharacter?: true
  isEnemy?: true
  three?: Object3D | null
}

export const world = new World<Entity>()

export const characterQuery = world.with('position', 'isCharacter', 'three')
export type CharacterEntity = (typeof characterQuery)['entities'][number]

// Only destructure Entities from React API
export const { Entities } = createReactAPI(world)
```

## ModelContainer Pattern

Capture Three.js object references on entities using a wrapper component, allowing systems to manipulate objects directly.

Similar to the Redux container/component pattern:

- **`*Entity`** components are smart wrappers that connect entity data to the view
- **`*Model`** components are dumb and only responsible for rendering

```
┌─────────────────────────────────────────┐
│  PlayerEntity (smart)                   │
│  - Wraps with ModelContainer            │
│  - Passes entity data as props          │
│                                         │
│    ┌─────────────────────────────────┐  │
│    │  PlayerModel (dumb)             │  │
│    │  - Pure rendering               │  │
│    │  - Receives props               │  │
│    │  - No knowledge of entities     │  │
│    └─────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

- Ref callback stores the Three.js object on the entity
- Cleanup function removes the reference when unmounted
- Systems access `entity.three` directly in `useFrame`
- Models are reusable and testable in isolation

## Entity as Props Pattern

The component passed to `<Entities>` receives the entity directly as props:

```tsx
// Dumb component - only renders, no entity knowledge
const CharacterModel = () => (
  <mesh>
    <sphereGeometry />
    <meshBasicMaterial color="blue" />
  </mesh>
)

// Smart wrapper - connects entity to model via ModelContainer
const CharacterEntity = (entity: CharacterEntity) => (
  <ModelContainer entity={entity}>
    <CharacterModel />
  </ModelContainer>
)

// entities/entities.tsx (contains <Entities> for all renderable entities)

const isCharacterQuery = world.with('isCharacter')

export const CharacterEntities = () => (
  <Entities in={isCharacterQuery}>{CharacterEntity}</Entities>
)
```

## Systems and Queries

### Query Placement

Define queries **near where they are used** (in the system file), not in a central file. But define them **outside the loop** at module scope:

```tsx
import { world } from '@/lib/ecs'

// ✅ Query defined at module scope, near where it's used
const movingEntities = world.with('position', 'velocity')
type MovingEntity = (typeof movingEntities)['entities'][number]
```

### One + System Pattern

Split logic into a **"One" function** (operates on a single entity) and the **system** (iterates and calls One):

```tsx
import { world } from '@/lib/ecs'

// Query at module scope
const movingEntities = world.with('position', 'velocity')
type MovingEntity = (typeof movingEntities)['entities'][number]

// "One" function - single entity logic, easy to test
const velocityOne = (e: MovingEntity, dt: number) => {
  e.position.x += e.velocity.x * dt
  e.position.y += e.velocity.y * dt
  e.position.z += e.velocity.z * dt
}

// System - just iteration
export const VelocitySystem = () => {
  useFrame((_, dt) => {
    for (const e of movingEntities) {
      velocityOne(e, dt)
    }
  })

  return null
}
```

### Query by Components, Not Types

Systems must iterate over queries tailored to their specific needs, not over entity types:

```tsx
// ✅ GOOD - Query targets entities with the components the system needs
const entitiesWithVelocity = world.with('position', 'velocity')

const VelocitySystem = () => {
  useFrame((_, delta) => {
    for (const entity of entitiesWithVelocity) {
      entity.position.x += entity.velocity.x * delta
    }
  })
  return null
}

// ❌ BAD - Iterating over specific entity types
const VelocitySystem = () => {
  useFrame((_, delta) => {
    for (const player of players) { /* ... */ }
    for (const enemy of enemies) { /* ... */ }
    for (const projectile of projectiles) { /* ... */ }
  })
  return null
}
```

The point of an ECS is that systems operate on a subset of entities matching exactly what they need. A `VelocitySystem` targets entities with `velocity`, not "players + enemies + projectiles".

### ThreeSystem - Syncing Three.js

```tsx
const threeEntities = world.with('position', 'three')
type ThreeEntity = (typeof threeEntities)['entities'][number]

const threeOne = (e: ThreeEntity) => {
  e.three.position.set(e.position.x, e.position.y, e.position.z)
}

export const ThreeSystem = () => {
  useFrame(() => {
    for (const e of threeEntities) {
      threeOne(e)
    }
  })

  return null
}
```

### Spawning Entities

```tsx
const SpawnSystem = () => {
  useEffect(() => {
    world.add({ position: { x: 0, y: 0, z: 0 }, isCharacter: true })
  }, [])

  return null
}
```

## Zustand Store Usage

Zustand stores are for state that doesn't belong in the ECS. Each store has a consistent API pattern:

```tsx
// In React components (reactive)
const areSettingsOpen = useUI('areSettingsOpen')

// Outside React / in systems (non-reactive)
const settings = getUI().areSettingsOpen

// Setting values
setUI('areSettingsOpen', true)
setUI({ areSettingsOpen: true, debug: { drawCalls: 100 } })

// Reset to defaults
resetUI()
```

- `use*` hooks for reactive access in React components
- `get*` for non-reactive access in systems or callbacks
- `set*` supports both single key-value and partial state updates
- `reset*` restores default state
- Attach `get*` to `window` for debugging in browser console
- Use `structuredClone(defaultState)` to avoid mutation issues

## Key Principles

- **R3F imports from WebGPU entry**: Always import from `@react-three/fiber/webgpu`, not `@react-three/fiber`
- **No `useFrame` in view components**: Most `useFrame` calls belong in systems
- **Entity/Model separation**: `*Entity` components are smart wrappers, `*Model` components are dumb renderers
- **Systems sync Three.js**: Systems update both entity state AND `entity.three` positions/rotations
- **Decouple completely**: The game should work if you delete all view components
- **Query by components, not types**: Systems iterate over queries based on required components
- **World and queries are plain module exports**: Not React context
- **`<Entities>` is the only React bridge**: Only use this from miniplex-react
- **Derive typed entities from queries**: `(typeof query)['entities'][number]`
- **Define queries near where they're used**: In the system file, at module scope
- **Split system logic**: "One" function for single entity, System for iteration

---

This skill is part of [verekia](https://x.com/verekia)'s [**r3f-gamedev**](https://github.com/verekia/r3f-gamedev).
