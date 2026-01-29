---
name: image-stitch
description: Stitches multiple scrolling screenshots into a single image. Supports both vertical (default) and horizontal stitching with automatic overlap detection and alignment using ORB feature matching. Use when user wants to combine sequential screenshots from scrolling content.
---

# Image Stitch Skill

Stitch multiple scrolling screenshots into one seamless image.

## Step 1: Ask Stitch Direction

Use the Question tool to ask user ONE question only:

**Question**: Select stitch direction
**Options** (exactly 2):
1. `Vertical (top to bottom)` - (Recommended) For vertically scrolling screenshots
2. `Horizontal (left to right)` - For horizontally scrolling screenshots

## Step 2: Ask Overlap Size

Use the Question tool to ask user ONE question only:

**Question**: How much overlap between screenshots?
**Options** (exactly 3):
1. `Small overlap` - Screenshots have minimal overlap (~10-20%)
2. `Medium overlap` - (Recommended) Screenshots have moderate overlap (~20-40%)
3. `Large overlap` - Screenshots have significant overlap (~40%+)

Based on user choice, set the edge parameter for modifying stitch.py:
- Small: `EDGE_PARAM=150`
- Medium: `EDGE_PARAM=300`
- Large: `EDGE_PARAM=600`

## Step 3: Setup Environment

**CRITICAL**: Must run this BEFORE any stitching. The skill directory contains a venv that needs activation.

```bash
# Get skill directory (where stitch.py lives)
SKILL_DIR="/path/to/image-stitch"  # Replace with actual skill path

# Activate venv and install dependencies (idempotent)
cd "$SKILL_DIR" && \
python3 -m venv venv 2>/dev/null || true && \
source venv/bin/activate && \
pip install -q opencv-python numpy

# Modify stitch.py edge parameters based on user's overlap choice
EDGE_PARAM=300  # Set this based on Step 2 user choice
sd "edge_h = min\([0-9]+, h1 // 4, h2 // 4\)" "edge_h = min($EDGE_PARAM, h1 // 4, h2 // 4)" stitch.py
sd "edge_w = min\([0-9]+, w1 // 4, w2 // 4\)" "edge_w = min($EDGE_PARAM, w1 // 4, w2 // 4)" stitch.py
```

## Step 4: Prepare Task Folders

Create task folders with timestamp:

```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
mkdir -p "$SKILL_DIR/input/$TIMESTAMP"
mkdir -p "$SKILL_DIR/output/$TIMESTAMP"
```

## Step 5: Copy and Rename Images

Copy images from source to `input/$TIMESTAMP/`, renaming by sequence order.

**IMPORTANT**: Use `find` command to handle paths with spaces and special characters correctly.

```bash
SOURCE_PATH="/path/to/source"  # User provided path

# Find and copy images, sorted by filename, renamed to 01.png, 02.png, etc.
find "$SOURCE_PATH" -maxdepth 1 -type f \( -iname "*.png" -o -iname "*.jpg" -o -iname "*.jpeg" \) | \
sort | \
nl -nrz -w2 | \
while read num file; do
    cp "$file" "$SKILL_DIR/input/$TIMESTAMP/${num}.png"
done
```

Verify copied files:
```bash
ls -la "$SKILL_DIR/input/$TIMESTAMP/"
```

## Step 6: Execute Stitching

**IMPORTANT**: Must run with venv activated.

```bash
cd "$SKILL_DIR" && source venv/bin/activate && \
python stitch.py \
    -i "input/$TIMESTAMP" \
    -o "output/$TIMESTAMP/stitched.png" \
    --debug \
    [--horizontal]  # Add this flag if user chose horizontal
```

## Step 7: Report Result

After stitching, report to user with **full absolute path**:

```
Stitching complete!

Task ID: $TIMESTAMP
Input: $SKILL_DIR/input/$TIMESTAMP/ (<N> images)
Output: $SKILL_DIR/output/$TIMESTAMP/stitched.png (<W>x<H>)

Full output path:
$SKILL_DIR/output/$TIMESTAMP/stitched.png
```

## Step 8: Ask to Open Output Folder

Use the Question tool to ask user ONE question only:

**Question**: Open output folder in Finder?
**Options** (exactly 2):
1. `Yes` - Open the output folder
2. `No` - Skip opening folder

If user chooses "Yes", run:
```bash
open "$SKILL_DIR/output/$TIMESTAMP"
```

## Script Options

| Option | Description |
|--------|-------------|
| `-i, --input` | Input folder (images sorted by filename) |
| `-o, --output` | Output path (default: `output/stitched.png`) |
| `-H, --horizontal` | Horizontal stitching mode |
| `--no-detect` | Disable overlap detection (direct concatenation) |
| `--debug` | Show detailed matching info |

## Troubleshooting

### ModuleNotFoundError: No module named 'cv2'
**Cause**: venv not activated or dependencies not installed.
**Fix**: Run Step 3 (Setup Environment) again.

### File copy fails with "No such file or directory"
**Cause**: Paths with spaces or special characters not quoted properly.
**Fix**: Always use `find` with proper quoting as shown in Step 5.

### No matches found: *.{png,jpg}
**Cause**: Brace expansion `{a,b}` not supported in all shells.
**Fix**: Use `find` with `-iname` instead of glob patterns.

## How It Works

1. **Feature Detection**: Uses ORB to find keypoints in overlap regions
2. **Matching**: Finds corresponding points between consecutive images
3. **Offset Calculation**: 
   - Primary axis: overlap amount (how much images share)
   - Secondary axis: alignment shift (corrects misalignment)
4. **Stitching**: Places images on canvas with calculated offsets
5. **Cropping**: Trims to common region

## Requirements

- Python 3.10+
- opencv-python
- numpy

Dependencies are auto-installed in venv during Step 2.

## Limitations

- Maximum 10 images per stitch
- Images should have 20%+ overlap for reliable matching
- Works best with content-rich areas (not pure solid colors)
