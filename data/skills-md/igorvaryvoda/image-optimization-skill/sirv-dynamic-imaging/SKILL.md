---
name: sirv-dynamic-imaging
description: Sirv dynamic imaging URL API for on-the-fly image transformation. Use when building image URLs with Sirv CDN, resizing images via URL parameters, adding watermarks/text overlays, cropping, applying filters, format conversion (WebP, AVIF), or any Sirv URL-based image manipulation. Covers 100+ URL parameters for scaling, cropping, effects, text, watermarks, frames, and optimization.
---

# Sirv Dynamic Imaging API

Transform images on-the-fly by adding URL parameters.

Base URL: `https://yourcdn.sirv.com/path/image.jpg?{options}`

## Quick Reference

### Sizing

| Option | Example | Description |
|--------|---------|-------------|
| `w` | `?w=800` | Width (px or %) |
| `h` | `?h=600` | Height (px or %) |
| `s` | `?s=500` | Longest dimension |
| `thumbnail` | `?thumbnail=200` | Square thumbnail |
| `scale.option` | `?scale.option=fit` | fit, fill, ignore, noup |

```
?w=800                    # 800px wide
?w=50%                    # 50% of original width
?w=800&h=600              # Specific dimensions
?w=800&scale.option=fit   # Fit within 800px (maintain aspect)
?w=800&scale.option=fill  # Fill 800px (may crop)
```

### Cropping

| Option | Example | Description |
|--------|---------|-------------|
| `cw`, `ch` | `?cw=500&ch=300` | Crop width/height |
| `cx`, `cy` | `?cx=100&cy=50` | Crop start position |
| `crop.type` | `?crop.type=face` | Auto-crop: trim, poi, face |

```
?cw=500&ch=300&cx=100&cy=50   # Manual crop
?crop.type=face&w=400          # Face detection crop
?crop.type=trim                # Trim whitespace
```

### Format & Quality

| Option | Example | Description |
|--------|---------|-------------|
| `format` | `?format=webp` | jpg, png, webp, avif, optimal |
| `q` | `?q=85` | JPEG quality 0-100 |
| `webp-fallback` | `?webp-fallback=jpg` | Fallback for non-WebP browsers |

```
?format=webp&q=80           # WebP at 80% quality
?format=optimal             # Auto-select best format
?format=avif                # AVIF format
```

### Effects

| Option | Range | Description |
|--------|-------|-------------|
| `blur` | 0-100 | Gaussian blur |
| `sharpen` | 0-100 | Sharpen |
| `brightness` | -100 to 100 | Brightness |
| `contrast` | -100 to 100 | Contrast |
| `saturation` | -100 to 100 | Saturation |
| `grayscale` | true/false | Black & white |
| `rotate` | -180 to 180 | Rotation degrees |
| `colortone` | preset name | sepia, warm, cold, sunset... |

```
?blur=10                    # Light blur
?grayscale=true&contrast=20 # B&W with more contrast
?colortone=sepia            # Sepia effect
?rotate=90                  # Rotate 90 degrees
```

### Text Overlay

```
?text=Hello%20World
?text=Hello&text.size=30%&text.color=white&text.position=southeast
?text=©2024&text.font.family=Open%20Sans&text.opacity=50
```

### Watermark

```
?watermark=/logo.png
?watermark=/logo.png&watermark.position=southeast&watermark.opacity=50
?watermark=/logo.png&watermark.scale.width=20%
```

### Canvas & Frame

```
?canvas.width=1200&canvas.height=800&canvas.color=white
?frame.style=solid&frame.color=black&frame.width=10
```

## Common Patterns

### Responsive srcset
```html
<img
  src="https://cdn.sirv.com/image.jpg?w=800"
  srcset="
    https://cdn.sirv.com/image.jpg?w=400 400w,
    https://cdn.sirv.com/image.jpg?w=800 800w,
    https://cdn.sirv.com/image.jpg?w=1200 1200w
  "
  sizes="(max-width: 600px) 100vw, 50vw"
  alt="Description"
>
```

### Modern format with fallback
```html
<picture>
  <source srcset="https://cdn.sirv.com/image.jpg?format=avif" type="image/avif">
  <source srcset="https://cdn.sirv.com/image.jpg?format=webp" type="image/webp">
  <img src="https://cdn.sirv.com/image.jpg" alt="Description">
</picture>
```

### Product thumbnail
```
?w=400&h=400&scale.option=fit&canvas.width=400&canvas.height=400&canvas.color=white
```

### Watermarked download
```
?watermark=/logo.png&watermark.position=southeast&watermark.opacity=30&dl
```

## When to Read Reference Files

- **Sizing & cropping** (scale options, crop modes, canvas): See [sizing.md](references/sizing.md)
- **Effects & filters** (color, blur, sharpen, colortone presets): See [effects.md](references/effects.md)
- **Text & watermarks** (fonts, positioning, styling): See [overlays.md](references/overlays.md)
- **Profiles & optimization** (reusable presets, caching, formats): See [profiles.md](references/profiles.md)

## Processing Order

1. Auto-crop
2. Scale
3. Crop
4. Canvas
5. Rotate
6. Other effects

## Profiles

Save reusable option sets as JSON profiles in `/Profiles/`:

```
?profile=my-thumbnail
```

Profile example:
```json
{
  "image": {
    "scale": {"width": 400},
    "format": "webp",
    "quality": 80
  }
}
```
