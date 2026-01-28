---
name: ask-gemini
description: Asks Gemini CLI for coding assistance. Use for getting a second opinion, code generation, debugging, or delegating coding tasks.
allowed-tools: Bash(gemini:*)
---

# Ask Gemini

Executes the local `gemini` CLI to get coding assistance.

**Note:** This skill requires the `gemini` CLI to be installed and available in your system's PATH.

## Quick start

Run a single query using positional prompt:

```bash
gemini "Your question or task here"
```

## Common options

| Option | Description |
|--------|-------------|
| `-m MODEL` | Specify model |
| `-y, --yolo` | Auto-approve all tool executions |

> For all available options, run `gemini --help`

## Examples

**Ask a coding question:**

```bash
gemini "How do I implement a binary search in Python?"
```

**Use a specific model:**

```bash
gemini -m gemini-2.5-pro "Review this code for potential issues"
```

**Let Gemini make changes automatically:**

```bash
gemini -y "Refactor this function to use async/await"
```

## Notes

- Positional prompts run Gemini non-interactively and output result to stdout
- Gemini CLI uses the `GEMINI_API_KEY` environment variable for authentication
- Use `-y/--yolo` for automatic execution without confirmation prompts
- The command inherits the current working directory
