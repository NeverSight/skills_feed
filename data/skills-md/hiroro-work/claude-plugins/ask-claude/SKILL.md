---
name: ask-claude
description: Asks Claude CLI for coding assistance. Use for getting a second opinion, code generation, debugging, or delegating coding tasks.
allowed-tools: Bash(claude:*)
---

# Ask Claude

Executes the local `claude` CLI to get coding assistance.

**Note:** This skill requires the `claude` CLI to be installed and available in your system's PATH.

## Quick start

Run a single query with `-p` (print mode):

```bash
claude -p "Your question or task here"
```

## Common options

| Option | Description |
|--------|-------------|
| `-p` | Non-interactive print mode (required for scripting) |
| `--model MODEL` | Specify model (e.g., `sonnet`, `opus`, `haiku`) |
| `--output-format FORMAT` | Output format: `text`, `json`, `stream-json` |
| `-c, --continue` | Continue the most recent conversation |

> For all available options, run `claude --help`

## Examples

**Ask a coding question:**

```bash
claude -p "How do I implement a binary search in Python?"
```

**Use a specific model:**

```bash
claude -p --model opus "Review this code for potential issues"
```

**Get JSON output:**

```bash
claude -p --output-format json "List the main functions in this file"
```

**Continue a previous conversation:**

```bash
claude -p -c "Now add error handling to that function"
```

## Notes

- The `-p` flag runs Claude non-interactively and outputs result to stdout
- If `--model` is not specified, the default model is used
- `stream-json` outputs responses incrementally as they are generated
- **Warning**: The `-p` flag skips the workspace trust dialog. Only use in directories you trust.
- The command inherits the current working directory
