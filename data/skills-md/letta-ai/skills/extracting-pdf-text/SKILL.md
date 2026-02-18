---
name: extracting-pdf-text
description: Extract text from PDFs for LLM consumption. Use when processing PDFs for RAG, document analysis, or text extraction. Supports API services (Mistral OCR) and local tools (PyMuPDF, pdfplumber). Handles text-based PDFs, tables, and scanned documents with OCR.
---

# Extracting PDF Text for LLMs

This skill provides tools and guidance for extracting text from PDFs in formats suitable for language model consumption.

## Quick Decision Guide

| PDF Type | Best Approach | Script |
|----------|--------------|--------|
| Simple text PDF | PyMuPDF | `scripts/extract_pymupdf.py` |
| PDF with tables | pdfplumber | `scripts/extract_pdfplumber.py` |
| Scanned/image PDF (local) | pytesseract | `scripts/extract_with_ocr.py` |
| Complex layout, highest accuracy | Mistral OCR API | `scripts/extract_mistral_ocr.py` |
| End-to-end RAG pipeline | marker-pdf | `pip install marker-pdf` |

## Recommended Workflow

1. **Try PyMuPDF first** - fastest, handles most text-based PDFs well
2. **If tables are mangled** - switch to pdfplumber
3. **If scanned/image-based** - use Mistral OCR API (best accuracy) or local OCR (free but slower)

## Local Extraction (No API Required)

### PyMuPDF - Fast General Extraction

Best for: Text-heavy PDFs, speed-critical workflows, basic structure preservation.

```bash
uv run scripts/extract_pymupdf.py input.pdf output.md
```

The script outputs markdown with preserved headings and paragraphs. For LLM-optimized output, it uses `pymupdf4llm` which formats text for RAG systems.

### pdfplumber - Table Extraction

Best for: PDFs with tables, financial documents, structured data.

```bash
uv run scripts/extract_pdfplumber.py input.pdf output.md
```

Tables are converted to markdown format. Note: pdfplumber works best on machine-generated PDFs, not scanned documents.

### Local OCR - Scanned Documents

Best for: Scanned PDFs when API access is unavailable.

```bash
uv run scripts/extract_with_ocr.py input.pdf output.txt
```

Requires: `pytesseract`, `pdf2image`, and Tesseract installed (`brew install tesseract` on macOS).

## API-Based Extraction

### Mistral OCR API

Best for: Complex layouts, scanned documents, highest accuracy, multilingual content, math formulas.

**Pricing**: ~1000 pages per dollar (very cost-effective)

```bash
export MISTRAL_API_KEY="your-key"
uv run scripts/extract_mistral_ocr.py input.pdf output.md
```

Features:
- Outputs clean markdown
- Preserves document structure (headings, lists, tables)
- Handles images, math equations, multilingual text
- 95%+ accuracy on complex documents

For detailed API options and other services, see [references/api-services.md](references/api-services.md).

## Output Format Recommendations

For LLM consumption, markdown is preferred:
- Preserves semantic structure (headings become context boundaries)
- Tables remain readable
- Compatible with most RAG chunking strategies

For detailed comparisons of local tools, see [references/local-tools.md](references/local-tools.md).
