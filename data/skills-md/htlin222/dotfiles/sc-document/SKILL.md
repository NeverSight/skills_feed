---
name: sc-document
description: Create focused documentation for specific components or features. Use when user needs documentation for code, APIs, or specific features.
---

# Focused Documentation

Generate precise, focused documentation for specific components, functions, or features.

## When to use

- User needs documentation for specific code
- API documentation required
- Inline code documentation updates needed
- User guide or feature documentation requested
- Documentation for specific component needed

## Instructions

### Usage

```
/sc:document [target] [--type inline|external|api|guide] [--style brief|detailed]
```

### Arguments

- `target` - Specific file, function, or component to document
- `--type` - Documentation type (inline, external, api, guide)
- `--style` - Documentation style (brief, detailed)
- `--template` - Use specific documentation template

### Execution

1. Analyze target component and extract key information
2. Identify documentation requirements and audience
3. Generate appropriate documentation based on type and style
4. Apply consistent formatting and structure
5. Integrate with existing documentation ecosystem

### Claude Code Integration

- Uses Read for deep component analysis
- Leverages Edit for inline documentation updates
- Applies Write for external documentation creation
- Maintains documentation standards and conventions
