---
name: inbox
description: 'Agent Mail inbox monitoring. Check pending messages, HELP_REQUESTs, and recent completions. Triggers: "inbox", "check mail", "any messages", "show inbox", "pending messages", "who needs help".'
dependencies: []
---

# Inbox Skill

> **Quick Ref:** Monitor Agent Mail from any session. View pending messages, help requests, completions.

**YOU MUST EXECUTE THIS WORKFLOW. Do not just describe it.**

Monitor Agent Mail messages for coordination across agents.

**Requires:** MCP Agent Mail tools OR HTTP endpoint at localhost:8765.

## Invocation

```bash
/inbox              # Show current inbox state
/inbox --watch      # Continuous polling mode
```

## Execution Steps

Given `/inbox [--watch]`:

### Step 1: Check Agent Mail Availability

```bash
# Check if Agent Mail MCP tools are available
# Look for tools starting with mcp__mcp-agent-mail__

# Alternatively, check HTTP endpoint
curl -s http://localhost:8765/health 2>/dev/null && echo "Agent Mail HTTP available" || echo "Agent Mail not running"
```

### Step 2: Determine Agent Identity

```bash
# Check environment for agent identity
if [ -n "$OLYMPUS_DEMIGOD_ID" ]; then
    AGENT_NAME="$OLYMPUS_DEMIGOD_ID"
elif [ -n "$AGENT_NAME" ]; then
    AGENT_NAME="$AGENT_NAME"
else
    # Default to asking or using hostname
    AGENT_NAME="${USER:-unknown}-$(hostname -s 2>/dev/null || echo local)"
fi

# Get project key (current repo path)
PROJECT_KEY=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
echo "Agent: $AGENT_NAME"
echo "Project: $PROJECT_KEY"
```

### Step 3: Fetch Inbox (MCP Method)

**Use MCP tool if available:**

```
Tool: mcp__mcp-agent-mail__fetch_inbox
Parameters:
  project_key: "<project-key>"
  agent_name: "<agent-name>"
```

**Parse results into categories:**
- **Pending:** Messages without acknowledgement
- **HELP_REQUEST:** Messages with subject containing "HELP_REQUEST"
- **Completions:** Messages with subject "OFFERING_READY" or "DONE"

### Step 4: Search for HELP_REQUESTs Needing Response

**Search for unresolved help requests:**

```
Tool: mcp__mcp-agent-mail__search_messages
Parameters:
  project_key: "<project-key>"
  query: "HELP_REQUEST"
```

**Filter to those without HELP_RESPONSE in same thread.**

### Step 5: Get Recent Completions

**Search for done messages:**

```
Tool: mcp__mcp-agent-mail__search_messages
Parameters:
  project_key: "<project-key>"
  query: "OFFERING_READY OR DONE OR COMPLETED"
```

### Step 6: Summarize Threads (Optional)

For active threads with multiple messages:

```
Tool: mcp__mcp-agent-mail__summarize_thread
Parameters:
  project_key: "<project-key>"
  thread_id: "<thread-id>"
```

### Step 7: Display Results

**Format output as:**

```markdown
# Agent Mail Inbox

**Agent:** <agent-name>
**Project:** <project-key>
**Checked:** <timestamp>

## Pending Messages (<count>)

| From | Subject | Thread | Age |
|------|---------|--------|-----|
| ... | ... | ... | ... |

## HELP_REQUESTs Needing Response (<count>)

| From | Issue | Problem | Waiting |
|------|-------|---------|---------|
| demigod-gt-123 | gt-123 | STUCK - Can't find auth module | 15m |
| ... | ... | ... | ... |

## Recent Completions (<count>)

| Agent | Issue | Status | Completed |
|-------|-------|--------|-----------|
| demigod-gt-124 | gt-124 | DONE | 2m ago |
| ... | ... | ... | ... |

## Actions Needed

- [ ] Respond to HELP_REQUEST from demigod-gt-123 (waiting 15m)
- [ ] Acknowledge completion of gt-124
```

## Watch Mode

When `--watch` flag is provided:

### Step W1: Enter Polling Loop

```bash
POLL_INTERVAL=30  # seconds

while true; do
    clear
    echo "=== Agent Mail Inbox (Watch Mode) ==="
    echo "Press Ctrl+C to exit"
    echo ""

    # Execute Steps 3-7 above

    # Show last update time
    echo ""
    echo "Last updated: $(date)"
    echo "Next refresh in ${POLL_INTERVAL}s"

    sleep $POLL_INTERVAL
done
```

### Step W2: Alert on New Messages

When new messages arrive since last poll:

```bash
# Compare message counts
if [ "$NEW_COUNT" -gt "$PREV_COUNT" ]; then
    echo "*** NEW MESSAGES ($((NEW_COUNT - PREV_COUNT))) ***"
    # Optionally use terminal bell
    echo -e "\a"
fi

# Highlight urgent HELP_REQUESTs
if [ "$HELP_WAITING_MINS" -gt 5 ]; then
    echo "*** URGENT: HELP_REQUEST waiting ${HELP_WAITING_MINS}m ***"
fi
```

### Step W3: Show Message Summaries

For each new message, display summary:

```markdown
---
**NEW:** From demigod-gt-125 | Thread: gt-125 | 10s ago
Subject: PROGRESS
> Step 4 in progress. Files touched: src/auth.py, tests/test_auth.py
---
```

## MCP Tool Reference

| Tool | Purpose |
|------|---------|
| `fetch_inbox` | Get messages for agent |
| `search_messages` | Find messages by query |
| `summarize_thread` | Summarize a thread |
| `acknowledge_message` | Mark message as read |

## HTTP Fallback

If MCP tools unavailable but HTTP server running:

```bash
# Fetch inbox via HTTP
curl -s "http://localhost:8765/mcp/" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "fetch_inbox",
    "params": {
      "project_key": "<project-key>",
      "agent_name": "<agent-name>"
    }
  }'

# Search messages
curl -s "http://localhost:8765/mcp/" \
  -H "Content-Type: application/json" \
  -d '{
    "method": "search_messages",
    "params": {
      "project_key": "<project-key>",
      "query": "HELP_REQUEST"
    }
  }'
```

## Key Rules

- **Check regularly** - Agents may be waiting for help
- **Prioritize HELP_REQUESTs** - Blocked agents waste resources
- **Acknowledge completions** - Closes the coordination loop
- **Use watch mode** - For active orchestration sessions

## Integration Points

| System | Integration |
|--------|-------------|
| **Beads** | Thread IDs often match beads issue IDs (e.g., gt-123) |
| **Demigod** | Demigods send progress, help requests, completions |
| **Mayor** | Mayor monitors inbox for coordination decisions |
| **Chiron** | Chiron watches for HELP_REQUESTs to answer |

## Example Session

```bash
# Quick check
/inbox

# Output:
# Agent Mail Inbox
# Agent: boden
# Project: /Users/fullerbt/gt/olympus
#
# Pending Messages (2)
# - PROGRESS from demigod-ol-527 (5m ago)
# - HELP_REQUEST from demigod-ol-528 (2m ago)
#
# HELP_REQUESTs Needing Response (1)
# - demigod-ol-528: STUCK - Can't find skill template format
#
# Actions Needed:
# - [ ] Respond to HELP_REQUEST from demigod-ol-528

# Start monitoring
/inbox --watch
```

## Without Agent Mail

If Agent Mail is not available:

```markdown
Agent Mail not available.

To enable:
1. Start MCP Agent Mail server:
   Start your Agent Mail MCP server (implementation-specific). See `docs/agent-mail.md`.

2. Add to ~/.claude/mcp_servers.json:
   {
     "mcp-agent-mail": {
       "type": "http",
       "url": "http://127.0.0.1:8765/mcp/"
     }
   }

3. Restart Claude Code session
```

---

## References

- **Agent Mail Protocol:** See `skills/shared/agent-mail-protocol.md` for message format specifications
- **Parser (Go):** `cli/internal/agentmail/` - shared parser for all message types
