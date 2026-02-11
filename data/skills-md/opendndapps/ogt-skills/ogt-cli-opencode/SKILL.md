---
name: ogt-cli-opencode
description: Run OpenCode CLI for code generation, analysis, and development tasks. Uses OAuth authentication. Use for rapid prototyping, code refactoring, testing, and automation. Preferred for load balancing sub-agent work (35% weight).
metadata: {"moltbot":{"emoji":"⚡","requires":{"bins":["opencode"]},"install":[{"id":"npm","kind":"node","package":"opencode-cli","bins":["opencode"],"label":"Install OpenCode CLI (npm)"}]}}
---

# OpenCode CLI Skill

Run OpenCode CLI to leverage fast code generation and analysis tools directly from the terminal.

## When to Use

- Rapid code generation and scaffolding
- Quick refactoring tasks
- Test file generation
- Code quality analysis
- API integration generation
- Boilerplate and template creation
- Fast prototyping tasks

## Quick Start

### Interactive mode
```bash
opencode
```

### One-shot generation
```bash
opencode generate "Create a function that validates user emails"
```

### With specific template
```bash
opencode generate --template react-component "Button with loading state"
```

### Analyze code
```bash
opencode analyze myfile.js
```

### Generate tests
```bash
opencode test "src/utils/auth.js"
```

## Installation

```bash
# npm (recommended)
npm install -g opencode-cli

# Verify installation
opencode --version
```

## Key Commands

| Command | Description |
|---------|-------------|
| `opencode` | Interactive mode |
| `opencode generate "<prompt>"` | Generate code from description |
| `opencode analyze <file>` | Analyze code quality and structure |
| `opencode test <file>` | Generate test cases for file |
| `opencode refactor <file>` | Suggest refactoring improvements |
| `opencode document <file>` | Generate documentation |

## Key Options

| Option | Description |
|--------|-------------|
| `--template <name>` | Use specific code template |
| `--language <lang>` | Target language (js, ts, python, go, etc.) |
| `--output <path>` | Output file path |
| `--format <fmt>` | Output format (default, json, etc.) |
| `--model <model>` | Model variant (default, fast, quality) |

## Authentication

OpenCode CLI uses OAuth:

```bash
# First-time authentication
opencode auth login

# Check auth status
opencode auth status
```

No API key configuration needed—authentication is OAuth-based.

## Working with Files

OpenCode can read and generate code for files in your project:

```bash
# Analyze a file
opencode analyze src/api.ts

# Generate tests for existing code
opencode test src/utils/helpers.js

# Refactor code
opencode refactor src/components/Form.jsx

# Generate documentation
opencode document src/services/auth.js
```

## Code Templates

OpenCode includes templates for common patterns:

```bash
# List available templates
opencode templates list

# Use a specific template
opencode generate --template express-api "User management API"
opencode generate --template react-form "Login form"
opencode generate --template node-cli "CLI tool for backups"
```

## Built-in Capabilities

- **Template Library:** Pre-configured patterns for common use cases
- **Multi-language Support:** JavaScript, TypeScript, Python, Go, Rust, etc.
- **Test Generation:** Automatic unit and integration test creation
- **Code Analysis:** Quality metrics and improvement suggestions
- **Refactoring:** Smart refactoring recommendations

## For Sub-Agent Delegation

When spawning OpenCode CLI for background work:

```bash
# Generate code non-interactively
opencode generate "Express API with validation" 2>&1

# Analyze code and capture output
opencode analyze myfile.js --format json > analysis.json

# Generate tests
opencode test src/utils.js --output test/utils.test.js 2>&1

# Run with timeout
timeout 180 opencode generate "Database schema for e-commerce" 2>&1
```

### Script: Run OpenCode Task

Use the bundled script for reliable sub-agent execution:

```bash
node {baseDir}/scripts/run-opencode-task.cjs "Your task prompt" [options]
```

Options:
- `--action <action>` — Action: `generate`, `analyze`, `test`, `refactor`, `document` (default: generate)
- `--file <path>` — File path for non-generation actions
- `--template <name>` — Template to use for generation
- `--language <lang>` — Programming language
- `--timeout <secs>` — Timeout in seconds (default: 180)
- `--output <path>` — Output file path
- `--workdir <path>` — Working directory

The script handles:
- Timeout protection
- Error capture and formatting
- Clean output for parsing
- Exit code propagation

## Model Selection

OpenCode offers different model variants:

| Variant | Best For |
|---------|----------|
| `fast` | Quick generation, simple tasks |
| `default` | Balanced speed and quality (recommended) |
| `quality` | Complex code, high-quality output |

```bash
opencode generate --model quality "Complex state management system"
```

## Tips

1. **Be specific with descriptions** — Better prompts yield better code
2. **Use templates** for consistent patterns in your codebase
3. **Review generated code** — Always review and test generated code
4. **Combine with analysis** — Analyze before refactoring
5. **Set timeouts** for long-running generation tasks

## Rate Limits

Rate limits depend on your OpenCode plan:
- Free tier: Limited generations per day
- Pro tier: Higher rate limits and priority
- Team tier: Custom limits with team management

## Comparison with Other CLIs

| Feature | OpenCode | Claude CLI | Gemini CLI | Copilot CLI |
|---------|----------|-----------|-----------|------------|
| Template library | ✅ Extensive | ❌ | ❌ | ❌ |
| Test generation | ✅ Native | ❌ | ❌ | ❌ |
| Code analysis | ✅ Native | ❌ | ❌ | ❌ |
| Fast generation | ✅ Optimized | Slower | Medium | Medium |
| Extended context | ❌ | ✅ 200K tokens | ✅ 1M tokens | Limited |

## Working with Output

### JSON Output for Parsing

```bash
opencode analyze myfile.js --format json | jq '.issues'
```

### Save Generated Code

```bash
# Output to file
opencode generate "REST API boilerplate" --output api.js

# Or redirect
opencode generate "Database schema" > schema.sql
```

### Pipeline with Other Tools

```bash
# Generate, format, then lint
opencode generate "Express app" | prettier --write /dev/stdin

# Generate test and run immediately
opencode test src/utils.js && npm test
```

## Troubleshooting

### Authentication Issues
```bash
# Check auth status
opencode auth status

# Re-authenticate
opencode auth logout
opencode auth login
```

### Command Not Found
```bash
# Verify installation
which opencode

# Reinstall
npm install -g opencode-cli
```

### Generation Timeout
```bash
# Use longer timeout or simpler prompt
timeout 300 opencode generate "Simpler version: Basic auth endpoint"

# Try fast model
opencode generate --model fast "Your prompt"
```

### Poor Quality Output

```bash
# Use quality model
opencode generate --model quality "Complex feature needed here"

# Be more specific in prompt
opencode generate "User authentication API with JWT, email verification, and refresh tokens"

# Check templates first
opencode templates list
```
