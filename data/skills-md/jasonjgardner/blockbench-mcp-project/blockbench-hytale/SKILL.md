---
name: blockbench-hytale
description: Create Hytale models and animations using Blockbench MCP tools. Use when working with Hytale character/prop formats, creating attachments, setting shading modes, using quads, or animating with visibility keyframes. Requires the Hytale Blockbench plugin to be installed.
---

# Blockbench Hytale

Create models for Hytale using Blockbench with the Hytale plugin.

**Prerequisite**: Hytale plugin must be installed in Blockbench.

## Available Tools

### Format & Validation
| Tool | Purpose |
|------|---------|
| `hytale_get_format_info` | Get format type, block size, node count |
| `hytale_validate_model` | Check against Hytale constraints |

### Cube Properties
| Tool | Purpose |
|------|---------|
| `hytale_set_cube_properties` | Set shading_mode, double_sided |
| `hytale_get_cube_properties` | Get Hytale cube properties |
| `hytale_set_cube_stretch` | Set stretch values [x, y, z] |
| `hytale_get_cube_stretch` | Get stretch values |
| `hytale_create_quad` | Create 2D plane with normal |

### Attachments
| Tool | Purpose |
|------|---------|
| `hytale_list_attachments` | List attachment collections |
| `hytale_set_attachment_piece` | Mark group as attachment piece |
| `hytale_list_attachment_pieces` | List all piece groups |

### Animation
| Tool | Purpose |
|------|---------|
| `hytale_create_visibility_keyframe` | Toggle bone visibility in animation |
| `hytale_set_animation_loop` | Set loop mode (loop/hold/once) |

## Resources

| Resource | URI | Purpose |
|----------|-----|---------|
| hytale-format | `hytale://format` | Format info |
| hytale-attachments | `hytale://attachments/{id}` | Attachment collections |
| hytale-pieces | `hytale://pieces/{id}` | Attachment pieces |
| hytale-cubes | `hytale://cubes/{id}` | Cubes with Hytale properties |

## Prompts

| Prompt | Arguments | Purpose |
|--------|-----------|---------|
| `hytale_model_creation` | format_type | Character/prop modeling guide |
| `hytale_animation_workflow` | animation_type | Animation creation guide |
| `hytale_attachments` | - | Attachments system guide |

## Hytale Formats

| Format | Block Size | Use Case |
|--------|------------|----------|
| `hytale_character` | 64px | Humanoids, creatures |
| `hytale_prop` | 32px | Items, weapons, decorations |

## Constraints

- **Max nodes**: 255 (groups + extra cubes)
- **Animation FPS**: 60
- **UV size**: Must match texture resolution

## Shading Modes

| Mode | Effect |
|------|--------|
| `standard` | Normal lighting (default) |
| `flat` | No lighting/shadows |
| `fullbright` | Always fully lit (emissive) |
| `reflective` | Reflective material |

## Quick Start

### Check Format

```
hytale_get_format_info
# Returns: formatType, blockSize, nodeCount, features
```

### Validate Model

```
hytale_validate_model
# Returns: valid, nodeCount, issues
```

## Cube Properties

### Set Shading Mode

```
hytale_set_cube_properties: cube_id="crystal", shading_mode="fullbright"
```

### Enable Double-Sided

```
hytale_set_cube_properties: cube_id="cloth", double_sided=true
```

### Set Stretch

```
hytale_set_cube_stretch: cube_id="arm", stretch=[1.2, 1.0, 1.0]
```

## Quads (2D Planes)

Create single-face planes:

```
hytale_create_quad: name="leaf",
  position=[0, 16, 0],
  normal="+Y",  # +X, -X, +Y, -Y, +Z, -Z
  size=[8, 8],
  double_sided=true
```

## Attachments

### List Attachments

```
hytale_list_attachments
```

### Mark as Attachment Piece

```
hytale_set_attachment_piece: group_name="hand_right", is_piece=true
```

This bone will attach to `hand_right` on the base model.

### List Attachment Pieces

```
hytale_list_attachment_pieces
```

## Animation

### Visibility Keyframe

Toggle bone visibility during animation:

```
hytale_create_visibility_keyframe:
  bone_name="weapon_sheathed",
  time=0.5,
  visible=false

hytale_create_visibility_keyframe:
  bone_name="weapon_drawn",
  time=0.5,
  visible=true
```

### Set Loop Mode

```
hytale_set_animation_loop: animation_id="walk", loop_mode="loop"
hytale_set_animation_loop: animation_id="attack", loop_mode="once"
hytale_set_animation_loop: animation_id="death", loop_mode="hold"
```

## Common Workflows

### Create Character Model

```
# 1. Create project (use bedrock format, Hytale format activates automatically)
create_project: name="goblin", format="bedrock"

# 2. Build bone hierarchy
add_group: name="root", origin=[0, 0, 0]
add_group: name="body", parent="root", origin=[0, 12, 0]
add_group: name="head", parent="body", origin=[0, 24, 0]
add_group: name="arm_left", parent="body", origin=[6, 22, 0]
add_group: name="arm_right", parent="body", origin=[-6, 22, 0]
add_group: name="hand_right", parent="arm_right", origin=[-8, 16, 0]

# 3. Add geometry
place_cube: elements=[{name: "torso", from: [-4, 12, -2], to: [4, 24, 2]}], group="body"

# 4. Set Hytale properties
hytale_set_cube_properties: cube_id="eyes", shading_mode="fullbright"

# 5. Validate
hytale_validate_model
```

### Create Weapon Attachment

```
# 1. Create attachment structure
add_group: name="hand_right", origin=[0, 0, 0]

# 2. Add weapon geometry
place_cube: elements=[{name: "blade", from: [-0.5, 0, -0.5], to: [0.5, 24, 0.5]}], group="hand_right"

# 3. Mark as attachment piece
hytale_set_attachment_piece: group_name="hand_right", is_piece=true

# 4. Add glowing effect
hytale_set_cube_properties: cube_id="rune", shading_mode="fullbright"
```

### Animate Weapon Draw

```
# Start with sheathed weapon visible
hytale_create_visibility_keyframe: bone_name="sword_sheathed", time=0, visible=true
hytale_create_visibility_keyframe: bone_name="sword_drawn", time=0, visible=false

# At draw point, swap
hytale_create_visibility_keyframe: bone_name="sword_sheathed", time=0.3, visible=false
hytale_create_visibility_keyframe: bone_name="sword_drawn", time=0.3, visible=true
```

## Tips

- Always run `hytale_validate_model` before export
- Keep node count under 255
- Use stretch instead of fractional cube sizes
- Set group origins at joint/pivot points
- Use `fullbright` shading for glowing elements
- Mark equipment bones as `is_piece=true` for attachments
- Use visibility keyframes for state changes (weapons, damage)
- Animation runs at 60 FPS (time 1.0 = 60 frames)
