---
name: optimize-images
description: Batch optimize images for web delivery. Converts to WebP, generates multiple sizes, and creates blur placeholders.
allowed-tools: Read, Bash, Glob
---

# Optimize Images

Optimize images in the specified directory for web delivery.

## Arguments
- `$ARGUMENTS` - Directory path containing images to optimize (default: `./public/images`)

## Process
1. Find all images:
   ```bash
   find ${ARGUMENTS:-./public/images} -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \)
   ```
2. For each image, generate:
   - WebP versions at 320w, 640w, 1280w, 1920w, 2560w
   - Thumbnail at 150x150, 300x300
   - Blur placeholder (10px width, base64)

## Commands
```bash
# Install sharp-cli if not present
pnpm add -D sharp-cli

# Optimize single image example
npx sharp -i input.jpg -o output.webp --format webp --quality 80

# Generate srcset for an image
for size in 320 640 1280 1920 2560; do
  npx sharp -i input.jpg -o "output-${size}w.webp" --resize $size --format webp --quality 80
done

# Generate thumbnail
npx sharp -i input.jpg -o thumb-150.webp --resize 150 150 --fit cover --format webp

# Generate blur placeholder
npx sharp -i input.jpg -o blur.webp --resize 10 --format webp --quality 20
```

## Output
Report:
- Number of images processed
- Original total size
- Optimized total size
- Size savings percentage
