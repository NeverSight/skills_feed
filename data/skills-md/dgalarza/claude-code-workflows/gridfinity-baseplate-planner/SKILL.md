---
name: gridfinity-baseplate-planner
description: Use this skill when planning and designing gridfinity baseplates for 3D printing. This includes calculating optimal grid sizes from given measurements, determining how to slice large grids into printable chunks based on printer bed dimensions, and calculating padding requirements for non-exact fits. The skill handles both metric and imperial measurements and provides guidance for using gridfinity.perplexinglabs.com to generate the actual STL files.
---

# Gridfinity Baseplate Planner

## Overview

This skill provides comprehensive guidance for planning gridfinity baseplates optimized for 3D printing. It handles the complete workflow from raw measurements to printable configurations, including unit conversion, grid optimization, multi-part slicing strategies, and padding calculations.

## Core Workflow

Follow these steps when planning a gridfinity baseplate:

### Step 1: Gather Information

Collect the following from the user:
- **Target dimensions**: The space to fill with gridfinity (drawer, shelf, etc.)
- **Printer bed size**: The maximum printable area
- **Grid size**: Default to 42mm if not specified (this is the gridfinity standard)
- **Padding preference**: Centered padding vs edge-specific padding

### Step 2: Convert Measurements

Convert all dimensions to millimeters for calculation:

| From | Conversion |
|------|------------|
| cm | × 10 |
| m | × 1000 |
| inches | × 25.4 |
| feet | × 304.8 |

### Step 3: Calculate Grid Configuration

**Formula for grid units:**
```
grid_units = floor(dimension_mm / grid_size_mm)
```

**Calculate totals:**
- Total grid dimensions: `grid_units × grid_size_mm`
- Padding: `target_dimension - total_grid_dimension`

**Example calculation:**
```
Target: 350mm width
Grid size: 42mm
Grid units: floor(350 / 42) = 8 units
Actual width: 8 × 42 = 336mm
Padding: 350 - 336 = 14mm (7mm per side if centered)
```

### Step 4: Plan Print Segments (if needed)

When the total grid exceeds printer bed dimensions:

1. **Calculate optimal segment sizes** that maximize grid units per print
2. **Determine number of segments** needed in each dimension
3. **Plan padding distribution**:
   - **Edge pieces**: padding on outer edges only
   - **Middle pieces**: no padding (exact grid dimensions)
   - **Corner pieces**: padding on two adjacent outer edges

**Segment calculation:**
```
max_units_per_print = floor(bed_dimension / grid_size)
segments_needed = ceiling(total_units / max_units_per_print)
```

### Step 5: Generate Output

Provide a structured plan in this format:

```
GRIDFINITY BASEPLATE PLAN
========================
Target Space: [dimensions]
Grid Size: [X]mm
Total Grid: [X] × [Y] units
Actual Dimensions: [X]mm × [Y]mm
Padding: [X]mm left/right, [Y]mm top/bottom

[If single print]
PRINT CONFIGURATION:
- Single piece: [dimensions]
- gridfinity.perplexinglabs.com settings:
  * Base Length: [X]mm
  * Base Width: [Y]mm
  * Padding: Auto-distribute

[If multiple prints]
PRINT SEGMENTS:
Segment 1 (Top-Left):
- Grid: [X] × [Y] units
- Dimensions: [X]mm × [Y]mm
- Padding: [X]mm left edge, [Y]mm top edge
- gridfinity.perplexinglabs.com settings:
  * Base Length: [X]mm
  * Base Width: [Y]mm
  * Force padding: Left and Top
[Continue for each segment...]
```

## Important Considerations

### Grid Unit Rules
- Always round DOWN grid units (partial units aren't valid)
- The standard gridfinity grid is 42mm × 42mm
- Custom grid sizes are supported but may limit compatibility with standard bins

### Padding Guidelines
- If padding exceeds 10mm on any side, suggest whether adding an additional grid unit might be better
- For multi-part prints, padding should only appear on outer edges
- Consider user preference: centered vs edge-specific padding

### Print Optimization
- When slicing, prefer equal-sized segments when possible
- For multi-part prints, consider adding alignment features or noting overlap requirements
- Account for typical 3D printer tolerances (0.2-0.4mm) when planning tight-fitting installations

### Multi-Part Assembly
- Number segments clearly (e.g., "Top-Left", "Top-Right", "Bottom-Left", "Bottom-Right")
- Provide assembly order recommendations
- Note any special considerations for joining pieces

## gridfinity.perplexinglabs.com Parameters

When generating parameters for the online tool:

| Parameter | Description |
|-----------|-------------|
| Base Length | Total X dimension in mm (including padding) |
| Base Width | Total Y dimension in mm (including padding) |
| Padding | How to distribute extra space |

For multi-part prints, each segment needs its own configuration with specific padding instructions.

## Example Scenarios

### Scenario 1: Simple Single Print

**Input:**
- Drawer: 180mm × 120mm
- Printer bed: 220mm × 220mm

**Output:**
```
GRIDFINITY BASEPLATE PLAN
========================
Target Space: 180mm × 120mm
Grid Size: 42mm
Total Grid: 4 × 2 units
Actual Dimensions: 168mm × 84mm
Padding: 6mm left/right, 18mm top/bottom

PRINT CONFIGURATION:
- Single piece: 180mm × 120mm
- gridfinity.perplexinglabs.com settings:
  * Base Length: 180mm
  * Base Width: 120mm
  * Padding: Auto-distribute
```

### Scenario 2: Multi-Part Print

**Input:**
- Drawer: 350mm × 250mm
- Printer bed: 220mm × 220mm

**Output:**
```
GRIDFINITY BASEPLATE PLAN
========================
Target Space: 350mm × 250mm
Grid Size: 42mm
Total Grid: 8 × 5 units
Actual Dimensions: 336mm × 210mm
Padding: 7mm left/right, 20mm top/bottom

PRINT SEGMENTS:
Segment 1 (Left):
- Grid: 4 × 5 units
- Dimensions: 175mm × 250mm (168mm grid + 7mm left padding)
- gridfinity.perplexinglabs.com settings:
  * Base Length: 175mm
  * Base Width: 250mm
  * Force padding: Left edge only, Top and Bottom edges

Segment 2 (Right):
- Grid: 4 × 5 units
- Dimensions: 175mm × 250mm (168mm grid + 7mm right padding)
- gridfinity.perplexinglabs.com settings:
  * Base Length: 175mm
  * Base Width: 250mm
  * Force padding: Right edge only, Top and Bottom edges

Assembly: Place Segment 1 on left, Segment 2 on right. Grids should align perfectly.
```

## Validation Checklist

Before finalizing a plan, verify:
- [ ] All measurements converted to millimeters correctly
- [ ] Grid units rounded DOWN (never up)
- [ ] Total grid dimensions + padding = target dimensions
- [ ] Each print segment fits within printer bed
- [ ] Padding only appears on outer edges for multi-part prints
- [ ] gridfinity.perplexinglabs.com parameters are accurate
