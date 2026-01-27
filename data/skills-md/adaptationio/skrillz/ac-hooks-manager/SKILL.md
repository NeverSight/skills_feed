---
name: ac-hooks-manager
description: Hook installation and management for autonomous coding. Use when setting up Stop hooks, managing pre/post tool hooks, or configuring autonomous continuation.
version: 1.0.0
layer: foundation
category: auto-claude-replication
triggers:
  - "install hooks"
  - "setup stop hook"
  - "configure hooks"
  - "hook status"
---

# AC Hooks Manager

Hook installation and management for enabling autonomous operation.

## Overview

Manages all Claude Code hooks for autonomous operation:
- **Stop Hook**: Enables autonomous continuation
- **PreToolUse Hook**: Security validation
- **PostToolUse Hook**: Result processing
- **SessionStart/End Hooks**: State management

## Quick Start

### Install Autonomous Hooks
```python
from scripts.hooks_manager import HooksManager

hooks = HooksManager(project_dir)
await hooks.install_autonomous_hooks()
# Installs Stop hook for autonomous continuation
```

### Check Hook Status
```python
status = await hooks.get_status()
print(f"Stop hook: {'installed' if status.stop_hook else 'missing'}")
```

## The Stop Hook (Core Innovation)

The Stop hook enables autonomous continuation by intercepting Claude Code's stop event:

```
Claude Code completes response
    │
    ▼ (Stop event fires)

Stop Hook Script
    ├─ Read transcript
    ├─ Check safety limits
    ├─ Call Opus analyzer
    └─ Return decision
    │
    ├─ CONTINUE: block stop, inject next task
    └─ COMPLETE: allow stop, terminate
```

### How It Works

1. **Claude Code finishes** a response
2. **Stop event fires** (hook receives JSON input)
3. **Hook script executes**:
   - Checks `stop_hook_active` (prevents infinite loops)
   - Checks iteration/cost limits
   - Calls Opus analyzer for decision
4. **Decision returned**:
   - `CONTINUE`: Exit code 2 + reason → Claude continues
   - `COMPLETE`: Exit code 0 → Claude stops

### Stop Hook Input

```json
{
  "session_id": "abc123",
  "transcript_path": "/path/to/conversation.jsonl",
  "cwd": "/current/working/directory",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": false
}
```

**Critical Field**: `stop_hook_active`
- `false`: First time hook firing (proceed with analysis)
- `true`: Hook already blocked once (allow stop to prevent doom loop)

### Stop Hook Output

**To Continue**:
```json
{
  "decision": "block",
  "reason": "Next task: implement the login endpoint"
}
```
Exit code: `2`

**To Stop**:
```json
{
  "decision": "approve"
}
```
Exit code: `0`

## Hook Configuration

### .claude/settings.json

```json
{
  "hooks": {
    "Stop": [{
      "matcher": {},
      "hooks": [{
        "type": "command",
        "command": ".claude/skills/ac-hooks-manager/scripts/autonomous-loop.sh"
      }],
      "timeout": 120
    }],
    "PreToolUse": [{
      "tools": ["Bash"],
      "hooks": [{
        "type": "command",
        "command": ".claude/skills/ac-security-sandbox/scripts/validate.sh"
      }]
    }],
    "PostToolUse": [{
      "tools": ["Write", "Edit"],
      "hooks": [{
        "type": "command",
        "command": "npx prettier --write \"$FILE\""
      }]
    }]
  }
}
```

## Hook Types

### 1. Stop Hook (Autonomous Continuation)

```python
await hooks.install_stop_hook(
    script_path=".claude/skills/ac-hooks-manager/scripts/autonomous-loop.sh",
    timeout=120
)
```

### 2. PreToolUse Hook (Security)

```python
await hooks.install_pre_tool_hook(
    tools=["Bash"],
    script_path=".claude/skills/ac-security-sandbox/scripts/validate.sh"
)
```

### 3. PostToolUse Hook (Formatting)

```python
await hooks.install_post_tool_hook(
    tools=["Write", "Edit"],
    command="npx prettier --write \"$FILE\""
)
```

### 4. Session Hooks

```python
await hooks.install_session_hooks(
    on_start=".claude/hooks/load-memory.sh",
    on_end=".claude/hooks/save-memory.sh"
)
```

## Operations

### 1. Install All Autonomous Hooks

```python
await hooks.install_autonomous_hooks()
# Installs:
#   - Stop hook (continuation)
#   - PreToolUse hook (security)
#   - Session hooks (memory)
```

### 2. Install Specific Hook

```python
await hooks.install_hook(
    event="Stop",
    config={
        "type": "command",
        "command": "path/to/script.sh"
    },
    timeout=120
)
```

### 3. Remove Hook

```python
await hooks.remove_hook(event="Stop")
```

### 4. Check Status

```python
status = await hooks.get_status()
# Returns:
#   stop_hook: bool
#   pre_tool_hooks: list
#   post_tool_hooks: list
#   session_hooks: dict
```

### 5. Validate Hooks

```python
errors = await hooks.validate()
if errors:
    for error in errors:
        print(f"Hook error: {error}")
```

## Autonomous Loop Script

### scripts/autonomous-loop.sh

```bash
#!/bin/bash

# Read input from stdin
INPUT=$(cat)

# Extract fields
STOP_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active')
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path')
CWD=$(echo "$INPUT" | jq -r '.cwd')

# Safety check: prevent doom loops
if [ "$STOP_ACTIVE" == "true" ]; then
    echo '{"decision": "approve"}'
    exit 0
fi

# Load state
STATE_FILE="$CWD/.claude/autonomous-state.json"
if [ -f "$STATE_FILE" ]; then
    ITERATION=$(jq -r '.iteration' "$STATE_FILE")
    COST=$(jq -r '.estimated_cost' "$STATE_FILE")
else
    ITERATION=0
    COST=0
fi

# Check limits
MAX_ITERATIONS=50
MAX_COST=20.00

if [ "$ITERATION" -ge "$MAX_ITERATIONS" ]; then
    echo '{"decision": "approve"}'
    exit 0
fi

if (( $(echo "$COST > $MAX_COST" | bc -l) )); then
    echo '{"decision": "approve"}'
    exit 0
fi

# Call Opus analyzer (see ac-opus-analyzer skill)
DECISION=$(python3 "$CWD/.claude/skills/ac-hooks-manager/scripts/analyze.py" \
    --transcript "$TRANSCRIPT" \
    --iteration "$ITERATION")

# Return decision
echo "$DECISION"
exit $(echo "$DECISION" | jq -r 'if .decision == "block" then 2 else 0 end')
```

## Safety Mechanisms

### 1. Doom Loop Prevention

```bash
if [ "$STOP_ACTIVE" == "true" ]; then
    exit 0  # Allow stop
fi
```

### 2. Iteration Limits

```bash
if [ "$ITERATION" -ge "$MAX_ITERATIONS" ]; then
    exit 0  # Allow stop
fi
```

### 3. Cost Limits

```bash
if (( $(echo "$COST > $MAX_COST" | bc -l) )); then
    exit 0  # Allow stop
fi
```

### 4. Failure Detection

```bash
FAILURES=$(jq -r '.consecutive_failures' "$STATE_FILE")
if [ "$FAILURES" -ge 3 ]; then
    exit 0  # Allow stop, escalate
fi
```

## Integration Points

- **ac-session-manager**: Triggers hooks
- **ac-security-sandbox**: PreToolUse validation
- **ac-opus-analyzer**: Decision making
- **ac-state-tracker**: State persistence
- **ac-config-manager**: Hook configuration

## References

- `references/HOOK-MECHANICS.md` - Detailed hook behavior
- `references/STOP-HOOK.md` - Stop hook deep dive
- `references/SAFETY.md` - Safety mechanisms

## Scripts

- `scripts/hooks_manager.py` - Core HooksManager
- `scripts/autonomous-loop.sh` - Stop hook handler
- `scripts/analyze.py` - Opus analyzer wrapper
- `scripts/hook_installer.py` - Hook installation
