---
name: html-to-pdf
description: Convert HTML to PDF with pixel-perfect rendering and excellent Hebrew/RTL support. Use when the user asks to 'convert HTML to PDF', 'generate PDF from HTML', 'create PDF from webpage', 'export to PDF', or needs PDF generation with Hebrew text support.
version: "1.0.0"
author: aviz85
tags:
  - pdf
  - conversion
  - html
  - rtl
  - hebrew
allowed-tools: Bash, Read, Write, Glob
---

# HTML to PDF Converter

Pixel-perfect HTML to PDF conversion using Puppeteer (Chrome headless). Provides excellent support for Hebrew, Arabic, and other RTL languages with automatic direction detection.

## Why Puppeteer?

- **Pixel-perfect rendering**: Uses actual Chrome engine
- **Full CSS3/HTML5 support**: Flexbox, Grid, custom fonts, backgrounds
- **JavaScript execution**: Renders dynamic content
- **Automatic RTL detection**: Detects Hebrew/Arabic and sets direction
- **Web font support**: Loads custom fonts properly

## CRITICAL: Fit Content to Single Page

**Backgrounds on `html` or `body` cause extra pages!** Put backgrounds on a container element instead:

```css
@page { size: A4; margin: 0; }

html, body {
  width: 210mm;
  height: 297mm;
  margin: 0;
  padding: 0;
  overflow: hidden;
  /* NO background here! */
}

.container {
  width: 100%;
  height: 100%;
  padding: 20mm;
  box-sizing: border-box;
  background: linear-gradient(...); /* Background goes HERE */
}
```

**Common causes of extra pages:**
1. **Background on html/body** - always put on `.container` instead
2. Content overflow - use `overflow: hidden`
3. Margins/padding pushing content out

**Tips:**
- Use `--scale=0.75 --margin=0` if content still overflows
- For landscape: use `--landscape`

## Setup (One-time)

Before first use, install dependencies:

```bash
cd ~/.claude/skills/html-to-pdf && npm install
```

## Quick Usage

### Convert local HTML file:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js input.html output.pdf
```

### Convert URL to PDF:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js https://example.com page.pdf
```

### Hebrew document with forced RTL:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js hebrew.html hebrew.pdf --rtl
```

### Pipe HTML content:
```bash
echo "<h1>שלום עולם</h1>" | node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js - output.pdf --rtl
```

## Options Reference

| Option | Description | Default |
|--------|-------------|---------|
| `--format=<format>` | Page format: A4, Letter, Legal, A3, A5 | A4 |
| `--landscape` | Use landscape orientation | false |
| `--margin=<value>` | Set all margins (e.g., "20mm", "1in") | 20mm |
| `--margin-top=<value>` | Top margin | 20mm |
| `--margin-right=<value>` | Right margin | 20mm |
| `--margin-bottom=<value>` | Bottom margin | 20mm |
| `--margin-left=<value>` | Left margin | 20mm |
| `--scale=<number>` | Scale factor 0.1-2.0 | 1 |
| `--background` | Print background graphics | true |
| `--no-background` | Don't print backgrounds | - |
| `--header=<html>` | Header HTML template | - |
| `--footer=<html>` | Footer HTML template | - |
| `--wait=<ms>` | Wait time for fonts/JS | 1000 |
| `--rtl` | Force RTL direction | auto-detect |

## Examples

### Basic conversion:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js report.html report.pdf
```

### Letter format with custom margins:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js doc.html doc.pdf --format=Letter --margin=1in
```

### Hebrew invoice:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js invoice-he.html invoice.pdf --rtl
```

### Landscape presentation:
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js slides.html slides.pdf --landscape --format=A4
```

### No margins (full bleed):
```bash
node ~/.claude/skills/html-to-pdf/scripts/html-to-pdf.js poster.html poster.pdf --margin=0
```

## Hebrew/RTL Best Practices

For best Hebrew rendering in your HTML:

1. **Set lang attribute**: `<html lang="he" dir="rtl">`
2. **Use UTF-8**: `<meta charset="UTF-8">`
3. **CSS direction**: Add `direction: rtl; text-align: right;` to body
4. **Fonts**: Use web fonts that support Hebrew (Noto Sans Hebrew, Heebo, Assistant)

### Example Hebrew HTML structure (single-page):
```html
<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
  <meta charset="UTF-8">
  <link href="https://fonts.googleapis.com/css2?family=Heebo:wght@400;700&display=swap" rel="stylesheet">
  <style>
    @page { size: A4; margin: 0; }
    html, body {
      width: 210mm;
      height: 297mm;
      margin: 0;
      padding: 0;
      overflow: hidden;
    }
    .container {
      width: 100%;
      height: 100%;
      padding: 20mm;
      box-sizing: border-box;
      font-family: 'Heebo', sans-serif;
      direction: rtl;
      text-align: right;
      background: #f5f5f5; /* Background on container, NOT body */
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>שלום עולם</h1>
    <p>זהו מסמך בעברית</p>
  </div>
</body>
</html>
```

## Troubleshooting

### Fonts not rendering correctly
- Add `--wait=2000` for more font loading time
- Ensure fonts are loaded via `@font-face` or Google Fonts

### Hebrew appearing left-to-right
- Use `--rtl` flag to force RTL direction
- Add `dir="rtl"` to your HTML element

### Page breaks not working
Use CSS page-break properties:
```css
.page-break { page-break-after: always; }
.no-break { page-break-inside: avoid; }
```

### Backgrounds not showing
- Ensure `--background` is set (default is true)
- Use `--no-background` only if you want to exclude backgrounds

## Technical Notes

- Uses Puppeteer with Chrome headless for rendering
- Waits for `networkidle0` to ensure all resources load
- Automatically waits for `document.fonts.ready`
- Supports `@page` CSS rules for print styling
- Device scale factor set to 2 for crisp rendering
