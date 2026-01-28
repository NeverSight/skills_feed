---
name: image-processing
description: Process, transform, and analyze images using common operations
---

# Image Processing

Process and transform images.

## Capabilities

- Resize and crop images
- Apply filters and adjustments
- Convert between formats
- Extract metadata and analyze content

## Common Operations

### Resize
```python
from PIL import Image

img = Image.open("input.jpg")
img_resized = img.resize((800, 600), Image.LANCZOS)
img_resized.save("output.jpg")
```

### Crop
```python
# Crop box: (left, upper, right, lower)
img_cropped = img.crop((100, 100, 500, 400))
```

### Format Conversion
```python
img = Image.open("input.png")
img.convert("RGB").save("output.jpg", quality=85)
```

## Filters

| Filter | Use Case |
|--------|----------|
| Blur | Reduce noise, privacy |
| Sharpen | Enhance details |
| Grayscale | Simplify, reduce size |
| Contrast | Improve visibility |

## Supported Formats

- Input: JPEG, PNG, GIF, WebP, BMP, TIFF
- Output: JPEG, PNG, WebP

## Best Practices

1. Preserve aspect ratio when resizing
2. Use appropriate quality settings (JPEG: 80-90)
3. Strip metadata for privacy if needed
4. Consider WebP for web delivery (smaller size)

## Metadata Extraction

```python
from PIL.ExifTags import TAGS

exif = img._getexif()
for tag_id, value in exif.items():
    tag = TAGS.get(tag_id, tag_id)
    print(f"{tag}: {value}")
```
