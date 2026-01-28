---
name: typst-creator
description: Generate Typst documents with proper syntax for markup, math, scripting, and styling. Based on Typst v0.14.2 documentation.
---

# Typst Document Creation Capability

This skill enables the agent to create Typst documents with correct syntax, styling, and mathematical formulas.

> **Version**: Based on Typst v0.14.2

## Core Capability

- **Function**: Generate Typst source code for documents, reports, papers, and presentations
- **Output Format**: `.typ` files with proper Typst syntax
- **Modes**: Markup, Math, and Code modes

## Typst Syntax Overview

| Mode | Entry Syntax | Purpose |
|------|--------------|---------|
| Markup | Default | Text, headings, lists, emphasis |
| Math | `$...$` | Mathematical formulas |
| Code | `#` prefix | Variables, functions, logic |

## Domain Knowledge

| Topic | Reference |
|-------|-----------|
| **Syntax** | Markup, math, and code mode syntax. See [./references/syntax.md](./references/syntax.md) |
| **Styling** | Set rules and show rules for styling. See [./references/styling.md](./references/styling.md) |
| **Scripting** | Variables, functions, control flow. See [./references/scripting.md](./references/scripting.md) |
| **Math** | Mathematical notation and symbols. See [./references/math.md](./references/math.md) |
| **Layout** | Page setup, grids, alignment. See [./references/layout.md](./references/layout.md) |

## Key Differences from LaTeX

| Feature | LaTeX | Typst |
|---------|-------|-------|
| Bold | `\textbf{text}` | `*text*` |
| Italic | `\textit{text}` | `_text_` |
| Heading | `\section{Title}` | `= Title` |
| Fraction | `\frac{a}{b}` | `a/b` or `frac(a, b)` |
| Function call | `\func{arg}` | `#func(arg)` |
| Set property | preamble commands | `#set func(prop: value)` |

## Constraints

- **File Extension**: Output files use `.typ` extension
- **Unicode Support**: Typst natively supports Unicode symbols
- **No Packages Required**: Most features are built-in (unlike LaTeX)
