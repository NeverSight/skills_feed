---
name: read-bin-docs
description: Straightforward text extraction from document files (text-based PDF only for now, no OCR or docx). Use when you just need to read/extract text from binary documents.
---

# Doc Formats

## Quick Start: Extract Text from PDF

Need to extract text from a PDF? Use this Python snippet:

```python
from pypdf import PdfReader

reader = PdfReader("document.pdf")
text = "".join(page.extract_text() for page in reader.pages)
print(text)
```

Or from the command line:

```bash
uvx --with pypdf python /path/to/extract_pdf_text.py document.pdf
```

## PDF Text Extraction

### Basic Usage

```python
from pypdf import PdfReader

# Read all pages
reader = PdfReader("file.pdf")
for page in reader.pages:
    text = page.extract_text()
    print(text)
```

### Extract Specific Pages

```python
from pypdf import PdfReader

reader = PdfReader("file.pdf")
# Get pages 1-5 (0-indexed)
for page in reader.pages[0:5]:
    print(page.extract_text())
```

### Using the Script

This skill includes `scripts/extract_pdf_text.py` for command-line extraction:

```bash
# Extract all pages to stdout
python extract_pdf_text.py document.pdf

# Extract to file
python extract_pdf_text.py document.pdf --output text.txt

# Extract specific pages
python extract_pdf_text.py document.pdf --pages 1-5
python extract_pdf_text.py document.pdf --pages 1,3,5
```

### Requirements

- **pypdf**: `uvx --with pypdf python <script>`
- Works with most text-based PDFs
- Scanned PDFs without OCR won't extract text

## Common Issues

**"No text extracted"**: The PDF may be scanned (image-based) without OCR. OCR support requires additional tools.

**"Encoding errors"**: pypdf handles most encodings, but some PDFs may have encoding issues. Use `page.extract_text(layout=True)` for layout-aware extraction if available.

---

**Future**: Support for DOCX, XLSX, and other formats coming soon.
