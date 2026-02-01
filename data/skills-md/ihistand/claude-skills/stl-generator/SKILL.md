---
name: stl-generator
description: Generate 3D printable STL files for woodworking jigs and fixtures using CadQuery. Use when the user requests lampshade jigs, circle cutting guides, angle wedges, spacing blocks, alignment fixtures, router jigs, or any custom 3D-printed woodworking aid. Optimized for Elegoo Neptune 4 Pro (225x225x265mm build volume, 0.2mm layer height). Always use metric measurements.
---

# STL Generator for Woodworking Jigs

Generate parametric 3D printable jigs and fixtures for woodworking projects using CadQuery.

## Target Printer Specifications

- **Printer**: Elegoo Neptune 4 Pro
- **Build volume**: 225mm × 225mm × 265mm
- **Layer height**: 0.2mm standard
- **Units**: Metric (millimeters)

For complete specifications and design constraints, read `references/printer_specs.md`.

## Available Pre-Built Scripts

### 1. Circle Cutting Jig (`scripts/circle_cutting_jig.py`)

Creates router jigs for cutting perfect circles - ideal for lampshade rings and circular frames.

**Usage**:
```bash
python scripts/circle_cutting_jig.py <outer_diameter> <inner_diameter> [output.stl]
```

**Example**:
```bash
python scripts/circle_cutting_jig.py 300 250 lampshade_jig.stl
```

**Features**:
- Adjustable inner/outer diameters
- Built-in guide ring for router stability  
- Center pivot hole for compass-style cutting
- Radial slot for router bit clearance
- Alignment marks every 45°

### 2. Angle Wedge (`scripts/angle_wedge.py`)

Creates angle guide wedges for compound cuts and angled assembly work.

**Usage**:
```bash
python scripts/angle_wedge.py <angle_degrees> [output.stl]
```

**Example**:
```bash
python scripts/angle_wedge.py 15 wedge_15deg.stl
```

**Features**:
- Any angle from 1-60 degrees
- Raised reference edge on hypotenuse
- Embossed angle label
- Stable base for accurate positioning

### 3. Spacing Blocks (`scripts/spacing_block.py`)

Creates precision spacing blocks for consistent assembly gaps and setup.

**Usage**:
```bash
# Single block
python scripts/spacing_block.py <height_mm> [width_mm] [depth_mm] [output.stl]

# Set of multiple heights
python scripts/spacing_block.py set <h1>,<h2>,<h3> [output.stl]
```

**Examples**:
```bash
python scripts/spacing_block.py 10 50 30 spacer_10mm.stl
python scripts/spacing_block.py set 5,10,15,20 spacer_set.stl
```

**Features**:
- Embossed dimension labels
- Finger relief cutouts for easy pickup
- Orientation markers
- Can generate matched sets

## Creating Custom Jigs

For custom jig designs not covered by pre-built scripts, write Python code using CadQuery. Read `references/cadquery_patterns.md` for common patterns and best practices.

### Workflow for Custom Jigs

1. **Understand requirements**: Get dimensions, constraints, and functional needs
2. **Check printer limits**: Verify design fits within 225×225×265mm build volume
3. **Apply design constraints**: Use guidelines from `references/printer_specs.md`:
   - Minimum wall thickness: 2-3mm for structural parts
   - Hole clearances: +0.3-0.5mm for hardware
   - Minimum feature size: 1.0mm
   - Text depth: 0.4-0.6mm
4. **Write CadQuery code**: Use patterns from `references/cadquery_patterns.md`
5. **Export to STL**: Use `cq.exporters.export(part, "filename.stl")`
6. **Save to outputs**: Move STL file to `/mnt/user-data/outputs/` for user access

### Example: Custom Router Template

```python
import cadquery as cq

def create_router_template(length, width, inset, guide_height):
    """Create router template with guide bushings."""
    
    # Base plate
    base = (
        cq.Workplane("XY")
        .rect(length, width)
        .extrude(6)
    )
    
    # Cut out center area
    base = (
        base.faces(">Z")
        .workplane()
        .rect(length - 2 * inset, width - 2 * inset)
        .cutThruAll()
    )
    
    # Add guide walls
    walls = (
        cq.Workplane("XY")
        .workplane(offset=6)
        .rect(length, width)
        .rect(length - 2 * inset, width - 2 * inset)
        .extrude(guide_height)
    )
    
    result = base.union(walls)
    
    # Add mounting holes (corners)
    for x in [-length/2 + 15, length/2 - 15]:
        for y in [-width/2 + 15, width/2 - 15]:
            result = (
                result.faces(">Z")
                .workplane()
                .center(x, y)
                .circle(2.5)  # M5 clearance
                .cutThruAll()
            )
    
    return result

# Generate and export
template = create_router_template(200, 150, 30, 8)
cq.exporters.export(template, "router_template.stl")
```

## Common Jig Types and Approaches

### Lampshade Jigs
- **Circle cutting**: Use `circle_cutting_jig.py` for ring frames
- **Angle guides**: Use `angle_wedge.py` for tapered shade angles
- **Spacing**: Use `spacing_block.py` for consistent rib spacing

### Router Jigs
- **Edge guides**: Rectangular frame with adjustable fence
- **Template guides**: Match standard template bushing sizes (16mm OD common)
- **Bit clearance**: 7-8mm slots for 1/4" shanks, 13-14mm for 1/2"

### Assembly Jigs
- **Right angle corners**: 90° blocks with reference edges
- **Spacing sets**: Multiple blocks for consistent gaps
- **Alignment pins**: 6mm diameter pins, 10mm height standard

### Clamping Aids
- **Cauls**: Flat plates with finger reliefs
- **Pressure distributors**: Curved or stepped surfaces
- **Clamp blocks**: Sacrificial blocks with protective surfaces

## Design Best Practices

### Structural Integrity
- Use 3-4 perimeter walls for strength
- Add chamfers/fillets (1-2mm) to reduce stress concentrations  
- Orient layer lines perpendicular to primary load direction
- Minimum 5mm base thickness for flatness

### Printability
- Keep overhangs under 45° to avoid supports
- Add 0.2mm draft angle for parts that nest
- Avoid unsupported bridges over 30mm
- Orient largest flat surface on print bed

### Woodworking Functionality
- Smooth reference surfaces (no text or features on work contact areas)
- Add visual alignment marks (notches, text, contrasting surfaces)
- Include finger reliefs on small parts for easy handling
- Consider clamping access (25mm+ clearance)

### Hardware Integration
Common hole sizes (add 0.3-0.5mm clearance):
- M3: 3.3mm hole
- M4: 4.3mm hole  
- M5: 5.3mm hole
- #8 wood screw: 4.5mm hole
- 1/4"-20 bolt: 6.6mm hole

## File Organization

When generating STL files:

1. **Work in** `/home/claude/` during development
2. **Test scripts** by running them to verify output
3. **Copy final STLs** to `/mnt/user-data/outputs/` before presenting to user
4. **Name files descriptively**: Include key dimensions or purpose
   - Good: `lampshade_jig_300mm_OD.stl`
   - Good: `wedge_22.5_degrees.stl`
   - Poor: `jig1.stl`

## CadQuery Quick Reference

For detailed patterns and examples, read `references/cadquery_patterns.md`.

**Basic structure**:
```python
import cadquery as cq

# Create base
part = cq.Workplane("XY").box(50, 30, 10)

# Add features on top
part = (
    part.faces(">Z")
    .workplane()
    .circle(5)
    .cutThruAll()
)

# Export
cq.exporters.export(part, "output.stl")
```

**Essential methods**:
- `.box(w, d, h)` - rectangular solid
- `.circle(r)` - circle sketch
- `.rect(w, h)` - rectangle sketch  
- `.extrude(height)` - extrude 2D to 3D
- `.cutThruAll()` - cut through entire part
- `.fillet(radius)` - round edges
- `.chamfer(distance)` - bevel edges
- `.translate((x, y, z))` - move part
- `.rotate((cx,cy,cz), (ax,ay,az), angle)` - rotate around axis

## Troubleshooting

### "Module 'cadquery' not found"
```bash
pip install --break-system-packages cadquery
```

### STL appears hollow in slicer
- This is normal - slicers add infill during slicing
- The generated STL is a shell (surface model)

### Features too small to print
- Check minimum feature size: 1.0mm
- Increase wall thickness to at least 2-3mm
- Verify hole diameters are >= 2mm

### Part doesn't fit on print bed
- Check dimensions against 220×220mm effective area
- Consider splitting large jigs into sections
- Rotate part to minimize footprint

## When to Read Reference Files

- **Always read** `references/printer_specs.md` when starting a new jig design
- **Read** `references/cadquery_patterns.md` when writing custom CadQuery code
- **Refer to** examples in pattern files for complex geometries

## Output Format

After generating STL file(s), always:
1. Move final STLs to `/mnt/user-data/outputs/`
2. Provide download link: `[View your file](computer:///mnt/user-data/outputs/filename.stl)`
3. Include brief summary: dimensions, purpose, estimated print time
4. Suggest print settings if relevant (infill %, supports, orientation)
