---
name: rive-scripting
description: |
  Trigger when: (1) Working with Rive scripts or Luau code,
  (2) Code contains Node, Layout, Converter, or PathEffect protocols,
  (3) User mentions "Rive scripting" or "Rive Luau",
  (4) Drawing with Path, Paint, Renderer APIs,
  (5) Files have .lua extension in a Rive project context.

  Best practices for Rive Scripting - Luau-based scripts for procedural
  graphics, custom layouts, data converters, and path effects that run
  inside Rive animations.
metadata:
  tags: rive, scripting, luau, animation, graphics, procedural
---

# Rive Scripting

Rive Scripting uses Luau (Roblox's Lua variant) to create interactive and procedural behaviors inside Rive animations. Scripts run in the Rive editor and export with your .riv file.

## Script Types

| Type | Purpose | Key Methods |
|------|---------|-------------|
| **Node Script** | Procedural drawing and interactivity | `init`, `advance`, `update`, `draw` |
| **Layout Script** | Custom sizing and positioning | `measure`, `resize` |
| **Converter Script** | Transform data for bindings | `convert`, `reverseConvert` |
| **PathEffect Script** | Modify paths procedurally | `effect` |
| **Util Script** | Reusable helper functions | `exports` |

## Luau Quick Reference

```lua
-- Types
type MyState = {
  count: number,
  active: boolean,
  items: {string},
}

-- Functions
local function add(a: number, b: number): number
  return a + b
end

-- Tables
local t = {x = 10, y = 20}
t.z = 30

-- Conditionals
if value > 0 then
  -- positive
elseif value < 0 then
  -- negative
else
  -- zero
end

-- Loops
for i = 1, 10 do
  print(i)
end

for key, value in pairs(table) do
  print(key, value)
end
```

## Core Pattern

All Rive scripts follow this pattern:

```lua
-- 1. Define your state type
type MyNode = {
  path: Path,
  paint: Paint,
  time: number,
}

-- 2. Define protocol methods
function draw(self: MyNode, renderer: Renderer)
  renderer:drawPath(self.path, self.paint)
end

function advance(self: MyNode, elapsed: number)
  self.time = self.time + elapsed
end

-- 3. Return factory function
return function(): Node<MyNode>
  return {
    draw = draw,
    advance = advance,
    path = Path.new(),
    paint = Paint.new(),
    time = 0,
  }
end
```

## Key APIs

### Drawing
- `Path` - Vector paths (moveTo, lineTo, quadTo, cubicTo, close)
- `Paint` - Fill/stroke styling (color, gradient, thickness)
- `Renderer` - Drawing operations (drawPath, clipPath, transform)

### Geometry
- `Vec2D` - 2D vectors (xy, length, normalize, dot)
- `AABB` - Axis-aligned bounding boxes
- `Mat2D` - 2D transformation matrices

### Data
- `ViewModel` - Access bound data
- `Property` - Read/write data values
- `Trigger` - Fire events

## Rules

@file rules/getting-started.md
@file rules/node-scripts.md
@file rules/drawing.md
@file rules/pointer-events.md
@file rules/layout-scripts.md
@file rules/converter-scripts.md
@file rules/path-effects.md
@file rules/data-binding.md
@file rules/util-scripts.md
@file rules/api-reference.md
