---
name: kicad-file-format
description: KiCad S-expression file format expertise. Complete reference for reading and writing .kicad_sch (schematic) and .kicad_pcb (PCB) files.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# KiCad File Format Reference

> Complete reference for KiCad 8.x S-expression file formats.

KiCad uses Lisp-style S-expressions for all file formats. Files are human-readable and text-based.

---

## 1. S-Expression Basics

### Syntax

```lisp
(keyword value)
(keyword (nested value))
(keyword
  (child1 value)
  (child2 value)
)
```

### Common Patterns

- Coordinates: `(at x y angle)` or `(xy x y)`
- UUIDs: `(uuid "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx")`
- Strings: `"quoted string"` or `unquoted_identifier`
- Numbers: `1.234` (always decimal, no units in file)
- Booleans: `yes` / `no`

---

## 2. Schematic Format (.kicad_sch)

### File Structure

```lisp
(kicad_sch
  (version 20231120)
  (generator "eeschema")
  (generator_version "8.0")
  (uuid "project-uuid")
  (paper "A4")
  
  ; Title block
  (title_block
    (title "Project Title")
    (date "2024-01-01")
    (rev "1.0")
    (company "Company Name")
  )
  
  ; Library symbols (embedded copies)
  (lib_symbols
    (symbol "Device:R" ...)
  )
  
  ; Placed symbols (component instances)
  (symbol ...)
  (symbol ...)
  
  ; Wires and connections
  (wire ...)
  (bus ...)
  (junction ...)
  
  ; Labels and nets
  (label ...)
  (global_label ...)
  (hierarchical_label ...)
  
  ; Hierarchical sheets
  (sheet ...)
  
  ; Text and graphics
  (text ...)
  (polyline ...)
  (rectangle ...)
)
```

### Symbol Instance

```lisp
(symbol
  (lib_id "Device:R")
  (at 100 50 0)              ; x, y, rotation (0, 90, 180, 270)
  (unit 1)                   ; Multi-unit symbols
  (exclude_from_sim no)
  (in_bom yes)
  (on_board yes)
  (dnp no)                   ; Do Not Populate
  (uuid "symbol-uuid")
  (property "Reference" "R1"
    (at 100 45 0)
    (effects (font (size 1.27 1.27)))
  )
  (property "Value" "10k"
    (at 100 55 0)
    (effects (font (size 1.27 1.27)))
  )
  (property "Footprint" "Resistor_SMD:R_0402_1005Metric"
    (at 100 50 0)
    (effects (font (size 1.27 1.27)) hide)
  )
  (property "LCSC" "C25744"
    (at 100 50 0)
    (effects (font (size 1.27 1.27)) hide)
  )
  (pin "1" (uuid "pin1-uuid"))
  (pin "2" (uuid "pin2-uuid"))
  (instances
    (project "project_name"
      (path "/root-uuid" (reference "R1") (unit 1))
    )
  )
)
```

### Wire

```lisp
(wire
  (pts
    (xy 100 50)
    (xy 120 50)
  )
  (stroke (width 0) (type default))
  (uuid "wire-uuid")
)
```

### Label (Local Net Name)

```lisp
(label "VCC"
  (at 100 50 0)
  (effects (font (size 1.27 1.27)))
  (uuid "label-uuid")
)
```

### Global Label (Cross-Sheet Net)

```lisp
(global_label "USB_D+"
  (shape input)              ; input, output, bidirectional, tri_state, passive
  (at 150 60 0)
  (effects (font (size 1.27 1.27)))
  (uuid "global-uuid")
  (property "Intersheetrefs" "${INTERSHEET_REFS}"
    (at 150 60 0)
    (effects (font (size 1.27 1.27)) hide)
  )
)
```

### Power Symbol

```lisp
(symbol
  (lib_id "power:GND")
  (at 100 80 0)
  (unit 1)
  (exclude_from_sim yes)
  (in_bom no)
  (on_board yes)
  (uuid "power-uuid")
  (property "Reference" "#PWR01" ...)
  (property "Value" "GND" ...)
  (pin "1" (uuid "..."))
)
```

### Hierarchical Sheet

```lisp
(sheet
  (at 50 50)
  (size 30 20)
  (fields_autoplaced yes)
  (stroke (width 0.1524) (type solid))
  (fill (color 255 255 255 0))
  (uuid "sheet-uuid")
  (property "Sheetname" "Power Supply"
    (at 50 49 0)
    (effects (font (size 1.27 1.27)))
  )
  (property "Sheetfile" "power_supply.kicad_sch"
    (at 50 72 0)
    (effects (font (size 1.27 1.27)) hide)
  )
  (pin "VIN" input
    (at 50 55 180)
    (effects (font (size 1.27 1.27)))
    (uuid "sheet-pin-uuid")
  )
)
```

---

## 3. PCB Format (.kicad_pcb)

### File Structure

```lisp
(kicad_pcb
  (version 20231014)
  (generator "pcbnew")
  (generator_version "8.0")
  (general
    (thickness 1.6)
    (legacy_teardrops no)
  )
  
  ; Page settings
  (paper "A4")
  (title_block ...)
  
  ; Layer definitions
  (layers
    (0 "F.Cu" signal)
    (31 "B.Cu" signal)
    (32 "B.Adhes" user "B.Adhesive")
    (33 "F.Adhes" user "F.Adhesive")
    (34 "B.Paste" user)
    (35 "F.Paste" user)
    (36 "B.SilkS" user "B.Silkscreen")
    (37 "F.SilkS" user "F.Silkscreen")
    (38 "B.Mask" user)
    (39 "F.Mask" user)
    (40 "Dwgs.User" user "User.Drawings")
    (41 "Cmts.User" user "User.Comments")
    (42 "Eco1.User" user "User.Eco1")
    (43 "Eco2.User" user "User.Eco2")
    (44 "Edge.Cuts" user)
    (45 "Margin" user)
    (46 "B.CrtYd" user "B.Courtyard")
    (47 "F.CrtYd" user "F.Courtyard")
    (48 "B.Fab" user)
    (49 "F.Fab" user)
  )
  
  ; Design rules setup
  (setup ...)
  
  ; Net definitions
  (net 0 "")
  (net 1 "GND")
  (net 2 "VCC")
  
  ; Footprints (component instances)
  (footprint ...)
  
  ; Traces
  (segment ...)
  
  ; Vias
  (via ...)
  
  ; Zones (copper pours)
  (zone ...)
  
  ; Graphics
  (gr_line ...)
  (gr_rect ...)
  (gr_circle ...)
  (gr_text ...)
)
```

### Footprint

```lisp
(footprint "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
  (layer "F.Cu")
  (uuid "footprint-uuid")
  (at 100 50 0)              ; x, y, rotation
  (descr "SOIC-8 package")
  (property "Reference" "U1"
    (at 0 -3.5 0)
    (layer "F.SilkS")
    (uuid "ref-uuid")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (property "Value" "ESP32-S3"
    (at 0 3.5 0)
    (layer "F.Fab")
    (uuid "val-uuid")
    (effects (font (size 1 1) (thickness 0.15)))
  )
  (property "Footprint" "Package_SO:SOIC-8..."
    (at 0 0 0)
    (layer "F.Fab")
    (hide yes)
    (uuid "fp-uuid")
  )
  
  ; Pads
  (pad "1" smd rect
    (at -1.905 -2.475)
    (size 0.6 1.5)
    (layers "F.Cu" "F.Paste" "F.Mask")
    (net 1 "GND")
    (uuid "pad-uuid")
  )
  (pad "2" thru_hole circle
    (at 0 0)
    (size 1.7 1.7)
    (drill 1.0)
    (layers "*.Cu" "*.Mask")
    (net 2 "VCC")
    (uuid "pad-uuid")
  )
  
  ; Silkscreen graphics
  (fp_line
    (start -2.5 -2.5)
    (end 2.5 -2.5)
    (stroke (width 0.12) (type solid))
    (layer "F.SilkS")
    (uuid "line-uuid")
  )
)
```

### Trace (Segment)

```lisp
(segment
  (start 100 50)
  (end 120 50)
  (width 0.25)
  (layer "F.Cu")
  (net 1)
  (uuid "segment-uuid")
)
```

### Arc Trace

```lisp
(arc
  (start 100 50)
  (mid 105 45)
  (end 110 50)
  (width 0.25)
  (layer "F.Cu")
  (net 1)
  (uuid "arc-uuid")
)
```

### Via

```lisp
(via
  (at 110 60)
  (size 0.8)
  (drill 0.4)
  (layers "F.Cu" "B.Cu")
  (net 1)
  (uuid "via-uuid")
)
```

### Zone (Copper Pour)

```lisp
(zone
  (net 1)
  (net_name "GND")
  (layer "F.Cu")
  (uuid "zone-uuid")
  (hatch edge 0.5)
  (connect_pads
    (clearance 0.25)
  )
  (min_thickness 0.25)
  (filled_areas_thickness no)
  (fill yes
    (thermal_gap 0.5)
    (thermal_bridge_width 0.5)
  )
  (polygon
    (pts
      (xy 0 0)
      (xy 100 0)
      (xy 100 100)
      (xy 0 100)
    )
  )
  (filled_polygon
    (layer "F.Cu")
    (pts ...)
  )
)
```

### Board Outline

```lisp
(gr_rect
  (start 0 0)
  (end 100 100)
  (stroke (width 0.1) (type default))
  (fill none)
  (layer "Edge.Cuts")
  (uuid "outline-uuid")
)
```

---

## 4. Common Operations

### Adding a Component to Schematic

1. Add symbol to `(lib_symbols ...)` if not already present
2. Add `(symbol ...)` block with:
   - Unique UUID
   - Position `(at x y rotation)`
   - Reference property
   - Value property
   - Footprint property
   - Pin mappings

### Adding a Trace to PCB

1. Find the net number for the connection
2. Add `(segment ...)` block with:
   - Start and end coordinates
   - Width
   - Layer
   - Net number
   - Unique UUID

### Creating a Net

1. In PCB file, add: `(net N "NetName")`
2. Reference the net number in pads and segments

---

## 5. Units and Coordinates

| Context | Unit |
|---------|------|
| Schematic | mils (1/1000 inch), stored as mm in file |
| PCB | millimeters |
| Angles | degrees (0, 90, 180, 270 typical) |

Coordinates are absolute from origin (0,0).

---

## 6. UUID Generation

All elements require unique UUIDs. Format: `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

Generate with: `uuidgen` command or programming language UUID library.

---

## 7. Parsing Tips

### Reading S-Expressions

```python
# Simple recursive descent parser concept
def parse_sexpr(text):
    tokens = tokenize(text)
    return parse_list(tokens)

def parse_list(tokens):
    result = []
    while tokens and tokens[0] != ')':
        if tokens[0] == '(':
            tokens.pop(0)
            result.append(parse_list(tokens))
        else:
            result.append(tokens.pop(0))
    if tokens:
        tokens.pop(0)  # Remove closing ')'
    return result
```

### Writing S-Expressions

- Maintain consistent indentation (2 spaces)
- Preserve existing UUIDs when editing
- Keep order of elements as expected by KiCad
- Use proper quoting for strings with spaces

---

## 8. File Validation

After editing:
1. Open in KiCad to verify parsing
2. Run ERC/DRC via kicad-cli
3. Check for warnings about unknown tokens

---

> **Important:** Always backup files before programmatic editing. KiCad may add/remove fields on save.
