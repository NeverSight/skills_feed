---
name: document-processing
description: >-
  Create, edit, and analyze office documents (PDF, DOCX, PPTX, XLSX). Use when working
  with PDFs, Word documents, PowerPoint presentations, or Excel spreadsheets. Covers text
  extraction, form filling, document creation, and data analysis.
license: MIT
metadata:
  version: "1.0.0"
---

# Document Processing

> **Source:** This skill is adapted from **[Anthropic's Skills](https://github.com/anthropics/skills)** 
> document processing skills (pdf, docx, pptx, xlsx) for Claude Code and AI agents.

Create, edit, and analyze office documents including PDFs, Word documents, PowerPoint presentations, 
and Excel spreadsheets.

---

## Quick Reference: Which Tool to Use

| Task | Document Type | Best Tool |
|------|---------------|-----------|
| Extract text | PDF | `pdfplumber`, `pdftotext` |
| Merge/split | PDF | `pypdf`, `qpdf` |
| Fill forms | PDF | `pdf-lib` (JS), `pypdf` |
| Create new | PDF | `reportlab` |
| OCR scanned | PDF | `pytesseract` + `pdf2image` |
| Extract text | DOCX | `pandoc`, `markitdown` |
| Create new | DOCX | `docx-js` (JS) |
| Edit existing | DOCX | OOXML (unpack/edit/pack) |
| Extract text | PPTX | `markitdown` |
| Create new | PPTX | `html2pptx`, `PptxGenJS` |
| Edit existing | PPTX | OOXML (unpack/edit/pack) |
| Data analysis | XLSX | `pandas` |
| Formulas/formatting | XLSX | `openpyxl` |

---

## PDF Processing

### Text Extraction

```python
import pdfplumber

# Extract text with layout preservation
with pdfplumber.open("document.pdf") as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        print(text)
```

### Table Extraction

```python
import pdfplumber
import pandas as pd

with pdfplumber.open("document.pdf") as pdf:
    all_tables = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])
                all_tables.append(df)

# Combine all tables
if all_tables:
    combined_df = pd.concat(all_tables, ignore_index=True)
    combined_df.to_excel("extracted_tables.xlsx", index=False)
```

### Merge PDFs

```python
from pypdf import PdfWriter, PdfReader

writer = PdfWriter()
for pdf_file in ["doc1.pdf", "doc2.pdf", "doc3.pdf"]:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)

with open("merged.pdf", "wb") as output:
    writer.write(output)
```

### Split PDF

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f"page_{i+1}.pdf", "wb") as output:
        writer.write(output)
```

### Rotate Pages

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

page = reader.pages[0]
page.rotate(90)  # Rotate 90 degrees clockwise
writer.add_page(page)

with open("rotated.pdf", "wb") as output:
    writer.write(output)
```

### OCR Scanned PDFs

```python
# Requires: pip install pytesseract pdf2image
import pytesseract
from pdf2image import convert_from_path

# Convert PDF to images
images = convert_from_path('scanned.pdf')

# OCR each page
text = ""
for i, image in enumerate(images):
    text += f"Page {i+1}:\n"
    text += pytesseract.image_to_string(image)
    text += "\n\n"

print(text)
```

### Add Watermark

```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()

for page in reader.pages:
    page.merge_page(watermark)
    writer.add_page(page)

with open("watermarked.pdf", "wb") as output:
    writer.write(output)
```

### Password Protection

```python
from pypdf import PdfReader, PdfWriter

reader = PdfReader("input.pdf")
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

writer.encrypt("userpassword", "ownerpassword")

with open("encrypted.pdf", "wb") as output:
    writer.write(output)
```

### Create PDF with ReportLab

```python
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("report.pdf", pagesize=letter)
styles = getSampleStyleSheet()
story = []

# Add content
title = Paragraph("Report Title", styles['Title'])
story.append(title)
story.append(Spacer(1, 12))

body = Paragraph("This is the body of the report. " * 20, styles['Normal'])
story.append(body)
story.append(PageBreak())

# Page 2
story.append(Paragraph("Page 2", styles['Heading1']))
story.append(Paragraph("Content for page 2", styles['Normal']))

doc.build(story)
```

### Command Line Tools

```bash
# Extract text (poppler-utils)
pdftotext input.pdf output.txt
pdftotext -layout input.pdf output.txt  # Preserve layout

# Merge PDFs (qpdf)
qpdf --empty --pages file1.pdf file2.pdf -- merged.pdf

# Split pages
qpdf input.pdf --pages . 1-5 -- pages1-5.pdf

# Rotate pages
qpdf input.pdf output.pdf --rotate=+90:1

# Remove password
qpdf --password=mypassword --decrypt encrypted.pdf decrypted.pdf

# Extract images
pdfimages -j input.pdf output_prefix
```

---

## Word Document (DOCX) Processing

### Text Extraction

```bash
# Convert to markdown with pandoc
pandoc document.docx -o output.md

# With tracked changes preserved
pandoc --track-changes=all document.docx -o output.md
```

### Create New Document (docx-js)

```javascript
import { Document, Paragraph, TextRun, HeadingLevel, Packer } from 'docx';
import * as fs from 'fs';

const doc = new Document({
  sections: [{
    properties: {},
    children: [
      new Paragraph({
        text: "Document Title",
        heading: HeadingLevel.HEADING_1,
      }),
      new Paragraph({
        children: [
          new TextRun("This is a "),
          new TextRun({
            text: "bold",
            bold: true,
          }),
          new TextRun(" word in a paragraph."),
        ],
      }),
      new Paragraph({
        text: "This is another paragraph.",
      }),
    ],
  }],
});

// Export to file
const buffer = await Packer.toBuffer(doc);
fs.writeFileSync("output.docx", buffer);
```

### Create Document with Tables

```javascript
import { Document, Paragraph, Table, TableRow, TableCell, Packer } from 'docx';

const table = new Table({
  rows: [
    new TableRow({
      children: [
        new TableCell({ children: [new Paragraph("Header 1")] }),
        new TableCell({ children: [new Paragraph("Header 2")] }),
        new TableCell({ children: [new Paragraph("Header 3")] }),
      ],
    }),
    new TableRow({
      children: [
        new TableCell({ children: [new Paragraph("Cell 1")] }),
        new TableCell({ children: [new Paragraph("Cell 2")] }),
        new TableCell({ children: [new Paragraph("Cell 3")] }),
      ],
    }),
  ],
});

const doc = new Document({
  sections: [{
    children: [
      new Paragraph({ text: "Table Example", heading: HeadingLevel.HEADING_1 }),
      table,
    ],
  }],
});
```

### Edit Existing Document (OOXML)

For complex edits, work with raw OOXML:

1. **Unpack the document:**
   ```bash
   python ooxml/scripts/unpack.py document.docx unpacked/
   ```

2. **Edit XML files** (primarily `word/document.xml`)

3. **Validate and pack:**
   ```bash
   python ooxml/scripts/validate.py unpacked/ --original document.docx
   python ooxml/scripts/pack.py unpacked/ output.docx
   ```

### Tracked Changes Workflow

For document review with track changes:

```bash
# 1. Get current state
pandoc --track-changes=all document.docx -o current.md

# 2. Unpack
python ooxml/scripts/unpack.py document.docx unpacked/

# 3. Edit using tracked change patterns
# Use <w:ins> for insertions, <w:del> for deletions

# 4. Pack final document
python ooxml/scripts/pack.py unpacked/ reviewed.docx
```

---

## PowerPoint (PPTX) Processing

### Text Extraction

```bash
python -m markitdown presentation.pptx
```

### Create New Presentation (PptxGenJS)

```javascript
import PptxGenJS from 'pptxgenjs';

const pptx = new PptxGenJS();

// Slide 1 - Title
const slide1 = pptx.addSlide();
slide1.addText("Presentation Title", {
  x: 1, y: 2, w: 8, h: 1.5,
  fontSize: 36,
  bold: true,
  color: "363636",
  align: "center",
});
slide1.addText("Subtitle goes here", {
  x: 1, y: 3.5, w: 8, h: 0.5,
  fontSize: 18,
  color: "666666",
  align: "center",
});

// Slide 2 - Content
const slide2 = pptx.addSlide();
slide2.addText("Key Points", {
  x: 0.5, y: 0.5, w: 9, h: 0.8,
  fontSize: 28,
  bold: true,
});
slide2.addText([
  { text: "• First important point\n", options: { bullet: true } },
  { text: "• Second important point\n", options: { bullet: true } },
  { text: "• Third important point\n", options: { bullet: true } },
], {
  x: 0.5, y: 1.5, w: 9, h: 3,
  fontSize: 18,
});

// Slide 3 - Chart
const slide3 = pptx.addSlide();
slide3.addChart(pptx.ChartType.bar, [
  { name: "Q1", labels: ["Jan", "Feb", "Mar"], values: [100, 200, 300] },
  { name: "Q2", labels: ["Apr", "May", "Jun"], values: [150, 250, 350] },
], {
  x: 1, y: 1, w: 8, h: 4,
  showLegend: true,
  legendPos: "b",
});

// Save
pptx.writeFile("output.pptx");
```

### Edit Existing Presentation (OOXML)

```bash
# 1. Unpack
python ooxml/scripts/unpack.py presentation.pptx unpacked/

# 2. Key files:
# - ppt/slides/slide1.xml, slide2.xml, etc.
# - ppt/notesSlides/ for speaker notes
# - ppt/theme/ for styling

# 3. Validate and pack
python ooxml/scripts/validate.py unpacked/ --original presentation.pptx
python ooxml/scripts/pack.py unpacked/ output.pptx
```

### Create Thumbnail Grid

```bash
# Create visual overview of all slides
python scripts/thumbnail.py presentation.pptx --cols 4
```

### Convert Slides to Images

```bash
# Convert to PDF first
soffice --headless --convert-to pdf presentation.pptx

# Then PDF to images
pdftoppm -jpeg -r 150 presentation.pdf slide
# Creates slide-1.jpg, slide-2.jpg, etc.
```

---

## Excel (XLSX) Processing

### Data Analysis with Pandas

```python
import pandas as pd

# Read Excel
df = pd.read_excel('file.xlsx')  # Default: first sheet
all_sheets = pd.read_excel('file.xlsx', sheet_name=None)  # All sheets as dict

# Analyze
df.head()      # Preview data
df.info()      # Column info
df.describe()  # Statistics

# Filter and transform
filtered = df[df['Sales'] > 1000]
grouped = df.groupby('Category')['Revenue'].sum()

# Write Excel
df.to_excel('output.xlsx', index=False)
```

### Create Excel with Formulas (openpyxl)

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
sheet = wb.active

# Add data
sheet['A1'] = 'Product'
sheet['B1'] = 'Price'
sheet['C1'] = 'Quantity'
sheet['D1'] = 'Total'

# Header formatting
for cell in ['A1', 'B1', 'C1', 'D1']:
    sheet[cell].font = Font(bold=True, color='FFFFFF')
    sheet[cell].fill = PatternFill('solid', start_color='4472C4')
    sheet[cell].alignment = Alignment(horizontal='center')

# Add data rows
data = [
    ('Widget A', 10.00, 5),
    ('Widget B', 15.00, 3),
    ('Widget C', 20.00, 8),
]

for row_idx, (product, price, qty) in enumerate(data, start=2):
    sheet[f'A{row_idx}'] = product
    sheet[f'B{row_idx}'] = price
    sheet[f'C{row_idx}'] = qty
    # FORMULA - not hardcoded value!
    sheet[f'D{row_idx}'] = f'=B{row_idx}*C{row_idx}'

# Add sum formula at bottom
last_row = len(data) + 2
sheet[f'D{last_row}'] = f'=SUM(D2:D{last_row-1})'

# Column width
sheet.column_dimensions['A'].width = 15
sheet.column_dimensions['B'].width = 10
sheet.column_dimensions['C'].width = 10
sheet.column_dimensions['D'].width = 10

wb.save('output.xlsx')
```

### Financial Model Standards

#### Color Coding

```python
from openpyxl.styles import Font

# Industry-standard colors
BLUE = Font(color='0000FF')   # Hardcoded inputs
BLACK = Font(color='000000')  # Formulas
GREEN = Font(color='008000')  # Links from other sheets
RED = Font(color='FF0000')    # External links

# Apply to cells
sheet['B5'].font = BLUE   # User input
sheet['B6'].font = BLACK  # Formula
```

#### Number Formatting

```python
# Currency with thousands separator
sheet['B5'].number_format = '$#,##0'

# Percentage with one decimal
sheet['B6'].number_format = '0.0%'

# Zeros as dashes
sheet['B7'].number_format = '$#,##0;($#,##0);"-"'

# Multiples
sheet['B8'].number_format = '0.0x'
```

### CRITICAL: Use Formulas, Not Hardcoded Values

```python
# ❌ WRONG - Hardcoding calculated values
total = df['Sales'].sum()
sheet['B10'] = total  # Hardcodes 5000

# ✅ CORRECT - Use Excel formulas
sheet['B10'] = '=SUM(B2:B9)'

# ❌ WRONG - Computing in Python
growth = (current - previous) / previous
sheet['C5'] = growth

# ✅ CORRECT - Excel formula
sheet['C5'] = '=(C4-C2)/C2'
```

### Edit Existing Excel

```python
from openpyxl import load_workbook

# Load with formulas preserved
wb = load_workbook('existing.xlsx')
sheet = wb.active

# Modify cells
sheet['A1'] = 'New Value'
sheet.insert_rows(2)
sheet.delete_cols(3)

# Add new sheet
new_sheet = wb.create_sheet('Analysis')
new_sheet['A1'] = 'Data'

wb.save('modified.xlsx')
```

### Recalculate Formulas

After creating/modifying Excel files with formulas:

```bash
# Recalculate all formulas using LibreOffice
python recalc.py output.xlsx
```

---

## Dependencies

Install as needed:

```bash
# PDF
pip install pypdf pdfplumber reportlab pytesseract pdf2image

# DOCX
npm install -g docx
pip install "markitdown[docx]"

# PPTX
npm install -g pptxgenjs
pip install "markitdown[pptx]"

# XLSX
pip install pandas openpyxl

# Command line tools
sudo apt-get install poppler-utils qpdf libreoffice pandoc
```

---

## Quick Task Reference

| I want to... | Command/Code |
|--------------|--------------|
| Extract PDF text | `pdfplumber.open(f).pages[0].extract_text()` |
| Merge PDFs | `pypdf.PdfWriter()` + loop |
| Split PDF | One `PdfWriter()` per page |
| OCR scanned PDF | `pdf2image` → `pytesseract` |
| Convert DOCX to MD | `pandoc doc.docx -o doc.md` |
| Create DOCX | `docx-js` (JavaScript) |
| Extract PPTX text | `python -m markitdown pres.pptx` |
| Create PPTX | `PptxGenJS` (JavaScript) |
| Analyze Excel | `pandas.read_excel()` |
| Excel with formulas | `openpyxl` |

---

## Credits & Attribution

This skill is adapted from **[Anthropic's Skills](https://github.com/anthropics/skills)**.

Original repositories:
- https://github.com/anthropics/skills (pdf, docx, pptx, xlsx)

**Copyright (c) Anthropic** - MIT License  
Adapted by webconsulting.at for this skill collection
