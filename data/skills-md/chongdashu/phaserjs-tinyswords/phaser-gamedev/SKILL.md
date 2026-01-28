---
name: phaser-gamedev
description: >
  Build 2D games with Phaser 3 framework. Covers scene lifecycle, sprites, physics (Arcade/Matter),
  tilemaps, animations, input handling, and game architecture. Trigger: "create phaser game",
  "add phaser scene", "phaser sprite", "phaser physics", "game development with phaser".
---

# Phaser Game Development

Build fast, polished 2D browser games using Phaser 3's scene-based architecture and physics systems.

## Philosophy: Games as Living Systems

Games are not static UIs—they are **dynamic systems** where entities interact, state evolves, and player input drives everything. Before writing code, think architecturally.

**Before building, ask**:
- What **scenes** does this game need? (Boot, Menu, Game, Pause, GameOver)
- What **entities** exist and how do they interact?
- What **state** must persist across scenes?
- What **physics** model fits? (Arcade for speed, Matter for realism)
- What **input methods** will players use?

**Core principles**:
1. **Scene-First Architecture**: Structure games around scenes, not global state
2. **Composition Over Inheritance**: Build entities from game objects and components
3. **Physics-Aware Design**: Choose physics system before coding collisions
4. **Asset Pipeline Discipline**: Preload everything, reference by key
5. **Frame-Rate Independence**: Use delta time, not frame counting

---

## Game Configuration

Every Phaser game starts with a configuration object.

### Minimal Configuration

```javascript
const config = {
  type: Phaser.AUTO,           // WebGL with Canvas fallback
  width: 800,
  height: 600,
  scene: [BootScene, GameScene]
};

const game = new Phaser.Game(config);
```

### Full Configuration Pattern

```javascript
const config = {
  type: Phaser.AUTO,
  width: 800,
  height: 600,
  parent: 'game-container',    // DOM element ID
  backgroundColor: '#2d2d2d',

  scale: {
    mode: Phaser.Scale.FIT,
    autoCenter: Phaser.Scale.CENTER_BOTH
  },

  physics: {
    default: 'arcade',
    arcade: {
      gravity: { y: 300 },
      debug: false              // Enable during development
    }
  },

  scene: [BootScene, MenuScene, GameScene, GameOverScene]
};
```

### Physics System Choice

| System | Use When |
|--------|----------|
| **Arcade** | Platformers, shooters, most 2D games. Fast, simple AABB collisions |
| **Matter** | Physics puzzles, ragdolls, realistic collisions. Slower, more accurate |
| **None** | Menu scenes, visual novels, card games |

---

## Scene Architecture

Scenes are the fundamental organizational unit. Each scene has a lifecycle.

### Scene Lifecycle Methods

```javascript
class GameScene extends Phaser.Scene {
  constructor() {
    super('GameScene');        // Scene key for reference
  }

  init(data) {
    // Called first. Receive data from previous scene
    this.level = data.level || 1;
  }

  preload() {
    // Load assets. Runs before create()
    this.load.image('player', 'assets/player.png');
    this.load.spritesheet('enemy', 'assets/enemy.png', {
      frameWidth: 32, frameHeight: 32
    });
  }

  create() {
    // Set up game objects, physics, input
    this.player = this.physics.add.sprite(100, 100, 'player');
    this.cursors = this.input.keyboard.createCursorKeys();
  }

  update(time, delta) {
    // Game loop. Called every frame
    // delta = milliseconds since last frame
    this.player.x += this.speed * (delta / 1000);
  }
}
```

### Scene Transitions

```javascript
// Start a new scene (stops current)
this.scene.start('GameOverScene', { score: this.score });

// Launch scene in parallel (both run)
this.scene.launch('UIScene');

// Pause/resume scenes
this.scene.pause('GameScene');
this.scene.resume('GameScene');

// Stop a scene
this.scene.stop('UIScene');
```

### Recommended Scene Structure

```
scenes/
├── BootScene.js      # Asset loading, progress bar
├── MenuScene.js      # Title screen, options
├── GameScene.js      # Main gameplay
├── UIScene.js        # HUD overlay (launched parallel)
├── PauseScene.js     # Pause menu overlay
└── GameOverScene.js  # End screen, restart option
```

---

## Game Objects

Everything visible in Phaser is a Game Object.

### Common Game Objects

```javascript
// Images (static)
this.add.image(400, 300, 'background');

// Sprites (can animate, physics-enabled)
const player = this.add.sprite(100, 100, 'player');

// Text
const score = this.add.text(16, 16, 'Score: 0', {
  fontSize: '32px',
  fill: '#fff'
});

// Graphics (draw shapes)
const graphics = this.add.graphics();
graphics.fillStyle(0xff0000);
graphics.fillRect(100, 100, 50, 50);

// Containers (group objects)
const container = this.add.container(400, 300, [sprite1, sprite2]);

// Tilemaps
const map = this.make.tilemap({ key: 'level1' });
```

### Sprite Creation Patterns

```javascript
// Basic sprite
const sprite = this.add.sprite(x, y, 'textureKey');

// Sprite with physics body
const sprite = this.physics.add.sprite(x, y, 'textureKey');

// From spritesheet frame
const sprite = this.add.sprite(x, y, 'sheet', frameIndex);

// From atlas
const sprite = this.add.sprite(x, y, 'atlas', 'frameName');
```

---

## Physics Systems

### Arcade Physics (Recommended Default)

Fast, simple physics for most 2D games.

```javascript
// Enable physics on sprite
this.physics.add.sprite(x, y, 'player');

// Or add physics to existing sprite
this.physics.add.existing(sprite);

// Configure body
sprite.body.setVelocity(200, 0);
sprite.body.setBounce(0.5);
sprite.body.setCollideWorldBounds(true);
sprite.body.setGravityY(300);

// Collision detection
this.physics.add.collider(player, platforms);
this.physics.add.overlap(player, coins, collectCoin, null, this);

function collectCoin(player, coin) {
  coin.disableBody(true, true);  // Remove from physics and hide
  this.score += 10;
}
```

### Physics Groups

```javascript
// Static group (platforms, walls)
const platforms = this.physics.add.staticGroup();
platforms.create(400, 568, 'ground').setScale(2).refreshBody();

// Dynamic group (enemies, bullets)
const enemies = this.physics.add.group({
  key: 'enemy',
  repeat: 5,
  setXY: { x: 100, y: 0, stepX: 70 }
});

enemies.children.iterate(enemy => {
  enemy.setBounce(Phaser.Math.FloatBetween(0.4, 0.8));
});
```

### Matter Physics

For realistic physics simulations.

```javascript
// Config
physics: {
  default: 'matter',
  matter: {
    gravity: { y: 1 },
    debug: true
  }
}

// Create bodies
const ball = this.matter.add.circle(400, 100, 25);
const box = this.matter.add.rectangle(400, 400, 100, 50, { isStatic: true });

// Sprite with Matter body
const player = this.matter.add.sprite(100, 100, 'player');
player.setFriction(0.005);
player.setBounce(0.9);
```

---

## Input Handling

### Keyboard Input

```javascript
// Cursor keys
this.cursors = this.input.keyboard.createCursorKeys();

// In update()
if (this.cursors.left.isDown) {
  player.setVelocityX(-160);
} else if (this.cursors.right.isDown) {
  player.setVelocityX(160);
}

if (this.cursors.up.isDown && player.body.touching.down) {
  player.setVelocityY(-330);  // Jump
}

// Custom keys
this.spaceKey = this.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.SPACE);

// Key events
this.input.keyboard.on('keydown-SPACE', () => {
  this.fire();
});
```

### Pointer/Mouse Input

```javascript
// Click/tap
this.input.on('pointerdown', (pointer) => {
  console.log(pointer.x, pointer.y);
});

// Make object interactive
sprite.setInteractive();
sprite.on('pointerdown', () => {
  sprite.setTint(0xff0000);
});
sprite.on('pointerup', () => {
  sprite.clearTint();
});

// Drag
this.input.setDraggable(sprite);
this.input.on('drag', (pointer, obj, dragX, dragY) => {
  obj.x = dragX;
  obj.y = dragY;
});
```

---

## Animations

### Creating Animations

```javascript
// In create() - define once
this.anims.create({
  key: 'walk',
  frames: this.anims.generateFrameNumbers('player', { start: 0, end: 3 }),
  frameRate: 10,
  repeat: -1  // Loop forever
});

this.anims.create({
  key: 'jump',
  frames: [{ key: 'player', frame: 4 }],
  frameRate: 20
});

// From atlas
this.anims.create({
  key: 'explode',
  frames: this.anims.generateFrameNames('atlas', {
    prefix: 'explosion_',
    start: 1,
    end: 8,
    zeroPad: 2
  }),
  frameRate: 16,
  hideOnComplete: true
});
```

### Playing Animations

```javascript
// Play animation
sprite.anims.play('walk', true);  // true = ignore if already playing

// Play once
sprite.anims.play('jump');

// Stop
sprite.anims.stop();

// Animation events
sprite.on('animationcomplete', (anim, frame) => {
  if (anim.key === 'die') {
    sprite.destroy();
  }
});
```

---

## Asset Loading

### Preload Patterns

```javascript
preload() {
  // Images
  this.load.image('sky', 'assets/sky.png');

  // Spritesheets
  this.load.spritesheet('player', 'assets/player.png', {
    frameWidth: 32,
    frameHeight: 48
  });

  // Atlases (TexturePacker)
  this.load.atlas('sprites', 'assets/sprites.png', 'assets/sprites.json');

  // Tilemaps
  this.load.tilemapTiledJSON('map', 'assets/level1.json');
  this.load.image('tiles', 'assets/tileset.png');

  // Audio
  this.load.audio('bgm', 'assets/music.mp3');
  this.load.audio('sfx', ['assets/sound.ogg', 'assets/sound.mp3']);

  // Progress tracking
  this.load.on('progress', (value) => {
    console.log(`Loading: ${Math.round(value * 100)}%`);
  });
}
```

### Boot Scene Pattern

```javascript
class BootScene extends Phaser.Scene {
  constructor() {
    super('BootScene');
  }

  preload() {
    // Loading bar
    const width = this.cameras.main.width;
    const height = this.cameras.main.height;

    const progressBar = this.add.graphics();
    const progressBox = this.add.graphics();
    progressBox.fillStyle(0x222222, 0.8);
    progressBox.fillRect(width/2 - 160, height/2 - 25, 320, 50);

    this.load.on('progress', (value) => {
      progressBar.clear();
      progressBar.fillStyle(0xffffff, 1);
      progressBar.fillRect(width/2 - 150, height/2 - 15, 300 * value, 30);
    });

    // Load all game assets here
    this.load.image('player', 'assets/player.png');
    // ... more assets
  }

  create() {
    this.scene.start('MenuScene');
  }
}
```

---

## Tilemaps (Tiled Integration)

### Loading and Creating

```javascript
preload() {
  this.load.tilemapTiledJSON('map', 'assets/map.json');
  this.load.image('tiles', 'assets/tileset.png');
}

create() {
  const map = this.make.tilemap({ key: 'map' });
  const tileset = map.addTilesetImage('tileset-name-in-tiled', 'tiles');

  // Create layers (match names from Tiled)
  const backgroundLayer = map.createLayer('Background', tileset, 0, 0);
  const groundLayer = map.createLayer('Ground', tileset, 0, 0);

  // Enable collision on specific tiles
  groundLayer.setCollisionByProperty({ collides: true });
  // Or by tile index
  groundLayer.setCollisionBetween(1, 100);

  // Add collision with player
  this.physics.add.collider(this.player, groundLayer);
}
```

### Object Layers

```javascript
// Spawn points from Tiled object layer
const spawnPoint = map.findObject('Objects', obj => obj.name === 'spawn');
this.player = this.physics.add.sprite(spawnPoint.x, spawnPoint.y, 'player');

// Create objects from layer
const coins = map.createFromObjects('Objects', {
  name: 'coin',
  key: 'coin'
});
this.physics.world.enable(coins);
```

---

## Project Structure

### Recommended Organization

```
game/
├── src/
│   ├── scenes/
│   │   ├── BootScene.js
│   │   ├── MenuScene.js
│   │   ├── GameScene.js
│   │   └── UIScene.js
│   ├── gameObjects/
│   │   ├── Player.js
│   │   ├── Enemy.js
│   │   └── Collectible.js
│   ├── systems/
│   │   ├── InputManager.js
│   │   └── AudioManager.js
│   ├── config/
│   │   └── gameConfig.js
│   └── main.js
├── assets/
│   ├── images/
│   ├── audio/
│   ├── tilemaps/
│   └── fonts/
├── index.html
└── package.json
```

### ES Module Setup

```javascript
// main.js
import Phaser from 'phaser';
import BootScene from './scenes/BootScene';
import GameScene from './scenes/GameScene';
import { gameConfig } from './config/gameConfig';

const config = {
  ...gameConfig,
  scene: [BootScene, GameScene]
};

new Phaser.Game(config);
```

---

## Anti-Patterns to Avoid

❌ **Global State Soup**: Storing game state on `window` or module globals
**Why bad**: Untrackable bugs, scene transitions break state
**Better**: Use scene data, registries, or dedicated state managers

❌ **Loading in Create**: Loading assets in `create()` instead of `preload()`
**Why bad**: Assets may not be ready when referenced
**Better**: Always load in `preload()`, use Boot scene for all assets

❌ **Frame-Dependent Logic**: Using frame count instead of delta time
**Why bad**: Game speed varies with frame rate
**Better**: `this.speed * (delta / 1000)` for consistent movement

❌ **Physics Overkill**: Using Matter for simple platformer collisions
**Why bad**: Performance hit, unnecessary complexity
**Better**: Arcade physics handles 90% of 2D game needs

❌ **Monolithic Scenes**: One giant scene with all game logic
**Why bad**: Unmaintainable, hard to add features
**Better**: Separate scenes for menus, gameplay, UI overlays

❌ **Magic Numbers**: Hardcoded values scattered in code
**Why bad**: Impossible to balance, inconsistent
**Better**: Config objects, constants files

❌ **Ignoring Object Pooling**: Creating/destroying objects every frame
**Why bad**: Memory churn, garbage collection stutters
**Better**: Use groups with `setActive(false)` / `setVisible(false)`

❌ **Synchronous Asset Access**: Assuming assets load instantly
**Why bad**: Race conditions, undefined textures
**Better**: Chain scene starts, use load events

❌ **Assuming Spritesheet Frame Dimensions**: Using guessed frame sizes without verifying
**Why bad**: Wrong dimensions cause silent frame corruption; off-by-pixels compounds into broken visuals
**Better**: Open asset file, measure frames, calculate with spacing/margin, verify math adds up

❌ **Ignoring Spritesheet Spacing**: Not specifying `spacing` for gapped spritesheets
**Why bad**: Frames shift progressively; later frames read wrong pixel regions
**Better**: Check source asset for gaps between frames; use `spacing: N` in loader config

❌ **Hardcoding Nine-Slice Colors**: Using single background color for all UI panel variants
**Why bad**: Transparent frame edges reveal wrong color for different asset color schemes
**Better**: Per-asset background color config; sample from center frame (frame 4)

❌ **Nine-Slice with Padded Frames**: Treating the full frame as the slice region when the art is centered/padded inside each tile
**Why bad**: Edge tiles contribute interior fill, showing up as opaque “side bars” inside the panel
**Better**: Trim tiles to their effective content bounds (alpha bbox) and composite/cache a texture; add ~1px overlap + disable smoothing to avoid seams

❌ **Scaling Discontinuous UI Art**: Stretching a cropped ribbon/banner row that contains internal transparent gaps
**Why bad**: The transparent gutters get stretched, so the UI looks segmented or the fill disappears behind the frame.
**Better**: Slice the asset into caps/center, stretch only the center, and stitch the pieces (with ~1px overlap + smoothing disabled) before rendering at pivot sizes.

---

## Variation Guidance

**IMPORTANT**: Game implementations should vary based on:

- **Game Genre**: Platformer physics differ from top-down shooter physics
- **Target Platform**: Mobile needs touch input, desktop can use keyboard
- **Art Style**: Pixel art uses nearest-neighbor scaling, HD art uses linear
- **Performance Needs**: Many sprites → object pooling; few sprites → simple creation
- **Complexity**: Simple games can inline; complex games need class hierarchies

**Avoid converging on**:
- Always using 800x600 resolution
- Always using Arcade physics
- Always using the same scene structure
- Copy-pasting boilerplate without adaptation

---

## Quick Reference

### Common Physics Properties

```javascript
body.setVelocity(x, y)
body.setVelocityX(x)
body.setBounce(x, y)
body.setGravityY(y)
body.setCollideWorldBounds(true)
body.setImmovable(true)        // For static-like dynamic bodies
body.setDrag(x, y)
body.setMaxVelocity(x, y)
```

### Useful Scene Properties

```javascript
this.cameras.main              // Main camera
this.physics.world             // Physics world
this.input.keyboard            // Keyboard manager
this.sound                     // Audio manager
this.time                      // Time/clock manager
this.tweens                    // Tween manager
this.anims                     // Animation manager
this.registry                  // Cross-scene data store
this.data                      // Scene-specific data store
```

### Essential Events

```javascript
// Scene events
this.events.on('pause', callback)
this.events.on('resume', callback)
this.events.on('shutdown', callback)

// Physics events
this.physics.world.on('worldbounds', callback)

// Game object events
sprite.on('destroy', callback)
sprite.on('animationcomplete', callback)
```

---

## See Also

- **references/arcade-physics.md** - Deep dive into Arcade physics
- **references/tilemaps.md** - Advanced tilemap techniques
- **references/performance.md** - Optimization strategies
- **references/spritesheets-nineslice.md** - Spritesheet loading (spacing/margin), nine-slice UI panels, asset inspection

---

## Remember

Phaser gives you powerful primitives—scenes, sprites, physics, input—but **architecture is your responsibility**.

Think in systems: What scenes do you need? What entities exist? How do they interact? Answer these questions before writing code, and your game will be maintainable as it grows.

**Claude is capable of building complete, polished Phaser games. These guidelines illuminate the path—they don't fence it.**
