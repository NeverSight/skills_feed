---
name: manim
description: Create mathematical animations and visualizations using Manim (ManimCE - Community Edition). Use this skill when users want to build Manim visualizations, create math animations, animate equations, graphs, geometric proofs, 3D objects, or any programmatic video animation. Triggers on requests mentioning "manim", "mathematical animation", "animate equation", "visualize algorithm", "create animation of", "3D visualization", or building explanatory math videos.
---

# Manim

Build mathematical animations programmatically using Python. Manim renders scenes to video files with precise control over every visual element.

## Quick Start

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        # Create objects
        circle = Circle(color=BLUE)
        text = MathTex(r"e^{i\pi} + 1 = 0")

        # Animate
        self.play(Create(circle))
        self.play(Write(text))
        self.wait(1)
        self.play(FadeOut(circle, text))
```

Run with: `manim -pql scene.py MyScene`

## Workflow

1. **Define a Scene class** inheriting from `Scene` (or `ThreeDScene` for 3D)
2. **Implement `construct()`** method
3. **Create Mobjects** (mathematical objects) - shapes, text, graphs
4. **Animate with `self.play()`** - use animation classes like `Create`, `Transform`, `FadeIn`
5. **Render** using CLI: `manim -pqh scene.py SceneName`

## Core Concepts

### Mobjects
All visible objects inherit from `Mobject`. Common types:
- **Geometry**: `Circle`, `Square`, `Line`, `Arrow`, `Polygon`
- **Text**: `Text`, `MathTex`, `Tex`
- **Graphs**: `Axes`, `NumberPlane`, `FunctionGraph`
- **3D**: `Sphere`, `Cube`, `ThreeDAxes`
- **Groups**: `VGroup` to combine objects

### Animations
Pass to `self.play()`:
- **Creation**: `Create`, `Write`, `FadeIn`, `GrowFromCenter`
- **Transform**: `Transform`, `ReplacementTransform`, `MoveToTarget`
- **Indication**: `Indicate`, `Flash`, `Circumscribe`
- **Removal**: `FadeOut`, `Uncreate`

### Positioning
```python
obj.move_to(ORIGIN)          # Move to point
obj.shift(RIGHT * 2)         # Relative shift
obj.next_to(other, UP)       # Position relative to another
obj.align_to(other, LEFT)    # Align edge
```

### Animation Parameters
```python
self.play(Create(obj), run_time=2)           # Duration
self.play(Create(obj), rate_func=smooth)     # Easing
self.play(anim1, anim2)                       # Simultaneous
self.play(Succession(anim1, anim2))          # Sequential
self.play(LaggedStart(*anims, lag_ratio=0.5)) # Staggered
```

## Common Patterns

### Mathematical Equation
```python
eq = MathTex(r"\int_0^1 x^2 \, dx = \frac{1}{3}")
self.play(Write(eq))
```

### Function Graph
```python
axes = Axes(x_range=[-3, 3], y_range=[-1, 5])
graph = axes.plot(lambda x: x**2, color=BLUE)
label = axes.get_graph_label(graph, label="x^2")
self.play(Create(axes), Create(graph), Write(label))
```

### Value Tracking (Animated Numbers)
```python
tracker = ValueTracker(0)
number = DecimalNumber(0).add_updater(
    lambda m: m.set_value(tracker.get_value())
)
self.add(number)
self.play(tracker.animate.set_value(10), run_time=2)
```

### 3D Scene
```python
class My3D(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        sphere = Sphere()
        self.set_camera_orientation(phi=75*DEGREES, theta=45*DEGREES)
        self.play(Create(axes), Create(sphere))
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(3)
```

### Transform Between States
```python
circle = Circle()
square = Square()
self.play(Create(circle))
self.play(Transform(circle, square))  # circle becomes square
```

## CLI Reference

```bash
manim scene.py SceneName      # Render scene
manim -p scene.py SceneName   # Preview after render
manim -s scene.py SceneName   # Save last frame only

# Quality flags
-ql  # Low (480p @ 15fps)
-qm  # Medium (720p @ 30fps)
-qh  # High (1080p @ 60fps)
-qk  # 4K (2160p @ 60fps)
```

## Key Gotchas

1. **Transform mutates first object**: After `Transform(a, b)`, reference `a` (now looks like `b`), not `b`
2. **Use ReplacementTransform** to avoid confusion: replaces `a` with `b` in scene
3. **Mobjects are mutable**: Use `.copy()` to avoid unintended changes
4. **LaTeX requires `r` prefix**: `MathTex(r"\frac{1}{2}")` not `MathTex("\frac{1}{2}")`
5. **3D requires ThreeDScene**: Regular `Scene` won't render 3D properly
6. **`self.add()` is instant**: Use `self.play(FadeIn(...))` for animated appearance

## References

- **Full API** (animations, mobjects, scenes, colors, constants): See [references/api.md](references/api.md)
- **Quick lookup** (tables, patterns, CLI): See [references/quick-reference.md](references/quick-reference.md)
