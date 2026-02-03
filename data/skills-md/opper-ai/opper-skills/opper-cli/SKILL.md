---
name: opper-cli
description: >
  Use the Opper CLI (oppercli) for terminal-based AI task completion, function management, knowledge base operations, model configuration, trace inspection, and usage analytics. Activate when users want to call Opper functions from the command line, manage indexes, inspect traces, track costs, or configure models via terminal.
---

# Opper CLI

Command-line interface for the Opper platform. Call functions, manage knowledge bases, configure models, inspect traces, and track usage from your terminal.

## Installation

**Homebrew (macOS):**

```bash
brew tap opper-ai/oppercli git@github.com:opper-ai/oppercli
brew install opper
```

**Binary download (macOS ARM64):**

```bash
sudo curl -o /usr/local/bin/opper https://github.com/opper-ai/oppercli/releases/latest/download/opper-darwin-arm64
sudo chmod 755 /usr/local/bin/opper
```

Other platforms: download from [GitHub Releases](https://github.com/opper-ai/oppercli/releases/latest) (`opper-linux-amd64`, `opper-darwin-amd64`, etc.).

## Configuration

Set up your API key:

```bash
opper config add default <your-api-key>
```

Use multiple configurations with the `--key` flag:

```bash
opper config add staging <staging-api-key>
opper call --key staging myfunction "instructions" "input"
```

## Core Command: `call`

Execute an Opper function from the terminal:

```bash
# Basic call
opper call myfunction "respond in kind" "what is 2+2?"

# With a specific model
opper call --model anthropic/claude-4-sonnet myfunction "summarize this" "long text..."

# Pipe input from stdin
echo "what is 2+2?" | opper call myfunction "respond in kind"
```

## Commands Overview

| Command | Description |
|---------|-------------|
| `call` | Execute a function with instructions and input |
| `functions` | List, get, chat with, and run evaluations on functions |
| `indexes` | Manage knowledge base indexes (list, get, create, delete, add, query, upload) |
| `models` | Register, list, get, test, delete custom models, and list builtins |
| `traces` | Inspect execution traces |
| `usage` | Track usage analytics, tokens, and costs by tags |
| `config` | Manage API key configurations |
| `version` | Display CLI version |

## Function Chat

Interactive chat with a function:

```bash
opper functions chat myfunction "Hello there!"
echo "Hello there!" | opper functions chat myfunction
```

## Model Management

Register custom models (uses LiteLLM identifiers):

```bash
# Register an Azure-deployed model
opper models create my-gpt4 azure/my-gpt4-deployment my-api-key '{"api_base": "https://my.openai.azure.com", "api_version": "2024-02-01"}'

# List registered models
opper models list

# List built-in models
opper models builtin

# Get details of a model
opper models get my-gpt4

# Test a model interactively
opper models test my-gpt4

# Delete a model
opper models delete my-gpt4
```

## Usage Tracking

Query usage analytics with filtering and grouping:

```bash
# Usage for a date range grouped by tag
opper usage list --from-date=2025-05-15 --to-date=2025-05-16 --fields=total_tokens --group-by=model

# Time-precise query (RFC3339 format)
opper usage list --from-date=2025-05-15T14:00:00Z --to-date=2025-05-15T16:00:00Z --granularity=minute

# Export as CSV
opper usage list --out=csv
```

Note: `cost` and `count` are always included automatically. Valid `--fields` values: `total_tokens`, `prompt_tokens`, `completion_tokens`. Do NOT pass `count` as a field.

## Global Flags

| Flag | Description |
|------|-------------|
| `--debug` | Enable diagnostic output |
| `--key <name>` | API key configuration to use (default: "default") |
| `-h, --help` | Show help for any command |

## Common Mistakes

- **Missing config**: Run `opper config add default <key>` before using any commands.
- **Wrong argument order for `call`**: It's `opper call <function> <instructions> <input>`, not `opper call <instructions> <function> <input>`.
- **Model identifiers**: Use LiteLLM format (`azure/deployment-name`, `anthropic/claude-4-sonnet`), not raw model names.
- **Piping with chat**: When piping, the function name still comes first: `echo "hi" | opper functions chat myfunction`.

## Additional Resources

- For function management details, see [references/FUNCTIONS.md](references/FUNCTIONS.md)
- For index/knowledge base operations, see [references/INDEXES.md](references/INDEXES.md)
- For usage analytics and cost tracking, see [references/USAGE.md](references/USAGE.md)
- For API key configuration, see [references/CONFIG.md](references/CONFIG.md)

## Related Skills

- **opper-api**: Use when you need the full REST API reference for HTTP-based integrations.
- **opper-python-sdk**: Use when building Python applications with the Opper SDK.
- **opper-node-sdk**: Use when building TypeScript applications with the Opper SDK.

## Upstream Sources

If this skill's content is outdated, check the canonical sources:

- **Source code**: https://github.com/opper-ai/oppercli
