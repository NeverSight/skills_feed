---
name: dev.mermaid
description: Generate Mermaid diagrams with proper syntax. Use when creating flowcharts, sequence diagrams, class diagrams, or any other Mermaid visualizations. Ensures correct label quoting to prevent parsing errors.
---

# Dev Mermaid

## Overview

This skill provides syntax guidelines for generating valid Mermaid diagrams. Mermaid is a diagramming language that renders text into diagrams, but it's strict about parsing—improper syntax causes rendering failures.

## Syntax Rules

When generating Mermaid:

1. **Always wrap node labels in double quotes** if they contain any of the following:

   * Parentheses `(` `)`
   * Commas `,`
   * Arrows like `->`, `=>`, `→`
   * Function-like text (e.g. `foo(a, b)`)
   * Operators or symbols (`+`, `-`, `_` in method names combined with punctuation)

2. Use this pattern:

   ```
   A["label text here"]
   ```

   not:

   ```
   A[label text here]
   ```

3. `<br/>` is allowed inside quoted labels.

4. Decision nodes `{}` may remain unquoted **only** if they contain simple words (e.g. `{dryRun?}`).

5. If unsure whether a label is safe, **quote it anyway** — quoted labels always parse correctly.

6. Never rely on Mermaid to "guess" intent; Mermaid is a grammar parser, not markdown.

## Mental Model (Important)

> **Mermaid is not Markdown.**
> It is closer to a programming language.
> If something *looks like code*, Mermaid will try to parse it as code.

Quoting labels opts out of that behavior.
