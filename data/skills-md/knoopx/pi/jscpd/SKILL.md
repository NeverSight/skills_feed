---
name: jscpd
description: Finds duplicate code blocks and analyzes duplication metrics across files. Use when identifying copy-pasted code, measuring technical debt, or preparing for refactoring.
---

# jscpd

Copy-paste detector for JavaScript, TypeScript, and many other languages.

## Quick Start

```bash
# With ignore patterns
bunx jscpd --ignore "**/node_modules/**,**/dist/**" <path>

```

## Common Options

| Option             | Description                              |
| ------------------ | ---------------------------------------- |
| `--min-tokens N`   | Minimum tokens for duplicate detection   |
| `--min-lines N`    | Minimum lines for duplicate detection    |
| `--threshold N`    | Fail if duplication % exceeds threshold  |
| `--ignore "glob"`  | Ignore patterns (comma-separated)        |
| `--reporters type` | Output format: `console`, `json`, `html` |
| `--output path`    | Output directory for reports             |
| `--silent`         | Suppress console output                  |

## Workflow

1. Run jscpd to find duplicates
2. Review the reported duplicates
3. Refactor to eliminate duplication
4. Re-run to verify cleanup

## Related Skills

- **maintenance**: Refactoring and technical debt management
- **design**: DRY principle violations
- **ast-grep**: Structural refactoring of duplicated patterns
