---
name: image-converter
description: Convert, resize, compress, and optimize images across formats (HEIC, PNG, JPEG, WebP, AVIF, GIF, TIFF, BMP). Use when working with image files for format conversion, resizing/downscaling, compression/optimization, batch processing, watermarking, metadata stripping, or any image manipulation task. Triggers on requests involving image files, photo processing, or web image optimization.
---

# Image Converter

Convert, resize, compress, and optimize images with Python Pillow.

## Quick Start

```python
from PIL import Image
import pillow_heif

# Register HEIF/HEIC support
pillow_heif.register_heif_opener()

img = Image.open("input.heic")
img.save("output.jpg", quality=85, optimize=True)
```

## Dependencies

```bash
pip install pillow pillow-heif
```

## Format Conversion

### Supported Formats
| Format | Read | Write | Notes |
|--------|------|-------|-------|
| JPEG/JPG | Yes | Yes | Lossy, best for photos |
| PNG | Yes | Yes | Lossless, supports transparency |
| WebP | Yes | Yes | Modern web format, excellent compression |
| HEIC/HEIF | Yes | No* | Apple format, requires pillow-heif |
| GIF | Yes | Yes | Animation support |
| TIFF | Yes | Yes | Lossless, large files |
| BMP | Yes | Yes | Uncompressed |
| AVIF | Yes | Yes* | Best compression, requires pillow-avif-plugin |

*Limited support, check library versions

### Mode Conversion

```python
# RGBA (with alpha) -> RGB (for JPEG)
if img.mode in ('RGBA', 'LA', 'P'):
    img = img.convert('RGB')

# RGB -> Grayscale
gray = img.convert('L')

# Grayscale -> RGB
rgb = gray.convert('RGB')
```

## Resizing & Downscaling

### Proportional Resize

```python
# Resize by percentage
scale = 0.5  # 50%
new_size = (int(img.width * scale), int(img.height * scale))
resized = img.resize(new_size, Image.LANCZOS)

# Resize to max dimension (preserve aspect ratio)
max_dim = 1920
ratio = min(max_dim / img.width, max_dim / img.height)
if ratio < 1:
    new_size = (int(img.width * ratio), int(img.height * ratio))
    resized = img.resize(new_size, Image.LANCZOS)
```

### Thumbnail (in-place, efficient)

```python
img.thumbnail((800, 800), Image.LANCZOS)  # Modifies in-place
```

### Resampling Filters
- `Image.LANCZOS` - Best quality, slower (recommended for downscaling)
- `Image.BICUBIC` - Good quality, faster
- `Image.BILINEAR` - Medium quality
- `Image.NEAREST` - Fastest, pixelated (good for pixel art)

## Compression & Optimization

### JPEG Quality

```python
# Quality 1-100 (80-85 is good balance)
img.save("out.jpg", quality=85, optimize=True)

# Progressive JPEG (loads gradually)
img.save("out.jpg", quality=85, optimize=True, progressive=True)
```

### PNG Optimization

```python
# Maximum compression
img.save("out.png", optimize=True, compress_level=9)

# Reduce colors for smaller file (256 colors max)
quantized = img.quantize(colors=256)
quantized.save("out.png", optimize=True)
```

### WebP (best for web)

```python
# Lossy (like JPEG)
img.save("out.webp", quality=85, method=6)

# Lossless (like PNG but smaller)
img.save("out.webp", lossless=True, quality=100)
```

## Batch Processing

See `scripts/batch_convert.py` for full batch processing with:
- Parallel processing with concurrent.futures
- Progress reporting
- Error handling
- Multiple output formats

### Basic Batch Pattern

```python
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

def convert_image(path, output_dir, target_format, quality=85):
    img = Image.open(path)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    output = output_dir / f"{path.stem}.{target_format}"
    img.save(output, quality=quality, optimize=True)
    return output

input_dir = Path("./images")
output_dir = Path("./converted")
output_dir.mkdir(exist_ok=True)

files = list(input_dir.glob("*.png"))
with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(
        lambda f: convert_image(f, output_dir, "jpg"),
        files
    ))
```

## Metadata & EXIF

### Strip All Metadata

```python
# Create clean image (removes ALL metadata including ICC profile)
clean = Image.new(img.mode, img.size)
clean.putdata(list(img.getdata()))
clean.save("clean.jpg", quality=85)
```

### Strip EXIF Only (preserve ICC color profile)

```python
icc = img.info.get('icc_profile')
if 'exif' in img.info:
    del img.info['exif']
img.save("out.jpg", quality=85, icc_profile=icc)
```

### Handle EXIF Orientation

```python
from PIL import ImageOps
img = ImageOps.exif_transpose(img)  # Auto-rotate based on EXIF
```

## Watermarking

```python
from PIL import Image, ImageDraw, ImageFont

def add_watermark(img, text, opacity=128):
    watermark = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark)

    # Use default font or specify path
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 36)
    except:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    x = img.width - text_width - 20
    y = img.height - text_height - 20

    draw.text((x, y), text, font=font, fill=(255, 255, 255, opacity))

    if img.mode != 'RGBA':
        img = img.convert('RGBA')

    return Image.alpha_composite(img, watermark)
```

## Common Tasks

### HEIC to JPEG (iPhone photos)

```python
import pillow_heif
pillow_heif.register_heif_opener()

img = Image.open("photo.heic")
img = ImageOps.exif_transpose(img)  # Fix orientation
if img.mode != 'RGB':
    img = img.convert('RGB')
img.save("photo.jpg", quality=85, optimize=True)
```

### Optimize for Web

```python
def optimize_for_web(input_path, output_path, max_width=1920, quality=85):
    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)

    # Resize if too large
    if img.width > max_width:
        ratio = max_width / img.width
        new_size = (max_width, int(img.height * ratio))
        img = img.resize(new_size, Image.LANCZOS)

    # Convert mode
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')

    # Strip metadata
    icc = img.info.get('icc_profile')

    # Save optimized
    img.save(output_path, quality=quality, optimize=True,
             progressive=True, icc_profile=icc)
```

### Create Thumbnails

```python
def create_thumbnail(input_path, output_path, size=(300, 300)):
    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)
    img.thumbnail(size, Image.LANCZOS)

    if img.mode != 'RGB':
        img = img.convert('RGB')

    img.save(output_path, quality=85, optimize=True)
```

## File Size Comparison

| Format | Typical Size | Best For |
|--------|-------------|----------|
| JPEG 85% | 100% baseline | Photos |
| WebP 85% | ~30% smaller | Web images |
| PNG | 2-5x larger | Graphics with transparency |
| AVIF 85% | ~50% smaller | Next-gen web |
| HEIC | ~50% smaller | Apple ecosystem |

## Scripts

- `scripts/batch_convert.py` - Full-featured batch converter with CLI
- `scripts/optimize_web.py` - Web optimization with size targets
