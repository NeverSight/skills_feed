---
name: hwp
description: This skill should be used when the user wants to view contents of HWP/HWPX files (Korean word processor documents), mentions ".hwp" or ".hwpx" file paths, asks to "read hwp", "read hwpx", "open hwp", "open hwpx", or needs to extract text from Korean word processor documents.
argument-hint: [file-path]
metadata:
    short-description: Extract and display HWP/HWPX document contents
user-invocable: true
---

# HWP/HWPX Document Reader

This skill reads Korean Hangul Word Processor files (.hwp, .hwpx) and prepares to respond based on the content using [pyhwp2md](https://github.com/pitzcarraldo/pyhwp2md).

## Supported Formats

| Format | Extension | Description |
|--------|-----------|-------------|
| HWP | `.hwp` | Binary format (HWP 5.0+) |
| HWPX | `.hwpx` | XML-based format (Hangul 2014+) |

## Workflow

> **CRITICAL**: NEVER run `uvx`, `pipx`, or `pip` commands directly. ALWAYS use the complete bash script below which automatically detects and uses the correct tool.

### 1. Verify File Exists

```bash
ls -la "[file-path]"
```

### 2. Detect and Extract Content

**Run this EXACT script** (do not modify or run individual commands):

```bash
TOOL=$(command -v uvx >/dev/null 2>&1 && echo "uvx" || (command -v pipx >/dev/null 2>&1 && echo "pipx" || (command -v pip >/dev/null 2>&1 && echo "pip" || echo "none"))) && case $TOOL in uvx) uvx pyhwp2md "[file-path]" ;; pipx) pipx run pyhwp2md "[file-path]" ;; pip) pip install -q pyhwp2md && pyhwp2md "[file-path]" ;; *) echo "Error: No Python package runner found" ;; esac
```

### 3. Handle Output Based on Size

**If content fits in context**: Use the stdout output directly to respond to user queries.

**If content is too large for context**: Save to a temporary file using this script:

```bash
TOOL=$(command -v uvx >/dev/null 2>&1 && echo "uvx" || (command -v pipx >/dev/null 2>&1 && echo "pipx" || (command -v pip >/dev/null 2>&1 && echo "pip" || echo "none"))) && case $TOOL in uvx) uvx pyhwp2md "[file-path]" -o /tmp/extracted_content.md ;; pipx) pipx run pyhwp2md "[file-path]" -o /tmp/extracted_content.md ;; pip) pyhwp2md "[file-path]" -o /tmp/extracted_content.md ;; esac
```

Then read the file in chunks as needed to answer user questions.

## Technical Requirements

| Requirement | Version | Note |
|-------------|---------|------|
| Python | 3.10+ | Required |
| uv/pipx/pip | Latest | Any one of these |

## Limitations

- **Images**: Not yet supported
- **Links**: Partial support
- **Formatting**: Styles, colors, and fonts are not preserved

## References

- [pyhwp2md GitHub](https://github.com/pitzcarraldo/pyhwp2md)
- [pyhwp2md PyPI](https://pypi.org/project/pyhwp2md/)
