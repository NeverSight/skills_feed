---
name: platonic-specs
description: Manage RFC-style specifications with validation, and dynamic generation of history, index, and namings files. Use when validating RFC documents, checking taxonomy compliance, or generating specification indices and terminology references.
license: MIT
metadata:
  version: "1.0.2"
  author: "Xiaming Chen"
  category: "documentation"
---

# Platonic Coding Specs

Manage RFC-style specifications in development projects with AI-driven operations.

## When to Use This Skill

Use this skill when you need to:

- **Validate** existing specifications for consistency and standard compliance
- **Generate** or update history, index, and terminology files
- **Check** taxonomy and cross-reference consistency
- **Refine** specifications following best practices

> **Note**: For project initialization (creating specs directories and templates), use **platonic-init**.

Keywords: RFC, specifications, documentation, validation, taxonomy, terminology

## Quick Start

### Refine Existing Specifications

Read `references/refine-specs.md` to run a comprehensive refinement that:
- Validates cross-references and dependencies
- Checks taxonomy compliance
- Updates history, index, and terminology files
- Reports errors and warnings

## Available Operations

This skill provides 7 distinct operations, each defined in `references/`:

| Operation | Reference File | Purpose |
|-----------|----------------|---------|
| **Refine** | `refine-specs.md` | Comprehensive validation and update |
| **Generate History** | `generate-history.md` | Update RFC change history |
| **Generate Index** | `generate-index.md` | Update RFC index with quick links |
| **Generate Namings** | `generate-namings.md` | Extract and organize terminology |
| **Validate Consistency** | `validate-consistency.md` | Check cross-references and metadata |
| **Check Taxonomy** | `check-taxonomy.md` | Verify terminology consistency |
| **Check Compliance** | `check-standard-compliance.md` | Validate against RFC standard |

See [references/REFERENCE.md](references/REFERENCE.md) for detailed operation guides and examples.

## Templates

Templates are provided in `assets/` as references:

- `rfc-standard.md.template` - RFC format and guidelines
- `rfc-history.md.template` - Change history structure
- `rfc-index.md.template` - RFC index format
- `rfc-namings.md.template` - Terminology reference format
- `rfc-template.md` - Individual RFC template

Templates use `{{PROJECT_NAME}}` placeholders.

## Best Practices

1. Always read the reference file before executing an operation
2. Check `rfc-standard.md` in your specs directory for project conventions
3. Update history when making changes to RFCs
4. Run validation operations regularly to maintain consistency
5. Keep terminology current - deprecated terms belong in history, not namings

## Dependencies

- Read/write access to specifications directory
- Markdown file support
- Date manipulation for history tracking
