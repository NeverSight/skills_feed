---
name: slidev-export
description: Export Slidev presentations to PDF, PPTX, and PNG. Use this skill for sharing, printing, and archiving presentations.
---

# Exporting Slidev Presentations

This skill covers all export options in Slidev, including PDF, PPTX, PNG, and Markdown exports with various configuration options.

## When to Use This Skill

- Sharing presentations without running Slidev
- Creating PDF handouts
- Archiving presentations
- Printing slides
- Converting to PowerPoint

## Export Methods

### Browser Exporter (Recommended)

Since v0.50.0, use the built-in browser exporter:

1. Run your presentation: `npm run dev`
2. Open the Export panel from navigation bar
3. Or navigate to: `http://localhost:3030/export`
4. Choose format and options
5. Click Export

### CLI Export

Requires `playwright-chromium`:

```bash
npm install -D playwright-chromium
```

Then:
```bash
npx slidev export
```

## Export Formats

### PDF Export

**Browser Method**:
1. Open `/export`
2. Select "PDF"
3. Configure options
4. Download

**CLI Method**:
```bash
npx slidev export
```

Output: `./slides-export.pdf`

### PPTX Export

**Browser Method**:
1. Open `/export`
2. Select "PPTX"
3. Download

**CLI Method**:
```bash
npx slidev export --format pptx
```

Output: `./slides-export.pptx`

**Note**: Slides exported as images, presenter notes included.

### PNG Export

**CLI Method**:
```bash
npx slidev export --format png
```

Output: Individual PNG files in `./slides-export/` directory.

### Markdown Export

```bash
npx slidev export --format md
```

Compiles Markdown with embedded PNG images.

## CLI Options

### Basic Options

| Option | Description |
|--------|-------------|
| `--format` | Export format: `pdf`, `pptx`, `png`, `md` |
| `--output` | Output file/directory name |
| `--dark` | Export in dark mode |
| `--with-clicks` | Export each click as separate page |
| `--range` | Export specific slides |

### Examples

**Custom output name**:
```bash
npx slidev export --output my-presentation
```

**Dark mode export**:
```bash
npx slidev export --dark
```

**Export with clicks**:
```bash
npx slidev export --with-clicks
```

Creates separate pages for each animation step.

**Specific slides**:
```bash
npx slidev export --range 1,4-5,8
```

Exports slides 1, 4, 5, and 8.

## Advanced Options

### Timeout Settings

For complex slides with animations:

```bash
npx slidev export --timeout 60000
```

Increases timeout to 60 seconds.

### Wait for Content

```bash
npx slidev export --wait 10000
```

Waits 10 seconds before starting export.

### Page Loading Strategy

```bash
npx slidev export --wait-until networkidle
```

Options: `none`, `load`, `domcontentloaded`, `networkidle`

### Table of Contents

```bash
npx slidev export --with-toc
```

Generates PDF outline with slide titles.

### Transparent Background (PNG)

```bash
npx slidev export --format png --omit-background
```

Removes default white background.

## Configuration in Frontmatter

### Export Filename

```yaml
---
exportFilename: my-awesome-presentation
---
```

### Download Button

```yaml
---
download: true
---
```

Shows download button in presentation.

### Export with Source

```yaml
---
download: 'https://example.com/slides.pdf'
---
```

Links to pre-generated PDF.

## Handling Click Animations

### Without --with-clicks

Only final state of each slide exported.

### With --with-clicks

Each click step becomes a separate page:
- Slide 1, Click 0 → Page 1
- Slide 1, Click 1 → Page 2
- Slide 1, Click 2 → Page 3
- Slide 2, Click 0 → Page 4
- etc.

### Recommended for Handouts

Use `--with-clicks` for handouts so readers see progression.

## Export Quality

### PDF Resolution

```bash
npx slidev export --scale 2
```

Higher scale = higher quality (and larger file).

### PNG Resolution

```bash
npx slidev export --format png --scale 2
```

## Package.json Scripts

Add convenient scripts:

```json
{
  "scripts": {
    "dev": "slidev --open",
    "build": "slidev build",
    "export": "slidev export",
    "export:pdf": "slidev export --format pdf",
    "export:pptx": "slidev export --format pptx",
    "export:png": "slidev export --format png",
    "export:dark": "slidev export --dark"
  }
}
```

## Handling Export Issues

### Fonts Not Rendering

1. Use web fonts (Google Fonts)
2. Or embed fonts in styles

### Code Not Highlighting

1. Ensure Shiki loads before export
2. Use `--wait` option

### Images Missing

1. Use absolute URLs or
2. Place in `public/` directory

### Animations Broken

Export doesn't include animations.
Use `--with-clicks` to capture states.

### Timeout Errors

```bash
npx slidev export --timeout 120000 --wait 5000
```

### Memory Issues

For large presentations:
```bash
NODE_OPTIONS="--max-old-space-size=4096" npx slidev export
```

## Export vs Build

| | Export | Build |
|---|--------|-------|
| Output | PDF/PPTX/PNG | Static website |
| Interactive | No | Yes |
| Animations | Static captures | Working |
| Size | Smaller | Larger |
| Sharing | Email/Drive | Web hosting |

## Best Practices

### 1. Test Export Early

Don't wait until presentation day:
```bash
npm run export
```

### 2. Review PDF Thoroughly

Check:
- All slides included
- Code readable
- Images appear
- Colors correct

### 3. Use Consistent Aspect Ratio

Standard is 16:9. Don't change mid-presentation.

### 4. Simplify for Export

Some features don't export well:
- Videos → Use screenshots
- iframes → Use screenshots
- Complex animations → Simplify

### 5. Include Speaker Notes in PPTX

PPTX export includes notes automatically.

### 6. Version Your Exports

```bash
npx slidev export --output presentation-v1.2
```

## Export Workflow

### For Conference Submission

```bash
# High-quality PDF
npx slidev export --with-toc --scale 2
```

### For Handouts

```bash
# Include all click states
npx slidev export --with-clicks
```

### For Social Media

```bash
# Individual images
npx slidev export --format png
```

### For Archiving

```bash
# Multiple formats
npm run export:pdf
npm run export:pptx
npm run export:png
```

## Output Format

When exporting:

```bash
# EXPORT COMMAND:
npx slidev export [options]

# OPTIONS USED:
--format [pdf|pptx|png|md]
--output [filename]
--with-clicks (if needed)
--dark (if needed)
--range [slide numbers]
--timeout [ms]
--wait [ms]
```

**CHECKLIST BEFORE EXPORT:**
- [ ] All slides render correctly
- [ ] Code blocks are readable
- [ ] Images load properly
- [ ] Fonts are correct
- [ ] Test export command works

**OUTPUT FILES:**
- PDF: ./[name].pdf
- PPTX: ./[name].pptx
- PNG: ./[name]/
