---
name: platonic-code-specs
description: Manage RFC-style specifications with templates, validation, and dynamic generation of history, index, and namings files. Use when initializing specification systems, validating RFC documents, checking taxonomy compliance, or generating specification indices and terminology references.
license: MIT
metadata:
  version: "1.0.0"
  author: "caesar0301"
  category: "documentation"
---

# Platonic Coding Specs

Manage RFC-style specifications in development projects with AI-driven operations.

## When to Use This Skill

Use this skill when you need to:

- **Initialize** a new project's RFC specification system
- **Validate** existing specifications for consistency and standard compliance
- **Generate** or update history, index, and terminology files
- **Check** taxonomy and cross-reference consistency
- **Refine** specifications following best practices

Keywords: RFC, specifications, documentation, validation, taxonomy, terminology

## Quick Start

### Initialize a New Specification System

Read `references/init-specs.md` and provide:
- Project name (e.g., "MyProject")
- Target specs directory path (e.g., "./specs")

This creates the foundation files: `rfc-standard.md`, `rfc-history.md`, `rfc-index.md`, `rfc-namings.md`

### Refine Existing Specifications

Read `references/refine-specs.md` to run a comprehensive refinement that:
- Validates cross-references and dependencies
- Checks taxonomy compliance
- Updates history, index, and terminology files
- Reports errors and warnings

## Available Operations

This skill provides 8 distinct operations, each defined in `references/`:

| Operation | Reference File | Purpose |
|-----------|----------------|---------|
| **Initialize** | `init-specs.md` | Create new specs folder from templates |
| **Refine** | `refine-specs.md` | Comprehensive validation and update |
| **Generate History** | `generate-history.md` | Update RFC change history |
| **Generate Index** | `generate-index.md` | Update RFC index with quick links |
| **Generate Namings** | `generate-namings.md` | Extract and organize terminology |
| **Validate Consistency** | `validate-consistency.md` | Check cross-references and metadata |
| **Check Taxonomy** | `check-taxonomy.md` | Verify terminology consistency |
| **Check Compliance** | `check-standard-compliance.md` | Validate against RFC standard |

See [references/REFERENCE.md](references/REFERENCE.md) for detailed operation guides and examples.

## Templates

Templates are provided in `assets/` for initializing new specification systems:

- `rfc-standard.md.template` - RFC format and guidelines
- `rfc-history.md.template` - Change history structure
- `rfc-index.md.template` - RFC index format
- `rfc-namings.md.template` - Terminology reference format
- `rfc-template.md` - Individual RFC template

Templates use `{{PROJECT_NAME}}` placeholders replaced during initialization.

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
