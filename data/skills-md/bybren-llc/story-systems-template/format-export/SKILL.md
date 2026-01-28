---
name: format-export
wtfbId: wtfb:format-export
description: |
  This skill provides screenplay export procedures for PDF, FDX, and HTML.
  Covers Better Fountain VS Code extension, afterwriting CLI, and Highland
  for converting Fountain files to industry-standard delivery formats.

  Use when: exporting screenplay to PDF, converting to Final Draft (FDX),
  generating HTML preview, or preparing scripts for delivery.
---

# Format Export Skill

## Invocation Triggers
Apply this skill when:
- Exporting screenplay to PDF
- Converting to Final Draft (FDX)
- Generating HTML preview
- Preparing scripts for delivery

## Recommended: Better Fountain Extension

The simplest export method uses the [Better Fountain](https://marketplace.visualstudio.com/items?itemName=piersdeseilligny.betterfountain) VS Code extension:

| Format | Command Palette Action |
|--------|------------------------|
| PDF | `Fountain: Export to PDF` |
| FDX | `Fountain: Export to FDX` |
| HTML | `Fountain: Export to HTML` |

**Steps:**
1. Open `.fountain` file in VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on macOS)
3. Type the export command
4. Choose output location

> **Extension**: [Better Fountain on VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=piersdeseilligny.betterfountain)

## Export Formats Overview

| Format | Extension | Purpose | Tools |
|--------|-----------|---------|-------|
| PDF | .pdf | Industry standard delivery | Better Fountain, afterwriting, Highland |
| FDX | .fdx | Final Draft import | Better Fountain, screenplain, Highland |
| HTML | .html | Web preview/sharing | Better Fountain, afterwriting |
| Plain Text | .txt | Accessibility, archival | direct copy |

## PDF Export

### Industry Standard Format
- **Font:** Courier 12pt
- **Margins:** 1.5" left, 1" right, 1" top/bottom
- **Page Size:** US Letter (8.5" x 11")
- **Page Numbers:** Top right, starting page 2

### Better Fountain (Recommended)
In VS Code: `Ctrl+Shift+P` → "Fountain: Export to PDF"

### CLI: afterwriting (for automation)
```bash
# Install
npm install -g afterwriting

# Basic PDF export
afterwriting --source screenplay.fountain --pdf

# With configuration
afterwriting --source screenplay.fountain --pdf --config pdf-config.json

# Output to specific file
afterwriting --source screenplay.fountain --pdf --output script.pdf
```

### PDF Configuration (pdf-config.json)
```json
{
  "print_title_page": true,
  "print_profile": "default",
  "print_header": "",
  "print_footer": "",
  "print_watermark": "",
  "print_dialogue_numbers": false,
  "print_notes": false,
  "print_sections": false,
  "print_synopses": false,
  "scenes_numbers": "none",
  "each_scene_on_new_page": false
}
```

### Highland (macOS)
1. Open .fountain file in Highland
2. File → Export → PDF
3. Configure options in preferences

### Wrap (macOS)
1. Open .fountain file
2. File → Export → PDF

## FDX Export (Final Draft XML)

### Purpose
- Import into Final Draft software
- Collaboration with Final Draft users
- Industry compatibility

### Better Fountain (Recommended)
In VS Code: `Ctrl+Shift+P` → "Fountain: Export to FDX"

### CLI: screenplain (for automation)
```bash
# One-time installation (requires Python 3.8+ and pipx)
pipx install screenplain

# Export to FDX
screenplain --format fdx screenplay.fountain output.fdx
```

> **Note**: `afterwriting` does NOT support FDX export. Use Better Fountain, screenplain, or Highland.

### Highland Export (macOS)
[Highland 2](https://quoteunquoteapps.com/highland-2/) offers native FDX export:
1. Open `.fountain` file in Highland 2
2. File → Export → Final Draft

### Compatibility Notes
- Basic Fountain elements export cleanly
- Notes, sections, synopses may not transfer
- Review formatting after import to Final Draft
- Scene numbers transfer if present

## HTML Export

### Purpose
- Web-based reading
- Easy sharing via URL
- Print from browser

### Better Fountain (Recommended)
In VS Code: `Ctrl+Shift+P` → "Fountain: Export to HTML"

### CLI: afterwriting (for automation)
```bash
afterwriting --source screenplay.fountain --html
```

### HTML Configuration
```json
{
  "html_use_paper_size": true,
  "html_scenes_numbers": "none",
  "html_print_dialogue_numbers": false
}
```

### Custom HTML Template
For custom styling, process Fountain to JSON then apply template:
```bash
afterwriting --source screenplay.fountain --fountain --output screenplay.json
# Then apply custom HTML template to JSON
```

## Export Workflow

### Pre-Export Checklist
- [ ] Script Supervisor approval
- [ ] Standards Reviewer approval
- [ ] All [[notes]] resolved or intentional
- [ ] Title page complete and current
- [ ] Fountain syntax validated

### Export Process
```markdown
1. Validate Fountain file
2. Run export command
3. Verify output file created
4. Open and review output
5. Check page count
6. Verify title page
7. Sample check formatting
8. Package for delivery
```

### Post-Export Verification
- [ ] File opens without errors
- [ ] Page count as expected
- [ ] Title page correct
- [ ] Character names format correctly
- [ ] Dialogue layout proper
- [ ] Transitions right-aligned
- [ ] No orphaned elements

## Version Naming

### Convention
```
[Title]_v[Major].[Minor]_[YYYYMMDD].[ext]
```

### Examples
```
Seoul_Identity_v1.0_20251227.pdf
Seoul_Identity_v1.1_20251228.pdf
Seoul_Identity_v2.0_20260115.pdf
Seoul_Identity_v2.0_20260115.fdx
```

### Major vs. Minor
- **Major (1.0 → 2.0):** Significant rewrite
- **Minor (1.0 → 1.1):** Polish, small changes

## Platform-Specific Notes

### macOS
- Highland: Best native Fountain support
- Wrap: Simple, clean interface
- Slugline: Also available

### Windows/Linux
- afterwriting CLI: Cross-platform
- Trelby: Open source screenwriting
- WriterSolo: Online option

### Online Tools
- afterwriting.com: Web-based export
- WriterSolo: Cloud-based option

## Troubleshooting

### PDF Issues
| Problem | Solution |
|---------|----------|
| Wrong fonts | Check PDF config, ensure Courier |
| Bad margins | Verify config matches standards |
| Missing title page | Enable in config |
| Notes appearing | Disable print_notes |

### FDX Issues
| Problem | Solution |
|---------|----------|
| Elements misformatted | Review in Final Draft, adjust |
| Notes missing | Expected - FDX doesn't support all |
| Dual dialogue broken | May need manual fix in FD |

### HTML Issues
| Problem | Solution |
|---------|----------|
| Print looks wrong | Use paper size option |
| Styling off | Use default CSS or customize |

## Export Scripts

> **Note**: For manual exports, use the Better Fountain extension. The scripts below are for CI/CD automation.

### Bash Export All Formats
```bash
#!/bin/bash
SCRIPT="screenplay.fountain"
NAME="Seoul_Identity"
DATE=$(date +%Y%m%d)
VERSION="1.0"

# PDF export (afterwriting)
afterwriting --source $SCRIPT --pdf --output "${NAME}_v${VERSION}_${DATE}.pdf"

# FDX export (screenplain - requires pipx install screenplain)
screenplain --format fdx $SCRIPT "${NAME}_v${VERSION}_${DATE}.fdx"

# HTML export (afterwriting)
afterwriting --source $SCRIPT --html --output "${NAME}_v${VERSION}_${DATE}.html"

echo "Export complete:"
ls -la ${NAME}_v${VERSION}_${DATE}.*
```

## Export Checklist

### PDF Delivery
- [ ] Page count within target
- [ ] Title page per standards
- [ ] No scene numbers (spec)
- [ ] No WGA numbers (spec)
- [ ] Filename follows convention
- [ ] File under 10MB

### FDX Delivery
- [ ] Opens in Final Draft
- [ ] Elements formatted correctly
- [ ] Scene headings intact
- [ ] Dialogue blocks correct

### Competition Submission
- [ ] Format matches guidelines
- [ ] Page count within limits
- [ ] Anonymous if required
- [ ] Filename as specified
