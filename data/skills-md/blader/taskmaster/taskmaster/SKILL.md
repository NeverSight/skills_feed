---
name: taskmaster
description: |
  Stop hook that keeps the agent working until all plans and user requests are
  100% complete. Fires on every stop attempt until the agent emits an explicit
  parseable done signal in its final response. Provides deterministic machine
  detection for true completion.
author: blader
version: 2.1.0
---

# Taskmaster

A stop hook that prevents the agent from stopping prematurely. When the agent
is about to stop, this hook checks for a session-specific done token in the
transcript. If the token is missing, it blocks the stop and forces another
completion review cycle.

## How It Works

1. **Agent tries to stop** — the stop hook fires every time.
2. **Hook scans transcript** for a parseable token:
   `TASKMASTER_DONE::<session_id>`
3. **Token missing** — hook blocks stop and injects a checklist plus the exact
   token to emit when truly done.
4. **Token present** — hook allows stop and clears session counter state.

## Parseable Done Signal

When the work is genuinely complete, the agent must include this exact line
in its final response (on its own line):

```text
TASKMASTER_DONE::<session_id>
```

This gives external automation a deterministic completion marker to parse.

## Configuration

- `TASKMASTER_MAX` (default `0`): Max number of blocked stop attempts before
  allowing stop. `0` means infinite (keep firing).
- `TASKMASTER_DONE_PREFIX` (default `TASKMASTER_DONE`): Prefix used for the
  done token.

## Setup

The hook must be registered in `~/.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.claude/skills/taskmaster/hooks/check-completion.sh",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

## Disabling

To temporarily disable, remove or comment out the Stop hook in
`~/.claude/settings.json`.
