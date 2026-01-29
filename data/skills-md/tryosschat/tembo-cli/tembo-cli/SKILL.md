---
name: tembo-cli
description: Interact with the Tembo Public API to create coding tasks, list repositories, and manage AI agent workflows. Use when automating Tembo tasks, integrating Tembo into CI/CD pipelines, or building custom tooling around Tembo's AI coding agents.
license: MIT
metadata:
  author: tryosschat
  version: "0.1.0"
compatibility: Requires Bun runtime. Works with Claude Code, Cursor, and other skills-compatible agents.
---

# Tembo CLI Skill

A CLI tool for interacting with the Tembo Public API - manage AI coding tasks and repositories programmatically.

## When to Use This Skill

Use this skill when:
- Creating coding tasks for Tembo AI agents
- Listing and searching existing tasks
- Managing repository connections
- Automating Tembo workflows in CI/CD pipelines
- Building custom integrations with Tembo

## Installation

```bash
bun add -g github:tryosschat/tembo-cli
```

## Authentication

Get your API key from [app.tembo.io](https://app.tembo.io) → Settings → API Keys.

```bash
# Set your API key
tembo-cli auth login YOUR_API_KEY

# Verify authentication
tembo-cli auth whoami

# Check status
tembo-cli auth status
```

You can also set the `TEMBO_API_KEY` environment variable.

## Permissions

**Important**: Agents using this skill MUST ask for explicit user confirmation before running any command that modifies state. This includes:

- `tasks create` — creates a new coding task (costs compute, triggers an AI agent)
- `auth login` / `auth logout` — modifies stored credentials

Read-only commands (`tasks list`, `tasks search`, `repos list`, `auth whoami`, `auth status`) are safe to run without confirmation.

**Example**: Before creating a task, always confirm:
> "I'd like to create a Tembo task: *Fix the login bug* on repo `myorg/myapp`. Should I proceed?"

Never run background tasks or batch-create tasks without the user explicitly allowing it.

## Commands

### Authentication

| Command | Description |
|---------|-------------|
| `tembo-cli auth login <key>` | Save API key (validates against API) |
| `tembo-cli auth logout` | Remove stored API key |
| `tembo-cli auth whoami` | Show current user/organization |
| `tembo-cli auth status` | Show config path and key status |

### Tasks

| Command | Description |
|---------|-------------|
| `tembo-cli tasks list` | List tasks (`--page`, `--limit`, `--json`) |
| `tembo-cli tasks search <query>` | Search tasks (`--limit`, `--json`) |
| `tembo-cli tasks create <prompt>` | Create a new task |

#### Create Task Options

```bash
tembo-cli tasks create "Fix the login bug" \
  --agent "claudeCode:claude-4-5-sonnet" \
  --repo "https://github.com/org/repo" \
  --branch "main"
```

| Option | Description |
|--------|-------------|
| `-a, --agent <agent>` | Agent to use (default: `claudeCode:claude-opus-4-5`) |
| `-r, --repo <urls...>` | Repository URLs |
| `-b, --branch <branch>` | Target branch |
| `--no-queue` | Don't start task immediately |
| `--json` | Output as JSON |

### Repositories

| Command | Description |
|---------|-------------|
| `tembo-cli repos list` | List enabled repositories (`--json`) |

## Available Agents

Tembo supports multiple coding agents:

| Agent | Format |
|-------|--------|
| Claude Opus | `claudeCode:claude-opus-4-5` |
| Claude Sonnet | `claudeCode:claude-4-5-sonnet` |
| OpenAI Codex | `codex:...` |

## Examples

### Create a Bug Fix Task

```bash
tembo-cli tasks create "Fix the authentication bug in the login component" \
  --repo "https://github.com/myorg/myapp" \
  --branch "main"
```

### Create Task with Sonnet (Faster)

```bash
tembo-cli tasks create "Add input validation to the signup form" \
  --agent "claudeCode:claude-4-5-sonnet" \
  --repo "https://github.com/myorg/myapp"
```

### List Recent Tasks as JSON

```bash
tembo-cli tasks list --limit 5 --json
```

### Search for Specific Tasks

```bash
tembo-cli tasks search "authentication" --limit 10
```

### CI/CD Integration

```bash
# In GitHub Actions or similar
export TEMBO_API_KEY=${{ secrets.TEMBO_API_KEY }}
tembo-cli tasks create "Fix failing tests in PR #${PR_NUMBER}" \
  --repo "$GITHUB_REPOSITORY" \
  --branch "$GITHUB_HEAD_REF"
```

## API Reference

The CLI wraps the Tembo Public API at `https://api.tembo.io`:

| Endpoint | CLI Command |
|----------|-------------|
| `GET /me` | `auth whoami` |
| `POST /task/create` | `tasks create` |
| `GET /task/list` | `tasks list` |
| `GET /task/search` | `tasks search` |
| `GET /repository/list` | `repos list` |

## Configuration

Config is stored at `~/.tembo-cli/config.json`:

```json
{
  "apiKey": "your-api-key",
  "apiUrl": "https://api.tembo.io"
}
```

## Error Handling

The CLI provides clear error messages:

| Code | Meaning |
|------|---------|
| 401 | Invalid or missing API key |
| 429 | Rate limited (100 req/min, 1000 req/hr) |
| 500 | Server error |

## Troubleshooting

**"No API key found"**
```bash
tembo-cli auth login YOUR_API_KEY
# or
export TEMBO_API_KEY=YOUR_API_KEY
```

**"Invalid API key"**
Regenerate your key at [app.tembo.io](https://app.tembo.io) → Settings → API Keys

**"Rate limited"**
Wait a minute and retry. Consider batching requests.
