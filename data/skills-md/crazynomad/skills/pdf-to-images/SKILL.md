---
name: pdf-to-images
description: Convert PDF files into a series of images (PNG/JPG) using ImageMagick
---

# PDF to Images Converter

Convert PDF files into a series of images using ImageMagick.

## Description

A simple yet powerful tool that converts PDF documents into individual PNG images, one per page. Useful for extracting slides from presentations, creating image previews, or processing PDF content for further analysis.

## When to Use

Use this skill when users:
- Want to convert PDF to images
- Need to extract slides from PDF presentations
- Mention "PDF 转图片", "拆解 PDF", "PDF to PNG"
- Want to create image previews from PDF documents
- Need individual page images from multi-page PDFs

## Features

- **ImageMagick Powered**: Industry-standard image processing
- **Configurable DPI**: Adjust output resolution (default: 150 DPI)
- **Multiple Formats**: Support PNG, JPG, TIFF output
- **Batch Processing**: Handles multi-page PDFs automatically
- **Sequential Naming**: Output files named with page numbers (slide-00, slide-01, etc.)

## Usage

### Basic Syntax

```bash
python scripts/pdf_to_images.py "PDF_FILE" [-o OUTPUT_DIR] [-d DPI] [-f FORMAT]
```

### Common Scenarios

**Convert PDF to PNG images (default)**:
```bash
python scripts/pdf_to_images.py "presentation.pdf"
```

**Specify output directory**:
```bash
python scripts/pdf_to_images.py "document.pdf" -o ./output-images
```

**High resolution output (300 DPI)**:
```bash
python scripts/pdf_to_images.py "document.pdf" -d 300
```

**Output as JPEG**:
```bash
python scripts/pdf_to_images.py "document.pdf" -f jpg -q 90
```

### Arguments

- `pdf_file` (required): Path to the PDF file
- `-o, --output`: Output directory (default: same directory as PDF, with `-slides` suffix)
- `-d, --dpi`: Resolution in DPI (default: 150)
- `-f, --format`: Output format: png, jpg, tiff (default: png)
- `-q, --quality`: JPEG quality 1-100 (default: 85, only for jpg format)
- `-p, --prefix`: Output filename prefix (default: slide)

## Dependencies

Requires ImageMagick installed on the system:

**macOS**:
```bash
brew install imagemagick
```

**Ubuntu/Debian**:
```bash
sudo apt-get install imagemagick
```

**Windows**:
Download from https://imagemagick.org/script/download.php

## Output Structure

```
output-directory/
├── slide-00.png    # Page 1
├── slide-01.png    # Page 2
├── slide-02.png    # Page 3
└── ...
```

## Claude Integration

When user requests PDF to images conversion:

1. **Check ImageMagick availability**:
   ```bash
   which magick || which convert
   ```

2. **Execute conversion**:
   ```bash
   python /mnt/skills/user/pdf-to-images/scripts/pdf_to_images.py \
     "USER_PDF_FILE" -o /mnt/user-data/outputs -d 150
   ```

3. **Present files** to user:
   ```python
   present_files(["/mnt/user-data/outputs/..."])
   ```

## How It Works

### Workflow

1. **Validation**: Check PDF file exists and ImageMagick is available
2. **Create Output Directory**: Create output folder if not exists
3. **Convert**: Use ImageMagick to convert each page to image
4. **Report**: Display generated files and total count

### ImageMagick Command

The script uses:
```bash
magick -density {DPI} "{input.pdf}" "{output_dir}/{prefix}-%02d.{format}"
```

Or for older ImageMagick (v6):
```bash
convert -density {DPI} "{input.pdf}" "{output_dir}/{prefix}-%02d.{format}"
```

## Limitations

- Requires ImageMagick installed on system
- Large PDFs may take time to process
- Memory usage depends on PDF complexity and DPI setting
- Some secured PDFs may not be convertible

## Common Issues

**Q: Getting "convert: not authorized" error?**
A: Edit ImageMagick policy file to allow PDF reading:
```bash
sudo sed -i 's/rights="none" pattern="PDF"/rights="read|write" pattern="PDF"/' /etc/ImageMagick-*/policy.xml
```

**Q: Output images are too small/large?**
A: Adjust DPI with `-d` flag. 150 DPI is good for screen, 300 DPI for print.

**Q: Conversion is slow?**
A: Lower DPI reduces processing time. Try `-d 100` for faster conversion.

## Example Conversation

**User**: "帮我把这个 PDF 拆解成图片: presentation.pdf"

**Claude**:
```bash
# Check ImageMagick
which magick || which convert

# Convert PDF to images
python /mnt/skills/user/pdf-to-images/scripts/pdf_to_images.py \
  "presentation.pdf" \
  -o ./presentation-slides \
  -d 150

# Present files
present_files(["./presentation-slides/slide-00.png", ...])
```

## Version History

**v1.0** (Current)
- ImageMagick-based PDF conversion
- Configurable DPI and format
- Automatic output directory creation
- Support for PNG, JPG, TIFF formats

## License

Personal use tool. Respects PDF document copyrights.
