---
name: ebook-extractor
description: Use when user wants to extract text from ebooks (EPUB, MOBI, PDF). Use for converting ebooks to plain text for analysis, processing, or reading. Handles all common ebook formats.
---

# Ebook Text Extractor

## Overview
Extract plain text from EPUB, MOBI, and PDF files using Python scripts. No LLM calls - pure text extraction.

## Supported Formats

| Format | Tool Used | Notes |
|--------|-----------|-------|
| EPUB | `ebooklib` + `BeautifulSoup` | Direct parsing, preserves structure |
| MOBI | Calibre `ebook-convert` | Converts to EPUB first, then extracts |
| PDF | `PyMuPDF` (fitz) | Fast, handles most PDFs well |

## Usage

**Unified extractor (auto-detects format):**
```bash
python3 ~/.claude/skills/ebook-extractor/scripts/extract.py /path/to/book.epub
python3 ~/.claude/skills/ebook-extractor/scripts/extract.py /path/to/book.mobi
python3 ~/.claude/skills/ebook-extractor/scripts/extract.py /path/to/book.pdf
```

**Output options:**
```bash
# To stdout (default)
python3 scripts/extract.py book.epub

# To file
python3 scripts/extract.py book.epub -o output.txt
python3 scripts/extract.py book.epub > output.txt
```

**Format-specific scripts:**
```bash
python3 scripts/extract_epub.py book.epub
python3 scripts/extract_mobi.py book.mobi
python3 scripts/extract_pdf.py book.pdf
```

## Setup

```bash
# One-command setup (installs all dependencies)
~/.claude/skills/ebook-extractor/setup.sh

# Or manually:
pip install -r ~/.claude/skills/ebook-extractor/requirements.txt
brew install calibre  # macOS, for MOBI support
```

## Script Location
`~/.claude/skills/ebook-extractor/scripts/`

## Common Issues

| Problem | Solution |
|---------|----------|
| Missing package | Run `setup.sh` or `pip install -r requirements.txt` |
| MOBI fails | Ensure Calibre is installed: `brew install calibre` |
| PDF garbled | Some PDFs are image-based; OCR needed (not supported) |
