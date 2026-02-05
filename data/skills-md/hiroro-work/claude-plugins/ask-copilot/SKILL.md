---
name: ask-copilot
description: Asks Copilot CLI for coding assistance. Use for getting a second opinion, code generation, debugging, or delegating coding tasks.
allowed-tools: Bash(copilot *)
---

# Ask Copilot

Executes the local `copilot` CLI to get coding assistance.

**Note:** This skill requires the `copilot` CLI to be installed and available in your system's PATH.

## Quick start

Run a single query with `-p` (prompt mode):

```bash
copilot -p "Your question or task here" --allow-all-tools
```

## Common options

| Option | Description |
|--------|-------------|
| `-p` | Non-interactive prompt mode (required for scripting) |
| `--model MODEL` | Specify model (e.g., `claude-sonnet-4.5`, `gpt-5`, `gpt-5-mini`) |
| `--allow-all-tools` | Auto-approve all tool executions (required for -p) |
| `--continue` | Resume the most recent session |

> For all available options, run `copilot --help`

## Examples

**Ask a coding question:**

```bash
copilot -p "How do I implement a binary search in Python?" --allow-all-tools
```

**Use a specific model:**

```bash
copilot -p "Review this code for potential issues" --model gpt-5 --allow-all-tools
```

**Let Copilot make changes automatically:**

```bash
copilot -p "Refactor this function to use async/await" --allow-all-tools
```

**Continue a previous session:**

```bash
copilot --continue --allow-all-tools
```

## Notes

- The `-p` flag runs Copilot non-interactively and requires `--allow-all-tools`
- Default model is claude-sonnet-4.5; use `--model` to switch models
- The command inherits the current working directory
