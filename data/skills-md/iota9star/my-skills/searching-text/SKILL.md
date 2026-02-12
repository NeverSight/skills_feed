---
name: searching-text
description: Performs fast text search with one-shot patterns that minimize iterations by getting files, lines, and context in a single call. Use this skill when searching for text patterns, finding specific code locations, or getting context around matches
---

# ripgrep: Powerful, one-shot text search

**Always invoke ripgrep skill for text search - do not execute bash commands directly.**

## Default Strategy

**Invoke ripgrep skill** for fast text search with one-shot patterns. Use `-e 'pattern' -n -C 2` to get files, line numbers, and context in a single call.

This minimizes iterations and context usage. Always prefer getting line numbers and surrounding context over multiple search attempts.

Common workflow: ripgrep skill → other skills (fzf, bat, sd, analyzing-code-structure) for interactive selection, preview, or modification.

## Tool Selection

**Grep tool** (built on ripgrep) - Use for structured searches:
- Basic pattern matching with structured output
- File type filtering with `type` parameter
- When special flags like `-F`, `-v`, `-w`, or pipe composition are not needed
- Handles 95% of search needs

**Bash(rg)** - Use for one-shot searches needing special flags or composition:
- Fixed string search (`-F`)
- Invert match (`-v`)
- Word boundaries (`-w`)
- Context lines with patterns (`-n -C 2`)
- Pipe composition (`| head`, `| wc -l`, `| sort`)
- Default choice for efficient one-shot results

**Glob tool** - Use for file name/path matching only (not content search)

## When to Load Detailed Reference

Load [ripgrep guide](./reference/ripgrep-guide.md) when needing:
- One-shot search pattern templates
- Effective flag combinations for complex searches
- Pipe composition patterns
- File type filters reference (`-t` flags)
- Performance optimization for large result sets
- Pattern syntax examples
- Translation between Grep tool and rg commands

The guide focuses on practical patterns for getting targeted results in minimal calls.

### Pipeline Combinations
- **rg | fzf**: Interactive selection from search results
- **rg | sd**: Batch replacements on search results  
- **rg | xargs**: Execute commands on matched files

## Skill Combinations

### For Discovery Phase
- **fd → ripgrep**: Find files of specific type, then search within them
- **extracting-code-structure → ripgrep**: Understand structure, then search for specific patterns
- **jq/yq → ripgrep**: Extract field values, then search for their usage

### For Analysis Phase
- **ripgrep → fzf**: Interactive selection from search matches
- **ripgrep → bat**: View matched files with syntax highlighting
- **ripgrep → ast-grep**: After finding text patterns, apply structural changes

### For Refactoring Phase
- **ripgrep → sd**: Replace found patterns with new content
- **ripgrep → xargs**: Execute commands on all matching files
- **ripgrep → tokei**: Get statistics for files containing specific patterns
- **ripgrep → analyzing-code-structure**: After finding text patterns, apply structural changes

### Integration Examples
```bash
# Find and edit all references to a function
rg "functionName" -l | fzf --multi --preview="bat --color=always --highlight-line $(rg -n "functionName" {} | head -1 | cut -d: -f2) {}" | xargs vim

# Find TODOs and create summary
rg "TODO|FIXME" -n | fzf --multi --preview="bat --color=always --highlight-line {2} {1}"
