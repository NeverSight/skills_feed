---
name: creo-master-engineer
description: >
  Expert-level PTC Creo Parametric modeling and design engineering resource. Use when users ask about:
  part modeling (extrude, revolve, sweep, blend, helical sweep, swept blend, boundary blend),
  sketcher constraints and dimensions, datum features (planes, axes, points, coordinate systems),
  assembly design (constraints, placements, mechanisms, exploded views, BOM),
  surfacing (ISDX, Freestyle, boundary surfaces, variable section sweeps),
  sheet metal design (flanges, bends, flat patterns, K-factor, forming tools),
  drawing creation (views, dimensions, annotations, GD&T, tables, formats),
  relations and parameters (design intent, equations, conditional logic),
  family tables (instances, parameters, feature suppression),
  model analysis (mass properties, interference, clearance, measurements),
  design best practices, feature failure resolution, parent/child relationships,
  config.pro options, model-based definition (MBD), top-down design,
  or any general Creo Parametric modeling and design questions.
---

# Creo Parametric Master Engineer Reference

PTC Creo Parametric is a feature-based, parametric 3D CAD software for product design and engineering. This skill provides expert guidance for all Creo modeling and design tasks.

## Core Design Philosophy

### Parametric Modeling
- Features maintain relationships through constraints and dimensions
- Changes propagate automatically through parent/child dependencies
- Design intent captured via relations, parameters, and constraints

### Feature-Based Design
- Models built by combining individual features sequentially
- Each feature builds upon previous features (parent/child)
- Feature order affects model behavior and regeneration

### Design Intent
Capture design intent through:
- **Constraints**: Geometric relationships (parallel, perpendicular, tangent, etc.)
- **Dimensions**: Parametric values that can be modified
- **Relations**: Equations linking dimensions and parameters
- **References**: How features connect to existing geometry

## Part Modeling Fundamentals

### Base Features (Shape-Based)

| Feature | Use Case | Requirements |
|---------|----------|--------------|
| Extrude | Constant cross-section along linear path | Closed sketch, depth |
| Revolve | Axisymmetric shapes | Closed sketch, axis, angle |
| Sweep | Cross-section along curved path | Trajectory + section sketch |
| Blend | Variable cross-sections at intervals | Multiple closed sketches, same entity count |
| Helical Sweep | Springs, threads, coils | Pitch/turns, axis, section |
| Swept Blend | Variable section along path | Trajectory + multiple sections |
| Boundary Blend | Surface from boundary curves | 2+ boundary chains |

### Engineering Features

| Feature | Purpose | Key Parameters |
|---------|---------|----------------|
| Hole | Standard/custom holes | Type (simple/standard), diameter, depth, thread |
| Round | Fillet edges | Radius, variable radius, full round |
| Chamfer | Beveled edges | D×D, D×A, 45°×D |
| Draft | Taper for moldability | Angle, pull direction, split |
| Shell | Hollow solid | Thickness, removed surfaces |
| Rib | Reinforcement structure | Sketch, thickness, draft |
| Pattern | Duplicate features | Dimension/direction/fill/table patterns |
| Mirror | Symmetric features | Mirror plane, dependency type |

### Sketch Constraints

| Constraint | Symbol | Description |
|------------|--------|-------------|
| Horizontal | H | Entity parallel to X-axis |
| Vertical | V | Entity parallel to Y-axis |
| Perpendicular | ⊥ | 90° angle between entities |
| Parallel | ∥ | Entities same orientation |
| Tangent | T | Smooth transition between curves |
| Equal | L= or R= | Equal length/radius |
| Coincident | • | Points share location |
| Symmetric | ↔ | Mirror about centerline |
| Collinear | — | Lines share same infinite line |

### Datum Features

- **Datum Planes**: Reference planes for sketching and orientation
  - Through point/line/plane, offset, angle, tangent
- **Datum Axes**: Reference lines for patterns, revolutions
  - Through cylinder, intersection, normal to surface
- **Datum Points**: Reference locations for measurements
  - On surface, curve, vertex, offset
- **Coordinate Systems**: Origin + orientation for analysis, assembly
  - Three planes, two axes + origin

## Sketcher Best Practices

1. **Start with strong references** - Select appropriate sketching plane and orientation
2. **Sketch loosely first** - Add constraints before precise dimensions
3. **Use intent manager** - Let Creo infer constraints from sketch geometry
4. **Minimize dimensions** - Use constraints where possible
5. **Dimension to design intent** - Dimension what you want to control
6. **Close all contours** - Solid features require closed sketches
7. **Avoid over-constraining** - Watch for conflicting constraints (red)

## Reference Files

For detailed information, see:
- **references/assembly-design.md** - Assembly constraints, mechanisms, BOM
- **references/surfacing.md** - Advanced surface creation and editing
- **references/sheetmetal.md** - Sheet metal features, bend tables, flat patterns
- **references/drawings.md** - Drawing views, annotations, GD&T
- **references/relations-parameters.md** - Relations, parameters, family tables
- **references/config-options.md** - Important configuration options
- **references/troubleshooting.md** - Feature failure resolution, best practices

## Quick Reference Commands

### Common Workflows

**Create new part:**
1. File > New > Part > Solid
2. Select template (mmns_part_solid or inlbs_part_solid)
3. Create first feature on default datum planes

**Create sketch:**
1. Select sketching plane
2. Choose sketch orientation reference
3. Draw geometry with constraints
4. Add dimensions for size control
5. Accept sketch when fully constrained (green)

**Add material:**
- Extrude/Revolve/Sweep/Blend with default material side

**Remove material:**
- Same features with "Remove Material" option
- Or use Hole, Cut features

**Modify feature:**
- Double-click dimension to edit value
- Right-click feature > Edit Definition for full control
- Right-click feature > Edit References to change parents

### Keyboard Shortcuts (Default)

| Shortcut | Action |
|----------|--------|
| Ctrl+S | Save |
| Ctrl+R | Repaint |
| Ctrl+G | Regenerate |
| Ctrl+D | Standard orientation |
| Middle-click+drag | Rotate view |
| Shift+Middle+drag | Pan view |
| Scroll wheel | Zoom |
| Ctrl+Alt+Middle | Spin model |

## Model Quality Checklist

- [ ] Features named descriptively
- [ ] Parameters named and organized
- [ ] Relations documented with comments
- [ ] Appropriate parent/child relationships
- [ ] Regeneration successful without warnings
- [ ] Model centered on coordinate system
- [ ] Mass properties assigned (material)
- [ ] Drawing views up to date
