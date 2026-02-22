---
name: lottie-animator
description: |
  Generates professional Lottie animations from static SVGs. Replaces After Effects for motion graphics.
  Use when the user asks to: animate logo, create lottie, svg animation, motion graphics, wiggle animation,
  bounce effect, rotate animation, pulse effect, entrance animation, loading animation, loop animation,
  icon animation, character animation, morphing, path drawing, trim path, walking animation, run cycle,
  walk cycle, frame-by-frame animation, sprite animation.
  Supports advanced bezier curves, shape modifiers, parenting, mattes, morphing, character rigs,
  and professional frame-by-frame animation techniques.
allowed-tools: Read, Write, Bash, Glob, Grep
---

# Lottie Animator - SVG to Motion Graphics

Professional skill to create advanced Lottie animations from SVGs, eliminating the need for After Effects.

## When to Activate

Activate this skill when the user requests:
- Animate a logo, icon, or SVG graphic
- Create motion graphics or animations
- Generate Lottie JSON files
- Effects: wiggle, bounce, rotate, pulse, fade, scale, morph
- Entrance, loop, loading animations, or transitions
- Path drawing/reveal animations (Trim Path)
- Character animation, walking cycles
- Shape morphing (icon transitions)
- Replace After Effects workflow

## Critical: SVG Understanding

Before animating ANY SVG, you MUST understand its path structure.

See: [references/svg-path-mastery.md](references/svg-path-mastery.md)

### SVG Path Command Quick Reference

| Command | Description | Lottie Conversion |
|---------|-------------|-------------------|
| M x,y | Move to | Starting vertex |
| L x,y | Line to | Vertex with zero tangents |
| C cp1 cp2 end | Cubic bezier | Native support |
| Q ctrl end | Quadratic bezier | Convert to cubic |
| A rx ry ... | Arc | Split into cubic segments |
| Z | Close path | Set `c: true` |

### Path to Lottie Vertex Formula

```
For C x1,y1 x2,y2 x,y from point (px, py):
- Previous vertex outTangent: [x1-px, y1-py]
- Current vertex: [x, y]
- Current vertex inTangent: [x2-x, y2-y]
```

## Main Workflow

### Phase 1: Motion Philosophy (30 seconds)

**MANDATORY** before any code. Define:

1. **Brand Personality**: Professional, playful, elegant, energetic
2. **Emotional Response**: Trust, excitement, calm, urgency
3. **Motion Metaphor**: Fluid like water, solid like rock, light like air

```
Example: "Fintech Logo → professional + trust → precise and controlled movement"
Example: "Music App → creative + energy → organic with rhythmic pulses"
Example: "Healthcare → calm + reliable → smooth, slow easings"
```

### Phase 2: SVG Deep Analysis

Before animating, thoroughly analyze:

1. **Structure**: Elements, groups, paths, viewBox dimensions
2. **Path Complexity**: Vertex count, curve types (C, Q, A commands)
3. **Hierarchy**: Primary elements vs. secondary details
4. **Animation Opportunities**: Independent parts, stroke-based vs fill-based

```bash
# Analyze SVG structure
cat icon.svg | grep -E '<(path|g|rect|circle|ellipse|line|polyline)' | head -30
```

**Key Questions**:
- Is it stroke-based? → Consider Trim Path animation
- Multiple paths? → Consider staggered entrance
- Complex shape? → Consider scale/rotate instead of morph
- Icon library (Phosphor/Lucide)? → Usually clean, minimal vertices

### Phase 3: Animation Strategy Selection

| Strategy | Best For | Technique |
|----------|----------|-----------|
| Draw On | Stroke icons, signatures | Trim Path |
| Pop In | Logos, buttons | Scale + Opacity |
| Morph | Icon transitions (hamburger→X) | Path keyframes |
| Stagger | Multiple elements | Delayed start times |
| Character | People, mascots | Parenting + bone hierarchy |
| Loader | Progress, spinners | Rotation + Trim Path |
| **Frame-by-Frame** | Walk/run cycles, complex characters | ip/op layer switching |

**Pro Tip**: For complex character animations (walk cycles, run cycles), use **Frame-by-Frame** technique instead of continuous animation. See [references/professional-techniques.md](references/professional-techniques.md)

### Phase 4: Create Lottie JSON

See: [references/lottie-structure.md](references/lottie-structure.md)

**Base Structure:**
```json
{
  "v": "5.12.1",
  "fr": 60,
  "ip": 0,
  "op": 120,
  "w": 512,
  "h": 512,
  "nm": "Animation Name",
  "ddd": 0,
  "assets": [],
  "layers": []
}
```

### Phase 5: Apply Professional Easing

See: [references/bezier-easing.md](references/bezier-easing.md)

| Use Case | Out Tangent | In Tangent |
|----------|-------------|------------|
| Entrance | `[0.33, 0]` | `[0.67, 1]` |
| Exit | `[0.55, 0.055]` | `[0.675, 0.19]` |
| Loop | `[0.645, 0.045]` | `[0.355, 1]` |
| Bounce | `[0.34, 1.56]` | `[0.64, 1]` |
| Spring | `[0.5, 1.5]` | `[0.5, 0.9]` |

### Phase 6: Validate and Export

```bash
# Validate JSON structure
python3 -c "import json; json.load(open('animation.json'))"

# Preview
echo "Open in: https://lottiefiles.com/preview"
```

## Shape Modifiers

See: [references/shape-modifiers.md](references/shape-modifiers.md)

### Trim Path (Icon Drawing Animation)

```json
{
  "ty": "tm",
  "s": {"a": 0, "k": 0},
  "e": {
    "a": 1,
    "k": [
      {"t": 0, "s": [0], "o": {"x": [0.33], "y": [0]}, "i": {"x": [0.67], "y": [1]}},
      {"t": 45, "s": [100]}
    ]
  },
  "o": {"a": 0, "k": 0},
  "m": 1
}
```

### Repeater (Radial/Linear Patterns)

```json
{
  "ty": "rp",
  "c": {"a": 0, "k": 8},
  "tr": {
    "r": {"a": 0, "k": 45},
    "so": {"a": 0, "k": 100},
    "eo": {"a": 0, "k": 30}
  }
}
```

### Offset Path (Glow/Outline Effects)

```json
{
  "ty": "op",
  "a": {"a": 1, "k": [{"t": 0, "s": [0]}, {"t": 30, "s": [8]}]},
  "lj": 2
}
```

## Advanced Techniques

See: [references/advanced-animation.md](references/advanced-animation.md) and [references/professional-techniques.md](references/professional-techniques.md)

### Frame-by-Frame Animation (Professional Technique)

The most professional technique for complex character animations. Instead of continuous animation, create multiple "poses" that appear/disappear in sequence using `ip` (in point) and `op` (out point).

```json
{
  "layers": [
    {"nm": "Pose 1", "ip": 0, "op": 6, "shapes": [/* pose 1 */]},
    {"nm": "Pose 2", "ip": 6, "op": 12, "shapes": [/* pose 2 */]},
    {"nm": "Pose 3", "ip": 12, "op": 18, "shapes": [/* pose 3 */]}
  ]
}
```

**Timing Formula**: `Total Frames = Poses × Frames_per_Pose` → `Duration = Total Frames / FPS`

**When to Use**:
- Walk/run cycles (each pose is a different leg position)
- Complex character animations with drastic shape changes
- When morphing produces ugly results
- Professional sprite-sheet style animations

### Layer Parenting (Bone Hierarchy)

Use `parent` property to create hierarchies where moving one layer moves all children.

```json
{
  "layers": [
    {"ind": 14, "nm": "Shadow", "ks": {"p": {"a": 0, "k": [340, 195, 0]}}},
    {"ind": 1, "nm": "Head", "parent": 14, "ks": {"p": {"a": 0, "k": [88, -84, 0]}}},
    {"ind": 2, "nm": "Body", "parent": 14, "ks": {"p": {"a": 0, "k": [0, -50, 0]}}}
  ]
}
```

**Key Insight**: Child positions are **RELATIVE** to parent. Moving Shadow moves all children with it.

**Professional Parent Strategies**:
- **Shadow as Parent**: Move shadow → entire character moves (for walk cycles)
- **Body as Parent**: Limbs and head follow body rotation
- **Joint as Parent**: Upper arm controls forearm and hand rotation

**Parent Chain Example**:
```
Shadow (Parent for entire character)
├── Head (child)
├── Body (child)
├── Ear Inner (child)
├── Eye (child)
└── ... 13 total children
```

### Path Morphing (Same Vertex Count Required)

```json
{
  "ty": "sh",
  "ks": {
    "a": 1,
    "k": [
      {"t": 0, "s": [{"c": true, "v": [[0,0], [100,0], [100,100], [0,100]], "i": [...], "o": [...]}]},
      {"t": 30, "s": [{"c": true, "v": [[50,-20], [120,50], [50,120], [-20,50]], "i": [...], "o": [...]}]}
    ]
  }
}
```

**Critical Rule**: Both shapes MUST have identical vertex count for smooth morphing.

### Track Mattes (Masking)

```json
// Matte layer (defines visible area)
{"ind": 1, "nm": "Matte", "td": 1, "ty": 4, ...}

// Content layer (uses the matte)
{"ind": 2, "nm": "Content", "tt": 1, "ty": 4, ...}
```

| tt Value | Mode |
|----------|------|
| 1 | Alpha Matte |
| 2 | Alpha Inverted |
| 3 | Luma Matte |
| 4 | Luma Inverted |

## Animation Principles Applied

### 1. Anticipation
```json
"s": {"a": 1, "k": [
  {"t": 0, "s": [100, 100]},
  {"t": 8, "s": [95, 105]},    // Slight crouch
  {"t": 25, "s": [115, 90]},   // Main action
  {"t": 40, "s": [100, 100]}
]}
```

### 2. Squash & Stretch (Volume Preservation)
```json
// X * Y should stay roughly constant
{"t": 0, "s": [100, 100]},   // 10000
{"t": 10, "s": [120, 83]},   // 9960 ≈ preserved
{"t": 20, "s": [85, 118]}    // 10030 ≈ preserved
```

### 3. Staggered Timing
```json
{"ind": 1, "st": 0, "ip": 0},
{"ind": 2, "st": 3, "ip": 3},   // 3 frame delay
{"ind": 3, "st": 6, "ip": 6},   // 6 frame delay
{"ind": 4, "st": 9, "ip": 9}    // 9 frame delay
```

### 4. Follow-Through with Overshoot
```json
"r": {"a": 1, "k": [
  {"t": 0, "s": [0]},
  {"t": 15, "s": [95]},    // Overshoot target
  {"t": 25, "s": [88]},    // Settle back
  {"t": 35, "s": [90]}     // Final position
]}
```

## Common Animation Recipes

### Loading Spinner
```json
{
  "shapes": [
    {"ty": "el", "s": {"a": 0, "k": [60, 60]}},
    {"ty": "st", "w": {"a": 0, "k": 4}, "c": {"a": 0, "k": [0.2, 0.5, 1, 1]}, "lc": 2},
    {"ty": "tm", "s": {"a": 0, "k": 0}, "e": {"a": 0, "k": 75},
     "o": {"a": 1, "k": [{"t": 0, "s": [0]}, {"t": 60, "s": [360]}]}}
  ],
  "ks": {"r": {"a": 1, "k": [{"t": 0, "s": [0]}, {"t": 120, "s": [360]}]}}
}
```

### Checkmark Draw
```json
{
  "shapes": [
    {"ty": "sh", "ks": {"a": 0, "k": {"c": false, "v": [[20,50], [40,70], [80,30]], "i": [[0,0], [0,0], [0,0]], "o": [[0,0], [0,0], [0,0]]}}},
    {"ty": "st", "w": {"a": 0, "k": 6}, "c": {"a": 0, "k": [0.2, 0.8, 0.4, 1]}, "lc": 2, "lj": 2},
    {"ty": "tm", "e": {"a": 1, "k": [{"t": 0, "s": [0]}, {"t": 30, "s": [100]}]}}
  ]
}
```

### Heart Beat (Organic)
```json
"s": {"a": 1, "k": [
  {"t": 0, "s": [100, 100]},
  {"t": 8, "s": [115, 115]},    // Systole (Lub)
  {"t": 12, "s": [90, 90]},     // Diastole start (Dub)
  {"t": 18, "s": [105, 105]},   // Refill
  {"t": 45, "s": [100, 100]}    // Rest
]}
```

### Icon Pop-In with Bounce
```json
{
  "ks": {
    "s": {"a": 1, "k": [
      {"t": 0, "s": [0, 0], "o": {"x": [0.34], "y": [1.56]}, "i": {"x": [0.64], "y": [1]}},
      {"t": 18, "s": [110, 110], "o": {"x": [0.33], "y": [0]}, "i": {"x": [0.67], "y": [1]}},
      {"t": 30, "s": [100, 100]}
    ]},
    "o": {"a": 1, "k": [
      {"t": 0, "s": [0]},
      {"t": 12, "s": [100]}
    ]}
  }
}
```

## Icon Library Optimization

### Phosphor/Lucide Icons
- **ViewBox**: Usually 256x256 (Phosphor) or 24x24 (Lucide)
- **Structure**: Clean paths, minimal vertices
- **Strokes**: `stroke-linecap="round"` for Trim Path compatibility
- **Scale**: Match your canvas to viewBox for 1:1

### Recommended Animation Approach

1. **Simple icons** → Scale + Opacity entrance
2. **Stroke icons** → Trim Path drawing
3. **Multi-part icons** → Staggered entrance
4. **Toggle icons** → Path morphing (if vertex counts match)

### Stroke + Fill Combination (Outline Style)

For professional character animations, combine **stroke (contour) + fill (color)** in each shape:

```json
{
  "ty": "gr",
  "it": [
    {"ty": "sh", "ks": {...}},
    {"ty": "st", "c": {"a": 0, "k": [0.259, 0.153, 0.141, 1]}, "w": {"a": 0, "k": 1}, "lc": 2, "lj": 2},
    {"ty": "fl", "c": {"a": 0, "k": [0.302, 0.604, 0.816, 1]}},
    {"ty": "tr", ...}
  ]
}
```

**Stroke Properties**:
| Property | Value | Description |
|----------|-------|-------------|
| `lc` (lineCap) | 1=Butt, 2=Round, 3=Square | Line end style |
| `lj` (lineJoin) | 1=Miter, 2=Round, 3=Bevel | Corner style |

**Professional Color Palette Example** (from Running Cat):
```json
{
  "body_fill": [0.302, 0.604, 0.816, 1],
  "outline": [0.259, 0.153, 0.141, 1],
  "eye_white": [0.902, 0.976, 1.0, 1],
  "shadow": [0.608, 0.706, 0.878, 1]
}
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| Non-looping | Last keyframe ≠ first value | Match start/end keyframe values |
| Stiff movement | No easing curves | Add bezier `i`/`o` tangents |
| Jerky animation | Keyframes too sparse | Add intermediate keyframes |
| Morph glitches | Different vertex counts | Add/remove vertices to match |
| Wrong rotation pivot | Incorrect anchor point | Set `a` to rotation center |
| Path draws wrong direction | Path not reversed | Use `"d": 3` to reverse |
| Ugly character animation | Trying to morph complex shapes | Use frame-by-frame instead |

## Performance Guidelines

1. **Layers**: <15 for complex animations
2. **Vertices**: <20 per shape for smooth morphing
3. **Frame Rate**: 30fps often sufficient, 60fps for ultra-smooth
4. **Modifiers**: Avoid nested repeaters
5. **Effects**: Minimize blur/shadow usage
6. **File Size**: Target <50KB for icons, <200KB for complex

## References

- [SVG Path Mastery](references/svg-path-mastery.md) - **START HERE** for SVG understanding
- [Professional Techniques](references/professional-techniques.md) - **Frame-by-frame, parenting, outline style**
- [Lottie JSON Structure](references/lottie-structure.md)
- [Bezier Curves and Easing](references/bezier-easing.md)
- [Shape Modifiers](references/shape-modifiers.md)
- [Advanced Animation](references/advanced-animation.md)
- [SVG to Lottie Conversion](references/svg-to-lottie.md)
- [Animation Examples](references/examples.md)
- [Official Lottie Documentation](https://lottiefiles.github.io/lottie-docs/)

## Final Checklist

- [ ] Motion philosophy defined
- [ ] SVG structure analyzed (path commands understood)
- [ ] Animation strategy selected (consider frame-by-frame for characters)
- [ ] Vertex counts verified (for morphing)
- [ ] Anchor points set correctly (for rotation)
- [ ] Parent hierarchy established (for characters)
- [ ] Keyframes with professional easing
- [ ] Animation principles applied (anticipation, follow-through)
- [ ] Stroke + fill style applied (for outline look)
- [ ] Seamless loop verified (if applicable)
- [ ] JSON validated
- [ ] Preview tested at https://lottiefiles.com/preview
