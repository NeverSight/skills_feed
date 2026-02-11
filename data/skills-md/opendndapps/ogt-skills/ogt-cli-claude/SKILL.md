---
name: ogt-cli-claude
description: Run Claude Code CLI for complex tasks, code generation, analysis, and research. Uses Anthropic OAuth (included in Claude Pro). Use for extended thinking, code review, architecture decisions. Preferred for load balancing sub-agent work (35% weight).
metadata: {"moltbot":{"emoji":"🧠","requires":{"bins":["claude"]},"install":[{"id":"npm","kind":"node","package":"@anthropic-ai/claude-code","bins":["claude"],"label":"Install Claude Code (npm)"}]}}
---

# Claude CLI Skill

Run Claude Code CLI to leverage Anthropic's models via OAuth authentication (no API tokens required).

## When to Use

- Complex coding tasks that benefit from extended context
- Multi-file code generation or refactoring
- Research and analysis requiring deep reasoning
- Tasks that would benefit from Claude's thinking mode
- Delegating substantial work to a sub-process

## Quick Start

### One-shot query (non-interactive)
```bash
echo "Your prompt here" | claude -p
```

### With specific model
```bash
echo "Complex task requiring Opus" | claude -p --model opus
echo "Standard task with Sonnet" | claude -p --model sonnet
```

**Note:** Piping the prompt via stdin is more reliable than passing it as an argument.

### With thinking/extended reasoning
```bash
claude -p --model opus "Analyze this complex problem"
```

### JSON output (for parsing)
```bash
claude -p --output-format json "Your prompt"
```

### Stream JSON (real-time)
```bash
claude -p --output-format stream-json "Your prompt"
```

## Key Options

| Option | Description |
|--------|-------------|
| `-p, --print` | Non-interactive mode, print and exit |
| `--model <model>` | Model alias: `sonnet`, `opus`, or full name |
| `--output-format <fmt>` | `text` (default), `json`, `stream-json` |
| `--system-prompt <prompt>` | Custom system prompt |
| `--max-budget-usd <amount>` | Spending limit for the call |
| `--allowedTools <tools>` | Restrict available tools |
| `--dangerously-skip-permissions` | Skip permission checks (sandboxed use only) |

## Working with Files

Claude CLI can read and write files in its working directory:

```bash
# Analyze a file
claude -p "Review this code for bugs" < myfile.py

# Work in a specific directory
cd /path/to/project && claude -p "Summarize this codebase"

# Give access to additional directories
claude -p --add-dir /other/path "Work with files in both locations"
```

## For Sub-Agent Delegation

When spawning Claude CLI for background work:

```bash
# Run with timeout protection
timeout 300 claude -p --model sonnet "Complete this task..." 2>&1

# Capture structured output
claude -p --output-format json "Generate a report" > result.json
```

### Script: Run Claude Task

Use the bundled script for reliable sub-agent execution:

```bash
node {baseDir}/scripts/run-claude-task.cjs "Your task prompt" [--model sonnet|opus] [--timeout 300]
```

The script handles:
- Timeout protection
- Error capture and formatting
- Clean output for parsing
- Exit code propagation

## Authentication

Claude CLI uses OAuth by default (linked to your Anthropic account). No API key configuration needed.

To check auth status:
```bash
claude --version
```

If not authenticated, run interactively once:
```bash
claude
```
Follow the OAuth prompts to link your account.

## Model Selection

| Alias | Best For |
|-------|----------|
| `sonnet` | Fast, capable, cost-effective. Default choice. |
| `opus` | Complex reasoning, nuanced tasks, extended thinking. |

## Tips

1. **Always use `-p`** for non-interactive/scripted use
2. **Set timeouts** for long-running tasks to prevent hangs
3. **Use `--output-format json`** when you need to parse results
4. **Pipe input** for file analysis: `cat file.py | claude -p "Review this"`
5. **Working directory matters** — Claude sees files relative to cwd

## Limitations

- OAuth requires initial interactive setup
- Rate limits apply based on your Anthropic account tier
- Some operations may timeout on very complex tasks
- Interactive features (like file editing confirmations) don't work with `-p`
