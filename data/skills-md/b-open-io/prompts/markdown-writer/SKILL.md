---
name: markdown-writer
version: 1.0.0
description: This skill should be used when the user asks to write, edit, review, or improve Markdown content (README, docs, changelog, guides), or needs Markdown formatting, syntax help, or advanced patterns (tables, callouts, task lists, mermaid, details/summary, footnotes).
---

# Markdown Writer

Write clean, portable Markdown and apply advanced Markdown patterns when appropriate.

## Workflow
1. Identify the target renderer (GitHub/GitLab/MDX/etc.). If unknown, assume GitHub Flavored Markdown and note compatibility when using advanced features.
2. Keep structure scannable with headings, short paragraphs, and lists.
3. Prefer native Markdown; use HTML only when required and supported by the target renderer.
4. Load [references/REFERENCE.md](references/REFERENCE.md) for advanced patterns and snippets.
5. Validate that syntax is consistent and examples are copy-pasteable.
