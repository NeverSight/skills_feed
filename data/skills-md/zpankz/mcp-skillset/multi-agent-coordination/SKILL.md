---
name: multi-agent-coordination
description: Automatically invoked when peer agents are detected in the same project. Establishes coordination protocols, file reservations, and message-based collaboration. Triggers on SessionStart when other agents exist in the project.
---

# Multi-Agent Coordination Protocol

You are operating in a **multi-agent environment**. Other agents are working on this project concurrently.

## Mandatory Coordination Behavior

### 1. Session Initialization (Do This First)

```yaml
sequence:
  1. register_agent:
      project_key: ${CWD}
      program: "claude-code"
      model: "claude-opus-4-5"
      # Name auto-generated (adjective+noun like "BlueLake")

  2. fetch_inbox:
      agent_name: ${YOUR_AGENT_NAME}
      include_bodies: true
      # Check for pending coordination messages

  3. Acknowledge any ack_required messages immediately
```

### 2. Before Editing Files

**Always reserve files before editing:**

```yaml
file_reservation_paths:
  project_key: ${CWD}
  agent_name: ${YOUR_AGENT_NAME}
  paths: ["path/to/file.py"]  # Or glob: "src/api/*.py"
  ttl_seconds: 3600
  exclusive: true
  reason: "Implementing feature X"
```

**If conflicts returned:**
- Check who holds the reservation
- Send a message requesting coordination
- Wait for response or reservation expiry

### 3. Communication Protocol

**Notify peers of significant changes:**

```yaml
send_message:
  to: ["PeerAgentName"]  # Or discovered via list_agents
  subject: "Working on: [component]"
  body_md: |
    ## What I'm doing
    - Modifying X
    - Adding Y

    ## Files affected
    - `src/foo.py`
    - `src/bar.py`

    ## Coordination needed?
    Let me know if this conflicts with your work.
  importance: "normal"
```

### 4. Periodic Inbox Polling

**Check inbox between major work units:**

```yaml
frequency: After each significant edit/commit
action: fetch_inbox → process messages → acknowledge
```

### 5. File Release on Completion

**Release reservations when done:**

```yaml
release_file_reservations:
  agent_name: ${YOUR_AGENT_NAME}
  # Omit paths to release all
```

## Quick Reference Commands

| Action | Tool |
|--------|------|
| Start session | `macro_start_session` |
| Check peers | `whois` + project agents resource |
| Reserve files | `file_reservation_paths` |
| Send update | `send_message` |
| Check inbox | `fetch_inbox` |
| Reply | `reply_message` |
| Release files | `release_file_reservations` |

## Conflict Resolution

1. **File conflict**: Message the holder, propose merge strategy
2. **Overlapping work**: Summarize thread, align on ownership
3. **Urgent coordination**: Use `importance: "urgent"` + `ack_required: true`

## Exit Protocol

Before ending session:
1. `release_file_reservations` (all)
2. `send_message` with session summary to active peers
3. Mark any pending inbox items as read
