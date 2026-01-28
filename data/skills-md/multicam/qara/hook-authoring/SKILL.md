---
name: hook-authoring
context: fork
description: |
  Claude Code hook creation and configuration. PAI event-driven automation.

  USE WHEN: "create hook", "hook system", "modify hooks", "add hook"
---

## Workflow Routing (SYSTEM PROMPT)

**When user requests creating a new hook:**
Examples: "create a hook for X", "add a hook", "make a SessionStart hook"
-> **READ:** ${PAI_DIR}/skills/hook-authoring/workflows/create-hook.md
-> **EXECUTE:** Follow hook creation workflow

**When user needs to debug hooks:**
Examples: "hook not working", "debug hooks", "hook troubleshooting"
-> **READ:** ${PAI_DIR}/skills/hook-authoring/workflows/debug-hooks.md
-> **EXECUTE:** Run debugging checklist

---

## Claude Code Hook Events

### SessionStart
**When:** New Claude Code session begins
**Use Cases:** Load context, initialize state, capture metadata

### Stop
**When:** Claude completes a response (not user)
**Use Cases:** Extract completion info, update tab titles, capture work

### UserPromptSubmit
**When:** User submits a prompt
**Use Cases:** Pre-processing, context injection, tab updates

### SubagentStop
**When:** A subagent (Task) completes
**Use Cases:** Agent tracking, result capture, coordination

### Notification
**When:** Notifications are triggered
**Use Cases:** Alerts, external integrations

---

## Hook Configuration

**Location:** `${PAI_DIR}/.claude/settings.json` or `~/.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": {},
        "hooks": [
          {
            "type": "command",
            "command": "${PAI_DIR}/hooks/my-hook.ts"
          }
        ]
      }
    ]
  }
}
```

---

## Hook Input/Output

### Input (stdin JSON)
```typescript
interface HookInput {
  session_id: string;
  transcript_path: string;
  // Event-specific fields...
}
```

### Output (stdout)
- **Continue:** `{ "continue": true }`
- **Block:** `{ "continue": false, "reason": "..." }`
- **Inject content:** `{ "result": "<system-reminder>...</system-reminder>" }`
- **Add context (CC 2.1.9+):** `{ "decision": "continue", "additionalContext": "..." }`

### Session ID Tracking (CC 2.1.9+)

Hooks receive `session_id` in input JSON. For persistent storage:

```typescript
// Use session_id from hook input
const sessionFile = `${PAI_DIR}/state/sessions/${input.session_id}.json`;

// Or use ${CLAUDE_SESSION_ID} substitution in settings.json:
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command", 
        "command": "${PAI_DIR}/hooks/init-session.ts --session ${CLAUDE_SESSION_ID}"
      }]
    }]
  }
}
```

---

## PAI Active Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `session-start.ts` | SessionStart | Load CORE skill, set tab |
| `stop-hook.ts` | Stop | Extract COMPLETED, update tab |
| `subagent-stop-hook.ts` | SubagentStop | Track agent completion |
| `capture-all-events.ts` | All | JSONL logging |

---

## Hook Best Practices

1. **Fail gracefully** - Hooks should never block Claude
2. **Timeout protection** - Use timeouts for external calls
3. **Async by default** - Don't block the main process
4. **TypeScript preferred** - Use Bun for execution
5. **Log errors** - Don't fail silently

---

## Quick Hook Template

```typescript
#!/usr/bin/env bun
// ${PAI_DIR}/hooks/my-hook.ts

import { readFileSync } from 'fs';

const input = JSON.parse(readFileSync('/dev/stdin', 'utf-8'));

// Your logic here

// Output (choose one):
console.log(JSON.stringify({ continue: true }));
// console.log(JSON.stringify({ result: "<system-reminder>...</system-reminder>" }));
```

Make executable: `chmod +x my-hook.ts`

---

## Related

- See `agent-observability` skill for event analysis
- See `capture-all-events.ts` for JSONL logging pattern
