---
name: agent-lens
aliases: [agent-lens]
context: fork
model: haiku
description: |
  Agent Lens: Real-time observability dashboard for multi-agent Claude Code sessions.

  Visualize agent interactions, tool usage, and session flows through a modern dual-pane interface. Track parent-child event relationships with hierarchical timeline visualization, HITL approvals, and comprehensive metrics.

  **Key Features:**
  - 👁️ Dual-pane layout (process timeline + results/metrics)
  - 🌳 Span hierarchy visualization with parent-child relationships
  - 🔴 Real-time event streaming via WebSocket
  - 🤖 HITL interface with timeout indicators and three-action pattern
  - 📊 Token usage, cost tracking, and performance metrics
  - 🎨 OLED-optimized dark theme (2026 standards)
  - 💾 Filesystem-based (no database required)

  **Version 2.0**
---

# Agent Lens

Real-time observability dashboard for multi-agent Claude Code sessions.

## Features

### Dual-Pane Interface
- **Process Timeline** - Hierarchical view of events with parent-child relationships
- **Results & Metrics** - Session statistics, event details, and performance data
- **Resizable panes** - Drag to adjust layout (25%-60% width)

### Event Visualization
- **Hierarchical timeline** - Nested events show tool call relationships
- **Collapse/expand** - Show/hide child events
- **Event icons** - Visual indicators for tool types
- **Session cards** - Track individual sessions and lifecycle

### Metrics & Monitoring
- **Token tracking** - Estimate usage per session
- **Cost calculation** - Track AI model costs (2026 pricing)
- **Tool usage breakdown** - Most frequently used tools
- **Performance metrics** - Latency, duration, error rates
- **Context tracking** - Monitor context window usage (CC 2.1.6)

### HITL (Human-in-the-Loop)
- **Approval interface** - Review and approve/reject requests
- **Timeout indicators** - Visual countdown for time-sensitive actions
- **Three-action pattern** - Approve, Edit, or Reject
- **Browser notifications** - Alert on urgent requests

### Event Types Captured
- **SessionStart** - New Claude Code session begins
- **UserPromptSubmit** - User sends a message
- **PreToolUse** - Before tool execution
- **PostToolUse** - After tool completion
- **Stop** - Main agent task completes
- **SubagentStop** - Subagent task completes
- **SessionEnd** - Session ends

## Quick Start

### Start the Dashboard

```bash
# Terminal 1: Start server
cd ~/.claude/skills/agent-lens/apps/server
bun run dev

# Terminal 2: Start client
cd ~/.claude/skills/agent-lens/apps/client
bun run dev

# Or use the project convenience script:
cd /path/to/qara
bun run start-obs
```

Open browser: **http://localhost:5173**

### Using with Claude Code

Once the dashboard is running:

1. Open Claude Code
2. Use any tool (Read, Write, Bash, etc.)
3. Launch subagents with Task tool
4. Watch events appear in real-time on the dashboard

## Data Storage

Events are stored in JSONL (JSON Lines) format:

```
~/.claude/history/raw-outputs/YYYY-MM/YYYY-MM-DD_all-events.jsonl
```

Each line is a complete JSON object:

```jsonl
{"source_app":"qara","session_id":"abc123","hook_event_type":"PreToolUse","payload":{...},"timestamp":1234567890,"timestamp_aedt":"2025-01-28 14:30:00 AEDT"}
```

## Configuration

### Environment Variables

**PAI_DIR** - Path to PAI directory (defaults to `~/.claude/`)

```bash
export PAI_DIR="/Users/yourname/.claude"
```

### Session Tracking (CC 2.1.9+)

Agent Lens automatically tracks sessions using Claude Code's native session IDs:

- **Current session:** `${CLAUDE_SESSION_ID}`
- **Events file:** `~/.claude/history/raw-outputs/YYYY-MM/YYYY-MM-DD_all-events.jsonl`
- **Session state:** `~/.claude/state/agent-lens/sessions/${CLAUDE_SESSION_ID}.json`

Each event includes the `session_id` field for correlation across the observability dashboard.

### Hooks Configuration

Hooks should be configured in `~/.claude/settings.json`. The `capture-all-events` hook is required for Agent Lens to function.

## Troubleshooting

### No events appearing

1. Check PAI_DIR: `echo $PAI_DIR`
2. Verify hooks exist: `ls ~/.claude/hooks/capture-all-events.ts`
3. Check hook is executable: `ls -l ~/.claude/hooks/capture-all-events.ts`
4. Verify today's events file: `ls ~/.claude/history/raw-outputs/$(date +%Y-%m)/`

### Server won't start

1. Check Bun: `bun --version`
2. Install dependencies: `cd apps/server && bun install`
3. Check port: `lsof -i :4000`

### Client won't connect

1. Ensure server is running first
2. Check browser console for WebSocket errors
3. Verify firewall not blocking localhost:4000

## Architecture

```
Claude Code (with hooks)
    ↓
capture-all-events.ts hook → JSONL files
    ↓
file-ingest.ts (Bun server) → In-memory stream
    ↓
Vue 3 Client → Real-time dashboard
```

**Approach:** Filesystem-based event capture with in-memory streaming. No database required.

## Credits

Inspired by [@indydevdan](https://github.com/indydevdan)'s work on multi-agent observability for Claude Code.

Our implementation uses filesystem-based event capture and in-memory streaming instead of SQLite database persistence.
