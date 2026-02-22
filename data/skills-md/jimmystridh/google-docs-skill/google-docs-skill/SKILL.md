---
name: google-docs-skill
description: Manage Google Docs, Google Sheets, and Google Drive with full document operations, spreadsheet editing, and file workflows. Includes Markdown support for headings, bold, italic, lists, tables, and checkboxes plus Drive upload/download/share/search and advanced Sheets operations.
category: productivity
version: 2.0.0
key_capabilities: create-from-markdown, insert-from-markdown, tables, formatted text, Drive upload/download/share/search, sheets
when_to_use: Document content operations, formatted document creation from Markdown, tables, Drive file management, sharing files, spreadsheet operations, sheets data read/write/format
---

# Google Docs, Sheets & Drive Management Skill

## Purpose

Manage Google Docs documents, Google Sheets spreadsheets, and Google Drive files with comprehensive operations:

**Google Docs:**
- Read document content and structure
- Insert and append text
- Find and replace text
- Basic text formatting (bold, italic, underline)
- Insert page breaks
- Create new documents
- Delete content ranges
- Get document structure (headings)
- Insert inline images from URLs

**Google Drive:**
- Upload files to Drive
- Download files from Drive
- Search and list files
- Share files with users or publicly
- Create folders
- Move, copy, and delete files
- Get file metadata

**Google Sheets:**
- Create, read, write, and append spreadsheet data
- Batch read/write across multiple ranges
- Format cells (bold, colors, fonts, alignment, borders, number formats)
- Merge/unmerge cells, freeze rows/columns
- Sort ranges, find and replace, add filters
- Add charts, protect ranges, conditional formatting
- Manage sheets/tabs (add, delete, rename, copy)
- Set column widths and row heights, auto-resize

**Integration**: All scripts share OAuth credentials

**📚 Additional Resources**:
- See `references/integration-patterns.md` for complete workflow examples
- See `references/troubleshooting.md` for error handling and debugging
- See `references/cli-patterns.md` for CLI interface design rationale

## Prerequisites

Two install modes are supported:

- **Source checkout**: Requires a recent Rust toolchain with Cargo.
- **Release archive**: Uses prebuilt binaries, no local Rust toolchain required.

For source checkouts, validate once before first use:
```bash
cd ~/.claude/skills/google-docs-skill
cargo check --offline
```

## When to Use This Skill

Use this skill when:
- User requests to read or view a Google Doc
- User wants to create a new document
- User wants to edit document content
- User requests text formatting or modifications
- User asks about document structure or headings
- User wants to find and replace text
- User wants to create, read, write, or format a Google Sheet/spreadsheet
- User wants to add charts, filters, or conditional formatting to a spreadsheet
- Keywords: "Google Doc", "document", "edit doc", "format text", "insert text", "spreadsheet", "Google Sheet", "sheet", "cells", "rows", "columns"

**📋 Discovering Your Documents**:
To list or search for documents, use drive_manager:
```bash
# List recent documents
scripts/drive_manager search \
  --query "mimeType='application/vnd.google-apps.document'" \
  --max-results 50

# Search by name
scripts/drive_manager search \
  --query "name contains 'Report' and mimeType='application/vnd.google-apps.document'"
```

## Core Workflows

### 1. Read Document

**Read full document content**:
```bash
scripts/docs_manager read <document_id>
```

**Get document structure (headings)**:
```bash
scripts/docs_manager structure <document_id>
```

**Output**:
- Full text content with paragraphs
- Document metadata (title, revision ID)
- Heading structure with levels and positions

### 2. Create Documents

**Create new document (plain text)**:
```bash
echo '{
  "title": "Project Proposal",
  "content": "Initial plain text content..."
}' | scripts/docs_manager create
```

**Create document from Markdown (RECOMMENDED)**:
```bash
echo '{
  "title": "Project Proposal",
  "markdown": "# Project Proposal\n\n## Overview\n\nThis is **bold** and *italic* text.\n\n- Bullet point 1\n- Bullet point 2\n\n| Column 1 | Column 2 |\n|----------|----------|\n| Data 1   | Data 2   |"
}' | scripts/docs_manager create-from-markdown
```

**Supported Markdown Features**:
- Headings: `#`, `##`, `###` → Google Docs HEADING_1, HEADING_2, HEADING_3
- Bold: `**text**`
- Italic: `*text*`
- Code: `` `text` `` → Courier New with grey background
- Bullet lists: `- item` or `* item`
- Numbered lists: `1. item`
- Checkboxes: `- [ ] unchecked` and `- [x] checked`
- Horizontal rules: `---`
- Tables: `| col1 | col2 |` (with separator row)

**Document ID**:
- Returned in response for future operations
- Use with drive_manager for sharing/organizing

### 3. Insert and Append Text

**Insert plain text at specific position**:
```bash
echo '{
  "document_id": "abc123",
  "text": "This text will be inserted at the beginning.\n\n",
  "index": 1
}' | scripts/docs_manager insert
```

**Insert formatted Markdown (RECOMMENDED)**:
```bash
echo '{
  "document_id": "abc123",
  "markdown": "## New Section\n\nThis has **bold** and *italic* formatting.\n\n- Item 1\n- Item 2",
  "index": 1
}' | scripts/docs_manager insert-from-markdown
```

**Append text to end of document**:
```bash
echo '{
  "document_id": "abc123",
  "text": "\n\nThis text will be appended to the end."
}' | scripts/docs_manager append
```

**Index Positions**:
- Document starts at index 1
- Use `read` command to see current content
- Use `structure` command to find heading positions
- End of document: use `append` instead of calculating index
- For `insert-from-markdown`, omit index to append at end

### 4. Find and Replace

**Simple find and replace**:
```bash
echo '{
  "document_id": "abc123",
  "find": "old text",
  "replace": "new text"
}' | scripts/docs_manager replace
```

**Case-sensitive replacement**:
```bash
echo '{
  "document_id": "abc123",
  "find": "IMPORTANT",
  "replace": "CRITICAL",
  "match_case": true
}' | scripts/docs_manager replace
```

**Replace all occurrences**:
- Automatically replaces all matches
- Returns count of replacements made
- Use for bulk text updates

### 5. Text Formatting

**Format text range (bold)**:
```bash
echo '{
  "document_id": "abc123",
  "start_index": 1,
  "end_index": 20,
  "bold": true
}' | scripts/docs_manager format
```

**Multiple formatting options**:
```bash
echo '{
  "document_id": "abc123",
  "start_index": 50,
  "end_index": 100,
  "bold": true,
  "italic": true,
  "underline": true
}' | scripts/docs_manager format
```

**Formatting Options**:
- `bold`: true/false
- `italic`: true/false
- `underline`: true/false
- All options are independent and can be combined

### 6. Page Breaks

**Insert page break**:
```bash
echo '{
  "document_id": "abc123",
  "index": 500
}' | scripts/docs_manager page-break
```

**Use Cases**:
- Separate document sections
- Start new content on fresh page
- Organize long documents

### 7. Delete Content

**Delete text range**:
```bash
echo '{
  "document_id": "abc123",
  "start_index": 100,
  "end_index": 200
}' | scripts/docs_manager delete
```

**Clear entire document**:
```bash
# Read document first to get end index
scripts/docs_manager read abc123

# Then delete all content (start at 1, end at last index - 1)
echo '{
  "document_id": "abc123",
  "start_index": 1,
  "end_index": 500
}' | scripts/docs_manager delete
```

### 8. Insert Images

**Insert image from URL**:
```bash
echo '{
  "document_id": "abc123",
  "image_url": "https://storage.googleapis.com/bucket/image.png"
}' | scripts/docs_manager insert-image
```

**Insert image with specific size**:
```bash
echo '{
  "document_id": "abc123",
  "image_url": "https://storage.googleapis.com/bucket/image.png",
  "width": 400,
  "height": 300
}' | scripts/docs_manager insert-image
```

**Insert image at specific position**:
```bash
echo '{
  "document_id": "abc123",
  "image_url": "https://storage.googleapis.com/bucket/image.png",
  "index": 100
}' | scripts/docs_manager insert-image
```

**Image URL Requirements**:
- URL must be publicly accessible (Google Docs fetches the image)
- Supported formats: PNG, JPEG, GIF
- SVG is NOT supported - convert to PNG first
- For private images, upload to GCS and make public, or use signed URLs

**Sizing Tips**:
- To fit page width with default margins: use `width: 468` (points)
- Specifying only width will auto-scale height proportionally
- Specifying only height will auto-scale width proportionally
- 1 inch = 72 points

### 9. Insert Tables

**Insert empty table**:
```bash
echo '{
  "document_id": "abc123",
  "rows": 3,
  "cols": 4
}' | scripts/docs_manager insert-table
```

**Insert table with data**:
```bash
echo '{
  "document_id": "abc123",
  "rows": 3,
  "cols": 2,
  "data": [
    ["Header 1", "Header 2"],
    ["Row 1 Col 1", "Row 1 Col 2"],
    ["Row 2 Col 1", "Row 2 Col 2"]
  ]
}' | scripts/docs_manager insert-table
```

**Insert table at specific position**:
```bash
echo '{
  "document_id": "abc123",
  "rows": 2,
  "cols": 3,
  "index": 100,
  "data": [["A", "B", "C"], ["1", "2", "3"]]
}' | scripts/docs_manager insert-table
```

**Note**: Tables can also be created via Markdown in `create-from-markdown`:
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data 1   | Data 2   | Data 3   |
```

## Natural Language Examples

### User Says: "Read the content of this Google Doc: abc123"
```bash
scripts/docs_manager read abc123
```

### User Says: "Create a new document called 'Meeting Notes' with the text 'Attendees: John, Sarah'"
```bash
echo '{
  "title": "Meeting Notes",
  "content": "Attendees: John, Sarah"
}' | scripts/docs_manager create
```

### User Says: "Add 'Next Steps' section to the end of document abc123"
```bash
echo '{
  "document_id": "abc123",
  "text": "\n\n## Next Steps\n\n- Review proposals\n- Schedule follow-up"
}' | scripts/docs_manager append
```

### User Says: "Replace all instances of 'Q3' with 'Q4' in document abc123"
```bash
echo '{
  "document_id": "abc123",
  "find": "Q3",
  "replace": "Q4"
}' | scripts/docs_manager replace
```

### User Says: "Make the first 50 characters of document abc123 bold"
```bash
echo '{
  "document_id": "abc123",
  "start_index": 1,
  "end_index": 50,
  "bold": true
}' | scripts/docs_manager format
```

## Understanding Document Index Positions

**Index System**:
- Documents use zero-based indexing with offset
- Index 1 = start of document (after title)
- Each character (including spaces and newlines) has an index
- Use `read` to see current content and plan insertions
- Use `structure` to find heading positions

**Finding Positions**:
1. Read document to see content
2. Count characters to desired position
3. Or use heading structure for section starts
4. Remember: index 1 = very beginning

**Example**:
```
"Hello World\n\nSecond paragraph"

Index 1: "H" (start)
Index 11: "\n" (first newline)
Index 13: "S" (start of "Second")
Index 29: end of document
```

## Google Drive Operations

The `drive_manager` script provides comprehensive Google Drive file management.

### Upload Files

```bash
# Upload a file to Drive root
scripts/drive_manager upload --file ./document.pdf

# Upload to specific folder
scripts/drive_manager upload --file ./diagram.excalidraw --folder-id abc123

# Upload with custom name
scripts/drive_manager upload --file ./local.txt --name "Remote Name.txt"
```

### Download Files

```bash
# Download a file
scripts/drive_manager download --file-id abc123 --output ./local_copy.pdf

# Download/export Google Doc (native Docs files are auto-exported, default PDF)
scripts/drive_manager download --file-id abc123 --output ./doc.pdf

# Download/export Google Sheet (native Sheets files are auto-exported, default CSV)
scripts/drive_manager download --file-id abc123 --output ./data.csv
```

### Search and List Files

```bash
# List recent files
scripts/drive_manager list --max-results 20

# Search by name
scripts/drive_manager search --query "name contains 'Report'"

# Search by type
scripts/drive_manager search --query "mimeType='application/vnd.google-apps.document'"

# Search in folder
scripts/drive_manager search --query "'folder_id' in parents"

# Combine queries
scripts/drive_manager search --query "name contains '.excalidraw' and modifiedTime > '2024-01-01'"
```

### Share Files

```bash
# Share with specific user (reader)
scripts/drive_manager share --file-id abc123 --email user@example.com --role reader

# Share with write access
scripts/drive_manager share --file-id abc123 --email user@example.com --role writer

# Make publicly accessible (anyone with link)
scripts/drive_manager share --file-id abc123 --type anyone --role reader

# Domain-wide sharing is not exposed as a dedicated CLI flag in this CLI
```

### Folder Management

```bash
# Create a folder
scripts/drive_manager create-folder --name "Project Documents"

# Create folder inside another folder
scripts/drive_manager create-folder --name "Diagrams" --parent-id abc123

# Move file to folder
scripts/drive_manager move --file-id file123 --folder-id folder456
```

### Other Operations

```bash
# Get file metadata
scripts/drive_manager get-metadata --file-id abc123

# Copy a file
scripts/drive_manager copy --file-id abc123 --name "Copy of Document"

# Update file content (replace)
scripts/drive_manager update --file-id abc123 --file ./new_content.pdf

# Delete file (moves to trash)
scripts/drive_manager delete --file-id abc123
```

### Output Format

All commands return JSON with consistent structure:
```json
{
  "status": "success",
  "operation": "upload",
  "file": {
    "id": "1abc...",
    "name": "document.pdf",
    "mime_type": "application/pdf",
    "web_view_link": "https://drive.google.com/file/d/1abc.../view",
    "web_content_link": "https://drive.google.com/uc?id=1abc...",
    "created_time": "2024-01-15T10:30:00Z",
    "modified_time": "2024-01-15T10:30:00Z",
    "size": 12345
  }
}
```

## Google Sheets Operations

The `sheets_manager` script provides comprehensive Google Sheets spreadsheet management. All commands accept JSON via stdin.

### Create Spreadsheet

```bash
# Create with default sheet
echo '{"title": "Budget 2024"}' | scripts/sheets_manager create

# Create with named sheets and initial data
echo '{
  "title": "Budget 2024",
  "sheets": ["Income", "Expenses", "Summary"],
  "data": [["Category", "Amount"], ["Salary", 5000]]
}' | scripts/sheets_manager create
```

### Read Data

```bash
# Read a range
echo '{
  "spreadsheet_id": "abc123",
  "range": "Sheet1!A1:C10"
}' | scripts/sheets_manager read

# Read multiple ranges at once
echo '{
  "spreadsheet_id": "abc123",
  "ranges": ["Sheet1!A1:C10", "Sheet2!A1:B5"]
}' | scripts/sheets_manager batch-read
```

### Write Data

```bash
# Write values to a range
echo '{
  "spreadsheet_id": "abc123",
  "range": "Sheet1!A1:B2",
  "values": [["Name", "Age"], ["Alice", 30]]
}' | scripts/sheets_manager write

# Append rows after existing data
echo '{
  "spreadsheet_id": "abc123",
  "range": "Sheet1!A:B",
  "values": [["Bob", 25], ["Carol", 28]]
}' | scripts/sheets_manager append

# Write to multiple ranges at once
echo '{
  "spreadsheet_id": "abc123",
  "data": [
    {"range": "Sheet1!A1:B2", "values": [["a", "b"], ["c", "d"]]},
    {"range": "Sheet2!A1:B2", "values": [["x", "y"], ["z", "w"]]}
  ]
}' | scripts/sheets_manager batch-write
```

### Clear Data

```bash
echo '{
  "spreadsheet_id": "abc123",
  "range": "Sheet1!A1:C10"
}' | scripts/sheets_manager clear
```

### Get Spreadsheet Metadata

```bash
echo '{"spreadsheet_id": "abc123"}' | scripts/sheets_manager get-metadata
```

Returns: title, locale, time zone, sheet names/IDs, row/column counts, frozen rows/columns.

### Sheet/Tab Management

```bash
# Add a new sheet
echo '{
  "spreadsheet_id": "abc123",
  "title": "New Sheet"
}' | scripts/sheets_manager add-sheet

# Delete a sheet (use sheet_id from get-metadata)
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 123456789
}' | scripts/sheets_manager delete-sheet

# Rename a sheet
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "title": "Renamed Sheet"
}' | scripts/sheets_manager rename-sheet

# Copy sheet within same spreadsheet
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0
}' | scripts/sheets_manager copy-sheet

# Copy sheet to another spreadsheet
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "destination_spreadsheet_id": "xyz789"
}' | scripts/sheets_manager copy-sheet
```

### Format Cells

```bash
# Bold headers with background color
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "range": "A1:D1",
  "bold": true,
  "background_color": {"red": 0.2, "green": 0.5, "blue": 0.8},
  "foreground_color": {"red": 1, "green": 1, "blue": 1},
  "horizontal_alignment": "CENTER"
}' | scripts/sheets_manager format

# Number formatting
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "range": "B2:B100",
  "number_format": {"type": "NUMBER", "pattern": "#,##0.00"}
}' | scripts/sheets_manager format

# Full formatting example
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "range": "A1:D1",
  "bold": true,
  "italic": false,
  "font_size": 12,
  "font_family": "Arial",
  "foreground_color": {"red": 0, "green": 0, "blue": 0},
  "background_color": {"red": 0.9, "green": 0.9, "blue": 0.9},
  "horizontal_alignment": "CENTER",
  "vertical_alignment": "MIDDLE",
  "wrap_strategy": "WRAP",
  "borders": {
    "bottom": {"style": "SOLID", "color": {"red": 0, "green": 0, "blue": 0}}
  }
}' | scripts/sheets_manager format
```

**Format options reference:**
- `bold`, `italic`, `underline` - boolean
- `font_size` - integer (points)
- `font_family` - string (e.g. "Arial", "Courier New")
- `foreground_color` / `background_color` - `{red, green, blue}` floats 0-1
- `horizontal_alignment` - `LEFT`, `CENTER`, `RIGHT`
- `vertical_alignment` - `TOP`, `MIDDLE`, `BOTTOM`
- `number_format` - `{type, pattern}` where type is `NUMBER`, `CURRENCY`, `PERCENT`, `DATE`, `TIME`, `SCIENTIFIC`, `TEXT`
- `wrap_strategy` - `OVERFLOW_CELL`, `CLIP`, `WRAP`
- `text_rotation` - angle in degrees
- `borders` - `{top, bottom, left, right}` each with `{style, color}` where style is `SOLID`, `DASHED`, `DOTTED`, `SOLID_MEDIUM`, `SOLID_THICK`, `DOUBLE`

### Merge and Unmerge Cells

```bash
# Merge cells
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "range": "A1:C1",
  "merge_type": "MERGE_ALL"
}' | scripts/sheets_manager merge-cells

# Unmerge cells
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "range": "A1:C1"
}' | scripts/sheets_manager unmerge-cells
```

Merge types: `MERGE_ALL`, `MERGE_ROWS`, `MERGE_COLUMNS`

### Freeze Rows/Columns

```bash
# Freeze first row (header)
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "rows": 1
}' | scripts/sheets_manager freeze

# Freeze first row and first column
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "rows": 1,
  "cols": 1
}' | scripts/sheets_manager freeze
```

### Column and Row Sizing

```bash
# Auto-resize columns to fit content (0-based indices)
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "start_col": 0,
  "end_col": 5
}' | scripts/sheets_manager auto-resize

# Set column width in pixels
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "start_col": 0,
  "end_col": 1,
  "width": 200
}' | scripts/sheets_manager set-column-width

# Set row height in pixels
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "start_row": 0,
  "end_row": 1,
  "height": 40
}' | scripts/sheets_manager set-row-height
```

### Sort Data

```bash
# Sort by column A ascending (sort_column is 0-based)
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "range": "A2:D100",
  "sort_column": 0,
  "ascending": true
}' | scripts/sheets_manager sort
```

### Find and Replace

```bash
# Replace across entire spreadsheet
echo '{
  "spreadsheet_id": "abc123",
  "find": "Q3",
  "replace": "Q4"
}' | scripts/sheets_manager find-replace

# Replace in specific sheet with options
echo '{
  "spreadsheet_id": "abc123",
  "find": "old value",
  "replace": "new value",
  "sheet_id": 0,
  "match_case": true,
  "match_entire_cell": false
}' | scripts/sheets_manager find-replace
```

### Add Filter

```bash
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "range": "A1:D100"
}' | scripts/sheets_manager add-filter
```

### Add Chart

```bash
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "range": "A1:C10",
  "chart_type": "BAR",
  "title": "Sales by Region"
}' | scripts/sheets_manager add-chart
```

Chart types: `BAR`, `LINE`, `PIE`, `COLUMN`, `AREA`, `SCATTER`

### Protect Range

```bash
# Protect with specific editors
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "range": "A1:D1",
  "description": "Header row - do not edit",
  "editors": ["admin@company.com"]
}' | scripts/sheets_manager protect-range
```

### Conditional Formatting

```bash
# Boolean rule: highlight cells greater than 100
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "range": "B2:B100",
  "rule_type": "BOOLEAN",
  "condition_type": "NUMBER_GREATER",
  "condition_values": ["100"],
  "format_background_color": {"red": 0.8, "green": 1, "blue": 0.8}
}' | scripts/sheets_manager add-conditional-format

# Gradient rule: color scale from red to green
echo '{
  "spreadsheet_id": "abc123",
  "sheet_id": 0,
  "range": "C2:C100",
  "rule_type": "GRADIENT",
  "min_color": {"red": 0.8, "green": 0.2, "blue": 0.2},
  "max_color": {"red": 0.2, "green": 0.8, "blue": 0.2}
}' | scripts/sheets_manager add-conditional-format
```

### Range Notation (A1 Format)

Ranges use standard spreadsheet A1 notation:
- `A1` - single cell
- `A1:C5` - rectangular range
- `A:C` - entire columns A through C
- `1:5` - entire rows 1 through 5
- `Sheet1!A1:C5` - range on specific sheet (the sheet name prefix is stripped; use `sheet_id` for sheet targeting in format/merge operations)

### Discovering Spreadsheets

Use drive_manager to find spreadsheets:
```bash
scripts/drive_manager search \
  --query "mimeType='application/vnd.google-apps.spreadsheet'"

scripts/drive_manager search \
  --query "name contains 'Budget' and mimeType='application/vnd.google-apps.spreadsheet'"
```

---

## Integration Workflows

### Create and Organize Documents

```bash
# Step 1: Create document (returns document_id)
echo '{"title":"Report"}' | scripts/docs_manager create
# Returns: {"document_id": "abc123"}

# Step 2: Add content
echo '{"document_id":"abc123","text":"# Report\n\nContent here"}' | scripts/docs_manager insert

# Step 3: Organize in folder
scripts/drive_manager move --file-id abc123 --folder-id [folder_id]

# Step 4: Share with team
scripts/drive_manager share --file-id abc123 --email team@company.com --role writer
```

### Export Document to PDF

```bash
scripts/drive_manager download --file-id abc123 --output ./report.pdf
```

### Excalidraw Diagrams Workflow

For creating and managing Excalidraw diagrams, see the `excalidraw-diagrams` skill which integrates with drive_manager for:
- Uploading .excalidraw files to Drive
- Getting shareable edit URLs for Excalidraw web
- Round-trip editing between AI and human

## Authentication Setup

**Files**:
- OAuth client JSON: `~/.claude/.google/client_secret.json`
- Token (auto-created): `~/.claude/.google/token.json`

**First Time Setup (Download or Source Checkout)**:
1. Create Google Cloud OAuth credentials (OAuth Client ID: Desktop app) and enable:
   - Google Drive API
   - Google Docs API
   - Google Sheets API
2. Save the downloaded client JSON as `~/.claude/.google/client_secret.json`.
3. Trigger the auth flow to get an authorization URL:
   ```bash
   scripts/drive_manager list --max-results 1
   ```
   If you are not authorized yet, the command prints a JSON error containing `auth_url`.
4. Open `auth_url` in your browser, complete consent, and copy the authorization code.
5. Store the token:
   ```bash
   scripts/docs_manager auth <code>
   # or
   scripts/sheets_manager auth <code>
   ```
6. Retry your original command.

**Re-authorization**:
- Token automatically refreshes when expired
- If refresh fails, re-run authorization flow
- All Google skills will work after single re-auth

## Bundled Resources

### Scripts

**`scripts/docs_manager`**
- Comprehensive Google Docs API wrapper
- All document operations: read, create, insert, append, replace, format, delete
- Document structure analysis (headings)
- Automatic token refresh
- Shared OAuth with other Google skills

**Operations**:
- `read`: View document content
- `structure`: Get document headings and structure
- `insert`: Insert plain text at specific index
- `insert-from-markdown`: Insert formatted markdown content
- `append`: Append text to end
- `replace`: Find and replace text
- `format`: Apply text formatting (bold, italic, underline)
- `page-break`: Insert page break
- `create`: Create new document (plain text)
- `create-from-markdown`: Create document with formatted markdown
- `delete`: Delete content range
- `insert-image`: Insert inline image from URL
- `insert-table`: Insert table with optional data

**Output Format**:
- JSON with `status: 'success'` or `status: 'error'`
- Document operations return document_id and revision_id
- See script help: `scripts/docs_manager --help`

**`scripts/sheets_manager`**
- Comprehensive Google Sheets API wrapper
- All spreadsheet operations: create, read, write, append, clear, format, sort, charts, filters
- Sheet/tab management: add, delete, rename, copy
- Cell formatting: bold, colors, fonts, alignment, borders, number formats, merge
- Batch read/write across multiple ranges
- Conditional formatting and protected ranges
- Shared OAuth with other Google skills

**Operations**:
- `create`: Create new spreadsheet with optional sheets and data
- `read`: Read cell range values
- `write`: Write values to range
- `append`: Append rows after existing data
- `clear`: Clear cell range
- `batch-read`: Read multiple ranges at once
- `batch-write`: Write to multiple ranges at once
- `get-metadata`: Get spreadsheet info (title, sheets, dimensions)
- `add-sheet`: Add new sheet/tab
- `delete-sheet`: Delete sheet/tab
- `rename-sheet`: Rename sheet/tab
- `copy-sheet`: Copy sheet within or to another spreadsheet
- `format`: Format cells (bold, colors, alignment, borders, number format, etc.)
- `merge-cells` / `unmerge-cells`: Merge or unmerge cell ranges
- `freeze`: Freeze rows and/or columns
- `auto-resize`: Auto-resize columns to fit content
- `sort`: Sort range by column
- `find-replace`: Find and replace across spreadsheet
- `set-column-width` / `set-row-height`: Set dimension sizes
- `add-filter`: Add basic filter to range
- `add-chart`: Add chart from data range
- `protect-range`: Protect cells from editing
- `add-conditional-format`: Add conditional formatting rules

**Output Format**:
- JSON with `status: 'success'` or `status: 'error'`
- Spreadsheet operations return spreadsheet_id and operation details
- See script help: `scripts/sheets_manager --help`

### References

**`references/docs_operations.md`**
- Complete operation reference
- Parameter documentation
- Index position examples
- Common workflows

**`references/formatting_guide.md`**
- Text formatting options
- Style guidelines
- Document structure best practices
- Heading hierarchy

### Examples

**`examples/sample_operations.md`**
- Common document operations
- Workflow examples
- Index calculation examples
- Integration with drive_manager for file operations

## Error Handling

**Authentication Error**:
```json
{
  "status": "error",
  "code": "AUTH_ERROR",
  "message": "Token refresh failed: ..."
}
```
**Action**: Guide user through re-authorization

**Document Not Found**:
```json
{
  "status": "error",
  "code": "API_ERROR",
  "message": "Document not found"
}
```
**Action**: Verify document ID, check permissions

**Invalid Index**:
```json
{
  "status": "error",
  "code": "API_ERROR",
  "message": "Invalid index position"
}
```
**Action**: Read document to verify current length, adjust index

**API Error**:
```json
{
  "status": "error",
  "code": "API_ERROR",
  "message": "Failed to update document: ..."
}
```
**Action**: Display error to user, suggest troubleshooting steps

## Best Practices

### Document Creation
1. Always provide meaningful title
2. Add initial content when creating for better context
3. Save returned document_id for future operations
4. Use drive_manager to organize and share

### Text Insertion
1. Read document first to understand current structure
2. Use `structure` command to find heading positions
3. Index 1 = start of document
4. Use `append` for adding to end (simpler than calculating index)
5. Include newlines (\n) for proper formatting

### Find and Replace
1. Test pattern match first on small section
2. Use case-sensitive matching for precise replacements
3. Returns count of replacements made
4. Cannot undo - consider reading document first for backup

### Text Formatting
1. Calculate index positions carefully
2. Read document to verify text location
3. Can combine bold, italic, underline
4. Formatting applies to exact character range

### Document Structure
1. Use heading structure for navigation
2. Insert page breaks between major sections
3. Maintain consistent formatting throughout
4. Use `structure` command to validate hierarchy

## Quick Reference

**Read document**:
```bash
scripts/docs_manager read <document_id>
```

**Create document from Markdown (RECOMMENDED)**:
```bash
echo '{"title":"My Doc","markdown":"# Heading\n\nParagraph with **bold**."}' | scripts/docs_manager create-from-markdown
```

**Create document (plain text)**:
```bash
echo '{"title":"My Doc","content":"Initial text"}' | scripts/docs_manager create
```

**Insert formatted Markdown**:
```bash
echo '{"document_id":"abc123","markdown":"## Section\n\n- Item 1\n- Item 2"}' | scripts/docs_manager insert-from-markdown
```

**Insert plain text at beginning**:
```bash
echo '{"document_id":"abc123","text":"New text","index":1}' | scripts/docs_manager insert
```

**Append to end**:
```bash
echo '{"document_id":"abc123","text":"Appended text"}' | scripts/docs_manager append
```

**Find and replace**:
```bash
echo '{"document_id":"abc123","find":"old","replace":"new"}' | scripts/docs_manager replace
```

**Format text**:
```bash
echo '{"document_id":"abc123","start_index":1,"end_index":50,"bold":true}' | scripts/docs_manager format
```

**Get document structure**:
```bash
scripts/docs_manager structure <document_id>
```

**Insert table**:
```bash
echo '{"document_id":"abc123","rows":3,"cols":2,"data":[["A","B"],["1","2"],["3","4"]]}' | scripts/docs_manager insert-table
```

**Insert image from URL**:
```bash
echo '{"document_id":"abc123","image_url":"https://example.com/image.png"}' | scripts/docs_manager insert-image
```

**Google Sheets - Create spreadsheet**:
```bash
echo '{"title":"My Sheet"}' | scripts/sheets_manager create
```

**Google Sheets - Read data**:
```bash
echo '{"spreadsheet_id":"abc123","range":"Sheet1!A1:C10"}' | scripts/sheets_manager read
```

**Google Sheets - Write data**:
```bash
echo '{"spreadsheet_id":"abc123","range":"Sheet1!A1:B2","values":[["Name","Age"],["Alice",30]]}' | scripts/sheets_manager write
```

**Google Sheets - Append rows**:
```bash
echo '{"spreadsheet_id":"abc123","range":"Sheet1!A:B","values":[["Bob",25]]}' | scripts/sheets_manager append
```

**Google Sheets - Format cells**:
```bash
echo '{"spreadsheet_id":"abc123","sheet_id":0,"range":"A1:D1","bold":true,"background_color":{"red":0.9,"green":0.9,"blue":0.9}}' | scripts/sheets_manager format
```

**Google Sheets - Get metadata**:
```bash
echo '{"spreadsheet_id":"abc123"}' | scripts/sheets_manager get-metadata
```

## Example Workflow: Creating and Editing a Report

1. **Create document with formatted content**:
   ```bash
   echo '{
     "title": "Q4 Report",
     "markdown": "# Q4 Report\n\n## Executive Summary\n\nRevenue increased **25%** over Q3 targets.\n\n## Key Metrics\n\n| Metric | Q3 | Q4 |\n|--------|-----|-----|\n| Revenue | $1M | $1.25M |\n| Users | 10K | 15K |\n\n## Next Steps\n\n- [ ] Finalize budget\n- [ ] Schedule review meeting\n- [x] Complete analysis"
   }' | scripts/docs_manager create-from-markdown
   # Returns: {"document_id": "abc123"}
   ```

2. **Add more content later**:
   ```bash
   echo '{
     "document_id": "abc123",
     "markdown": "\n\n## Appendix\n\nAdditional *details* and **notes** here."
   }' | scripts/docs_manager insert-from-markdown
   ```

3. **Replace text if needed**:
   ```bash
   echo '{
     "document_id": "abc123",
     "find": "Q3",
     "replace": "Q4"
   }' | scripts/docs_manager replace
   ```

4. **Share with team**:
   ```bash
   scripts/drive_manager share --file-id abc123 --email team@company.com --role writer
   ```

## Version History

- **2.0.0** (2026-02-06) - Compiled binaries + wrapper scripts while preserving CLI behavior and JSON response contracts across Docs, Drive, and Sheets managers.
- **1.3.0** (2026-02-06) - Added full Google Sheets support via sheets_manager: create, read, write, append, clear, batch operations, format cells (bold, colors, fonts, alignment, borders, number formats), merge/unmerge, freeze, sort, find-replace, charts, filters, conditional formatting, protected ranges, sheet/tab management (add, delete, rename, copy), column/row sizing.
- **1.2.0** (2025-12-25) - Added markdown support documentation: `create-from-markdown`, `insert-from-markdown`, `insert-table` commands. Supports headings, bold, italic, code, lists, checkboxes, tables, and horizontal rules.
- **1.1.0** (2025-12-20) - Added Google Drive operations via drive_manager: upload, download, search, list, share, move, copy, delete, folder management. Integrated with excalidraw-diagrams skill for diagram workflows.
- **1.0.0** (2025-11-10) - Initial Google Docs skill with full document operations: read, create, insert, append, replace, format, page breaks, structure analysis. Shared OAuth token with email, calendar, contacts, drive, and sheets skills.

---

**Dependencies**:
- Source checkout: Rust + Cargo
- Release archive: none (prebuilt binaries)

Source checkout validation:

```bash
cargo check --offline
```
