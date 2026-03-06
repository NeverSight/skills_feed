---
name: scientific-figure-assembly
description: Assemble multi-panel scientific figures with panel labels (A, B, C) at publication quality (300 DPI) using R. Use when combining individual plots into journal-ready figures.
allowed-tools: Bash(Rscript *), Write, Read
---

# Scientific Figure Assembly (R-based)

Create publication-ready multi-panel figures using R packages (patchwork, cowplot) with professional panel labels (A, B, C, D) at 300 DPI resolution.

**⚠️ IMPORTANT**: This workflow uses R for figure assembly. For meta-analysis projects, all figures should be generated and assembled in R.

## When to Use

- Combining multiple plots into a single multi-panel figure for publication
- Adding panel labels (A, B, C) to existing figures
- Ensuring figures meet journal requirements (300 DPI minimum)
- Creating consistent figure layouts for manuscripts
- Preparing figures for Nature, Science, Cell, JAMA, Lancet submissions

## Quick Start

Tell me:

1. **Plot objects**: R plot objects (ggplot, forest plots, etc.) OR paths to PNG/JPG files
2. **Layout**: Vertical (stacked), horizontal (side-by-side), or grid (2x2, 2x3, etc.)
3. **Output name**: What to call the final figure
4. **Labels**: Which panel labels to use (default: A, B, C, D...)

I'll create an R script using patchwork or cowplot to assemble the figure with proper spacing and labels.

## R Package Approach (Recommended)

### Method 1: patchwork (For ggplot2 objects)

The simplest and most powerful method for combining ggplot2 objects:

```r
library(ggplot2)
library(patchwork)

# Create or load individual plots
p1 <- ggplot(data1, aes(x, y)) + geom_point() + ggtitle("A. First Panel")
p2 <- ggplot(data2, aes(x, y)) + geom_line() + ggtitle("B. Second Panel")
p3 <- ggplot(data3, aes(x, y)) + geom_bar(stat="identity") + ggtitle("C. Third Panel")

# Combine vertically
combined <- p1 / p2 / p3

# Or combine horizontally
combined <- p1 | p2 | p3

# Or grid layout (2 columns)
combined <- (p1 | p2) / p3

# Export at 300 DPI
ggsave("figures/figure1_combined.png",
       plot = combined,
       width = 10, height = 12, dpi = 300)
```

### Method 2: cowplot (For any R plots)

More flexible, works with base R plots and ggplot2:

```r
library(ggplot2)
library(cowplot)

# Create individual plots
p1 <- ggplot(data1, aes(x, y)) + geom_point()
p2 <- ggplot(data2, aes(x, y)) + geom_line()
p3 <- ggplot(data3, aes(x, y)) + geom_bar(stat="identity")

# Combine with automatic panel labels
combined <- plot_grid(
  p1, p2, p3,
  labels = c("A", "B", "C"),
  label_size = 18,
  ncol = 1,                    # Vertical stack
  rel_heights = c(1, 1, 1)     # Equal heights
)

# Export
ggsave("figures/figure1_combined.png",
       plot = combined,
       width = 10, height = 12, dpi = 300)
```

## Legacy Python Script Template (Not Recommended)

**⚠️ For meta-analysis projects, use R methods above instead.**

If you absolutely need Python for existing PNG files:

```python
#!/usr/bin/env python3
"""Legacy: Assemble multi-panel scientific figure from PNG files."""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

def add_panel_label(img, label, position='top-left',
                   font_size=80, offset=(40, 40),
                   bg_color='white', text_color='black',
                   border=True):
    """
    Add panel label (A, B, C) to image.

    Args:
        img: PIL Image object
        label: Label text (e.g., 'A', 'B', 'C')
        position: 'top-left', 'top-right', 'bottom-left', 'bottom-right'
        font_size: Font size in pixels (80 works well for 3000px wide images)
        offset: (x, y) offset from corner in pixels
        bg_color: Background color for label box
        text_color: Label text color
        border: Whether to draw border around label box
    """
    draw = ImageDraw.Draw(img)

    # Try system fonts (macOS, then Linux)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except:
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", font_size
            )
        except:
            font = ImageFont.load_default()
            print(f"Warning: Using default font for label {label}")

    # Calculate label position
    x, y = offset
    if 'right' in position:
        bbox = draw.textbbox((0, 0), label, font=font)
        text_width = bbox[2] - bbox[0]
        x = img.width - text_width - offset[0]
    if 'bottom' in position:
        bbox = draw.textbbox((0, 0), label, font=font)
        text_height = bbox[3] - bbox[1]
        y = img.height - text_height - offset[1]

    # Draw background box
    bbox = draw.textbbox((x, y), label, font=font)
    padding = 10
    draw.rectangle(
        [bbox[0] - padding, bbox[1] - padding,
         bbox[2] + padding, bbox[3] + padding],
        fill=bg_color,
        outline='black' if border else None,
        width=2 if border else 0
    )

    # Draw text
    draw.text((x, y), label, fill=text_color, font=font)

    return img


def assemble_vertical(input_files, output_file, labels=None,
                     spacing=40, dpi=300):
    """
    Stack images vertically with panel labels.

    Args:
        input_files: List of paths to input images
        output_file: Path for output image
        labels: List of labels (default: A, B, C, ...)
        spacing: Vertical spacing between panels in pixels
        dpi: Output resolution
    """
    if labels is None:
        labels = [chr(65 + i) for i in range(len(input_files))]  # A, B, C, ...

    # Load all images
    images = [Image.open(f) for f in input_files]

    # Add labels
    labeled = [add_panel_label(img, label)
               for img, label in zip(images, labels)]

    # Calculate dimensions
    max_width = max(img.width for img in labeled)
    total_height = sum(img.height for img in labeled) + spacing * (len(labeled) - 1)

    # Create combined image
    combined = Image.new('RGB', (max_width, total_height), 'white')

    # Paste images
    y_offset = 0
    for img in labeled:
        combined.paste(img, (0, y_offset))
        y_offset += img.height + spacing

    # Save with specified DPI
    combined.save(output_file, dpi=(dpi, dpi))
    print(f"✅ Created {output_file}")
    print(f"   Dimensions: {combined.width}×{combined.height} px at {dpi} DPI")

    return output_file


def assemble_horizontal(input_files, output_file, labels=None,
                       spacing=40, dpi=300):
    """Stack images horizontally with panel labels."""
    if labels is None:
        labels = [chr(65 + i) for i in range(len(input_files))]

    images = [Image.open(f) for f in input_files]
    labeled = [add_panel_label(img, label)
               for img, label in zip(images, labels)]

    max_height = max(img.height for img in labeled)
    total_width = sum(img.width for img in labeled) + spacing * (len(labeled) - 1)

    combined = Image.new('RGB', (total_width, max_height), 'white')

    x_offset = 0
    for img in labeled:
        combined.paste(img, (x_offset, 0))
        x_offset += img.width + spacing

    combined.save(output_file, dpi=(dpi, dpi))
    print(f"✅ Created {output_file}")
    print(f"   Dimensions: {combined.width}×{combined.height} px at {dpi} DPI")

    return output_file


def assemble_grid(input_files, output_file, rows, cols,
                 labels=None, spacing=40, dpi=300):
    """
    Arrange images in a grid with panel labels.

    Args:
        rows: Number of rows
        cols: Number of columns
        Other args same as assemble_vertical
    """
    if labels is None:
        labels = [chr(65 + i) for i in range(len(input_files))]

    images = [Image.open(f) for f in input_files]
    labeled = [add_panel_label(img, label)
               for img, label in zip(images, labels)]

    # Calculate cell dimensions (use max from each row/col)
    cell_width = max(img.width for img in labeled)
    cell_height = max(img.height for img in labeled)

    # Total dimensions
    total_width = cell_width * cols + spacing * (cols - 1)
    total_height = cell_height * rows + spacing * (rows - 1)

    combined = Image.new('RGB', (total_width, total_height), 'white')

    # Place images
    for idx, img in enumerate(labeled):
        if idx >= rows * cols:
            break
        row = idx // cols
        col = idx % cols
        x = col * (cell_width + spacing)
        y = row * (cell_height + spacing)
        combined.paste(img, (x, y))

    combined.save(output_file, dpi=(dpi, dpi))
    print(f"✅ Created {output_file}")
    print(f"   Dimensions: {combined.width}×{combined.height} px at {dpi} DPI")

    return output_file


if __name__ == '__main__':
    import sys

    # Example usage
    if len(sys.argv) < 3:
        print("Usage: python assemble_figures.py <output> <layout> <input1> <input2> ...")
        print("  layout: vertical, horizontal, or grid:RxC (e.g., grid:2x2)")
        sys.exit(1)

    output = sys.argv[1]
    layout = sys.argv[2]
    inputs = sys.argv[3:]

    if layout == 'vertical':
        assemble_vertical(inputs, output)
    elif layout == 'horizontal':
        assemble_horizontal(inputs, output)
    elif layout.startswith('grid:'):
        rows, cols = map(int, layout.split(':')[1].split('x'))
        assemble_grid(inputs, output, rows, cols)
    else:
        print(f"Unknown layout: {layout}")
        sys.exit(1)
```

## Common Layouts

### Vertical (Most Common)

Stack plots on top of each other - good for showing progression or related outcomes.

**Example**: Three forest plots (pCR, EFS, OS) stacked vertically

- Panel A: pCR forest plot
- Panel B: EFS forest plot
- Panel C: OS forest plot

### Horizontal

Place plots side-by-side - good for comparisons.

**Example**: Two funnel plots showing publication bias

- Panel A: pCR funnel plot
- Panel B: EFS funnel plot

### Grid (2x2, 2x3, etc.)

Arrange in rows and columns - good for systematic comparisons.

**Example**: 2x2 grid of subgroup analyses

- Panel A: Age subgroup
- Panel B: Sex subgroup
- Panel C: Stage subgroup
- Panel D: Histology subgroup

## R Workflow (Recommended)

### Complete Example: Meta-Analysis Forest Plots

```r
#!/usr/bin/env Rscript
# assemble_forest_plots.R
# Combine multiple forest plots into a single figure

library(meta)
library(metafor)
library(patchwork)

# Set working directory
setwd("/Users/htlin/meta-pipe/06_analysis")

# Load extraction data
data <- read.csv("../05_extraction/extraction.csv")

# --- Create individual forest plots ---

# Plot 1: Pathologic complete response
res_pcr <- metabin(
  event.e = events_pcr_ici,
  n.e = total_ici,
  event.c = events_pcr_control,
  n.c = total_control,
  data = data,
  studlab = study_id,
  sm = "RR",
  method = "MH"
)

# Save as ggplot-compatible object
p1 <- forest(res_pcr, layout = "RevMan5") +
  ggtitle("A. Pathologic Complete Response")

# Plot 2: Event-free survival
res_efs <- metagen(
  TE = log_hr_efs,
  seTE = se_log_hr_efs,
  data = data,
  studlab = study_id,
  sm = "HR"
)

p2 <- forest(res_efs) +
  ggtitle("B. Event-Free Survival")

# Plot 3: Overall survival
res_os <- metagen(
  TE = log_hr_os,
  seTE = se_log_hr_os,
  data = data,
  studlab = study_id,
  sm = "HR"
)

p3 <- forest(res_os) +
  ggtitle("C. Overall Survival")

# --- Combine with patchwork ---

combined <- p1 / p2 / p3 +
  plot_annotation(
    title = "Figure 1. Efficacy Outcomes with ICI vs Control",
    theme = theme(plot.title = element_text(size = 16, face = "bold"))
  )

# Export at 300 DPI
ggsave("../07_manuscript/figures/figure1_efficacy.png",
       plot = combined,
       width = 10,
       height = 14,
       dpi = 300,
       bg = "white")

cat("✅ Created figure1_efficacy.png\n")
cat("   Dimensions: 3000×4200 px at 300 DPI\n")
```

### Using cowplot for More Control

```r
library(cowplot)

# Combine with explicit panel labels and alignment
combined <- plot_grid(
  p1, p2, p3,
  labels = c("A", "B", "C"),
  label_size = 18,
  label_fontface = "bold",
  ncol = 1,
  align = "v",           # Vertical alignment
  axis = "l",            # Align left axis
  rel_heights = c(1, 1, 1)
)

# Add overall title
title <- ggdraw() +
  draw_label(
    "Figure 1. Efficacy Outcomes with ICI vs Control",
    fontface = "bold",
    size = 16,
    x = 0.5,
    hjust = 0.5
  )

# Combine title and plots
final <- plot_grid(
  title,
  combined,
  ncol = 1,
  rel_heights = c(0.1, 1)
)

# Export
ggsave("../07_manuscript/figures/figure1_efficacy.png",
       plot = final,
       width = 10, height = 14, dpi = 300, bg = "white")
```

### Grid Layout (2x2 or 2x3)

```r
library(patchwork)

# 2x2 grid
combined <- (p1 | p2) / (p3 | p4) +
  plot_annotation(tag_levels = "A")

# 2x3 grid
combined <- (p1 | p2 | p3) / (p4 | p5 | p6) +
  plot_annotation(tag_levels = "A")

ggsave("figure_grid.png", width = 14, height = 10, dpi = 300)
```

## Python Workflow (Legacy - For PNG Files Only)

**⚠️ Only use if you have existing PNG files and cannot regenerate in R.**

### Step 1: Verify Input Files

```bash
# Check that all files exist and are PNG/JPG
ls -lh path/to/plots/*.png
```

### Step 2: Create Assembly Script

Use the Python template provided in this skill.

### Step 3: Run Assembly

```bash
# Using uv (recommended for dependency management)
uv run python assemble_figures.py Figure1_Efficacy.png vertical \
    forest_plot_pCR.png \
    forest_plot_EFS.png \
    forest_plot_OS.png

# Or with system Python (requires PIL/Pillow)
python assemble_figures.py Figure1.png grid:2x2 \
    plot1.png plot2.png plot3.png plot4.png
```

### Step 4: Verify Output

```bash
# Check dimensions and file size
ls -lh Figure1_Efficacy.png

# Verify DPI (should show 300x300)
file Figure1_Efficacy.png
```

## Customization Options

### Font Size Adjustment

For different image sizes:

- 3000px wide images: `font_size=80` (default)
- 1500px wide images: `font_size=40`
- 6000px wide images: `font_size=160`

### Label Position

- `position='top-left'` (default)
- `position='top-right'`
- `position='bottom-left'`
- `position='bottom-right'`

### Spacing Between Panels

- Default: `spacing=40` pixels
- Tight spacing: `spacing=20`
- Loose spacing: `spacing=80`

### Label Style

- White background with black border (default, best visibility)
- Transparent background: `bg_color=None, border=False`
- Custom colors: `bg_color='#f0f0f0', text_color='#333333'`

## Journal Requirements

### Nature, Science, Cell

- **Resolution**: 300-600 DPI
- **Format**: TIFF or high-quality PDF preferred, PNG acceptable
- **Width**: 89mm (single column) or 183mm (double column) at final size
- **Font**: Arial, Helvetica, or similar sans-serif
- **Labels**: Bold, 8-10pt at final size

### Lancet, JAMA, NEJM

- **Resolution**: 300 DPI minimum
- **Format**: TIFF, EPS, or PNG
- **Width**: Fit within column width (typically 3-4 inches)
- **Labels**: Clear, high contrast
- **Grayscale**: Must be readable in B&W

## Quality Checklist

Before submitting:

- [ ] All figures at 300 DPI minimum
- [ ] Panel labels (A, B, C) visible and correctly ordered
- [ ] Labels don't obscure important data
- [ ] All panels aligned properly
- [ ] Spacing consistent between panels
- [ ] File size reasonable (<10 MB for PNG)
- [ ] Figures readable when printed at final journal size
- [ ] Color schemes work in grayscale (if required)

## Common Issues & Solutions

**Problem**: Labels too small
**Solution**: Increase `font_size` parameter (try doubling it)

**Problem**: Labels obscure data
**Solution**: Change `position` to different corner or adjust `offset`

**Problem**: DPI too low
**Solution**: Regenerate input plots at higher resolution first, then reassemble

**Problem**: Uneven spacing
**Solution**: Crop input images to remove excess white space before assembly

**Problem**: File too large
**Solution**: Use PNG compression or convert to JPEG (may lose quality)

## Example Use Cases

### Meta-Analysis Figures (R)

```r
# Figure 1: Efficacy outcomes (3 vertical panels)
library(patchwork)

combined <- p_pcr / p_efs / p_os +
  plot_annotation(
    title = "Figure 1. Efficacy Outcomes",
    tag_levels = "A"
  )

ggsave("07_manuscript/figures/figure1_efficacy.png",
       width = 10, height = 14, dpi = 300)

# Figure 2: Safety + Bias (2 vertical panels)
combined <- p_safety / p_funnel +
  plot_annotation(tag_levels = "A")

ggsave("07_manuscript/figures/figure2_safety.png",
       width = 10, height = 10, dpi = 300)

# Figure 3: Subgroup analysis (2x2 grid)
combined <- (p_age | p_sex) / (p_stage | p_histology) +
  plot_annotation(
    title = "Figure 3. Subgroup Analyses",
    tag_levels = "A"
  )

ggsave("07_manuscript/figures/figure3_subgroups.png",
       width = 14, height = 12, dpi = 300)
```

### Legacy Python Examples (Not Recommended)

```bash
# Figure 1: Efficacy outcomes (3 vertical panels)
uv run python assemble.py Figure1_Efficacy.png vertical \
    forest_plot_pCR.png \
    forest_plot_EFS.png \
    forest_plot_OS.png

# Figure 2: Safety + Bias (2 vertical panels)
uv run python assemble.py Figure2_Safety.png vertical \
    forest_plot_SAE.png \
    funnel_plot_pCR.png
```

## Dependencies

### R Packages (Recommended)

```r
# Install from CRAN
install.packages(c("patchwork", "cowplot", "ggplot2"))

# For meta-analysis plots
install.packages(c("meta", "metafor"))
```

### Python (Legacy - Only for PNG Assembly)

```bash
# Install using uv (if needed for legacy workflows)
uv add Pillow

# Or using pip
pip install Pillow
```

## Output Example

### R Output

```
✅ Created figure1_efficacy.png
   Dimensions: 3000×4200 px at 300 DPI
   Size: 2.3 MB
```

The output file will have:

- Professional panel labels (A, B, C) automatically added by patchwork/cowplot
- Consistent spacing between panels
- 300 DPI resolution suitable for publication
- Aligned axes for easy comparison
- Publication-ready theme

### Python Output (Legacy)

```
✅ Created Figure1_Efficacy.png
   Dimensions: 3000×6080 px at 300 DPI
```

The output file will have:

- Professional panel labels (A, B, C) in top-left corners
- Consistent spacing between panels
- 300 DPI resolution suitable for publication
- White background with black border around labels for maximum visibility

## Related Skills

- `/meta-manuscript-assembly` - Complete meta-analysis manuscript preparation
- `/plot-publication` - Create individual publication-ready plots
- `/figure-legends` - Generate comprehensive figure legends

## Pro Tips

### R Workflow Tips

1. **Work in R throughout**: Generate plots AND assemble in R for best results
2. **Use patchwork for ggplot2**: Simplest syntax (`p1 / p2` for vertical)
3. **Use cowplot for mixed plots**: Works with base R and ggplot2
4. **Set theme globally**: Use `theme_set(theme_minimal())` for consistency
5. **Export once at end**: Create all plots, combine, then export (faster)
6. **Check alignment**: Use `align = "v"` and `axis = "l"` in cowplot
7. **Consistent sizes**: Set `base_size` in theme for readable text

### General Tips

1. **Generate high-quality inputs first**: Assembly won't improve low-quality source plots
2. **Label systematically**: A-B-C top-to-bottom or left-to-right
3. **Check in print preview**: Ensure labels readable at final print size
4. **Keep R scripts**: Save R code for reproducibility
5. **Version control figures**: Commit both R scripts and final PNG files
6. **Test on different screens**: Check readability on laptop and printed page

### R Package Resources

When you need help with R packages:

- **CRAN**: https://cran.r-project.org/ (patchwork, cowplot documentation)
- **Tidyverse**: https://www.tidyverse.org/ (ggplot2 reference)
- **R-universe**: https://r-universe.dev/search/ (search all R packages)
- **patchwork guide**: https://patchwork.data-imaginist.com/
- **cowplot guide**: https://wilkelab.org/cowplot/
