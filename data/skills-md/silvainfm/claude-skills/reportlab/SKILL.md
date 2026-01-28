---
name: reportlab
description: Python library for programmatic PDF generation and creation. Use when user wants to generate PDFs from scratch, create invoices, reports, certificates, labels, or custom documents with precise control over layout, fonts, graphics, tables, and charts. Supports both low-level drawing (Canvas) and high-level documents (Platypus).
---

# ReportLab

## Overview

ReportLab is a powerful open-source Python library for creating PDF documents programmatically. Generate professional PDFs with precise control over layout, typography, graphics, tables, and charts. Perfect for automated report generation, invoices, certificates, and custom documents.

## When to Use This Skill

Activate when the user:
- Wants to generate PDF documents programmatically
- Needs to create invoices, reports, or receipts
- Asks to create certificates, labels, or forms
- Mentions ReportLab explicitly
- Wants custom PDF layouts with tables, charts, or graphics
- Needs to automate document generation
- Wants precise control over PDF layout and styling

## Installation

Check if ReportLab is installed:

```bash
python3 -c "import reportlab; print(reportlab.Version)"
```

If not installed:

```bash
pip3 install reportlab
```

For additional fonts and features:

```bash
pip3 install reportlab[renderPM,rlPyCairo]
```

## Two Approaches: Canvas vs Platypus

ReportLab provides two APIs:

**Canvas API (Low-Level)**
- Direct drawing on PDF pages
- Precise positioning with x, y coordinates
- Like painting on a canvas
- Best for: Simple documents, custom layouts, graphics-heavy PDFs

**Platypus API (High-Level)**
- Flowable document elements
- Automatic layout and pagination
- Easier for complex multi-page documents
- Best for: Reports, articles, documents with lots of text

## Canvas API (Low-Level Drawing)

### Basic Canvas Usage

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch

# Create PDF
c = canvas.Canvas("output.pdf", pagesize=letter)
width, height = letter

# Draw text
c.drawString(100, height - 100, "Hello, World!")

# Set font
c.setFont("Helvetica-Bold", 24)
c.drawString(100, height - 150, "Large Bold Text")

# Save PDF
c.save()
```

### Drawing Shapes and Lines

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

c = canvas.Canvas("shapes.pdf", pagesize=letter)
width, height = letter

# Line
c.line(50, height - 50, width - 50, height - 50)

# Rectangle
c.rect(50, height - 200, 200, 100, stroke=1, fill=0)

# Filled rectangle with color
c.setFillColor(colors.lightblue)
c.setStrokeColor(colors.blue)
c.rect(300, height - 200, 200, 100, stroke=1, fill=1)

# Circle
c.circle(150, height - 350, 50, stroke=1, fill=0)

# Rounded rectangle
c.roundRect(300, height - 400, 200, 100, 10, stroke=1, fill=0)

c.save()
```

### Working with Text

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

c = canvas.Canvas("text.pdf", pagesize=letter)
width, height = letter

# Different fonts and sizes
c.setFont("Helvetica", 12)
c.drawString(50, height - 50, "Helvetica 12pt")

c.setFont("Helvetica-Bold", 16)
c.drawString(50, height - 80, "Helvetica Bold 16pt")

c.setFont("Times-Roman", 14)
c.drawString(50, height - 110, "Times Roman 14pt")

# Colored text
c.setFillColor(colors.red)
c.drawString(50, height - 140, "Red text")

c.setFillColor(colors.blue)
c.drawString(50, height - 170, "Blue text")

# Text alignment
text = "Right-aligned text"
text_width = c.stringWidth(text, "Helvetica", 12)
c.setFont("Helvetica", 12)
c.setFillColor(colors.black)
c.drawString(width - text_width - 50, height - 200, text)

# Multi-line text with textobject
textobject = c.beginText(50, height - 250)
textobject.setFont("Helvetica", 12)
textobject.textLines("""This is multi-line text.
Each line will be rendered separately.
Great for paragraphs!""")
c.drawText(textobject)

c.save()
```

### Adding Images

```python
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

c = canvas.Canvas("images.pdf", pagesize=letter)
width, height = letter

# Draw image
c.drawImage("logo.png", 50, height - 200, width=2*inch, height=1*inch)

# Image with preserved aspect ratio
c.drawImage("photo.jpg", 50, height - 400, width=3*inch, preserveAspectRatio=True)

c.save()
```

## Platypus API (High-Level Documents)

### Basic Document Structure

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

# Create document
doc = SimpleDocTemplate("document.pdf", pagesize=letter)
story = []  # Container for flowable elements

# Get styles
styles = getSampleStyleSheet()

# Add content
story.append(Paragraph("Document Title", styles['Title']))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("This is a paragraph of text.", styles['Normal']))
story.append(Paragraph("This is another paragraph.", styles['Normal']))

# Build PDF
doc.build(story)
```

### Working with Paragraphs and Styles

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.units import inch
from reportlab.lib import colors

doc = SimpleDocTemplate("styled_doc.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()

# Built-in styles
story.append(Paragraph("Title Style", styles['Title']))
story.append(Paragraph("Heading 1", styles['Heading1']))
story.append(Paragraph("Heading 2", styles['Heading2']))
story.append(Paragraph("Normal paragraph text.", styles['Normal']))
story.append(Spacer(1, 0.2*inch))

# Custom style
custom_style = ParagraphStyle(
    'CustomStyle',
    parent=styles['Normal'],
    fontSize=14,
    textColor=colors.blue,
    alignment=TA_CENTER,
    spaceAfter=10,
)
story.append(Paragraph("Centered blue text", custom_style))

# Justified paragraph
justified_style = ParagraphStyle(
    'Justified',
    parent=styles['Normal'],
    alignment=TA_JUSTIFY,
)
long_text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10
story.append(Paragraph(long_text, justified_style))

doc.build(story)
```

### Creating Tables

```python
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

doc = SimpleDocTemplate("table.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()

story.append(Paragraph("Sales Report", styles['Title']))

# Table data
data = [
    ['Product', 'Q1', 'Q2', 'Q3', 'Q4'],
    ['Widget A', '$1,000', '$1,200', '$1,100', '$1,300'],
    ['Widget B', '$800', '$900', '$950', '$1,000'],
    ['Widget C', '$1,500', '$1,600', '$1,700', '$1,800'],
    ['Total', '$3,300', '$3,700', '$3,750', '$4,100'],
]

# Create table
table = Table(data)

# Style table
table.setStyle(TableStyle([
    # Header row
    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 12),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),

    # Data rows
    ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
    ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 1, colors.black),

    # Total row
    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
]))

story.append(table)
doc.build(story)
```

### Adding Charts

```python
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.lib import colors

doc = SimpleDocTemplate("charts.pdf", pagesize=letter)
story = []
styles = getSampleStyleSheet()

story.append(Paragraph("Sales Charts", styles['Title']))

# Bar chart
drawing = Drawing(400, 200)
bar_chart = VerticalBarChart()
bar_chart.x = 50
bar_chart.y = 50
bar_chart.height = 125
bar_chart.width = 300
bar_chart.data = [[100, 150, 200, 175, 225]]
bar_chart.categoryAxis.categoryNames = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5']
bar_chart.bars[0].fillColor = colors.blue
drawing.add(bar_chart)
story.append(drawing)

# Pie chart
drawing2 = Drawing(400, 200)
pie = Pie()
pie.x = 150
pie.y = 50
pie.width = 100
pie.height = 100
pie.data = [30, 25, 20, 15, 10]
pie.labels = ['Product A', 'Product B', 'Product C', 'Product D', 'Other']
pie.slices.strokeWidth = 0.5
drawing2.add(pie)
story.append(drawing2)

doc.build(story)
```

## Common Patterns

See references/patterns.md for common patterns and uses.

## Best Practices

1. **Choose the right API** - Use Canvas for simple layouts, Platypus for complex documents
2. **Use constants for measurements** - Use `inch`, `cm` from `reportlab.lib.units`
3. **Define styles once** - Create custom styles and reuse them
4. **Test page sizes** - Verify output on different page sizes (letter, A4, etc.)
5. **Handle images carefully** - Check image paths exist before adding to PDF
6. **Use tables for layouts** - Tables are great for structured layouts
7. **Cache fonts** - Register custom fonts once at module level

## Common Issues

### Issue: Text going off page

Calculate available space before drawing:

```python
from reportlab.lib.pagesizes import letter

width, height = letter
margin = 50  # pixels
usable_width = width - 2 * margin
usable_height = height - 2 * margin
```

### Issue: Images not found

Use absolute paths or verify file existence:

```python
import os

image_path = "logo.png"
if os.path.exists(image_path):
    c.drawImage(image_path, x, y, width=w, height=h)
```

### Issue: Unicode characters not displaying

Register and use TrueType fonts:

```python
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))
c.setFont('Arial', 12)
```

## Resources

- **references/api_reference.md**: Quick reference for common ReportLab operations
- Official docs: https://docs.reportlab.com/
- User guide (PDF): https://www.reportlab.com/docs/reportlab-userguide.pdf
- PyPI: https://pypi.org/project/reportlab/
