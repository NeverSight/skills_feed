---
name: blockbench-pbr-materials
description: Create and manage PBR (Physically Based Rendering) materials in Blockbench using MCP tools. Use when working with texture_set.json files, creating normal/height/MER maps, configuring material properties for Minecraft Bedrock RTX, or setting up multi-channel texture workflows.
---

# Blockbench PBR Materials

Create and manage PBR materials for Minecraft Bedrock RTX and other PBR workflows.

## Available Tools

| Tool | Purpose |
|------|---------|
| `create_pbr_material` | Create new PBR material with texture channels |
| `configure_material` | Configure material properties |
| `list_materials` | List all PBR materials |
| `get_material_info` | Get detailed material info |
| `import_texture_set` | Import texture_set.json file |
| `assign_texture_channel` | Assign texture to PBR channel |
| `save_material_config` | Export texture_set.json |

## PBR Channels

| Channel | Description | Format |
|---------|-------------|--------|
| `color` | Base color/albedo | RGB texture |
| `normal` | Normal map for surface detail | RGB (tangent space) |
| `height` | Heightmap for parallax/displacement | Grayscale |
| `mer` | Metalness/Emissive/Roughness packed | R=Metal, G=Emissive, B=Roughness |

## Quick Start

### Create Basic PBR Material

```
create_pbr_material: name="stone_pbr", textures={
  color: "stone_color",
  normal: "stone_normal"
}
```

### Create Full Material

```
create_pbr_material: name="gold_block", textures={
  color: "gold_color",
  normal: "gold_normal",
  height: "gold_height",
  mer: "gold_mer"
}
```

## Material Configuration

### Set Material Properties

```
configure_material: material_id="stone_pbr", config={
  metalness_emissive_roughness: {
    metalness: 0.0,
    emissive: 0.0,
    roughness: 0.8
  }
}
```

### Metallic Material

```
configure_material: material_id="gold_block", config={
  metalness_emissive_roughness: {
    metalness: 1.0,
    emissive: 0.0,
    roughness: 0.3
  }
}
```

### Emissive Material (Glowing)

```
configure_material: material_id="glowstone", config={
  metalness_emissive_roughness: {
    metalness: 0.0,
    emissive: 1.0,
    roughness: 0.9
  }
}
```

## Texture Assignment

### Assign Individual Channel

```
assign_texture_channel: material_id="stone_pbr", channel="height",
  texture_id="stone_heightmap"
```

### Replace Channel

```
assign_texture_channel: material_id="stone_pbr", channel="normal",
  texture_id="stone_normal_v2"
```

## Import/Export

### Import texture_set.json

```
import_texture_set: file_path="C:/packs/stone_texture_set.json"
```

### Export texture_set.json

```
save_material_config: material_id="stone_pbr",
  output_path="C:/packs/textures/stone_texture_set.json"
```

## Querying Materials

### List All Materials

```
list_materials
# Returns: [{uuid, name, textureCount, hasColor, hasNormal, hasHeight, hasMER}]
```

### Get Material Details

```
get_material_info: material_id="stone_pbr"
# Returns full channel assignments and config
```

## MER Texture Format

The MER channel packs three properties into RGB:

- **R (Red)**: Metalness (0=dielectric, 1=metal)
- **G (Green)**: Emissive intensity (0=none, 1=full glow)
- **B (Blue)**: Roughness (0=smooth/shiny, 1=rough/matte)

### Creating MER Texture

```
# Create blank MER texture
create_texture: name="block_mer", width=16, height=16,
  fill_color=[0, 0, 204, 255]  # Non-metal, no glow, 80% rough

# Paint metallic areas (R channel)
paint_with_brush: texture_id="block_mer", coordinates=[{x: 8, y: 8}],
  brush_settings={color: "#FF0000", size: 4}  # Metallic spot

# Paint glowing areas (G channel)
paint_with_brush: texture_id="block_mer", coordinates=[{x: 4, y: 4}],
  brush_settings={color: "#00FF00", size: 2, blend_mode: "add"}
```

## Common Material Types

### Stone/Rock

```
create_pbr_material: name="stone", textures={color: "stone_color", normal: "stone_normal"}
configure_material: material_id="stone", config={
  metalness_emissive_roughness: {metalness: 0, emissive: 0, roughness: 0.9}
}
```

### Metal (Gold, Iron)

```
create_pbr_material: name="gold", textures={color: "gold_color", normal: "gold_normal", mer: "gold_mer"}
configure_material: material_id="gold", config={
  metalness_emissive_roughness: {metalness: 1.0, emissive: 0, roughness: 0.25}
}
```

### Glass/Crystal

```
create_pbr_material: name="glass", textures={color: "glass_color"}
configure_material: material_id="glass", config={
  metalness_emissive_roughness: {metalness: 0, emissive: 0, roughness: 0.05}
}
```

### Glowing Block

```
create_pbr_material: name="lamp", textures={color: "lamp_color", mer: "lamp_mer"}
configure_material: material_id="lamp", config={
  metalness_emissive_roughness: {metalness: 0, emissive: 1.0, roughness: 0.8}
}
```

### Subsurface Scattering (Bedrock 1.21.30+)

```
configure_material: material_id="leaves", config={
  subsurface_scattering: {
    red: 0.3,
    green: 0.8,
    blue: 0.2
  }
}
```

## Workflow Example

### Complete Block Material

```
# 1. Create base textures
create_texture: name="brick_color", width=16, height=16
create_texture: name="brick_normal", width=16, height=16, fill_color="#8080FF"
create_texture: name="brick_mer", width=16, height=16, fill_color=[0, 0, 200, 255]

# 2. Paint textures (color, normal, mer)
paint_with_brush: texture_id="brick_color", ...
paint_with_brush: texture_id="brick_normal", ...

# 3. Create material
create_pbr_material: name="brick", textures={
  color: "brick_color",
  normal: "brick_normal",
  mer: "brick_mer"
}

# 4. Configure
configure_material: material_id="brick", config={
  metalness_emissive_roughness: {metalness: 0, emissive: 0, roughness: 0.85}
}

# 5. Export
save_material_config: material_id="brick", output_path="./textures/brick_texture_set.json"
```

## Tips

- Normal maps use tangent space (blue-ish color, RGB where B is up)
- Height maps are grayscale (white=high, black=low)
- MER channels can be painted separately or as a combined texture
- Use `list_materials` to see what's available
- Always test in-game with RTX enabled for accurate preview
- Roughness 0 = mirror-like, Roughness 1 = completely diffuse
