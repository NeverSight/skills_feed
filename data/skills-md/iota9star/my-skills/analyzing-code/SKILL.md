---
name: analyzing-code
description: Analyzes code statistics by language for project insight, CI/CD metrics, or before refactoring. Use this skill when understanding project composition, measuring change impact, or generating CI/CD metrics
---

# tokei: Code Statistics Analysis

**Always invoke tokei skill for code statistics - do not execute bash commands directly.**

Use tokei for fast, accurate code statistics across multiple languages and projects.

## Default Strategy

**Invoke tokei skill** for analyzing code statistics by language. Use when understanding project composition, measuring change impact before refactoring, or generating CI/CD metrics.

Common workflow: tokei skill → other skills (fd, jq, yq) for filtering or tokei skill after refactoring to measure impact.

## Key Options

### Basic Output Control
- `-f/--files` show individual file statistics
- `-l/--languages` list supported languages and extensions
- `-v/--verbose` show unknown file extensions (1-3)
- `-V/--version` show version information
- `--hidden` include hidden files
- `-c/--columns N` set strict column width

### Filtering & Exclusion
- `-t/--type TYPES` filter by language types (comma-separated)
- `-e/--exclude PATTERNS` exclude files/dirs (gitignore syntax)
- `--no-ignore` don't respect ignore files
  - `--no-ignore-dot` don't respect .ignore/.tokeignore
  - `--no-ignore-vcs` don't respect VCS ignore files
  - `--no-ignore-parent` don't respect parent ignore files

### Output Formats
- `-o/--output FORMAT` output format (json|yaml|cbor)
  - Requires compilation with features: `cargo install tokei --features all`
- `-i/--input FILE` read from previous tokei run or stdin

### Sorting Options
- `-s/--sort COLUMN` sort by column
  - Possible values: `files|lines|blanks|code|comments`

## When to Use

- **Project Analysis**: Get comprehensive code statistics for entire codebase
- **Language Breakdown**: Understand project composition by language
- **CI/CD Integration**: Export metrics for build processes
- **Code Auditing**: Identify file types and their distributions
- **Performance Monitoring**: Track code growth over time

## Core Principles

1. **Speed**: Optimized to count millions of lines in seconds
2. **Accuracy**: Correctly handles nested comments, multi-line strings
3. **Language Coverage**: Supports 150+ programming languages
4. **Flexibility**: Multiple output formats for integration

## Detailed Reference

For comprehensive usage patterns, output formats, language filtering, and integration examples, load [tokei guide](./reference/tokei-guide.md) when needing:
- Advanced language filtering and exclusion
- JSON/YAML output processing
- CI/CD integration patterns
- Docker usage examples
- Performance tuning for large codebases

The guide includes:
- Basic usage and output control options
- Language filtering and exclusion patterns
- Output format configuration (JSON, YAML, CBOR)
- Performance tips for large codebases
- Docker usage and CI/CD integration
- Configuration files and environment variables

## Skill Combinations

### For Discovery Phase
- **fd → tokei**: Analyze specific file types or directories
- **extracting-code-structure → tokei**: Get statistics for specific code components
- **git diff → tokei**: Analyze changed files statistics

### For Analysis Phase
- **tokei → jq/yq**: Parse statistics output for reports
- **tokei → fzf**: Interactive selection from language breakdown
- **tokei → bat**: View statistics with formatted output

### For Refactoring Phase
- **tokei → replacing-text**: Update configuration based on code statistics
- **analyzing-code-structure → tokei**: Measure impact of structural changes
- **tokei → searching-text**: Find files contributing to specific language statistics

### Multi-Skill Workflows
- **tokei → fd → searching-text → analyzing-code-structure**: Statistics-driven refactoring pipeline
- **tokei → jq → fzf**: Interactive language-based file selection
- **git workflow**: git diff → tokei → fd → bat (analyze changes, select files, preview)

### Integration Examples
```bash
# Get language breakdown and filter for top languages
tokei -o json | jq '.data | to_entries | sort_by(.value.stats.code) | reverse | .[0:5] | .[].key'

# Analyze changes after refactoring
git diff --name-only | xargs tokei --files

# Find and analyze specific components
fd -e py src/components | xargs tokei -t Python
```
