---
name: excel-parser
description: Smart Excel/CSV file parsing with intelligent routing based on file complexity analysis. Analyzes file structure (merged cells, row count, table layout) using lightweight metadata scanning, then recommends optimal processing strategy - either high-speed Pandas mode for standard tables or semantic HTML mode for complex reports. Use when processing Excel/CSV files with unknown or varying structure where optimization between speed and accuracy is needed.
---

# Excel Parser

## Table of Contents

- [Overview](#overview)
- [Core Philosophy: Scout Pattern](#core-philosophy-scout-pattern)
- [When to Use This Skill](#when-to-use-this-skill)
- [Processing Workflow](#processing-workflow)
- [Complexity Scoring Rules](#complexity-scoring-rules)
- [Path A: Pandas Standard Mode](#path-a-pandas-standard-mode)
- [Path B: HTML Semantic Mode](#path-b-html-semantic-mode)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [Dependencies](#dependencies)
- [Resources](#resources)

## Overview

Provide intelligent routing strategies for parsing Excel/CSV files by analyzing complexity and choosing the optimal processing path. The skill implements a "Scout Pattern" that scans file metadata before processing to balance speed (Pandas) with accuracy (semantic extraction).

## Core Philosophy: Scout Pattern

Before processing data, deploy a lightweight "scout" to analyze file metadata and make intelligent routing decisions:

1. **Metadata Scanning** - Use `openpyxl` to scan file structure without loading data
2. **Complexity Scoring** - Calculate score based on merged cells, row count, and layout
3. **Path Selection** - Choose between Pandas (fast) or HTML (accurate) processing
4. **Optimized Execution** - Execute with the most appropriate tool for the file type

**Key Principle**: "LLM handles metadata decisions, Pandas/HTML processes bulk data"

## When to Use This Skill

**Use excel-parser when:**
- Processing Excel/CSV files with unknown structure or varying complexity
- Handling files ranging from simple data tables to complex financial reports
- Need to optimize between processing speed and extraction accuracy
- Working with files that may contain merged cells, multi-level headers, or irregular layouts

**Skip this skill when:**
- File structure is already known and documented
- Processing simple, well-structured tables with confirmed format
- Using predefined scripts for specific file formats

## Processing Workflow

### Step 1: Analyze File Complexity

Use the `scripts/complexity_analyzer.py` to scan file metadata:

```bash
python scripts/complexity_analyzer.py <file_path> [sheet_name]
```

**What it analyzes** (without loading data):
- Merged cell distribution (shallow vs deep in the table)
- Row count and data continuity
- Empty row interruptions (indicates multi-table layouts)

**Output** (JSON format):
```json
{
  "is_complex": false,
  "recommended_strategy": "pandas",
  "reasons": ["No deep merges detected", "Row count exceeds 1000, forcing Pandas mode"],
  "stats": {
    "total_rows": 5000,
    "deep_merges": 0,
    "empty_interruptions": 0
  }
}
```

### Step 2: Route to Optimal Strategy

Based on complexity analysis:

- **is_complex = false** → Use **Path A (Pandas Standard Mode)**
- **is_complex = true** → Use **Path B (HTML Semantic Mode)**

### Step 3: Execute Processing

Follow the selected path's workflow to extract data.

## Complexity Scoring Rules

### Rule 1: Deep Merged Cells
- **Condition**: Merged cells appearing beyond row 5
- **Interpretation**: Complex table structure (not just header formatting)
- **Decision**: Mark as complex if >2 deep merges detected
- **Example**: Financial reports with merged category labels in data region

### Rule 2: Empty Row Interruptions
- **Condition**: Multiple empty rows within the table
- **Interpretation**: Multiple sub-tables in single sheet
- **Decision**: Mark as complex if >2 empty row interruptions found
- **Example**: Summary table + detail table in one sheet

### Rule 3: Row Count Override
- **Condition**: Total rows >1000
- **Interpretation**: Too large for HTML processing (token explosion)
- **Decision**: Force Pandas mode regardless of complexity
- **Rationale**: HTML conversion would exceed token limits

### Rule 4: Default (Standard Table)
- **Condition**: No deep merges, continuous data, moderate size
- **Interpretation**: Standard data table
- **Decision**: Use Pandas for optimal speed

## Path A: Pandas Standard Mode

**When**: Simple/large tables (most common case)

**Strategy**: Agent analyzes ONLY the first 20 rows to determine header position, then use Pandas to read full data at native speed.

**Workflow**:

1. **Sample First 20 Rows**
   - Read only the first 20 rows using `pd.read_excel(..., nrows=20)`
   - Convert to CSV format for analysis

2. **Determine Header Position**
   - Examine the sampled rows to identify which row contains the actual column headers
   - Common patterns: Row 0 (standard), Row 1-2 (if title rows exist), Row with distinct column names

3. **Read Full Data**
   - Use `pd.read_excel(..., header=<detected_row>)` to load complete data
   - The header parameter ensures proper column naming

**Token Cost**: ~500 tokens (only 20 rows analyzed)
**Processing Speed**: Very fast (Pandas native speed)

> For implementation details, see `references/smart_excel_router.py`

## Path B: HTML Semantic Mode

**When**: Complex/irregular tables (merged cells, multi-level headers)

**Strategy**: Convert to semantic HTML preserving structure (rowspan/colspan), then extract data understanding the visual layout.

**Workflow**:

1. **Convert to Semantic HTML**
   - Load workbook with `openpyxl`
   - Build HTML table preserving merged cell spans
   - Use `rowspan` and `colspan` attributes to maintain structure

2. **Extract Structured Data**
   - Analyze HTML table structure
   - Identify hierarchical headers from merged cells
   - Extract data preserving semantic relationships

**Token Cost**: Higher (full HTML structure analyzed)
**Processing Speed**: Slower (semantic extraction)
**Use Case**: Only for small (<1000 rows), complex files where Pandas would fail

> For implementation details, see `references/smart_excel_router.py`

## Best Practices

### 1. Trust the Scout
Always run complexity analysis before processing. The metadata scan is fast (<1 second) and prevents wasted effort on wrong approach.

### 2. Respect the Row Count Rule
Never attempt HTML mode on files >1000 rows. Token limits will cause failures.

### 3. Pandas First for Unknown Files
When in doubt, try Pandas mode first. It fails fast and clearly when structure is incompatible.

### 4. Cache Analysis Results
If processing multiple sheets from same file, run analysis once and cache results.

### 5. Preserve Original Files
Never modify the original Excel file during analysis or processing.

## Troubleshooting

### File Cannot Be Opened
- **Symptom**: `FileNotFoundError` or permission errors
- **Causes**: Invalid path, file locked by another process, insufficient permissions
- **Solutions**:
  - Verify file path is correct and file exists
  - Close the file if open in Excel or another application
  - Check read permissions on the file

### Corrupted File Errors
- **Symptom**: `BadZipFile` or `InvalidFileException`
- **Causes**: Incomplete download, file corruption, wrong file extension
- **Solutions**:
  - Re-download or obtain fresh copy of the file
  - Verify file is actual Excel format (not CSV with .xlsx extension)
  - Try opening in Excel to confirm file integrity

### Memory Issues with Large Files
- **Symptom**: `MemoryError` or system slowdown
- **Causes**: File too large for available RAM
- **Solutions**:
  - Use `read_only=True` mode in openpyxl
  - Process file in chunks using Pandas `chunksize` parameter
  - Increase system memory or use machine with more RAM

### Encoding Problems
- **Symptom**: Garbled text or `UnicodeDecodeError`
- **Causes**: Non-UTF8 encoding in source data
- **Solutions**:
  - Specify encoding when reading CSV: `pd.read_csv(..., encoding='gbk')`
  - For Excel, data is usually UTF-8; check source data generation

### HTML Mode Token Overflow
- **Symptom**: Truncated output or API errors
- **Causes**: Complex file exceeds token limits despite row count check
- **Solutions**:
  - Force Pandas mode even for complex files
  - Split sheet into smaller ranges and process separately
  - Extract only essential columns before HTML conversion

### Incorrect Header Detection
- **Symptom**: Wrong columns or data shifted
- **Causes**: Unusual header patterns not caught by sampling
- **Solutions**:
  - Manually specify header row if known
  - Increase sample size beyond 20 rows
  - Use HTML mode for better structure understanding

## Dependencies

Required Python packages:
- `openpyxl` - Metadata scanning and Excel file manipulation
- `pandas` - High-speed data reading and manipulation

## Resources

This skill includes:
- `scripts/complexity_analyzer.py` - Standalone executable for complexity analysis
- `references/smart_excel_router.py` - Complete implementation reference with both processing paths
