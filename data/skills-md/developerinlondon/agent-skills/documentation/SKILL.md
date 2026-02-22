---
name: documentation
description: >-
  Documentation standards: ASCII box-drawing diagrams (not Mermaid), structured plan format,
  compact tables for comparisons. Use when writing docs, plans, READMEs, or architecture
  documents in any project.
---

# Documentation Standards

## Diagrams

- Use ASCII box-drawing diagrams (NOT Mermaid) -- they render everywhere: terminals, git diffs, code
  review, plain text, any monospace font
- Use box-drawing characters: + - | / \ > < = and standard ASCII art
- Wrap diagrams in triple-backtick code blocks (no language tag)
- Keep diagrams compact -- max ~40 lines, ~80 chars wide
- For data flow: use arrows ---> and ---- with labels
- For hierarchy: use tree notation +-- |

## Plan Files

- Plans should include: Status, Created date, Dependencies, Architecture diagram, Task list
- Task items use checkbox format: `- [ ] description`

## Format

- Always run the project's formatter on markdown files after editing
- Use tables for structured comparisons
- Use code blocks with language tags for all code/config snippets
- Keep lines under 100 characters where possible
