---
name: refactoring-code
description: Batch refactoring via MorphLLM edit_file. Use for "refactor across files", "batch rename", "update pattern everywhere", large files (500+ lines), or 5+ edits in same file.
user-invocable: false
allowed-tools:
  - mcp__morphllm__edit_file
  - mcp__morphllm__warpgrep_codebase_search
  - mcp__morphllm__codebase_search
  - Read
  - Grep
  - Glob
---

# Fast Refactoring with MorphLLM

MorphLLM edit_file provides semantic code merging at 10,500+ tokens/sec with 98% accuracy.

## When to Use edit_file

| Use edit_file                   | Use Built-in Edit/MultiEdit      |
| ------------------------------- | -------------------------------- |
| Multi-file batch refactoring    | Single file, clear edit          |
| Style/pattern update everywhere | 2-3 targeted replacements        |
| Complex prompt → many changes   | Need clear diff to review/tune   |
| Structural refactoring at scale | Simple rename (replace_all)      |
| 5+ files need same pattern      | Straightforward single-file work |

## Key Features

- **Semantic merge**: Understands code structure, not just text
- **Speed**: 10,500 tok/s vs 180 tok/s streaming
- **Accuracy**: 98% success rate on edge cases
- **dryRun**: Preview changes before applying

## Workflow

### Standard Refactoring

```
1. Use WarpGrep to find all locations needing change
2. For each file: call edit_file with changes
3. Verify with lint/test
```

### High-Stakes Changes (dryRun)

```
1. Call edit_file with dryRun: true
2. Review preview output
3. If approved, call again with dryRun: false
```

## Parameters

```
path: "/absolute/path/to/file"
code_edit: "changed lines with // ... existing code ... markers"
instruction: "brief description of changes"
dryRun: false (set true to preview)
```

## Edit Format

Use `// ... existing code ...` markers for unchanged sections:

```typescript
// ... existing code ...
function updatedFunction() {
  // new implementation
}
// ... existing code ...
```

## Common Patterns

### Batch Error Handling

```
instruction: "Add error wrapping to all repository methods"
code_edit: Shows only changed functions with context markers
```

### Import Updates

```
instruction: "Update imports from old-pkg to new-pkg"
code_edit: Shows import section with changes
```

### Multi-Location Rename

```
instruction: "Rename getUserById to findUser throughout file"
code_edit: Shows all locations with changes
```

## Tips

- Batch all edits to same file in one call
- Include enough context to locate changes precisely
- Preserve exact indentation in code_edit
- Use WarpGrep first to understand scope
- Run tests after each file to catch issues early
