---
name: md-slides
description: Convert Markdown to presentation slides in multiple formats (PDF, PPTX, HTML). Use when user mentions slides, presentations, Marp, Beamer, or wants to generate PDF/PPTX from markdown. Supports flavors (audience, style, language) and visual comparisons.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Markdown Universal Slides Generator

Convert Markdown source files to presentation slides in multiple formats.

> **First Step:** Always read and apply a visual template from `templates/visual/` before generating slides. This ensures consistent visual output.

## Core Concept

**One source, multiple outputs:**
```
slides.md → Marp/Pandoc/python-pptx → PDF / PPTX / HTML
```

## Slide Flavors

When creating slides, ask or infer these parameters to customize output:

### Audience Types

| Audience | Characteristics |
|----------|-----------------|
| **manager** | Executive summary, key metrics, recommendations, minimal technical details |
| **developer** | Code examples, technical details, implementation specifics |
| **learner** | Step-by-step explanations, examples, progressive complexity |
| **general** | Balanced, accessible language, visual explanations |

### Visual Styles

| Style | Theme | Characteristics |
|-------|-------|-----------------|
| **professional** | `gaia` | Clean, corporate colors, structured layouts |
| **minimal** | `default` | Simple, lots of whitespace, focus on content |
| **visual** | `gaia` + custom CSS | Rich graphics, comparisons, diagrams, screenshots |
| **academic** | Beamer `metropolis` | Formal, math-friendly, citations |

### Language Options

| Option | Usage |
|--------|-------|
| `zh` | Chinese content, Chinese-friendly themes |
| `en` | English content |
| `mixed` | Bilingual titles/subtitles |

### Content Density

| Length | Slides | Bullets per slide |
|--------|--------|-------------------|
| **brief** | 5-8 | 3-4 |
| **standard** | 10-15 | 4-6 |
| **detailed** | 20+ | 5-8 |

## Flavor Examples

**Manager presentation (Chinese):**
```yaml
audience: manager
style: professional
language: zh
length: standard
```
→ Use Gaia theme, executive summary, key findings, recommendations

**Technical tutorial (English):**
```yaml
audience: developer
style: minimal
language: en
length: detailed
```
→ Use default theme, code examples, step-by-step

**Research showcase:**
```yaml
audience: general
style: visual
language: mixed
length: standard
```
→ Use Gaia with custom CSS, screenshots, comparisons

## Prerequisites Check

Before generating output, verify required tools are installed:

| Tool | Check | Linux | macOS |
|------|-------|-------|-------|
| Marp | `marp --version` | `npm i -g @marp-team/marp-cli` | `brew install marp-cli` |
| Pandoc | `pandoc --version` | `sudo apt install pandoc` | `brew install pandoc` |
| XeLaTeX | `xelatex --version` | `sudo apt install texlive-full` | `brew install --cask mactex` |
| pdftoppm | `pdftoppm -v` | `sudo apt install poppler-utils` | `brew install poppler` |

**Workflow:**
1. Check if required tool exists before running
2. If missing, detect OS (`uname -s`) and show install command
3. After install, verify with version check

## Available Tools & Best Use Cases

| Tool | Best For | Output Formats | Command |
|------|----------|----------------|---------|
| **Marp** | Modern slides, LLM workflows | PDF, PPTX, HTML | `marp input.md -o output.{pdf,pptx,html}` |
| **Pandoc Beamer** | Academic, math-heavy | PDF | `pandoc input.md -t beamer --pdf-engine=xelatex -o output.pdf` |
| **Pandoc PPTX** | Editable PowerPoint | PPTX | `pandoc input.md -o output.pptx` |
| **reveal.js** | Web presentations | HTML | `pandoc input.md -t revealjs -s -o output.html` |

## Quick Commands

### Generate with Marp (Recommended)

```bash
# PDF output
marp slides.md -o slides.pdf

# PPTX output
marp slides.md -o slides.pptx

# HTML output
marp slides.md -o slides.html

# With custom theme
marp slides.md --theme gaia -o slides.pdf

# Allow local images
marp slides.md -o slides.pdf --allow-local-files
```

### Generate with Pandoc Beamer

```bash
# Basic PDF
pandoc slides.md -t beamer -o slides.pdf

# With XeLaTeX (better font support, required for CJK)
pandoc slides.md -t beamer --pdf-engine=xelatex -o slides.pdf

# With theme
pandoc slides.md -t beamer -V theme:metropolis -o slides.pdf

# CJK support
pandoc slides.md -t beamer --pdf-engine=xelatex \
  -V mainfont="Noto Sans CJK SC" -o slides.pdf
```

### Generate with reveal.js

```bash
pandoc slides.md -t revealjs -s -o slides.html
pandoc slides.md -t revealjs -s -V theme=moon -o slides.html
```

## Visual Templates (Visual Consistency)

**IMPORTANT:** Before generating slides, always use a visual template for consistent rendering.

Visual templates are in `templates/visual/`:
- `default-zh.md` — Chinese slides
- `default-en.md` — English slides

### How to Use

1. Read the appropriate template: `templates/visual/default-{lang}.md`
2. Copy its frontmatter exactly (don't modify)
3. Follow the gotchas listed in the template

### Quick Reference (Chinese)

```yaml
---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section {
    font-family: 'Noto Sans CJK SC', 'Microsoft YaHei', sans-serif;
  }
  section.small-table table { font-size: 0.85em; }
---
```

### Rules for Consistent Output

| Rule | Reason |
|------|--------|
| Use frontmatter exactly as provided | Ensures consistent rendering |
| Keep font stack as `'Noto Sans CJK SC', 'Microsoft YaHei', sans-serif` | Consistent date/number rendering |
| End slides with content, not directives | Clean final page |
| Use `<!-- _class: lead -->` only on title slide | Proper centering where needed |

### Custom Looks

Users can add custom visual templates to `templates/visual/`. See `templates/visual/README.md`.

---

## Markdown Slide Format

### Marp Format

```markdown
---
marp: true
theme: default  # or gaia, uncover
paginate: true
---

# Slide Title

Content here

---

# Next Slide

- Bullet points
- More content
```

### Pandoc/Beamer Format

```markdown
---
title: Presentation Title
author: Author Name
date: 2026
---

# Section Title

## Slide Title

- Content
- More content

---

## Another Slide

Content continues
```

## Generating Visual Showcases

When user wants to compare tools visually:

1. **Create sample slides** with representative content:
   - Title slide with Chinese/English
   - Code highlighting example
   - Math formulas
   - Tables

2. **Generate outputs** from all tools:
   ```bash
   # Marp outputs
   marp sample.md -o output/marp.pdf
   marp sample.md -o output/marp.pptx

   # Beamer outputs
   pandoc sample.md -t beamer --pdf-engine=xelatex -o output/beamer.pdf

   # Pandoc PPTX
   pandoc sample.md -o output/pandoc.pptx
   ```

3. **Create screenshots** for comparison:
   ```bash
   pdftoppm -png -f 1 -l 1 -r 150 output/marp.pdf screenshots/marp
   pdftoppm -png -f 1 -l 1 -r 150 output/beamer.pdf screenshots/beamer
   ```

4. **Build comparison presentation** with embedded screenshots

## Tool Selection Guide

| Scenario | Recommended Tool |
|----------|------------------|
| LLM/Agent automation | Marp |
| Academic/Math-heavy | Pandoc Beamer |
| Editable PPTX needed | Pandoc PPTX or python-pptx |
| Web presentation | reveal.js |
| Enterprise templates | python-pptx |
| Quick prototyping | Marp |

## LLM Integration Pattern

```python
import subprocess

def generate_slides(content: str, output_path: str):
    """Generate slides from LLM-produced content."""
    md_content = f"""---
marp: true
theme: gaia
paginate: true
---

{content}
"""
    with open("/tmp/slides.md", "w") as f:
        f.write(md_content)

    subprocess.run(["marp", "/tmp/slides.md", "-o", output_path], check=True)
    return output_path
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Chinese characters broken (Beamer) | Use `--pdf-engine=xelatex` with CJK font |
| Images not loading (Marp) | Add `--allow-local-files` flag |
| PPTX too large (Marp) | Normal - Marp embeds resources |
| Math not rendering (reveal.js) | Add `--mathjax` flag |

## Reference Files

- Sample Markdown: `docs/sample-universal.md`
- Marp-specific sample: `docs/sample-marp-format.md`
- Research report: `docs/report-research-zh.md`
- Showcase presentation: `docs/presentation-showcase-zh.md`
