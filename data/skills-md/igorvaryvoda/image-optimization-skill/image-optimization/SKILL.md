---
name: image-optimization
description: Expert guidance on image optimization for web performance. Use when working with image formats (WebP, AVIF, JPEG, PNG, GIF, SVG, HEIC, JPEG XL), compression settings, responsive images, lazy loading, CDNs, Core Web Vitals, or any image-related web development task. Covers format selection, quality settings, srcset/sizes, picture element, art direction, fetchpriority, placeholder strategies (LQIP, blur-up, blurhash), container queries, HDR/wide color gamut, AI-powered image tools, edge/serverless processing, and performance optimization.
---

# Image Optimization Expert

## Quick Reference

### Format Selection

| Use Case | Best Format | Fallback |
|----------|-------------|----------|
| Photos | AVIF | WebP → JPEG |
| Graphics/logos with transparency | SVG | WebP → PNG |
| Photos with transparency | WebP | PNG |
| Animations | WebP | GIF (or MP4 for long animations) |
| Icons | SVG | WebP → PNG |
| Screenshots | WebP | PNG |

### Quality Settings by Format

| Format | Recommended Quality | Notes |
|--------|---------------------|-------|
| JPEG | 75-85 | 80 is sweet spot for photos |
| WebP | 75-85 | More efficient than JPEG at same quality |
| AVIF | 60-75 | Much more efficient, use lower numbers |
| PNG | N/A | Lossless, optimize with tools like oxipng |

### Responsive Image Breakpoints

Standard widths: 320, 480, 768, 1024, 1366, 1600, 1920, 2560

```html
<img
  src="image-800.jpg"
  srcset="
    image-320.jpg 320w,
    image-480.jpg 480w,
    image-768.jpg 768w,
    image-1024.jpg 1024w,
    image-1600.jpg 1600w
  "
  sizes="(max-width: 768px) 100vw, 50vw"
  alt="Description"
  loading="lazy"
  decoding="async"
>
```

### Modern Format with Fallbacks

```html
<picture>
  <source srcset="image.avif" type="image/avif">
  <source srcset="image.webp" type="image/webp">
  <img src="image.jpg" alt="Description" loading="lazy">
</picture>
```

## When to Read Reference Files

- **Format details** (compression algorithms, browser support, encoding options, HDR, wide color gamut): See [formats.md](references/formats.md)
- **Compression techniques** (lossy vs lossless, quality optimization, SSIM/VMAF thresholds, batch processing): See [optimization.md](references/optimization.md)
- **Responsive images** (srcset, sizes, art direction, fetchpriority, container queries): See [responsive.md](references/responsive.md)
- **Performance** (lazy loading, Core Web Vitals, placeholder strategies, preloading, CDNs): See [performance.md](references/performance.md)
- **Tools and services** (Sirv, Cloudinary, imgix, AI tools, edge/serverless, CLI tools): See [tools.md](references/tools.md)

## Core Principles

1. **Serve modern formats** - AVIF/WebP with JPEG/PNG fallbacks
2. **Right-size images** - Never serve larger than display size
3. **Lazy load below-fold** - Use `loading="lazy"` for offscreen images
4. **Optimize LCP images** - Preload hero images, avoid lazy loading
5. **Use CDN** - Edge caching and automatic optimization
6. **Set dimensions** - Always include width/height to prevent layout shift

## Common Mistakes

- Lazy loading LCP (hero) images - hurts performance
- Missing width/height attributes - causes layout shift (CLS)
- Serving 4K images to mobile devices
- Using PNG for photos (use JPEG/WebP/AVIF)
- Using JPEG for graphics with text/transparency
- Not providing fallbacks for AVIF/WebP
- Over-compressing and creating visible artifacts
- Ignoring aspect ratio in responsive images
