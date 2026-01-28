---
name: godot
description: This skill should be used when working on Godot Engine projects. It provides specialized knowledge of Godot's file formats (.gd, .tscn, .tres), architecture patterns (component-based, signal-driven, resource-based), common pitfalls, validation tools, code templates, and CLI workflows. The `godot` command is available for running the game, validating scripts, importing resources, and exporting builds. Use this skill for tasks involving Godot game development, debugging scene/resource files, implementing game systems, or creating new Godot components.
---

# Godot Engine Development Skill

Specialized guidance for developing games and applications with Godot Engine, with emphasis on effective collaboration between LLM coding assistants and Godot's unique file structure.

## Overview

Godot projects use a mix of GDScript code files (.gd) and text-based resource files (.tscn for scenes, .tres for resources). While GDScript is straightforward, the resource files have strict formatting requirements that differ significantly from GDScript syntax. This skill provides file format expertise, proven architecture patterns, validation tools, code templates, and debugging workflows to enable effective development of Godot projects.

## When to Use This Skill

Invoke this skill when:

- Working on any Godot Engine project
- Creating or modifying .tscn (scene) or .tres (resource) files
- Implementing game systems (interactions, attributes, spells, inventory, etc.)
- Debugging "file failed to load" or similar resource errors
- Setting up component-based architectures
- Creating signal-driven systems
- Implementing resource-based data (items, spells, abilities)

## Key Principles

### 1. Understand File Format Differences

**GDScript (.gd) - Full Programming Language:**
```gdscript
extends Node
class_name MyClass

var speed: float = 5.0
const MAX_HEALTH = 100

func _ready():
    print("Ready")
```

**Scene Files (.tscn) - Strict Serialization Format:**
```
[ext_resource type="Script" path="res://script.gd" id="1"]

[node name="Player" type="CharacterBody3D"]
script = ExtResource("1")  # NOT preload()!
```

**Resource Files (.tres) - NO GDScript Syntax:**
```
[ext_resource type="Script" path="res://item.gd" id="1"]

[resource]
script = ExtResource("1")  # NOT preload()!
item_name = "Sword"        # NOT var item_name = "Sword"!
```

### 2. Critical Rules for .tres and .tscn Files

**NEVER use in .tres/.tscn files:**
- `preload()` - Use `ExtResource("id")` instead
- `var`, `const`, `func` - These are GDScript keywords
- Untyped arrays - Use `Array[Type]([...])` syntax

**ALWAYS use in .tres/.tscn files:**
- `ExtResource("id")` for external resources
- `SubResource("id")` for inline resources
- Typed arrays: `Array[Resource]([...])`
- Proper ExtResource declarations before use

### 3. Separation of Concerns

**Keep logic in .gd files, data in .tres files:**
```
src/
  spells/
    spell_resource.gd      # Class definition + logic
    spell_effect.gd        # Effect logic
resources/
  spells/
    fireball.tres          # Data only, references scripts
    ice_spike.tres         # Data only
```

This makes LLM editing much safer and clearer.

### 4. Component-Based Architecture

Break functionality into small, focused components:
```
Player (CharacterBody3D)
├─ HealthAttribute (Node)     # Component
├─ ManaAttribute (Node)        # Component
├─ Inventory (Node)            # Component
└─ StateMachine (Node)         # Component
    ├─ IdleState (Node)
    ├─ MoveState (Node)
    └─ AttackState (Node)
```

**Benefits:**
- Each component is a small, focused file
- Easy to understand and modify
- Clear responsibilities
- Reusable across different entities

### 5. Signal-Driven Communication

Use signals for loose coupling:
```gdscript
# Component emits signals
signal health_changed(current, max)
signal death()

# Parent connects to signals
func _ready():
    $HealthAttribute.health_changed.connect(_on_health_changed)
    $HealthAttribute.death.connect(_on_death)
```

**Benefits:**
- No tight coupling between systems
- Easy to add new listeners
- Self-documenting (signals show available events)
- UI can connect without modifying game logic

## Using Bundled Resources

### Validation Scripts

Validate .tres and .tscn files before testing in Godot to catch syntax errors early.

**Validate .tres file:**
```bash
python3 scripts/validate_tres.py resources/spells/fireball.tres
```

**Validate .tscn file:**
```bash
python3 scripts/validate_tscn.py scenes/player/player.tscn
```

Use these scripts when:
- After creating or editing .tres/.tscn files programmatically
- When debugging "failed to load" errors
- Before committing scene/resource changes
- When user reports issues with custom resources

### Reference Documentation

Load reference files when needed for detailed information:

**`references/file-formats.md`** - Deep dive into .gd, .tscn, .tres syntax:
- Complete syntax rules for each file type
- Common mistakes with examples
- Safe vs risky editing patterns
- ExtResource and SubResource usage

**`references/architecture-patterns.md`** - Proven architectural patterns:
- Component-based interaction system
- Attribute system (health, mana, etc.)
- Resource-based effect system (spells, items)
- Inventory system
- State machine pattern
- Examples of combining patterns

Read these references when:
- Implementing new game systems
- Unsure about .tres/.tscn syntax
- Debugging file format errors
- Planning architecture for new features

### Code Templates

Use templates as starting points for common patterns. Templates are in `assets/templates/`:

**`component_template.gd`** - Base component with signals, exports, activation:
```gdscript
# Copy and customize for new components
cp assets/templates/component_template.gd src/components/my_component.gd
```

**`attribute_template.gd`** - Numeric attribute (health, mana, stamina):
```gdscript
# Use for any numeric attribute with min/max
cp assets/templates/attribute_template.gd src/attributes/stamina_attribute.gd
```

**`interaction_template.gd`** - Interaction component base class:
```gdscript
# Extend for custom interactions (pickup, door, switch, etc.)
cp assets/templates/interaction_template.gd src/interactions/lever_interaction.gd
```

**`spell_resource.tres`** - Example spell with effects:
```bash
# Use as reference for creating new spell data
cat assets/templates/spell_resource.tres
```

**`item_resource.tres`** - Example item resource:
```bash
# Use as reference for creating new item data
cat assets/templates/item_resource.tres
```

## Workflows

### Workflow 1: Creating a New Component System

Example: Adding a health system to enemies.

**Steps:**

1. **Read architecture patterns reference:**
   ```bash
   # Check for similar patterns
   Read references/architecture-patterns.md
   # Look for "Attribute System" section
   ```

2. **Create base class using template:**
   ```bash
   cp assets/templates/attribute_template.gd src/attributes/attribute.gd
   # Customize the base class
   ```

3. **Create specialized subclass:**
   ```bash
   # Create health_attribute.gd extending attribute.gd
   # Add health-specific signals (damage_taken, death)
   ```

4. **Add to scene via .tscn edit:**
   ```
   [ext_resource type="Script" path="res://src/attributes/health_attribute.gd" id="4_health"]

   [node name="HealthAttribute" type="Node" parent="Enemy"]
   script = ExtResource("4_health")
   value_max = 50.0
   value_start = 50.0
   ```

5. **Test immediately in Godot editor**

6. **If issues, validate the scene file:**
   ```bash
   python3 scripts/validate_tscn.py scenes/enemies/base_enemy.tscn
   ```

### Workflow 2: Creating Resource Data Files (.tres)

Example: Creating a new spell.

**Steps:**

1. **Reference the template:**
   ```bash
   cat assets/templates/spell_resource.tres
   ```

2. **Create new .tres file with proper structure:**
   ```tres
   [gd_resource type="Resource" script_class="SpellResource" load_steps=3 format=3]

   [ext_resource type="Script" path="res://src/spells/spell_resource.gd" id="1"]
   [ext_resource type="Script" path="res://src/spells/spell_effect.gd" id="2"]

   [sub_resource type="Resource" id="Effect_1"]
   script = ExtResource("2")
   effect_type = 0
   magnitude_min = 15.0
   magnitude_max = 25.0

   [resource]
   script = ExtResource("1")
   spell_name = "Fireball"
   spell_id = "fireball"
   mana_cost = 25.0
   effects = Array[ExtResource("2")]([SubResource("Effect_1")])
   ```

3. **Validate before testing:**
   ```bash
   python3 scripts/validate_tres.py resources/spells/fireball.tres
   ```

4. **Fix any errors reported by validator**

5. **Test in Godot editor**

### Workflow 3: Debugging Resource Loading Issues

When user reports "resource failed to load" or similar errors.

**Steps:**

1. **Read the file reported in error:**
   ```bash
   # Check file syntax
   Read resources/spells/problem_spell.tres
   ```

2. **Run validation script:**
   ```bash
   python3 scripts/validate_tres.py resources/spells/problem_spell.tres
   ```

3. **Check for common mistakes:**
   - Using `preload()` instead of `ExtResource()`
   - Using `var`, `const`, `func` keywords
   - Missing ExtResource declarations
   - Incorrect array syntax (not typed)

4. **Read file format reference if needed:**
   ```bash
   Read references/file-formats.md
   # Focus on "Resource Files (.tres)" section
   # Check "Common Mistakes Reference"
   ```

5. **Fix errors and re-validate**

### Workflow 4: Implementing from Architecture Patterns

When implementing a known pattern (interaction system, state machine, etc.).

**Steps:**

1. **Read the relevant pattern:**
   ```bash
   Read references/architecture-patterns.md
   # Find the specific pattern (e.g., "Component-Based Interaction System")
   ```

2. **Copy relevant template:**
   ```bash
   cp assets/templates/interaction_template.gd src/interactions/door_interaction.gd
   ```

3. **Customize the template:**
   - Override `_perform_interaction()`
   - Add custom exports for configuration
   - Add custom signals if needed

4. **Create scene structure following pattern:**
   ```
   [node name="Door" type="StaticBody3D"]
   script = ExtResource("base_interactable.gd")

   [node name="DoorInteraction" type="Node" parent="."]
   script = ExtResource("door_interaction.gd")
   interaction_text = "Open Door"
   ```

5. **Test incrementally**

## Common Pitfalls and Solutions

### Pitfall 1: Using GDScript Syntax in .tres Files

**Problem:**
```tres
# ❌ WRONG
script = preload("res://script.gd")
var items = [1, 2, 3]
```

**Solution:**
```tres
# ✅ CORRECT
[ext_resource type="Script" path="res://script.gd" id="1"]
script = ExtResource("1")
items = Array[int]([1, 2, 3])
```

**Prevention:** Run validation script before testing.

### Pitfall 2: Missing ExtResource Declarations

**Problem:**
```tres
[resource]
script = ExtResource("1_script")  # Not declared!
```

**Solution:**
```tres
[ext_resource type="Script" path="res://script.gd" id="1_script"]

[resource]
script = ExtResource("1_script")
```

**Detection:** Validation script will catch this.

### Pitfall 3: Editing Complex .tscn Hierarchies

**Problem:** Modifying instanced scene children can break when editor re-saves.

**Solution:**
- Make only simple property edits in .tscn files
- For complex changes, use Godot editor
- Test immediately after text edits
- Use git to track changes and revert if needed

### Pitfall 4: Untyped Arrays in .tres Files

**Problem:**
```tres
effects = [SubResource("Effect_1")]  # Missing type
```

**Solution:**
```tres
effects = Array[Resource]([SubResource("Effect_1")])
```

**Prevention:** Validation script warns about this.

### Pitfall 5: Forgetting Instance Property Overrides

**Problem:** When instancing a scene, forgetting to override child node properties. The instance uses default values (often `null`), causing silent bugs.

```
# level.tscn
[node name="KeyPickup" parent="." instance=ExtResource("6_pickup")]
# Oops! PickupInteraction.item_resource is null - pickup won't work!
```

**Solution:** Always configure instanced scene properties using the `index` syntax:

```
[node name="KeyPickup" parent="." instance=ExtResource("6_pickup")]

[node name="PickupInteraction" parent="KeyPickup" index="0"]
item_resource = ExtResource("7_key")
```

**Detection:**
- Test the instance in-game immediately
- Read `references/file-formats.md` "Instance Property Overrides" section for details
- When creating scene instances, ask: "Does this scene have configurable components that need properties set?"

**Prevention:** After instancing any scene with configurable children (PickupInteraction, DoorInteraction, etc.), always verify critical properties are overridden.

### Pitfall 6: CPUParticles3D color_ramp Not Displaying Colors

**Problem:** Setting `color_ramp` on CPUParticles3D, but particles still appear white or don't show the gradient colors.

```tres
[node name="CPUParticles3D" type="CPUParticles3D" parent="."]
mesh = SubResource("SphereMesh_1")
color_ramp = SubResource("Gradient_1")  # Gradient is set but doesn't work!
```

**Root Cause:** The mesh needs a material with `vertex_color_use_as_albedo = true` to apply particle colors to the mesh surface.

**Solution:** Add a StandardMaterial3D to the mesh with vertex color enabled:

```tres
[sub_resource type="StandardMaterial3D" id="StandardMaterial3D_1"]
vertex_color_use_as_albedo = true

[sub_resource type="SphereMesh" id="SphereMesh_1"]
material = SubResource("StandardMaterial3D_1")
radius = 0.12
height = 0.24

[node name="CPUParticles3D" type="CPUParticles3D" parent="."]
mesh = SubResource("SphereMesh_1")
color_ramp = SubResource("Gradient_1")  # Now works!
```

**Prevention:** When creating CPUParticles3D with `color` or `color_ramp`, always add a material with `vertex_color_use_as_albedo = true` to the mesh.

## Best Practices

### 1. Consult References for Common Issues

When encountering issues, consult the reference documentation:

**`references/common-pitfalls.md`** - Common Godot gotchas and solutions:
- Initialization and @onready timing issues
- Node reference and get_node() problems
- Signal connection issues
- Resource loading and modification
- CharacterBody3D movement
- Transform and basis confusion
- Input handling
- Type safety issues
- Scene instancing pitfalls
- Tween issues

**`references/godot4-physics-api.md`** - Physics API quick reference:
- Correct raycast API (`PhysicsRayQueryParameters3D`)
- Shape queries and collision detection
- Collision layers and masks
- Area3D vs RigidBody3D vs CharacterBody3D
- Common physics patterns
- Performance tips

Load these when:
- Getting null reference errors
- Implementing physics/collision systems
- Debugging timing issues with @onready
- Working with CharacterBody3D movement
- Setting up raycasts or shape queries

### 2. Always Validate After Editing .tres/.tscn

```bash
python3 scripts/validate_tres.py path/to/file.tres
python3 scripts/validate_tscn.py path/to/file.tscn
```

### 2. Use Templates as Starting Points

Don't write components from scratch - adapt templates:
```bash
cp assets/templates/component_template.gd src/my_component.gd
```

### 3. Read References for Detailed Syntax

When unsure about syntax, load the reference:
```bash
Read references/file-formats.md
```

### 4. Follow Separation of Concerns

- Logic → .gd files
- Data → .tres files
- Scene structure → .tscn files (prefer editor for complex changes)

### 5. Use Signals for Communication

Prefer signals over direct method calls:
```gdscript
# ✅ Good - Loose coupling
signal item_picked_up(item)
item_picked_up.emit(item)

# ❌ Avoid - Tight coupling
get_parent().get_parent().add_to_inventory(item)
```

### 6. Test Incrementally

After each change:
1. Validate with scripts
2. Test in Godot editor
3. Verify functionality
4. Commit to git

### 7. Use Export Variables Liberally

Make configuration visible and editable:
```gdscript
@export_group("Movement")
@export var speed: float = 5.0
@export var jump_force: float = 10.0

@export_group("Combat")
@export var damage: int = 10
```

## Using the Godot CLI

The `godot` command-line tool is available for running the game and performing various operations without opening the editor.

### Running the Game

**Run the current project:**
```bash
godot --path . --headless
```

**Run a specific scene:**
```bash
godot --path . --scene scenes/main_menu.tscn
```

**Run with debug flags:**
```bash
# Show collision shapes
godot --path . --debug-collisions

# Show navigation debug visuals
godot --path . --debug-navigation

# Show path lines
godot --path . --debug-paths
```

### Checking/Validating Code

**Check GDScript syntax without running:**
```bash
godot --path . --check-only --script path/to/script.gd
```

**Run headless tests (for automated testing):**
```bash
godot --path . --headless --quit --script path/to/test_script.gd
```

### Editor Operations from CLI

**Import resources without opening editor:**
```bash
godot --path . --import --headless --quit
```

**Export project:**
```bash
# Export release build
godot --path . --export-release "Preset Name" builds/game.exe

# Export debug build
godot --path . --export-debug "Preset Name" builds/game_debug.exe
```

### Common CLI Workflows

**Workflow: Quick Test Run**
```bash
# Run the project and quit after testing
godot --path . --quit-after 300  # Runs for 300 frames then quits
```

**Workflow: Automated Resource Import**
```bash
# Import all resources and exit (useful in CI/CD)
godot --path . --import --headless --quit
```

**Workflow: Script Validation**
```bash
# Validate a GDScript file before committing
godot --path . --check-only --script src/player/player.gd
```

**Workflow: Headless Server**
```bash
# Run as dedicated server (no rendering)
godot --path . --headless --scene scenes/multiplayer_server.tscn
```

### CLI Usage Tips

1. **Always specify `--path .`** when running from project directory to ensure Godot finds `project.godot`
2. **Use `--headless`** for CI/CD and automated testing (no window, no rendering)
3. **Use `--quit` or `--quit-after N`** to exit automatically after task completion
4. **Combine `--check-only` with `--script`** to validate GDScript syntax quickly
5. **Use debug flags** (`--debug-collisions`, `--debug-navigation`) to visualize systems during development
6. **Check exit codes** - Non-zero indicates errors (useful for CI/CD scripts)

### Example: Pre-commit Hook for GDScript Validation

```bash
#!/bin/bash
# Validate all changed .gd files before committing

for file in $(git diff --cached --name-only --diff-filter=ACM | grep '\.gd$'); do
    if ! godot --path . --check-only --script "$file" --headless --quit; then
        echo "GDScript validation failed for $file"
        exit 1
    fi
done
```

## Quick Reference

### File Type Decision Tree

**Writing game logic?** → Use .gd file

**Storing data (item stats, spell configs)?** → Use .tres file

**Creating scene structure?** → Use .tscn file (prefer Godot editor for complex structures)

### Syntax Quick Check

**In .gd files:** Full GDScript - `var`, `func`, `preload()`, etc. ✅

**In .tres/.tscn files:**
- `preload()` ❌ → Use `ExtResource("id")` ✅
- `var`, `const`, `func` ❌ → Just property values ✅
- `[1, 2, 3]` ❌ → `Array[int]([1, 2, 3])` ✅

### When to Use Each Validation Script

**`validate_tres.py`** - For resource files:
- Items, spells, abilities
- Custom resource data
- After creating .tres files

**`validate_tscn.py`** - For scene files:
- Player, enemies, levels
- UI scenes
- After editing .tscn files

### When to Read Each Reference

**`file-formats.md`** - When:
- Creating/editing .tres/.tscn files
- Getting "failed to load" errors
- Unsure about syntax rules

**`architecture-patterns.md`** - When:
- Implementing new game systems
- Planning component structure
- Looking for proven patterns

## Summary

Work with Godot projects effectively by:

1. **Understanding file formats** - .gd is code, .tres/.tscn are data with strict syntax
2. **Using validation tools** - Catch errors before testing
3. **Following patterns** - Use proven architectures from references
4. **Starting from templates** - Adapt rather than create from scratch
5. **Testing incrementally** - Validate, test, commit frequently

The key insight: Godot's text-based files are LLM-friendly when you respect the syntax differences between GDScript and resource serialization formats.
