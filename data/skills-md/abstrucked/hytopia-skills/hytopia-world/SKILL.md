---
name: hytopia-world
description: Helps build and manage worlds in HYTOPIA SDK. Use when users need to create terrain, place blocks, manage chunks, or work with the world editor integration. Covers blocks, chunk loading, world generation, and build.hytopia.com workflow.
---

# HYTOPIA World Building

This skill helps you build and manage worlds in HYTOPIA SDK games.

## When to Use This Skill

Use this skill when the user:

- Wants to create terrain or place blocks programmatically
- Needs to work with chunk loading/unloading
- Asks about world generation or procedural terrain
- Wants to integrate with build.hytopia.com world editor
- Needs to save/load world data
- Asks about block types, textures, or custom blocks

## Core World Concepts

### Basic Block Placement

```typescript
import { World, BlockType } from 'hytopia';

// Place a single block
world.setBlock({ x: 0, y: 0, z: 0 }, BlockType.GRASS);

// Remove a block
world.setBlock({ x: 0, y: 0, z: 0 }, BlockType.AIR);

// Get block at position
const block = world.getBlock({ x: 0, y: 0, z: 0 });
```

### Creating Custom Blocks

```typescript
import { BlockType, Block } from 'hytopia';

const customBlock = new BlockType({
  id: 'my-mod:custom-block',
  name: 'Custom Block',
  textureUri: 'textures/custom.png',
  isSolid: true,
  opacity: 1.0
});

// Register the block
world.blockRegistry.register(customBlock);
```

### World Generation

```typescript
import { World, BlockType } from 'hytopia';

class TerrainGenerator {
  generateChunk(chunkX: number, chunkZ: number, world: World) {
    for (let x = 0; x < 16; x++) {
      for (let z = 0; z < 16; z++) {
        const worldX = chunkX * 16 + x;
        const worldZ = chunkZ * 16 + z;
        
        // Simple heightmap
        const height = Math.floor(Math.sin(worldX * 0.1) * 5 + 10);
        
        for (let y = 0; y < height; y++) {
          const block = y === height - 1 ? BlockType.GRASS : BlockType.DIRT;
          world.setBlock({ x: worldX, y, z: worldZ }, block);
        }
      }
    }
  }
}
```

### Loading World from Editor

```typescript
import { World } from 'hytopia';
import worldData from './assets/world.json';

// Load world created in build.hytopia.com
world.loadFromJSON(worldData);
```

## Chunk Management

### Chunk Loading

```typescript
// Enable chunk loading around players
world.chunkLoadingEnabled = true;
world.chunkLoadRadius = 8; // chunks

// Custom chunk loader
world.onChunkLoad = (chunkX, chunkZ) => {
  // Generate or load chunk data
  terrainGenerator.generateChunk(chunkX, chunkZ, world);
};

world.onChunkUnload = (chunkX, chunkZ) => {
  // Save chunk data if needed
};
```

### Manual Chunk Control

```typescript
// Load specific chunk
world.loadChunk(0, 0);

// Unload chunk
world.unloadChunk(0, 0);

// Check if chunk is loaded
const isLoaded = world.isChunkLoaded(0, 0);
```

## Build.hytopia.com Integration

### Exporting from Editor

1. Build your world at https://build.hytopia.com
2. Export as JSON
3. Place in `assets/world.json`

### Loading Exported World

```typescript
import worldData from './assets/world.json';

world.loadFromJSON(worldData, {
  // Options
  clearExisting: true,  // Remove existing blocks
  offset: { x: 0, y: 0, z: 0 }  // Apply offset
});
```

## Best Practices

1. **Use chunk loading** for large worlds - don't load everything at once
2. **Batch block operations** - set multiple blocks at once when possible
3. **Save modified chunks** - persist player changes
4. **Use block palettes** - define reusable block combinations
5. **Optimize collision** - mark non-solid blocks appropriately

## Common Patterns

### Placing Structure

```typescript
function placeStructure(world: World, position: Vector3, structure: Block[][]) {
  for (let y = 0; y < structure.length; y++) {
    for (let x = 0; x < structure[y].length; x++) {
      for (let z = 0; z < structure[y][x].length; z++) {
        const block = structure[y][x][z];
        if (block !== BlockType.AIR) {
          world.setBlock({
            x: position.x + x,
            y: position.y + y,
            z: position.z + z
          }, block);
        }
      }
    }
  }
}
```

### Raycast Block Placement

```typescript
// Place block where player is looking
const raycast = world.raycast(player.position, player.lookDirection, 5);
if (raycast.hit) {
  const placePos = raycast.position.add(raycast.normal);
  world.setBlock(placePos, BlockType.STONE);
}
```
