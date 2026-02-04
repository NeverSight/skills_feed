---
name: repomix
description: Pack entire codebases into AI-friendly files for LLM analysis. Use when consolidating code for AI review, generating codebase summaries, or preparing context for ChatGPT, Claude, or other AI tools.
---

# Repomix - Codebase Packing for AI

Pack your entire repository into a single, AI-friendly file optimized for LLMs like Claude, ChatGPT, Gemini, and more.

## When to Use This Skill

- Feeding codebase to AI for analysis or refactoring
- Generating comprehensive code reviews
- Creating documentation from code
- Preparing context for AI-assisted development
- Analyzing remote repositories without cloning
- Token counting for LLM context limits

## Quick Start

```bash
# Pack current directory (no install required)
npx repomix@latest

# Pack specific directory
npx repomix path/to/directory

# Pack with compression (~70% token reduction)
npx repomix --compress

# Copy output to clipboard
npx repomix --copy
```

**Default output:** `./repomix-output.xml` in current directory

## Examples

**Example: Prepare codebase for Claude review**
```
User: "Pack my src folder for Claude to review the architecture"
→ npx repomix --include "src/**/*" --style xml --copy
→ Output copied to clipboard, ready to paste into Claude
```

**Example: Analyze remote repo without cloning**
```
User: "I want to understand how shadcn/ui implements its button"
→ npx repomix --remote shadcn-ui/ui --include "**/button/**/*" --compress
→ Generates focused output of button component
```

**Example: Prepare PR diff for review**
```
User: "Pack only the files I changed for a code review"
→ git diff --name-only main | npx repomix --stdin --compress
→ Packs only modified files with compression
```

**Example: Check token usage before sending to AI**
```
User: "Is my codebase too large for GPT-4?"
→ npx repomix --token-count-tree
→ Shows token breakdown per file/directory
```

**Example: Generate skills reference from library**
```
User: "Create a Claude skill from the zod repository"
→ npx repomix --remote colinhacks/zod --skill-generate zod-reference
→ Generates AI-optimized reference documentation
```

## Output Formats

```bash
# XML (default) - best for Claude
npx repomix --style xml

# Markdown - human readable
npx repomix --style markdown

# JSON - programmatic processing
npx repomix --style json

# Plain text
npx repomix --style plain
```

## Token Optimization

### LLM Context Limits Reference

| Model | Context Window | Typical Repo Fit |
|-------|---------------|------------------|
| Claude 3.5/Opus | 200K tokens | Large monorepos |
| GPT-4 Turbo/4o | 128K tokens | Medium projects |
| Gemini 1.5 Pro | 1M tokens | Very large codebases |
| Gemini 1.5 Flash | 1M tokens | Very large codebases |

### Token Analysis

```bash
# Show token count tree
npx repomix --token-count-tree

# Filter by minimum tokens (show files with 1000+ tokens)
npx repomix --token-count-tree 1000

# Split output for large codebases
npx repomix --split-output 1mb
```

## File Selection

### Include Patterns

```bash
# Include only TypeScript files
npx repomix --include "**/*.ts"

# Include multiple patterns
npx repomix --include "src/**/*.ts,**/*.md"

# Include specific directories
npx repomix --include "src/**/*,tests/**/*"
```

### Ignore Patterns

```bash
# Ignore test files
npx repomix --ignore "**/*.test.ts"

# Ignore multiple patterns
npx repomix --ignore "**/*.log,tmp/,dist/"

# Combine include and ignore
npx repomix --include "src/**/*.ts" --ignore "**/*.test.ts"
```

### Stdin Input

```bash
# From find command
find src -name "*.ts" -type f | npx repomix --stdin

# From git tracked files
git ls-files "*.ts" | npx repomix --stdin

# Interactive selection with fzf
find . -name "*.ts" -type f | fzf -m | npx repomix --stdin

# From ripgrep
rg --files --type ts | npx repomix --stdin
```

## Common Workflows

### PR Review Preparation

```bash
# Pack only changed files for review
git diff --name-only main | npx repomix --stdin --compress

# Pack with diff context included
npx repomix --include-diffs --compress
```

### Architecture Analysis

```bash
# Pack structure without implementation details
npx repomix --compress --include "src/**/*" --ignore "**/*.test.*"

# Focus on specific layer
npx repomix --include "src/api/**/*,src/services/**/*" --compress
```

### Documentation Generation

```bash
# Pack with full context for docs
npx repomix --include "src/**/*,**/*.md" --style markdown

# Include git history for changelog
npx repomix --include-logs --include-logs-count 50
```

### Dependency Analysis

```bash
# Pack only config and dependency files
npx repomix --include "package.json,tsconfig.json,**/*.config.*"
```

## Remote Repositories

```bash
# Pack remote repository
npx repomix --remote https://github.com/user/repo

# GitHub shorthand
npx repomix --remote user/repo

# Specific branch
npx repomix --remote user/repo --remote-branch main

# Specific commit
npx repomix --remote user/repo --remote-branch 935b695

# Branch URL format
npx repomix --remote https://github.com/user/repo/tree/feature-branch
```

## Code Compression

Tree-sitter powered compression extracts signatures while removing implementation details.

### Supported Languages

Tree-sitter compression works with: JavaScript, TypeScript, Python, Ruby, Go, Rust, Java, C, C++, C#, PHP, Swift, Kotlin, and more.

### Usage

```bash
npx repomix --compress

# Combine with remote
npx repomix --remote user/repo --compress
```

**Before compression:**
```typescript
const calculateTotal = (items: Item[]) => {
  let total = 0;
  for (const item of items) {
    total += item.price * item.quantity;
  }
  return total;
};
```

**After compression:**
```typescript
const calculateTotal = (items: Item[]) => { /* ... */ };
```

## Git Integration

```bash
# Include git logs (last 50 commits)
npx repomix --include-logs

# Specify commit count
npx repomix --include-logs --include-logs-count 20

# Include git diffs
npx repomix --include-diffs

# Combine logs and diffs
npx repomix --include-logs --include-diffs
```

## Configuration

### Initialize Config

```bash
# Create repomix.config.json
npx repomix --init

# Global config
npx repomix --init --global
```

### Configuration File

```json
{
  "$schema": "https://repomix.com/schemas/latest/schema.json",
  "output": {
    "filePath": "repomix-output.xml",
    "style": "xml",
    "compress": false,
    "removeComments": false,
    "showLineNumbers": false,
    "copyToClipboard": false
  },
  "include": ["src/**/*", "**/*.md"],
  "ignore": {
    "useGitignore": true,
    "useDefaultPatterns": true,
    "customPatterns": ["**/*.test.ts", "dist/"]
  },
  "security": {
    "enableSecurityCheck": true
  }
}
```

## Docker Usage

```bash
# Pack current directory
docker run -v .:/app -it --rm ghcr.io/yamadashy/repomix

# Pack specific directory
docker run -v .:/app -it --rm ghcr.io/yamadashy/repomix path/to/directory

# Remote repository
docker run -v ./output:/app -it --rm ghcr.io/yamadashy/repomix --remote user/repo
```

## MCP Server Integration

Run as Model Context Protocol server for AI assistants:

```bash
npx repomix --mcp
```

### Configure for Claude Code

```bash
claude mcp add repomix -- npx -y repomix --mcp
```

### Available MCP Tools

When running as MCP server, provides:

| Tool | Description |
|------|-------------|
| `pack_codebase` | Pack local directory into AI-friendly format |
| `pack_remote_repository` | Pack GitHub repository without cloning |
| `read_repomix_output` | Read contents of generated output file |
| `file_system_tree` | Get directory tree structure |

## Claude Agent Skills Generation

Generate skills format output for Claude:

```bash
# Generate skills from local directory
npx repomix --skill-generate

# Generate with custom name
npx repomix --skill-generate my-project-reference

# From remote repository
npx repomix --remote user/repo --skill-generate
```

## CLI Options Reference

| Option | Description |
|--------|-------------|
| `-o, --output <file>` | Output file path |
| `--style <style>` | Output format: xml, markdown, json, plain |
| `--compress` | Enable Tree-sitter compression |
| `--include <patterns>` | Include files matching glob patterns |
| `-i, --ignore <patterns>` | Exclude files matching patterns |
| `--remote <url>` | Process remote repository |
| `--remote-branch <name>` | Branch, tag, or commit for remote |
| `--stdin` | Read file paths from stdin |
| `--copy` | Copy output to clipboard |
| `--token-count-tree` | Show token counts per file |
| `--split-output <size>` | Split output by size (e.g., 1mb) |
| `--include-logs` | Include git commit history |
| `--include-diffs` | Include git diffs |
| `--no-security-check` | Skip sensitive data detection |
| `--mcp` | Run as MCP server |
| `--skill-generate` | Generate Claude skills format |
| `--init` | Create configuration file |
| `--help` | Show all available options |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Output too large for LLM | Use `--compress` or filter with `--include` |
| Missing expected files | Check `.repomixignore`, `.gitignore`, and ignore patterns |
| Secrets detected (blocking) | Review flagged files; use `--no-security-check` if false positive |
| Memory issues on large repos | Use `--split-output 1mb` to chunk output |
| Remote repo access denied | Check URL format; ensure repo is public or use SSH |
| Compression not working | Verify language is supported by Tree-sitter |
| Output not in clipboard | Ensure clipboard access; try `--output - \| pbcopy` on macOS |

## Ignore Files

Repomix respects multiple ignore sources (priority order):

1. `ignore.customPatterns` in config
2. `.repomixignore` (Repomix-specific)
3. `.ignore` (ripgrep compatible)
4. `.gitignore`
5. Default patterns (node_modules, .git, etc.)

## Security

Repomix includes Secretlint for detecting sensitive information:

```bash
# Security check enabled by default
npx repomix

# Disable security check (use with caution)
npx repomix --no-security-check
```

**Detected secret types:** API keys, tokens, passwords, private keys, AWS credentials, database connection strings, and more.

## Best Practices

1. **Use compression** for large codebases to reduce token count (~70% reduction)
2. **Filter with --include** to focus on relevant files
3. **Use --token-count-tree** to identify large files before packing
4. **Split output** when hitting AI context limits
5. **Include git logs** for evolution context when needed
6. **Use XML style** for Claude (optimized for XML tags)
7. **Use Markdown** for human-readable output or other LLMs
8. **Check token counts** against your target LLM's context window
9. **Review security warnings** before sharing packed output

## Requirements

- Node.js 18.0.0 or higher
- npm or npx available in PATH

## Resources

- Website: https://repomix.com
- GitHub: https://github.com/yamadashy/repomix
- Chrome Extension: Repomix - Chrome Web Store
- VSCode Extension: Repomix Runner
