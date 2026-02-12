---
name: watermark-removal
description: "Universal watermark removal with ML-based inpainting and automatic detection. Works on ANY watermark type (Google SynthID, Midjourney, DALL-E, stock photos, logos). Four methods: inpaint (ML, best quality), aggressive (fast), crop (fastest), paint (basic). Auto-detects watermark location in any corner. Use when: (1) Removing ANY type of watermark, (2) Google AI/Imagen/Gemini watermarks, (3) Stock photo watermarks, (4) Logo overlays, (5) Cleaning images for production, (6) Batch processing, or (7) User mentions 'watermark', 'remove watermark', 'clean image', 'SynthID'"
---

# Universal Watermark Removal

Remove watermarks from ANY image source using intelligent detection and proven methods. **Smart routing: automatically detects Google SynthID and uses the proven aggressive method, falls back to ML inpainting for unknown watermark types.**

## Quick Start

### Single Image - Smart Auto-Detection (Recommended)

```bash
# Smart detection: Google SynthID → aggressive method (proven), Unknown → inpaint (ML)
python .claude/skills/watermark-removal/scripts/remove-watermark.py \
  input.png \
  output.png
```

### Single Image - Preserve Dimensions (Force ML)

```bash
# Force ML inpainting even for Google SynthID (preserves exact dimensions)
python .claude/skills/watermark-removal/scripts/remove-watermark.py \
  input.png \
  output.png \
  --method inpaint
```

### Batch Processing (Get User Approval First!)

**⚠️ IMPORTANT:** Always ask user before batch processing, especially with crop/aggressive methods that alter dimensions.

```bash
# Recommended: Preserves dimensions
python .claude/skills/watermark-removal/scripts/batch-process.py \
  /path/to/input-dir \
  /path/to/output-dir \
  --method inpaint

# Alternative: Fast but crops 120px (requires user approval)
python .claude/skills/watermark-removal/scripts/batch-process.py \
  /path/to/input-dir \
  /path/to/output-dir \
  --method aggressive
```

## Smart Detection System ⭐ NEW

The skill automatically detects Google SynthID watermarks and routes to the optimal removal method:

### Google SynthID Detection

**Characteristics analyzed:**
- RGBA mode (PNG format with alpha channel)
- Large dimensions (>1500px width and height)
- Typical Google AI aspect ratios (1.83, 1.0, 1.5, 1.78 with 10% tolerance)
- Automatic corner detection for watermark location

**Smart routing logic:**
1. **If Google SynthID detected** → Uses `aggressive` method (proven to work perfectly)
   - Crops 120px from detected corner
   - Removes alpha channel watermarking
   - Paints over any remnants
   - Works 100% reliably on Google AI images

2. **If unknown/other watermark** → Uses `inpaint` method (ML-based)
   - Preserves exact dimensions
   - Uses OpenCV Navier-Stokes algorithm
   - Works on any watermark type

### Override Default Behavior

```bash
# Force ML inpainting even for Google SynthID (preserves dimensions)
python scripts/remove-watermark.py input.png output.png --method inpaint

# Force aggressive method for non-Google watermarks
python scripts/remove-watermark.py input.png output.png --method aggressive

# Disable auto-detection (assume bottom-right corner)
python scripts/remove-watermark.py input.png output.png --no-detect
```

## Methods

### Inpaint Method (Best Quality) ⭐ NEW

**What it does:** ML-based inpainting with automatic watermark detection

**Features:**
- Automatically detects watermark location (any corner)
- Uses OpenCV's Navier-Stokes inpainting algorithm
- Intelligently fills watermark area with surrounding patterns
- Works on ANY watermark type (not just Google SynthID)

**Pros:**
- Highest quality results
- Preserves exact dimensions
- Works on watermarks in any corner
- Handles complex backgrounds intelligently
- Universal - works on all watermark types

**Cons:**
- Requires OpenCV installation (`pip install opencv-python`)
- Slightly slower than crop method
- May need parameter tuning for very large watermarks

**Use when:**
- You need the best possible quality
- Watermark is on complex/detailed background
- Preserving exact dimensions is critical
- Working with non-Google watermarks

### Aggressive Method (Fast & Reliable)

**What it does:** Auto-detects corner, crops 120px, removes alpha channel, paints remnants

**Pros:**
- Fast and reliable
- Automatic detection of watermark corner
- Handles RGBA images properly
- Good for batch processing

**Cons:**
- Reduces image size by 120px
- May crop content near edges

**Use when:**
- Processing many images quickly (default for batch)
- Size reduction is acceptable
- Google SynthID watermarks

### Crop Method

**What it does:** Auto-detects and crops watermark corner

**Pros:**
- Fastest method
- Automatic detection
- Minimal processing

**Cons:**
- May leave watermark remnants
- Doesn't handle alpha channel watermarking

**Use when:**
- Speed is top priority
- Quick preview needed

### Paint Method

**What it does:** Paints over watermark without cropping (no auto-detection)

**Pros:**
- Preserves dimensions
- Simple approach

**Cons:**
- Assumes bottom-right corner only
- May leave visible artifacts
- Less reliable than inpaint

**Use when:**
- Simple watermarks on solid backgrounds
- Legacy compatibility

## Important Guidelines

### Dimension Preservation Priority

**BALANCE DOMAIN KNOWLEDGE WITH DIMENSION PRESERVATION**

1. **Smart default behavior:**
   - Google SynthID detected → `aggressive` method (proven perfect, crops 120px)
   - Unknown watermark → `inpaint` method (preserves dimensions)

2. **User override available:**
   - Force dimension preservation with `--method inpaint` flag
   - Force cropping with `--method aggressive` flag

3. **User approval required for batch cropping:**
   - If processing multiple Google SynthID images with aggressive method
   - Explain that method will reduce image size by 120px
   - Get explicit confirmation
   - Show before/after dimensions

### Batch Processing Protocol

**NEVER start batch processing without user confirmation:**

1. **Show what will happen:**
   - Number of images to process
   - Method to be used
   - Whether dimensions will be preserved or altered

2. **Get explicit approval:**
   - "I will process X images using [method]. This [will/will not] alter dimensions. Proceed?"

3. **Prefer non-destructive:**
   - Default to `inpaint` for batch processing
   - Only use `aggressive` if user specifically requests speed over quality

## Workflow

### 1. Identify Watermarked Images

Common watermark types:
- **Google SynthID:** Small star/sparkle icon in corner
- **Stock photos:** Logo or text overlay
- **AI services:** Corner badges (Midjourney, DALL-E)
- **Camera watermarks:** Date/time stamps

### 2. Choose Method

**Smart Default Workflow (NEW):**
1. **Run script without --method flag** - Smart detection automatically routes to best method
2. **Google SynthID detected** → Uses `aggressive` method (proven perfect)
3. **Unknown watermark** → Uses `inpaint` method (ML-based, preserves dimensions)
4. **Override with --method flag** if needed

**Method Selection Guide:**
- **Smart auto (recommended):** No flag (detects Google SynthID → aggressive, else → inpaint)
- **Force dimension preservation:** `--method inpaint` (ML-based, works on any watermark)
- **Force Google method:** `--method aggressive` (crops 120px, perfect for SynthID)
- **Maximum speed:** `--method crop` (fastest, crops but may leave remnants)
- **Legacy:** `--method paint` (basic, preserves dimensions but less reliable)

### 3. Process Images

**Smart auto-detection (recommended):**
```bash
python scripts/remove-watermark.py input.png output.png
```

**Force dimension preservation:**
```bash
python scripts/remove-watermark.py input.png output.png --method inpaint
```

**Fast batch processing:**
```bash
python scripts/batch-process.py ./input ./output --method aggressive
```

**Disable auto-detection (force bottom-right):**
```bash
python scripts/remove-watermark.py input.png output.png --method inpaint --no-detect
```

### 4. Verify Results

- Check output images for clean corners
- Verify no important content was cropped
- Confirm watermark fully removed

## Command Reference

### remove-watermark.py

```bash
python scripts/remove-watermark.py INPUT OUTPUT [OPTIONS]

Arguments:
  INPUT                 Input image path
  OUTPUT                Output image path

Options:
  --method {crop|inpaint}   Removal method (default: crop)
  --size INT               Watermark size in pixels (default: 60)
```

### batch-process.py

```bash
python scripts/batch-process.py INPUT_DIR OUTPUT_DIR [OPTIONS]

Arguments:
  INPUT_DIR             Directory with images to process
  OUTPUT_DIR            Directory for cleaned images

Options:
  --method {crop|inpaint}   Removal method (default: crop)
  --pattern PATTERN        File pattern to match (default: *.png)
  --size INT               Watermark size in pixels (default: 60)
```

## Examples

### Example 1: Website Images

**Scenario:** User has 3 Google AI images for website, watermarks need removal

```bash
# Batch process all PNG images
python scripts/batch-process.py \
  ./public/images \
  ./public/images-clean \
  --method crop \
  --pattern "*.png"
```

**Output:**
```
Found 3 images to process
Input: ./public/images
Output: ./public/images-clean
Method: crop

[1/3] Processing: ad-design-bedroom.png
   ✅ Saved to: ad-design-bedroom.png
[2/3] Processing: ad-design-kitchen.png
   ✅ Saved to: ad-design-kitchen.png
[3/3] Processing: ad-designs-bathroom.png
   ✅ Saved to: ad-designs-bathroom.png

✅ Successfully processed: 3/3
```

### Example 2: Preserve Exact Dimensions

**Scenario:** Client needs exact 1920x1080 image, can't crop

```bash
python scripts/remove-watermark.py \
  hero-image.png \
  hero-image-clean.png \
  --method inpaint
```

### Example 3: Larger Watermark

**Scenario:** Watermark is bigger than usual (70px)

```bash
python scripts/batch-process.py \
  ./images \
  ./images-clean \
  --method crop \
  --size 70
```

## Technical Details

See [references/synthid-watermark.md](references/synthid-watermark.md) for:
- SynthID watermark specifications
- Method comparison details
- Edge cases and considerations
- Legal/ethical guidelines

## Dependencies

**Required:**
- Python 3.7+
- Pillow (PIL): `pip install Pillow`
- NumPy: `pip install numpy`

**Optional (for ML inpainting):**
- OpenCV: `pip install opencv-python`

Install all dependencies:
```bash
pip install Pillow numpy opencv-python
```

**Note:** The `inpaint` method requires OpenCV. Other methods work without it.

## Tips

**Performance:**
- Crop method is 5-10x faster than inpaint
- For 100+ images, use crop method

**Quality:**
- Save with quality=95 to minimize compression
- PNG format preserves quality better than JPEG

**Backup:**
- Always keep original watermarked images
- Process copies, not originals

**Testing:**
- Test on one image before batch processing
- Verify watermark size with `--size` flag if needed
