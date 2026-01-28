---
name: hytale-custom-assets
description: Create and manage custom assets for Hytale including models, textures, sounds, particles, and asset packs. Use when asked to "add custom assets", "create textures", "make models", "add sounds", "configure particles", or "build an asset pack".
metadata:
  author: Liam Robinson (MnkyArts)
  version: "1.0.0"
---

# Creating Custom Hytale Assets

Complete guide for creating and managing custom assets including models, textures, sounds, and particles.

## When to use this skill

Use this skill when:
- Creating asset packs for plugins
- Adding custom textures and models
- Configuring sounds and music
- Creating particle effects
- Setting up animations
- Managing asset inheritance and tags

## Asset System Architecture

Hytale uses a hierarchical asset system:

```
AssetPack
├── Server/          # Server-side assets
│   └── Content/     # Game content definitions
│       ├── BlockTypes/
│       ├── Items/
│       ├── Entities/
│       └── ...
└── Client/          # Client-side assets
    ├── Models/
    ├── Textures/
    ├── Sounds/
    ├── Particles/
    └── ...
```

## Asset Pack Structure

```
my-plugin/
└── assets/
    ├── pack.json                    # Pack metadata
    ├── Server/
    │   └── Content/
    │       ├── BlockTypes/
    │       │   └── custom_block.blocktype
    │       ├── Items/
    │       │   └── custom_item.item
    │       ├── Entities/
    │       │   └── custom_entity.entity
    │       ├── Recipes/
    │       │   └── custom_recipe.recipe
    │       └── Sounds/
    │           └── custom_soundset.soundset
    └── Client/
        ├── Models/
        │   └── custom_model.model
        ├── Textures/
        │   ├── blocks/
        │   │   └── custom_block.png
        │   ├── items/
        │   │   └── custom_item.png
        │   └── entities/
        │       └── custom_entity.png
        ├── Sounds/
        │   └── custom/
        │       └── sound.ogg
        ├── Particles/
        │   └── custom_particle.particle
        └── Animations/
            └── custom_animation.animation
```

## Pack Metadata

**File**: `pack.json`

```json
{
  "Name": "MyPlugin Assets",
  "Id": "MyPlugin",
  "Version": "1.0.0",
  "Description": "Custom assets for MyPlugin",
  "Author": "Your Name",
  "Priority": 100,
  "Dependencies": ["Hytale:Core"]
}
```

### Pack Properties

| Property | Type | Description |
|----------|------|-------------|
| `Name` | String | Display name |
| `Id` | String | Unique identifier |
| `Version` | String | Semantic version |
| `Description` | String | Pack description |
| `Author` | String | Creator name |
| `Priority` | Integer | Load order (higher = later) |
| `Dependencies` | Array | Required packs |

## Textures

### Texture Formats

| Format | Use Case |
|--------|----------|
| PNG | Standard textures (recommended) |
| TGA | Textures with alpha |
| DDS | Compressed textures |

### Block Textures

**Location**: `Client/Textures/blocks/`

```
custom_block.png          # All faces
custom_block_top.png      # Top face only
custom_block_side.png     # Side faces
custom_block_bottom.png   # Bottom face
```

**Texture Size**: 16x16, 32x32, 64x64 (power of 2)

### Item Textures

**Location**: `Client/Textures/items/`

```
custom_item.png           # Inventory icon (32x32)
custom_item_held.png      # Held model texture
```

### Entity Textures

**Location**: `Client/Textures/entities/`

```
custom_entity.png         # Main texture atlas
custom_entity_glow.png    # Emissive layer
custom_entity_normal.png  # Normal map
```

## Models

### Model Format

Hytale uses a custom JSON-based model format.

**File**: `custom_model.model`

```json
{
  "Parent": "Hytale/Models/base_entity",
  "Textures": {
    "main": "MyPlugin/Textures/entities/custom_entity"
  },
  "Bones": [
    {
      "Name": "root",
      "Pivot": [0, 0, 0],
      "Children": [
        {
          "Name": "body",
          "Pivot": [0, 12, 0],
          "Cubes": [
            {
              "Origin": [-4, 0, -2],
              "Size": [8, 12, 4],
              "UV": [0, 0]
            }
          ],
          "Children": [
            {
              "Name": "head",
              "Pivot": [0, 24, 0],
              "Cubes": [
                {
                  "Origin": [-4, 0, -4],
                  "Size": [8, 8, 8],
                  "UV": [0, 16]
                }
              ]
            }
          ]
        }
      ]
    }
  ],
  "Animations": {
    "idle": "MyPlugin/Animations/custom_idle",
    "walk": "MyPlugin/Animations/custom_walk"
  }
}
```

### Model Properties

| Property | Type | Description |
|----------|------|-------------|
| `Parent` | String | Parent model to inherit |
| `Textures` | Object | Texture bindings |
| `Bones` | Array | Bone hierarchy |
| `Animations` | Object | Animation bindings |
| `Scale` | Float | Overall scale |
| `TextureSize` | Array | Texture dimensions [W, H] |

### Bone Properties

| Property | Type | Description |
|----------|------|-------------|
| `Name` | String | Bone identifier |
| `Pivot` | Array | Rotation pivot point |
| `Rotation` | Array | Default rotation [X, Y, Z] |
| `Cubes` | Array | Geometry cubes |
| `Children` | Array | Child bones |
| `Mirror` | Boolean | Mirror UV horizontally |

### Cube Properties

| Property | Type | Description |
|----------|------|-------------|
| `Origin` | Array | Position offset |
| `Size` | Array | Dimensions [W, H, D] |
| `UV` | Array | Texture UV offset [U, V] |
| `Inflate` | Float | Expand cube size |
| `Mirror` | Boolean | Mirror this cube |

## Animations

**File**: `custom_animation.animation`

```json
{
  "Length": 1.0,
  "Loop": true,
  "Bones": {
    "body": {
      "Rotation": {
        "0.0": [0, 0, 0],
        "0.5": [5, 0, 0],
        "1.0": [0, 0, 0]
      }
    },
    "leftArm": {
      "Rotation": {
        "0.0": [0, 0, 0],
        "0.25": [-30, 0, 0],
        "0.5": [0, 0, 0],
        "0.75": [30, 0, 0],
        "1.0": [0, 0, 0]
      }
    },
    "rightArm": {
      "Rotation": {
        "0.0": [0, 0, 0],
        "0.25": [30, 0, 0],
        "0.5": [0, 0, 0],
        "0.75": [-30, 0, 0],
        "1.0": [0, 0, 0]
      }
    }
  }
}
```

### Animation Properties

| Property | Type | Description |
|----------|------|-------------|
| `Length` | Float | Duration in seconds |
| `Loop` | Boolean | Loop animation |
| `Bones` | Object | Per-bone keyframes |

### Keyframe Channels

| Channel | Type | Description |
|---------|------|-------------|
| `Rotation` | Array | Rotation [X, Y, Z] degrees |
| `Position` | Array | Position offset [X, Y, Z] |
| `Scale` | Array | Scale [X, Y, Z] |

## Sounds

### Sound Formats

| Format | Use Case |
|--------|----------|
| OGG | Music, ambient (recommended) |
| WAV | Short sound effects |

### Sound Event

**File**: `custom_sound.soundevent`

```json
{
  "Sounds": [
    {
      "Path": "MyPlugin/Sounds/custom/sound1",
      "Weight": 1.0
    },
    {
      "Path": "MyPlugin/Sounds/custom/sound2",
      "Weight": 0.5
    }
  ],
  "Volume": {
    "Min": 0.8,
    "Max": 1.0
  },
  "Pitch": {
    "Min": 0.9,
    "Max": 1.1
  },
  "Category": "Effects",
  "Subtitle": {
    "en-US": "Custom sound plays"
  }
}
```

### Sound Set

**File**: `custom_soundset.soundset`

```json
{
  "Sounds": {
    "break": "MyPlugin/SoundEvents/custom_break",
    "place": "MyPlugin/SoundEvents/custom_place",
    "step": "MyPlugin/SoundEvents/custom_step",
    "hit": "MyPlugin/SoundEvents/custom_hit"
  }
}
```

### Block Sound Set

**File**: `custom_blocksound.blocksound`

```json
{
  "Break": {
    "Sound": "MyPlugin/SoundEvents/metal_break",
    "Volume": 1.0,
    "Pitch": 1.0
  },
  "Place": {
    "Sound": "MyPlugin/SoundEvents/metal_place",
    "Volume": 1.0
  },
  "Step": {
    "Sound": "MyPlugin/SoundEvents/metal_step",
    "Volume": 0.5
  },
  "Fall": {
    "Sound": "MyPlugin/SoundEvents/metal_fall"
  }
}
```

### Sound Categories

| Category | Description |
|----------|-------------|
| `Master` | All sounds |
| `Music` | Background music |
| `Effects` | Sound effects |
| `Ambient` | Environmental sounds |
| `Voice` | Voice/dialogue |
| `UI` | Interface sounds |
| `Weather` | Weather sounds |

## Particles

**File**: `custom_particle.particle`

```json
{
  "Texture": "MyPlugin/Textures/particles/sparkle",
  "MaxParticles": 100,
  "EmissionRate": 10,
  "Lifetime": {
    "Min": 0.5,
    "Max": 1.5
  },
  "Size": {
    "Start": 0.2,
    "End": 0.0
  },
  "Color": {
    "Start": { "R": 1.0, "G": 0.8, "B": 0.2, "A": 1.0 },
    "End": { "R": 1.0, "G": 0.2, "B": 0.0, "A": 0.0 }
  },
  "Velocity": {
    "Min": [-0.5, 1.0, -0.5],
    "Max": [0.5, 2.0, 0.5]
  },
  "Gravity": -0.5,
  "Collision": false,
  "BlendMode": "Additive"
}
```

### Particle Properties

| Property | Type | Description |
|----------|------|-------------|
| `Texture` | String | Particle texture |
| `MaxParticles` | Integer | Maximum active particles |
| `EmissionRate` | Float | Particles per second |
| `Lifetime` | Range | Particle lifespan |
| `Size` | Range/Gradient | Size over lifetime |
| `Color` | Color/Gradient | Color over lifetime |
| `Velocity` | Range | Initial velocity |
| `Gravity` | Float | Gravity effect |
| `Collision` | Boolean | Collide with blocks |
| `BlendMode` | Enum | `Alpha`, `Additive`, `Multiply` |

### Block Particle

**File**: `custom_blockparticle.blockparticle`

```json
{
  "Break": {
    "Particle": "MyPlugin/Particles/shatter",
    "Count": 30
  },
  "Step": {
    "Particle": "MyPlugin/Particles/dust",
    "Count": 3
  },
  "Ambient": {
    "Particle": "MyPlugin/Particles/glow",
    "Rate": 1,
    "Radius": 0.5
  }
}
```

## Trails

**File**: `custom_trail.trail`

```json
{
  "Texture": "MyPlugin/Textures/trails/slash",
  "Width": 0.5,
  "Length": 10,
  "Lifetime": 0.3,
  "Color": {
    "Start": { "R": 1.0, "G": 1.0, "B": 1.0, "A": 1.0 },
    "End": { "R": 1.0, "G": 1.0, "B": 1.0, "A": 0.0 }
  },
  "BlendMode": "Additive",
  "AttachPoint": "weapon_tip"
}
```

## Asset Inheritance

Assets can inherit from parents:

```json
{
  "Parent": "Hytale:Stone",
  "DisplayName": { "en-US": "Enchanted Stone" },
  "LightLevel": 5
}
```

### Inheritance Rules

1. Child inherits all parent properties
2. Child can override any property
3. Nested objects merge (not replace)
4. Arrays replace (not merge)

## Asset Tags

Categorize assets with tags:

```json
{
  "Tags": {
    "Category": ["Building", "Decorative"],
    "Material": ["Stone"],
    "Origin": ["Natural", "Cave"]
  }
}
```

### Tag Queries

Used in spawning, loot tables, etc.:

```json
{
  "Blocks": {
    "MatchAll": ["Material:Stone"],
    "MatchAny": ["Category:Natural", "Origin:Cave"],
    "Exclude": ["Category:Artificial"]
  }
}
```

## Localization

**File**: `lang/en-US.json`

```json
{
  "item.myPlugin.customItem.name": "Custom Item",
  "item.myPlugin.customItem.description": "A special custom item",
  "block.myPlugin.customBlock.name": "Custom Block",
  "entity.myPlugin.customEntity.name": "Custom Creature"
}
```

### Localization Keys

| Pattern | Example |
|---------|---------|
| `item.{plugin}.{id}.name` | `item.myPlugin.sword.name` |
| `block.{plugin}.{id}.name` | `block.myPlugin.ore.name` |
| `entity.{plugin}.{id}.name` | `entity.myPlugin.mob.name` |
| `ui.{plugin}.{key}` | `ui.myPlugin.menuTitle` |

## Registering Assets in Plugin

```java
@Override
protected void setup() {
    // Asset pack is auto-registered if manifest.json has:
    // "IncludesAssetPack": true
    
    // Listen for asset loading
    getEventRegistry().register(
        LoadedAssetsEvent.class,
        BlockType.class,
        this::onBlockTypesLoaded
    );
    
    getEventRegistry().register(
        LoadedAssetsEvent.class,
        Item.class,
        this::onItemsLoaded
    );
}

private void onBlockTypesLoaded(LoadedAssetsEvent<BlockType> event) {
    // Access loaded block types
    for (BlockType block : event.getLoadedAssets()) {
        getLogger().atInfo().log("Loaded block: %s", block.getId());
    }
}
```

## Hot Reloading

Assets support hot-reload during development:

```
/reload assets
```

Listen for reload events:

```java
getEventRegistry().register(
    AssetStoreMonitorEvent.class,
    this::onAssetReload
);

private void onAssetReload(AssetStoreMonitorEvent event) {
    if (event.getAssetStore().getAssetClass() == BlockType.class) {
        getLogger().atInfo().log("Block types reloaded");
        // Re-initialize dependent systems
    }
}
```

## Custom Asset Store

Register entirely new asset types:

```java
public class MyCustomAsset implements JsonAssetWithMap<String, DefaultAssetMap<String, MyCustomAsset>> {
    public static final AssetBuilderCodec<String, MyCustomAsset> CODEC = 
        AssetBuilderCodec.builder(MyCustomAsset.class, "MyCustomAsset")
            .appendRequired(Codec.STRING.fieldOf("Name"), MyCustomAsset::getName, (a, v) -> a.name = v)
            .appendOptional(Codec.INT.fieldOf("Value"), MyCustomAsset::getValue, (a, v) -> a.value = v, 0)
            .build();
    
    private String id;
    private String name;
    private int value;
    
    @Override
    public String getId() { return id; }
    public String getName() { return name; }
    public int getValue() { return value; }
}

// Register in plugin
@Override
protected void setup() {
    HytaleAssetStore<String, MyCustomAsset, DefaultAssetMap<String, MyCustomAsset>> store = 
        new HytaleAssetStore<>(
            MyCustomAsset.class,
            "MyCustomAssets",      // Directory name
            ".mycustomasset",      // File extension
            MyCustomAsset.CODEC,
            DefaultAssetMap::new
        );
    
    getAssetRegistry().register(store);
}
```

## Troubleshooting

### Textures Not Loading

1. Check file path matches reference
2. Verify PNG format and dimensions
3. Ensure pack.json is valid
4. Check console for loading errors

### Models Not Displaying

1. Verify model JSON syntax
2. Check texture references exist
3. Ensure bone hierarchy is valid
4. Test with simpler model first

### Sounds Not Playing

1. Check OGG/WAV format compatibility
2. Verify sound event references
3. Check volume and category settings
4. Ensure sound files exist at path

### Asset Inheritance Not Working

1. Verify Parent path is correct
2. Check parent asset loads first
3. Ensure pack dependencies are set

See `references/asset-formats.md` for detailed format specs.
See `references/texture-specs.md` for texture requirements.
