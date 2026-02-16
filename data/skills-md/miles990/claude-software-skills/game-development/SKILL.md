---
name: game-development
description: Game development patterns, architectures, and best practices
domain: domain-applications
version: 1.0.0
tags: [game, unity, unreal, godot, flame, flutter, ecs, physics, multiplayer, ai]
triggers:
  keywords:
    primary: [game, game development, unity, unreal, godot, flame, flutter game, ecs, game loop]
    secondary: [sprite, collision, physics, multiplayer, pathfinding, ai, behavior tree, dart game, 2d game]
  context_boost: [2d, 3d, animation, rendering, engine]
  context_penalty: [web, api, database, backend]
  priority: medium
---

# Game Development

## Overview

Patterns and practices for building games across platforms. Covers architecture, rendering, physics, AI, multiplayer, and optimization.

---

## Game Architecture

### Game Loop

```
┌─────────────────────────────────────────────────────────────┐
│                      Game Loop                              │
│                                                             │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐ │
│   │  Input  │ ─→ │ Update  │ ─→ │ Physics │ ─→ │ Render  │ │
│   │ Process │    │  Logic  │    │  Step   │    │  Frame  │ │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘ │
│        ↑                                             │      │
│        └─────────────────────────────────────────────┘      │
│                        Next Frame                           │
└─────────────────────────────────────────────────────────────┘
```

### Fixed vs Variable Timestep

| Type | Use Case | Code Pattern |
|------|----------|--------------|
| Fixed | Physics, determinism | `while (accumulator >= dt) { update(dt); }` |
| Variable | Rendering, animations | `update(deltaTime);` |
| Hybrid | Most games | Fixed physics, variable render |

```typescript
// Hybrid game loop
let accumulator = 0;
const FIXED_DT = 1/60;

function gameLoop(currentTime: number) {
  const deltaTime = currentTime - lastTime;
  accumulator += deltaTime;

  // Fixed timestep for physics
  while (accumulator >= FIXED_DT) {
    physicsUpdate(FIXED_DT);
    accumulator -= FIXED_DT;
  }

  // Variable timestep for rendering
  const alpha = accumulator / FIXED_DT;
  render(alpha); // Interpolate between states

  requestAnimationFrame(gameLoop);
}
```

---

### Entity Component System (ECS)

```
┌─────────────────────────────────────────────────────────────┐
│                    ECS Architecture                         │
│                                                             │
│  Entity: Just an ID                                         │
│  ┌─────┐  ┌─────┐  ┌─────┐                                 │
│  │  1  │  │  2  │  │  3  │                                 │
│  └─────┘  └─────┘  └─────┘                                 │
│                                                             │
│  Components: Pure Data                                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Position │  │ Velocity │  │  Sprite  │                  │
│  │ x, y, z  │  │ vx, vy   │  │ texture  │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
│                                                             │
│  Systems: Logic                                             │
│  ┌────────────────┐  ┌────────────────┐                    │
│  │ MovementSystem │  │ RenderSystem   │                    │
│  │ Position+Vel   │  │ Position+Sprite│                    │
│  └────────────────┘  └────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

```typescript
// Component definitions
interface Position { x: number; y: number; }
interface Velocity { vx: number; vy: number; }
interface Sprite { texture: string; width: number; height: number; }

// System
function movementSystem(entities: Entity[], dt: number) {
  for (const entity of entities) {
    if (entity.has(Position) && entity.has(Velocity)) {
      const pos = entity.get(Position);
      const vel = entity.get(Velocity);
      pos.x += vel.vx * dt;
      pos.y += vel.vy * dt;
    }
  }
}
```

---

## 2D Game Development

### Sprite Animation

```typescript
interface Animation {
  frames: string[];       // Texture names
  frameDuration: number;  // Seconds per frame
  loop: boolean;
}

class AnimatedSprite {
  private currentFrame = 0;
  private elapsed = 0;

  update(dt: number) {
    this.elapsed += dt;
    if (this.elapsed >= this.animation.frameDuration) {
      this.elapsed = 0;
      this.currentFrame++;
      if (this.currentFrame >= this.animation.frames.length) {
        this.currentFrame = this.animation.loop ? 0 : this.animation.frames.length - 1;
      }
    }
  }

  get texture(): string {
    return this.animation.frames[this.currentFrame];
  }
}
```

### Collision Detection

| Method | Complexity | Use Case |
|--------|------------|----------|
| AABB | O(n²) → O(n log n) | Boxes, simple shapes |
| Circle | O(n²) | Projectiles, characters |
| SAT | O(n²) | Complex convex polygons |
| Pixel Perfect | Expensive | Precise collision |

```typescript
// AABB collision
function aabbIntersect(a: AABB, b: AABB): boolean {
  return a.x < b.x + b.width &&
         a.x + a.width > b.x &&
         a.y < b.y + b.height &&
         a.y + a.height > b.y;
}

// Spatial hash for broad phase
class SpatialHash {
  private cells = new Map<string, Entity[]>();
  private cellSize: number;

  insert(entity: Entity) {
    const key = this.getKey(entity.position);
    if (!this.cells.has(key)) this.cells.set(key, []);
    this.cells.get(key)!.push(entity);
  }

  query(position: Vector2): Entity[] {
    // Check neighboring cells
    const nearby: Entity[] = [];
    for (let dx = -1; dx <= 1; dx++) {
      for (let dy = -1; dy <= 1; dy++) {
        const key = this.getKey({ x: position.x + dx * this.cellSize, y: position.y + dy * this.cellSize });
        nearby.push(...(this.cells.get(key) || []));
      }
    }
    return nearby;
  }
}
```

---

## Game AI

### Finite State Machine

```typescript
interface State {
  enter(): void;
  update(dt: number): void;
  exit(): void;
}

class EnemyAI {
  private states = new Map<string, State>();
  private currentState: State;

  transition(stateName: string) {
    this.currentState?.exit();
    this.currentState = this.states.get(stateName)!;
    this.currentState.enter();
  }
}

// Example: Patrol → Chase → Attack
class PatrolState implements State {
  enter() { this.setAnimation('walk'); }
  update(dt: number) {
    this.patrol();
    if (this.canSeePlayer()) {
      this.fsm.transition('chase');
    }
  }
  exit() {}
}
```

### Behavior Trees

```
┌─────────────────────────────────────────────────────────────┐
│                    Behavior Tree                            │
│                                                             │
│                      [Selector]                             │
│                     /          \                            │
│              [Sequence]      [Patrol]                       │
│              /        \                                     │
│        [CanSee?]    [Attack]                               │
│            │                                                │
│         [Chase]                                             │
└─────────────────────────────────────────────────────────────┘
```

### Pathfinding (A*)

```typescript
function aStar(start: Node, goal: Node): Node[] {
  const openSet = new PriorityQueue<Node>();
  const cameFrom = new Map<Node, Node>();
  const gScore = new Map<Node, number>();
  const fScore = new Map<Node, number>();

  gScore.set(start, 0);
  fScore.set(start, heuristic(start, goal));
  openSet.enqueue(start, fScore.get(start)!);

  while (!openSet.isEmpty()) {
    const current = openSet.dequeue()!;

    if (current === goal) {
      return reconstructPath(cameFrom, current);
    }

    for (const neighbor of getNeighbors(current)) {
      const tentativeG = gScore.get(current)! + distance(current, neighbor);

      if (tentativeG < (gScore.get(neighbor) ?? Infinity)) {
        cameFrom.set(neighbor, current);
        gScore.set(neighbor, tentativeG);
        fScore.set(neighbor, tentativeG + heuristic(neighbor, goal));
        openSet.enqueue(neighbor, fScore.get(neighbor)!);
      }
    }
  }

  return []; // No path found
}
```

---

## Multiplayer Games

### Network Architecture

| Model | Latency | Complexity | Use Case |
|-------|---------|------------|----------|
| Peer-to-Peer | Low | Medium | Fighting games, small lobbies |
| Client-Server | Medium | High | Most online games |
| Authoritative Server | Higher | Highest | Competitive games |

### Lag Compensation

```typescript
// Client-side prediction
class NetworkedPlayer {
  private pendingInputs: Input[] = [];
  private serverState: PlayerState;

  update(input: Input) {
    // 1. Apply input locally (prediction)
    this.applyInput(input);
    this.pendingInputs.push(input);

    // 2. Send to server
    this.sendInput(input);
  }

  onServerUpdate(state: PlayerState, lastProcessedInput: number) {
    // 3. Reconcile with server
    this.serverState = state;

    // 4. Re-apply unprocessed inputs
    this.pendingInputs = this.pendingInputs.filter(i => i.id > lastProcessedInput);
    for (const input of this.pendingInputs) {
      this.applyInput(input);
    }
  }
}
```

### State Synchronization

```typescript
// Delta compression
interface StateDelta {
  timestamp: number;
  changes: Map<EntityId, ComponentChanges>;
}

function computeDelta(prev: GameState, curr: GameState): StateDelta {
  const changes = new Map();
  for (const [id, entity] of curr.entities) {
    const prevEntity = prev.entities.get(id);
    if (!prevEntity || hasChanged(prevEntity, entity)) {
      changes.set(id, getChangedComponents(prevEntity, entity));
    }
  }
  return { timestamp: curr.timestamp, changes };
}
```

---

## Game Optimization

### Rendering Optimization

| Technique | Benefit | Implementation |
|-----------|---------|----------------|
| Batching | Reduce draw calls | Combine sprites with same texture |
| Culling | Skip invisible objects | Frustum culling, occlusion culling |
| LOD | Reduce polygon count | Distance-based model switching |
| Instancing | Efficient duplicates | GPU instancing for repeated objects |

### Memory Optimization

```typescript
// Object pooling
class ObjectPool<T> {
  private pool: T[] = [];
  private factory: () => T;

  acquire(): T {
    return this.pool.pop() ?? this.factory();
  }

  release(obj: T) {
    this.reset(obj);
    this.pool.push(obj);
  }
}

// Usage
const bulletPool = new ObjectPool(() => new Bullet());

function fireBullet() {
  const bullet = bulletPool.acquire();
  bullet.init(position, direction);
  activeBullets.add(bullet);
}

function onBulletHit(bullet: Bullet) {
  activeBullets.delete(bullet);
  bulletPool.release(bullet);
}
```

---

## Game Engines Reference

| Engine | Language | Best For | Platform | Skill |
|--------|----------|----------|----------|-------|
| Unity | C# | Mobile, indie, VR | All | - |
| Unreal | C++, Blueprint | AAA, realistic | PC, Console | - |
| Godot | GDScript, C# | Indie, 2D | All | - |
| **Flame** | Dart | Flutter 2D, casual | All | [flame/](./flame/) |
| Phaser | JavaScript | Web 2D | Browser | - |
| Three.js | JavaScript | Web 3D | Browser | - |
| Bevy | Rust | Performance | Desktop | - |
| LÖVE | Lua | Simple 2D | Desktop | - |

### Flame Engine (Flutter)

專為 Flutter 開發者設計的 2D 遊戲引擎，詳細文件請參考 [flame/SKILL.md](./flame/SKILL.md)：

- **flame-core/** - 組件、輸入、碰撞、相機、動畫、音效、粒子
- **flame-systems/** - 14 個遊戲系統（任務、對話、背包、戰鬥等）
- **flame-templates/** - RPG、Platformer、Roguelike 模板

---

## Related Skills

- [[performance-optimization]] - General optimization
- [[realtime-systems]] - WebSocket, networking
- [[cpp]] - Performance-critical code
- [[javascript-typescript]] - Web games
