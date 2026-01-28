---
name: svg-icon-maker
description: Generate production-quality SVG icons with COLOR support using VTracer vectorization. Converts raster images to clean, colorful SVG paths.
---

# SVG Icon Maker

Convert raster images to **colorful SVG** using `@neplex/vectorizer`.

## Output Directory

All files saved to workspace with timestamped folders (format: `YYYY-MM-DDTHH-mm-ss-SSSZ`):
```
<workspace>/svg-output/
└── <timestamp>/              # e.g., 2026-01-27T02-13-38-811Z
    ├── reference.png         # Generated reference image
    ├── icon.svg              # Color SVG output
    └── icon_preview.png      # Preview for comparison
```

## Prerequisites

```bash
cd <workspace>
npm init -y
npm install @neplex/vectorizer sharp
```

## Workflow

### Step 1: Generate Reference Image

Use `generate_image` tool, save to `svg-output` root first (or directly to output folder if managed manually):
```bash
# Generate image, then move to proper folder later or keep in root for processing
```

**Prompt template:**
```
"[subject] avatar, high fidelity vector illustration, clear line style, 
black closed outlines, flat uniform colors, no gradients, 
white background, distinct separation between colors"
```

### Step 2: Convert to Color SVG

Run the conversion script directly from skill resources (no copying needed):

```bash
node .agent/skills/svg-icon-maker/script/convert-template.js <input-file> [output-dir]
```

**Example:**
```bash
# Using default output directory (./svg-output)
node .agent/skills/svg-icon-maker/script/convert-template.js ./my-image.png

# Specifying custom output directory
node .agent/skills/svg-icon-maker/script/convert-template.js ./my-image.png ./custom-output
```

**Key Features:**
- **4-Corner Flood Fill**: Removes background starting from all corners to handle split backgrounds.
- **Inner Detail Protection**: Preserves white/light details inside the subject (e.g., eyes).
- **Auto-Threshold**: Adapts to the specific background color found at the corners.
- **Timestamped Output**: Automatically creates folders with format `YYYY-MM-DDTHH-mm-ss-SSSZ`.

### Step 3: Verify & Compare

```bash
ls -la <workspace>/svg-output/
```

Use `view_file` to compare `reference.png` with `icon_preview.png`.

## Parameters

**Default settings optimized for HIGH color fidelity** - preserves original colors, only removes background.

| Parameter | Default | Description |
|-----------|---------|-------------|
| `colorMode` | Color | `ColorMode.Color` or `Binary` |
| `colorPrecision` | 8 | 1-8, higher = more colors (8 = max fidelity) |
| `layerDifference` | 8 | Color layer threshold (lower = less merging) |
| `filterSpeckle` | 4 | Remove noise pixels (lower = more detail) |
| `mode` | Spline | `PathSimplifyMode.Spline` or `Polygon` |
| `cornerThreshold` | 60 | Corner detection angle |
| `spliceThreshold` | 45 | Spline angle threshold |
