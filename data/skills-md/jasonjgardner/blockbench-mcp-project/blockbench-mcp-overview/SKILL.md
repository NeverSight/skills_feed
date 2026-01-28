---
name: blockbench-mcp-overview
description: Overview of the Blockbench MCP server tools, resources, and prompts. Use to understand the full MCP capability set, learn how tools work together, or when starting a new Blockbench project. Covers all domains (modeling, animation, texturing, PBR, UI, camera) and their MCP interfaces.
---

# Blockbench MCP Overview

Complete guide to the Blockbench MCP server for AI-assisted 3D modeling.

## What is Blockbench MCP?

An MCP server that exposes Blockbench functionality to AI agents through:
- **Tools**: Actions that create, modify, or query the 3D model
- **Resources**: Read-only data endpoints for model information
- **Prompts**: Reusable guidance for specific workflows

## Tool Categories

| Domain | Tools | Purpose |
|--------|-------|---------|
| Animation | 7 | Keyframes, rigs, curves, timeline |
| Camera | 3 | Screenshots, camera control |
| Cubes | 2 | Cube creation and modification |
| Elements | 5 | Groups, outliner, duplication |
| Import | 1 | GeoJSON import |
| Mesh | 11 | Spheres, cylinders, extrusion, vertices |
| Paint | 12 | Brushes, fill, shapes, layers |
| Texture | 13 | Textures, PBR materials |
| UI | 4 | Actions, evaluation, dialogs |
| UV | 3 | UV mapping |
| Hytale | 12 | Hytale-specific (requires plugin) |

## Resources

| Resource | URI Pattern | Data |
|----------|-------------|------|
| projects | `projects://{id}` | Project info, formats |
| textures | `textures://{id}` | Texture metadata |
| nodes | `nodes://{id}` | 3D node data |
| hytale-format | `hytale://format` | Hytale format info |
| hytale-attachments | `hytale://attachments/{id}` | Attachment collections |
| hytale-pieces | `hytale://pieces/{id}` | Attachment pieces |
| hytale-cubes | `hytale://cubes/{id}` | Hytale cube properties |

## Prompts

| Prompt | Purpose |
|--------|---------|
| `blockbench_native_apis` | Blockbench v5.0 API security guide |
| `blockbench_code_eval_safety` | Safe code evaluation patterns |
| `model_creation_strategy` | Model creation guidance |
| `hytale_model_creation` | Hytale modeling guide |
| `hytale_animation_workflow` | Hytale animation guide |
| `hytale_attachments` | Hytale attachments guide |

## Quick Start Workflows

### Create a Simple Model

```
# 1. Create project
create_project: name="my_model", format="bedrock"

# 2. Create texture
create_texture: name="skin", width=64, height=64

# 3. Add bone structure
add_group: name="root", origin=[0, 0, 0]
add_group: name="body", parent="root", origin=[0, 12, 0]

# 4. Add geometry
place_cube: elements=[{name: "torso", from: [-4, 12, -2], to: [4, 24, 2]}], group="body"

# 5. Apply texture
apply_texture: id="torso", texture="skin"

# 6. View result
capture_screenshot
```

### Create and Animate

```
# 1. Build model (see above)

# 2. Create animation
create_animation: name="idle", animation_length=2.0, loop=true

# 3. Add keyframes
manage_keyframes: bone_name="body", channel="rotation",
  keyframes=[
    {time: 0, values: [0, 0, 0]},
    {time: 1.0, values: [0, 5, 0]},
    {time: 2.0, values: [0, 0, 0]}
  ]

# 4. Play animation
animation_timeline: action="play"
```

### Paint a Texture

```
# 1. Create texture
create_texture: name="block", width=16, height=16, fill_color="#8B4513"

# 2. Add details
draw_shape_tool: shape="rectangle", start={x: 2, y: 2}, end={x: 14, y: 14}, color="#A0522D"
paint_with_brush: coordinates=[{x: 8, y: 8}], brush_settings={color: "#654321", size: 2}

# 3. View texture
get_texture: texture="block"
```

## Tool Patterns

### Information Gathering

```
list_outline            # View model hierarchy
list_textures           # View textures
list_materials          # View PBR materials
hytale_get_format_info  # View Hytale format (if active)
```

### Modification Pattern

Most modification tools follow:
1. Identify target by ID or name
2. Specify changes
3. Changes are recorded for undo

### Screenshot Workflow

```
set_camera_angle: position=[0, 20, 50], rotation=[0, 0, 0], projection="perspective"
capture_screenshot      # 3D view only
capture_app_screenshot  # Entire Blockbench window
```

### Evaluation (Advanced)

```
risky_eval: code="Cube.all.length"  # Query Blockbench directly
trigger_action: action="undo"       # Trigger Blockbench actions
```

## Domain Integration

### Model + Texture

```
# Create model
place_cube: elements=[{name: "block", from: [0,0,0], to: [16,16,16]}]

# Create texture
create_texture: name="block_tex", width=16, height=16

# Paint texture
paint_fill_tool: texture_id="block_tex", x=0, y=0, color="#00FF00", fill_mode="element"

# Apply
apply_texture: id="block", texture="block_tex"
```

### Model + Animation

```
# Create bone hierarchy (important for animation)
add_group: name="root", origin=[0, 0, 0]
add_group: name="arm", parent="root", origin=[4, 12, 0]

# Add geometry to bones
place_cube: elements=[{name: "arm_geo", from: [0, 0, -1], to: [2, 10, 1]}], group="arm"

# Animate the bone
create_animation: name="wave", animation_length=1.0
manage_keyframes: bone_name="arm", channel="rotation",
  keyframes=[{time: 0, values: [0, 0, 0]}, {time: 0.5, values: [0, 0, 90]}]
```

### PBR Material Workflow

```
# Create textures for each channel
create_texture: name="stone_color", width=16, height=16
create_texture: name="stone_normal", width=16, height=16, fill_color="#8080FF"
create_texture: name="stone_mer", width=16, height=16, fill_color=[0, 0, 200, 255]

# Create material
create_pbr_material: name="stone", textures={
  color: "stone_color",
  normal: "stone_normal",
  mer: "stone_mer"
}

# Configure
configure_material: material_id="stone", config={
  metalness_emissive_roughness: {metalness: 0, emissive: 0, roughness: 0.9}
}
```

## Error Handling

Tools throw descriptive errors with suggestions:

- **Element not found**: "Use list_outline tool to see available elements"
- **Texture not found**: "Use list_textures tool to see available textures"
- **Invalid format**: "Current project is not using a Hytale format"

## Best Practices

1. **Query first**: Use `list_*` tools to understand current state
2. **Build hierarchy**: Create bone structure before geometry
3. **Set origins**: Place group origins at pivot points for animation
4. **Name elements**: Use descriptive names for easy reference
5. **Validate**: Use `hytale_validate_model` for Hytale projects
6. **Screenshot**: Capture progress with `capture_screenshot`

## Tool Status

- **stable**: Production-ready
- **experimental**: Working but may change

Most tools are experimental but functional. Check tool annotations for current status.
