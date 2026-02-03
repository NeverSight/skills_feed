---
name: hytopia-assets
description: Helps manage assets in HYTOPIA SDK games. Use when users need to load models, textures, audio, or UI elements. Covers asset loading, HytopiaUI, models, textures, sounds, and asset optimization.
---

# HYTOPIA Assets & UI

This skill helps you manage assets and UI in HYTOPIA SDK games.

## When to Use This Skill

Use this skill when the user:

- Wants to load 3D models (GLTF/GLB)
- Needs to add textures or materials
- Asks about playing sounds or music
- Wants to create UI elements (HUD, menus)
- Needs to optimize asset loading
- Asks about default SDK assets

## Core Asset Concepts

### Loading Models

```typescript
import { Model, Entity } from 'hytopia';

class Character extends Entity {
  constructor() {
    super();
    
    this.model = new Model({
      modelUri: 'models/character.gltf',
      scale: 1.0,
      rotation: { x: 0, y: 0, z: 0 }
    });
  }
}

// Load with animation
const animatedModel = new Model({
  modelUri: 'models/player.gltf',
  animationUri: 'animations/player-idle.gltf',
  loopAnimation: true
});
```

### Using Default Assets

```typescript
import { Model, BlockType } from 'hytopia';

// Default models included with SDK
const defaultModels = {
  player: 'hytopia:models/player.gltf',
  cube: 'hytopia:models/cube.gltf',
  sphere: 'hytopia:models/sphere.gltf'
};

// Default block textures
const defaultBlocks = {
  grass: BlockType.GRASS,
  dirt: BlockType.DIRT,
  stone: BlockType.STONE,
  wood: BlockType.WOOD,
  leaves: BlockType.LEAVES
};
```

### Custom Textures

```typescript
import { BlockType, Material } from 'hytopia';

// Create block with custom texture
const customBlock = new BlockType({
  id: 'my-mod:custom-block',
  name: 'Custom Block',
  textureUri: 'textures/custom-block.png',
  material: new Material({
    roughness: 0.8,
    metalness: 0.0
  })
});
```

## Audio

### Playing Sounds

```typescript
import { Audio, Entity } from 'hytopia';

class SoundEntity extends Entity {
  playSound() {
    // One-shot sound
    this.playAudio({
      uri: 'sounds/explosion.mp3',
      volume: 1.0,
      pitch: 1.0,
      spatial: true,  // 3D positional audio
      range: 20       // Audible within 20 units
    });
  }
  
  playMusic() {
    // Looping background music
    this.playAudio({
      uri: 'music/background.mp3',
      volume: 0.5,
      loop: true,
      spatial: false  // Global audio
    });
  }
}

// Play at location
world.playAudioAtPosition(
  { x: 0, y: 10, z: 0 },
  { uri: 'sounds/ambient.mp3', volume: 0.3, range: 30 }
);
```

### Audio Management

```typescript
// Stop specific sound
entity.stopAudio('sounds/explosion.mp3');

// Stop all sounds on entity
entity.stopAllAudio();

// Fade out
entity.fadeAudio('music/background.mp3', 0, 2000);  // Fade to 0 over 2 seconds
```

## HytopiaUI

### Creating UI Elements

```typescript
import { Player, UI } from 'hytopia';

// Send UI to player
player.sendUI({
  type: 'panel',
  id: 'hud',
  position: { x: 0.5, y: 0.9 },  // Normalized screen position
  anchor: 'center-bottom',
  children: [
    {
      type: 'text',
      id: 'score',
      text: 'Score: 0',
      style: { fontSize: 24, color: '#ffffff' }
    },
    {
      type: 'bar',
      id: 'health',
      value: 100,
      max: 100,
      style: { 
        width: 200, 
        height: 20, 
        backgroundColor: '#333333',
        fillColor: '#ff0000'
      }
    }
  ]
});
```

### Updating UI

```typescript
// Update specific element
player.updateUI('score', {
  text: `Score: ${player.getData('score')}`
});

player.updateUI('health', {
  value: player.getData('health'),
  max: 100
});

// Remove UI
player.removeUI('hud');
```

### Interactive UI

```typescript
player.sendUI({
  type: 'panel',
  id: 'menu',
  children: [
    {
      type: 'button',
      id: 'start-btn',
      text: 'Start Game',
      onClick: 'start-game'
    },
    {
      type: 'button',
      id: 'settings-btn',
      text: 'Settings',
      onClick: 'open-settings'
    }
  ]
});

// Handle clicks
player.onUIEvent = (event) => {
  if (event.elementId === 'start-btn') {
    startGame(player);
  } else if (event.elementId === 'settings-btn') {
    openSettings(player);
  }
};
```

## Asset Organization

### Recommended Structure

```
assets/
├── models/
│   ├── characters/
│   ├── items/
│   └── environment/
├── textures/
│   ├── blocks/
│   ├── ui/
│   └── effects/
├── audio/
│   ├── sfx/
│   ├── music/
│   └── ambient/
└── ui/
    ├── hud.json
    ├── menu.json
    └── inventory.json
```

### Asset Loading Strategy

```typescript
import { AssetManager } from 'hytopia';

// Preload critical assets
await AssetManager.preload([
  'models/player.gltf',
  'textures/crosshair.png',
  'sounds/jump.mp3'
]);

// Load on demand
function loadLevel(levelId: string) {
  return AssetManager.loadBatch([
    `levels/${levelId}/terrain.gltf`,
    `levels/${levelId}/skybox.png`
  ]);
}
```

## Best Practices

1. **Optimize models** - Use GLB format, limit polygon count
2. **Compress textures** - Use appropriate formats (PNG for UI, compressed for 3D)
3. **Audio formats** - MP3 for music, WAV for short SFX
4. **Lazy loading** - Load assets only when needed
5. **Reuse materials** - Don't create duplicate materials
6. **Atlas textures** - Combine UI sprites into atlases

## Common Patterns

### Crosshair UI

```typescript
player.sendUI({
  type: 'image',
  id: 'crosshair',
  position: { x: 0.5, y: 0.5 },
  anchor: 'center-center',
  source: 'textures/crosshair.png',
  style: { width: 32, height: 32 }
});
```

### Damage Indicator

```typescript
function showDamageIndicator(player: Player, damage: number) {
  player.sendUI({
    type: 'text',
    id: 'damage-text',
    position: { x: 0.5, y: 0.4 },
    anchor: 'center-center',
    text: `-${damage}`,
    style: { 
      fontSize: 36, 
      color: '#ff0000',
      fontWeight: 'bold'
    }
  });
  
  // Remove after delay
  setTimeout(() => player.removeUI('damage-text'), 1000);
}
```

### Loading Screen

```typescript
function showLoadingScreen(player: Player) {
  player.sendUI({
    type: 'panel',
    id: 'loading',
    fullScreen: true,
    style: { backgroundColor: '#000000' },
    children: [
      {
        type: 'text',
        text: 'Loading...',
        style: { fontSize: 48, color: '#ffffff' }
      },
      {
        type: 'progress',
        id: 'loading-bar',
        value: 0,
        max: 100,
        style: { width: 400, height: 20 }
      }
    ]
  });
}

function updateLoadingProgress(player: Player, percent: number) {
  player.updateUI('loading-bar', { value: percent });
  
  if (percent >= 100) {
    player.removeUI('loading');
  }
}
```
