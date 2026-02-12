---
name: replacing-text
description: Provides intuitive find & replace CLI with JavaScript regex and string-literal mode. Use this skill when performing text replacements, batch transformations, or need JavaScript-style regex syntax
---

# sd: Fast Find & Replace

**Always invoke sd skill for find & replace operations - do not execute bash commands directly.**

Use sd for intuitive text replacement that's 2-12x faster than sed.

## When to Use sd vs ripgrep

**Use sd when:**
- Performing replacements on known patterns
- Batch text transformations across files
- Need JavaScript-style regex syntax
- Direct file modifications without search first

**Use ripgrep when:**
- Finding unknown patterns or locations
- Need search results without immediate changes
- Complex file filtering and type matching
- Want to preview before modifying

**Common workflow**: ripgrep skill → sd skill (search first, then replace)

## Default Strategy

**Invoke sd skill** for fast find & replace operations. Use when performing replacements on known patterns, batch text transformations across files, or need JavaScript-style regex syntax.

Common workflow: ripgrep skill → sd skill (search first, then replace) or fd skill → sd skill for batch operations.

## Key Options

- `-F` for string-literal mode (no regex)
- `$1, $2` or `${var}` for capture groups
- `--preview` to preview changes
- `--` before patterns starting with `-`
- `$$` for literal `$` in replacement

## When to Use

- Quick file edits
- Pipeline replacements: `cat file | sd "old" "new"`
- Batch operations across multiple files
- Complex regex with capture groups

### Common Workflows
- `fd → sd`: Find files and perform batch replacements
- `ripgrep | sd`: Search patterns and replace across matches
- `jq | sd`: Extract JSON data and transform to other formats
- `cat file | sd | bat`: Transform content and preview with highlighting

## Core Principle

Replace text with familiar JavaScript/Python regex syntax - no sed escape hell.

## Detailed Reference

For comprehensive find & replace patterns, regex syntax examples, and workflow tips, load [sd guide](./reference/sd-guide.md) when needing:
- Advanced regex patterns with capture groups
- Pipeline operations and batch processing
- Escape sequence handling
- Common text transformation recipes
- Integration with other command-line tools

The guide includes:
- String-literal vs regex mode usage
- Capture group patterns and replacements
- Pipeline operations and batch processing
- Advanced regex patterns and edge cases
- Integration with other command-line tools

## Skill Combinations

### For Discovery Phase
- **ripgrep → sd**: Search patterns first, then replace across matches
- **fd → sd**: Find files and perform batch replacements
- **jq/yq → sd**: Extract data and transform to other formats

### For Analysis Phase
- **sd --preview → bat**: Preview changes with syntax highlighting
- **sd → fzf**: Interactive selection of changes to apply
- **sd → jq/yq**: Transform data back to structured formats

### For Refactoring Phase
- **sd → searching-text**: Verify replacements didn't introduce issues
- **sd → analyzing-code-structure**: Follow up with structural changes if needed
- **sd → analyzing-code**: Measure impact of text-based changes

### Integration Examples
```bash
# Find and replace across project
fd -e js -x sd "oldPattern" "newPattern" --preview

# Chain transformations
cat config.json | jq '.version' | sd '"v' '' | sd '"' '' | xargs git tag

# Interactive replacement with preview
rg "deprecated" -l | fzf --multi | xargs sd "deprecated" "legacy" --preview | bat
```
