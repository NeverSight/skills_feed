---
name: paddleocr-vl-1.5
description: >
  Advanced document parsing with PaddleOCR-VL 1.5 vision-language model. Returns complete document
  structure including text, tables, formulas, charts, and layout information. Claude extracts
  relevant content based on user needs.
---

# PaddleOCR-VL 1.5 Document Parsing Skill

## When to Use This Skill

✅ **Use PaddleOCR-VL 1.5 for**:
- Documents with tables (invoices, financial reports, spreadsheets)
- Documents with mathematical formulas (academic papers, scientific documents)
- Documents with charts and diagrams
- Multi-column layouts (newspapers, magazines, brochures)
- Complex document structures requiring layout analysis
- Any document requiring structured understanding

❌ **Use PP-OCRv5 instead for**:
- Simple text-only extraction
- Quick OCR tasks where speed is critical
- Screenshots or simple images with clear text

## How to Use This Skill

**⛔ MANDATORY RESTRICTIONS - DO NOT VIOLATE ⛔**

1. **ONLY use PaddleOCR-VL 1.5 API** - Execute the script `python scripts/paddleocr-vl-1.5/vl_caller.py`
2. **NEVER use Claude's built-in vision** - Do NOT parse documents yourself
3. **NEVER offer alternatives** - Do NOT suggest "I can try to analyze it" or similar
4. **IF API fails** - Display the error message and STOP immediately
5. **NO fallback methods** - Do NOT attempt document parsing any other way

If the script execution fails (API not configured, network error, etc.):
- Show the error message to the user
- Do NOT offer to help using your vision capabilities
- Do NOT ask "Would you like me to try parsing it?"
- Simply stop and wait for user to fix the configuration

### Basic Workflow

1. **Execute document parsing**:
   ```bash
   python scripts/paddleocr-vl-1.5/vl_caller.py --file-url "URL provided by user"
   ```
   Or for local files:
   ```bash
   python scripts/paddleocr-vl-1.5/vl_caller.py --file-path "file path"
   ```

   **Save result to file** (recommended):
   ```bash
   python scripts/paddleocr-vl-1.5/vl_caller.py --file-url "URL" --output result.json --pretty
   ```
   - The script will display: `Result saved to: /absolute/path/to/result.json`
   - This message appears on stderr, the JSON is saved to the file
   - **Tell the user the file path** shown in the message

2. **The script returns COMPLETE JSON** with all document content:
   - Headers, footers, page numbers
   - Main text content
   - Tables with structure
   - Formulas (with LaTeX)
   - Figures and charts
   - Footnotes and references
   - Layout and reading order

3. **Extract what the user needs** from the complete data based on their request.

### IMPORTANT: Complete Content Display

**CRITICAL**: You must display the COMPLETE extracted content to the user based on their needs.

- The script returns ALL document content in a structured format
- **Display the full content requested by the user**, do NOT truncate or summarize
- If user asks for "all text", show the entire `result.full_text`
- If user asks for "tables", show ALL tables in the document
- If user asks for "main content", filter out headers/footers but show ALL body text

**What this means**:
- ✅ **DO**: Display complete text, all tables, all formulas as requested
- ✅ **DO**: Present content in reading order using `reading_order` array
- ❌ **DON'T**: Truncate with "..." unless content is excessively long (>10,000 chars)
- ❌ **DON'T**: Summarize or provide excerpts when user asks for full content
- ❌ **DON'T**: Say "Here's a preview" when user expects complete output

**Example - Correct**:
```
User: "Extract all the text from this document"
Claude: I've parsed the complete document. Here's all the extracted text:

[Display entire result.full_text or concatenated regions in reading order]

Document Statistics:
- Total regions: 25
- Text blocks: 15
- Tables: 3
- Formulas: 2
Quality: Excellent (confidence: 0.92)
```

**Example - Incorrect** ❌:
```
User: "Extract all the text"
Claude: "I found a document with multiple sections. Here's the beginning:
'Introduction...' (content truncated for brevity)"
```

### Understanding the JSON Response

The script returns a complete JSON structure:

```json
{
  "ok": true,
  "result": {
    "full_text": "Complete text with all content including headers, footers, etc.",
    "layout": {
      "regions": [
        {
          "id": 0,
          "type": "header",
          "content": "Chapter 3: Methods",
          "bbox": [100, 50, 500, 100]
        },
        {
          "id": 1,
          "type": "text",
          "content": "Main body text content...",
          "bbox": [100, 150, 500, 300]
        },
        {
          "id": 2,
          "type": "table",
          "content": {
            "rows": 3,
            "cols": 2,
            "cells": [["Header1", "Header2"], ["Data1", "Data2"]]
          },
          "bbox": [100, 350, 500, 550]
        },
        {
          "id": 3,
          "type": "formula",
          "content": "E = mc^2",
          "latex": "$E = mc^2$",
          "bbox": [200, 600, 400, 630]
        },
        {
          "id": 4,
          "type": "footnote",
          "content": "[1] Reference citation",
          "bbox": [100, 650, 500, 680]
        },
        {
          "id": 5,
          "type": "footer",
          "content": "University Name 2024",
          "bbox": [100, 750, 500, 800]
        },
        {
          "id": 6,
          "type": "page_number",
          "content": "25",
          "bbox": [250, 770, 280, 790]
        }
      ],
      "reading_order": [0, 1, 2, 3, 4, 5, 6]
    }
  },
  "metadata": {
    "processing_time_ms": 3500,
    "total_pages": 1,
    "model_version": "paddleocr-vl-1.5"
  }
}
```

### Region Types

The `type` field indicates the element category:

| Type | Description | Typically Include? |
|------|-------------|-------------------|
| `header` | Page headers (chapter/section titles) | Exclude (usually repetitive) |
| `text` | Main body text | **Include** |
| `table` | Tables with structured data | **Include** |
| `formula` | Mathematical formulas | **Include** |
| `figure` | Images, charts, diagrams | **Include** |
| `footnote` | Footnotes and references | **Include** (often important) |
| `footer` | Page footers (author/institution) | Exclude (usually repetitive) |
| `page_number` | Page numbers | Exclude (not content) |
| `margin_note` | Margin annotations | Context-dependent |

### Content Extraction Guidelines

**Based on user intent, filter the regions**:

| User Says | What to Extract | How |
|-----------|-----------------|-----|
| "Extract main content" | text, table, formula, figure, footnote | Skip header, footer, page_number |
| "Get all tables" | table only | Filter by type="table" |
| "Extract formulas" | formula only | Filter by type="formula" |
| "Complete document" | Everything | Use all regions or full_text |
| "Without headers/footers" | Core content | Skip header, footer types |
| "Include page numbers" | Core + page_number | Keep page_number type |

### Usage Examples

**Example 1: Extract Main Content** (default behavior)
```bash
python scripts/paddleocr-vl-1.5/vl_caller.py \
  --file-url "https://example.com/paper.pdf" \
  --pretty
```

Then filter JSON to extract core content:
- Include: text, table, formula, figure, footnote
- Exclude: header, footer, page_number

**Example 2: Extract Tables Only**
```bash
python scripts/paddleocr-vl-1.5/vl_caller.py \
  --file-path "./financial_report.pdf" \
  --pretty
```

Then filter JSON:
- Only keep regions where type="table"
- Present table content in markdown format

**Example 3: Complete Document with Everything**
```bash
python scripts/paddleocr-vl-1.5/vl_caller.py \
  --file-url "URL" \
  --pretty
```

Then use `result.full_text` or present all regions in reading_order.

### First-Time Configuration

**When API is not configured**:

The error will show:
```
Configuration error: API not configured. Get your API at: https://aistudio.baidu.com/paddleocr/task
```

**Auto-configuration workflow**:

1. **Show the exact error message** to user (including the URL)

2. **Tell user to provide credentials**:
   ```
   Please visit the URL above to get your VL_API_URL and VL_TOKEN.
   Once you have them, send them to me and I'll configure it automatically.
   ```

3. **When user provides credentials** (accept any format):
   - `VL_API_URL=https://xxx.com/v1, VL_TOKEN=abc123...`
   - `Here's my API: https://xxx and token: abc123`
   - Copy-pasted code format
   - Any other reasonable format

4. **Parse credentials from user's message**:
   - Extract VL_API_URL value (look for URLs)
   - Extract VL_TOKEN value (long alphanumeric string, usually 40+ chars)

5. **Configure automatically**:
   ```bash
   python scripts/paddleocr-vl-1.5/configure.py --api-url "PARSED_URL" --token "PARSED_TOKEN"
   ```

6. **If configuration succeeds**:
   - Inform user: "Configuration complete! Parsing document now..."
   - Retry the original parsing task

7. **If configuration fails**:
   - Show the error
   - Ask user to verify the credentials

**IMPORTANT**: The error message format is STRICT and must be shown exactly as provided by the script. Do not modify or paraphrase it.

### Handling Large Files (>20MB)

**Problem**: Local files larger than 20MB are rejected by default.

**Solutions** (Choose based on your situation):

#### Solution 1: Use URL Upload (Recommended) ⭐
Upload your file to a web server and use `--file-url`:
```bash
# Instead of local file
python scripts/paddleocr-vl-1.5/vl_caller.py --file-path "large_file.pdf"  # ❌ May fail

# Use URL instead
python scripts/paddleocr-vl-1.5/vl_caller.py --file-url "https://your-server.com/large_file.pdf"  # ✅ No size limit
```

Benefits:
- No local file size limit
- Faster upload (direct from API server)
- Suitable for very large files (>100MB)

#### Solution 2: Increase Size Limit
Adjust the limit in `.env` file:
```bash
# .env
VL_MAX_FILE_SIZE_MB=50  # Increase from 20MB to 50MB
```

Then process as usual:
```bash
python scripts/paddleocr-vl-1.5/vl_caller.py --file-path "large_file.pdf"
```

**Note**: Your API provider may still have upload limits. Check with your VL API service.

#### Solution 3: Compress/Optimize File
Use the built-in optimizer to reduce file size:

```bash
# Install optimization dependencies first
pip install -r scripts/paddleocr-vl-1.5/requirements-optimize.txt

# Optimize image (reduce quality)
python scripts/paddleocr-vl-1.5/optimize_file.py input.png output.png --quality 70

# Optimize PDF (compress images within)
python scripts/paddleocr-vl-1.5/optimize_file.py input.pdf output.pdf --target-size 15

# Then process optimized file
python scripts/paddleocr-vl-1.5/vl_caller.py --file-path "output.pdf" --pretty
```

The optimizer will:
- Compress images (adjust JPEG quality)
- Resize images if needed (maintain aspect ratio)
- Compress PDF images (reduce DPI to 150)
- Show before/after size comparison

#### Solution 4: Process Specific Pages (PDF Only)
If you only need certain pages from a large PDF, extract them first:

```bash
# Using PyMuPDF (requires: pip install PyMuPDF)
python -c "
import fitz
doc = fitz.open('large.pdf')
writer = fitz.open()
writer.insert_pdf(doc, from_page=0, to_page=4)  # Pages 1-5
writer.save('pages_1_5.pdf')
"

# Then process the smaller file
python scripts/paddleocr-vl-1.5/vl_caller.py --file-path "pages_1_5.pdf"
```

#### Solution 5: Upload to Cloud Storage
For extremely large files (>100MB), use cloud storage with public URLs:

```bash
# Example: Upload to AWS S3, Google Drive, or similar
# Get public URL: https://storage.example.com/my-document.pdf

# Process via URL
python scripts/paddleocr-vl-1.5/vl_caller.py --file-url "https://storage.example.com/my-document.pdf"
```

**Comparison Table**:

| Solution | Max Size | Speed | Complexity | Best For |
|----------|----------|-------|------------|----------|
| URL Upload | Unlimited | Fast | Low | Any large file |
| Increase Limit | Configurable | Medium | Very Low | Slightly over limit |
| Compress | ~70% reduction | Slow | Medium | Images/PDFs with images |
| Extract Pages | As needed | Fast | Medium | Multi-page PDFs |
| Cloud Storage | Unlimited | Fast | High | Very large files (>100MB) |

### Error Handling

**Authentication failed (401/403)**:
```
error: Authentication failed
```
→ Token is invalid, reconfigure with correct credentials

**API quota exceeded (429)**:
```
error: API quota exceeded
```
→ Daily API quota exhausted, inform user to wait or upgrade

**Unsupported format**:
```
error: Unsupported file format
```
→ File format not supported, convert to PDF/PNG/JPG

### Pseudo-Code: Content Extraction

**Extract main content** (most common):
```python
def extract_main_content(json_response):
    regions = json_response['result']['layout']['regions']

    # Keep only core content types
    core_types = ['text', 'table', 'formula', 'figure', 'footnote']
    main_regions = [r for r in regions if r['type'] in core_types]

    # Sort by reading order
    reading_order = json_response['result']['layout']['reading_order']
    sorted_regions = sort_by_order(main_regions, reading_order)

    # Present to user
    for region in sorted_regions:
        if region['type'] == 'text':
            print(region['content'])
        elif region['type'] == 'table':
            print_as_markdown_table(region['content'])
        elif region['type'] == 'formula':
            print(f"Formula: {region['latex']}")
```

**Extract tables only**:
```python
def extract_tables(json_response):
    regions = json_response['result']['layout']['regions']
    tables = [r for r in regions if r['type'] == 'table']

    for i, table in enumerate(tables):
        print(f"Table {i+1}:")
        print_as_markdown_table(table['content'])
```

**Extract everything**:
```python
def extract_complete(json_response):
    # Simply use the full_text which includes everything
    print(json_response['result']['full_text'])

    # Or present all regions in order
    regions = json_response['result']['layout']['regions']
    reading_order = json_response['result']['layout']['reading_order']

    for idx in reading_order:
        region = regions[idx]
        print(f"[{region['type']}] {region['content']}")
```

## Important Notes

- **The script NEVER filters content** - It always returns complete data
- **Claude decides what to present** - Based on user's specific request
- **All data is always available** - Can be re-interpreted for different needs
- **No information is lost** - Complete document structure preserved

## Reference Documentation

For in-depth understanding of the PaddleOCR-VL 1.5 system, refer to:
- `references/paddleocr-vl-1.5/vl_model_spec.md` - VL model specifications
- `references/paddleocr-vl-1.5/layout_schema.md` - Layout detection schema
- `references/paddleocr-vl-1.5/output_format.md` - Complete output format specification

Load these reference documents into context when:
- Debugging complex parsing issues
- Understanding layout detection algorithm
- Working with special document types
- Customizing content extraction logic

## Testing the Skill

To verify the skill is working properly:
```bash
python scripts/paddleocr-vl-1.5/smoke_test.py
```

This tests configuration and optionally API connectivity.
