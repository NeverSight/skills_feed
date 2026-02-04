---
name: pandoc-pdf-generation
description: PDF generation from markdown via Pandoc/XeLaTeX. TRIGGERS - markdown for PDF, print document, pandoc, xelatex, section numbering, table of contents, page breaks.
---

# Pandoc PDF Generation

## Overview

Generate professional PDF documents from Markdown using Pandoc with the XeLaTeX engine. This skill covers automatic section numbering, table of contents, bibliography management, LaTeX customization, and common troubleshooting patterns learned through production use.

## When to Use This Skill

Use this skill when:

- Converting Markdown to PDF with professional formatting requirements
- Needing automatic section numbering and table of contents
- Managing citations and bibliographies without manual duplication
- Controlling table formatting and page breaks in LaTeX output
- Building automated PDF generation workflows

## Quick Start: Universal Build Script

### Single Source of Truth Pattern

This skill provides production-proven assets in `${CLAUDE_PLUGIN_ROOT}/skills/pandoc-pdf-generation/assets/`:

- `table-spacing-template.tex` - Production-tuned LaTeX preamble (booktabs, colortbl, ToC fixes)
- `build-pdf.sh` - Universal auto-detecting build script

### From Any Project

```bash
/usr/bin/env bash << 'DETECT_EOF'
# Create symlink once per project (git-friendly)
ln -s ${CLAUDE_PLUGIN_ROOT}/skills/pandoc-pdf-generation/assets/build-pdf.sh build-pdf.sh

# Auto-detect single .md file in directory (landscape default)
./build-pdf.sh

# Portrait mode
./build-pdf.sh --portrait document.md

# Monospace font for ASCII diagrams
./build-pdf.sh --monospace diagrams.md

# Explicit input/output
./build-pdf.sh input.md output.pdf
DETECT_EOF
```

**Options:**

| Flag             | Description                                                |
| ---------------- | ---------------------------------------------------------- |
| `--landscape`    | Landscape orientation (default)                            |
| `--portrait`     | Portrait orientation                                       |
| `--monospace`    | Use DejaVu Sans Mono - ideal for ASCII diagrams            |
| `--hide-details` | Hide `<details>` blocks (e.g., graph-easy source) from PDF |
| `-h, --help`     | Show help message                                          |

**Features:**

- ✅ Auto-detects input file (if single .md exists)
- ✅ Auto-detects bibliography (`references.bib`) and CSL files
- ✅ Always uses production-proven LaTeX preamble from skill
- ✅ Pre-flight checks (pandoc, xelatex, files exist)
- ✅ Post-build validation (file size, page count)
- ✅ Code blocks stay on same page (no splitting across pages)
- ✅ Lua filter to hide `<details>` blocks from PDF output

### Landscape PDF (Quick Command)

For landscape PDFs with blue hyperlinks (no build-pdf.sh dependency):

```bash
pandoc file.md -o file.pdf \
  --pdf-engine=xelatex \
  -V geometry:a4paper,landscape \
  -V geometry:margin=1in \
  -V fontsize=11pt \
  -V mainfont="DejaVu Sans" \
  -V colorlinks=true \
  -V linkcolor=blue \
  -V urlcolor=blue \
  --toc --toc-depth=2 \
  --number-sections
```

**Use landscape for**: Wide data tables, comparison matrices, technical docs with code blocks.

### Manual Command (With LaTeX Preamble)

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF'
pandoc document.md \
  -o document.pdf \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=3 \
  --number-sections \
  -V geometry:margin=1in \
  -V mainfont="DejaVu Sans" \
  -H ${CLAUDE_PLUGIN_ROOT}/skills/pandoc-pdf-generation/assets/table-spacing-template.tex
SKILL_SCRIPT_EOF
```

---

## ASCII Diagrams: Always Use graph-easy

**CRITICAL**: Never manually type ASCII diagrams. Always use the `itp:graph-easy` skill.

Manual ASCII art causes alignment issues in PDFs. The graph-easy skill ensures:

- Proper boxart character alignment
- Consistent spacing
- Reproducible output

```bash
# Invoke the skill for general diagrams
Skill(itp:graph-easy)

# For ADR architecture diagrams
Skill(itp:adr-graph-easy-architect)
```

**Also important**: Keep annotations OUTSIDE code blocks. Don't add inline comments like `# contains: file1, file2` inside diagram code blocks - they break alignment.

---

## Hiding Content for PDF Output

Use `--hide-details` to remove `<details>` blocks from PDF output. This is useful when:

- **graph-easy source blocks**: Keep source in markdown for diagram regeneration, but hide from printed PDFs
- **Technical implementation notes**: Show in web/markdown view, hide from printed handouts
- **Collapsible sections**: HTML `<details>` tags don't render as collapsible in PDF

**Usage:**

```bash
./build-pdf.sh --hide-details document.md
```

**Markdown pattern:**

````markdown
## My Section

```diagram
┌─────┐     ┌─────┐
│ Box │ ──> │ Box │
└─────┘     └─────┘
```
````

<details>
<summary>graph-easy source</summary>

```
[Box] -> [Box]
```

</details>
```

With `--hide-details`, the entire `<details>` block is stripped from PDF output while remaining visible in markdown/HTML.

---

## Verification Checklist

Before considering a PDF "done", verify:

**Pre-Generation:**

- [ ] No manual section numbering in markdown (use `--number-sections`)
- [ ] All ASCII diagrams generated via `itp:graph-easy` skill
- [ ] Annotations are outside code blocks, not inside

**Post-Generation:**

- [ ] Open PDF and visually inspect each page
- [ ] Verify diagrams don't break across pages
- [ ] Check section numbering is correct (no "1. 1. Title" duplication)
- [ ] Confirm bullet lists render as bullets, not inline dashes

**Pre-Print:**

- [ ] Get user approval before printing
- [ ] Confirm orientation preference (landscape/portrait)
- [ ] Confirm duplex preference (one-sided/two-sided)

---

## Printing Workflow

Always let the user review the PDF before printing.

**Open for review:**

```bash
open output.pdf
```

**Print one-sided (simplex):**

```bash
lpr -P "PRINTER_NAME" -o Duplex=None output.pdf
```

**Print two-sided (duplex):**

```bash
lpr -P "PRINTER_NAME" -o Duplex=DuplexNoTumble output.pdf  # Long-edge binding
lpr -P "PRINTER_NAME" -o Duplex=DuplexTumble output.pdf    # Short-edge binding
```

**Find printer name:**

```bash
lpstat -p -d
```

**Never print without user approval** - this wastes paper if issues exist.

---

## Reference Documentation

For detailed information, see:

- [Core Development Principles](./references/core-principles.md) - **START HERE** - Universal principles learned from production failures
- [Markdown for PDF](./references/markdown-for-pdf.md) - Markdown structure patterns for clean landscape PDFs
- [YAML Front Matter Structure](./references/yaml-structure.md) - YAML metadata patterns
- [LaTeX Customization](./references/latex-parameters.md) - Preamble and table formatting
- [Bibliography & Citations](./references/bibliography-citations.md) - BibTeX and CSL styles
- [Document Patterns](./references/document-patterns.md) - Document type templates
- [Troubleshooting](./references/troubleshooting-pandoc.md) - Common issues and fixes

---

## Troubleshooting

| Issue                         | Cause                        | Solution                                          |
| ----------------------------- | ---------------------------- | ------------------------------------------------- |
| Font not found                | DejaVu Sans not installed    | `brew install font-dejavu`                        |
| xelatex not found             | MacTeX not installed         | `brew install --cask mactex`                      |
| Table breaks across pages     | Missing longtable package    | Include table-spacing-template.tex preamble       |
| Double section numbers        | Manual numbering in markdown | Remove manual numbers, use --number-sections only |
| ASCII diagram misaligned      | Manual ASCII art             | Use graph-easy skill for all diagrams             |
| Bullet list renders as dashes | Markdown formatting issue    | Check for proper blank lines before lists         |
| Bibliography not rendering    | Missing references.bib       | Create .bib file or remove --bibliography flag    |
| PDF file size too large       | Embedded fonts               | Use --pdf-engine-opt=-dEmbedAllFonts=false        |
