---
name: html-to-pptx
description: "Convert HTML to PowerPoint (PPTX) with excellent Hebrew/RTL support. Use when the user asks to 'convert HTML to PowerPoint', 'create presentation from HTML', 'generate PPTX', 'make slides from HTML', or needs to create PowerPoint presentations programmatically."
version: "1.0.0"
author: aviz85
tags:
  - powerpoint
  - pptx
  - conversion
  - html
  - rtl
  - hebrew
  - presentations
---

# HTML to PowerPoint Converter

Convert HTML to PowerPoint (.pptx) with excellent Hebrew/RTL support using PptxGenJS.

## Setup (One-time)

```bash
cd ~/.claude/skills/html-to-pptx && npm install
```

## Quick Usage

### Basic conversion:
```bash
node ~/.claude/skills/html-to-pptx/scripts/html-to-pptx.js input.html output.pptx
```

### Hebrew document with RTL:
```bash
node ~/.claude/skills/html-to-pptx/scripts/html-to-pptx.js hebrew.html presentation.pptx --rtl
```

### Convert URL to PowerPoint:
```bash
node ~/.claude/skills/html-to-pptx/scripts/html-to-pptx.js https://example.com slides.pptx
```

### Complex HTML as images (pixel-perfect):
```bash
node ~/.claude/skills/html-to-pptx/scripts/html-to-pptx.js complex.html slides.pptx --mode=image
```

## Conversion Modes

| Mode | Description | Best For |
|------|-------------|----------|
| `text` | Parse HTML, create native PPTX elements | Simple HTML, editable text |
| `image` | Screenshot HTML, embed as images | Complex layouts, exact rendering |
| `auto` | Auto-detect best mode | Default |

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--mode=<mode>` | text, image, auto | auto |
| `--rtl` | Force RTL for Hebrew/Arabic | auto-detect |
| `--title=<title>` | Presentation title | auto |
| `--author=<author>` | Author name | AVIZ |
| `--layout=<layout>` | LAYOUT_16x9, LAYOUT_4x3 | LAYOUT_16x9 |
| `--font=<font>` | Default font | Heebo (Hebrew) / Arial |
| `--font-size=<size>` | Font size in points | 18 |
| `--background=<color>` | Background color (hex) | - |
| `--slide-per=<selector>` | Split slides by CSS selector | - |
| `--wait=<ms>` | Wait for rendering (image mode) | 2000 |

## Examples

### Hebrew presentation:
```bash
node ~/.claude/skills/html-to-pptx/scripts/html-to-pptx.js hebrew.html slides.pptx --rtl --font=Heebo
```

### Split by sections:
```bash
node ~/.claude/skills/html-to-pptx/scripts/html-to-pptx.js doc.html slides.pptx --slide-per=section
```

### Custom styling:
```bash
node ~/.claude/skills/html-to-pptx/scripts/html-to-pptx.js doc.html slides.pptx --font=David --font-size=24 --background=F5F5F5
```

### Pipe HTML:
```bash
echo "<h1>שלום עולם</h1>" | node ~/.claude/skills/html-to-pptx/scripts/html-to-pptx.js - output.pptx --rtl
```

## Hebrew Best Practices

1. Use `<html lang="he" dir="rtl">` in HTML
2. Always add `--rtl` flag
3. Use Hebrew-supporting fonts: Heebo, David, Noto Sans Hebrew
4. For complex layouts, use `--mode=image` for pixel-perfect results

## Slide Structure

The converter auto-detects slide boundaries:
1. `<section>` elements
2. `<article>` elements
3. `.slide` class
4. `<hr>` elements

Or use `--slide-per=".my-slide"` for custom selectors.
