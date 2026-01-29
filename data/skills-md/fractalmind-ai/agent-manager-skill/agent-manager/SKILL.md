---
name: agent-manager
description: Employee agent lifecycle management system. Use when working with agents/ directory employee agents - starting, stopping, monitoring, or assigning tasks to Dev/QA agents running in tmux sessions. Completely independent of CAO, uses only tmux + Python.
license: MIT
allowed-tools: [Read, Write, Edit, Bash, Task]
---

# Agent Manager

Employee agent orchestration system for managing AI agents in tmux sessions. A simple, dependency-light alternative to CAO.

## Quick Start

```bash
# Project-local install path varies by tool. If `.agent/skills/` doesn't exist, try `.claude/skills/`.
# List all agents
python3 .agent/skills/agent-manager/scripts/main.py list
python3 .claude/skills/agent-manager/scripts/main.py list

# (use the same path you chose above for the remaining commands)
# Start dev agent
python3 .agent/skills/agent-manager/scripts/main.py start dev

# Monitor output (live)
python3 .agent/skills/agent-manager/scripts/main.py monitor dev --follow

# Assign task
python3 .agent/skills/agent-manager/scripts/main.py assign dev <<EOF
Fix the login bug in the auth module
EOF

# Stop agent
python3 .agent/skills/agent-manager/scripts/main.py stop dev
```

## Core Concepts

### Agent Configuration

Agents are defined in `agents/EMP_*.md` files with YAML frontmatter:

```yaml
---
name: dev
description: Dev Agent (project-agnostic)
working_directory: ${REPO_ROOT}
launcher: ${REPO_ROOT}/projects/claude-code-switch/ccc
launcher_args:
  - cp
  - --dangerously-skip-permissions
skills:
  - review-pr
  - bsc-contract-development
---

# DEV AGENT

## Role and Identity
You are the Dev Agent...
```

**Fields:**
- `name`: Agent identifier (dev, qa)
- `description`: Agent description
- `enabled`: Whether agent can be started (default: `true`, set `false` to disable)
- `working_directory`: Default working directory (supports `${REPO_ROOT}`)
- `launcher`: Full path OR provider name
- `launcher_args`: Arguments for launcher
- `skills`: Array of skill names from `.agent/skills/` (optional, injected at start)
- `schedules`: Array of scheduled jobs (optional, see Scheduling section)
- `tmux`: Optional tmux layout metadata (layout + target pane)

### Tmux Sessions

Each agent runs in a dedicated tmux session (`agent-{name}`):

- **Easy monitoring**: `tmux capture-pane -t agent-dev`
- **Direct interaction**: `tmux attach -t agent-dev`
- **Clean separation**: No process pollution

### Optional: Tmux Layouts

You can auto-create a tmux layout and launch the agent in a specific pane:

```yaml
tmux:
  layout:
    split: h
    panes:
      - {}
      - split: v
        panes:
          - {}
          - {}
  target_pane: "1.1"
```

Notes:
- `split`: `h` (left/right) or `v` (top/bottom). `horizontal`/`vertical` also work.
- `target_pane`: dot-separated path of `0`/`1` indexes into the layout tree.
  `0` = left/top, `1` = right/bottom. `"1.1"` means right -> bottom.
- If `tmux.layout` is set, `tmux.target_pane` is required.

### Launcher Types

**Full path**: Local Claude Code launcher
```yaml
launcher: ${REPO_ROOT}/projects/claude-code-switch/ccc
launcher_args: ["cp", "--dangerously-skip-permissions"]
```

**Provider name**: CAO provider (optional integration)
```yaml
launcher: droid
launcher_args: []
```

**Provider name**: OpenAI Codex CLI
```yaml
launcher: codex
launcher_args:
  - --model=gpt-5.2
```

Note: For scheduled jobs, `agent-manager` will best-effort auto-dismiss Codex's first-run/upgrade model selection prompt to keep cron runs non-interactive.

## Commands

### `list` - List All Agents

Show all configured agents and their status.

```bash
python3 scripts/main.py list              # All agents
python3 scripts/main.py list --running    # Only running
```

Output:
```
📋 Agents:

✅ Running dev (session: agent-dev)
   Description: Dev Agent (project-agnostic)
   Working Dir: /home/user/repo
   Skills: review-pr, bsc-contract-development

⭕ Stopped qa
   Description: QA Agent in a multi-agent system
   Working Dir: /home/user/repo/projects/CloudBank-feat-invite-code

⛔ Disabled old-dev
   Description: Legacy Dev Agent (deprecated)
   Working Dir: /home/user/repo
```

### `start` - Start an Agent

Start an agent in a tmux session.

```bash
python3 scripts/main.py start dev                      # Use default working_dir
python3 scripts/main.py start dev --working-dir /path   # Override working dir
```

- Rejects if already running (one agent, one terminal)
- Rejects if agent is disabled (`enabled: false` in config)
- Loads skills and injects as system prompt
- Session named `agent-{name}`

### `stop` - Stop a Running Agent

Stop (kill) an agent's tmux session.

```bash
python3 scripts/main.py stop dev
```

### `monitor` - Monitor Agent Output

View agent output from tmux session.

```bash
python3 scripts/main.py monitor dev              # Last 100 lines
python3 scripts/main.py monitor dev -n 500       # Last 500 lines
python3 scripts/main.py monitor dev --follow     # Live monitoring (Ctrl+C to stop)
```

### `send` - Send Message to Agent

Send a message/command to a running agent.

```bash
python3 scripts/main.py send dev "Please run tests"
# ⚠️ Don't forget: tmux send-keys -t agent-dev Enter
```

### `assign` - Assign Task to Agent

Assign a task to an agent (starts if not running).

```bash
# From stdin
python3 scripts/main.py assign dev <<EOF
🎯 Task: Fix the login bug

1. Reproduce the issue
2. Identify root cause
3. Implement fix
4. Add tests
EOF

# From file
python3 scripts/main.py assign dev --task-file task.md
```

> **⚠️ Important**: After assigning a task, send an ENTER key to trigger execution:
> ```bash
> tmux send-keys -t agent-dev Enter
> ```

## Disabling Agents

Agents can be temporarily disabled to prevent them from being started (useful for maintenance, testing, or decommissioning).

### Disable an Agent

Add `enabled: false` to the agent's YAML frontmatter:

```yaml
---
name: dev
description: Dev Agent (project-agnostic)
enabled: false  # ← Agent cannot be started
working_directory: ${REPO_ROOT}
launcher: ${REPO_ROOT}/projects/claude-code-switch/ccc
---
```

### Behavior

**When an agent is disabled:**
- ⛔ `list` command shows "Disabled" status
- ⚠️ `start` command is rejected with error message
- `schedule sync` skips all schedules for the disabled agent
- Running sessions are NOT automatically stopped (manual stop required)

**To re-enable:** Set `enabled: true` or remove the field (defaults to `true`)

### Use Cases

- **Maintenance**: Temporarily disable an agent while updating its configuration
- **Testing**: Prevent a scheduled agent from running during testing
- **Decommissioning**: Mark an agent as obsolete before removing its file

## Scheduling

Agents can be configured to run automatically on a schedule using cron expressions.

### Schedule Configuration

Add a `schedules` array to the agent's YAML frontmatter:

```yaml
---
name: dev
description: Dev Agent
working_directory: ${REPO_ROOT}
launcher: ${REPO_ROOT}/projects/claude-code-switch/ccc
launcher_args:
  - cp
  - --dangerously-skip-permissions
skills:
  - bsc-contract-development

schedules:
  - name: daily-standup
    cron: "0 9 * * 1-5"
    task: |
      Review GitHub issues, prioritize today's work
    max_runtime: 30m

  - name: code-review
    cron: "0 14 * * 1-5"
    task_file: ${REPO_ROOT}/tasks/templates/code-review.md
    max_runtime: 2h

  - name: weekly-report
    cron: "0 17 * * 5"
    task: |
      Generate weekly progress report and commit to docs/
    max_runtime: 1h
    enabled: true
---
```

**Schedule Fields:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | ✓ | Unique job identifier |
| `cron` | string | ✓ | Cron expression (e.g., `0 9 * * 1-5`) |
| `task` | string | △ | Inline task description |
| `task_file` | string | △ | Path to task file (supports `${REPO_ROOT}`) |
| `max_runtime` | string | | Maximum runtime (e.g., `30m`, `2h`, `8h`) |
| `enabled` | bool | | Default: `true` |

> **Note**: Either `task` or `task_file` must be provided.

### Schedule Commands

#### `schedule list` - List All Scheduled Jobs

```bash
python3 scripts/main.py schedule list
```

Output:
```
📅 Scheduled Jobs:

dev (EMP_0001):
  ✓ daily-standup         0 9 * * 1-5          (30m)
  ✓ code-review           0 14 * * 1-5         (2h)
  ✓ weekly-report         0 17 * * 5           (1h)

qa (EMP_0002):
  ✓ nightly-tests         0 2 * * *            (4h)
```

#### `schedule sync` - Sync Schedules to Crontab

Synchronize all agent schedules to the system crontab.

```bash
# Preview changes (dry run)
python3 scripts/main.py schedule sync --dry-run

# Apply changes
python3 scripts/main.py schedule sync
```

This generates crontab entries like:
```cron
# === agent-manager schedules (auto-generated) ===
# dev (EMP_0001)
# daily-standup
0 9 * * 1-5 cd /path/to/repo && python3 .agent/skills/agent-manager/scripts/main.py schedule run dev --job daily-standup >> /tmp/agent-emp-0001-daily-standup.log 2>&1
# === end agent-manager schedules ===
```

#### `schedule run` - Run a Scheduled Job Manually

Manually trigger a scheduled job (useful for testing).

```bash
python3 scripts/main.py schedule run dev --job daily-standup

# Override timeout
python3 scripts/main.py schedule run dev --job daily-standup --timeout 1h
```

## Skills Integration

Agents can reference skills from `.agent/skills/`:

```yaml
skills:
  - review-pr
  - bsc-contract-development
  - cao
```

When the agent starts, skill contents are injected as system prompt:

```
## Available Skills

### review-pr
Code review skill for GitHub PRs and local changes...

### bsc-contract-development
Comprehensive BSC smart contract development expertise...
```

**Available Skills:**
- `bsc-contract-development` - BSC smart contract development
- `cao` - CLI Agent Orchestrator
- `collab-pr-fix-loop` - QA→Dev→QA PR iteration
- `review-pr` - Code review for PRs
- `skill-creator` - Creating new skills

## Architecture

```
.agent/skills/agent-manager/
├── SKILL.md                    # This file
├── scripts/
│   ├── main.py                 # CLI entry point
│   ├── agent_config.py         # Agent file parser
│   ├── tmux_helper.py          # Tmux wrapper
│   └── schedule_helper.py      # Crontab management
├── providers/
│   └── __init__.py             # CLI provider configs
└── references/
    └── task_templates.md       # Optional task templates
```

### Design Principles

1. **Zero CAO Dependency**: Only tmux + Python required
2. **Provider Pattern Inspiration**: Learn from CAO but implement simply
3. **Tmux-Native**: Each agent in its own tmux session
4. **YAML Frontmatter**: Leverage existing agent file format
5. **Environment Variables**: Handle `${REPO_ROOT}` expansion
6. **One Agent, One Terminal**: Reject duplicate starts

## Comparison with CAO

| Feature | CAO | Agent Manager |
|---------|-----|--------------|
| Dependencies | CAO server, uvx, requests | tmux, Python only |
| Complexity | High (HTTP API, providers) | Low (direct tmux) |
| Session Mgmt | CAO server | Native tmux |
| Monitoring | HTTP API calls | Native tmux |
| Extensibility | Provider system | Direct script editing |
| Installation | CAO server setup | No server needed |
| Use Case | Complex workflows | Simple agent management |

## Error Handling

- **tmux not installed**: Clear error with install command
- **Agent not found**: Lists available agents
- **Already running**: Prompts to stop first
- **Not running**: Prompts to start first

## Advanced Usage

### Direct Tmux Interaction

```bash
# Attach to agent session (interactive)
tmux attach -t agent-dev

# Detach from session: Ctrl+b, then d

# Capture output manually
tmux capture-pane -p -t agent-dev -S -100

# List all agent sessions
tmux ls | grep ^agent-
```

### Workflow Example

```bash
# Morning: Start agents
python3 scripts/main.py start dev
python3 scripts/main.py start qa

# Assign task to dev
python3 scripts/main.py assign dev <<EOF
Implement the user profile feature:
1. Profile update API
2. Profile view component
3. Integration tests
EOF
# ⚠️ Don't forget: tmux send-keys -t agent-dev Enter

# Monitor progress
python3 scripts/main.py monitor dev --follow

# Send clarification if needed
python3 scripts/main.py send dev "Please add validation for email format"

# After dev completes, assign to QA
python3 scripts/main.py assign qa <<EOF
Review the user profile feature:
- Security check
- Edge cases
- Test coverage
EOF

# Evening: Stop agents
python3 scripts/main.py stop dev
python3 scripts/main.py stop qa
```
