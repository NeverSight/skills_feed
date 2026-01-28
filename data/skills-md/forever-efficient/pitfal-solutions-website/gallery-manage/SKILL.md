---
name: gallery-manage
description: Organize, validate, and manage photo/video galleries. Create gallery structures, validate image files, and prepare content for upload.
allowed-tools: Bash, Read, Glob, Write
---

# Gallery Management

Manage local gallery content before uploading to S3.

## Arguments
- `$ARGUMENTS` - Command to execute: `list`, `create`, `validate`, `organize`, or `stats`

## Commands

### List Galleries
Show all local galleries and their status:
```bash
ls -la content/galleries/
```

### Create New Gallery

Create a properly structured gallery folder:
```bash
GALLERY_ID=$1  # e.g., "portrait-002"
CATEGORY=$2    # brands, portraits, events, custom

mkdir -p content/galleries/$GALLERY_ID/{originals,processed,thumbnails,blur}

# Create gallery metadata file
cat > content/galleries/$GALLERY_ID/metadata.json << 'EOF'
{
  "id": "GALLERY_ID_PLACEHOLDER",
  "title": "",
  "category": "CATEGORY_PLACEHOLDER",
  "description": "",
  "isPublic": true,
  "isClientGallery": false,
  "createdAt": "TIMESTAMP_PLACEHOLDER"
}
EOF
```

### Validate Gallery Images

Check images meet requirements before upload:
```bash
GALLERY_PATH=$1  # e.g., "content/galleries/portrait-002"

# Check for supported formats
find $GALLERY_PATH/originals -type f \( \
  -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \
  -o -name "*.webp" -o -name "*.heic" -o -name "*.heif" \
  -o -name "*.tiff" -o -name "*.tif" \
\) -print

# Check for unsupported formats (should be empty)
find $GALLERY_PATH/originals -type f \( \
  -name "*.cr2" -o -name "*.nef" -o -name "*.arw" \
  -o -name "*.gif" -o -name "*.bmp" -o -name "*.psd" \
\) -print

# Check file sizes (warn if > 50MB)
find $GALLERY_PATH/originals -type f -size +50M -print

# Count total images
find $GALLERY_PATH/originals -type f \( -name "*.jpg" -o -name "*.jpeg" -o -name "*.png" \) | wc -l
```

### Organize Gallery

Rename files with consistent naming and ordering:
```bash
GALLERY_PATH=$1

# Generate sequential names while preserving extension
cd $GALLERY_PATH/originals
count=1
for file in *.{jpg,jpeg,png,webp}; do
  if [ -f "$file" ]; then
    ext="${file##*.}"
    newname=$(printf "img-%03d.%s" $count "$ext")
    mv "$file" "$newname"
    ((count++))
  fi
done
```

### Gallery Statistics

Show comprehensive stats for a gallery:
```bash
GALLERY_PATH=$1

echo "=== Gallery Statistics ==="
echo "Path: $GALLERY_PATH"
echo ""

# Count by type
echo "Image counts:"
echo "  JPG/JPEG: $(find $GALLERY_PATH/originals -name "*.jpg" -o -name "*.jpeg" | wc -l)"
echo "  PNG: $(find $GALLERY_PATH/originals -name "*.png" | wc -l)"
echo "  WebP: $(find $GALLERY_PATH/originals -name "*.webp" | wc -l)"
echo "  HEIC: $(find $GALLERY_PATH/originals -name "*.heic" -o -name "*.heif" | wc -l)"
echo ""

# Total size
echo "Total size:"
du -sh $GALLERY_PATH/originals

# Processed status
echo ""
echo "Processing status:"
echo "  Processed variants: $(find $GALLERY_PATH/processed -type f 2>/dev/null | wc -l)"
echo "  Thumbnails: $(find $GALLERY_PATH/thumbnails -type f 2>/dev/null | wc -l)"
echo "  Blur placeholders: $(find $GALLERY_PATH/blur -type f 2>/dev/null | wc -l)"
```

## Directory Structure

Expected gallery structure:
```
content/galleries/{gallery-id}/
├── metadata.json      # Gallery metadata
├── originals/         # Original uploaded images
│   ├── img-001.jpg
│   ├── img-002.jpg
│   └── ...
├── processed/         # Generated WebP variants
│   └── img-001/
│       ├── 320w.webp
│       ├── 640w.webp
│       └── ...
├── thumbnails/        # Generated thumbnails
│   └── img-001/
│       ├── sm.webp
│       ├── md.webp
│       └── lg.webp
└── blur/             # Blur placeholders
    ├── img-001.txt
    └── ...
```

## Workflow Integration

This skill works with other skills in this order:

1. `/gallery-manage create` - Create new gallery structure
2. Copy images to `originals/` folder
3. `/gallery-manage validate` - Check images meet requirements
4. `/optimize-images` - Generate variants and thumbnails
5. `/sync-content` - Upload to S3
6. `/db-seed` or API call - Create gallery record in DynamoDB

## Supported Formats

| Format | Extension | Supported | Max Size |
|--------|-----------|-----------|----------|
| JPEG | .jpg, .jpeg | ✓ | 50MB |
| PNG | .png | ✓ | 50MB |
| WebP | .webp | ✓ | 50MB |
| HEIC | .heic, .heif | ✓ | 50MB |
| TIFF | .tiff, .tif | ✓ | 50MB |
| RAW | .cr2, .nef, .arw | ✗ | N/A |
| GIF | .gif | ✗ | N/A |
| PSD | .psd | ✗ | N/A |

## Output

After each command, report:
- Action taken
- Number of files affected
- Any warnings or errors
- Next recommended action
