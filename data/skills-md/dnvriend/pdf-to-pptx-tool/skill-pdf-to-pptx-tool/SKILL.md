---
name: skill-pdf-to-pptx-tool
description: Convert PDF to PowerPoint presentations
---

# When to use
- Converting PDF documents to editable PowerPoint presentations
- Creating slide decks from PDF reports or documents
- Need high-quality PDF to PPTX conversion with custom DPI
- Want multi-level verbosity logging for debugging conversions

# PDF to PowerPoint Converter Skill

## Purpose

This skill provides comprehensive guidance for using `pdf-to-pptx-tool`, a professional CLI tool that converts PDF documents into PowerPoint presentations. Each PDF page becomes a high-quality slide with customizable resolution.

## When to Use This Skill

**Use this skill when:**
- You need to convert PDF documents to PowerPoint format
- You want to customize conversion quality (DPI settings)
- You need to debug conversion issues with verbose logging
- You're working with multi-page PDF documents
- You need programmatic PDF to PPTX conversion in workflows

**Do NOT use this skill for:**
- Editing existing PowerPoint files (use PowerPoint directly)
- Converting other formats (images, Word docs) to PPTX
- Extracting text from PDFs (use PDF text extraction tools)
- Creating PowerPoint from scratch (use PowerPoint or python-pptx)

## CLI Tool: pdf-to-pptx-tool

A modern Python CLI tool built with Click, featuring multi-level verbosity logging, shell completion, and type-safe code.

### Installation

```bash
# Clone the repository
git clone https://github.com/dnvriend/pdf-to-pptx-tool.git
cd pdf-to-pptx-tool

# Install globally with uv
uv tool install .
```

### Prerequisites

- Python 3.14+
- `poppler` system library (for PDF rendering)
  - macOS: `brew install poppler`
  - Ubuntu/Debian: `apt-get install poppler-utils`
  - Windows: Download from poppler releases

### Quick Start

```bash
# Basic conversion
pdf-to-pptx-tool convert document.pdf slides.pptx

# High quality (300 DPI)
pdf-to-pptx-tool convert report.pdf presentation.pptx --dpi 300

# With verbose logging
pdf-to-pptx-tool -v convert input.pdf output.pptx
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

### convert - Convert PDF to PowerPoint

Converts a PDF document to PowerPoint format, creating one slide per PDF page with customizable quality settings.

**Usage:**
```bash
pdf-to-pptx-tool convert INPUT_PDF OUTPUT_PPTX [OPTIONS]
```

**Arguments:**
- `INPUT_PDF`: Path to input PDF file (required)
  - Must exist and be a valid PDF file
  - Supports any PDF version
  - No size limit (memory permitting)
- `OUTPUT_PPTX`: Path to output PowerPoint file (required)
  - Will be created or overwritten
  - Extension should be `.pptx`
  - Parent directory must exist
- `--dpi INTEGER`: Resolution for page conversion (optional)
  - Default: 200 DPI (good quality, reasonable size)
  - Range: 72-600 DPI
  - Higher DPI = better quality but larger files
  - Recommended: 200-300 for presentations
- `-v, --verbose`: Multi-level verbosity
  - No flag: Warnings/errors only
  - `-v`: INFO level (operations and progress)
  - `-vv`: DEBUG level (detailed steps)
  - `-vvv`: TRACE level (library internals)

**Examples:**
```bash
# Example 1: Basic conversion (default 200 DPI)
pdf-to-pptx-tool convert quarterly-report.pdf q4-presentation.pptx

# Example 2: High quality for detailed diagrams
pdf-to-pptx-tool convert technical-diagram.pdf slides.pptx --dpi 300

# Example 3: Lower quality for quick preview
pdf-to-pptx-tool convert draft.pdf preview.pptx --dpi 150

# Example 4: With INFO logging to see progress
pdf-to-pptx-tool -v convert large-doc.pdf output.pptx

# Example 5: With DEBUG logging for troubleshooting
pdf-to-pptx-tool -vv convert problematic.pdf fixed.pptx

# Example 6: Batch conversion with shell loop
for pdf in *.pdf; do
  pdf-to-pptx-tool convert "$pdf" "${pdf%.pdf}.pptx"
done
```

**Output:**
- Creates PowerPoint file at specified path
- Slide properties:
  - Aspect ratio: 16:9 (widescreen)
  - Dimensions: 10" × 5.625"
  - Layout: One full-slide image per PDF page
  - Background: Transparent
- Console output:
  - Success: "✓ Successfully converted input.pdf to output.pptx"
  - Error: "✗ Error: [detailed error message]"
- Exit codes:
  - 0: Success
  - 1: Error (file not found, invalid input, conversion failed)

---

### completion - Generate shell completion scripts

Generates shell completion scripts for bash, zsh, or fish shells.

**Usage:**
```bash
pdf-to-pptx-tool completion SHELL
```

**Arguments:**
- `SHELL`: Shell type (required)
  - Options: `bash`, `zsh`, `fish`
  - Case-insensitive

**Examples:**
```bash
# Generate bash completion
eval "$(pdf-to-pptx-tool completion bash)"

# Generate zsh completion
eval "$(pdf-to-pptx-tool completion zsh)"

# Generate fish completion
pdf-to-pptx-tool completion fish | source

# Save to file for permanent installation
pdf-to-pptx-tool completion bash > ~/.pdf-to-pptx-tool-completion.bash
echo 'source ~/.pdf-to-pptx-tool-completion.bash' >> ~/.bashrc
```

**Output:**
Shell-specific completion script printed to stdout.

</details>

<details>
<summary><strong>⚙️  Advanced Features (Click to expand)</strong></summary>

### Multi-Level Verbosity Logging

The tool supports progressive verbosity levels for debugging and monitoring conversions.

**Logging Levels:**

| Flag | Level | Output | Use Case |
|------|-------|--------|----------|
| (none) | WARNING | Errors/warnings only | Production, quiet mode |
| `-v` | INFO | + Operations, progress | Normal debugging |
| `-vv` | DEBUG | + Detailed steps, file sizes | Development, troubleshooting |
| `-vvv` | TRACE | + Library internals (pdf2image, PIL, pptx) | Deep debugging |

**Examples:**
```bash
# Quiet mode - only see errors
pdf-to-pptx-tool convert input.pdf output.pptx

# INFO - see conversion progress
pdf-to-pptx-tool -v convert input.pdf output.pptx
# Output:
# [INFO] Starting PDF to PPTX conversion
# [INFO] Converting input.pdf to output.pptx (DPI: 200)
# [INFO] Converting PDF pages to images...
# [INFO] Converted 5 pages
# [INFO] Creating PowerPoint presentation...
# [INFO] Saving presentation to output.pptx

# DEBUG - see detailed processing
pdf-to-pptx-tool -vv convert input.pdf output.pptx
# Additional output:
# [DEBUG] Input: input.pdf, Output: output.pptx, DPI: 200
# [DEBUG] Validating input file: input.pdf
# [DEBUG] Input file size: 2.45 MB
# [DEBUG] Using DPI setting: 200
# [DEBUG] Processing slide 1/5
# [DEBUG] Output file size: 8.23 MB

# TRACE - see library internals
pdf-to-pptx-tool -vvv convert input.pdf output.pptx
# Shows pdf2image, PIL, and pptx library debug messages
```

### DPI Quality Guidelines

Choose DPI based on your use case:

| DPI | Quality | File Size | Best For |
|-----|---------|-----------|----------|
| 72 | Low | Smallest | Quick previews, draft slides |
| 150 | Medium | Small | Web presentations, email |
| 200 | Good | Medium | **Default - recommended for most** |
| 300 | High | Large | Print quality, detailed diagrams |
| 600 | Very High | Very Large | Professional print, posters |

**Trade-offs:**
- **Higher DPI**: Better quality, larger file size, slower conversion
- **Lower DPI**: Faster conversion, smaller files, lower quality
- **Sweet spot**: 200-300 DPI for most presentations

### Batch Processing

Process multiple PDFs efficiently:

```bash
# Convert all PDFs in directory
for pdf in *.pdf; do
  echo "Converting $pdf..."
  pdf-to-pptx-tool convert "$pdf" "${pdf%.pdf}.pptx"
done

# With custom DPI
for pdf in *.pdf; do
  pdf-to-pptx-tool convert "$pdf" "${pdf%.pdf}.pptx" --dpi 300
done

# With error handling
for pdf in *.pdf; do
  if pdf-to-pptx-tool -v convert "$pdf" "${pdf%.pdf}.pptx"; then
    echo "✓ Converted $pdf"
  else
    echo "✗ Failed to convert $pdf"
  fi
done
```

### Shell Completion

Enable tab completion for faster usage:

```bash
# Bash - add to ~/.bashrc
eval "$(pdf-to-pptx-tool completion bash)"

# Zsh - add to ~/.zshrc
eval "$(pdf-to-pptx-tool completion zsh)"

# Fish - save to completions directory
mkdir -p ~/.config/fish/completions
pdf-to-pptx-tool completion fish > ~/.config/fish/completions/pdf-to-pptx-tool.fish
```

**Benefits:**
- Tab-complete commands: `pdf-to-pptx-tool <TAB>`
- Tab-complete options: `pdf-to-pptx-tool convert --<TAB>`
- Tab-complete file paths automatically

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: "poppler not found" or PDF conversion fails**
```bash
# Symptom
RuntimeError: Failed to convert PDF pages: poppler not found
```

**Solution:**
Install poppler system library:
```bash
# macOS
brew install poppler

# Ubuntu/Debian
sudo apt-get install poppler-utils

# Fedora
sudo dnf install poppler-utils

# Verify installation
pdftoppm -v
```

---

**Issue: "File not found" error**
```bash
# Symptom
✗ Error: Input PDF file not found: document.pdf
```

**Solution:**
- Verify file path is correct
- Use absolute paths if needed
- Check file permissions
```bash
# Check file exists
ls -l document.pdf

# Use absolute path
pdf-to-pptx-tool convert /full/path/to/document.pdf output.pptx
```

---

**Issue: Output file is too large**
```bash
# Symptom
Generated 50MB PPTX from 2MB PDF
```

**Solution:**
Reduce DPI setting:
```bash
# Try lower DPI
pdf-to-pptx-tool convert input.pdf output.pptx --dpi 150

# Or use default 200 DPI
pdf-to-pptx-tool convert input.pdf output.pptx
```

---

**Issue: Images look blurry in PowerPoint**
```bash
# Symptom
Text and diagrams appear pixelated
```

**Solution:**
Increase DPI setting:
```bash
# Use higher quality
pdf-to-pptx-tool convert input.pdf output.pptx --dpi 300

# For print quality
pdf-to-pptx-tool convert input.pdf output.pptx --dpi 600
```

---

**Issue: Conversion is very slow**
```bash
# Symptom
Large PDF takes minutes to convert
```

**Solution:**
1. Use DEBUG logging to see progress:
```bash
pdf-to-pptx-tool -vv convert large.pdf output.pptx
```

2. Consider lower DPI for faster conversion:
```bash
pdf-to-pptx-tool convert large.pdf output.pptx --dpi 150
```

3. Split large PDF into chunks and convert separately

---

**Issue: Permission denied writing output file**
```bash
# Symptom
PermissionError: [Errno 13] Permission denied: 'output.pptx'
```

**Solution:**
- Check directory write permissions
- Use different output location
```bash
# Write to home directory
pdf-to-pptx-tool convert input.pdf ~/output.pptx

# Or create directory first
mkdir -p output-dir
pdf-to-pptx-tool convert input.pdf output-dir/output.pptx
```

### Getting Help

```bash
# Tool help
pdf-to-pptx-tool --help

# Command help
pdf-to-pptx-tool convert --help

# Completion help
pdf-to-pptx-tool completion --help

# Version info
pdf-to-pptx-tool --version
```

### Debug Workflow

When conversion fails, use this debugging workflow:

```bash
# 1. Check file exists and is readable
ls -lh document.pdf
file document.pdf

# 2. Verify poppler is installed
pdftoppm -v

# 3. Try with DEBUG logging
pdf-to-pptx-tool -vv convert document.pdf test.pptx

# 4. Try with lower DPI if memory issues
pdf-to-pptx-tool -vv convert document.pdf test.pptx --dpi 150

# 5. Check Python and dependencies
python --version
pdf-to-pptx-tool --version
```

</details>

## Exit Codes

- `0`: Success - conversion completed successfully
- `1`: Error - file not found, invalid input, conversion failed, or permission denied

## Output Formats

**Default PowerPoint Output:**
- **Format**: Office Open XML (.pptx)
- **Aspect Ratio**: 16:9 widescreen
- **Slide Size**: 10 inches × 5.625 inches
- **Layout**: One full-slide image per PDF page
- **Image Format**: PNG embedded in slides
- **Compatibility**: PowerPoint 2007+ (Windows/Mac/Online)

**Console Output:**
```bash
# Success
✓ Successfully converted document.pdf to slides.pptx

# Error
✗ Error: Input PDF file not found: document.pdf
```

**Logging Output (with -v/-vv/-vvv):**
```bash
[INFO] Starting PDF to PPTX conversion
[INFO] Converting document.pdf to slides.pptx (DPI: 200)
[DEBUG] Input file size: 2.45 MB
[INFO] Converted 10 pages
[DEBUG] Output file size: 12.78 MB
[INFO] Conversion completed successfully
```

## Best Practices

1. **Start with default DPI (200)**: Good balance of quality and file size
2. **Use verbose logging for debugging**: `-vv` shows detailed conversion steps
3. **Test with sample PDFs first**: Verify quality before batch processing
4. **Monitor output file sizes**: Adjust DPI if files are too large
5. **Batch process efficiently**: Use shell loops for multiple files
6. **Enable shell completion**: Speeds up command-line usage
7. **Keep poppler updated**: Ensures compatibility with latest PDF features
8. **Use absolute paths**: Avoids confusion with relative paths
9. **Verify prerequisites**: Check poppler installation before bulk conversions
10. **Handle errors gracefully**: Check exit codes in scripts

## Resources

- **GitHub Repository**: https://github.com/dnvriend/pdf-to-pptx-tool
- **Python Dependencies**:
  - pdf2image (PDF to image conversion)
  - python-pptx (PowerPoint file creation)
  - Pillow (Image processing)
  - Click (CLI framework)
- **System Dependencies**: poppler (PDF rendering engine)
- **Related Tools**:
  - PyPDF2 (PDF text extraction)
  - ReportLab (PDF generation)
  - pandoc (Universal document converter)
