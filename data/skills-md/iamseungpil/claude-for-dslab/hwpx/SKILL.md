---
name: hwpx
description: "Comprehensive HWPX (Korean Hancom Office) document creation, editing, and analysis. When Claude needs to work with Korean word processor documents (.hwpx files) for: (1) Reading and extracting content, (2) Creating new documents, (3) Modifying or editing content, (4) Extracting tables to CSV, (5) Modifying tables or table cells, or any other HWPX document tasks. MANDATORY TRIGGERS: hwpx, hwp, 한글, 한컴, Hancom, Korean document"
---

# HWPX creation, editing, and analysis

## Overview

A .hwpx file is a ZIP archive containing XML files, based on the OWPML (Open Word-Processor Markup Language) standard (KS X 6101).

## Quick Reference

| Task | Approach |
|------|----------|
| Read/analyze content | `hwpxjs` or unpack for raw XML |
| Create new document | Use `hwpxjs` - see Creating New Documents below |
| Edit existing document | Unpack → edit XML → repack - see Editing Existing Documents below |

### Converting .hwp to .hwpx

Legacy `.hwp` files must be converted before editing:

```bash
# Using hwpxjs CLI (pure TypeScript, no external dependencies)
npx hwpxjs convert:hwp document.hwp output.hwpx

# Or using LibreOffice as fallback
python scripts/office/soffice.py --headless --convert-to hwpx document.hwp
```

### Reading Content

```bash
# Text extraction via CLI
npx hwpxjs txt document.hwpx

# HTML conversion (includes images/styles)
npx hwpxjs html document.hwpx > output.html

# Raw XML access
python scripts/unpack.py document.hwpx unpacked/
```

### Converting to Images

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.hwpx
pdftoppm -jpeg -r 150 document.pdf page
```

---

## Creating New Documents

Generate .hwpx files with JavaScript. Install: `npm install @ssabrojs/hwpxjs`

### Setup
```javascript
const { HwpxWriter, HwpxReader } = require("@ssabrojs/hwpxjs");
const fs = require("fs");

// Create document from plain text
const writer = new HwpxWriter();
const content = `문서 제목

첫 번째 문단입니다.
두 번째 문단입니다.`;

const buffer = await writer.createFromPlainText(content);
fs.writeFileSync("output.hwpx", buffer);
```

### Reading Documents

```javascript
const { HwpxReader } = require("@ssabrojs/hwpxjs");
const fs = require("fs");

const reader = new HwpxReader();
const fileBuffer = fs.readFileSync("document.hwpx");
await reader.loadFromArrayBuffer(fileBuffer.buffer);

// Extract text
const text = await reader.extractText();
console.log(text);

// Get document info
const info = await reader.getDocumentInfo();
console.log(info);

// List images
const images = await reader.listImages();
console.log(images);
// [{ binPath: "BinData/0.jpg", width: 200, height: 150, format: "jpg" }]
```

### HTML Conversion

```javascript
// Basic HTML conversion
const html = await reader.extractHtml();

// With all options
const fullHtml = await reader.extractHtml({
  paragraphTag: "p",
  tableClassName: "hwpx-table",
  renderImages: true,       // Include images
  renderTables: true,       // Include tables
  renderStyles: true,       // Apply styles (bold, italic, color)
  embedImages: true,        // Base64 embed images
  tableHeaderFirstRow: true // First row as <th>
});
```

### HWP to HWPX Conversion

```javascript
const { HwpConverter } = require("@ssabrojs/hwpxjs");

const converter = new HwpConverter({ verbose: true });

// Check availability
if (converter.isAvailable()) {
  // Convert HWP to HWPX
  const result = await converter.convertHwpToHwpx("input.hwp", "output.hwpx");
  if (result.success) {
    console.log(`Converted: ${result.processingTime}ms`);
  }

  // Or extract text only
  const text = await converter.convertHwpToText("input.hwp");
}
```

### Template Processing

```javascript
// hwpxjs supports {{key}} template replacement
const reader = new HwpxReader();
await reader.loadFromArrayBuffer(templateBuffer);

// Apply template replacements
const html = await reader.extractHtml();
const result = html
  .replace(/\{\{name\}\}/g, "홍길동")
  .replace(/\{\{date\}\}/g, "2025-01-01");
```

### Critical Rules for hwpxjs

- **createFromPlainText returns Buffer** - save with `fs.writeFileSync(path, buffer)`
- **loadFromArrayBuffer for reading** - pass `fileBuffer.buffer` not `fileBuffer`
- **Text-only creation** - for tables/images, use XML editing approach below
- **HwpConverter for HWP files** - pure TypeScript, no LibreOffice needed
- **extractHtml for rich content** - includes styles, tables, images

---

## Editing Existing Documents

**Follow all 3 steps in order.**

### Step 1: Unpack
```bash
python scripts/unpack.py document.hwpx unpacked/
```

### Step 2: Edit XML

Edit files in `unpacked/Contents/`. See XML Reference below for patterns.

**Use the Edit tool directly for string replacement. Do not write Python scripts.** Scripts introduce unnecessary complexity. The Edit tool shows exactly what is being replaced.

**CRITICAL: Remove `<hp:linesegarray>` when modifying text.** This element contains cached layout data. Leaving stale linesegarray causes character overlap:

```xml
<!-- BEFORE: paragraph with stale layout cache -->
<hp:p id="0" paraPrIDRef="0" styleIDRef="0">
  <hp:run charPrIDRef="19">
    <hp:t>Original text</hp:t>
  </hp:run>
  <hp:linesegarray>
    <hp:lineseg textpos="0" vertpos="0" vertsize="1000" horzsize="5000" .../>
  </hp:linesegarray>
</hp:p>

<!-- AFTER: remove linesegarray entirely -->
<hp:p id="0" paraPrIDRef="0" styleIDRef="0">
  <hp:run charPrIDRef="19">
    <hp:t>New longer text that exceeds original width</hp:t>
  </hp:run>
</hp:p>
```

**Note**: Multiple `<hp:run>` elements share one `<hp:linesegarray>`. Remove it when editing ANY run in the paragraph.

### Step 3: Pack
```bash
python scripts/pack.py unpacked/ output.hwpx
```

### Common Pitfalls

- **Character overlap after edit**: Remove `<hp:linesegarray>` from the edited `<hp:p>`. Multiple `<hp:run>` elements share one linesegarray—remove it when editing ANY run.
- **Wrong table cell modified**: Include `<hp:cellAddr>` in search pattern. **CRITICAL: `<hp:cellAddr>` appears AFTER cell content, not before.** Use `grep -B20 'colAddr="2" rowAddr="0"' section0.xml`.
- **Preserve `charPrIDRef`**: Don't change charPrIDRef when editing text—it references font/size/style in header.xml.
- **File corruption from string replacement**: Use lxml for structural changes (inserting elements). String replacement breaks XML parent-child relationships.
- **Page overflow from text replacement**: Replacing blanks/spaces with text can cause content overflow and page breaks. Solutions: (1) Keep replacement text similar in length to original spaces, (2) Preserve charPrIDRef for underlined fields to maintain underline style, (3) Reduce unnecessary whitespace proportionally, (4) Cell/margin adjustments may be needed.
- **Image size too large (e.g., 635mm)**: HWP unit calculation error. 1 HWP unit = 1/7200 inch, so **1mm ≈ 283.5 HWP units**.
  - ❌ Wrong: `width="180000"` → 635mm (too large!)
  - ✅ Correct: `width="3400"` → ~12mm (signature size)
  - Formula: `mm × (7200 ÷ 25.4) = HWP units`

---

## XML Reference

### Key Elements

| Element | Purpose |
|---------|---------|
| `<hp:p>` | Paragraph |
| `<hp:run>` | Text run with formatting |
| `<hp:t>` | Text content |
| `<hp:tbl>` | Table |
| `<hp:tc>` | Table cell |
| `<hp:cellAddr>` | Cell position (AFTER content) |
| `<hp:pic>` | Image |
| `<hp:linesegarray>` | Layout cache (remove when editing) |

### Paragraph Structure

```xml
<hp:p id="0" paraPrIDRef="0" styleIDRef="0" pageBreak="0">
  <hp:run charPrIDRef="0">
    <hp:t>Text content</hp:t>
  </hp:run>
  <hp:linesegarray>  <!-- Remove this when editing text -->
    <hp:lineseg textpos="0" vertpos="0" vertsize="1000" .../>
  </hp:linesegarray>
</hp:p>
```

### Table Cell Structure

```xml
<hp:tc borderFillIDRef="5">
  <hp:subList textDirection="HORIZONTAL" vertAlign="CENTER">
    <hp:p paraPrIDRef="20">
      <hp:run charPrIDRef="19">
        <hp:t>Cell content</hp:t>
      </hp:run>
    </hp:p>
  </hp:subList>
  <hp:cellAddr colAddr="0" rowAddr="0"/>  <!-- Position identifier -->
  <hp:cellSpan colSpan="1" rowSpan="1"/>
  <hp:cellSz width="5136" height="4179"/>
</hp:tc>
```

### Images

**CRITICAL: `<hp:pic>` MUST be inside `<hp:run>`, followed by empty `<hp:t/>`**

1. Add image file to `BinData/`
2. Add to manifest `Contents/content.hpf`:
```xml
<opf:item id="image1" href="BinData/image1.png" media-type="image/png" isEmbeded="1"/>
```
3. Reference in section0.xml:
```xml
<hp:p id="0" paraPrIDRef="38" styleIDRef="41">
  <hp:run charPrIDRef="0">
    <hp:pic id="12345" zOrder="0" numberingType="PICTURE" textWrap="TOP_AND_BOTTOM">
      <hp:orgSz width="7200" height="7200"/>  <!-- 1 inch = 7200 HWP units -->
      <hp:curSz width="3600" height="3600"/>  <!-- Display: 0.5 inch -->
      <hc:img binaryItemIDRef="image1" bright="0" contrast="0" effect="REAL_PIC" alpha="0"/>
      <hp:sz width="3600" widthRelTo="ABSOLUTE" height="3600" heightRelTo="ABSOLUTE"/>
      <hp:pos treatAsChar="1" horzRelTo="COLUMN" horzAlign="CENTER" vertRelTo="PARA" vertAlign="TOP"/>
    </hp:pic>
    <hp:t/>  <!-- REQUIRED: empty text element after hp:pic -->
  </hp:run>
</hp:p>
```

**Size units:** HWP uses 1/7200 inch units. **1mm ≈ 283.5 units** (7200 ÷ 25.4)

For safe image insertion using lxml, see [references/image-insertion.md](references/image-insertion.md).

### Page Break

```xml
<hp:p pageBreak="1" ...>  <!-- pageBreak="1" inserts break before paragraph -->
```

### Differences from DOCX

| Aspect | HWPX | DOCX |
|--------|------|------|
| Text element | `<hp:t>` | `<w:t>` |
| Paragraph | `<hp:p>` | `<w:p>` |
| Run | `<hp:run>` | `<w:r>` |
| Layout cache | `<hp:linesegarray>` | None |
| Content location | `Contents/section*.xml` | `word/document.xml` |
| Cell identifier | `<hp:cellAddr>` after content | implicit order |

**Key difference**: HWPX stores layout cache in linesegarray; DOCX doesn't. This is why editing HWPX requires removing linesegarray.

For detailed XML structures (headers/footers, lists/numbering, paragraph formatting), see [references/xml-reference.md](references/xml-reference.md).

---

## Dependencies

```bash
npm install @ssabrojs/hwpxjs
```

- **hwpxjs**: `npm install @ssabrojs/hwpxjs` - reading, writing, HTML conversion, HWP→HWPX conversion
- **pyhwp2md**: Converting HWP/HWPX to Markdown (alternative)
- **LibreOffice**: PDF conversion (auto-configured via `scripts/office/soffice.py`)
- **Poppler**: `pdftoppm` for PDF to images
