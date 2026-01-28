---
name: hytale-custom-blocks
description: Create custom block types for Hytale with textures, physics, states, farming, and interactions. Use when asked to "add a custom block", "create a new block type", "make blocks farmable", "add block interactions", or "configure block physics".
metadata:
  author: Liam Robinson (MnkyArts)
  version: "1.0.0"
---

# Creating Custom Hytale Blocks

Complete guide for defining custom block types with all available properties and configurations.

## When to use this skill

Use this skill when:
- Creating new block types
- Configuring block rendering (textures, models)
- Setting up block physics (support, bouncy, climbable)
- Making blocks farmable with growth stages
- Adding crafting benches
- Defining block interactions
- Setting up block sounds and particles
- Managing block states

## Block Asset Structure

Blocks are defined as JSON assets in your plugin's asset pack:

```
my-plugin/
└── assets/
    └── Server/
        └── Content/
            └── BlockTypes/
                ├── my_custom_block.blocktype
                ├── my_crop.blocktype
                └── my_bench.blocktype
```

## Basic Block Definition

**File**: `my_custom_block.blocktype`

```json
{
  "DisplayName": {
    "en-US": "Custom Block"
  },
  "Description": {
    "en-US": "A custom block with special properties"
  },
  "DrawType": "Cube",
  "Texture": "MyPlugin/Textures/custom_block",
  "Material": "Stone",
  "Tags": {
    "Category": ["Building", "Decorative"]
  }
}
```

## Block Properties Reference

### Core Properties

| Property | Type | Description |
|----------|------|-------------|
| `DisplayName` | LocalizedString | Localized display name |
| `Description` | LocalizedString | Localized description |
| `Parent` | String | Inherit from another block type |
| `Tags` | Object | Category tags for filtering |

### Rendering Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `DrawType` | Enum | `Cube` | `Cube`, `Model`, `Empty` |
| `Texture` | String | - | Texture path for cube rendering |
| `TextureTop` | String | - | Top face texture |
| `TextureSide` | String | - | Side faces texture |
| `TextureBottom` | String | - | Bottom face texture |
| `Model` | String | - | Model asset for DrawType=Model |
| `Shader` | String | - | Custom shader |
| `Opacity` | Float | 1.0 | Block opacity (0-1) |
| `AlphaBlend` | Boolean | false | Enable alpha blending |
| `RandomRotation` | Boolean | false | Random Y rotation on place |
| `VariantRotation` | Enum | - | Rotation variant mode |
| `FlipType` | Enum | - | Random flipping mode |
| `RotationOffset` | Float | 0 | Rotation offset in degrees |

### Physics Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Material` | String | - | Physics material type |
| `IsSolid` | Boolean | true | Collision enabled |
| `IsReplaceable` | Boolean | false | Can be replaced when placing |
| `HasGravity` | Boolean | false | Falls like sand |
| `BlockFaceSupport` | Object | - | Support provided to neighbors |
| `RequiredBlockFaceSupport` | Object | - | Support needed from neighbors |

### Movement Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `Climbable` | Boolean | false | Can be climbed (ladders) |
| `Bouncy` | Float | 0 | Bounce factor (0-1) |
| `Drag` | Float | 0 | Movement drag |
| `Friction` | Float | 1 | Surface friction |
| `SpeedMultiplier` | Float | 1 | Walk speed multiplier |

### Behavior Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `IsUsable` | Boolean | false | Right-click interaction |
| `IsStackable` | Boolean | true | Can be placed adjacent |
| `ItemId` | String | - | Item dropped when broken |
| `LightLevel` | Integer | 0 | Light emission (0-15) |
| `LightColor` | Color | white | Light color |
| `Flammable` | Boolean | false | Can catch fire |
| `FlammableSpread` | Integer | 0 | Fire spread rate |

## Draw Types

### Cube (Default)

Standard voxel block with 6-sided textures:

```json
{
  "DrawType": "Cube",
  "Texture": "MyPlugin/Textures/stone",
  "TextureTop": "MyPlugin/Textures/stone_top"
}
```

### Model

Custom 3D model:

```json
{
  "DrawType": "Model",
  "Model": "MyPlugin/Models/custom_model",
  "BoundingBox": "MyPlugin/BoundingBoxes/custom_box"
}
```

### Empty

Invisible block (air-like, for logic):

```json
{
  "DrawType": "Empty",
  "IsSolid": false
}
```

## Block Physics System

### Block Face Support

Define which faces provide support:

```json
{
  "BlockFaceSupport": {
    "Top": {
      "Type": "Full",
      "SupportStrength": 100
    },
    "Bottom": {
      "Type": "Full",
      "SupportStrength": 100
    },
    "North": { "Type": "Full" },
    "South": { "Type": "Full" },
    "East": { "Type": "Full" },
    "West": { "Type": "Full" }
  }
}
```

**Support Types**: `Full`, `Partial`, `None`, `Center`

### Required Support

Define what support the block needs:

```json
{
  "RequiredBlockFaceSupport": {
    "Bottom": [
      {
        "Type": "Full",
        "Match": "REQUIRED"
      }
    ]
  }
}
```

**Match Types**:
- `REQUIRED` - Must have this support
- `IGNORED` - Don't care
- `DISALLOWED` - Must NOT have this support

### Gravity Blocks

```json
{
  "HasGravity": true,
  "GravityDelay": 5,
  "PhysicsDrop": {
    "GatherType": "Shovel",
    "Drops": [
      {
        "Item": "minecraft:sand",
        "Quantity": 1
      }
    ]
  }
}
```

## Block Gathering/Breaking

### Breaking Configuration

```json
{
  "Gathering": {
    "Breaking": {
      "GatherType": "Pickaxe",
      "Power": 2,
      "Quality": 1,
      "Drops": [
        {
          "Item": "my_plugin:custom_ore",
          "Quantity": {
            "Min": 1,
            "Max": 3
          },
          "Chance": 1.0
        }
      ]
    },
    "Harvest": {
      "GatherType": "Hoe",
      "Quality": 1,
      "Drops": [
        {
          "Item": "my_plugin:seeds",
          "Quantity": 1
        }
      ]
    },
    "SoftBlock": {
      "Enabled": true,
      "Drops": [
        {
          "Item": "my_plugin:dust",
          "Quantity": 1
        }
      ]
    }
  }
}
```

**Gather Types**: `Hand`, `Pickaxe`, `Axe`, `Shovel`, `Hoe`, `Sword`

## Block States

Define different visual/behavioral states:

```json
{
  "States": {
    "powered": {
      "Values": ["true", "false"],
      "Default": "false"
    },
    "facing": {
      "Values": ["north", "south", "east", "west"],
      "Default": "north"
    }
  },
  "StateData": {
    "powered=true,facing=north": {
      "Model": "MyPlugin/Models/powered_north"
    },
    "powered=true,facing=south": {
      "Model": "MyPlugin/Models/powered_south"
    },
    "powered=false": {
      "Model": "MyPlugin/Models/unpowered"
    }
  }
}
```

## Farming Blocks

Create crops with growth stages:

```json
{
  "DisplayName": { "en-US": "Wheat" },
  "DrawType": "Model",
  "FarmingData": {
    "Stages": [
      {
        "Model": "Hytale/Models/Crops/wheat_stage_0",
        "GrowthTime": 300,
        "LightRequired": 8
      },
      {
        "Model": "Hytale/Models/Crops/wheat_stage_1",
        "GrowthTime": 300,
        "LightRequired": 8
      },
      {
        "Model": "Hytale/Models/Crops/wheat_stage_2",
        "GrowthTime": 300,
        "LightRequired": 8
      },
      {
        "Model": "Hytale/Models/Crops/wheat_stage_3",
        "GrowthTime": 0,
        "LightRequired": 0,
        "IsFinalStage": true
      }
    ],
    "Modifiers": {
      "Biome": {
        "Plains": 1.2,
        "Desert": 0.5
      },
      "Weather": {
        "Rain": 1.3
      }
    },
    "SpreadSettings": {
      "Enabled": true,
      "Chance": 0.1,
      "Radius": 2
    },
    "RequiredSoil": ["Hytale:Farmland", "Hytale:Dirt"]
  }
}
```

## Crafting Benches

Create blocks that open crafting interfaces:

### Standard Crafting Bench

```json
{
  "DisplayName": { "en-US": "Workbench" },
  "DrawType": "Model",
  "Model": "MyPlugin/Models/workbench",
  "IsUsable": true,
  "Bench": {
    "Type": "Crafting",
    "Categories": ["MyPlugin:BasicCrafting", "MyPlugin:AdvancedCrafting"],
    "GridSize": {
      "Width": 3,
      "Height": 3
    },
    "OutputSlots": 1
  }
}
```

### Processing Bench

```json
{
  "Bench": {
    "Type": "Processing",
    "Categories": ["MyPlugin:Smelting"],
    "InputSlots": 1,
    "FuelSlots": 1,
    "OutputSlots": 1,
    "ProcessingTime": 200,
    "FuelTypes": ["Hytale:Coal", "Hytale:Charcoal"]
  }
}
```

### Diagram Crafting Bench

```json
{
  "Bench": {
    "Type": "DiagramCrafting",
    "Categories": ["MyPlugin:BlueprintCrafting"],
    "DiagramSlot": true,
    "MaterialSlots": 6,
    "OutputSlots": 1
  }
}
```

## Block Sounds

```json
{
  "BlockSound": "MyPlugin/BlockSounds/metal",
  "AmbientSound": {
    "Sound": "MyPlugin/Sounds/machine_hum",
    "Volume": 0.5,
    "Radius": 8
  }
}
```

**Standard BlockSound sets**: `Stone`, `Wood`, `Metal`, `Glass`, `Dirt`, `Sand`, `Grass`, `Gravel`, `Snow`, `Wool`

## Block Particles

```json
{
  "BreakParticle": "MyPlugin/Particles/stone_break",
  "AmbientParticle": {
    "Particle": "MyPlugin/Particles/sparkle",
    "SpawnRate": 2,
    "Radius": 0.5
  },
  "FootstepParticle": "MyPlugin/Particles/dust"
}
```

## Block Interactions

Define custom interactions via the Interaction system:

```json
{
  "Interactions": {
    "Use": "MyPlugin:MyBlockInteraction",
    "Attack": "MyPlugin:MyBlockAttackInteraction"
  }
}
```

### Interaction Types

| Type | Trigger |
|------|---------|
| `Use` | Right-click |
| `Attack` | Left-click |
| `Look` | Look at block |
| `Touch` | Walk into block |

## Complete Example: Custom Ore

```json
{
  "DisplayName": {
    "en-US": "Mythril Ore"
  },
  "Description": {
    "en-US": "A rare ore found deep underground"
  },
  "DrawType": "Cube",
  "Texture": "MyPlugin/Textures/mythril_ore",
  "Material": "Stone",
  "LightLevel": 3,
  "LightColor": { "R": 0.5, "G": 0.8, "B": 1.0 },
  "Tags": {
    "Category": ["Ore", "Mining"]
  },
  "Gathering": {
    "Breaking": {
      "GatherType": "Pickaxe",
      "Power": 4,
      "Quality": 3,
      "Drops": [
        {
          "Item": "MyPlugin:RawMythril",
          "Quantity": { "Min": 1, "Max": 2 }
        }
      ]
    }
  },
  "BlockFaceSupport": {
    "Top": { "Type": "Full" },
    "Bottom": { "Type": "Full" },
    "North": { "Type": "Full" },
    "South": { "Type": "Full" },
    "East": { "Type": "Full" },
    "West": { "Type": "Full" }
  },
  "BlockSound": "Hytale/BlockSounds/Stone",
  "BreakParticle": "MyPlugin/Particles/mythril_break",
  "AmbientParticle": {
    "Particle": "MyPlugin/Particles/mythril_sparkle",
    "SpawnRate": 0.5
  }
}
```

## Complete Example: Door Block

```json
{
  "DisplayName": { "en-US": "Wooden Door" },
  "DrawType": "Model",
  "Material": "Wood",
  "IsUsable": true,
  "States": {
    "open": {
      "Values": ["true", "false"],
      "Default": "false"
    },
    "facing": {
      "Values": ["north", "south", "east", "west"],
      "Default": "north"
    },
    "half": {
      "Values": ["upper", "lower"],
      "Default": "lower"
    }
  },
  "StateData": {
    "open=false,facing=north,half=lower": {
      "Model": "MyPlugin/Models/door_closed_lower_n"
    },
    "open=true,facing=north,half=lower": {
      "Model": "MyPlugin/Models/door_open_lower_n"
    }
  },
  "IsSolid": false,
  "Interactions": {
    "Use": "MyPlugin:DoorInteraction"
  },
  "PlacementSettings": {
    "RotationMode": "PlayerFacing",
    "MultiBlock": {
      "Pattern": [
        { "Offset": [0, 1, 0], "State": "half=upper" }
      ]
    }
  },
  "BlockSound": "Hytale/BlockSounds/Wood",
  "RequiredBlockFaceSupport": {
    "Bottom": [
      { "Type": "Full", "Match": "REQUIRED" }
    ]
  }
}
```

## Registering Blocks from Plugin Code

For dynamic block registration:

```java
@Override
protected void setup() {
    // Listen for block type loading
    getEventRegistry().register(
        LoadedAssetsEvent.class, 
        BlockType.class, 
        this::onBlockTypesLoaded
    );
}

private void onBlockTypesLoaded(LoadedAssetsEvent<BlockType> event) {
    // Access loaded block types
    BlockType myBlock = event.getAssetStore().get("MyPlugin:my_custom_block");
    if (myBlock != null) {
        getLogger().atInfo().log("Custom block loaded: %s", myBlock.getDisplayName());
    }
}
```

## Block Events

Handle block-related events:

```java
@Override
protected void setup() {
    // Block break event
    getEntityStoreRegistry().registerSystem(new BreakBlockHandler());
    
    // Block place event  
    getEntityStoreRegistry().registerSystem(new PlaceBlockHandler());
    
    // Block use event
    getEntityStoreRegistry().registerSystem(new UseBlockHandler());
}

public class BreakBlockHandler extends EntityEventSystem<EntityStore, BreakBlockEvent> {
    public BreakBlockHandler() {
        super(BreakBlockEvent.class);
    }
    
    @Override
    public void handle(int index, ArchetypeChunk<EntityStore> chunk, 
                       Store<EntityStore> store, CommandBuffer<EntityStore> buffer,
                       BreakBlockEvent event) {
        BlockType blockType = event.getBlockType();
        Vector3i position = event.getPosition();
        
        // Custom logic here
        if (blockType.getId().equals("MyPlugin:protected_block")) {
            event.setCancelled(true);
        }
    }
}
```

## Troubleshooting

### Block Not Rendering

1. Verify `DrawType` is correct
2. Check texture path exists
3. Ensure asset pack is registered in manifest

### Block Breaking Instantly

1. Check `Material` property
2. Verify `GatherType` and `Power` settings
3. Ensure tool requirements are set

### Physics Not Working

1. Verify `BlockFaceSupport` configuration
2. Check `RequiredBlockFaceSupport` matches
3. Ensure `IsSolid` is true

See `references/block-materials.md` for material properties.
See `references/block-states.md` for advanced state management.
