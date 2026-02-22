---
name: byterover
description: ByteRover CLI for context engineering - manage project knowledge, decisions, and patterns with AI coding agents.
---

# ByteRover CLI - Context Engineering Platform

ByteRover is a context engineering platform that lets you curate context for your coding agents—patterns, decisions, and learnings. It automatically syncs context across team members and eliminates manual markdown file management.

## Configuration

API credentials are stored in `~/.clawdbot/byterover-config.json`:
```json
{
  "apiKey": "your_byterover_api_key_here",
  "team": "your_team_name",
  "space": "your_space_name"
}
```

## Docker-Based Usage

ByteRover CLI requires Node.js 20+ and libsecret for credential storage. This skill uses Docker to provide an isolated environment with all dependencies.

### Start ByteRover Container

```bash
cd ~/.openclaw/workspace/skills/byterover
docker-compose up -d
```

### Run Commands in Container

**Login with API Key:**
```bash
docker-compose exec byterover brv login --api-key $BRV_API_KEY
```

**Initialize Project:**
```bash
docker-compose exec byterover brv init --headless --team "$BRV_TEAM" --space "$BRV_SPACE"
```

**Check Status:**
```bash
docker-compose exec byterover brv status --headless --format json
```

**Query Context:**
```bash
docker-compose exec byterover brv query "What are the testing strategies?" --headless --format json
```

**Curate Context:**
```bash
docker-compose exec byterover brv curate "Make sure to document API authentication patterns" --headless --format json
```

**Push Changes:**
```bash
docker-compose exec byterover brv push --headless --format json
```

**Pull Changes:**
```bash
docker-compose exec byterover brv pull --headless --format json
```

## Headless Mode

ByteRover CLI supports headless mode for automation and scripting. Headless mode disables interactive prompts and supports machine-readable JSON output.

### Supported Commands with --headless

- `brv init` (requires `--team` and `--space`)
- `brv status`
- `brv query`
- `brv curate`
- `brv push` (auto-skips confirmation)
- `brv pull`

### Output Formats

Use `--format` to control output:
- `text` (default): Human-readable text output
- `json`: NDJSON (newline-delimited JSON) for machine parsing

## API Key Authentication

Instead of OAuth browser flow, use API key for headless environments:

```bash
brv login --api-key $BRV_API_KEY
```

## Context Tree

The **Context Tree** is ByteRover's structured knowledge system that organizes project context into domains:
- **Structure** - Project architecture and patterns
- **Database** - Schema, migrations, relationships
- **Backend** - API endpoints, business logic
- **Frontend** - UI components, state management
- **Testing** - Test strategies, fixtures
- **Deployment** - Infrastructure, CI/CD
- **Documentation** - Guides, API docs

## Usage Examples

### For AI Coding Agents

**Prompt your coding agent:**
> Use brv query command to check what authentication patterns are used in this project

**Agent will execute:**
```bash
brv query "What authentication patterns are used?" --headless --format json
```

### Manual Usage

**Check project status:**
```bash
~/.openclaw/workspace/skills/byterover/docker-compose exec byterover brv status
```

**Add context from terminal:**
```bash
~/.openclaw/workspace/skills/byterover/docker-compose exec byterover brv curate "Document the API rate limiting strategy"
```

**Query specific knowledge:**
```bash
~/.openclaw/workspace/skills/byterover/docker-compose exec byterover brv query "How do we handle rate limiting?"
```

## Helper Scripts

### Quick Status Check
```bash
#!/bin/bash
# ~/.openclaw/workspace/skills/byterover/scripts/status.sh

CONFIG=$(cat ~/.clawdbot/byterover-config.json)
API_KEY=$(echo "$CONFIG" | jq -r '.apiKey')
TEAM=$(echo "$CONFIG" | jq -r '.team')
SPACE=$(echo "$CONFIG" | jq -r '.space')

cd ~/.openclaw/workspace/skills/byterover
BRV_API_KEY="$API_KEY" BRV_TEAM="$TEAM" BRV_SPACE="$SPACE" \
  docker-compose exec -T byterover brv status --headless --format json
```

### Query Context
```bash
#!/bin/bash
# ~/.openclaw/workspace/skills/byterover/scripts/query.sh

QUERY="${1:-project overview}"
CONFIG=$(cat ~/.clawdbot/byterover-config.json)
API_KEY=$(echo "$CONFIG" | jq -r '.apiKey')
TEAM=$(echo "$CONFIG" | jq -r '.team')
SPACE=$(echo "$CONFIG" | jq -r '.space')

cd ~/.openclaw/workspace/skills/byterover
BRV_API_KEY="$API_KEY" BRV_TEAM="$TEAM" BRV_SPACE="$SPACE" \
  docker-compose exec -T byterover brv query "$QUERY" --headless --format json
```

### Add Context
```bash
#!/bin/bash
# ~/.openclaw/workspace/skills/byterover/scripts/curate.sh

CONTEXT="${1}"
CONFIG=$(cat ~/.clawdbot/byterover-config.json)
API_KEY=$(echo "$CONFIG" | jq -r '.apiKey')
TEAM=$(echo "$CONFIG" | jq -r '.team')
SPACE=$(echo "$CONFIG" | jq -r '.space')

cd ~/.openclaw/workspace/skills/byterover
BRV_API_KEY="$API_KEY" BRV_TEAM="$TEAM" BRV_SPACE="$SPACE" \
  docker-compose exec -T byterover brv curate "$CONTEXT" --headless --format json
```

### Sync Changes
```bash
#!/bin/bash
# ~/.openclaw/workspace/skills/byterover/scripts/sync.sh

CONFIG=$(cat ~/.clawdbot/byterover-config.json)
API_KEY=$(echo "$CONFIG" | jq -r '.apiKey')
TEAM=$(echo "$CONFIG" | jq -r '.team')
SPACE=$(echo "$CONFIG" | jq -r '.space')

cd ~/.openclaw/workspace/skills/byterover

echo "Pulling latest context..."
BRV_API_KEY="$API_KEY" BRV_TEAM="$TEAM" BRV_SPACE="$SPACE" \
  docker-compose exec -T byterover brv pull --headless --format json

echo "Pushing local changes..."
BRV_API_KEY="$API_KEY" BRV_TEAM="$TEAM" BRV_SPACE="$SPACE" \
  docker-compose exec -T byterover brv push --headless --format json
```

## Docker Management

**Build image:**
```bash
cd ~/.openclaw/workspace/skills/byterover
docker-compose build
```

**Start container:**
```bash
docker-compose up -d
```

**Stop container:**
```bash
docker-compose down
```

**View logs:**
```bash
docker-compose logs -f
```

**Enter container shell:**
```bash
docker-compose exec byterover bash
```

## Integration with AI Agents

ByteRover provides multiple integration methods:

### 1. Skill Files (Claude Code, Cursor)
Modern, discoverable skill files that agents can inspect and execute automatically.

### 2. MCP Tools (Universal)
Model Context Protocol tools for broad agent compatibility.

### 3. Rules-Based (Legacy)
Generated rule files for older integrations.

## JSON Output Structure

NDJSON format with message types:
- `log`: Progress messages
- `output`: Main output content
- `error`: Error messages
- `warning`: Warning messages
- `result`: Final operation result

## Environment Variables

- `BRV_API_KEY` - ByteRover API key
- `BRV_TEAM` - Team name
- `BRV_SPACE` - Space name
- `BRV_HEADLESS` - Enable headless mode (true)
- `BRV_FORMAT` - Output format (json/text)

## Notes

- ByteRover requires a browser-based OAuth flow for first-time setup
- API key authentication bypasses OAuth for headless environments
- Context is automatically synced across team members
- No markdown files cluttering your codebase
- Works with 19+ AI coding agents

## Troubleshooting

**Build fails:**
- Ensure Docker daemon is running
- Check that port 80/443 is available

**Login fails:**
- Verify API key is valid
- Check team and space names are correct

**Container exits:**
- Check logs: `docker-compose logs`
- Ensure /workspace is mounted correctly

**Query returns no results:**
- Initialize project with `brv init`
- Add context with `brv curate`
- Sync with `brv pull`

## Requirements

- Docker
- Docker Compose
- ByteRover account
- Active team and space

## License

MIT

## Author

Created for OpenClaw by Jun Suzuki

---

For more information about ByteRover, visit: https://docs.byterover.dev/
