---
name: markdown-crossref-validator
description: Validate cross-references in markdown documents, ensuring links and references point to existing sections, headings, or files.
---

# Markdown Cross-Reference Validator

## When to use this skill
Use this skill when the user asks to validate or check cross-references in markdown files. This includes verifying that internal links (e.g., [text](#heading)) point to existing headings, and that file references (e.g., [text](file.md)) point to existing files.

## Algorithm & Workflow

### Phase 1: Document Preparation
1. **Identify target file(s)**: Determine which markdown file(s) to validate
2. **Read content**: Load the full markdown document(s) into memory
3. **Establish base path**: Determine the root directory for relative file references

### Phase 2: Heading Extraction
1. **Scan for headings**: Find all lines matching regex `^#+\s+(.*)$`
2. **Build anchor map**: For each heading:
   - Extract heading text: `# Introduction` → `Introduction`
   - Convert to anchor ID: lowercase, replace spaces with hyphens, remove special chars
   - Store mapping: `introduction` → heading level (1-6)
3. **Handle special cases**: Account for heading IDs, custom anchors using HTML comments
4. **Normalize anchors**: Ensure consistent anchor formatting for comparison

### Phase 3: Link Extraction
1. **Find all link patterns**:
   - Inline links: `[text](url)` using regex `\[([^\]]+)\]\(([^)]+)\)`
   - Reference links: `[text][ref]` using regex `\[([^\]]+)\]\[([^\]]+)\]`
   - Reference definitions: `[ref]: url` using regex `^\s*\[([^\]]+)\]:\s*(.+)$`
   - HTML links: `<a href="url">text</a>`
2. **Categorize links**:
   - Internal anchors: `#heading-name`
   - File references: `path/to/file.md`
   - Combined: `path/to/file.md#section`
   - External: `http://...`, `https://...`
   - Relative path: `../other.md`

### Phase 4: Link Validation

#### For Internal Anchor Links (`#anchor`)
1. Extract anchor identifier
2. Normalize anchor (lowercase, hyphenate)
3. Check against anchor map from Phase 2
4. Record as ✓ Valid or ✗ Broken

#### For File References (`path/to/file.md`)
1. Resolve relative path from current document location
2. Check file existence in project
3. If file + anchor (`path/to/file.md#section`):
   - Verify file exists
   - Parse target file for headings
   - Verify anchor exists in target file
4. Record as ✓ Valid or ✗ Broken with reason

#### For External Links (`http://`, `https://`)
1. Mark as external (scope: not validated for internal consistency)
2. Optionally note for manual review

### Phase 5: Issue Categorization
Classify all broken references by type:
- **Missing Heading**: Anchor exists but no matching heading in file
- **Missing File**: File reference path doesn't exist
- **Invalid Anchor in Target**: File exists but referenced section doesn't
- **Malformed Reference**: Link syntax is invalid or unparseable

### Phase 6: Report Generation
1. **Create summary**: Total links checked, valid count, broken count, broken percentage
2. **Group issues**: Organize by file and issue type
3. **Provide context**: Show the line number and actual link text
4. **Suggest fixes**: Recommend corrected anchor names or file paths
5. **Verify output**: Ensure report is complete and accurate

## Validation & Verification

### Validation Checklist
- ✅ All markdown files are readable and parseable
- ✅ All heading anchors are properly extracted and normalized
- ✅ All link patterns (inline, reference, HTML) are detected
- ✅ Internal anchor references are validated
- ✅ File references exist and are properly resolved
- ✅ Cross-file anchors are verified in target files
- ✅ Report categorizes all issues by type
- ✅ All broken references are identified with context

### Report Verification Steps
1. Random sample 5-10 links and manually verify they match report findings
2. Check that issue count matches actual broken references
3. Verify all line numbers and file paths are accurate
4. Confirm suggestions for fixes are actionable

## Concrete Examples

### Example 1: Simple Document with Internal Links

**Input: `docs/guide.md`**
```markdown
# Getting Started Guide

## Table of Contents
- [Installation](#installation)
- [Configuration](#configuration)
- [Advanced Setup](#advanced-setup)

## Installation

Follow these steps to install...

## Configuration

See [Installation](#installation) for prerequisites.

## Advanced Setup

For complex scenarios, refer to [Config](#configuration).

## Troubleshooting

Check [Non-existent Section](#missing-section) for help.
```

**Validation Report:**
```
═══════════════════════════════════════════════════════════
MARKDOWN CROSS-REFERENCE VALIDATION REPORT
═══════════════════════════════════════════════════════════

File: docs/guide.md
Scan Date: 2024-02-21
Status: ✓ VALIDATED WITH ISSUES

───────────────────────────────────────────────────────────
SUMMARY
───────────────────────────────────────────────────────────
Total Links Found:     5
Valid References:      4
Broken References:     1
Validation Rate:       80%

───────────────────────────────────────────────────────────
VALID REFERENCES ✓
───────────────────────────────────────────────────────────

✓ Line 4: [Installation](#installation)
  Type: Internal anchor
  Status: Heading "Installation" found at line 11

✓ Line 5: [Configuration](#configuration)
  Type: Internal anchor
  Status: Heading "Configuration" found at line 18

✓ Line 5: [Advanced Setup](#advanced-setup)
  Type: Internal anchor
  Status: Heading "Advanced Setup" found at line 22

✓ Line 19: [Installation](#installation)
  Type: Internal anchor (cross-reference)
  Status: Valid, heading exists

───────────────────────────────────────────────────────────
BROKEN REFERENCES ✗
───────────────────────────────────────────────────────────

✗ Line 26: [Non-existent Section](#missing-section)
  Type: Internal anchor
  Issue: MISSING HEADING
  Anchor: #missing-section
  Status: No heading found matching "missing-section"
  
  Suggestion: Available sections in document:
    - #getting-started-guide (h1)
    - #table-of-contents (h2)
    - #installation (h2)
    - #configuration (h2)
    - #advanced-setup (h2)
    - #troubleshooting (h2)

───────────────────────────────────────────────────────────
ANCHOR MAPPING
───────────────────────────────────────────────────────────
getting-started-guide (Level 1) → Line 1
table-of-contents (Level 2) → Line 3
installation (Level 2) → Line 11
configuration (Level 2) → Line 18
advanced-setup (Level 2) → Line 22
troubleshooting (Level 2) → Line 25

═══════════════════════════════════════════════════════════
```

### Example 2: Cross-File References

**Input: Multiple files in `docs/` directory**

**Files:**
- `docs/index.md` - Main documentation index
- `docs/guide/installation.md` - Installation guide
- `docs/guide/config.md` - Configuration guide
- `docs/api/endpoints.md` - API reference

**Content: `docs/index.md`**
```markdown
# Documentation Index

- [Installation Guide](guide/installation.md)
- [Configuration](guide/config.md#configuration)
- [API Reference](api/endpoints.md)
- [Getting Help](support/help.md)
- [Basic Setup](#quick-start)

## Quick Start

See [Installation](guide/installation.md#system-requirements) for details.
```

**Validation Report:**
```
═══════════════════════════════════════════════════════════
MARKDOWN CROSS-REFERENCE VALIDATION REPORT
═══════════════════════════════════════════════════════════

File: docs/index.md
Scan Date: 2024-02-21
Status: ⚠ VALIDATED WITH CRITICAL ISSUES

───────────────────────────────────────────────────────────
SUMMARY
───────────────────────────────────────────────────────────
Total Links Found:     6
Valid References:      3
Broken References:     3
Validation Rate:       50%

───────────────────────────────────────────────────────────
VALID REFERENCES ✓
───────────────────────────────────────────────────────────

✓ Line 3: [Installation Guide](guide/installation.md)
  Type: File reference
  Path: docs/guide/installation.md
  Status: File exists (2.5 KB)

✓ Line 4: [Configuration](guide/config.md#configuration)
  Type: File with anchor
  Path: docs/guide/config.md
  Anchor: #configuration
  Status: File exists, heading found in target

✓ Line 8: [Installation](guide/installation.md#system-requirements)
  Type: File with anchor
  Path: docs/guide/installation.md
  Anchor: #system-requirements
  Status: File exists, heading found in target

───────────────────────────────────────────────────────────
BROKEN REFERENCES ✗
───────────────────────────────────────────────────────────

✗ Line 5: [API Reference](api/endpoints.md)
  Type: File reference
  Issue: MISSING FILE
  Path: docs/api/endpoints.md
  Status: File not found in project
  
  Suggestion: Did you mean?
    - docs/api/reference.md (exists)
    - docs/endpoints.md (exists)

✗ Line 6: [Getting Help](support/help.md)
  Type: File reference
  Issue: MISSING FILE
  Path: docs/support/help.md
  Status: File not found in project
  
  Suggestion: No similar files found. Check path spelling.

✗ Line 7: [Basic Setup](#quick-start)
  Type: Internal anchor
  Issue: MISSING HEADING
  Anchor: #quick-start
  Status: Anchor not found (likely typo: #quickstart exists)
  
  Suggestion: Did you mean #quickstart?

───────────────────────────────────────────────────────────
CROSS-FILE ANALYSIS
───────────────────────────────────────────────────────────

Scanned 4 files in project:
- docs/index.md (6 links)
- docs/guide/installation.md (12 links, all valid)
- docs/guide/config.md (8 links, 1 broken)
- docs/api/reference.md (5 links, all valid)

Cross-file reference summary:
- Files referenced: 4
- Valid file references: 3
- Invalid file references: 2
- Unresolvable anchors in targets: 0

═══════════════════════════════════════════════════════════
```

### Example 3: Reference-Style Links

**Input: `docs/readme.md`**
```markdown
# Project Documentation

See the [Getting Started][gs] guide for setup instructions.

For API details, check [API Reference][api] or [CLI Reference][cli].

Invalid reference: [Missing Reference][unknown]

[gs]: guide/getting-started.md#prerequisites
[api]: https://api.example.com
[cli]: guide/cli.md#commands
```

**Validation Report:**
```
═══════════════════════════════════════════════════════════
MARKDOWN CROSS-REFERENCE VALIDATION REPORT
═══════════════════════════════════════════════════════════

File: docs/readme.md
Scan Date: 2024-02-21
Type: Reference-style links
Status: ✓ VALIDATED WITH ISSUES

───────────────────────────────────────────────────────────
SUMMARY
───────────────────────────────────────────────────────────
Total Links Found:     4
Valid References:      3
Broken References:     1
External Links:        1
Validation Rate:       75%

───────────────────────────────────────────────────────────
REFERENCE DEFINITIONS FOUND
───────────────────────────────────────────────────────────

[gs] → guide/getting-started.md#prerequisites (Line 9)
[api] → https://api.example.com (Line 10, External)
[cli] → guide/cli.md#commands (Line 11)

───────────────────────────────────────────────────────────
VALIDATION RESULTS
───────────────────────────────────────────────────────────

✓ [Getting Started][gs] (Line 3)
  Reference defined: Yes
  Target: guide/getting-started.md#prerequisites
  File status: Exists
  Anchor status: Valid
  Result: VALID

✓ [API Reference][api] (Line 5)
  Reference defined: Yes
  Target: https://api.example.com
  Type: External URL
  Result: EXTERNAL (not validated)

✓ [CLI Reference][cli] (Line 5)
  Reference defined: Yes
  Target: guide/cli.md#commands
  File status: Exists
  Anchor status: Valid
  Result: VALID

✗ [Missing Reference][unknown] (Line 7)
  Reference defined: No
  Status: UNDEFINED REFERENCE
  Issue: Reference label "[unknown]" not found in definitions
  
  Suggestion: Available references in document:
    - [gs]
    - [api]
    - [cli]

═══════════════════════════════════════════════════════════
```

## Tools to use
- Use file reading tools to access markdown files.
- Use grep or parsing to extract links and headings.
- For file existence, use directory listing tools.

## Quick Reference: Link Patterns

| Pattern | Example | Type |
|---------|---------|------|
| Inline link | `[text](#anchor)` | Internal anchor |
| Inline file | `[text](file.md)` | File reference |
| Combined | `[text](file.md#section)` | File with anchor |
| Reference-style | `[text][ref]` + `[ref]: url` | Reference link |
| HTML link | `<a href="#id">text</a>` | HTML anchor |
| External | `[text](https://example.com)` | External URL |