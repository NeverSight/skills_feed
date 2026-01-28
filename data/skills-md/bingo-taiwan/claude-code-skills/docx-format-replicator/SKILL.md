---
name: docx-format-replicator
description: Extract formatting from existing Word documents and generate new documents with the same format but different content. Use this skill when users need to create multiple documents with consistent formatting, replicate document templates, or maintain corporate document standards across different content.
---

# DOCX Format Replicator

## Overview

Extract formatting information from existing Word documents (.docx) and use it to generate new documents with identical formatting but different content. This skill enables creating document templates, maintaining consistent formatting across multiple documents, and replicating complex Word document structures.

## When to Use This Skill

Use this skill when the user:
- Wants to extract formatting from an existing Word document
- Needs to create multiple documents with the same format
- Has a template document and wants to generate similar documents with new content
- Asks to "replicate", "copy format", "use the same style", or "create a document like"
- Mentions document templates, corporate standards, or format consistency

## Workflow

### Step 1: Extract Format from Template

Extract formatting information from an existing Word document to create a reusable format configuration.

```bash
python scripts/extract_format.py <template.docx> <output.json>
```

**Example**:
```bash
python scripts/extract_format.py "HY研制任务书.docx" format_template.json
```

**What Gets Extracted**:
- Style definitions (fonts, sizes, colors, alignment)
- Paragraph and character styles
- Numbering schemes (1, 1.1, 1.1.1, etc.)
- Table structures and styles
- Header and footer configurations

**Output**: JSON file containing all format information (see `references/format_config_schema.md` for details)

### Step 2: Prepare Content Data

Create a JSON file with the actual content for the new document. The content must follow the structure defined in `references/content_data_schema.md`.

**Content Structure**:
```json
{
  "metadata": {
    "title": "Document Title",
    "author": "Author Name",
    "version": "1.0",
    "date": "2025-01-15"
  },
  "sections": [
    {
      "type": "heading",
      "content": "Section Title",
      "level": 1,
      "number": "1"
    },
    {
      "type": "paragraph",
      "content": "Paragraph text content."
    },
    {
      "type": "table",
      "rows": 3,
      "cells": [
        ["Header 1", "Header 2"],
        ["Data 1", "Data 2"]
      ]
    }
  ]
}
```

**Supported Section Types**:
- `heading` - Headings with optional numbering
- `paragraph` - Text paragraphs
- `table` - Tables with configurable rows and columns
- `page_break` - Page breaks

See `assets/example_content.json` for a complete example.

### Step 3: Generate New Document

Generate a new Word document using the extracted format and prepared content.

```bash
python scripts/generate_document.py <format.json> <content.json> <output.docx>
```

**Example**:
```bash
python scripts/generate_document.py format_template.json new_content.json output_document.docx
```

**Result**: A new .docx file with the format from the template applied to the new content.

## Complete Example Workflow

User asks: "I have a research task document. I need to create 5 more documents with the same format but different content."

1. **Extract the format**:
```bash
python scripts/extract_format.py research_task_template.docx template_format.json
```

2. **Create content files** for each new document (content1.json, content2.json, etc.)

3. **Generate documents**:
```bash
python scripts/generate_document.py template_format.json content1.json document1.docx
python scripts/generate_document.py template_format.json content2.json document2.docx
# ... repeat for all documents
```

## Common Use Cases

### Corporate Document Templates

Extract format from a company template and generate reports, proposals, or specifications with consistent branding.

```bash
# One-time: Extract company template
python scripts/extract_format.py "Company Template.docx" company_format.json

# For each new document:
python scripts/generate_document.py company_format.json new_report.json "Monthly Report.docx"
```

### Technical Documentation Series

Create multiple technical documents (specifications, test plans, manuals) with identical formatting.

```bash
# Extract from specification template
python scripts/extract_format.py spec_template.docx spec_format.json

# Generate multiple specs
python scripts/generate_document.py spec_format.json product_a_spec.json "Product A Spec.docx"
python scripts/generate_document.py spec_format.json product_b_spec.json "Product B Spec.docx"
```

### Research Task Documents

The included example template (`assets/hy_template_format.json`) demonstrates a complete research task document format with:
- Approval/review table in header
- Multi-level numbering (1, 1.1, 1.1.1)
- Technical specification tables
- Structured sections

Use this as a starting point for similar technical documents.

## Advanced Usage

### Customizing Extraction

Modify `scripts/extract_format.py` to extract additional properties not covered by default:
- Custom XML elements
- Advanced table features (merged cells, borders)
- Embedded objects
- Custom properties

### Extending Content Types

Add new section types in `scripts/generate_document.py`:
- Images with captions
- Bulleted or numbered lists
- Footnotes and endnotes
- Custom content blocks

See `references/content_data_schema.md` for extension guidelines.

### Batch Processing

Create a wrapper script to generate multiple documents:

```python
import json
import subprocess

format_file = "template_format.json"
content_files = ["content1.json", "content2.json", "content3.json"]

for i, content_file in enumerate(content_files, 1):
    output = f"document_{i}.docx"
    subprocess.run([
        "python", "scripts/generate_document.py",
        format_file, content_file, output
    ])
```

## Dependencies

The scripts require:
- Python 3.7+
- `python-docx` library: `pip install python-docx`

No additional dependencies are needed for the core functionality.

## Resources

### scripts/

- **extract_format.py** - Extract formatting from Word documents
- **generate_document.py** - Generate new documents from format + content

Both scripts include built-in help:
```bash
python scripts/extract_format.py --help
python scripts/generate_document.py --help
```

### references/

- **format_config_schema.md** - Complete schema for format configuration files
- **content_data_schema.md** - Complete schema for content data files

Read these for detailed information on file structures and available options.

### assets/

- **hy_template_format.json** - Example extracted format from a technical research task document
- **example_content.json** - Example content data showing all section types

Use these as references when creating your own format and content files.

## Troubleshooting

**Missing styles in output**: Ensure style IDs in content data match those in format config. Check `format.json` for available style IDs.

**Table formatting issues**: Verify table dimensions (rows/columns) match between content data and format config. See `format_config_schema.md` for table structure.

**Font not displaying correctly**: Some fonts may not be available on all systems. Check that referenced fonts are installed.

**Dependencies missing**: Install required Python packages:
```bash
pip install python-docx
```

## Tips

1. **Test with examples first**: Use the included `hy_template_format.json` and `example_content.json` to understand the workflow before extracting your own formats.

2. **Start simple**: Begin with basic headings and paragraphs, then add tables and complex formatting.

3. **Validate JSON**: Use a JSON validator to check content data files before generating documents.

4. **Keep format configs**: Store extracted format configurations for reuse across multiple projects.

5. **Version control**: Track both format configs and content data in version control for reproducible document generation.
