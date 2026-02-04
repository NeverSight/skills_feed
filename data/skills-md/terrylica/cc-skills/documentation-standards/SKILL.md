---
name: documentation-standards
description: Markdown documentation standards for LLM and Pandoc PDF. TRIGGERS - markdown standards, section numbering, documentation style.
---

# Documentation Standards

## Overview

Standards for writing markdown documentation optimized for both LLM consumption and conversion to professional PDFs using Pandoc. Ensures consistency across all documentation.

## When to Use This Skill

Use when:

- Writing markdown documentation (README, skills, guides, specifications)
- Creating new skills that include markdown content
- Authoring content that may be converted to PDF
- Reviewing documentation for standards compliance

## Core Principles

### 1. LLM-Optimized Documentation Architecture

**Machine-Readable Priority**: OpenAPI 3.1.0 specs, JSON Schema, YAML specifications take precedence over human documentation.

**Why**: Structured formats provide unambiguous contracts that both humans and LLMs can consume reliably. Human docs supplement, don't replace, machine-readable specs.

**Application**:

- Workflow specifications → OpenAPI 3.1.1 YAML in specifications/
- Data schemas → JSON Schema with examples
- Configuration → YAML with validation schemas
- Human docs → Markdown referencing canonical machine-readable specs

### 2. Hub-and-Spoke Progressive Disclosure

**Pattern**: Central hubs (like CLAUDE.md, INDEX.md) link to detailed spokes (skills, docs directories).

**Structure**:

```
CLAUDE.md (Hub - Essentials Only)
    ↓ links to
Skills (Spokes - Progressive Disclosure)
    ├── SKILL.md (Overview + Quick Start)
    └── references/ (Detailed Documentation)
```

**Rules**:

- Hubs contain essentials only (what + where to find more)
- Spokes contain progressive detail (load as needed)
- Single source of truth per topic (no duplication)

### 3. Markdown Section Numbering

**Critical Rule**: Never manually number markdown headings.

❌ **Wrong**:

```markdown
## 1. Introduction

### 1.1 Background

### 1.2 Objectives

## 2. Implementation
```

✅ **Correct**:

```markdown
## Introduction

### Background

### Objectives

## Implementation
```

**Rationale**:

- Pandoc's `--number-sections` flag auto-numbers all sections when generating PDFs
- Manual numbering creates duplication: "1. 1. Introduction" in rendered output
- Auto-numbering is consistent, updates automatically when sections reorganize
- Applies to ALL markdown: documentation, skills, project files, README files

**Rule**: If markdown might ever convert to PDF, never manually number headings. Use semantic heading levels (##, ###) and let tools handle numbering.

## Standards Checklist

Use this checklist when creating or reviewing documentation:

### Structure

- [ ] Follows hub-and-spoke pattern (essentials in main doc, details in references)
- [ ] Links to deeper documentation for progressive disclosure
- [ ] Single source of truth (no duplicate content across docs)

### Markdown Formatting

- [ ] No manual section numbering in headings
- [ ] Semantic heading levels (##, ###, ####) used correctly
- [ ] Code blocks have language identifiers for syntax highlighting
- [ ] Links use markdown format `[text](url)`, not bare URLs

### Machine-Readable Content

- [ ] Workflows documented as OpenAPI 3.1.1 specs (when applicable)
- [ ] Data structures use JSON Schema (when applicable)
- [ ] Configuration uses YAML with validation (when applicable)
- [ ] Human docs reference canonical machine-readable specs

### File Organization

- [ ] Documentation lives in appropriate location:
  - Global standards → docs/standards/
  - Skill documentation → skills/{skill-name}/references/
  - Project documentation → {project}/.claude/ or {project}/docs/
- [ ] Index files provide navigation (INDEX.md, README.md)

## Related Resources

- **ASCII Diagram Validation**: [ascii-diagram-validator](../ascii-diagram-validator/SKILL.md) - Validate ASCII diagrams in markdown
- **Skill Architecture**: See skill-architecture plugin for creating effective skills

## Examples

### Good Hub-and-Spoke Structure

**Hub (CLAUDE.md)**:

```markdown
## PDF Generation from Markdown

**Quick Start**: Use pandoc-pdf-generation skill

**Critical Rules**:

1. Never write ad-hoc pandoc commands
2. Always verify PDFs before presenting
3. See skill for detailed principles
```

**Spoke (skill/SKILL.md)**:

- Quick start with examples
- Link to references/ for detailed documentation
- Progressive disclosure as needed

### Good Machine-Readable Documentation

**Workflow Specification** (specifications/hook-prompt-capture.yaml):

```yaml
openapi: 3.1.1
info:
  title: Hook Prompt Capture Workflow
  version: 1.0.0
paths:
  /capture-prompt:
    post:
      summary: Capture user prompt from hook
      # ... detailed spec
```

**Human Documentation** (README.md):

```markdown
## Workflow

See [hook-prompt-capture.yaml](./specifications/hook-prompt-capture.yaml)
for complete workflow specification.

Quick overview: ...
```

## Summary

Documentation standards ensure:

- **Consistency** across all workspace documentation
- **LLM optimization** through machine-readable formats
- **Maintainability** via hub-and-spoke + single source of truth
- **PDF compatibility** through proper markdown formatting

Follow these standards for all documentation.

---

## Troubleshooting

| Issue                         | Cause                        | Solution                                          |
| ----------------------------- | ---------------------------- | ------------------------------------------------- |
| Double section numbers in PDF | Manual numbering in markdown | Remove manual numbers, use --number-sections only |
| Broken links in PDF           | Relative paths incorrect     | Use repo-root paths for cross-document links      |
| Code block no syntax color    | Missing language identifier  | Add language after opening triple backticks       |
| Tables render poorly          | Column widths too wide       | Use shorter headers or pipe-table format          |
| Hub doc too long              | Too much detail in hub       | Move details to spoke documents, link from hub    |
| Duplicate content             | Same info in multiple docs   | Identify SSoT, remove duplicates, add links       |
| YAML spec not rendering       | Wrong file extension         | Use .yaml extension for OpenAPI specs             |
| Index navigation missing      | No INDEX.md or README.md     | Create navigation index in each directory         |
