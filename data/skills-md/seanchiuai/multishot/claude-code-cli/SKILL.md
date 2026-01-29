---
name: claude-code-cli
description: Claude Code CLI usage for automated/headless execution in Daytona sandboxes. Use when running Claude Code commands, configuring authentication, or setting up non-interactive mode.
---

# Claude Code CLI

> Source: [Claude Code CLI Reference](https://code.claude.com/docs/en/cli-usage), [Headless Usage](https://code.claude.com/docs/en/headless)

## Installation

```bash
# Native (recommended)
curl -fsSL https://claude.ai/install.sh | bash

# NPM (deprecated)
npm install -g @anthropic-ai/claude-code
```

Verify: `claude --version`

## Authentication

### Environment Variables

| Variable | Description | Priority |
|----------|-------------|----------|
| `ANTHROPIC_API_KEY` | API key from console.anthropic.com | High (overrides OAuth) |
| `CLAUDE_CODE_OAUTH_TOKEN` | OAuth token for subscription auth | Normal |

**Warning**: Setting `ANTHROPIC_API_KEY` bypasses subscription and uses pay-as-you-go API rates.

### For Headless/Sandbox Use

Since Claude Code requires browser-based OAuth, use one of:

1. **API Key** (recommended for CI/sandboxes):
   ```bash
   export ANTHROPIC_API_KEY="sk-ant-..."
   claude -p "your prompt"
   ```

2. **OAuth Token Transfer** (from authenticated machine):
   ```bash
   # On local machine: authenticate normally, then copy token
   # Location: ~/.config/claude-code/auth.json
   # Transfer to sandbox via environment variable
   export CLAUDE_CODE_OAUTH_TOKEN="token-from-auth-json"
   ```

### Check Current Auth

In interactive mode: `/status`

## Non-Interactive Mode (-p / --print)

For automated execution, use `-p` flag:

```bash
claude -p "your prompt here"
```

This runs the prompt and exits (no REPL).

## Essential Flags

### Core Flags

| Flag | Description | Example |
|------|-------------|---------|
| `-p, --print` | Non-interactive mode, exit after response | `claude -p "explain this"` |
| `-c, --continue` | Continue most recent conversation | `claude -c -p "now fix it"` |
| `-r, --resume <id>` | Resume specific session | `claude -r "abc123" "continue"` |
| `--model <name>` | Set model (`sonnet`, `opus`, or full name) | `claude --model opus -p "..."` |

### Permission & Security

| Flag | Description |
|------|-------------|
| `--dangerously-skip-permissions` | Skip ALL permission prompts (use with caution) |
| `--allowedTools <tools>` | Auto-approve specific tools without prompting |
| `--disallowedTools <tools>` | Block specific tools entirely |
| `--permission-mode <mode>` | Start in specific mode (e.g., `plan`) |

### Tool Control

```bash
# Allow specific tools (comma-separated)
claude -p "fix the bug" --allowedTools "Read,Edit,Bash"

# Allow with prefix matching (e.g., any git command)
claude -p "commit changes" --allowedTools "Bash(git:*)"

# Disable all tools
claude -p "explain this" --tools ""

# Use only specific tools
claude -p "review code" --tools "Read,Grep,Glob"
```

### Output Formats

| Flag | Value | Description |
|------|-------|-------------|
| `--output-format` | `text` | Plain text (default) |
| | `json` | JSON with metadata |
| | `stream-json` | Newline-delimited JSON streaming |

```bash
# Get JSON output
claude -p "summarize" --output-format json

# Parse with jq
claude -p "summarize" --output-format json | jq -r '.result'

# Structured output with schema
claude -p "list functions" --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}}}'
```

### System Prompt

| Flag | Description |
|------|-------------|
| `--system-prompt <text>` | Replace entire system prompt |
| `--append-system-prompt <text>` | Add to default prompt (recommended) |
| `--system-prompt-file <path>` | Load replacement from file |
| `--append-system-prompt-file <path>` | Append from file |

```bash
# Append custom instructions (keeps defaults)
claude -p "review this" --append-system-prompt "Focus on security vulnerabilities"

# Replace entire prompt
claude -p "task" --system-prompt "You are a Python expert"
```

### Budget & Limits

| Flag | Description |
|------|-------------|
| `--max-budget-usd <amount>` | Maximum spend (print mode only) |
| `--max-turns <n>` | Limit agentic turns (print mode only) |

```bash
claude -p "refactor this file" --max-budget-usd 5.00 --max-turns 10
```

### Session Management

```bash
# Get session ID from output
session_id=$(claude -p "start review" --output-format json | jq -r '.session_id')

# Resume later
claude -p "continue" --resume "$session_id"

# Continue most recent
claude -p "what was I doing?" --continue
```

## Recommended Sandbox Configuration

For running in Daytona sandboxes:

```bash
# Full automated execution with tool access
ANTHROPIC_API_KEY="sk-ant-..." claude -p "Create a hello world Python script" \
  --dangerously-skip-permissions \
  --output-format json \
  --max-turns 20

# Or with specific tool allowlist
ANTHROPIC_API_KEY="sk-ant-..." claude -p "Fix the bug in auth.py" \
  --allowedTools "Read,Edit,Bash,Grep,Glob" \
  --output-format json

# With OAuth token instead
CLAUDE_CODE_OAUTH_TOKEN="token..." claude -p "Explain this codebase" \
  --dangerously-skip-permissions
```

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (check stderr) |

## Piped Input

```bash
# Pipe file content
cat src/main.ts | claude -p "explain this code"

# Pipe command output
git diff | claude -p "review these changes"

# Pipe multiple files
cat src/*.ts | claude -p "find security issues"
```

## Common Patterns

### Code Review

```bash
git diff HEAD~1 | claude -p "Review these changes for bugs and improvements" \
  --append-system-prompt "Focus on security and performance" \
  --output-format json
```

### Bug Fix

```bash
claude -p "Fix the failing test in tests/auth.test.ts" \
  --allowedTools "Read,Edit,Bash(npm test:*)" \
  --max-turns 15
```

### Code Generation

```bash
claude -p "Create a REST API endpoint for user registration" \
  --dangerously-skip-permissions \
  --max-turns 30
```

### Explanation Only (No Tools)

```bash
cat complex-file.ts | claude -p "Explain how this works" --tools ""
```

## Error Messages to Watch For

In sandbox output, watch for:
- `"Authentication failed"` - Invalid token/key
- `"OAuth token has expired"` - Need fresh token
- `"Invalid API key"` - Check ANTHROPIC_API_KEY
- `"Rate limit exceeded"` - Back off and retry
- `"Context length exceeded"` - Reduce input size

## Notes

- **Skills/slash commands** (like `/commit`) only work in interactive mode, not with `-p`
- `-p` mode exits after completion; use `--continue` for multi-step tasks
- `--dangerously-skip-permissions` gives full tool access - use in trusted environments only
- Output buffering: Claude streams output, buffer at ~100ms for IPC efficiency
