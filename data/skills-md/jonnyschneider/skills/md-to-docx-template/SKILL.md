---
name: md-to-docx-template
description: Convert markdown to beautifully styled Word documents using custom templates. Supports branded fonts, colors, and table styling. Extract styles from existing docs or generate fresh templates.
---

# Markdown to DOCX with Templates

Convert markdown to professionally styled Word documents. Not plain exports — beautiful, branded documents with your fonts, colors, and table styling applied automatically.

## When to Use

- User wants to convert markdown to Word/DOCX
- User needs a branded document from markdown source
- User asks about exporting markdown with styling
- User mentions "md to docx", "markdown to word", or similar

## Prerequisites

- `pandoc` installed (`brew install pandoc` on macOS)
- Python 3.8+ with packages: `python-docx`, `lxml`, `click`, `pyyaml`

## Installation

Clone this skill's scripts to your preferred location:

```bash
git clone https://github.com/jonnyschneider/skills.git
cd skills/skills/md-to-docx-template
pip install python-docx lxml click pyyaml
```

## Quick Conversion

```bash
./md-to-docx.py input.md -o output.docx
```

## With Custom Template

### Option A: Generate template with specific fonts/colors

```bash
./create-reference-template.py template.docx \
  --font-body "DM Sans" \
  --font-heading "DM Sans" \
  --accent-color "0D494D" \
  --heading-color "0D494D"

./md-to-docx.py input.md -o output.docx --template template.docx
```

### Option B: Extract styles from existing branded document

```bash
# Full pipeline for best results:
./extract-styles.py source-branded.docx template.docx
./md-to-docx.py input.md -o output.docx --template template.docx --no-fix-indent
./apply-template-styles.py template.docx output.docx
./fix-table-headers.py output.docx
```

## Multi-file Documents

Create a `manifest.yaml`:

```yaml
template: template.docx
output: final-document.docx
sections:
  - 01-intro.md
  - 02-content.md
  - 03-conclusion.md
```

Then run:

```bash
./md-to-docx.py manifest.yaml --open
```

## Key Options

| Option | Description |
|--------|-------------|
| `-o, --output` | Output DOCX path |
| `--template` | Custom reference template |
| `--toc` | Generate table of contents |
| `--open` | Open after building |
| `--no-fix-indent` | Skip list indent fix (use with extract pipeline) |

## Template Options

| Option | Description |
|--------|-------------|
| `--font-body` | Body text font (default: Calibri) |
| `--font-heading` | Heading font (default: Calibri) |
| `--font-mono` | Code font (default: Consolas) |
| `--accent-color` | Table header color (hex, default: 4472C4) |
| `--heading-color` | Heading text color (hex, default: 000000) |

## Limitations

- Custom fonts must be installed on target machines
- Complex tables may not render perfectly
- SVG images require `rsvg-convert`
- Some pandoc quirks require post-processing scripts
