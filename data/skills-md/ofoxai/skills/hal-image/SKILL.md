---
name: hal-image
description: Handle images with ImageMagick (magick) — read metadata, resize, crop, rotate, convert format, combine images (side-by-side or grids with montage), overlay logos/watermarks, and losslessly compress with oxipng before sending. Use when the user sends an image to process, when you produce an image to deliver, or before attaching any image to a message or upload — compressing first keeps transfers fast and tokens low. Core discipline - always compress before delivering, never expose local file paths to the user, and fail open (if a tool is missing or a step errors, pass the original through unchanged; never block the task).
license: MIT
version: "1.1.0"
homepage: https://github.com/ofoxai/skills/tree/main/skills/hal-image
metadata:
  author: ofoxai
  version: "1.1.0"
  openclaw:
    requires:
      bins: [magick, oxipng]
    emoji: "🏞️"
    homepage: https://github.com/ofoxai/skills/tree/main/skills/hal-image
---

# hal-image: agent-safe image handling

One tool does almost everything: **`magick`** (ImageMagick) reads metadata and
resizes / crops / rotates / converts / combines / watermarks images. One extra
tool, **`oxipng`**, does best-in-class *lossless* PNG compression. Together they
let an agent process and deliver images without bloating tokens or stalling
uploads.

## Core discipline

1. **Compress before you deliver.** Before attaching/uploading/sending any
   image, run it through lossless compression (below). A 2 MB screenshot
   becomes ~0.7 MB with *zero* pixel change — saving multimodal tokens and
   avoiding slow/aborted transfers.
2. **Never expose local paths to the user.** Work with files locally, but the
   message to the user references the image itself, not `/Users/...`/`~/...`.
3. **Fail open.** This is a helper, not a gate. If `magick`/`oxipng` is missing
   or a command errors, pass the *original* image through and continue — never
   block the task on image tooling.

## When to apply

- The user sends an image you need to inspect or transform (resize, crop,
  annotate, combine).
- You generated or rendered an image (a chart, a poster, a screenshot) and are
  about to deliver it.
- **Always** right before attaching any image to a message or upload — compress
  it first.

## Check availability

```bash
magick --version     # ImageMagick 7+; the `magick` command (not legacy `convert`)
oxipng --version     # lossless PNG optimizer
```

Install if missing (macOS/Linux via Homebrew):

```bash
brew install imagemagick oxipng
# JPEG/WebP compressors (optional, for those formats):
brew install jpegoptim webp
```

`magick` covers metadata + all processing; `oxipng` is the PNG compressor.
`jpegoptim`/`cwebp` are only needed for JPEG/WebP compression.

## 1. Read metadata first

Always look before you act — know the format and size so you can decide whether
to compress and how to resize.

```bash
identify -format '%m %wx%h %[bit-depth]-bit %[size] bytes\n' image.png
# e.g. -> PNG 2160x2880 8-bit 2287044 bytes
```

(`identify` ships with ImageMagick.) If an image is large (say > 1 MB or wider
than you need), resize and/or compress before using or sending it.

## 2. Everyday processing (all `magick`)

Each command is `magick <input> <operations...> <output>`. Verified working.

```bash
# Resize to 800px wide, keep aspect ratio
magick in.png -resize 800x out.png

# Crop a centered 400x400 region (+repage clears the crop offset)
magick in.png -gravity center -crop 400x400+0+0 +repage out.png

# Combine images: side by side (+append) or stacked (-append)
magick a.png b.png +append row.png      # horizontal
magick a.png b.png -append column.png   # vertical

# Grid / collage: 2x2 tiles with 6px gaps on a dark background
montage a.png b.png c.png d.png -tile 2x2 -geometry +6+6 -background "#0b0e14" grid.png

# Overlay a logo in the bottom-right corner (-composite)
magick base.png logo.png -gravity southeast -geometry +12+12 -composite out.png

# Rotate, desaturate, and convert format in one pass
magick in.png -rotate 12 -colorspace Gray out.jpg

# Flatten transparency onto white when converting PNG -> JPEG
magick in.png -background white -flatten out.jpg
```

### Text watermark (font must be explicit)

ImageMagick has **no reliable default font** on many machines, so `-annotate`
fails with `unable to read font ''` unless you pass `-font` with a real path.
Always specify a font:

```bash
# Find a system font (macOS / common Linux paths)
FONT=$(for f in \
  /System/Library/Fonts/Supplemental/Arial.ttf \
  /System/Library/Fonts/Helvetica.ttc \
  /usr/share/fonts/truetype/dejavu/DejaVuSans.ttf \
  /usr/share/fonts/TTF/DejaVuSans.ttf; do
  [ -f "$f" ] && echo "$f" && break; done)

magick in.png -gravity south -font "$FONT" -pointsize 30 -fill "#4cc4ff" \
  -annotate +0+24 "watermark text" out.png
```

If no font is found, skip the watermark (fail open) rather than erroring.

## 3. Lossless compression (do this before delivering)

Compression is **lossless** — pixels are identical, only the encoding shrinks.
Pick by format:

```bash
# PNG (preferred path) — oxipng, ~70% smaller, pixel-identical
oxipng -o max --strip safe image.png        # rewrites image.png in place

# JPEG — jpegoptim, lossless re-optimization
jpegoptim --strip-all image.jpg             # rewrites in place

# WebP — lossless encode (also a good way to shrink a PNG if WebP is acceptable)
cwebp -lossless -quiet in.png -o out.webp
```

`oxipng -o max` keeps the file a PNG (best for compatibility); `--strip safe`
removes non-essential metadata without touching pixels. Verify losslessness if
ever in doubt:

```bash
magick compare -metric RMSE before.png after.png null:   # prints 0 = identical
```

If the compressor is missing or fails, deliver the original (fail open).

## Typical flow

Receiving an image to look at:

```bash
identify -format '%m %wx%h %[size] bytes\n' inbox/photo.jpg   # 1. inspect
# 2. if huge, shrink before reading it into context:
magick inbox/photo.jpg -resize 1600x inbox/photo.small.jpg && jpegoptim --strip-all inbox/photo.small.jpg
# 3. read the smaller file
```

Delivering an image you produced:

```bash
# 1. (optional) process — crop / annotate / combine
magick raw.png -resize 1200x staged.png
# 2. ALWAYS compress before sending
oxipng -o max --strip safe staged.png
# 3. send staged.png through the channel — never mention its local path
```

## References

| File | Read when |
|------|-----------|
| [`references/recipes.md`](references/recipes.md) | You need a less common operation: borders, padding, format-specific tricks, GIF from frames, batch processing, EXIF handling, transparency, quality/size trade-offs. |
