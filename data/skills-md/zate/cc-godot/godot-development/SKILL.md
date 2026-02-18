---
name: godot-development
description: Expert knowledge of Godot Engine game development including scene creation, node management, GDScript programming, and project structure. Use when working with Godot projects, creating or modifying scenes, adding nodes, writing game scripts, or solving Godot-specific problems.
allowed-tools:
  - mcp__godot__*
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

# Godot Development Skill

You are an expert in Godot Engine game development with deep knowledge of:

## Core Concepts

**Scene Tree Architecture**
- Scenes are collections of nodes arranged in a tree hierarchy
- Every scene has a root node
- Nodes inherit from parent nodes and can have multiple children
- Scene instances can be nested and reused
- The scene tree is traversed from root to leaves

**Node Types**

*2D Nodes:*
- Node2D: Base for all 2D nodes, has position, rotation, scale
- Sprite2D: Displays 2D textures
- AnimatedSprite2D: Plays sprite animations
- CollisionShape2D: Defines collision areas (must be child of physics body)
- Area2D: Detects overlapping bodies/areas
- CharacterBody2D: Physics body with built-in movement functions
- RigidBody2D: Physics body affected by forces
- StaticBody2D: Immovable physics body
- TileMap: Grid-based tile system
- Camera2D: 2D camera with follow and zoom
- CanvasLayer: UI layer that stays fixed on screen
- Control: Base for UI elements (Button, Label, Panel, etc.)

*3D Nodes:*
- Node3D: Base for all 3D nodes
- MeshInstance3D: Displays 3D meshes
- Camera3D: 3D camera
- DirectionalLight3D, OmniLight3D, SpotLight3D: Lighting
- CollisionShape3D: 3D collision shapes
- Area3D, CharacterBody3D, RigidBody3D, StaticBody3D: 3D physics bodies

*Common Nodes:*
- Timer: Execute code after a delay
- AudioStreamPlayer: Play sounds
- AnimationPlayer: Control complex animations

## Godot MCP Tools

You have access to specialized Godot MCP tools:

- `mcp__godot__launch_editor`: Open Godot editor for a project
- `mcp__godot__run_project`: Run the game project
- `mcp__godot__get_debug_output`: Get console output and errors
- `mcp__godot__stop_project`: Stop running project
- `mcp__godot__get_godot_version`: Check Godot version
- `mcp__godot__list_projects`: Find Godot projects in a directory
- `mcp__godot__get_project_info`: Get project metadata
- `mcp__godot__create_scene`: Create a new .tscn scene file
- `mcp__godot__add_node`: Add nodes to existing scenes
- `mcp__godot__load_sprite`: Load texture into Sprite2D node
- `mcp__godot__save_scene`: Save scene changes
- `mcp__godot__get_uid`: Get file UID (Godot 4.4+)
- `mcp__godot__update_project_uids`: Update UID references

## Project Structure Best Practices

```
project/
├── project.godot           # Project configuration
├── scenes/                 # All scene files
│   ├── main/              # Main game scenes
│   ├── ui/                # UI scenes
│   ├── characters/        # Character scenes
│   └── levels/            # Level scenes
├── scripts/               # GDScript files
│   ├── autoload/         # Singleton scripts
│   ├── characters/       # Character scripts
│   └── systems/          # Game systems
├── assets/               # Art, audio, etc.
│   ├── sprites/
│   ├── audio/
│   ├── fonts/
│   └── shaders/
└── resources/            # .tres resource files
    ├── materials/
    └── animations/
```

## GDScript Patterns

**Node References:**
```gdscript
# Get child node
@onready var sprite = $Sprite2D
@onready var collision = $CollisionShape2D

# Get node by path
var player = get_node("/root/Main/Player")

# Find node by type
var camera = get_tree().get_first_node_in_group("camera")
```

**Common Lifecycle Methods:**
```gdscript
func _ready():
    # Called when node enters scene tree
    pass

func _process(delta):
    # Called every frame
    pass

func _physics_process(delta):
    # Called every physics frame (fixed timestep)
    pass
```

## Common Tasks

**Creating a Basic 2D Character:**
1. Create scene with CharacterBody2D root
2. Add Sprite2D child for visuals
3. Add CollisionShape2D child for physics
4. Attach script to root node
5. Implement movement in _physics_process

**Setting Up Camera:**
- 2D: Add Camera2D, enable "Current"
- 3D: Add Camera3D, adjust position and rotation
- Use smoothing for better feel

**Input Handling:**
```gdscript
func _input(event):
    if event.is_action_pressed("jump"):
        jump()

func _process(delta):
    var direction = Input.get_axis("left", "right")
```

## When to Use This Skill

Activate when the user:
- Asks about Godot features or capabilities
- Needs help creating or modifying scenes
- Wants to add nodes or configure properties
- Has questions about GDScript
- Needs project structure advice
- Encounters Godot-specific errors
- Asks about best practices for game development in Godot

Use the MCP tools proactively to accomplish tasks rather than just explaining how to do them manually.
