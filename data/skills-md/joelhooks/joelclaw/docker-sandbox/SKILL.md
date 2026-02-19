---
name: docker-sandbox
description: Create, manage, and execute agent tools (claude, codex) inside Docker sandboxes for isolated code execution. Use when running agent loops, spawning tool subprocesses, or any task requiring process isolation. Triggers on "sandbox", "isolated execution", "docker sandbox", "safe agent execution", or when working on agent loop infrastructure.
---

# Docker Sandbox for Agent Tools

Isolated execution of `claude`, `codex`, and other agent tools using Docker Desktop's `docker sandbox` (v0.11.0+). Uses existing Claude Max and ChatGPT Pro subscriptions — no API key billing.

**ADR**: [ADR-0023](https://joelclaw.com/adrs/0023-docker-sandbox-for-agent-loops)

## Prerequisites

- Docker Desktop running (OrbStack works)
- `docker sandbox version` returns ≥0.11.0
- Auth secrets stored in `agent-secrets`:
  - `claude_setup_token` — from `claude setup-token` (1-year token, Max subscription)
  - `codex_auth_json` — contents of `~/.codex/auth.json` (ChatGPT Pro subscription)

## Quick Reference

```bash
# Create a sandbox
docker sandbox create --name my-sandbox claude /path/to/project

# Run a command in it
docker sandbox exec -e "CLAUDE_CODE_OAUTH_TOKEN=..." -w /path/to/project my-sandbox \
  claude -p "implement the feature" --output-format text --dangerously-skip-permissions

# List sandboxes
docker sandbox ls

# Remove
docker sandbox rm my-sandbox
```

## Auth Setup (One-Time)

### Claude (Max subscription)

Run interactively on the host (needs browser for OAuth):

```bash
claude setup-token
```

This opens a browser, completes OAuth, and prints a token like `sk-ant-oat01-...`. Valid for **1 year**.

Store it:
```bash
secrets add claude_setup_token --value "sk-ant-oat01-..."
```

Use in sandbox:
```bash
TOKEN=$(secrets lease claude_setup_token --ttl 1h --raw)
docker sandbox exec -e "CLAUDE_CODE_OAUTH_TOKEN=$TOKEN" my-sandbox claude auth status
# → loggedIn: true, authMethod: oauth_token
```

### Codex (ChatGPT Pro subscription)

Authenticate codex locally (needs browser):
```bash
codex  # Select "Sign in with ChatGPT", complete OAuth
```

The auth file at `~/.codex/auth.json` is **portable** (not host-tied). Store it:
```bash
secrets add codex_auth_json --value "$(cat ~/.codex/auth.json)"
```

Inject into sandbox:
```bash
AUTH=$(secrets lease codex_auth_json --ttl 1h --raw)
docker sandbox exec my-sandbox bash -c "mkdir -p ~/.codex && cat > ~/.codex/auth.json << 'EOF'
${AUTH}
EOF"
```

### Token Refresh

| Token | Lifetime | Refresh |
|-------|----------|---------|
| `claude_setup_token` | 1 year | Run `claude setup-token` again, update secret |
| `codex_auth_json` | Until subscription change | Re-run `codex` login if auth fails, update secret |

## Agent Loop Integration

### Pre-warm Pattern

Create sandbox(es) at loop start, reuse for all stories, destroy at loop end.

```
PLANNER (loop start)
  ├── docker sandbox create --name loop-{loopId}-claude claude {workDir}
  ├── docker sandbox create --name loop-{loopId}-codex codex {workDir}  # if needed
  └── inject auth into both

IMPLEMENTOR / TEST-WRITER / REVIEWER (per story)
  └── docker sandbox exec -w {workDir} -e CLAUDE_CODE_OAUTH_TOKEN=... loop-{loopId}-{tool} \
        {tool command}
      # ~90ms overhead, workspace changes visible on host immediately

COMPLETE / CANCEL (loop end)
  ├── docker sandbox rm loop-{loopId}-claude
  └── docker sandbox rm loop-{loopId}-codex
```

### Timing

| Operation | Time |
|-----------|------|
| Create (cached image) | ~14s |
| Exec (warm sandbox) | ~90ms |
| Stop | ~11s |
| Remove | ~150ms |

**Net overhead per loop**: ~14s create + ~90ms × N stories = negligible for loops running 5-10 stories at 5-15min each.

### Workspace Mount

The workspace is **bidirectional** — same path on host and in sandbox:
- File created in sandbox → visible on host at same path
- File created on host → visible in sandbox
- Git operations work normally (host sees sandbox changes, sandbox sees host commits)

### Sandbox Templates

| Template | Tools Included |
|----------|---------------|
| `claude` | claude 2.1.42, git, node 20, npm |
| `codex` | codex 0.101.0, git, node 20, npm |

Neither includes `bun`. If bun is needed, use host-mode fallback or install it post-create.

### Env Vars

Pass via `docker sandbox exec -e`:

```bash
docker sandbox exec \
  -e "CLAUDE_CODE_OAUTH_TOKEN=$TOKEN" \
  -e "NODE_ENV=development" \
  -w /path/to/project \
  my-sandbox \
  claude -p "prompt" --output-format text --dangerously-skip-permissions
```

### Network Control

Sandboxes have network access by default. Restrict with proxy rules:

```bash
# Allow only API endpoints
docker sandbox network proxy my-sandbox --policy deny
docker sandbox network proxy my-sandbox --allow-host api.anthropic.com
docker sandbox network proxy my-sandbox --allow-host api.openai.com
```

### Fallback to Host Mode

If Docker is unavailable:

```bash
# Check availability
docker info >/dev/null 2>&1 || echo "Docker not available"

# Force host mode
export AGENT_LOOP_HOST=1
```

## Saving Custom Templates

If you install additional tools in a sandbox, save it as a template:

```bash
# Install tools
docker sandbox exec my-sandbox bash -c 'npm i -g @anthropic-ai/claude-code @openai/codex'

# Save as template
docker sandbox save my-sandbox my-agent-template:v1

# Use the template for future sandboxes
docker sandbox create --name fast-sandbox -t my-agent-template:v1 claude /path/to/project
```

## Implementation in utils.ts

### New Functions (ADR-0023)

```typescript
// Create sandbox for a loop
async function createLoopSandbox(
  loopId: string,
  tool: "claude" | "codex",
  workDir: string
): Promise<string>  // returns sandbox name

// Execute command in existing sandbox
async function execInSandbox(
  sandboxName: string,
  command: string[],
  opts: { env?: Record<string, string>; workDir?: string; timeout?: number }
): Promise<{ exitCode: number; output: string }>

// Destroy loop sandbox(es)
async function destroyLoopSandbox(loopId: string): Promise<void>
```

### Replacing spawnTool()

Current `spawnTool()` in implement.ts checks `AGENT_LOOP_HOST` and `isDockerAvailable()`. Update it to:

1. Check if sandbox `loop-{loopId}-{tool}` exists (created by planner)
2. If yes → `execInSandbox()` with auth env vars
3. If no → fall back to `spawnToolHost()` (current host-mode behavior)

## Troubleshooting

### "Not logged in" in sandbox
Auth not injected. Check:
```bash
docker sandbox exec my-sandbox bash -c 'claude auth status'
docker sandbox exec my-sandbox bash -c 'cat ~/.codex/auth.json | head -3'
```

### Sandbox creation slow
First pull downloads ~500MB image. Subsequent creates use cached image (~14s). Use `docker sandbox save` to create a pre-configured template.

### File not visible between host and sandbox
Only the workspace path is mounted. Files outside the workspace directory are not shared.

### "docker sandbox: command not found"
Docker Desktop must be running. Check version: `docker sandbox version`. Requires Docker Desktop 4.40+ with sandbox extension.
