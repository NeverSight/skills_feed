---
name: optimize-images
description: This skill should be used when the user asks to "optimize images", "compress images", "reduce image file size", "make images smaller", "optimize PNGs", "optimize JPEGs", "speed up website images", "reduce bundle size images", or needs help with image compression for web projects. Provides workflows and scripts for batch image optimization using sharp.
version: 1.0.0
---

# Image Optimization for Web Projects

Optimize images for web performance using modern tools. This skill provides scripts and workflows for compressing PNG and JPEG images while maintaining visual quality.

## When to Use This Skill

- Preparing images for production web deployment
- Reducing page load times
- Optimizing public/images directories
- Batch compressing screenshots, watercolors, photos
- Auditing image sizes before/after optimization

## Core Tool: Sharp

Sharp is the fastest Node.js image processing library, built on libvips. Use it for all image optimization tasks.

### Install Sharp

```bash
bun add -d sharp
# or
npm install -D sharp
```

## Quick Start Workflow

### 1. Benchmark Current State

Before optimization, measure baseline metrics:

```bash
# Total size and count
du -sh public/images/
find public/images -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" \) | wc -l

# Size by format
find public/images -name "*.png" -exec du -ch {} + | tail -1
find public/images \( -name "*.jpg" -o -name "*.jpeg" \) -exec du -ch {} + | tail -1

# Top 20 largest files
find public/images -type f \( -name "*.png" -o -name "*.jpg" \) -exec ls -la {} \; | \
  awk '{print $5, $9}' | sort -rn | head -20 | \
  awk '{printf "%6.1fMB  %s\n", $1/1048576, $2}'
```

### 2. Test on Single Image

Always test optimization settings on one image first:

```bash
bun run scripts/optimize-images.ts --file=public/images/largest-image.png --dry-run
```

### 3. Run Full Optimization

After verifying settings work well:

```bash
bun run scripts/optimize-images.ts
```

### 4. Verify Results

```bash
# Compare before/after
du -sh public/images/

# Visually inspect optimized images
# Run production build
bun run build
```

## Optimization Settings

### PNG Optimization

Sharp's PNG encoder with palette mode for maximum compression:

```typescript
sharp(filePath)
  .png({
    quality: 80,           // 1-100, lower = smaller
    compressionLevel: 9,   // 0-9, higher = more compression
    adaptiveFiltering: true,
    palette: true,         // Use palette for smaller files
  })
  .toBuffer();
```

**Recommended settings:**
- Screenshots: quality 80, compression 9
- Photos: quality 85, compression 9
- Icons/logos: quality 90, compression 9 (preserve crispness)

### JPEG Optimization

Sharp with mozjpeg for superior compression:

```typescript
sharp(filePath)
  .jpeg({
    quality: 80,    // 1-100, lower = smaller
    mozjpeg: true,  // Use mozjpeg encoder
  })
  .toBuffer();
```

**Recommended settings:**
- Photos: quality 75-80
- Screenshots: quality 80-85
- Hero images: quality 85

## The Optimization Script

Copy `scripts/optimize-images.ts` to the project's scripts directory. The script:

1. Recursively finds all PNG/JPEG images
2. Applies compression settings
3. Overwrites originals (only if smaller)
4. Reports savings per file
5. Shows total savings summary

### Script Usage

```bash
# Dry run (see what would happen)
bun run scripts/optimize-images.ts --dry-run

# Test single file
bun run scripts/optimize-images.ts --file=path/to/image.png

# Full optimization
bun run scripts/optimize-images.ts
```

### Expected Savings

Typical results for unoptimized web images:

| Image Type | Typical Savings |
|------------|-----------------|
| Screenshots (PNG) | 40-60% |
| Photos (JPEG) | 20-40% |
| Watercolors (PNG) | 30-50% |
| Icons (PNG) | 10-30% |

## Next.js Considerations

Next.js provides automatic image optimization via `next/image`. However, optimizing source images still helps:

1. **Faster builds** - Smaller source images = faster processing
2. **Fallback support** - Non-Next.js imports still benefit
3. **Reduced storage** - Smaller repo size
4. **CDN efficiency** - Less data to cache/serve

Keep source images optimized even when using `next/image`.

## Workflow Integration

### Pre-commit Hook (Optional)

Add to `.husky/pre-commit` or git hooks:

```bash
# Warn if large images are being committed
find public/images -name "*.png" -size +500k -exec echo "Warning: Large image: {}" \;
```

### CI/CD Check

Add to build pipeline:

```bash
# Fail if images exceed threshold
MAX_SIZE=79  # MB
CURRENT=$(du -sm public/images | cut -f1)
if [ "$CURRENT" -gt "$MAX_SIZE" ]; then
  echo "Error: Images exceed ${MAX_SIZE}MB (currently ${CURRENT}MB)"
  exit 1
fi
```

## Troubleshooting

### Image Quality Too Low

Increase quality settings:
- PNG: Increase `quality` to 85-90
- JPEG: Increase `quality` to 85-90

### Transparent PNGs Look Wrong

Ensure `palette: true` handles transparency correctly. For complex transparency, use:

```typescript
.png({ quality: 85, palette: false })
```

### Sharp Installation Issues

On macOS, ensure libvips is available:

```bash
brew install vips
```

Or let sharp download pre-built binaries:

```bash
npm rebuild sharp
```

## Additional Resources

### Reference Files

- **`references/optimization-guide.md`** - Detailed compression algorithms and format comparison
- **`references/sharp-api.md`** - Complete sharp API reference for images

### Scripts

- **`scripts/optimize-images.ts`** - Production-ready optimization script

## Context Discipline

**Do not read optimized images back into context.** The script outputs a summary table with file sizes, savings percentages, and totals. Ask the user to visually inspect results if quality verification is needed. Even optimized images can be large enough to fill the context window when processing many files.

## Summary

1. Install sharp: `bun add -d sharp`
2. Copy optimization script to project
3. Benchmark: `du -sh public/images/`
4. Test: `bun run scripts/optimize-images.ts --dry-run`
5. Optimize: `bun run scripts/optimize-images.ts`
6. Verify: Check sizes and visual quality
7. Commit: Include optimized images in deployment
