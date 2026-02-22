---
name: ogt-cli-gemini
description: Run Gemini CLI for AI-powered tasks, code understanding, file operations, and automation. Free tier with Google OAuth (included in Gemini Advanced). Use for fast generation, bulk content, debugging, and research. Preferred for load balancing sub-agent work (35% weight).
metadata: {"moltbot":{"emoji":"💎","requires":{"bins":["gemini"]},"install":[{"id":"npm","kind":"node","package":"@google/gemini-cli","bins":["gemini"],"label":"Install Gemini CLI (npm)"},{"id":"brew","kind":"homebrew","package":"gemini-cli","bins":["gemini"],"label":"Install Gemini CLI (Homebrew)"}]}}
---

# Gemini CLI Skill

Run Google's Gemini CLI to leverage Gemini 3 models directly from the terminal.

## When to Use

- Code understanding and generation
- Multi-file analysis and refactoring
- Debugging with natural language
- Research with Google Search grounding
- Automation and scripting tasks
- Tasks benefiting from 1M token context window

## Quick Start

### Interactive mode
```bash
gemini
```

### One-shot query (non-interactive)
```bash
gemini -p "Your prompt here"
```

### With specific model
```bash
gemini -p "Complex task" -m gemini-2.5-pro
gemini -p "Quick task" -m gemini-2.5-flash
```

### JSON output (for parsing)
```bash
gemini -p "Your prompt" --output-format json
```

### Stream JSON (real-time events)
```bash
gemini -p "Run tests and deploy" --output-format stream-json
```

## Installation

```bash
# npm (recommended)
npm install -g @google/gemini-cli

# Homebrew (macOS/Linux)
brew install gemini-cli

# Run without installing
npx @google/gemini-cli
```

## Key Options

| Option | Description |
|--------|-------------|
| `-p, --prompt` | Non-interactive mode, print response and exit |
| `-m, --model` | Model: `gemini-2.5-flash`, `gemini-2.5-pro` |
| `--output-format` | `text` (default), `json`, `stream-json` |
| `--include-directories` | Include additional directories |
| `--yolo` | Auto-approve tool calls (use with caution) |
| `--sandbox` | Run in sandbox mode (safer) |

## Authentication

### Option 1: Google OAuth (Recommended)
```bash
gemini
# Follow browser auth flow on first run
```
- **Free tier:** 60 req/min, 1,000 req/day
- No API key needed

### Option 2: Gemini API Key
```bash
export GEMINI_API_KEY="YOUR_API_KEY"
gemini
```
Get key from: https://aistudio.google.com/apikey

### Option 3: Vertex AI (Enterprise)
```bash
export GOOGLE_API_KEY="YOUR_API_KEY"
export GOOGLE_GENAI_USE_VERTEXAI=true
gemini
```

## Working with Files

Gemini CLI can read and work with files in the current directory:

```bash
# Analyze codebase
cd /path/to/project && gemini -p "Explain this codebase architecture"

# Include multiple directories
gemini --include-directories ../lib,../docs -p "Review the API"

# Pipe file content
cat myfile.py | gemini -p "Review this code"
```

## Built-in Tools

Gemini CLI has built-in capabilities:
- **Google Search:** Ground responses with real-time web data
- **File Operations:** Read, write, edit files
- **Shell Commands:** Execute terminal commands
- **Web Fetching:** Retrieve content from URLs

## For Sub-Agent Delegation

When spawning Gemini CLI for background work:

```bash
# Run with timeout
timeout 300 gemini -p "Complete this task..." 2>&1

# Capture structured output
gemini -p "Generate a report" --output-format json > result.json

# Auto-approve for automation (careful!)
gemini -p "Run the build" --yolo
```

### Script: Run Gemini Task

Use the bundled script for reliable sub-agent execution:

```bash
node {baseDir}/scripts/run-gemini-task.cjs "Your task prompt" [options]
```

Options:
- `--model <model>` — Model to use (default: gemini-2.5-flash)
- `--timeout <secs>` — Timeout in seconds (default: 300)
- `--json` — Output in JSON format
- `--workdir <path>` — Working directory

The script handles:
- Timeout protection
- Error capture and formatting
- Clean output for parsing
- Exit code propagation

## Model Selection

| Model | Best For |
|-------|----------|
| `gemini-2.5-flash` | Fast, cost-effective, everyday tasks |
| `gemini-2.5-pro` | Complex reasoning, large context, nuanced tasks |

## Context File (GEMINI.md)

Create a `GEMINI.md` file in your project root to customize behavior:

```markdown
# Project: My App

## Guidelines
- Use TypeScript for all new code
- Follow existing patterns in src/
- Run tests before committing

## Architecture
- Frontend: React + Vite
- Backend: Node.js + Express
```

Gemini will automatically read this for project context.

## Tips

1. **Use `-p` for scripts** — Non-interactive mode for automation
2. **Set timeouts** for long-running tasks
3. **Use `--output-format json`** when parsing results programmatically
4. **Working directory matters** — Gemini sees files relative to cwd
5. **Use `--yolo` carefully** — Auto-approves all tool calls
6. **Google Search grounding** — Great for real-time info queries

## Rate Limits (Free Tier)

- 60 requests per minute
- 1,000 requests per day
- 1M token context window

## Comparison with Claude CLI

| Feature | Gemini CLI | Claude CLI |
|---------|------------|------------|
| Free tier | ✅ 1000/day | ✅ Limited |
| Context window | 1M tokens | 200K tokens |
| Google Search | ✅ Built-in | ❌ |
| Shell execution | ✅ Built-in | ✅ Built-in |
| MCP support | ✅ | ✅ |
| Auth | Google OAuth | Anthropic OAuth |

## Troubleshooting

### Authentication Issues
```bash
# Clear cached auth
rm -rf ~/.gemini-cli

# Re-authenticate
gemini
```

### Command Not Found
```bash
# Check installation
which gemini

# Reinstall
npm install -g @google/gemini-cli
```
