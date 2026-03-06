---
name: map
description: Generate semantic codebase symbol map for precise code navigation. Use when starting work on unfamiliar codebase, before refactoring, or when you need to understand where classes/functions/interfaces are defined instead of using rg text-matching.
---

# Codebase Symbol Map Generator

Generate a semantic symbol map showing where all exports, classes, functions, and interfaces are defined. This eliminates guessing with `rg` by providing precise `file:line` locations.

## When to Use

- Starting work on an unfamiliar codebase
- Before large-scale refactoring
- When needing to understand code structure
- To avoid `rg` text-matching confusion (same name in comments/strings)

## Execution

Run the generator script:

```bash
python3 ~/.claude/skills/map/scripts/symbol_map.py
```

The script will:

1. Detect project language (TypeScript/JavaScript/Python/Rust/Go)
2. Extract all exported symbols with their locations
3. Generate a markdown map at `~/.claude/codebase-maps/{project}_symbols.md`

## Output Format

```markdown
## Symbol Index by Type

### Classes

| Symbol         | Location                  |
| -------------- | ------------------------- |
| `AuthProvider` | `src/auth/provider.ts:15` |

### Functions

| Symbol       | Location               |
| ------------ | ---------------------- |
| `formatDate` | `src/utils/date.ts:42` |
```

## Usage After Generation

After running `/map`, use the symbol locations directly:

- "Read `src/auth/provider.ts:15` to check AuthProvider"
- "The `formatDate` function at `src/utils/date.ts:42` needs modification"

No more grepping and guessing.
