---
name: pdf-to-markdown
description: Convert entire PDF documents to clean, structured Markdown for full context loading. Use this skill when the user wants to extract ALL text from a PDF into context (not grep/search), when discussing or analyzing PDF content in full, when the user mentions "load the whole PDF", "bring the PDF into context", "read the entire PDF", or when partial extraction/grepping would miss important context. This is the preferred method for PDF text extraction over page-by-page or grep approaches.
---

# PDF to Markdown Converter

Extract complete PDF content as structured Markdown using IBM Docling AI, preserving:
- Headers (detected by font size, converted to # tags)
- Bold, italic, monospace formatting
- Tables (high-accuracy extraction using TableFormer AI model)
- Lists (ordered and unordered)
- Multi-column layouts (correct reading order)
- Code blocks
- **Images** (extracted and copied next to output with relative paths)

## When to Use This Skill

**USE THIS** when:
- User wants the "whole PDF" or "entire document" in context
- Analyzing, summarizing, or discussing PDF content
- User says "load", "read", "bring in", "extract" a PDF
- Grepping/searching would miss context or structure
- PDF has tables, formatting, or structure to preserve

## Environment Setup

This skill uses a dedicated virtual environment at `~/.claude/skills/pdf-to-markdown/.venv/` to avoid polluting the user's working directory.

### First-Time Setup (if .venv doesn't exist)
```bash
cd ~/.claude/skills/pdf-to-markdown && uv venv .venv && uv pip install --python .venv/bin/python pymupdf docling docling-core
```

### Verify Installation
```bash
~/.claude/skills/pdf-to-markdown/.venv/bin/python -c "import pymupdf; import docling; import docling_core; print('OK')"
```

## Quick Start

```bash
# Convert PDF to markdown (always extracts images)
~/.claude/skills/pdf-to-markdown/.venv/bin/python ~/.claude/skills/pdf-to-markdown/scripts/pdf_to_md.py document.pdf

# Output: document.md + images/ folder (next to the .md file)
```

## Standard Workflow

When user provides a PDF and wants full content in context:

### Step 1: Ensure the skill venv exists
```bash
test -d ~/.claude/skills/pdf-to-markdown/.venv || (cd ~/.claude/skills/pdf-to-markdown && uv venv .venv && uv pip install --python .venv/bin/python pymupdf docling docling-core)
```

### Step 2: Convert PDF to Markdown
```bash
~/.claude/skills/pdf-to-markdown/.venv/bin/python ~/.claude/skills/pdf-to-markdown/scripts/pdf_to_md.py "/path/to/document.pdf"
```

### Step 3: Read the output
```bash
# Output is written to document.md in the same directory as the PDF
cat /path/to/document.md
```

## Caching

PDFs are **aggressively cached** to avoid re-processing. First extraction is slow (~1 sec/page), every subsequent request is instant.

### How It Works
- **Cache location**: `~/.cache/pdf-to-markdown/<cache_key>/`
- **Cache key**: Based on file content hash
- **Invalidation**: Cache is invalidated when:
  - Source PDF is modified (size or mtime changes)
  - Extractor version changes (automatic re-extraction)
  - Explicitly cleared with `--clear-cache` or `--clear-all-cache`

### Cache Commands
```bash
# Clear cache for a specific PDF
~/.claude/skills/pdf-to-markdown/.venv/bin/python ~/.claude/skills/pdf-to-markdown/scripts/pdf_to_md.py document.pdf --clear-cache

# Clear entire cache
~/.claude/skills/pdf-to-markdown/.venv/bin/python ~/.claude/skills/pdf-to-markdown/scripts/pdf_to_md.py --clear-all-cache

# Show cache statistics
~/.claude/skills/pdf-to-markdown/.venv/bin/python ~/.claude/skills/pdf-to-markdown/scripts/pdf_to_md.py --cache-stats
```

### Cache Contents
```
~/.cache/pdf-to-markdown/<cache_key>/
├── metadata.json    # source path, mtime, size, total_pages
├── full_output.md   # cached full markdown
└── images/          # extracted images
```

## Image Handling

Images are always extracted. They are:
- **Cached** in `~/.cache/pdf-to-markdown/<cache_key>/images/`
- **Copied** to `images/` folder next to the output `.md` file
- **Referenced** in the markdown with relative paths (`images/filename.png`)
- **Summarized** in a table at the end of the document

### Auto-View Behavior for Images

**IMPORTANT:** When the extracted markdown contains image references like:
```
**[Image: figure_1.png (1200x800, 125.3KB)]**
```

And the user asks about something that might be visual (charts, graphs, diagrams, figures, screenshots, layouts, designs, plots, illustrations), **automatically use the Read tool** to view the relevant image file(s) before answering. Don't ask the user - just look at it.

**Examples of when to auto-view images:**
- User: "What does the chart on page 3 show?" → Read the image file
- User: "Summarize the figures in this paper" → Read all image files
- User: "What's in the diagram?" → Read the image file
- User: "Describe the architecture shown" → Read the image file
- User: "What are the results?" (and there's a results figure) → Read it

## Output Format

The markdown output includes:

### Header (metadata)
```yaml
---
source: document.pdf
total_pages: 42
extracted_at: 2025-01-15T10:30:00
from_cache: true
images_dir: images
---
```

### Content with image references
```markdown
# Main Title

## Section Header

Regular paragraph text with **bold**, *italic*, and `code` formatting.

![Figure 1](images/figure_1.png)

**[Image: figure_1.png (800x600, 45.2KB)]**

| Column A | Column B |
|----------|----------|
| Data 1   | Data 2   |
```

### Image summary table (at end)
```markdown
---

## Extracted Images

| # | File | Dimensions | Size |
|---|------|------------|------|
| 1 | figure_1.png | 800x600 | 45.2KB |
| 2 | chart_2.png | 1200x800 | 89.1KB |
```

## Script Reference

Location: `~/.claude/skills/pdf-to-markdown/scripts/pdf_to_md.py`

```
Usage: pdf_to_md.py <input.pdf> [output.md] [options]

Options:
  --no-progress     Disable progress indicator

Cache Options:
  --clear-cache        Clear cache for this PDF and re-extract
  --clear-all-cache    Clear entire cache directory and exit
  --cache-stats        Show cache statistics and exit
```

## Performance

- **First extraction**: ~1 second per page (Docling AI processing)
- **First run**: Downloads AI models (~500MB one-time)
- **Cached extraction**: Instant
- **High-resolution images**: 4x default resolution for crisp output

## Troubleshooting

### "No module named docling" or venv doesn't exist
Recreate the skill's virtual environment:
```bash
cd ~/.claude/skills/pdf-to-markdown && rm -rf .venv && uv venv .venv && uv pip install --python .venv/bin/python pymupdf docling docling-core
```

### Poor extraction quality
For scanned PDFs, ensure Tesseract OCR is installed: `brew install tesseract`

### Tables not formatting correctly
This skill uses IBM's TableFormer AI model which has ~93.6% accuracy on complex tables. If tables are still garbled, the PDF may have unusual formatting.
