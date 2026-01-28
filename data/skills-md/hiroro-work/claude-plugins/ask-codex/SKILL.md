---
name: ask-codex
description: Asks Codex CLI for coding assistance. Use for getting a second opinion, code generation, debugging, or delegating coding tasks.
allowed-tools: Bash(codex:*)
---

# Ask Codex

Executes the local `codex` CLI to get coding assistance.

**Note:** This skill requires the `codex` CLI to be installed and available in your system's PATH.

## Quick start

Run a single query with `codex exec`:

```bash
codex exec "Your question or task here"
```

## Common options

| Option | Description |
|--------|-------------|
| `-m MODEL` | Specify model |
| `-C DIR` | Set working directory |
| `--full-auto` | Enable automatic execution with workspace-write sandbox |

> For all available options, run `codex exec --help`

## Examples

**Ask a coding question:**

```bash
codex exec "How do I implement a binary search in Python?"
```

**Analyze code in a specific directory:**

```bash
codex exec -C /path/to/project "Explain the architecture of this codebase"
```

**Use a specific model:**

```bash
codex exec -m o4-mini "Write a function that validates email addresses"
```

**Let Codex make changes automatically:**

```bash
codex exec --full-auto "Add error handling to all API endpoints"
```

## Notes

- Codex runs non-interactively with `exec` subcommand
- By default, output goes to stdout and no files are modified without approval
- Use `--full-auto` for automatic execution within sandbox constraints
- The command inherits the current working directory unless `-C` is specified
