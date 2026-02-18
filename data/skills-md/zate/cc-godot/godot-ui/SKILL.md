---
name: godot-ui
description: Expert knowledge of Godot's UI system including Control nodes, themes, styling, responsive layouts, and common UI patterns for menus, HUDs, inventories, and dialogue systems. Use when working with Godot UI/menu creation or styling.
allowed_tools:
  - mcp__godot__*
  - Read
  - Write
  - Edit
  - Glob
  - Grep
---

You are a Godot UI/UX expert with deep knowledge of Godot's Control node system, theme customization, responsive design, and common game UI patterns.

# Core UI Knowledge

## Control Node Hierarchy

**Base Control Node Properties:**
- `anchor_*`: Positioning relative to parent edges (0.0 to 1.0)
- `offset_*`: Pixel offset from anchor points
- `size_flags_*`: How the node should grow/shrink
- `custom_minimum_size`: Minimum size constraints
- `mouse_filter`: Control mouse input handling (STOP, PASS, IGNORE)
- `focus_mode`: Keyboard/gamepad focus behavior

**Common Control Nodes:**

### Container Nodes (Layout Management)
- **VBoxContainer**: Vertical stacking with automatic spacing
- **HBoxContainer**: Horizontal arrangement with automatic spacing
- **GridContainer**: Grid layout with columns
- **MarginContainer**: Adds margins around children
- **CenterContainer**: Centers a single child
- **PanelContainer**: Container with panel background
- **ScrollContainer**: Scrollable area for overflow content
- **TabContainer**: Tabbed interface with multiple pages
- **SplitContainer**: Resizable split between two children

### Interactive Controls
- **Button**: Standard clickable button
- **TextureButton**: Button with custom textures for states
- **CheckBox**: Toggle checkbox
- **CheckButton**: Toggle switch style
- **OptionButton**: Dropdown selection menu
- **LineEdit**: Single-line text input
- **TextEdit**: Multi-line text editor
- **Slider/HSlider/VSlider**: Value adjustment sliders
- **SpinBox**: Numeric input with increment buttons
- **ProgressBar**: Visual progress indicator
- **ItemList**: Scrollable list of items
- **Tree**: Hierarchical tree view

### Display Nodes
- **Label**: Text display
- **RichTextLabel**: Text with BBCode formatting, images, effects
- **TextureRect**: Image display with scaling options
- **NinePatchRect**: Scalable image using 9-slice method
- **ColorRect**: Solid color rectangle
- **VideoStreamPlayer**: Video playback in UI
- **GraphEdit/GraphNode**: Node-graph interface

### Advanced Controls
- **Popup**: Modal/modeless popup window
- **PopupMenu**: Context menu
- **MenuBar**: Top menu bar
- **FileDialog**: File picker
- **ColorPicker**: Color selection
- **SubViewport**: Embedded viewport for 3D-in-2D UI

## Anchor & Container System

**Anchor Presets:**
```gdscript
# Common anchor configurations
# Top-left (default): anchor_left=0, anchor_top=0, anchor_right=0, anchor_bottom=0
# Full rect: anchor_left=0, anchor_top=0, anchor_right=1, anchor_bottom=1
# Top wide: anchor_left=0, anchor_top=0, anchor_right=1, anchor_bottom=0
# Center: anchor_left=0.5, anchor_top=0.5, anchor_right=0.5, anchor_bottom=0.5
```

**Responsive Design Pattern:**
```gdscript
# In _ready() for responsive UI
func _ready():
    # Connect to viewport size changes
    get_viewport().size_changed.connect(_on_viewport_size_changed)
    _on_viewport_size_changed()

func _on_viewport_size_changed():
    var viewport_size = get_viewport_rect().size
    # Adjust UI based on aspect ratio or screen size
    if viewport_size.x / viewport_size.y < 1.5:  # Portrait or square
        # Switch to mobile layout
        pass
    else:  # Landscape
        # Use desktop layout
        pass
```

## Theme System

**Theme Structure:**
- **StyleBoxes**: Background styles for controls (StyleBoxFlat, StyleBoxTexture)
- **Fonts**: Font resources with size and variants
- **Colors**: Named color values
- **Icons**: Texture2D for icons and graphics
- **Constants**: Numeric values (spacing, margins)

**Creating Themes in Code:**
```gdscript
# Create a theme
var theme = Theme.new()

# StyleBox for buttons
var style_normal = StyleBoxFlat.new()
style_normal.bg_color = Color(0.2, 0.2, 0.2)
style_normal.corner_radius_top_left = 5
style_normal.corner_radius_top_right = 5
style_normal.corner_radius_bottom_left = 5
style_normal.corner_radius_bottom_right = 5
style_normal.content_margin_left = 10
style_normal.content_margin_right = 10
style_normal.content_margin_top = 5
style_normal.content_margin_bottom = 5

var style_hover = StyleBoxFlat.new()
style_hover.bg_color = Color(0.3, 0.3, 0.3)
# ... same corner radius and margins

var style_pressed = StyleBoxFlat.new()
style_pressed.bg_color = Color(0.15, 0.15, 0.15)
# ... same corner radius and margins

theme.set_stylebox("normal", "Button", style_normal)
theme.set_stylebox("hover", "Button", style_hover)
theme.set_stylebox("pressed", "Button", style_pressed)

# Apply to Control node
$MyControl.theme = theme
```

**Theme Resources:**
Best practice: Create .tres theme files and save them in `resources/themes/`
- Allows visual editing in Inspector
- Can be shared across multiple scenes
- Supports inheritance (base theme + overrides)

## Common UI Patterns

### Main Menu
```
CanvasLayer
├── MarginContainer (margins for screen edges)
│   └── VBoxContainer (vertical menu layout)
│       ├── TextureRect (logo)
│       ├── VBoxContainer (button container)
│       │   ├── Button (New Game)
│       │   ├── Button (Continue)
│       │   ├── Button (Settings)
│       │   └── Button (Quit)
│       └── Label (version info)
```

### Settings Menu
```
CanvasLayer
├── ColorRect (semi-transparent overlay)
└── PanelContainer (settings panel)
    └── MarginContainer
        └── VBoxContainer
            ├── Label (Settings Header)
            ├── TabContainer
            │   ├── VBoxContainer (Graphics Tab)
            │   │   ├── HBoxContainer
            │   │   │   ├── Label (Resolution:)
            │   │   │   └── OptionButton
            │   │   └── HBoxContainer
            │   │       ├── Label (Fullscreen:)
            │   │       └── CheckBox
            │   └── VBoxContainer (Audio Tab)
            │       ├── HBoxContainer
            │       │   ├── Label (Master Volume:)
            │       │   └── HSlider
            │       └── HBoxContainer
            │           ├── Label (Music Volume:)
            │           └── HSlider
            └── HBoxContainer (button row)
                ├── Button (Apply)
                └── Button (Back)
```

### HUD (Heads-Up Display)
```
CanvasLayer (layer = 10 for top rendering)
├── MarginContainer (screen margins)
│   └── VBoxContainer
│       ├── HBoxContainer (top bar)
│       │   ├── TextureRect (health icon)
│       │   ├── ProgressBar (health)
│       │   ├── Control (spacer)
│       │   ├── Label (score)
│       │   └── TextureRect (coin icon)
│       ├── Control (spacer - expands)
│       └── HBoxContainer (bottom bar)
│           ├── TextureButton (inventory)
│           ├── TextureButton (map)
│           └── TextureButton (pause)
```

### Inventory System
```
CanvasLayer
├── ColorRect (overlay background)
└── PanelContainer (inventory panel)
    └── MarginContainer
        └── VBoxContainer
            ├── Label (Inventory Header)
            ├── HBoxContainer (main area)
            │   ├── GridContainer (item grid - columns=5)
            │   │   ├── TextureButton (item slot)
            │   │   ├── TextureButton (item slot)
            │   │   └── ... (more slots)
            │   └── PanelContainer (item details)
            │       └── VBoxContainer
            │           ├── TextureRect (item image)
            │           ├── Label (item name)
            │           ├── RichTextLabel (description)
            │           └── Button (Use/Equip)
            └── Button (Close)
```

### Dialogue System
```
CanvasLayer (layer = 5)
├── Control (spacer)
└── PanelContainer (dialogue box - anchored to bottom)
    └── MarginContainer
        └── VBoxContainer
            ├── HBoxContainer (character info)
            │   ├── TextureRect (character portrait)
            │   └── Label (character name)
            ├── RichTextLabel (dialogue text with BBCode)
            └── VBoxContainer (choice container)
                ├── Button (choice 1)
                ├── Button (choice 2)
                └── Button (choice 3)
```

### Pause Menu
```
CanvasLayer (layer = 100)
├── ColorRect (semi-transparent overlay - modulate alpha)
└── CenterContainer (full rect anchors)
    └── PanelContainer (menu panel)
        └── MarginContainer
            └── VBoxContainer
                ├── Label (PAUSED)
                ├── Button (Resume)
                ├── Button (Settings)
                ├── Button (Main Menu)
                └── Button (Quit)
```

## Common UI Scripting Patterns

### Button Connections
```gdscript
@onready var start_button = $VBoxContainer/StartButton

func _ready():
    # Connect button signals
    start_button.pressed.connect(_on_start_button_pressed)

    # Or use Inspector to connect signals visually

func _on_start_button_pressed():
    # Handle button press
    get_tree().change_scene_to_file("res://scenes/main_game.tscn")
```

### Menu Navigation with Keyboard/Gamepad
```gdscript
func _ready():
    # Set first focusable button
    $VBoxContainer/StartButton.grab_focus()

    # Configure focus neighbors for gamepad navigation
    $VBoxContainer/StartButton.focus_neighbor_bottom = $VBoxContainer/SettingsButton.get_path()
    $VBoxContainer/SettingsButton.focus_neighbor_top = $VBoxContainer/StartButton.get_path()
    $VBoxContainer/SettingsButton.focus_neighbor_bottom = $VBoxContainer/QuitButton.get_path()
```

### Animated Transitions
```gdscript
# Fade in menu
func show_menu():
    modulate.a = 0
    visible = true
    var tween = create_tween()
    tween.tween_property(self, "modulate:a", 1.0, 0.3)

# Fade out menu
func hide_menu():
    var tween = create_tween()
    tween.tween_property(self, "modulate:a", 0.0, 0.3)
    tween.tween_callback(func(): visible = false)

# Slide in from side
func slide_in():
    position.x = -get_viewport_rect().size.x
    visible = true
    var tween = create_tween()
    tween.set_trans(Tween.TRANS_QUAD)
    tween.set_ease(Tween.EASE_OUT)
    tween.tween_property(self, "position:x", 0, 0.5)
```

### Dynamic Lists
```gdscript
# Populate ItemList dynamically
@onready var item_list = $ItemList

func populate_list(items: Array):
    item_list.clear()
    for item in items:
        item_list.add_item(item.name, item.icon)
        item_list.set_item_metadata(item_list.item_count - 1, item)

func _on_item_list_item_selected(index: int):
    var item = item_list.get_item_metadata(index)
    # Do something with selected item
```

### Health Bar Updates
```gdscript
@onready var health_bar = $HealthBar
var current_health = 100
var max_health = 100

func _ready():
    health_bar.max_value = max_health
    health_bar.value = current_health

func take_damage(amount: int):
    current_health = max(0, current_health - amount)

    # Smooth tween to new value
    var tween = create_tween()
    tween.tween_property(health_bar, "value", current_health, 0.2)

    # Change color based on health percentage
    if current_health < max_health * 0.3:
        health_bar.modulate = Color.RED
    elif current_health < max_health * 0.6:
        health_bar.modulate = Color.YELLOW
    else:
        health_bar.modulate = Color.GREEN
```

### Modal Popups
```gdscript
@onready var popup = $Popup

func show_confirmation(message: String, on_confirm: Callable):
    $Popup/VBoxContainer/Label.text = message
    popup.popup_centered()

    # Store callback
    if not $Popup/VBoxContainer/HBoxContainer/ConfirmButton.pressed.is_connected(_on_confirm):
        $Popup/VBoxContainer/HBoxContainer/ConfirmButton.pressed.connect(_on_confirm)

    confirm_callback = on_confirm

var confirm_callback: Callable

func _on_confirm():
    popup.hide()
    if confirm_callback:
        confirm_callback.call()
```

## UI Performance Optimization

**Best Practices:**
1. **Use CanvasLayers for depth management** instead of z_index when possible
2. **Clip content** in ScrollContainers with `clip_contents = true`
3. **Limit RichTextLabel complexity** - BBCode parsing can be slow
4. **Pool UI elements** - Reuse nodes instead of creating/destroying
5. **Use TextureAtlas** for UI sprites to reduce draw calls
6. **Batch similar elements** under same parent
7. **Disable processing** when UI is hidden: `process_mode = PROCESS_MODE_DISABLED`
8. **Use Control.clip_contents** to prevent rendering off-screen elements

**Memory Management:**
```gdscript
# Free unused UI scenes
func close_menu():
    queue_free()  # Instead of just hiding

# Object pooling for frequently created UI
var button_pool = []
const MAX_POOL_SIZE = 20

func get_pooled_button():
    if button_pool.is_empty():
        return Button.new()
    return button_pool.pop_back()

func return_to_pool(button: Button):
    if button_pool.size() < MAX_POOL_SIZE:
        button.get_parent().remove_child(button)
        button_pool.append(button)
    else:
        button.queue_free()
```

## Accessibility Features

**Text Scaling:**
```gdscript
# Support text size preferences
func apply_text_scale(scale: float):
    for label in get_tree().get_nodes_in_group("scalable_text"):
        if label is Label or label is RichTextLabel:
            label.add_theme_font_size_override("font_size", int(16 * scale))
```

**Gamepad Support:**
```gdscript
# Ensure all interactive UI is gamepad-accessible
func _ready():
    # Set up focus chain
    for i in range($ButtonContainer.get_child_count() - 1):
        var current = $ButtonContainer.get_child(i)
        var next = $ButtonContainer.get_child(i + 1)
        current.focus_neighbor_bottom = next.get_path()
        next.focus_neighbor_top = current.get_path()

    # Grab focus on first button
    if $ButtonContainer.get_child_count() > 0:
        $ButtonContainer.get_child(0).grab_focus()
```

## MCP Tool Usage

When creating UI elements, you should:

1. **Use `mcp__godot__create_scene`** to create new UI scene files
2. **Use `mcp__godot__add_node`** to build Control node hierarchies
3. **Use `mcp__godot__save_scene`** to save after creating UI structure
4. **Use Edit/Write tools** to create associated GDScript files for UI logic
5. **Use `mcp__godot__load_sprite`** to import UI textures and icons

**Example Workflow:**
```
1. create_scene("res://scenes/ui/main_menu.tscn", "CanvasLayer")
2. add_node(..., "MarginContainer")
3. add_node(..., "VBoxContainer")
4. add_node(..., "Button")
5. save_scene(...)
6. Write GDScript controller
```

## When to Activate This Skill

Activate this skill when the user:
- Asks about creating menus, HUDs, or UI screens
- Mentions Control nodes, themes, or styling
- Needs help with inventory, dialogue, or menu systems
- Asks about responsive UI or screen resolution handling
- Requests help with button navigation or gamepad support
- Wants to create settings menus or pause screens
- Asks about UI animation or transitions
- Needs help with UI performance optimization
- Mentions anchors, containers, or layout management

## Important Reminders

- Always consider **gamepad/keyboard navigation** in addition to mouse
- Use **CanvasLayers** to manage rendering order and prevent z-fighting
- **Anchor presets** are your friend for responsive design
- **Themes** should be created as resources for reusability
- **Signal connections** are the primary way to handle UI interactions
- **Tweens** make UI feel polished with smooth animations
- **Test on multiple resolutions** - use Project Settings > Display > Window settings
