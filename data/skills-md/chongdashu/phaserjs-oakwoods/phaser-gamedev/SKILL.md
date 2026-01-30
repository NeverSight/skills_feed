---
name: phaser-gamedev
description: >
  Build 2D games with Phaser 3 framework. Covers scene lifecycle, sprites, physics (Arcade/Matter),
  tilemaps, animations, input handling, and game architecture. Trigger: "create phaser game",
  "add phaser scene", "phaser sprite", "phaser physics", "game development with phaser".
---

# Phaser Game Development

Build 2D browser games using Phaser 3's scene-based architecture and physics systems.

---

## STOP: Before Loading Any Spritesheet

**Read [spritesheets-nineslice.md](references/spritesheets-nineslice.md) FIRST.**

Spritesheet loading is fragile—a few pixels off causes silent corruption that compounds into broken visuals. The reference file contains the mandatory inspection protocol.

**Quick rules** (details in reference):

1. **Measure the asset** before writing loader code—never guess frame dimensions
2. **Character sprites use SQUARE frames**: If you calculate frameWidth=56, try 56 for height first
3. **Different animations have different frame sizes**: A run cycle needs wider frames than idle; an attack needs extra width for weapon swing. Measure EACH spritesheet independently
4. **Check for spacing**: Gaps between frames require `spacing: N` in loader config
5. **Verify the math**: `imageWidth = (frameWidth × cols) + (spacing × (cols - 1))`

---

## Reference Files

Read these BEFORE working on the relevant feature:

| When working on... | Read first |
|--------------------|------------|
| Loading ANY spritesheet | [spritesheets-nineslice.md](references/spritesheets-nineslice.md) |
| Nine-slice UI panels | [spritesheets-nineslice.md](references/spritesheets-nineslice.md) |
| Tiled tilemaps, collision layers | [tilemaps.md](references/tilemaps.md) |
| Physics tuning, groups, pooling | [arcade-physics.md](references/arcade-physics.md) |
| Performance issues, object pooling | [performance.md](references/performance.md) |

---

## Architecture Decisions (Make Early)

### Physics System Choice

| System | Use When |
|--------|----------|
| **Arcade** | Platformers, shooters, most 2D games. Fast AABB collisions |
| **Matter** | Physics puzzles, ragdolls, realistic collisions. Slower, more accurate |
| **None** | Menu scenes, visual novels, card games |

### Scene Structure

```
scenes/
├── BootScene.ts      # Asset loading, progress bar
├── MenuScene.ts      # Title screen, options
├── GameScene.ts      # Main gameplay
├── UIScene.ts        # HUD overlay (launched parallel)
└── GameOverScene.ts  # End screen, restart
```

### Scene Transitions

```typescript
this.scene.start('GameScene', { level: 1 });     // Stop current, start new
this.scene.launch('UIScene');                     // Run in parallel
this.scene.pause('GameScene');                    // Pause
this.scene.stop('UIScene');                       // Stop
```

---

## Core Patterns

### Game Configuration

```typescript
const config: Phaser.Types.Core.GameConfig = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },
  physics: {
    default: 'arcade',
    arcade: { gravity: { y: 300 }, debug: false }
  },
  scene: [BootScene, MenuScene, GameScene]
};
```

### Scene Lifecycle

```typescript
class GameScene extends Phaser.Scene {
  init(data) { }      // Receive data from previous scene
  preload() { }       // Load assets (runs before create)
  create() { }        // Set up game objects, physics, input
  update(time, delta) { }  // Game loop, use delta for frame-rate independence
}
```

### Frame-Rate Independent Movement

```typescript
// CORRECT: scales with frame rate
this.player.x += this.speed * (delta / 1000);

// WRONG: varies with frame rate
this.player.x += this.speed;
```

---

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
|--------------|---------|----------|
| Global state on `window` | Scene transitions break state | Use scene data, registries |
| Loading in `create()` | Assets not ready when referenced | Load in `preload()`, use Boot scene |
| Frame counting | Game speed varies with FPS | Use `delta / 1000` |
| Matter for simple collisions | Unnecessary complexity | Arcade handles most 2D games |
| One giant scene | Hard to extend | Separate gameplay/UI/menus |
| Magic numbers | Impossible to balance | Config objects, constants |
| No object pooling | GC stutters | Groups with `setActive(false)` |

---

## Remember

Phaser provides powerful primitives—scenes, sprites, physics, input—but **architecture is your responsibility**.

Before coding: What scenes? What entities? How do they interact? What physics model?

**Claude can build complete, polished Phaser games. These guidelines illuminate the path—they don't fence it.**
