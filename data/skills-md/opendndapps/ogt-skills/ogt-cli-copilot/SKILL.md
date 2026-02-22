---
name: ogt-cli-copilot
description: Run GitHub Copilot CLI for code generation, repository analysis, and development tasks. GitHub OAuth integrated. Use for quick coding tasks, context-aware completions, and repository-wide insights. Preferred for load balancing sub-agent work (30% weight).
metadata: {"moltbot":{"emoji":"🚀","requires":{"bins":["gh"]},"install":[{"id":"gh-cli","kind":"github","package":"cli","bins":["gh"],"label":"Install GitHub CLI (gh)"}]}}
---

# GitHub Copilot CLI Skill

Use GitHub Copilot CLI to leverage GitHub's code intelligence directly from the terminal via GitHub OAuth.

## When to Use

- Quick code generation and scaffolding
- Repository-aware code suggestions and completions
- Code explanation and documentation generation
- Multi-file code analysis
- Git-aware tasks and automation
- Fast iteration on coding problems

## Quick Start

### Interactive mode
```bash
gh copilot
```

### Explain code
```bash
gh copilot explain "path/to/file.py"
```

### Generate code
```bash
gh copilot suggest "create a function that validates email addresses"
```

### With specific context
```bash
cd /path/to/repo && gh copilot suggest "add error handling to main.py"
```

## Installation

```bash
# GitHub CLI is required
brew install gh  # macOS
# or apt-get install gh  # Linux
# or choco install gh  # Windows

# Verify installation
gh --version
```

## Key Commands

| Command | Description |
|---------|-------------|
| `gh copilot` | Interactive mode |
| `gh copilot explain <file>` | Explain code in a file |
| `gh copilot suggest "<prompt>"` | Generate code from description |
| `gh copilot review <file>` | Review code for issues |

## Authentication

Copilot CLI uses GitHub OAuth via `gh cli`:

```bash
# First-time authentication
gh auth login

# Check auth status
gh auth status
```

No API key configuration needed—authentication is linked to your GitHub account.

## Working with Files

Copilot CLI is repository-aware and understands your codebase:

```bash
# Explain file in current repo
gh copilot explain src/api.ts

# Generate code in context of repo
cd /path/to/project && gh copilot suggest "add unit tests for User service"

# Review code changes
gh copilot review src/components/Button.tsx
```

## Built-in Capabilities

- **Repository Awareness:** Understands your codebase structure and conventions
- **Git Integration:** Access to commit history and branch context
- **Language Support:** Works with multiple programming languages
- **Smart Suggestions:** Context-aware code generation

## For Sub-Agent Delegation

When spawning Copilot CLI for background work:

```bash
# Explain code non-interactively
gh copilot explain myfile.js 2>&1

# Generate code and capture output
gh copilot suggest "parse JSON file" 2>&1 > generated_code.js

# Run with timeout
timeout 120 gh copilot suggest "implement authentication" 2>&1
```

### Script: Run Copilot Task

Use the bundled script for reliable sub-agent execution:

```bash
node {baseDir}/scripts/run-copilot-task.cjs "Your task prompt" [options]
```

Options:
- `--action <action>` — Action: `suggest`, `explain`, `review` (default: suggest)
- `--file <path>` — File path for `explain` or `review` actions
- `--timeout <secs>` — Timeout in seconds (default: 120)
- `--workdir <path>` — Working directory

The script handles:
- Timeout protection
- Error capture and formatting
- Clean output for parsing
- Exit code propagation

## Tips

1. **Repository matters** — Copilot uses your codebase for context
2. **Use relative paths** — File paths relative to current directory
3. **Brief prompts work best** — Clear, specific suggestions get better results
4. **Check git status** — Copilot uses git history for context
5. **Review generated code** — Always review suggestions before committing

## Rate Limits

Rate limits depend on your GitHub plan:
- GitHub Free: Limited suggestions per day
- GitHub Pro/Teams: Higher rate limits
- GitHub Enterprise: Custom limits

## Comparison with Other CLIs

| Feature | Copilot | Claude CLI | Gemini CLI |
|---------|---------|-----------|-----------|
| Repository awareness | ✅ Native | ❌ | ❌ |
| Git integration | ✅ Native | ❌ | ❌ |
| GitHub OAuth | ✅ | ❌ | ❌ |
| Free tier | ✅ Limited | ✅ Limited | ✅ 1000/day |
| Extended thinking | ❌ | ✅ | ❌ |

## Troubleshooting

### Authentication Issues
```bash
# Check auth status
gh auth status

# Re-authenticate
gh auth logout
gh auth login
```

### Command Not Found
```bash
# Verify GitHub CLI installed
which gh

# Check Copilot extension
gh extension list

# Reinstall GitHub CLI
brew reinstall gh
```

### No Copilot Suggestions
```bash
# Ensure you have GitHub Copilot license/subscription
gh auth status

# Try from repository directory
cd /path/to/repo && gh copilot suggest "your prompt"
```
