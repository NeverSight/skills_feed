---
name: hytopia-physics
description: Helps implement physics and collision in HYTOPIA SDK games. Use when users need rigid bodies, collision detection, raycasting, forces, or physics-based gameplay. Covers PhysicsComponent, colliders, raycasting, and physics simulation.
---

# HYTOPIA Physics & Collision

This skill helps you implement physics and collision in HYTOPIA SDK games.

## When to Use This Skill

Use this skill when the user:

- Wants to add physics to entities (gravity, velocity, forces)
- Needs collision detection between objects
- Asks about raycasting for hit detection
- Wants to create physics-based gameplay (projectiles, explosions)
- Needs to configure colliders (boxes, spheres, meshes)
- Asks about physics materials (friction, bounciness)

## Core Physics Concepts

### Adding Physics to Entity

```typescript
import { Entity, PhysicsComponent, BoxCollider } from 'hytopia';

class PhysicsEntity extends Entity {
  constructor() {
    super();
    
    this.addComponent(new PhysicsComponent({
      mass: 1.0,           // Kilograms
      gravity: { x: 0, y: -9.81, z: 0 },
      linearDamping: 0.1,  // Air resistance
      angularDamping: 0.1,
      useGravity: true
    }));
    
    // Add collision shape
    this.addComponent(new BoxCollider({
      size: { x: 1, y: 1, z: 1 },
      offset: { x: 0, y: 0.5, z: 0 }
    }));
  }
}
```

### Collider Types

```typescript
import { BoxCollider, SphereCollider, MeshCollider } from 'hytopia';

// Box collider
const box = new BoxCollider({
  size: { x: 2, y: 1, z: 0.5 },
  offset: { x: 0, y: 0, z: 0 }
});

// Sphere collider
const sphere = new SphereCollider({
  radius: 0.5,
  offset: { x: 0, y: 0.5, z: 0 }
});

// Mesh collider (from model)
const mesh = new MeshCollider({
  modelUri: 'models/terrain.gltf',
  convex: false  // false = exact mesh, true = convex hull (faster)
});
```

### Applying Forces

```typescript
import { Entity, PhysicsComponent } from 'hytopia';

class Projectile extends Entity {
  physics: PhysicsComponent;
  
  constructor() {
    super();
    this.physics = new PhysicsComponent({
      mass: 0.1,
      useGravity: true
    });
    this.addComponent(this.physics);
  }
  
  launch(direction: Vector3, force: number) {
    // Apply impulse (instant force)
    this.physics.applyImpulse(direction.multiply(force));
    
    // Or apply continuous force
    this.physics.applyForce(direction.multiply(force));
    
    // Apply torque (rotation)
    this.physics.applyTorque({ x: 0, y: 100, z: 0 });
  }
}
```

## Raycasting

### Basic Raycast

```typescript
import { World } from 'hytopia';

// Raycast from point in direction
const result = world.raycast(
  { x: 0, y: 10, z: 0 },     // Origin
  { x: 0, y: -1, z: 0 },     // Direction (normalized)
  100                         // Max distance
);

if (result.hit) {
  console.log('Hit at:', result.position);
  console.log('Hit entity:', result.entity);
  console.log('Hit normal:', result.normal);
  console.log('Hit distance:', result.distance);
}
```

### Player Look Raycast

```typescript
// What is player looking at?
const raycast = world.raycast(
  player.position,
  player.lookDirection,
  5  // Reach distance
);

if (raycast.hit) {
  if (raycast.block) {
    // Looking at a block
    console.log('Block:', raycast.block.type);
  }
  if (raycast.entity) {
    // Looking at an entity
    console.log('Entity:', raycast.entity.id);
  }
}
```

## Collision Detection

### Collision Events

```typescript
import { Entity, CollisionComponent } from 'hytopia';

class CollidableEntity extends Entity {
  constructor() {
    super();
    
    const collision = new CollisionComponent();
    
    collision.onCollisionEnter = (other) => {
      console.log('Started colliding with:', other.id);
      
      if (other instanceof Projectile) {
        this.takeDamage(10);
      }
    };
    
    collision.onCollisionExit = (other) => {
      console.log('Stopped colliding with:', other.id);
    };
    
    collision.onCollisionStay = (other) => {
      // Called every frame while colliding
    };
    
    this.addComponent(collision);
  }
}
```

### Collision Layers

```typescript
import { PhysicsComponent, CollisionLayer } from 'hytopia';

// Define what collides with what
const physics = new PhysicsComponent({
  mass: 1,
  collisionLayer: CollisionLayer.DEFAULT,
  collisionMask: CollisionLayer.DEFAULT | CollisionLayer.PLAYER
});

// Layers: DEFAULT, PLAYER, ENEMY, PROJECTILE, TRIGGER, etc.
// Player doesn't collide with other players but collides with enemies
const playerPhysics = new PhysicsComponent({
  collisionLayer: CollisionLayer.PLAYER,
  collisionMask: CollisionLayer.DEFAULT | CollisionLayer.ENEMY | CollisionLayer.PROJECTILE
});
```

## Physics Materials

```typescript
import { PhysicsMaterial } from 'hytopia';

const bouncyMaterial = new PhysicsMaterial({
  friction: 0.5,        // 0 = slippery, 1 = rough
  restitution: 0.8,     // 0 = no bounce, 1 = perfect bounce
  density: 1.0          // Affects mass calculation
});

const iceMaterial = new PhysicsMaterial({
  friction: 0.1,
  restitution: 0.1
});

// Apply to collider
const collider = new BoxCollider({
  size: { x: 1, y: 1, z: 1 },
  material: bouncyMaterial
});
```

## Best Practices

1. **Use simple colliders** - Box/Sphere are faster than Mesh
2. **Set appropriate mass** - Realistic values (kg) work best
3. **Use layers wisely** - Filter collisions to improve performance
4. **Raycast before spawning** - Check if space is clear
5. **Sleep inactive bodies** - Saves CPU for stationary objects

## Common Patterns

### Ground Check

```typescript
function isGrounded(entity: Entity): boolean {
  const raycast = world.raycast(
    entity.position,
    { x: 0, y: -1, z: 0 },
    0.1  // Small distance below entity
  );
  return raycast.hit && raycast.distance < 0.05;
}

// Usage
if (isGrounded(player) && input.isPressed('space')) {
  player.physics.applyImpulse({ x: 0, y: 10, z: 0 });
}
```

### Explosion Force

```typescript
function applyExplosion(center: Vector3, radius: number, force: number) {
  // Get all entities in radius
  const entities = world.getEntitiesInRadius(center, radius);
  
  for (const entity of entities) {
    const direction = entity.position.subtract(center).normalize();
    const distance = entity.position.distance(center);
    const falloff = 1 - (distance / radius);  // Stronger closer to center
    
    if (entity.physics) {
      entity.physics.applyImpulse(
        direction.multiply(force * falloff)
      );
    }
  }
}
```
