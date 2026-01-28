---
name: blockbench-modeling
description: Create and edit 3D models in Blockbench using MCP tools. Use when building geometry with cubes, creating meshes, placing spheres/cylinders, editing vertices, extruding faces, or organizing models with groups. Covers both cube-based Minecraft modeling and freeform mesh editing.
---

# Blockbench Modeling

Build 3D models using cubes and meshes in Blockbench.

## Available Tools

### Cube Tools
| Tool | Purpose |
|------|---------|
| `place_cube` | Create cubes with position, size, texture |
| `modify_cube` | Edit cube properties (position, rotation, UV, etc.) |

### Mesh Tools
| Tool | Purpose |
|------|---------|
| `place_mesh` | Create mesh with vertices |
| `create_sphere` | Create sphere mesh |
| `create_cylinder` | Create cylinder mesh |
| `extrude_mesh` | Extrude faces/edges/vertices |
| `subdivide_mesh` | Add geometry detail |
| `select_mesh_elements` | Select vertices/edges/faces |
| `move_mesh_vertices` | Move selected vertices |
| `delete_mesh_elements` | Remove geometry |
| `merge_mesh_vertices` | Weld nearby vertices |
| `create_mesh_face` | Create face from vertices |
| `knife_tool` | Cut edges into faces |

### Element Tools
| Tool | Purpose |
|------|---------|
| `add_group` | Create bone/group |
| `list_outline` | View model hierarchy |
| `duplicate_element` | Copy elements |
| `rename_element` | Rename elements |
| `remove_element` | Delete elements |

## Cube Modeling

### Place a Cube

```
place_cube: elements=[{
  name: "body",
  from: [-4, 0, -2],
  to: [4, 12, 2]
}], faces=true  # Auto UV
```

### Place Multiple Cubes

```
place_cube: elements=[
  {name: "head", from: [-4, 12, -4], to: [4, 20, 4]},
  {name: "arm_left", from: [4, 4, -1], to: [6, 12, 1]},
  {name: "arm_right", from: [-6, 4, -1], to: [-4, 12, 1]}
], group="body"
```

### Modify Cube

```
modify_cube: id="body", rotation=[0, 45, 0], origin=[0, 6, 0]
```

### Cube with Texture

```
place_cube: elements=[{name: "block", from: [0,0,0], to: [16,16,16]}],
  texture="stone", faces=true
```

## Mesh Modeling

### Create Sphere

```
create_sphere: elements=[{
  name: "ball",
  position: [0, 8, 0],
  diameter: 16,
  sides: 12
}]
```

### Create Cylinder

```
create_cylinder: elements=[{
  name: "pillar",
  position: [0, 0, 0],
  diameter: 8,
  height: 24,
  sides: 12,
  capped: true
}]
```

### Extrude Face

```
select_mesh_elements: mesh_id="pillar", mode="face", elements=["top_face"]
extrude_mesh: mesh_id="pillar", mode="faces", distance=4
```

### Subdivide for Detail

```
subdivide_mesh: mesh_id="sphere", cuts=2
```

### Move Vertices

```
select_mesh_elements: mesh_id="mesh1", mode="vertex", elements=["v1", "v2"]
move_mesh_vertices: offset=[0, 2, 0]
```

### Merge Close Vertices

```
merge_mesh_vertices: mesh_id="mesh1", threshold=0.1
```

### Knife Cut

```
knife_tool: mesh_id="cube_mesh", points=[
  {position: [0, 8, -4]},
  {position: [0, 8, 4]}
]
```

## Organization

### Create Group Hierarchy

```
add_group: name="root", origin=[0, 0, 0], rotation=[0, 0, 0]
add_group: name="body", parent="root", origin=[0, 12, 0]
add_group: name="head", parent="body", origin=[0, 24, 0]
```

### Add Cubes to Groups

```
place_cube: elements=[{name: "torso", from: [-4, 12, -2], to: [4, 24, 2]}],
  group="body"
```

### Duplicate Element

```
duplicate_element: id="arm_left", newName="arm_right", offset=[-8, 0, 0]
```

### View Hierarchy

```
list_outline  # Returns all groups and elements
```

## Common Patterns

### Minecraft Character

```
# Create hierarchy
add_group: name="root", origin=[0, 0, 0]
add_group: name="body", parent="root", origin=[0, 24, 0]
add_group: name="head", parent="body", origin=[0, 24, 0]
add_group: name="arm_left", parent="body", origin=[5, 22, 0]
add_group: name="arm_right", parent="body", origin=[-5, 22, 0]
add_group: name="leg_left", parent="root", origin=[2, 12, 0]
add_group: name="leg_right", parent="root", origin=[-2, 12, 0]

# Add geometry
place_cube: elements=[{name: "head", from: [-4, 24, -4], to: [4, 32, 4]}], group="head"
place_cube: elements=[{name: "body", from: [-4, 12, -2], to: [4, 24, 2]}], group="body"
place_cube: elements=[{name: "arm", from: [-1, 0, -1], to: [1, 10, 1]}], group="arm_left"
place_cube: elements=[{name: "arm", from: [-1, 0, -1], to: [1, 10, 1]}], group="arm_right"
place_cube: elements=[{name: "leg", from: [-2, 0, -2], to: [2, 12, 2]}], group="leg_left"
place_cube: elements=[{name: "leg", from: [-2, 0, -2], to: [2, 12, 2]}], group="leg_right"
```

### Smooth Organic Shape

```
create_sphere: elements=[{name: "base", position: [0, 8, 0], diameter: 16, sides: 16}]
subdivide_mesh: mesh_id="base", cuts=1
# Select and move vertices to shape
select_mesh_elements: mesh_id="base", mode="vertex"
move_mesh_vertices: offset=[0, 4, 0], vertices=["top_verts"]
```

## Tips

- Use `list_outline` to see current model structure
- Set group origins at joint/pivot points for animation
- Use `faces=true` for auto UV mapping on cubes
- Create bone hierarchy before adding geometry
- Use `duplicate_element` with offset for symmetrical parts
- Mesh editing is more flexible but cubes are simpler for Minecraft-style models
