---
name: 3b1b-style-animation
description: Create mathematical animations in 3Blue1Brown style using Manim
metadata:
  author: subinium
  version: 2.1.0
  tags: manim, 3b1b, math, education, visualization, animation
---

## When to use

Use this skill when creating mathematical animations, visualizations, or educational videos using Manim (ManimCE).

---

## Quick Reference (Core Patterns)

### Colors
```python
BG = "#1c1c1c"           # Background (MUST use)
BLUE = "#3b82f6"         # Primary, nodes
YELLOW = "#fbbf24"       # Highlights, emphasis
GREEN = "#22c55e"        # Success, done, positive
RED = "#ef4444"          # Error, negative
GRAY = "#9ca3af"         # Inactive, labels
```

### Scene Template
```python
from manim import *

class MyScene(Scene):
    def construct(self):
        self.camera.background_color = "#1c1c1c"
        # Your code here
        self.wait(2)  # End padding
```

### Audio-Synced Scene (StrictSync)
```python
TIMING = {
    "01": {"start": 0, "end": 5.5},
    "02": {"start": 5.5, "end": 10.0},
}

class SyncedScene(Scene):
    def construct(self):
        self.camera.background_color = "#1c1c1c"
        for seg_id in sorted(TIMING.keys()):
            method = getattr(self, f"seg_{seg_id}", None)
            if method:
                self._run(seg_id, method)
        self.wait(2)

    def _run(self, seg_id, method):
        t = TIMING[seg_id]
        target = t["end"] - t["start"]
        start = self.renderer.time
        method()
        elapsed = self.renderer.time - start
        if elapsed < target:
            self.wait(target - elapsed)

    def seg_01(self):
        pass  # Your animation
```

### Animation Patterns
```python
# Cascading appear
self.play(LaggedStartMap(FadeIn, VGroup(*items), lag_ratio=0.15), run_time=1)

# Highlight
self.play(Flash(mob, color=YELLOW, line_length=0.2), run_time=0.3)
self.play(Indicate(mob, color=YELLOW), run_time=0.5)

# Transform text
self.play(TransformMatchingStrings(old_text, new_text), run_time=0.5)

# Coordinated (not sequential)
self.play(FadeIn(a), Create(b), Write(c), run_time=1)  # Good
# self.play(FadeIn(a)); self.play(Create(b))  # Bad
```

### Layout
```python
# Screen zones
title.to_edge(UP, buff=0.5)
content.move_to(ORIGIN)
info.to_edge(DOWN, buff=0.8)
sidebar.to_edge(RIGHT, buff=1.0)

# Spacing constants
NODE_GAP = 1.5        # Minimum between nodes
EDGE_LABEL_OFFSET = 0.22  # Perpendicular to edge

# Edge label placement
mid = line.get_center()
direction = end - start
perp = np.array([-direction[1], direction[0], 0])
perp = perp / np.linalg.norm(perp) * 0.22
label.move_to(mid + perp)
```

### Graph Creation Pattern
```python
self.node_to_circle = {}  # Dictionary mapping
for name, pos in positions.items():
    circle = Circle(radius=0.3, color=BLUE, fill_opacity=0.5, stroke_width=2)
    circle.move_to(pos)
    self.node_to_circle[name] = circle
```

### Pedagogy (3b1b Style)
```
1. HOOK: Pose interesting question
2. INTUITION: Visual understanding (NO formulas yet)
3. STEP-BY-STEP: Concrete example with numbers
4. FORMALIZATION: NOW introduce formula/name
```

---

## Rules (Detailed Reference)

### Setup & Basics
- [rules/manim-setup.md](rules/manim-setup.md) - Installation
- [rules/scene-basics.md](rules/scene-basics.md) - Scene structure
- [rules/color-scheme.md](rules/color-scheme.md) - Full color palette

### Animation
- [rules/animation-patterns.md](rules/animation-patterns.md) - LaggedStartMap, state save/restore
- [rules/text-transforms.md](rules/text-transforms.md) - TransformMatchingStrings
- [rules/updaters.md](rules/updaters.md) - add_updater for dynamic motion
- [rules/seamless-transitions.md](rules/seamless-transitions.md) - Smooth transitions

### Layout & Visual
- [rules/layout-spacing.md](rules/layout-spacing.md) - Spacing, screen zones
- [rules/mobject-grouping.md](rules/mobject-grouping.md) - VGroup organization
- [rules/visual-quality.md](rules/visual-quality.md) - Quality checks
- [rules/camera-work.md](rules/camera-work.md) - MovingCameraScene

### Content Types
- [rules/equations.md](rules/equations.md) - LaTeX, MathTex
- [rules/graphs.md](rules/graphs.md) - Function plotting
- [rules/3d-surfaces.md](rules/3d-surfaces.md) - ThreeDScene

### Audio & Sync
- [rules/audio-sync.md](rules/audio-sync.md) - Audio-visual sync
- [rules/strict-sync.md](rules/strict-sync.md) - StrictSyncScene

### Philosophy
- [rules/pedagogy.md](rules/pedagogy.md) - Intuition before formalism

---

## MUST / MUST NOT

### MUST
- Use `#1c1c1c` background
- Use `LaggedStartMap` for cascading effects
- Group related elements with VGroup + dictionary
- End with `self.wait(2)` for padding
- Keep NODE_GAP >= 1.5
- Place edge labels perpendicular to edge

### MUST NOT
- Use pure black (#000000) background
- Animate elements one-by-one with separate play() calls
- Place nodes too close (< 1.5 units apart)
- Show formulas before building intuition
- End play() without wait()
