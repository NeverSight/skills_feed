---
name: typst
description: "Typst document creation and package development. Use when: (1) Working with .typ files, (2) User mentions typst, typst.toml, or typst-cli, (3) Creating or using Typst packages, (4) Developing document templates, (5) Converting Markdown/LaTeX to Typst"
---

# Typst

Typst is a modern typesetting system designed as an alternative to LaTeX. It offers a simpler syntax, faster compilation, and programmatic document creation.

## Agent Patterns

### Detection

```bash
typst --version  # Check if installed
```

### Verify Compilation

Agents cannot preview PDFs. Verify success via exit code:

```bash
typst compile document.typ && echo "Success" || echo "Failed"
```

For text-level verification, see [debug.md](debug.md) (`pdftotext` workflow).

### Common Errors

| Error                                  | Cause                | Fix                                        |
| -------------------------------------- | -------------------- | ------------------------------------------ |
| "unknown variable"                     | Undefined identifier | Check spelling, ensure `#let` before use   |
| "expected X, found Y"                  | Type mismatch        | Check function signature in docs           |
| "file not found"                       | Bad import path      | Paths resolve relative to the current file |
| "unknown font"                         | Font not installed   | Use system fonts or web-safe alternatives  |
| "maximum function call depth exceeded" | Deep recursion       | Limit recursion, use iteration instead     |

### Minimal Document

```typst
#set page(paper: "a4", margin: 2cm)
#set text(size: 11pt)

= Title

Content goes here.
```

## Quick Reference

| Task                                            | Reference                      |
| ----------------------------------------------- | ------------------------------ |
| Language basics (types, functions, operators)   | [basics.md](basics.md)         |
| State, context, query, XML parsing              | [advanced.md](advanced.md)     |
| Templates, styling, set/show rules              | [template.md](template.md)     |
| Package development, publishing                 | [package.md](package.md)       |
| Converting from Markdown/LaTeX                  | [conversion.md](conversion.md) |
| Debugging techniques (pdftotext, repr, measure) | [debug.md](debug.md)           |
| Performance profiling (timings, hotspots)       | [perf.md](perf.md)             |

## When to Use Each Reference

### basics.md

**Read first** for any Typst work. Complete language reference:

- Markup vs code mode switching
- **Imports and path resolution** (relative, root-relative, `--root`)
- All data types and their operations (string, array, dict)
- Regex pattern matching
- Functions, control flow, operators
- Common pitfalls (closure mutability, none returns)

### advanced.md

For cross-document features and complex patterns:

- State management (`state()`, `context`)
- Query system (`query()`, metadata, labels)
- XML parsing
- Working around closure limitations
- Performance optimization

### template.md

For document templates and styling:

- Set rules (defaults) and show rules (transformations)
- Page layout, headers, footers
- Counters and numbering
- Heading and figure customization

### package.md

For creating reusable Typst packages:

- `typst.toml` manifest format
- Module organization and imports
- API design patterns
- Publishing to Typst Universe

### conversion.md

For converting existing documents to Typst:

- Syntax mapping tables (Markdown/LaTeX → Typst)
- Math formula conversion
- Escaping rules
- Pandoc integration

### debug.md

For debugging Typst documents (especially for agents):

- `pdftotext` for text content verification
- `repr()` for inspecting complex objects
- `measure()` + `place()` for layout debugging
- State and query debugging patterns

### perf.md

For performance profiling and timing analysis:

- `--timings` JSON trace output
- Aggregating hotspots from trace events
- Viewing traces in Chrome/Perfetto

## Compilation

```bash
# Compile once
typst compile document.typ

# Watch mode (recompile on changes)
typst watch document.typ

# Specify output file
typst compile document.typ output.pdf

# Set project root (for multi-file projects)
# Root controls where "/path" resolves and security boundary
typst compile src/main.typ --root .
```

**When to use `--root`**: If your document imports files using `/`-prefixed paths (e.g., `#import "/lib/utils.typ"`), set `--root` to the directory those paths should resolve from. See [basics.md](basics.md) for path resolution rules.

## Common Packages

| Package              | Purpose                                        |
| -------------------- | ---------------------------------------------- |
| `@preview/codly`     | Code block formatting with syntax highlighting |
| `@preview/ctheorems` | Theorem environments                           |
| `@preview/mitex`     | LaTeX math rendering                           |
| `@preview/cuti`      | CJK typography utilities                       |
| `@preview/citegeist` | BibTeX parsing                                 |

Import packages (check https://typst.app/universe for latest versions):

```typst
#import "@preview/codly:1.3.0": *
```

## Examples

The `examples/` directory contains runnable examples:

| Example                                             | Description                                          |
| --------------------------------------------------- | ---------------------------------------------------- |
| [basic-document.typ](examples/basic-document.typ)   | Complete beginner document with all common elements  |
| [template-report.typ](examples/template-report.typ) | Reusable template with headers, counters, note boxes |
| [package-example/](examples/package-example/)       | Minimal publishable package with submodules          |

## Dependencies

- **typst CLI**: Install from https://typst.app or via package manager
  - macOS: `brew install typst`
  - Linux: `cargo install typst-cli`
  - Windows: `winget install typst`
