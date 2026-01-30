---
name: docx
description: Comprehensive document creation, editing, and analysis with support for tracked changes, comments, formatting preservation, and text extraction. When Claude needs to work with professional documents (.docx files) for creating new documents, modifying content, working with tracked changes, or adding comments.
source: anthropics/skills
license: Apache-2.0
---

# DOCX Processing

## Workflow Decision Tree

- **Reading/Analyzing**: Use text extraction or raw XML access
- **Creating New Document**: Use docx-js (JavaScript)
- **Editing Existing**: Use OOXML editing or redlining workflow

## Reading Content

### Text Extraction with Pandoc
```bash
# Convert to markdown with tracked changes
pandoc --track-changes=all file.docx -o output.md
```

### Raw XML Access
```bash
# Unpack document
unzip document.docx -d unpacked/
# Key files:
# word/document.xml - Main content
# word/comments.xml - Comments
# word/media/ - Images
```

## Creating New Documents (docx-js)

```javascript
import { Document, Paragraph, TextRun, Packer } from 'docx';
import fs from 'fs';

const doc = new Document({
  sections: [{
    children: [
      new Paragraph({
        children: [
          new TextRun({ text: "Hello ", bold: true }),
          new TextRun({ text: "World", italics: true })
        ]
      })
    ]
  }]
});

const buffer = await Packer.toBuffer(doc);
fs.writeFileSync('document.docx', buffer);
```

## Editing Existing Documents

### Simple Edits
1. Unpack: `unzip doc.docx -d unpacked/`
2. Edit `word/document.xml`
3. Repack: `cd unpacked && zip -r ../edited.docx .`

### Tracked Changes (Redlining)
For professional documents, use tracked changes:

```xml
<!-- Deletion -->
<w:del w:author="Author" w:date="2025-01-01T00:00:00Z">
  <w:r><w:delText>old text</w:delText></w:r>
</w:del>

<!-- Insertion -->
<w:ins w:author="Author" w:date="2025-01-01T00:00:00Z">
  <w:r><w:t>new text</w:t></w:r>
</w:ins>
```

## Converting to Images

```bash
# DOCX to PDF
soffice --headless --convert-to pdf document.docx

# PDF to images
pdftoppm -jpeg -r 150 document.pdf page
```

## Best Practices

- Use Pandoc for text extraction
- Use docx-js for creating new documents
- For legal/business docs, always use tracked changes
- Preserve original RSIDs when editing
