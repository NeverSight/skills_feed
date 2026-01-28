---
name: packx
description: Bundle code context for AI. ALWAYS use --limit 49k unless user explicitly requests otherwise. Use for creating shareable code bundles and preparing context for LLMs.
---

# PACKX - AI Context Bundler

Bundle and filter code files for AI context.

## CRITICAL: Always Use `--limit 49k`

**MANDATORY**: Every packx command MUST include `--limit 49k` unless the user explicitly requests a different limit. This is non-negotiable. Using 49k instead of 50k provides a safety buffer.

```bash
# CORRECT - always include --limit 49k
packx --limit 49k -c src/
packx --limit 49k -s "pattern" -i "*.ts" -c

# WRONG - never omit the limit
packx -c src/                        # NO! Missing --limit
packx -s "pattern" -i "*.ts" -c      # NO! Missing --limit
```

## Prerequisites

```bash
packx --version    # Verify installed
npm install -g packx   # If not installed
```

## Standard Command Pattern

```bash
packx --limit 49k [filters] [output] [paths]
```

**Always start with `--limit 49k`**, then add filters and output options.

## CLI Reference

### Token Budget (Required)

```bash
# Standard (default for all commands)
packx --limit 49k -c src/

# Only use different limits if user explicitly requests
packx --limit 32k -c src/            # User said "32k"
packx --limit 128k -c src/           # User said "large context"

# Split into chunks if content exceeds limit (requires -o for numbered files)
packx -M 49k -o context src/         # Creates context-1.xml, context-2.xml
```

**Limit formats:** `8k`=8,000 | `32K`=32,768 | `50000`=50,000

### Search & Filter

```bash
# Find files containing text
packx --limit 49k -s "TODO" -c
packx --limit 49k -s "useState" -i "*.tsx" -c
packx --limit 49k -s "error" -s "warning" -c

# Exclude content
packx --limit 49k -S "test" -S "mock" -c

# Filter by glob patterns
packx --limit 49k -i "*.ts" -c
packx --limit 49k -i "src/**/*.tsx" -c
packx --limit 49k -x "*.test.ts" -x "*.spec.ts" -c

# Regex patterns
packx --limit 49k -R -s "function\s+\w+" -c

# Case-sensitive
packx --limit 49k -C -s "Error" -c
```

### Git Integration

```bash
packx --limit 49k --staged -c        # Staged files
packx --limit 49k --diff -c          # Changed from main
packx --limit 49k --dirty -c         # Modified/untracked
```

### Processing Options

```bash
# Strip comments (reduces tokens)
packx --limit 49k --strip-comments -c src/

# Minify (remove empty lines)
packx --limit 49k --minify -c src/

# Both (maximum token efficiency)
packx --limit 49k --strip-comments --minify -c src/

# Context lines around matches
packx --limit 49k -s "TODO" -l 5 -c

# Follow imports
packx --limit 49k --follow-imports src/index.ts -c

# Related files (tests, stories)
packx --limit 49k -r src/utils.ts -c
```

### Output Options

```bash
# Copy to clipboard (most common)
packx --limit 49k -c src/

# Save to file (use --stdout > to avoid WriteFile hook limits)
packx --limit 49k --stdout src/ > context.md

# Output formats
packx --limit 49k -f xml -c src/         # XML (default)
packx --limit 49k -f markdown -c src/    # Markdown
packx --limit 49k -f plain -c src/       # Plain text
packx --limit 49k -f jsonl -c src/       # JSONL
```

**IMPORTANT:** Always use `--stdout > <file>` instead of `--output <file>` to avoid triggering WriteFile hook size limits on large bundles.

### Preview (Check Before Packing)

```bash
# Preview matching files without packing
packx --limit 49k --preview src/
packx --limit 49k -s "pattern" --preview
```

### Interactive Mode

```bash
packx --limit 49k -I src/            # Interactive selection
packx --limit 49k --no-interactive src/  # Scripting mode
```

**Controls:** Tab=preview focus | PgUp/PgDn=scroll | Enter=confirm

### Bundles (Saved Configs)

```bash
packx -b api                         # Load .pack/bundles/api
```

## Common Workflows

### Default: Feature Context

```bash
# Most common - search for feature, copy to clipboard
packx --limit 49k -s "auth" -i "*.ts" -c
```

### PR Review Context

```bash
packx --limit 49k --diff -c
packx --limit 49k --staged -f markdown --stdout > pr.md
```

### Debug Context

```bash
packx --limit 49k --follow-imports src/problem.ts -c
packx --limit 49k -r src/problem.ts -c    # Include tests
```

### Minimal Context (Max Efficiency)

```bash
packx --limit 49k --strip-comments --minify -i "*.ts" -c src/
```

### Specific Files

```bash
# List specific files directly
packx --limit 49k src/auth.ts src/user.ts src/api.ts -c
```

## Best Practices

1. **ALWAYS use `--limit 49k`** - No exceptions unless user specifies
2. **Use `-c` for clipboard** - Most common output method
3. **Preview first** - `--preview` to check file selection
4. **Strip noise** - `--strip-comments --minify` when token-tight
5. **Be specific** - Use `-s` search and `-i` globs to narrow scope
6. **Check git state** - `--diff` and `--staged` for PR context

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Too many tokens | Add `-i "*.ts"`, `-x "test"`, or `--strip-comments` |
| Missing files | Check globs, use `--preview` |
| Over 49k needed | Split with `-M 49k -o output` (creates numbered files) |
| WriteFile hook error | Use `--stdout > file.md` instead of `--output file.md` |
