---
name: create-visualization
description: Creates diagrams and animations for STEM education using Matplotlib and Manim. Use for physics diagrams (FBD, vectors), math plots (functions, geometry), flowcharts, or 3Blue1Brown-style animations.
---

# Visualization Skill

สร้าง diagrams และ animations สำหรับอธิบาย STEM concepts

## Quick Decision

| Need | Tool | Script |
|------|------|--------|
| Physics FBD | Matplotlib | `scripts/physics_fbd.py` |
| Math plots/geometry | Matplotlib | `scripts/math_plots.py` |
| Flowcharts | Matplotlib | `scripts/flowchart.py` |
| Animations (3b1b style) | Manim | `scripts/manim_physics.py` |

**Rule:** Static → Matplotlib (fast) | Motion/transform → Manim (powerful)

---

## 1. Physics: Free Body Diagrams

```python
from scripts.physics_fbd import draw_inclined_plane_fbd, draw_two_blocks_rope

# Inclined plane with force decomposition
draw_inclined_plane_fbd(mass=4, angle=30, show_components=True)

# Two blocks connected by rope
draw_two_blocks_rope(mass_A=2, mass_B=3, F_pull=10)
```

**Output:** PNG in `learning-notes/` folder

---

## 2. Math: Plots & Geometry

```python
from scripts.math_plots import plot_function, draw_unit_circle, draw_coordinate_plane
import numpy as np

# Function plot
plot_function(lambda x: np.sin(x), x_range=(-2*np.pi, 2*np.pi), title="sin(x)")

# Unit circle with angles
draw_unit_circle(angles_deg=[0, 30, 45, 60, 90])

# Coordinate plane with vectors
draw_coordinate_plane(
    vectors=[((0,0), (3,2), "a", "red"), ((0,0), (1,4), "b", "blue")]
)
```

---

## 3. Flowcharts

```python
from scripts.flowchart import draw_simple_flowchart, draw_decision_flowchart

# Linear flow
draw_simple_flowchart([
    ("Start", "start"),
    ("Input x", "io"),
    ("Process", "process"),
    ("End", "end"),
])

# Decision branching
draw_decision_flowchart(
    before_decision=[("Start", "start")],
    decision_text="x > 0?",
    yes_branch=[("Positive", "process")],
    no_branch=[("Negative", "process")],
    after_merge=[("End", "end")]
)
```

---

## 4. Animations (Manim)

For 3Blue1Brown-style animations. See **[references/manim-guide.md](references/manim-guide.md)** for full guide.

### Available Scenes in `scripts/manim_physics.py`

| Scene | Description |
|-------|-------------|
| `VectorAddition` | Head-to-tail vector addition |
| `ForcesOnBox` | FBD with motion |
| `NewtonThirdLaw` | Action-reaction pairs |
| `InclinedPlane` | Forces on incline with equations |
| `ProjectileMotion` | Parabolic path with velocity vectors |
| `CircularMotion` | Centripetal acceleration |
| `AtwoodIncline` | Pulley system (customizable m1, m2, θ) |

### Render Command

```bash
# Preview (low quality, fast)
manim -pql scripts/manim_physics.py VectorAddition

# GIF output
manim -ql --format=gif scripts/manim_physics.py VectorAddition
```

### Custom Animation

```python
from manim import *

class MyScene(Scene):
    def construct(self):
        circle = Circle(color=BLUE)
        self.play(Create(circle))
        self.play(circle.animate.shift(RIGHT * 2))
```

---

## 5. Function Explainer Visualization

สร้างภาพอธิบายการทำงานของ Excel/DAX/Power Query functions

### Quick Start

```bash
# 1. Generate visualization
python3 tools/visualize_function.py excel left 1

# 2. Upload to server (--mkdir creates directory if needed)
python3 tools/ftp_upload.py -f media/function-viz/excel/left-1.png -r wp-content/uploads/function-viz/excel/ --mkdir

# 3. Add image_url to JSON example, then publish
python3 tools/smart_publish.py --slugs left --program excel --allow
```

**Output:** `media/function-viz/{program}/{slug}-{example_number}.png`
**Server:** `https://www.thepexcel.com/wp-content/uploads/function-viz/{program}/{slug}-{example}.png`

### Supported Functions

| Function | Description |
|----------|-------------|
| LEFT | ดึงตัวอักษรจากซ้าย |
| RIGHT | ดึงตัวอักษรจากขวา |
| MID | ดึงตัวอักษรจากตรงกลาง |
| FIND | หาตำแหน่งข้อความ |
| SUBSTITUTE | แทนที่ข้อความ |

### Workflow

1. **Generate** — `python3 tools/visualize_function.py {program} {slug} {example_num}`
2. **Upload** — `python3 tools/ftp_upload.py -f {file} -r wp-content/uploads/function-viz/{program}/ --mkdir`
3. **Update JSON** — เพิ่ม `"image_url": "https://..."` ใน example
4. **Publish** — `python3 tools/smart_publish.py --slugs {slug} --program {program} --allow`

### Custom Visualization (Nested Functions)

สำหรับ formula ซับซ้อน เช่น `=LEFT(A1, FIND(" ", A1)-1)` ต้องเขียน script แยก:

```python
# ดูตัวอย่างที่ media/function-viz/excel/left-5-custom.py
```

**Note:** Script หลักรองรับ formula ง่ายๆ ที่มี string literal เท่านั้น

---

## Workflow

1. **Choose tool** — Static (Matplotlib) vs Animation (Manim)
2. **Run script** — `python3 scripts/physics_fbd.py` or `manim -pql ...`
3. **View output** — `explorer.exe output.png` or use image viewer

**Tip:** Use `run_in_background=true` for viewers to avoid blocking conversation.

## Related Skills (Optional)

| When | Suggest |
|------|---------|
| AI-generated images/videos (realistic, artistic) | `/prompt-ai-image-video` - prompt engineering |
| Teaching concepts with visuals | `/explain-concepts` - ACES methodology |
| Need facts before visualizing | `/deep-research` - verify data |
| Problem-solving context | `/problem-solving` - structured thinking |

**Note:** Use `/create-visualization` for technical diagrams (FBD, plots, flowcharts). Use `/prompt-ai-image-video` for AI-generated realistic/artistic images and videos.
