---
name: quarto-book
description: Generate Quarto Book project structure with chapters, configuration, and output settings. Use when user wants to create a book, multi-chapter document, technical manual, or asks about Quarto book setup.
---

# Quarto Book Generator

Generate complete Quarto Book project structure with proper configuration.

## When to use

- User wants to create a book or multi-chapter document
- User asks to set up a Quarto book project
- User needs a technical manual or documentation structure
- User mentions "quarto book" or "book project"

## Quick generation

Run the generator script with book name:

```bash
python3 ~/.claude/skills/quarto-book/scripts/generate.py <book-name> [--chapters N] [--author "Name"]
```

Or use Quarto CLI directly:

```bash
quarto create project book <book-name>
```

## Project structure

```
mybook/
├── _quarto.yml      # Book configuration
├── index.qmd        # Preface/Introduction
├── intro.qmd        # Chapter 1
├── methods.qmd      # Chapter 2
├── results.qmd      # Chapter 3
├── summary.qmd      # Summary/Conclusion
├── references.qmd   # References
├── references.bib   # Bibliography
└── _book/           # Output directory (generated)
```

## \_quarto.yml template

```yaml
project:
  type: book
  output-dir: _book

book:
  title: "Book Title"
  author: "Author Name"
  date: today
  chapters:
    - index.qmd
    - intro.qmd
    - methods.qmd
    - results.qmd
    - summary.qmd
    - references.qmd

bibliography: references.bib
csl: apa.csl

format:
  html:
    theme: cosmo
    toc: true
  pdf:
    documentclass: scrbook
    papersize: a4
  epub:
    toc: true
```

## Chapter template

```markdown
# Chapter Title {#sec-chapter-id}

## Section 1

Content here...

## Section 2

More content...

## References

::: {#refs}
:::
```

## Commands

| Command                   | Description             |
| ------------------------- | ----------------------- |
| `quarto preview`          | Live preview in browser |
| `quarto render`           | Render all formats      |
| `quarto render --to html` | Render HTML only        |
| `quarto render --to pdf`  | Render PDF only         |

## Multi-part structure

For books with parts:

```yaml
book:
  chapters:
    - index.qmd
    - part: "Part I: Foundation"
      chapters:
        - basics.qmd
        - theory.qmd
    - part: "Part II: Application"
      chapters:
        - methods.qmd
        - results.qmd
    - references.qmd
```

## Output formats

- **HTML**: Interactive web book with search
- **PDF**: Print-ready document (requires LaTeX)
- **EPUB**: E-reader format
- **MS Word**: Editable document
