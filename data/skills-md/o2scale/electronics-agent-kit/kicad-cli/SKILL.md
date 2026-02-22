---
name: kicad-cli
description: KiCad command-line interface expertise. Complete reference for schematic/PCB exports, DRC/ERC validation, manufacturing outputs, and automation.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# KiCad CLI Reference

> Complete command reference for kicad-cli (KiCad 8.x)

---

## 1. Command Structure

```bash
kicad-cli <application> <command> [options] <input-file>
```

Applications:
- `sch` - Schematic operations
- `pcb` - PCB operations
- `fp` - Footprint operations
- `sym` - Symbol operations

---

## 2. Schematic Commands

### Export Netlist

```bash
kicad-cli sch export netlist \
  --output project.net \
  project.kicad_sch
```

### Export BOM

```bash
# Basic BOM
kicad-cli sch export bom \
  --output bom.csv \
  project.kicad_sch

# With specific fields
kicad-cli sch export bom \
  --output bom.csv \
  --fields "Reference,Value,Footprint,LCSC,MPN" \
  --group-by "Value,Footprint" \
  --sort-asc \
  project.kicad_sch
```

### Export PDF

```bash
kicad-cli sch export pdf \
  --output schematic.pdf \
  --black-and-white \
  project.kicad_sch
```

### Export SVG

```bash
kicad-cli sch export svg \
  --output ./svg/ \
  --black-and-white \
  project.kicad_sch
```

### Run ERC (Electrical Rules Check)

```bash
kicad-cli sch erc \
  --output erc-report.rpt \
  --severity-all \
  --exit-code-violations \
  project.kicad_sch
```

Options:
- `--severity-all` - Report all severities
- `--severity-error` - Only errors
- `--exit-code-violations` - Return non-zero on violations

---

## 3. PCB Commands

### Run DRC (Design Rules Check)

```bash
kicad-cli pcb drc \
  --output drc-report.rpt \
  --severity-all \
  --exit-code-violations \
  project.kicad_pcb
```

### Export Gerbers

```bash
kicad-cli pcb export gerbers \
  --output ./gerbers/ \
  --layers "F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts" \
  --subtract-soldermask \
  project.kicad_pcb
```

Common layers:
- `F.Cu`, `B.Cu` - Copper layers
- `In1.Cu`, `In2.Cu` - Inner copper layers
- `F.SilkS`, `B.SilkS` - Silkscreen
- `F.Mask`, `B.Mask` - Solder mask
- `F.Paste`, `B.Paste` - Solder paste
- `Edge.Cuts` - Board outline
- `F.Fab`, `B.Fab` - Fabrication layers

### Export Drill Files

```bash
kicad-cli pcb export drill \
  --output ./gerbers/ \
  --format excellon \
  --excellon-units mm \
  --generate-map \
  --map-format pdf \
  project.kicad_pcb
```

Options:
- `--format excellon` - Standard drill format
- `--excellon-units mm` or `in`
- `--excellon-zeros-format decimal`
- `--generate-map` - Create drill map
- `--map-format gerberx2|ps|pdf|svg|dxf`

### Export Position/Pick-and-Place

```bash
kicad-cli pcb export pos \
  --output positions.csv \
  --format csv \
  --units mm \
  --side front \
  --exclude-dnp \
  project.kicad_pcb
```

Options:
- `--format csv|ascii`
- `--units mm|in`
- `--side front|back|both`
- `--exclude-dnp` - Exclude Do Not Populate

### Export 3D Models

```bash
# STEP format (for mechanical CAD)
kicad-cli pcb export step \
  --output project.step \
  --subst-models \
  project.kicad_pcb

# VRML format
kicad-cli pcb export vrml \
  --output project.wrl \
  project.kicad_pcb
```

### Export PDF

```bash
kicad-cli pcb export pdf \
  --output pcb.pdf \
  --layers "F.Cu,B.Cu,Edge.Cuts" \
  --black-and-white \
  project.kicad_pcb
```

### Export SVG

```bash
kicad-cli pcb export svg \
  --output pcb.svg \
  --layers "F.Cu,Edge.Cuts" \
  --black-and-white \
  project.kicad_pcb
```

### Export DXF

```bash
kicad-cli pcb export dxf \
  --output pcb.dxf \
  --layers "Edge.Cuts" \
  project.kicad_pcb
```

---

## 4. Footprint Commands

### Export SVG

```bash
kicad-cli fp export svg \
  --output footprint.svg \
  footprint.kicad_mod
```

### Upgrade Footprint Library

```bash
kicad-cli fp upgrade \
  --output ./upgraded/ \
  ./library.pretty/
```

---

## 5. Symbol Commands

### Export SVG

```bash
kicad-cli sym export svg \
  --output ./symbols/ \
  library.kicad_sym
```

### Upgrade Symbol Library

```bash
kicad-cli sym upgrade \
  --output upgraded.kicad_sym \
  legacy.lib
```

---

## 6. Common Options

| Option | Description |
|--------|-------------|
| `--help` | Show command help |
| `--output`, `-o` | Output file/directory |
| `--define-var` | Define text variable |
| `--force`, `-f` | Overwrite existing files |

---

## 7. Automation Examples

### CI/CD Build Script

```bash
#!/bin/bash
set -euo pipefail

PROJECT="myproject"

# Run ERC
echo "Running ERC..."
kicad-cli sch erc \
  --output reports/erc.rpt \
  --exit-code-violations \
  ${PROJECT}.kicad_sch

# Run DRC  
echo "Running DRC..."
kicad-cli pcb drc \
  --output reports/drc.rpt \
  --exit-code-violations \
  ${PROJECT}.kicad_pcb

# Generate manufacturing files
echo "Generating manufacturing files..."
mkdir -p output/gerbers

kicad-cli pcb export gerbers \
  --output output/gerbers/ \
  --layers "F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts" \
  ${PROJECT}.kicad_pcb

kicad-cli pcb export drill \
  --output output/gerbers/ \
  --format excellon \
  ${PROJECT}.kicad_pcb

# Generate BOM
kicad-cli sch export bom \
  --output output/bom.csv \
  --fields "Reference,Value,Footprint,LCSC,MPN" \
  ${PROJECT}.kicad_sch

# Generate position file
kicad-cli pcb export pos \
  --output output/positions.csv \
  --format csv \
  --units mm \
  ${PROJECT}.kicad_pcb

echo "Done!"
```

### JLCPCB Preparation

```bash
#!/bin/bash
PROJECT="$1"
OUTPUT="./jlcpcb"
mkdir -p "$OUTPUT"

# Gerbers (zip for upload)
kicad-cli pcb export gerbers \
  --output "$OUTPUT/" \
  --layers "F.Cu,B.Cu,F.SilkS,B.SilkS,F.Mask,B.Mask,Edge.Cuts" \
  "${PROJECT}.kicad_pcb"

kicad-cli pcb export drill \
  --output "$OUTPUT/" \
  --format excellon \
  --excellon-units mm \
  "${PROJECT}.kicad_pcb"

cd "$OUTPUT" && zip -r gerbers.zip *.g* *.drl && cd -

# BOM for assembly
kicad-cli sch export bom \
  --output "$OUTPUT/bom.csv" \
  --fields "Comment,Designator,Footprint,LCSC" \
  "${PROJECT}.kicad_sch"

# CPL (Component Placement List)
kicad-cli pcb export pos \
  --output "$OUTPUT/cpl.csv" \
  --format csv \
  --units mm \
  --side front \
  "${PROJECT}.kicad_pcb"
```

---

## 8. Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | DRC/ERC violations found (with --exit-code-violations) |

---

## 9. Important Notes

### What kicad-cli CAN Do
- Export files (Gerber, PDF, SVG, netlist, BOM, 3D)
- Run validation (DRC, ERC)
- Upgrade library formats
- Automation and CI/CD

### What kicad-cli CANNOT Do
- Modify designs (add components, routes)
- Edit schematic/PCB content
- Interactive operations

For design modifications, use:
- File manipulation (S-expression format)
- KiCad Python scripting console
- KiCad IPC API (experimental)

---

> **Version:** This reference is for KiCad 8.x. Commands may differ in older versions.
