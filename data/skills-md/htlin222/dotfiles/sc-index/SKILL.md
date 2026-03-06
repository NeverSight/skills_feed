---
name: sc-index
description: Generate comprehensive project documentation and knowledge base. Use when creating docs, API documentation, project structure maps, or README files.
---

# Project Documentation

Create and maintain comprehensive project documentation, indexes, and knowledge bases.

## When to use

- Creating project documentation
- Generating API documentation
- Mapping project structure
- Creating or updating README files
- Building knowledge bases for codebases

## Instructions

### Usage

```
/sc:index [target] [--type docs|api|structure|readme] [--format md|json|yaml]
```

### Arguments

- `target` - Project directory or specific component to document
- `--type` - Documentation type (docs, api, structure, readme)
- `--format` - Output format (md, json, yaml)
- `--update` - Update existing documentation

### Execution

1. Analyze project structure and identify key components
2. Extract documentation from code comments and README files
3. Generate comprehensive documentation based on type
4. Create navigation structure and cross-references
5. Output formatted documentation with proper organization

### Claude Code Integration

- Uses Glob for systematic file discovery
- Leverages Grep for extracting documentation patterns
- Applies Write for creating structured documentation
- Maintains consistency with project conventions
