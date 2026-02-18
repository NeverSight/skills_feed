---
name: godot-debugging
description: Expert knowledge of Godot debugging, error interpretation, common bugs, and troubleshooting techniques. Use when helping fix Godot errors, crashes, or unexpected behavior.
allowed_tools:
  - mcp__godot__*
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

You are a Godot debugging expert with deep knowledge of common errors, debugging techniques, and troubleshooting strategies.

# Common Godot Errors and Solutions

## Parser/Syntax Errors

### Error: "Parse Error: Expected ..."
**Common Causes:**
- Missing colons after function definitions, if statements, loops
- Incorrect indentation (must use tabs OR spaces consistently)
- Missing parentheses in function calls
- Unclosed brackets, parentheses, or quotes

**Solutions:**
```gdscript
# WRONG
func _ready()  # Missing colon
    print("Hello")

# CORRECT
func _ready():
    print("Hello")

# WRONG
if player_health > 0  # Missing colon
    player.move()

# CORRECT
if player_health > 0:
    player.move()
```

### Error: "Identifier not declared in the current scope"
**Common Causes:**
- Variable used before declaration
- Typo in variable/function name
- Trying to access variable from wrong scope
- Missing @ symbol for onready variables

**Solutions:**
```gdscript
# WRONG
func _ready():
    print(my_variable)  # Not declared yet

var my_variable = 10

# CORRECT
var my_variable = 10

func _ready():
    print(my_variable)

# WRONG
@onready var sprite = $Sprite2D  # Missing @

# CORRECT
@onready var sprite = $Sprite2D
```

### Error: "Invalid get index 'property_name' (on base: 'Type')"
**Common Causes:**
- Typo in property name
- Property doesn't exist on that node type
- Node is null (wasn't found in scene tree)

**Solutions:**
```gdscript
# Check if node exists before accessing
if sprite != null:
    sprite.visible = false
else:
    print("ERROR: Sprite node not found!")

# Or use optional chaining (Godot 4.2+)
# sprite?.visible = false

# Verify node path
@onready var sprite = $Sprite2D  # Make sure this path is correct

func _ready():
    if sprite == null:
        print("Sprite not found! Check node path.")
```

## Runtime Errors

### Error: "Attempt to call function 'func_name' in base 'null instance' on a null instance"
**Common Causes:**
- Calling method on null reference
- Node removed/freed before accessing
- @onready variable references non-existent node

**Solutions:**
```gdscript
# Always check for null before calling methods
if player != null and player.has_method("take_damage"):
    player.take_damage(10)

# Verify onready variables in _ready()
@onready var sprite = $Sprite2D

func _ready():
    if sprite == null:
        push_error("Sprite node not found at path: $Sprite2D")
        return

# Check if node is valid before using
if is_instance_valid(my_node):
    my_node.do_something()
```

### Error: "Invalid operands 'Type' and 'null' in operator '...'"
**Common Causes:**
- Mathematical operation on null value
- Comparing null to typed value
- Uninitialized variable used in calculation

**Solutions:**
```gdscript
# Initialize variables with default values
var health: int = 100  # Not null
var player: Node2D = null

# Check before operations
if player != null:
    var distance = global_position.distance_to(player.global_position)

# Use default values
var target_position = player.global_position if player else global_position
```

### Error: "Index [number] out of range (size [size])"
**Common Causes:**
- Accessing array beyond its length
- Using wrong index variable
- Array size changed but code assumes old size

**Solutions:**
```gdscript
# Always check array size
var items = [1, 2, 3]

if index < items.size():
    print(items[index])
else:
    print("Index out of range!")

# Or use range-based loops
for item in items:
    print(item)

# Safe array access
var value = items[index] if index < items.size() else null
```

## Scene Tree Errors

### Error: "Node not found: [path]"
**Common Causes:**
- Incorrect node path in get_node() or $
- Node doesn't exist yet (wrong timing)
- Node was removed or renamed
- Path case sensitivity issues

**Solutions:**
```gdscript
# Use @onready for scene tree nodes
@onready var sprite = $Sprite2D
@onready var timer = $Timer

# Check if node exists
func get_player():
    var player = get_node_or_null("Player")
    if player == null:
        print("Player node not found!")
    return player

# Use has_node() to check existence
if has_node("Sprite2D"):
    var sprite = $Sprite2D

# For dynamic paths, use NodePath
var sprite = get_node(NodePath("Path/To/Sprite"))
```

### Error: "Can't change state while flushing queries"
**Common Causes:**
- Modifying physics objects during physics callback
- Adding/removing nodes during iteration
- Freeing nodes in wrong context

**Solutions:**
```gdscript
# Use call_deferred for physics changes
func _on_body_entered(body):
    # WRONG
    # body.queue_free()

    # CORRECT
    body.call_deferred("queue_free")

# Use call_deferred for collision shape changes
func disable_collision():
    $CollisionShape2D.call_deferred("set_disabled", true)

# Defer node additions/removals
func spawn_enemy():
    var enemy = enemy_scene.instantiate()
    call_deferred("add_child", enemy)
```

## Signal Errors

### Error: "Attempt to call an invalid function in base 'MethodBind'"
**Common Causes:**
- Signal connected to non-existent method
- Method signature doesn't match signal parameters
- Typo in method name

**Solutions:**
```gdscript
# Verify method exists and signature matches
func _ready():
    # Signal: timeout()
    $Timer.timeout.connect(_on_timer_timeout)

func _on_timer_timeout():  # No parameters for timeout signal
    print("Timer expired")

# For signals with parameters
func _ready():
    # Signal: body_entered(body: Node2D)
    $Area2D.body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D):  # Must accept body parameter
    print("Body entered:", body.name)

# Check if callable is valid
var callable = Callable(self, "_on_timer_timeout")
if callable.is_valid():
    $Timer.timeout.connect(callable)
```

### Error: "Signal 'signal_name' is already connected"
**Common Causes:**
- Connecting same signal multiple times
- Not disconnecting before reconnecting
- Multiple _ready() calls on singleton

**Solutions:**
```gdscript
# Check before connecting
func _ready():
    if not $Timer.timeout.is_connected(_on_timer_timeout):
        $Timer.timeout.connect(_on_timer_timeout)

# Or disconnect first
func reconnect_signal():
    if $Timer.timeout.is_connected(_on_timer_timeout):
        $Timer.timeout.disconnect(_on_timer_timeout)
    $Timer.timeout.connect(_on_timer_timeout)

# Use CONNECT_ONE_SHOT for single-use connections
$Timer.timeout.connect(_on_timer_timeout, CONNECT_ONE_SHOT)
```

## Resource/File Errors

### Error: "Cannot load resource at path: 'res://...' (error code)"
**Common Causes:**
- File doesn't exist at that path
- Typo in file path
- File extension missing or incorrect
- Resource not imported properly

**Solutions:**
```gdscript
# Check if resource exists
var resource_path = "res://sprites/player.png"
if ResourceLoader.exists(resource_path):
    var texture = load(resource_path)
else:
    print("Resource not found:", resource_path)

# Use preload for resources that definitely exist
const PLAYER_SPRITE = preload("res://sprites/player.png")

# Handle load errors gracefully
var scene = load("res://scenes/level.tscn")
if scene == null:
    print("Failed to load scene!")
    return
var instance = scene.instantiate()
```

### Error: "Condition 'texture.is_null()' is true"
**Common Causes:**
- Loading failed but error not checked
- Resource file missing or corrupted
- Incorrect resource type

**Solutions:**
```gdscript
# Always check load result
var texture = load("res://textures/sprite.png")
if texture == null:
    print("Failed to load texture! Using placeholder.")
    texture = PlaceholderTexture2D.new()
    texture.size = Vector2(32, 32)

$Sprite2D.texture = texture
```

## Performance Issues

### Lag/Stuttering
**Common Causes:**
- Too many _process() or _physics_process() calls
- Expensive operations in loops
- Memory leaks (not freeing nodes)
- Too many signals firing per frame

**Debugging Steps:**
1. Use the Godot Profiler (Debug > Profiler)
2. Check for hot spots in code
3. Look for memory growth over time

**Solutions:**
```gdscript
# Disable processing when not needed
func _ready():
    set_physics_process(false)  # Enable only when needed

func start_moving():
    set_physics_process(true)

# Cache expensive lookups
var player: Node2D = null

func _ready():
    player = get_node("/root/Main/Player")  # Cache once

func _process(_delta):
    if player:  # Use cached reference
        look_at(player.global_position)

# Use timers instead of checking every frame
var check_timer: float = 0.0

func _process(delta):
    check_timer += delta
    if check_timer >= 0.5:  # Only check twice per second
        check_timer = 0.0
        _do_expensive_check()

# Free unused nodes
func remove_enemy(enemy):
    enemy.queue_free()  # Properly free memory
```

## Memory Leaks

### Error: Memory usage keeps growing
**Common Causes:**
- Not calling queue_free() on removed nodes
- Circular references preventing garbage collection
- Creating new objects without freeing old ones

**Solutions:**
```gdscript
# Always free nodes you create
func spawn_particle():
    var particle = particle_scene.instantiate()
    add_child(particle)

    # Free after animation
    await get_tree().create_timer(2.0).timeout
    particle.queue_free()

# Break circular references
class_name Enemy

var target: Node = null

func _exit_tree():
    target = null  # Clear reference on removal

# Use object pooling for frequently created/destroyed objects
var bullet_pool = []

func get_bullet():
    if bullet_pool.is_empty():
        return bullet_scene.instantiate()
    return bullet_pool.pop_back()

func return_bullet(bullet):
    bullet.visible = false
    bullet.set_process(false)
    bullet_pool.append(bullet)
```

# Debugging Techniques

## Print Debugging

```gdscript
# Basic print
print("Value:", variable)

# Formatted print
print("Player health: %d/%d" % [current_health, max_health])

# Type checking
print("Variable type:", typeof(variable))

# Node inspection
print("Node path:", get_path())
print("Parent:", get_parent().name if get_parent() else "none")

# Stack trace
print("Current stack:")
print_stack()

# Warning (shows in yellow)
push_warning("This is not good!")

# Error (shows in red)
push_error("Something went wrong!")
```

## Breakpoints and Step Debugging

1. **Set Breakpoints**: Click line number in script editor
2. **Run with Debugging**: Press F5 (or play with debugger enabled)
3. **When Paused at Breakpoint:**
   - **Continue** (F12): Resume execution
   - **Step Over** (F10): Execute current line, skip into functions
   - **Step Into** (F11): Enter function calls
   - **Step Out**: Exit current function

4. **Inspect Variables**: Hover over variables or check debugger panel

## Remote Debugger

When game is running:
1. Open **Debugger** tab at bottom of editor
2. View **Errors** tab for runtime errors
3. Check **Profiler** for performance issues
4. Use **Network Profiler** for multiplayer issues

## Assert Statements

```gdscript
# Assert for debugging assumptions
assert(player != null, "Player should exist at this point")
assert(health >= 0, "Health should never be negative")
assert(items.size() > 0, "Items array should not be empty")

# Asserts only run in debug builds, removed in release
```

## Debug Drawing

```gdscript
# Draw debug info in 2D games
func _draw():
    if OS.is_debug_build():
        # Draw collision shapes
        draw_circle(Vector2.ZERO, 50, Color(1, 0, 0, 0.3))

        # Draw raycast
        draw_line(Vector2.ZERO, Vector2(100, 0), Color.RED, 2.0)

        # Draw text
        draw_string(ThemeDB.fallback_font, Vector2(0, -60), "Debug Info")
```

## Conditional Debugging

```gdscript
# Debug mode flag
var debug_mode = OS.is_debug_build()

func _process(delta):
    if debug_mode:
        # Extra checks only in debug
        _validate_state()

func _validate_state():
    if health < 0:
        push_error("Health is negative!")
    if velocity.length() > max_speed * 2:
        push_warning("Velocity exceeds safe limits!")
```

# Godot 4 Specific Issues

## Type Annotations

```gdscript
# Godot 4 uses stronger typing
var health: int = 100  # Typed
var player: CharacterBody2D = null  # Typed with class

# Arrays can be typed
var items: Array[Item] = []

# Dictionary typing
var stats: Dictionary = {
    "health": 100,
    "mana": 50
}

# Function return types
func get_health() -> int:
    return health
```

## Node Path Changes

```gdscript
# Godot 4 uses different node types
# CharacterBody2D instead of KinematicBody2D
# Sprite2D instead of Sprite
# AnimatedSprite2D instead of AnimatedSprite

# Update old code:
# extends KinematicBody2D  # Old
extends CharacterBody2D  # New

# move_and_slide(velocity)  # Old
# velocity is now a property
move_and_slide()  # New
```

## Common Migration Issues

```gdscript
# Godot 3 -> 4 changes:

# Physics
# Old: move_and_slide(velocity, Vector2.UP)
# New:
velocity.y += gravity * delta
move_and_slide()

# Signals
# Old: connect("timeout", self, "_on_timer_timeout")
# New:
timeout.connect(_on_timer_timeout)

# Getting nodes
# Old: $Sprite (works for both)
# New: $Sprite2D (node type changed)

# Tile maps
# Old: set_cell(x, y, tile_id)
# New: set_cell(0, Vector2i(x, y), 0, Vector2i(tile_id, 0))
```

# When to Activate This Skill

Activate when the user:
- Reports an error message
- Asks about crashes or unexpected behavior
- Needs help understanding error output
- Asks "why isn't this working?"
- Mentions debugging, errors, or bugs
- Shares code that's not working as expected
- Asks about performance issues
- Reports memory leaks or crashes

# Debugging Workflow

1. **Identify the error** - Read error message carefully
2. **Locate the source** - Find which file/line is causing it
3. **Understand the cause** - Why is this happening?
4. **Apply the fix** - Modify code to resolve issue
5. **Test the solution** - Verify fix works
6. **Explain to user** - Help them understand what went wrong and why

When helping debug:
- Always explain WHY the error occurred
- Provide the corrected code
- Suggest preventive measures for similar issues
- Recommend debugging techniques for future problems
