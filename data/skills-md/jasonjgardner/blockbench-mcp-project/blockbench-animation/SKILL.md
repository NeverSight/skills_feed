---
name: blockbench-animation
description: Create and manage animations in Blockbench using MCP tools. Use when animating 3D models, creating keyframes, managing bone rigs, editing animation curves, or working with animation timelines. Covers walk cycles, idle animations, combat animations, and complex multi-bone animations.
---

# Blockbench Animation

Create animations for 3D models using Blockbench MCP tools.

## Available Tools

| Tool | Purpose |
|------|---------|
| `create_animation` | Create animation with keyframes for bones |
| `manage_keyframes` | Create/edit/delete keyframes per bone and channel |
| `animation_graph_editor` | Fine-tune animation curves (smooth, linear, ease) |
| `bone_rigging` | Create/modify bone structure for animation |
| `animation_timeline` | Control playback, time, FPS, loop settings |
| `batch_keyframe_operations` | Batch operations: offset, scale, reverse, mirror |
| `animation_copy_paste` | Copy animation data between bones/animations |

## Quick Start

### Create a Simple Animation

```
1. create_animation: name="walk", animation_length=1.0, loop=true
2. manage_keyframes: bone_name="leg_left", channel="rotation",
   keyframes=[{time: 0, values: [30, 0, 0]}, {time: 0.5, values: [-30, 0, 0]}]
3. animation_timeline: action="play"
```

### Animation Channels

- `position` - [x, y, z] offset
- `rotation` - [x, y, z] degrees
- `scale` - [x, y, z] or uniform number

### Interpolation Types

- `linear` - Constant rate
- `catmullrom` - Smooth spline
- `bezier` - Custom curves
- `step` - Instant change

## Common Workflows

### Walk Cycle (1 second)

```
create_animation: name="walk", animation_length=1.0, loop=true, bones={
  "leg_left": [
    {time: 0, rotation: [30, 0, 0]},
    {time: 0.5, rotation: [-30, 0, 0]},
    {time: 1.0, rotation: [30, 0, 0]}
  ],
  "leg_right": [
    {time: 0, rotation: [-30, 0, 0]},
    {time: 0.5, rotation: [30, 0, 0]},
    {time: 1.0, rotation: [-30, 0, 0]}
  ]
}
```

### Smooth Curves

```
animation_graph_editor: bone_name="arm", channel="rotation", action="smooth"
```

### Copy Animation to Mirrored Bone

```
animation_copy_paste: action="copy", source={bone: "arm_left"}
animation_copy_paste: action="mirror_paste", target={bone: "arm_right", mirror_axis: "x"}
```

### Batch Timing Adjustment

```
batch_keyframe_operations: operation="scale", selection="all",
  parameters={scale_factor: 2.0}  # Double animation duration
```

## Bone Rigging

### Create Bone Structure

```
bone_rigging: action="create", bone_data={name: "spine", origin: [0, 12, 0]}
bone_rigging: action="create", bone_data={name: "head", origin: [0, 24, 0], parent: "spine"}
```

### Set Pivot Point

```
bone_rigging: action="set_pivot", bone_data={name: "arm_left", origin: [4, 22, 0]}
```

## Timeline Control

```
animation_timeline: action="set_fps", fps=60
animation_timeline: action="set_length", length=2.5
animation_timeline: action="loop", loop_mode="loop"  # or "once", "hold"
animation_timeline: action="set_time", time=0.5
animation_timeline: action="play"
```

## Tips

- Use `list_outline` to see available bones before animating
- Set up bone hierarchy first with `bone_rigging` before adding keyframes
- Use `catmullrom` interpolation for organic movement
- Use `step` interpolation for mechanical/robotic movement
- Mirror animations for symmetrical rigs to save time
