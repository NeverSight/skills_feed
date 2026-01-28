---
name: pdf
description: Comprehensive PDF manipulation toolkit for extracting text and tables, creating new PDFs, merging/splitting documents, handling forms, and OCR on scanned documents. Use when filling PDF forms, extracting data from PDFs, merging or splitting documents, creating PDFs programmatically, processing documents at scale, or performing OCR on image-based PDFs.
allowed-tools: [Read, Bash]
---

# PDF Processing Guide

## Reference Files

Detailed guides for specific tasks and libraries:

- [python-libraries.md](python-libraries.md) - Comprehensive Python library examples (pypdf, pdfplumber, reportlab)
- [cli-tools.md](cli-tools.md) - Command-line tools reference (pdftotext, qpdf, pdftk)
- [reference.md](reference.md) - Advanced features (pypdfium2, pdf-lib JavaScript, OCR)
- [forms.md](forms.md) - Complete workflow for filling PDF forms

## Quick Start

### Extract Text

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        print(page.extract_text())
```

### Extract Tables

```python
import pdfplumber

with pdfplumber.open("document.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        tables = page.extract_tables()
        for table in tables:
            print(table)
```

### Merge PDFs

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

### Split PDF into Pages

```python
from pypdf import PdfWriter, PdfReader

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

### Create PDF

```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

c = canvas.Canvas("hello.pdf", pagesize=letter)
c.drawString(100, 750, "Hello World!")
c.save()
```

## Common Workflows

### Fill Out a Form

PDF forms can be fillable (with form fields) or non-fillable (requiring manual positioning). For complete step-by-step instructions, see [forms.md](forms.md).

### Extract and Analyze Data

Combine text extraction with JSON export for downstream processing:

```python
import pdfplumber
import json

# Extract all text
with pdfplumber.open("document.pdf") as pdf:
    full_text = "\n".join(
        page.extract_text() or "" for page in pdf.pages
    )

# Extract tables as structured data
data = []
with pdfplumber.open("document.pdf") as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        for table in (page.extract_tables() or []):
            data.append({"page": page_num, "data": table})

with open("output.json", "w") as f:
    json.dump(data, f, indent=2)
```

### Process Scanned PDFs (OCR)

Extract text from image-based PDFs using OCR. See [reference.md](reference.md) for detailed OCR examples.

### Add Password Protection

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

writer.encrypt("password")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

## Tool Selection Guide

| Task                    | Recommended Tool | See Also                                   |
| ----------------------- | ---------------- | ------------------------------------------ |
| Extract text/tables     | pdfplumber       | [python-libraries.md](python-libraries.md) |
| Merge/split/rotate      | pypdf            | [python-libraries.md](python-libraries.md) |
| Create PDFs             | reportlab        | [python-libraries.md](python-libraries.md) |
| Command-line operations | qpdf/pdftotext   | [cli-tools.md](cli-tools.md)               |
| Fill forms              | pypdf/pdf-lib    | [forms.md](forms.md)                       |
| Scanned PDFs/OCR        | pytesseract      | [reference.md](reference.md)               |
| Advanced rendering      | pypdfium2        | [reference.md](reference.md)               |
| JavaScript context      | pdf-lib          | [reference.md](reference.md)               |

## Next Steps

- **Filling a form?** → [forms.md](forms.md)
- **Need Python library details?** → [python-libraries.md](python-libraries.md)
- **Using command line?** → [cli-tools.md](cli-tools.md)
- **Advanced features (OCR, rendering, JS)?** → [reference.md](reference.md)
