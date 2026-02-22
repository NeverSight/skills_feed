---
name: file-naming
description: "Analyze file content and propose intelligent renames using context-aware naming conventions. Date-prefixed for transactional/periodic documents, content-first for creative works. Use for organizing files, cleaning up downloads, or standardizing filenames."
metadata:
  author: nweii
  version: "1.0.2"
---

# Rename Files

Analyze files and propose intelligent renames based on content type and metadata. Provide: a single file path, list of file paths, or folder path.

## Naming Conventions

### Transactional/Periodic Documents

**Repetitive transactions** (orders, receipts, invoices, appointments):

- Format: `YYYY-MM-DD Category Type - Details.extension`
- Example: `2025-06-13 Amazon Order 123-456 - USB Cable.pdf`
- Include: dates, entity names, order/invoice numbers, item descriptions

**Periodic documents** (statements, bills, forms):

- Format: `YYYY-MM Type - Entity.extension`
- Example: `2025-06 Bank Statement - Chase Checking.pdf`
- Example: `2023-12 W2 - Acme Corp.pdf`

**Ongoing agreements** (contracts, policies):

- Format: `YYYY-MM Type - Entity.extension`
- Example: `2025-01 Service Agreement - Internet Provider.pdf`

**Appointments/visits**:

- Format: `YYYY-MM-DD Type - Provider/Location.extension`
- Example: `2025-06-13 Dental Visit - Dr Johnson.pdf`

### Creative/Project Files

**Date as supplementary** (photos, projects, creative work):

- Format: `Description - Date.extension` or `Description - Context Date.extension`
- Example: `Vacation Photos - Hawaii 2025.jpg`
- Example: `Website Redesign - Draft 2025-06.pdf`
- Example: `Company Logo 2025.png`

**Evergreen content** (manuals, references):

- Format: `Type - Name/Description.extension`
- Example: `Product Manual - Widget Pro.pdf`

## Key Principles

- **ISO 8601 dates**: YYYY-MM-DD (specific dates) or YYYY-MM (monthly/annual)
- **Date placement**: Start for time-critical sorting; end for contextual info
- **Remove**: Technical metadata (1080p, WEB-DL), problematic characters (`:*?"<>|#%&`)
- **Keep**: Scannable and sortable filenames

## Process

1. Analyze files using OCR, text extraction, vision analysis, filename patterns
2. Present preview table: "Original Filename" | "New Filename"
3. Show up to 15 files if many present
4. Note any files that couldn't be analyzed
5. Wait for confirmation before renaming

If content unclear: make best guess from filename, clean up existing name, or leave unchanged with note.

**For TV show files**, see [references/tv-episodes.md](references/tv-episodes.md) for Plex/media manager naming conventions.
