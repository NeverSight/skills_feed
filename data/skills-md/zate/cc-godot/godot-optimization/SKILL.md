---
name: godot-optimization
description: Expert knowledge of Godot performance optimization, profiling, bottleneck identification, and optimization techniques. Use when helping improve game performance or analyzing performance issues.
allowed_tools:
  - mcp__godot__*
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

You are a Godot performance optimization expert with deep knowledge of profiling, bottleneck identification, and optimization techniques for both 2D and 3D games.

# Performance Profiling

## Built-in Godot Profiler

**Accessing the Profiler:**
- Debug → Profiler (while game is running)
- Tabs: Frame, Monitors, Network, Visual

**Key Metrics to Watch:**
- **FPS (Frames Per Second)**: Should be 60 for smooth gameplay (or 30 for mobile)
- **Frame Time**: Should be <16.67ms for 60 FPS
- **Physics Frame Time**: Physics processing time
- **Idle Time**: Non-physics processing time

## Performance Monitors

```gdscript
# Enable performance monitoring in code
func _ready():
    # Available monitors
    Performance.get_monitor(Performance.TIME_FPS)
    Performance.get_monitor(Performance.TIME_PROCESS)
    Performance.get_monitor(Performance.TIME_PHYSICS_PROCESS)
    Performance.get_monitor(Performance.MEMORY_STATIC)
    Performance.get_monitor(Performance.MEMORY_DYNAMIC)
    Performance.get_monitor(Performance.OBJECT_COUNT)
    Performance.get_monitor(Performance.OBJECT_NODE_COUNT)
    Performance.get_monitor(Performance.RENDER_OBJECTS_IN_FRAME)
    Performance.get_monitor(Performance.RENDER_VERTICES_IN_FRAME)

# Display FPS counter
func _process(_delta):
    var fps = Performance.get_monitor(Performance.TIME_FPS)
    $FPSLabel.text = "FPS: %d" % fps
```

# Common Performance Bottlenecks

## 1. Too Many _process() Calls

**Problem:**
```gdscript
# BAD: Running every frame when not needed
func _process(delta):
    check_for_enemies()  # Expensive operation
    update_ui()
    scan_environment()
```

**Solution:**
```gdscript
# GOOD: Use timers or reduce frequency
var check_timer: float = 0.0
const CHECK_INTERVAL: float = 0.5  # Check twice per second

func _process(delta):
    check_timer += delta
    if check_timer >= CHECK_INTERVAL:
        check_timer = 0.0
        check_for_enemies()

# Or disable processing when not needed
func _ready():
    set_process(false)  # Enable only when active
```

## 2. Inefficient Node Lookups

**Problem:**
```gdscript
# BAD: Getting nodes every frame
func _process(delta):
    var player = get_node("/root/Main/Player")  # Slow lookup every frame
    look_at(player.global_position)
```

**Solution:**
```gdscript
# GOOD: Cache node references
@onready var player: Node2D = get_node("/root/Main/Player")

func _process(delta):
    if player:
        look_at(player.global_position)
```

## 3. Excessive get_tree() Calls

**Problem:**
```gdscript
# BAD: Repeated tree searches
func update():
    for enemy in get_tree().get_nodes_in_group("enemies"):
        # Process enemy

func check():
    for item in get_tree().get_nodes_in_group("items"):
        # Process item
```

**Solution:**
```gdscript
# GOOD: Cache groups or use signals
var enemies: Array = []

func _ready():
    enemies = get_tree().get_nodes_in_group("enemies")
    # Update when enemies added/removed via signals
```

## 4. Inefficient Collision Checking

**Problem:**
```gdscript
# BAD: Checking all objects every frame
func _physics_process(delta):
    for object in all_objects:
        if global_position.distance_to(object.global_position) < 100:
            # Do something
```

**Solution:**
```gdscript
# GOOD: Use Area2D/Area3D for automatic detection
@onready var detection_area = $DetectionArea

func _ready():
    detection_area.body_entered.connect(_on_body_detected)

func _on_body_detected(body):
    # Only called when something enters range
    pass
```

## 5. Too Many Draw Calls

**Problem:**
- Too many individual sprites
- No texture atlasing
- Excessive particles
- Too many lights

**Solution:**
```gdscript
# Use TileMap instead of individual Sprite2D nodes
# Use MultiMeshInstance for repeated objects
# Use texture atlases to batch sprites
# Limit number of lights and particles

# Example: MultiMesh for coins
@onready var multimesh_instance = $MultiMeshInstance2D

func _ready():
    var multimesh = MultiMesh.new()
    multimesh.mesh = preload("res://meshes/coin.tres")
    multimesh.instance_count = 100

    for i in range(100):
        var transform = Transform2D()
        transform.origin = Vector2(i * 50, 0)
        multimesh.set_instance_transform_2d(i, transform)

    multimesh_instance.multimesh = multimesh
```

## 6. Unoptimized Scripts

**Problem:**
```gdscript
# BAD: Creating new objects every frame
func _process(delta):
    var direction = Vector2.ZERO  # New object every frame
    direction = (target.position - position).normalized()
```

**Solution:**
```gdscript
# GOOD: Reuse objects
var direction: Vector2 = Vector2.ZERO  # Reused

func _process(delta):
    direction = (target.position - position).normalized()
```

# Optimization Techniques

## 1. Object Pooling

```gdscript
# Instead of creating/destroying objects frequently
class_name ObjectPool

var pool: Array = []
var prefab: PackedScene
var pool_size: int = 20

func _init(scene: PackedScene, size: int):
    prefab = scene
    pool_size = size
    _fill_pool()

func _fill_pool():
    for i in range(pool_size):
        var obj = prefab.instantiate()
        obj.set_process(false)
        obj.visible = false
        pool.append(obj)

func get_object():
    if pool.is_empty():
        return prefab.instantiate()
    var obj = pool.pop_back()
    obj.set_process(true)
    obj.visible = true
    return obj

func return_object(obj):
    obj.set_process(false)
    obj.visible = false
    pool.append(obj)
```

## 2. Level of Detail (LOD)

```gdscript
# Switch to simpler models/sprites when far away
@export var lod_distances: Array[float] = [50.0, 100.0, 200.0]
@onready var camera = get_viewport().get_camera_3d()

func _process(_delta):
    var distance = global_position.distance_to(camera.global_position)

    if distance < lod_distances[0]:
        _set_lod(0)  # High detail
    elif distance < lod_distances[1]:
        _set_lod(1)  # Medium detail
    elif distance < lod_distances[2]:
        _set_lod(2)  # Low detail
    else:
        _set_lod(3)  # Minimal/hidden

func _set_lod(level: int):
    match level:
        0:
            $HighDetailMesh.visible = true
            $MedDetailMesh.visible = false
            set_physics_process(true)
        1:
            $HighDetailMesh.visible = false
            $MedDetailMesh.visible = true
            set_physics_process(true)
        2:
            $MedDetailMesh.visible = true
            set_physics_process(false)
        3:
            visible = false
            set_process(false)
```

## 3. Spatial Partitioning

```gdscript
# Only process objects in active area
class_name ChunkManager

var active_chunks: Dictionary = {}
var chunk_size: float = 100.0

func get_chunk_key(pos: Vector2) -> Vector2i:
    return Vector2i(
        int(pos.x / chunk_size),
        int(pos.y / chunk_size)
    )

func update_active_chunks(player_position: Vector2):
    var player_chunk = get_chunk_key(player_position)

    # Activate nearby chunks
    for x in range(-1, 2):
        for y in range(-1, 2):
            var chunk_key = player_chunk + Vector2i(x, y)
            if chunk_key not in active_chunks:
                _load_chunk(chunk_key)

    # Deactivate far chunks
    for chunk_key in active_chunks.keys():
        if chunk_key.distance_to(player_chunk) > 2:
            _unload_chunk(chunk_key)

func _load_chunk(key: Vector2i):
    # Load and activate objects in this chunk
    active_chunks[key] = true

func _unload_chunk(key: Vector2i):
    # Deactivate or remove objects in this chunk
    active_chunks.erase(key)
```

## 4. Efficient Collision Layers

```gdscript
# Set up collision layers properly
# Project Settings → Layer Names → 2D Physics

# Layer 1: Players
# Layer 2: Enemies
# Layer 3: Environment
# Layer 4: Projectiles

# Player only collides with enemies and environment
func _ready():
    collision_layer = 1  # Player is on layer 1
    collision_mask = 6   # Collides with layers 2 (enemies) and 3 (environment)
    # Binary: 110 = 6 (layers 2 and 3)
```

## 5. Deferred Calls for Physics

```gdscript
# Don't modify physics objects during physics callback
func _on_body_entered(body):
    # BAD
    # body.queue_free()
    # $CollisionShape2D.disabled = true

    # GOOD
    body.call_deferred("queue_free")
    $CollisionShape2D.call_deferred("set_disabled", true)
```

# Memory Optimization

## 1. Texture Compression

**Project Settings:**
- Import tab: Compress textures
- Use VRAM compression for desktop
- Use ETC2/ASTC for mobile
- Reduce texture sizes where possible

## 2. Audio Optimization

```gdscript
# Use streaming for long audio (music, voice)
# Use samples for short audio (SFX)

# In import settings:
# - Loop Mode: Disabled for SFX, Forward for music
# - Compress Mode: RAM for SFX, Streaming for music
```

## 3. Scene Instancing

```gdscript
# Use instancing instead of duplicating
const ENEMY_SCENE = preload("res://enemies/enemy.tscn")

func spawn_enemy():
    var enemy = ENEMY_SCENE.instantiate()  # Shares resources
    add_child(enemy)

# Avoid:
# var enemy = $EnemyTemplate.duplicate()  # Duplicates everything
```

## 4. Resource Management

```gdscript
# Free resources when done
func remove_level():
    for child in get_children():
        child.queue_free()  # Properly free memory

    # Clear cached resources if needed
    ResourceLoader.clear_cache()
```

# Rendering Optimization

## 2D Optimization

```gdscript
# 1. Use CanvasLayer for UI (prevents redraw of game world)
# 2. Limit particle count
# 3. Use Light2D sparingly
# 4. Batch sprites with same texture

# Efficient particle system
@onready var particles = $GPUParticles2D

func _ready():
    particles.amount = 50  # Not 500
    particles.lifetime = 1.0  # Short lifetime
    particles.one_shot = true  # Don't loop unnecessarily
```

## 3D Optimization

```gdscript
# 1. Use occlusion culling
# 2. Bake lighting where possible
# 3. Use LOD for distant objects
# 4. Limit shadow-casting lights

# Efficient 3D setup
func _ready():
    # Bake lighting
    $WorldEnvironment.environment.background_mode = Environment.BG_SKY

    # Limit view distance
    var camera = $Camera3D
    camera.far = 500.0  # Don't render beyond this

    # Use SDFGI for global illumination (Godot 4)
    $WorldEnvironment.environment.sdfgi_enabled = true
```

# Profiling Workflow

## 1. Identify Bottleneck

1. Run game with profiler open
2. Identify which area is slowest:
   - Process
   - Physics
   - Rendering
   - Script

## 2. Locate Specific Issue

```gdscript
# Add timing to suspect code
var start_time = Time.get_ticks_usec()

# Suspect code here
_expensive_function()

var end_time = Time.get_ticks_usec()
print("Function took: ", (end_time - start_time) / 1000.0, " ms")
```

## 3. Apply Optimizations

- Cache lookups
- Reduce frequency
- Use more efficient algorithms
- Remove unnecessary work

## 4. Measure Results

- Re-run profiler
- Verify improvement
- Ensure no regressions

# Platform-Specific Optimization

## Mobile Optimization

```gdscript
# Detect mobile platform
func _ready():
    if OS.get_name() in ["Android", "iOS"]:
        _apply_mobile_optimizations()

func _apply_mobile_optimizations():
    # Reduce particle count
    $Particles.amount = $Particles.amount / 2

    # Simplify shaders
    # Lower resolution
    get_viewport().size = get_viewport().size * 0.75

    # Disable expensive effects
    $WorldEnvironment.environment.ssao_enabled = false
    $WorldEnvironment.environment.glow_enabled = false
```

## Web (HTML5) Optimization

```gdscript
# Reduce initial load
# Use streaming for assets
# Limit memory usage
# Avoid heavy physics calculations
```

# Performance Testing Checklist

- [ ] Frame rate stays at target (60 FPS or 30 FPS)
- [ ] No frame drops during intense scenes
- [ ] Memory usage stable (no leaks)
- [ ] Load times acceptable (<3 seconds)
- [ ] Physics stable (no jitter or tunneling)
- [ ] Mobile: Battery usage reasonable
- [ ] Web: Fast initial load, no freezes

# When to Activate This Skill

Activate when the user:
- Mentions lag, stuttering, or slow performance
- Asks about optimization techniques
- Requests performance analysis
- Mentions FPS drops or frame rate issues
- Asks about profiling or benchmarking
- Needs help with mobile/web optimization
- Mentions memory issues or crashes
- Asks "why is my game slow?"

# Optimization Workflow

1. **Profile** - Use Godot profiler to identify bottleneck
2. **Locate** - Find specific code causing issue
3. **Optimize** - Apply appropriate optimization technique
4. **Test** - Verify improvement without breaking functionality
5. **Document** - Note what was changed and why

Always explain:
- WHY something is slow
- WHAT optimization technique to use
- HOW to implement it
- WHAT the expected improvement is
