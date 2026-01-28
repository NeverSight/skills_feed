---
name: convert-doc
description: |
  Smart Document Pipeline - Context-Efficient Document Handling

  Converts PDF, Word, PowerPoint, Excel to clean markdown.
  Auto-summarizes large documents. Caches for reuse.

  TRIGGERS: convert, konvertera, pdf to markdown, docx to md, pptx

  WHY:
  - PDFs can consume 30+ MB context when read directly
  - Converted markdown is 95-99% smaller
  - Summary versions are 99.9% smaller
  - Cached versions reuse across sessions
---

# Smart Document Pipeline

## Quick Reference

```bash
# Convert document (auto-caches, auto-summarizes if >100KB)
python ~/.claude/lib/document-converter.py "/path/to/file.pdf"

# Force regenerate
python ~/.claude/lib/document-converter.py "/path/to/file.pdf" --force

# List cached documents
python ~/.claude/lib/document-converter.py --list

# Cleanup old cache (>1 week)
python ~/.claude/lib/document-converter.py --cleanup
```

## Supported Formats

| Format | Extension | Tool | Notes |
|--------|-----------|------|-------|
| PDF | .pdf | PyMuPDF | Text extraction, page-by-page |
| Word | .docx, .doc | pandoc/python-docx | Full markdown |
| PowerPoint | .pptx, .ppt | python-pptx | Slide-by-slide with notes |
| Excel | .xlsx, .xls | openpyxl | Tables as markdown |
| RTF | .rtf | pandoc | Rich text |

## Output Structure

```json
{
  "cache_path": "/path/to/cached/file.md",
  "summary_path": "/path/to/cached/file_summary.md",  // if >100KB
  "from_cache": false,
  "original_size": 26744198,
  "converted_size": 129844,
  "summary_size": 30638,
  "savings_percent": 99.5,
  "recommendation": "summary"  // "summary" or "full"
}
```

## Auto-Summary

Documents >100KB automatically get a summary version:

| Version | Purpose | Size Target |
|---------|---------|-------------|
| Full | Complete content | As converted |
| Summary | Quick overview | ~30KB |

The summary preserves:
- All headers and structure
- First portion of each section
- Metadata and source reference

## Automatic Integration

The `smart-read-interceptor` hook automatically triggers when you read:
- PDF, Word, PowerPoint, Excel files
- Any file >200KB

It will suggest:
1. **Use summary** - If summary exists (best for overview)
2. **Use cache** - If full cached version exists
3. **Convert first** - If no cache exists
4. **Delegate** - For very large files, use subagent

## Subagent Delegation Pattern

For very large documents, delegate to isolated context:

```
Task(
  subagent_type="Explore",
  prompt="Read and summarize key points from: /path/to/large-file.pdf.
         Focus on: [specific topics]. Max 500 words summary."
)
```

This keeps the large content OUT of main context.

## Cache Location

```
~/.claude/cache/documents/
├── filename_hash.md           # Full converted version
├── filename_hash_summary.md   # Summary (if >100KB)
└── ...
```

Cache expires after 1 week. Run `--cleanup` to remove old files.

## Real-World Results

| Document | Original | Converted | Summary | Savings |
|----------|----------|-----------|---------|---------|
| Google AI Guide (PDF) | 26.7 MB | 127 KB | 30 KB | 99.9% |
| Debatt (Word) | 206 KB | 5.4 KB | - | 97% |
| Övning (PowerPoint) | 7.2 MB | 3.1 KB | - | 99.96% |

## Workflow Examples

### Reading a PDF for research
```
1. User asks to analyze a PDF
2. Hook detects: "📄 DOCUMENT FILE: .PDF"
3. Convert: python ~/.claude/lib/document-converter.py "file.pdf"
4. Read the summary for overview
5. Read specific sections from full version if needed
```

### Processing multiple documents
```
1. Convert all documents first (batch):
   for f in *.pdf; do python ~/.claude/lib/document-converter.py "$f"; done

2. Read summaries in main context
3. Delegate deep analysis to subagents
```
