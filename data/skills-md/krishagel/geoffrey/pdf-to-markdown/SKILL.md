---
name: pdf-to-markdown
description: Convert PDF to clean Markdown with image content described as text. Use when user wants to convert a PDF to markdown, extract content from PDF, or prepare PDF content for AI tools.
allowed-tools: Read, Bash
version: 1.0.0
---

# PDF to Markdown Converter

Convert PDF files to clean, well-structured Markdown. Tables become markdown tables. Images and graphics are described as text (no image files generated).

## Quick Start

```bash
uv run skills/pdf-to-markdown/scripts/convert_to_markdown.py input.pdf
```

Output: `~/Desktop/{filename}.md`

## Options

| Flag | Description |
|------|-------------|
| `--no-llm` | Skip LLM processing (faster, images become `[Image]` placeholders) |
| `--force-ocr` | Force OCR on all pages (for scanned PDFs) |
| `--page-range "0,5-10"` | Process specific pages only |

## Common Use Cases

### Convert a PDF with default settings
```bash
uv run skills/pdf-to-markdown/scripts/convert_to_markdown.py ~/Documents/report.pdf
```

### Specify output location
```bash
uv run skills/pdf-to-markdown/scripts/convert_to_markdown.py report.pdf ~/Documents/report.md
```

### Fast conversion (no image descriptions)
```bash
uv run skills/pdf-to-markdown/scripts/convert_to_markdown.py --no-llm report.pdf
```

### Scanned PDF (force OCR)
```bash
uv run skills/pdf-to-markdown/scripts/convert_to_markdown.py --force-ocr scanned_doc.pdf
```

### Extract specific pages
```bash
uv run skills/pdf-to-markdown/scripts/convert_to_markdown.py --page-range "0-5" large_report.pdf
```

## Output

- Pure Markdown text (no embedded images)
- Tables converted to Markdown table format
- Images/charts described as text using LLM
- Clean formatting suitable for AI processing

## Requirements

- **GEMINI_API_KEY**: Required for LLM image descriptions (loaded from 1Password)
- Use `--no-llm` flag if you don't have Gemini API access

## First Run Note

The first run downloads ML models (~1-2GB) which are cached at `~/.cache/marker/`. Subsequent runs are faster.

## Technical Details

Uses [Marker](https://github.com/VikParuchuri/marker) library:
- 31k+ GitHub stars
- Best-in-class PDF conversion accuracy
- Surya OCR for 90+ languages
- Gemini LLM integration for image understanding
