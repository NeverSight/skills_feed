---
name: iconset-maker
description: Create icon sets for multiple operating systems (macOS, Windows, Linux, iOS, Android, Web). Covers required sizes, formats, and conversion workflows using sips, iconutil, ImageMagick, and rsvg-convert.
---

# Icon Set Maker

Expert guidance for creating complete icon sets across all major platforms.

## Available Tools

### macOS Native Tools

| Tool | Command | Purpose |
|------|---------|---------|
| **sips** | `/usr/bin/sips` | Resize, resample, convert between formats |
| **iconutil** | `/usr/bin/iconutil` | Convert .iconset ↔ .icns |

### Homebrew Tools

| Tool | Install | Purpose |
|------|---------|---------|
| **ImageMagick** | `brew install imagemagick` | Multi-size ICO, advanced compositing |
| **librsvg** | `brew install librsvg` | SVG → PNG conversion |
| **optipng** | `brew install optipng` | PNG optimization |
| **pngquant** | `brew install pngquant` | PNG size reduction |

## Platform Requirements

### macOS (.icns)

Required sizes for App.iconset directory:

```
icon_16x16.png        (16×16)
icon_16x16@2x.png     (32×32)
icon_32x32.png        (32×32)
icon_32x32@2x.png     (64×64)
icon_128x128.png      (128×128)
icon_128x128@2x.png   (256×256)
icon_256x256.png      (256×256)
icon_256x256@2x.png   (512×512)
icon_512x512.png      (512×512)
icon_512x512@2x.png   (1024×1024)
```

### Windows (.ico)

Standard sizes to include:

```
16×16     - Small icon (taskbar, file lists)
24×24     - Explorer medium
32×32     - Desktop, Explorer
48×48     - Large icon view
64×64     - Extra large
128×128   - Jumbo (Vista+)
256×256   - High DPI displays (Vista+)
```

### Linux (freedesktop.org)

Directory structure under `/usr/share/icons/hicolor/`:

```
16x16/apps/appname.png
22x22/apps/appname.png
24x24/apps/appname.png
32x32/apps/appname.png
48x48/apps/appname.png
64x64/apps/appname.png
128x128/apps/appname.png
256x256/apps/appname.png
512x512/apps/appname.png
scalable/apps/appname.svg   (optional, preferred)
```

### iOS App Icons

Required for App Store submission:

```
# iPhone
Icon-60@2x.png        (120×120)
Icon-60@3x.png        (180×180)

# iPad
Icon-76.png           (76×76)
Icon-76@2x.png        (152×152)
Icon-83.5@2x.png      (167×167)

# App Store
Icon-1024.png         (1024×1024) - No transparency!

# Spotlight
Icon-40@2x.png        (80×80)
Icon-40@3x.png        (120×120)

# Settings
Icon-29@2x.png        (58×58)
Icon-29@3x.png        (87×87)

# Notification
Icon-20@2x.png        (40×40)
Icon-20@3x.png        (60×60)
```

### Android App Icons

Density buckets in `res/mipmap-*/`:

```
mipmap-mdpi/ic_launcher.png       (48×48)
mipmap-hdpi/ic_launcher.png       (72×72)
mipmap-xhdpi/ic_launcher.png      (96×96)
mipmap-xxhdpi/ic_launcher.png     (144×144)
mipmap-xxxhdpi/ic_launcher.png    (192×192)

# Adaptive icons (Android 8+)
mipmap-anydpi-v26/ic_launcher.xml
mipmap-*/ic_launcher_foreground.png  (108dp with 72dp safe zone)
mipmap-*/ic_launcher_background.png
```

### Web Favicons

```
favicon.ico           (16×16, 32×32 multi-size)
favicon-16x16.png     (16×16)
favicon-32x32.png     (32×32)
apple-touch-icon.png  (180×180)
icon-192.png          (192×192) - PWA
icon-512.png          (512×512) - PWA
safari-pinned-tab.svg (monochrome SVG)
mstile-150x150.png    (150×150) - Windows tiles
```

---

## Conversion Workflows

### From SVG Source (Recommended)

SVG is the ideal source - infinite scalability:

```bash
#!/bin/bash
# Generate all sizes from SVG source

SOURCE_SVG="icon.svg"
OUTPUT_DIR="./icons"
mkdir -p "$OUTPUT_DIR"

# Define all needed sizes
SIZES=(16 20 24 29 32 40 48 58 60 64 72 76 80 87 96 120 128 144 152 167 180 192 256 512 1024)

for SIZE in "${SIZES[@]}"; do
    rsvg-convert -w "$SIZE" -h "$SIZE" "$SOURCE_SVG" -o "$OUTPUT_DIR/icon-${SIZE}.png"
    echo "Generated: icon-${SIZE}.png"
done
```

### Using sips (macOS)

```bash
# Resize a PNG
sips -z 512 512 source.png --out icon_512x512.png

# Resize maintaining aspect ratio (fit within box)
sips --resampleHeightWidth 256 256 source.png --out icon_256.png

# Convert format
sips -s format png source.jpg --out output.png
sips -s format icns source.png --out output.icns

# Batch resize
for SIZE in 16 32 64 128 256 512 1024; do
    sips -z $SIZE $SIZE source.png --out "icon_${SIZE}.png"
done

# Query image properties
sips -g pixelWidth -g pixelHeight -g format image.png
```

### Create macOS .icns

```bash
#!/bin/bash
# Create .icns from a 1024×1024 source PNG

SOURCE_PNG="icon-1024.png"
ICONSET_DIR="AppIcon.iconset"
OUTPUT_ICNS="AppIcon.icns"

# Create iconset directory
mkdir -p "$ICONSET_DIR"

# Generate all required sizes
sips -z 16 16     "$SOURCE_PNG" --out "${ICONSET_DIR}/icon_16x16.png"
sips -z 32 32     "$SOURCE_PNG" --out "${ICONSET_DIR}/icon_16x16@2x.png"
sips -z 32 32     "$SOURCE_PNG" --out "${ICONSET_DIR}/icon_32x32.png"
sips -z 64 64     "$SOURCE_PNG" --out "${ICONSET_DIR}/icon_32x32@2x.png"
sips -z 128 128   "$SOURCE_PNG" --out "${ICONSET_DIR}/icon_128x128.png"
sips -z 256 256   "$SOURCE_PNG" --out "${ICONSET_DIR}/icon_128x128@2x.png"
sips -z 256 256   "$SOURCE_PNG" --out "${ICONSET_DIR}/icon_256x256.png"
sips -z 512 512   "$SOURCE_PNG" --out "${ICONSET_DIR}/icon_256x256@2x.png"
sips -z 512 512   "$SOURCE_PNG" --out "${ICONSET_DIR}/icon_512x512.png"
sips -z 1024 1024 "$SOURCE_PNG" --out "${ICONSET_DIR}/icon_512x512@2x.png"

# Convert to icns
iconutil -c icns "$ICONSET_DIR" -o "$OUTPUT_ICNS"

echo "Created: $OUTPUT_ICNS"

# Cleanup (optional)
# rm -rf "$ICONSET_DIR"
```

### Create Windows .ico

Using ImageMagick (recommended for multi-size ICO):

```bash
#!/bin/bash
# Create .ico with multiple sizes

SOURCE_PNG="icon-1024.png"
OUTPUT_ICO="app.ico"

# Generate individual sizes
magick "$SOURCE_PNG" -resize 16x16   icon-16.png
magick "$SOURCE_PNG" -resize 24x24   icon-24.png
magick "$SOURCE_PNG" -resize 32x32   icon-32.png
magick "$SOURCE_PNG" -resize 48x48   icon-48.png
magick "$SOURCE_PNG" -resize 64x64   icon-64.png
magick "$SOURCE_PNG" -resize 128x128 icon-128.png
magick "$SOURCE_PNG" -resize 256x256 icon-256.png

# Combine into multi-size ICO
magick icon-16.png icon-24.png icon-32.png icon-48.png \
       icon-64.png icon-128.png icon-256.png "$OUTPUT_ICO"

echo "Created: $OUTPUT_ICO"

# Cleanup
rm icon-{16,24,32,48,64,128,256}.png
```

Alternative using sips + ImageMagick:

```bash
# sips for resize, ImageMagick for ICO assembly
for SIZE in 16 24 32 48 64 128 256; do
    sips -z $SIZE $SIZE source.png --out "tmp_${SIZE}.png"
done

magick tmp_*.png app.ico
rm tmp_*.png
```

### Create Web Favicon Package

```bash
#!/bin/bash
# Complete web favicon package

SOURCE_PNG="icon-1024.png"
OUTPUT_DIR="./favicons"
mkdir -p "$OUTPUT_DIR"

# Standard favicons
sips -z 16 16 "$SOURCE_PNG" --out "$OUTPUT_DIR/favicon-16x16.png"
sips -z 32 32 "$SOURCE_PNG" --out "$OUTPUT_DIR/favicon-32x32.png"

# Multi-size favicon.ico
magick "$OUTPUT_DIR/favicon-16x16.png" "$OUTPUT_DIR/favicon-32x32.png" "$OUTPUT_DIR/favicon.ico"

# Apple Touch Icon (no transparency, add background if needed)
sips -z 180 180 "$SOURCE_PNG" --out "$OUTPUT_DIR/apple-touch-icon.png"

# PWA icons
sips -z 192 192 "$SOURCE_PNG" --out "$OUTPUT_DIR/icon-192.png"
sips -z 512 512 "$SOURCE_PNG" --out "$OUTPUT_DIR/icon-512.png"

# Microsoft tile
sips -z 150 150 "$SOURCE_PNG" --out "$OUTPUT_DIR/mstile-150x150.png"

echo "Generated web favicon package in $OUTPUT_DIR/"
```

### Create iOS App Icon Set

```bash
#!/bin/bash
# iOS App Icon generation

SOURCE_PNG="icon-1024.png"
OUTPUT_DIR="./AppIcon.appiconset"
mkdir -p "$OUTPUT_DIR"

# Generate all iOS sizes
declare -A IOS_SIZES=(
    ["Icon-20@2x.png"]=40
    ["Icon-20@3x.png"]=60
    ["Icon-29@2x.png"]=58
    ["Icon-29@3x.png"]=87
    ["Icon-40@2x.png"]=80
    ["Icon-40@3x.png"]=120
    ["Icon-60@2x.png"]=120
    ["Icon-60@3x.png"]=180
    ["Icon-76.png"]=76
    ["Icon-76@2x.png"]=152
    ["Icon-83.5@2x.png"]=167
    ["Icon-1024.png"]=1024
)

for FILENAME in "${!IOS_SIZES[@]}"; do
    SIZE="${IOS_SIZES[$FILENAME]}"
    sips -z "$SIZE" "$SIZE" "$SOURCE_PNG" --out "$OUTPUT_DIR/$FILENAME"
    echo "Generated: $FILENAME (${SIZE}×${SIZE})"
done

# Generate Contents.json for Xcode
cat > "$OUTPUT_DIR/Contents.json" << 'EOF'
{
  "images" : [
    {"filename":"Icon-20@2x.png","idiom":"iphone","scale":"2x","size":"20x20"},
    {"filename":"Icon-20@3x.png","idiom":"iphone","scale":"3x","size":"20x20"},
    {"filename":"Icon-29@2x.png","idiom":"iphone","scale":"2x","size":"29x29"},
    {"filename":"Icon-29@3x.png","idiom":"iphone","scale":"3x","size":"29x29"},
    {"filename":"Icon-40@2x.png","idiom":"iphone","scale":"2x","size":"40x40"},
    {"filename":"Icon-40@3x.png","idiom":"iphone","scale":"3x","size":"40x40"},
    {"filename":"Icon-60@2x.png","idiom":"iphone","scale":"2x","size":"60x60"},
    {"filename":"Icon-60@3x.png","idiom":"iphone","scale":"3x","size":"60x60"},
    {"filename":"Icon-76.png","idiom":"ipad","scale":"1x","size":"76x76"},
    {"filename":"Icon-76@2x.png","idiom":"ipad","scale":"2x","size":"76x76"},
    {"filename":"Icon-83.5@2x.png","idiom":"ipad","scale":"2x","size":"83.5x83.5"},
    {"filename":"Icon-1024.png","idiom":"ios-marketing","scale":"1x","size":"1024x1024"}
  ],
  "info" : {"author":"xcode","version":1}
}
EOF

echo "Created iOS App Icon set in $OUTPUT_DIR/"
```

### Create Android Adaptive Icons

```bash
#!/bin/bash
# Android adaptive icon generation

SOURCE_PNG="icon-1024.png"
OUTPUT_DIR="./android"

# Standard launcher icons
declare -A ANDROID_SIZES=(
    ["mipmap-mdpi"]=48
    ["mipmap-hdpi"]=72
    ["mipmap-xhdpi"]=96
    ["mipmap-xxhdpi"]=144
    ["mipmap-xxxhdpi"]=192
)

for DENSITY in "${!ANDROID_SIZES[@]}"; do
    SIZE="${ANDROID_SIZES[$DENSITY]}"
    mkdir -p "$OUTPUT_DIR/$DENSITY"
    sips -z "$SIZE" "$SIZE" "$SOURCE_PNG" --out "$OUTPUT_DIR/$DENSITY/ic_launcher.png"
    echo "Generated: $DENSITY/ic_launcher.png (${SIZE}×${SIZE})"
done

# For adaptive icons, also generate foreground/background
# Foreground should be 108dp with content in center 72dp
ADAPTIVE_SIZES=(
    ["mipmap-mdpi"]=108
    ["mipmap-hdpi"]=162
    ["mipmap-xhdpi"]=216
    ["mipmap-xxhdpi"]=324
    ["mipmap-xxxhdpi"]=432
)

echo ""
echo "For adaptive icons (Android 8+), create:"
echo "  - ic_launcher_foreground.png (108dp, content in center 72dp)"
echo "  - ic_launcher_background.png (solid color or pattern)"
echo "  - ic_launcher.xml referencing both"
```

---

## Complete Multi-Platform Script

```bash
#!/bin/bash
# Generate icons for ALL platforms from a single source

set -e

SOURCE="${1:-icon.svg}"
OUTPUT_BASE="${2:-./icons}"

if [[ ! -f "$SOURCE" ]]; then
    echo "Usage: $0 <source-image> [output-directory]"
    echo "Source should be SVG (preferred) or 1024×1024+ PNG"
    exit 1
fi

echo "=== Multi-Platform Icon Generator ==="
echo "Source: $SOURCE"
echo "Output: $OUTPUT_BASE"
echo ""

# Detect source type
if [[ "$SOURCE" == *.svg ]]; then
    CONVERT_CMD="rsvg-convert"
    echo "Source type: SVG (using rsvg-convert)"
else
    CONVERT_CMD="sips"
    echo "Source type: Raster (using sips)"
fi

# Function to generate PNG at size
generate_png() {
    local SIZE=$1
    local OUTPUT=$2

    if [[ "$CONVERT_CMD" == "rsvg-convert" ]]; then
        rsvg-convert -w "$SIZE" -h "$SIZE" "$SOURCE" -o "$OUTPUT"
    else
        sips -z "$SIZE" "$SIZE" "$SOURCE" --out "$OUTPUT" >/dev/null
    fi
}

# === macOS ===
echo "Generating macOS icons..."
MACOS_DIR="$OUTPUT_BASE/macos/AppIcon.iconset"
mkdir -p "$MACOS_DIR"

generate_png 16   "$MACOS_DIR/icon_16x16.png"
generate_png 32   "$MACOS_DIR/icon_16x16@2x.png"
generate_png 32   "$MACOS_DIR/icon_32x32.png"
generate_png 64   "$MACOS_DIR/icon_32x32@2x.png"
generate_png 128  "$MACOS_DIR/icon_128x128.png"
generate_png 256  "$MACOS_DIR/icon_128x128@2x.png"
generate_png 256  "$MACOS_DIR/icon_256x256.png"
generate_png 512  "$MACOS_DIR/icon_256x256@2x.png"
generate_png 512  "$MACOS_DIR/icon_512x512.png"
generate_png 1024 "$MACOS_DIR/icon_512x512@2x.png"

iconutil -c icns "$MACOS_DIR" -o "$OUTPUT_BASE/macos/AppIcon.icns"
echo "  ✓ AppIcon.icns"

# === Windows ===
echo "Generating Windows icons..."
WIN_DIR="$OUTPUT_BASE/windows"
mkdir -p "$WIN_DIR"

for SIZE in 16 24 32 48 64 128 256; do
    generate_png "$SIZE" "$WIN_DIR/icon-${SIZE}.png"
done

magick "$WIN_DIR/icon-16.png" "$WIN_DIR/icon-24.png" "$WIN_DIR/icon-32.png" \
       "$WIN_DIR/icon-48.png" "$WIN_DIR/icon-64.png" "$WIN_DIR/icon-128.png" \
       "$WIN_DIR/icon-256.png" "$WIN_DIR/app.ico"
echo "  ✓ app.ico"

# === Web ===
echo "Generating web favicons..."
WEB_DIR="$OUTPUT_BASE/web"
mkdir -p "$WEB_DIR"

generate_png 16  "$WEB_DIR/favicon-16x16.png"
generate_png 32  "$WEB_DIR/favicon-32x32.png"
generate_png 180 "$WEB_DIR/apple-touch-icon.png"
generate_png 192 "$WEB_DIR/icon-192.png"
generate_png 512 "$WEB_DIR/icon-512.png"
generate_png 150 "$WEB_DIR/mstile-150x150.png"

magick "$WEB_DIR/favicon-16x16.png" "$WEB_DIR/favicon-32x32.png" "$WEB_DIR/favicon.ico"
echo "  ✓ favicon package"

# === iOS ===
echo "Generating iOS icons..."
IOS_DIR="$OUTPUT_BASE/ios/AppIcon.appiconset"
mkdir -p "$IOS_DIR"

generate_png 40   "$IOS_DIR/Icon-20@2x.png"
generate_png 60   "$IOS_DIR/Icon-20@3x.png"
generate_png 58   "$IOS_DIR/Icon-29@2x.png"
generate_png 87   "$IOS_DIR/Icon-29@3x.png"
generate_png 80   "$IOS_DIR/Icon-40@2x.png"
generate_png 120  "$IOS_DIR/Icon-40@3x.png"
generate_png 120  "$IOS_DIR/Icon-60@2x.png"
generate_png 180  "$IOS_DIR/Icon-60@3x.png"
generate_png 76   "$IOS_DIR/Icon-76.png"
generate_png 152  "$IOS_DIR/Icon-76@2x.png"
generate_png 167  "$IOS_DIR/Icon-83.5@2x.png"
generate_png 1024 "$IOS_DIR/Icon-1024.png"
echo "  ✓ iOS App Icon set"

# === Android ===
echo "Generating Android icons..."
ANDROID_DIR="$OUTPUT_BASE/android"

for DENSITY_SIZE in "mdpi:48" "hdpi:72" "xhdpi:96" "xxhdpi:144" "xxxhdpi:192"; do
    DENSITY="${DENSITY_SIZE%%:*}"
    SIZE="${DENSITY_SIZE##*:}"
    mkdir -p "$ANDROID_DIR/mipmap-$DENSITY"
    generate_png "$SIZE" "$ANDROID_DIR/mipmap-$DENSITY/ic_launcher.png"
done
echo "  ✓ Android mipmap icons"

# === Linux ===
echo "Generating Linux icons..."
LINUX_DIR="$OUTPUT_BASE/linux/hicolor"

for SIZE in 16 22 24 32 48 64 128 256 512; do
    mkdir -p "$LINUX_DIR/${SIZE}x${SIZE}/apps"
    generate_png "$SIZE" "$LINUX_DIR/${SIZE}x${SIZE}/apps/app.png"
done
echo "  ✓ Linux hicolor icons"

echo ""
echo "=== Complete ==="
echo "Icons generated in: $OUTPUT_BASE/"
find "$OUTPUT_BASE" -name "*.icns" -o -name "*.ico" | sort
```

---

## Quality Tips

### Source Image Requirements

- **Minimum size**: 1024×1024 pixels for raster, any size for SVG
- **Format**: SVG preferred, PNG with transparency for raster
- **Color space**: sRGB
- **Transparency**: Supported except iOS App Store icon

### Optimization

```bash
# Optimize PNGs (lossless)
optipng -o7 *.png

# Reduce PNG file size (lossy but visually identical)
pngquant --quality=80-100 --ext .png --force *.png
```

### Verification

```bash
# Check generated icon properties
sips -g pixelWidth -g pixelHeight -g format icon.png

# Verify .icns contents
iconutil -c iconset AppIcon.icns -o verify.iconset
ls -la verify.iconset/

# Verify .ico contents
magick identify app.ico
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| sips: unrecognized format | Ensure source is valid PNG/JPEG |
| iconutil: invalid iconset | Check all required sizes present with exact naming |
| ICO appears blurry | Include 256×256 size for high-DPI displays |
| iOS icon rejected | Ensure 1024×1024 has no transparency |
| Colors look wrong | Convert to sRGB color space first |

## Checklist

Before distribution:

- [ ] Source is 1024×1024+ or SVG
- [ ] All platform-required sizes generated
- [ ] No transparency in iOS App Store icon
- [ ] Windows ICO includes 256×256 for high-DPI
- [ ] PNGs optimized for file size
- [ ] Verified icons render correctly at all sizes
