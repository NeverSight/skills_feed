---
name: hytopia-entities
description: Helps create and manage entities in HYTOPIA SDK games. Use when users need to create game objects, NPCs, items, or any interactive objects. Covers Entity class, spawn/despawn, components, animations, and lifecycle management.
---

# HYTOPIA Entities

This skill helps you create and manage entities in HYTOPIA SDK games.

## When to Use This Skill

Use this skill when the user:

- Wants to create game objects, NPCs, items, or interactive objects
- Needs to spawn or despawn entities
- Asks about entity components or behaviors
- Wants to animate entities or handle entity lifecycle
- Needs collision detection between entities
- Asks about player entities vs non-player entities

## Core Entity Concepts

### Creating an Entity

```typescript
import { Entity } from 'hytopia';

class MyEntity extends Entity {
  constructor() {
    super();
    // Initialize entity properties
  }
  
  onSpawn() {
    // Called when entity is spawned into the world
  }
  
  onDespawn() {
    // Called when entity is removed from the world
  }
  
  tick(deltaTime: number) {
    // Called every frame - use for continuous updates
  }
}
```

### Spawning Entities

```typescript
// Spawn an entity in the world
const entity = new MyEntity();
world.spawnEntity(entity, {
  position: { x: 0, y: 10, z: 0 },
  rotation: { x: 0, y: 0, z: 0 }
});

// Despawn when done
world.despawnEntity(entity);
```

### Entity with Model

```typescript
import { Entity, Model } from 'hytopia';

class ItemEntity extends Entity {
  constructor() {
    super();
    this.model = new Model({
      modelUri: 'models/sword.gltf',
      scale: 0.5
    });
  }
}
```

### Entity Components

```typescript
import { Entity, PhysicsComponent, HealthComponent } from 'hytopia';

class EnemyEntity extends Entity {
  constructor() {
    super();
    
    // Add physics
    this.addComponent(new PhysicsComponent({
      mass: 10,
      colliders: [/* collision shapes */]
    }));
    
    // Add health
    this.addComponent(new HealthComponent({
      maxHealth: 100,
      currentHealth: 100
    }));
  }
}
```

## Common Patterns

### Following Player

```typescript
tick(deltaTime: number) {
  const player = world.getClosestPlayer(this.position);
  if (player) {
    const direction = player.position.subtract(this.position).normalize();
    this.position.add(direction.multiply(5 * deltaTime));
  }
}
```

### Projectile Entity

```typescript
class Projectile extends Entity {
  velocity: Vector3;
  lifetime: number = 5;
  
  tick(deltaTime: number) {
    this.position.add(this.velocity.multiply(deltaTime));
    this.lifetime -= deltaTime;
    
    if (this.lifetime <= 0) {
      world.despawnEntity(this);
    }
  }
}
```

## Best Practices

1. **Always clean up** in `onDespawn()` - remove event listeners, stop sounds
2. **Use `tick()` sparingly** - expensive operations every frame hurt performance
3. **Pool reusable entities** - don't constantly spawn/despawn the same type
4. **Set proper collision layers** - use layers to filter what collides with what
5. **Network efficiently** - only sync properties that change and need to be visible to clients

## Common Mistakes to Avoid

- Don't forget to call `super()` in constructor
- Don't modify entity properties directly on the client - server is authoritative
- Don't spawn entities before world is initialized
- Don't forget to handle entity cleanup on game end
