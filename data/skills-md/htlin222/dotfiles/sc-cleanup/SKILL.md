---
name: sc-cleanup
description: Clean up code, remove dead code, and optimize project structure. Use when user wants to clean codebase, remove unused code, or optimize imports.
---

# Code and Project Cleanup

Systematically clean up code, remove dead code, optimize imports, and improve project structure.

## When to use

- User asks to clean up code or project
- Dead code or unused imports need removal
- Project structure needs optimization
- Technical debt cleanup requested
- File organization improvements needed

## Instructions

### Usage

```
/sc:cleanup [target] [--type code|imports|files|all] [--safe|--aggressive]
```

### Arguments

- `target` - Files, directories, or entire project to clean
- `--type` - Cleanup type (code, imports, files, all)
- `--safe` - Conservative cleanup (default)
- `--aggressive` - More thorough cleanup with higher risk
- `--dry-run` - Preview changes without applying them

### Execution

1. Analyze target for cleanup opportunities
2. Identify dead code, unused imports, and redundant files
3. Create cleanup plan with risk assessment
4. Execute cleanup operations with appropriate safety measures
5. Validate changes and report cleanup results

### Claude Code Integration

- Uses Glob for systematic file discovery
- Leverages Grep for dead code detection
- Applies MultiEdit for batch cleanup operations
- Maintains backup and rollback capabilities
