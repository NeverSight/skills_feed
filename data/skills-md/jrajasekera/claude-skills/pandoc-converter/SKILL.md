---
name: pandoc-converter
description: Convert documents between formats using Pandoc. Use when the user asks to convert files between formats like markdown, docx, html, pdf, latex, epub, rtf, csv, xlsx, or pptx. Triggers on requests like "convert this to Word", "export as PDF", "turn this markdown into HTML", or "convert the CSV to a table".
---

# Pandoc Converter

Convert documents between common formats using Pandoc.

## Quick Start

```bash
# Basic conversion (format auto-detected from extensions)
python scripts/convert.py input.md output.docx

# Specify output format only
python scripts/convert.py document.md --to html

# Check if Pandoc is installed
python scripts/convert.py --check

# List supported formats
python scripts/convert.py --formats
```

## Supported Formats

**Document formats (read/write):** markdown, html, docx, latex, epub, rtf, pptx, pdf  
**Data formats (read only):** csv, tsv, xlsx  
**Markdown variants:** gfm (GitHub), commonmark

For detailed compatibility, see `references/format-compatibility.md`.

## Common Conversions

| From | To | Command |
|------|-----|---------|
| Markdown | Word | `python scripts/convert.py doc.md doc.docx` |
| Markdown | PDF | `python scripts/convert.py doc.md doc.pdf` |
| Markdown | HTML | `python scripts/convert.py doc.md doc.html` |
| Word | Markdown | `python scripts/convert.py doc.docx doc.md` |
| CSV | HTML table | `python scripts/convert.py data.csv data.html` |
| LaTeX | PDF | `python scripts/convert.py paper.tex paper.pdf` |

## Options

| Option | Description |
|--------|-------------|
| `--from <fmt>` | Override input format detection |
| `--to <fmt>` | Specify output format (if no output file) |
| `--standalone` | Include document headers/footers |
| `--toc` | Add table of contents |
| `--pdf-engine <eng>` | PDF engine: pdflatex, xelatex, lualatex |

Additional Pandoc options pass through directly.

## Workflow

1. **Check installation:** Run `python scripts/convert.py --check`
2. **If not installed:** Follow the installation instructions provided
3. **Convert:** Run the conversion with input and output files
4. **Present result:** Provide the converted file to the user

## Installation (if needed)

The script provides installation guidance, but here's a summary:

```bash
# macOS
brew install pandoc

# Ubuntu/Debian  
sudo apt-get install pandoc

# For PDF output, also install LaTeX:
# macOS: brew install --cask mactex-no-gui
# Ubuntu: sudo apt-get install texlive-xetex
```

## Limitations

- **CSV/TSV/XLSX:** Input only (converts to tables in other formats)
- **PDF output:** Requires LaTeX installation
- **PPTX:** Text extraction works; complex layouts may simplify
- **Complex formatting:** Some features may not transfer between formats
