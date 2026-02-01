---
name: bitecs
description: Comprehensive guide for using bitECS v0.4.0, a flexible, minimal, data-oriented ECS library for TypeScript. Use when building games or simulations with Entity Component System architecture, creating entity hierarchies, defining components, querying entities, or working with serialization.
---

# bitECS v0.4.0 Agent Skill

This skill provides comprehensive guidance for using bitECS, a flexible, minimal, data-oriented Entity Component System (ECS) library for TypeScript.

## When to Use This Skill

Use this skill when:
- Building games or simulations using ECS architecture
- Creating and managing entities with components
- Defining component data structures (SoA or AoS)
- Querying entities based on component composition
- Building entity hierarchies with relationships
- Implementing prefabs and entity templates
- Serializing/deserializing ECS data for networking or save systems
- Implementing observer patterns for reactive component changes
- Working with multithreaded ECS systems

## Installation

```bash
npm i bitecs
```

## Module Structure

bitECS 0.4.0 provides three modules:

| Module | Import | Purpose |
|--------|--------|---------|
| Core | `bitecs` | Main ECS toolkit |
| Serialization | `bitecs/serialization` | Binary serialization utilities |
| Legacy | `bitecs/legacy` | Backward compatibility with 0.3.x API |

---

# Core Concepts

## World

A world is a container for ECS data. Entities are created in a world and data is queried based on the existence and shape of entities in a world. Each world is independent of all others.

```ts
import { createWorld, resetWorld, deleteWorld, getAllEntities, getWorldComponents } from 'bitecs'

// Basic world creation
const world = createWorld()

// World with custom context
const world = createWorld({
    time: { delta: 0, elapsed: 0, then: 0 },
    components: {
        Position: { x: [] as number[], y: [] as number[] }
    }
})

// Shared entity index between worlds
const entityIndex = createEntityIndex()
const worldA = createWorld(entityIndex)
const worldB = createWorld(entityIndex)

// Combined: custom context + shared entity index (any order)
createWorld({ data: 1 }, entityIndex)
createWorld(entityIndex, { data: 1 })

// World utilities
resetWorld(world)                    // Reset world state
deleteWorld(world)                   // Delete world and free resources
getAllEntities(world)                // Get all entities in world
getWorldComponents(world)            // Get all registered components
```

## Entity

Entities are unique numerical identifiers (entity IDs or eids). They are unique across all worlds unless worlds share an entity index.

```ts
import {
    addEntity,
    removeEntity,
    entityExists,
    getEntityComponents,
    createEntityIndex,
    addEntityId,
    removeEntityId,
    isEntityIdAlive
} from 'bitecs'

// Basic entity operations
const eid = addEntity(world)
removeEntity(world, eid)

// Entity utilities
entityExists(world, eid)              // Check if entity exists
getEntityComponents(world, eid)       // Get all components for entity

// Direct entity index operations
const index = createEntityIndex()
const id = addEntityId(index)
removeEntityId(index, id)
isEntityIdAlive(index, id)
```

### Entity ID Recycling

Entity IDs are recycled immediately after removal:

```ts
const eid1 = addEntity(world)
const eid2 = addEntity(world)
removeEntity(world, eid1)
const eid3 = addEntity(world)
// eid1 === eid3 (recycled)
```

### Manual Entity ID Recycling (Recommended)

For more control over entity lifecycle, implement manual recycling:

```ts
const Removed = {}

const markEntityForRemoval = (world, eid) => {
    addComponent(world, eid, Removed)
}

const removeMarkedEntities = (world) => {
    for (const eid of query(world, [Removed])) {
        removeEntity(world, eid)
    }
}
```

### Entity ID Versioning

Prevents collision issues with recycled IDs by adding version numbers:

```ts
import { createEntityIndex, withVersioning, getId, getVersion, incrementVersion } from 'bitecs'

// Version bits options:
// 8 bits: 16M entities / 256 recycles
// 10 bits: 4M entities / 1K recycles
// 12 bits: 1M entities / 4K recycles (default)
// 14 bits: 262K entities / 16K recycles
// 16 bits: 65K entities / 65K recycles

const entityIndex = createEntityIndex(withVersioning(8))
const world = createWorld(entityIndex)

const eid1 = addEntity(world)
removeEntity(world, eid1)
const eid2 = addEntity(world)
// eid1 !== eid2 (different versions)

// Version utilities
getId(entityIndex, eid)              // Extract entity ID without version
getVersion(entityIndex, eid)         // Extract version from entity ID
incrementVersion(entityIndex, eid)   // Increment version of entity ID
```

**Warning**: When using versioning with TypedArrays, ensure arrays are large enough as versioned IDs can be much larger than the base entity ID.

## Component

Components are modular data containers representing specific attributes of an entity. Any valid JavaScript reference can serve as a component.

### Component Formats

```ts
// SoA with regular arrays (recommended for minimal memory footprint)
const Position = {
    x: [] as number[],
    y: [] as number[],
}

// SoA with TypedArrays (recommended for threading and eliminating memory thrash)
const Position = {
    x: new Float64Array(10000),
    y: new Float64Array(10000),
}

// AoS (performant for small shapes with < 100k objects)
const Position = [] as { x: number; y: number }[]

// Array of TypedArrays
const Position = Array.from({ length: 10000 }, () => new Float32Array(3))

// Tag component (no data)
const Flying = {}
```

### Component Operations

```ts
import {
    addComponent,
    addComponents,
    removeComponent,
    removeComponents,
    hasComponent,
    getComponent,
    setComponent,
    set,
    registerComponent,
    registerComponents
} from 'bitecs'

// Add single component
addComponent(world, eid, Position)

// Add with initial data (requires onSet observer)
addComponent(world, eid, set(Position, { x: 10, y: 20 }))

// Add multiple components
addComponents(world, eid, Position, Velocity, Mass)
addComponents(world, eid, [Position, Velocity, Mass])
addComponents(world, eid,
    set(Position, { x: 10, y: 20 }),
    set(Velocity, { x: 1, y: 1 }),
    Health
)

// Remove components
removeComponent(world, eid, Position)
removeComponent(world, eid, Position, Velocity)
removeComponents(world, eid, Position, Velocity)

// Check component presence
hasComponent(world, eid, Position)

// Get component data (triggers onGet observers)
const data = getComponent(world, eid, Position)

// Set component data (triggers onSet observers)
setComponent(world, eid, Position, { x: 10, y: 20 })

// Register components explicitly (automatic on first addComponent)
registerComponent(world, Position)
registerComponents(world, [Position, Velocity, Mass])
```

### Component Data Access

```ts
addComponent(world, eid, Position)

// SoA access
Position.x[eid] = 0
Position.y[eid] = 0
Position.x[eid] += 1

// AoS access
Position[eid] = { x: 0, y: 0 }
Position[eid].x += 1

// Array of TypedArrays
const pos = Position[eid]
pos[0] += 1
```

### Storing Components on World

```ts
// Components stored on world for clean access
const world = createWorld({
    components: {
        Position: Array(1e5).fill(3).map(n => new Float32Array(n))
    }
})

const { Position } = world.components
```

## Query

Queries retrieve entities based on their components, relationships, or hierarchies.

```ts
import { query, And, Or, Not, All, Any, None, Hierarchy, Cascade, asBuffer, isNested, noCommit } from 'bitecs'

// Basic query
const entities = query(world, [Position, Mass])

// Query operators
query(world, [Position, Velocity])                    // AND (default)
query(world, [And(Position, Velocity)])               // Explicit AND
query(world, [All(Position, Velocity)])               // Alias for AND
query(world, [Or(Position, Velocity)])                // OR
query(world, [Any(Position, Velocity)])               // Alias for OR
query(world, [Position, Not(Velocity)])               // NOT
query(world, [Position, None(Velocity)])              // Alias for NOT

// Complex combinations
query(world, [
    Position,                    // Must have Position
    Or(Health, Shield),          // Must have Health OR Shield
    Not(Stunned, Paralyzed)      // Must NOT have Stunned AND must NOT have Paralyzed
])
```

### Query Options and Modifiers

```ts
// Options object approach
query(world, [Position], { commit: false })                   // Skip pending removals
query(world, [Position], { buffered: true })                  // Returns Uint32Array
query(world, [Position], { commit: false, buffered: true })   // Combined

// Query modifier approach
query(world, [Position], isNested)                            // Safe nested iteration
query(world, [Position], noCommit)                            // Alias for isNested
query(world, [Position], asBuffer)                            // Returns Uint32Array
query(world, [Position], asBuffer, isNested)                  // Combined modifiers
```

### Nested Queries for Safe Iteration

When iterating over query results, calling another query will flush pending removals. Use `isNested` or `noCommit` for safe nested iteration:

```ts
for (const entity of query(world, [Position, Velocity])) {
    // Use nested to prevent removals during iteration
    for (const inner of query(world, [Mass], isNested)) {
        // Safe nested iteration
    }
}
```

### Hierarchical Queries

Query entities in topological order (parents before children):

```ts
import { Hierarchy, Cascade, getHierarchyDepth, getMaxHierarchyDepth } from 'bitecs'

const ChildOf = createRelation()

// All entities with Position in hierarchy order
for (const eid of query(world, [Position, Hierarchy(ChildOf)])) {
    // Parents processed before children
}

// Entities at specific depth level
for (const eid of query(world, [Position, Hierarchy(ChildOf, 2)])) {
    // Only entities at depth 2
}

// Cascade is an alias for Hierarchy
query(world, [Position, Cascade(ChildOf)])

// Hierarchy utilities
getHierarchyDepth(world, eid, ChildOf)    // Get depth of entity
getMaxHierarchyDepth(world, ChildOf)      // Get max depth in hierarchy
```

## Relationships

Relationships define how entities relate to each other.

```ts
import {
    createRelation,
    withStore,
    makeExclusive,
    withAutoRemoveSubject,
    withOnTargetRemoved,
    withValidation,
    getRelationTargets,
    Wildcard,
    Pair
} from 'bitecs'

// Basic relation
const ChildOf = createRelation()

// Relation with data store
const Contains = createRelation(
    withStore(() => ({ amount: [] as number[] }))
)
// Or with options object:
const Contains = createRelation({
    store: () => ({ amount: [] as number[] })
})

// Auto-remove subject when target is removed
const ChildOf = createRelation(withAutoRemoveSubject)
// Or: createRelation({ autoRemoveSubject: true })

// Exclusive relation (subject can only relate to one target)
const Targeting = createRelation(makeExclusive)
// Or: createRelation({ exclusive: true })

// Custom callback when target removed
const Following = createRelation(
    withOnTargetRemoved((subject, target) => {
        console.log(`${subject} lost target ${target}`)
    })
)

// Validation
const ValidatedRelation = createRelation(
    withValidation((target) => target > 0)
)
```

### Using Relationships

```ts
const inventory = addEntity(world)
const gold = addEntity(world)
const silver = addEntity(world)

// Add relationships
addComponent(world, inventory, Contains(gold))
Contains(gold).amount[inventory] = 5

addComponent(world, inventory, Contains(silver))
Contains(silver).amount[inventory] = 12

// Query relationships
const children = query(world, [ChildOf(parent)])

// Get relation targets
const targets = getRelationTargets(world, inventory, Contains)  // [gold, silver]
```

### Relationship Wildcards

```ts
// Find all entities with any Contains relationship
query(world, [Contains('*')])
query(world, [Contains(Wildcard)])

// Inverted wildcard: find all entities related TO a specific target
const earth = addEntity(world)
addComponent(world, earth, OrbitedBy(moon))
addComponent(world, earth, IlluminatedBy(sun))
query(world, [Wildcard(earth)])  // Entities related to earth

// Find all parents (entities that have children)
query(world, [Wildcard(ChildOf)])

// Find all children (entities that have parents)
query(world, [ChildOf(Wildcard)])
```

## Prefabs

Prefabs are reusable entity templates.

```ts
import { addPrefab, IsA } from 'bitecs'

// Create prefab
const Animal = addPrefab(world)
addComponent(world, Animal, Vitals)
Vitals.health[Animal] = 100

// Inheritance with IsA relation
const Sheep = addPrefab(world)
addComponent(world, Sheep, IsA(Animal))  // Inherits Vitals
addComponent(world, Sheep, Contains(Wool))

// Instantiate from prefab
const sheep = addEntity(world)
addComponent(world, sheep, IsA(Sheep))
hasComponent(world, sheep, Contains(Wool))  // true

// Query instances
query(world, [IsA(Animal)])  // Returns all animals
```

**Note**: Prefabs do not appear in queries themselves. For inheritance to work with component values, you must define `onSet` and `onGet` observers:

```ts
observe(world, onSet(Vitals), (eid, params) => {
    Vitals.health[eid] = params.health
})
observe(world, onGet(Vitals), (eid) => ({
    health: Vitals.health[eid]
}))
```

## Observers

Observers react to component changes.

```ts
import { observe, onAdd, onRemove, onSet, onGet } from 'bitecs'

// Observe component additions
const unsubscribe = observe(world, onAdd(Position), (eid) => {
    console.log(`Entity ${eid} gained Position`)
})

// Observe component removals
observe(world, onRemove(Health), (eid) => {
    console.log(`Entity ${eid} lost Health`)
})

// Complex observation patterns
observe(world, onAdd(Position, Not(Velocity)), (eid) => {
    console.log(`Entity ${eid} has Position but no Velocity`)
})

// onSet: Called when setComponent or set() helper is used
observe(world, onSet(Position), (eid, params) => {
    Position.x[eid] = params.x
    Position.y[eid] = params.y
    console.log(`Position set for ${eid}:`, params)
})

// onGet: Called when getComponent is used
observe(world, onGet(Position), (eid) => ({
    x: Position.x[eid],
    y: Position.y[eid]
}))

// Computed values
observe(world, onSet(Health), (eid, params) => {
    return { value: Math.max(0, Math.min(100, params.value)) }
})

// Network synchronization
observe(world, onSet(Inventory), (eid, params) => {
    syncWithServer(eid, 'inventory', params)
    return params
})

// Unsubscribe when done
unsubscribe()
```

## Systems

Systems define entity behavior. bitECS doesn't enforce a specific implementation, but recommends simple chainable functions:

```ts
const moveBody = (world) => {
    for (const entity of query(world, [Position, Velocity])) {
        Position.x[entity] += Velocity.x[entity] * world.time.delta
        Position.y[entity] += Velocity.y[entity] * world.time.delta
    }
}

const applyGravity = (world) => {
    const gravity = 9.81
    for (const entity of query(world, [Position, Mass])) {
        Position.y[entity] -= gravity * Mass.value[entity] * world.time.delta
    }
}

const timeSystem = (world) => {
    const now = performance.now()
    world.time.delta = (now - world.time.then) / 1000
    world.time.elapsed += world.time.delta
    world.time.then = now
}

// Game loop
const update = (world) => {
    timeSystem(world)
    moveBody(world)
    applyGravity(world)
}

// Browser
requestAnimationFrame(function animate() {
    update(world)
    requestAnimationFrame(animate)
})

// Node
setInterval(() => update(world), 1000/60)
```

---

# Serialization Module

Import from `bitecs/serialization`.

## Data Type Tags

For regular arrays, use type tags to specify serialization format:

| Tag | Description |
|-----|-------------|
| `u8()`, `i8()` | 8-bit unsigned/signed integers |
| `u16()`, `i16()` | 16-bit unsigned/signed integers |
| `u32()`, `i32()` | 32-bit unsigned/signed integers |
| `f32()` | 32-bit floats |
| `f64()` | 64-bit floats (default) |
| `str()` | UTF-8 strings |
| `array(type)` | Arrays of specified type |

TypedArrays (Uint8Array, Float32Array, etc.) don't need tags.

## SoA Serialization

For Structure of Arrays component data:

```ts
import { createSoASerializer, createSoADeserializer, f32, u8, str, array } from 'bitecs/serialization'

const Position = { x: f32([]), y: f32([]) }
const Velocity = { vx: f32([]), vy: f32([]) }
const Health = new Uint8Array(1e5)
const Meta = { name: str([]), tags: array(str) }

const components = [Position, Velocity, Health, Meta]

const serialize = createSoASerializer(components)
const deserialize = createSoADeserializer(components)

// Set data
Position.x[eid] = 10.5
Position.y[eid] = 20.2
Health[eid] = 100
Meta.name[eid] = 'Player'
Meta.tags[eid] = ['hero', 'active']

// Serialize entities
const buffer = serialize([eid])

// Deserialize
deserialize(buffer)

// ID mapping for network/save systems
const idMap = new Map([[1, 10]])  // Map entity 1 to 10
deserialize(buffer, idMap)
```

### Serializer Options

```ts
const serialize = createSoASerializer(components, {
    diff: true,                          // Only serialize changed values
    buffer: new ArrayBuffer(1 << 20),    // 1MB backing buffer (default: 100MB)
    epsilon: 1e-3                         // Float comparison threshold (default: 0.0001)
})

const deserialize = createSoADeserializer(components, { diff: true })
```

### Nested Arrays

```ts
const Inventory = {
    pages: array(array(u8))  // Array of arrays of u8
}

Inventory.pages[eid] = [
    [1, 2, 3],      // Page 1
    [10, 20],       // Page 2
    [100, 101, 102] // Page 3
]
```

## AoS Serialization

For Array of Structures component data:

```ts
import { createAoSSerializer, createAoSDeserializer, f32, u8, str, array } from 'bitecs/serialization'

const Position = Object.assign([], { x: f32(), y: f32() })
const Health = u8()
const Meta = Object.assign([], { name: str(), tags: array(str) })

const serialize = createAoSSerializer(components, { diff: true })
const deserialize = createAoSDeserializer(components, { diff: true })

const buffer = serialize([0, 1])

// ID mapping
const idMap = new Map([[0, 10], [1, 11]])
deserialize(buffer, idMap)
```

## Observer Serialization

Tracks entity/component additions and removals:

```ts
import { createObserverSerializer, createObserverDeserializer } from 'bitecs/serialization'

const Networked = {}  // Tag component for network entities

const serializer = createObserverSerializer(world, Networked, [Position, Health], {
    buffer: new ArrayBuffer(1 << 20)  // Optional backing buffer
})

const deserializer = createObserverDeserializer(world, Networked, [Position, Health], {
    idMap: new Map()  // Optional initial ID mapping
})

// Add components
addComponent(world, eid, Networked)
addComponent(world, eid, Position)
addComponent(world, eid, Health)

// Serialize changes
const buffer = serializer()

// Deserialize on receiver
deserializer(buffer)
// Or with override ID map
deserializer(buffer, new Map([[1, 100]]))
```

## Snapshot Serialization

Captures complete world state:

```ts
import { createSnapshotSerializer, createSnapshotDeserializer, f32, u8 } from 'bitecs/serialization'

const Position = { x: f32([]), y: f32([]) }
const Health = u8([])

const serialize = createSnapshotSerializer(world, [Position, Health])
const deserialize = createSnapshotDeserializer(world, [Position, Health])

// Capture full state
const buffer = serialize()

// Restore state
deserialize(buffer)
// Or with ID mapping
deserialize(buffer, new Map([[1, 10]]))
```

---

# Multithreading

bitECS is designed to work efficiently with worker threads.

## SharedArrayBuffer Components

```ts
const MAX_ENTS = 1e6
const world = createWorld({
    components: {
        Position: {
            x: new Float32Array(new SharedArrayBuffer(MAX_ENTS * Float32Array.BYTES_PER_ELEMENT)),
            y: new Float32Array(new SharedArrayBuffer(MAX_ENTS * Float32Array.BYTES_PER_ELEMENT))
        }
    }
})
```

## Query with asBuffer

Returns SAB-backed Uint32Array for thread sharing:

```ts
const entities = query(world, [Position, Mass], asBuffer)
```

## Worker Communication Pattern

```ts
// Main thread
const worker = new Worker('./worker.js')

worker.postMessage({
    entities: query(world, [world.components.Position], asBuffer),
    components: world.components
})

worker.on('message', ({ removeQueue }) => {
    for (let i = 0; i < removeQueue.length; i++) {
        removeEntity(world, removeQueue[i])
    }
})

// Worker thread (worker.js)
const MAX_CMDS = 1e6
const removeQueue = new Uint32Array(new SharedArrayBuffer(MAX_CMDS * Uint32Array.BYTES_PER_ELEMENT))

self.onmessage = ({ data }) => {
    const { entities, components: { Position } } = data
    let removeCount = 0

    for (let i = 0; i < entities.length; i++) {
        const eid = entities[i]
        Position.x[eid] += 1
        Position.y[eid] += 1
        removeQueue[removeCount++] = eid
    }

    self.postMessage({ removeQueue: removeQueue.subarray(0, removeCount) })
}
```

## Parallel Processing Pattern

```ts
const WORKER_COUNT = 4
const workers = Array(WORKER_COUNT).fill(null).map(() => new Worker('worker.js'))

let completedWorkers = 0
workers.forEach(worker => worker.on('message', () => {
    completedWorkers++
    if (completedWorkers === WORKER_COUNT) {
        processQueues()
        completedWorkers = 0
    }
}))

function processEntitiesParallel(world) {
    const entities = query(world, [Position], asBuffer)
    const partitionSize = Math.ceil(entities.length / WORKER_COUNT)

    for (let i = 0; i < WORKER_COUNT; i++) {
        const start = i * partitionSize
        const end = Math.min(start + partitionSize, entities.length)
        workers[i].postMessage({
            entities: entities.subarray(start, end),
            components: world.components
        })
    }
}
```

**Important**: ECS API functions (addEntity, removeEntity, addComponent, etc.) cannot be used directly in workers. Use message queues to send commands back to the main thread.

---

# Complete API Reference

## World Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `createWorld` | `(context?, entityIndex?) => World` | Create a new world |
| `resetWorld` | `(world) => World` | Reset world state |
| `deleteWorld` | `(world) => void` | Delete world and free resources |
| `getAllEntities` | `(world) => number[]` | Get all entities in world |
| `getWorldComponents` | `(world) => ComponentRef[]` | Get all registered components |

## Entity Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `addEntity` | `(world) => number` | Add new entity |
| `removeEntity` | `(world, eid) => void` | Remove entity |
| `entityExists` | `(world, eid) => boolean` | Check if entity exists |
| `getEntityComponents` | `(world, eid) => ComponentRef[]` | Get entity's components |

## Entity Index Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `createEntityIndex` | `(options?) => EntityIndex` | Create entity index |
| `withVersioning` | `(versionBits?) => options` | Configure versioning |
| `addEntityId` | `(index) => number` | Add ID to index |
| `removeEntityId` | `(index, id) => void` | Remove ID from index |
| `isEntityIdAlive` | `(index, id) => boolean` | Check if ID is alive |
| `getId` | `(index, id) => number` | Extract entity ID |
| `getVersion` | `(index, id) => number` | Extract version |
| `incrementVersion` | `(index, id) => number` | Increment version |

## Component Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `addComponent` | `(world, eid, component) => boolean` | Add component to entity |
| `addComponents` | `(world, eid, ...components) => void` | Add multiple components |
| `removeComponent` | `(world, eid, ...components) => void` | Remove components |
| `removeComponents` | `(world, eid, ...components) => void` | Alias for removeComponent |
| `hasComponent` | `(world, eid, component) => boolean` | Check component presence |
| `getComponent` | `(world, eid, component) => any` | Get component data |
| `setComponent` | `(world, eid, component, data) => void` | Set component data |
| `set` | `(component, data) => ComponentSetter` | Create component setter |
| `registerComponent` | `(world, component) => ComponentData` | Register component |
| `registerComponents` | `(world, components) => void` | Register multiple |

## Query Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `query` | `(world, terms, ...modifiers) => QueryResult` | Query entities |
| `And` / `All` | `(...components) => OpReturnType` | AND operator |
| `Or` / `Any` | `(...components) => OpReturnType` | OR operator |
| `Not` / `None` | `(...components) => OpReturnType` | NOT operator |
| `Hierarchy` / `Cascade` | `(relation, depth?) => HierarchyTerm` | Hierarchy ordering |
| `asBuffer` | `QueryModifier` | Return Uint32Array |
| `isNested` / `noCommit` | `QueryModifier` | Safe nested iteration |
| `commitRemovals` | `(world) => void` | Commit pending removals |
| `registerQuery` | `(world, terms, options?) => Query` | Register query |
| `removeQuery` | `(world, terms) => void` | Remove query |

## Hierarchy Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `getHierarchyDepth` | `(world, eid, relation) => number` | Get entity depth |
| `getMaxHierarchyDepth` | `(world, relation) => number` | Get max depth |
| `ensureDepthTracking` | `(world, relation) => void` | Initialize tracking |

## Relation Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `createRelation` | `(...modifiers) => Relation` | Create relation |
| `withStore` | `(createStore) => modifier` | Add data store |
| `makeExclusive` | `(relation) => Relation` | Make exclusive |
| `withAutoRemoveSubject` | `(relation) => Relation` | Auto-remove subject |
| `withOnTargetRemoved` | `(callback) => modifier` | Target removed callback |
| `withValidation` | `(validateFn) => modifier` | Add validation |
| `getRelationTargets` | `(world, eid, relation) => number[]` | Get targets |
| `Pair` | `(relation, target) => component` | Create pair |
| `Wildcard` | `Relation` | Wildcard relation |
| `IsA` | `Relation` | Inheritance relation |
| `isRelation` | `(component) => boolean` | Check if relation |
| `isWildcard` | `(relation) => boolean` | Check if wildcard |

## Prefab Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `addPrefab` | `(world) => EntityId` | Create prefab entity |

## Observer Functions

| Function | Signature | Description |
|----------|-----------|-------------|
| `observe` | `(world, hook, callback) => unsubscribe` | Subscribe to changes |
| `onAdd` | `(...terms) => ObservableHook` | Addition hook |
| `onRemove` | `(...terms) => ObservableHook` | Removal hook |
| `onSet` | `(component) => ObservableHook` | Set hook |
| `onGet` | `(component) => ObservableHook` | Get hook |

## Serialization Functions (bitecs/serialization)

| Function | Signature | Description |
|----------|-----------|-------------|
| `createSoASerializer` | `(components, options?) => (entities) => ArrayBuffer` | SoA serializer |
| `createSoADeserializer` | `(components, options?) => (buffer, idMap?) => void` | SoA deserializer |
| `createAoSSerializer` | `(components, options?) => (entities) => ArrayBuffer` | AoS serializer |
| `createAoSDeserializer` | `(components, options?) => (buffer, idMap?) => void` | AoS deserializer |
| `createObserverSerializer` | `(world, tag, components, options?) => () => ArrayBuffer` | Observer serializer |
| `createObserverDeserializer` | `(world, tag, components, options?) => (buffer, idMap?) => void` | Observer deserializer |
| `createSnapshotSerializer` | `(world, components, buffer?) => () => ArrayBuffer` | Snapshot serializer |
| `createSnapshotDeserializer` | `(world, components) => (buffer, idMap?) => void` | Snapshot deserializer |
| `f32`, `f64`, `u8`, `u16`, `u32`, `i8`, `i16`, `i32` | `(array?) => TypedArray` | Type tags |
| `str` | `(array?) => string[]` | String type tag |
| `array` | `(type) => array` | Array type tag |

---

# Best Practices

## Component Design

1. **Prefer SoA format** for optimal cache performance and memory efficiency
2. **Use TypedArrays** for threading compatibility and predictable memory
3. **Keep components small and focused** on a single concern
4. **Use tag components** (empty objects) for boolean flags
5. **Pre-allocate TypedArrays** based on expected entity count

```ts
// Good: Focused components
const Position = { x: new Float32Array(MAX_ENTS), y: new Float32Array(MAX_ENTS) }
const Velocity = { x: new Float32Array(MAX_ENTS), y: new Float32Array(MAX_ENTS) }
const Flying = {}  // Tag

// Avoid: Monolithic components
const Entity = { x: [], y: [], vx: [], vy: [], health: [], name: [] }
```

## Query Optimization

1. **Query once per system**, iterate results
2. **Use `isNested` for nested queries** to prevent removal issues
3. **Use `asBuffer` for threading** or when you need Uint32Array
4. **Avoid querying in tight loops**

```ts
// Good: Query once
const moveSystem = (world) => {
    const entities = query(world, [Position, Velocity])
    for (const eid of entities) {
        Position.x[eid] += Velocity.x[eid]
    }
}

// Avoid: Query in loop
for (let i = 0; i < 1000; i++) {
    const entities = query(world, [Position])  // Inefficient
}
```

## Entity Lifecycle

1. **Use manual recycling** for controlled removal timing
2. **Consider versioning** if entity ID reuse causes issues
3. **Batch entity removals** for better performance

```ts
const Removed = {}
const removeSystem = (world) => {
    for (const eid of query(world, [Removed])) {
        removeEntity(world, eid)
    }
}
```

## Observer Usage

1. **Use observers for cross-cutting concerns** (logging, sync, validation)
2. **Keep observer callbacks lightweight**
3. **Unsubscribe when no longer needed**
4. **Define onSet/onGet for prefab inheritance**

## Serialization

1. **Use Observer + SoA serializers together** for complete network sync
2. **Pre-allocate serialization buffers** to avoid GC pressure
3. **Use diff mode** for bandwidth-sensitive applications
4. **Map entity IDs** when deserializing to different worlds

## Threading

1. **Use SharedArrayBuffer** for cross-thread component stores
2. **Use `asBuffer` queries** for thread-safe entity lists
3. **Implement command queues** for main thread operations
4. **Partition work** across workers for parallel processing

---

# Migration from 0.3.x

## Key Changes

| 0.3.x | 0.4.0 |
|-------|-------|
| `defineComponent({ x: Types.f32 })` | `{ x: [] as number[] }` or `{ x: new Float32Array(n) }` |
| `addComponent(world, Component, eid)` | `addComponent(world, eid, Component)` |
| `defineQuery([A, B])` then `query(world)` | `query(world, [A, B])` |
| `enterQuery(query)` | `observe(world, onAdd(...), cb)` |
| `exitQuery(query)` | `observe(world, onRemove(...), cb)` |
| `Changed(Component)` | `observe(world, onSet(Component), cb)` |
| `Types.eid` for references | `createRelation()` |

## Legacy Module

For gradual migration, use `bitecs/legacy`:

```ts
import {
    defineComponent,
    defineQuery,
    enterQuery,
    exitQuery,
    Types,
    addComponent  // Uses old parameter order
} from 'bitecs/legacy'
```

---

# Common Patterns

## Enter/Exit Queues

```ts
const world = createWorld({
    enteredMovers: [] as number[],
    exitedMovers: [] as number[]
})

observe(world, onAdd(Position, Velocity), (eid) => world.enteredMovers.push(eid))
observe(world, onRemove(Position, Velocity), (eid) => world.exitedMovers.push(eid))

const movementSystem = (world) => {
    // Process entered
    for (const eid of world.enteredMovers.splice(0)) {
        console.log(`${eid} started moving`)
    }

    // Process exited
    for (const eid of world.exitedMovers.splice(0)) {
        console.log(`${eid} stopped moving`)
    }
}
```

## Parent-Child Hierarchies

```ts
const ChildOf = createRelation(withAutoRemoveSubject)

// Create hierarchy
const parent = addEntity(world)
const child = addEntity(world)
addComponent(world, child, ChildOf(parent))

// Process in order
for (const eid of query(world, [Transform, Hierarchy(ChildOf)])) {
    // Parents processed before children
    updateWorldTransform(eid)
}
```

## Inventory System

```ts
const Contains = createRelation(withStore(() => ({ amount: [] as number[] })))

const chest = addEntity(world)
const gold = addEntity(world)

addComponent(world, chest, Contains(gold))
Contains(gold).amount[chest] = 100

// Get all items in chest
const items = getRelationTargets(world, chest, Contains)
```

## Network Replication

```ts
import { createObserverSerializer, createObserverDeserializer, createSoASerializer, createSoADeserializer } from 'bitecs/serialization'

const Networked = {}
const components = [Position, Velocity, Health]

// Server
const observerSerializer = createObserverSerializer(world, Networked, components)
const dataSerializer = createSoASerializer(components)

const sendUpdate = () => {
    const entities = query(world, [Networked])
    const observerPacket = observerSerializer()
    const dataPacket = dataSerializer(entities)
    broadcast({ observer: observerPacket, data: dataPacket })
}

// Client
const observerDeserializer = createObserverDeserializer(world, Networked, components)
const dataDeserializer = createSoADeserializer(components)

const receiveUpdate = ({ observer, data }) => {
    observerDeserializer(observer)
    dataDeserializer(data)
}
```
