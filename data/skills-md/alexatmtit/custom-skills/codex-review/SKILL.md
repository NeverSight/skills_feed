---
name: codex-review
description: Run Codex CLI /review via tmux to review uncommitted changes. Launches Codex in isolated tmux session, sends /review command, selects option 2, captures output. Use when you want a second opinion on uncommitted code changes.
---

# Codex Review via Tmux

## Overview

Launch OpenAI's Codex CLI in a tmux session and run the `/review` command to get a code review of uncommitted changes. The skill handles the full lifecycle: setup, command execution, waiting for completion (up to 60 minutes), capturing output, and cleanup.

## Prerequisites

Before running, verify:
- `tmux` is installed and available
- `codex` CLI is installed and available

## The Process

### Step 1: Setup Tmux Session

```bash
SOCKET="${TMPDIR:-/tmp}/codex-review-$$.sock"
SESSION="codex-review-$$"
tmux -S "$SOCKET" new-session -d -s "$SESSION"
```

### Step 2: Launch Codex and Send Commands

```bash
# Launch codex
tmux -S "$SOCKET" send-keys -t "$SESSION" "codex" Enter

# Wait for codex to initialize
sleep 5

# Type /review command
tmux -S "$SOCKET" send-keys -t "$SESSION" -l "/review"

# Press Enter to execute the /review command
tmux -S "$SOCKET" send-keys -t "$SESSION" Enter

# Wait for menu to appear
sleep 2

# Select option 2: Review uncommitted changes (no Enter needed)
tmux -S "$SOCKET" send-keys -t "$SESSION" -l "2"
```

### Step 3: Wait for Completion

Poll every 60 seconds for up to 60 minutes:

```bash
wait_for_completion() {
  local timeout=3600 interval=60 elapsed=0
  while [ $elapsed -lt $timeout ]; do
    output=$(tmux -S "$SOCKET" capture-pane -p -t "$SESSION" -S -100)

    # Check for completion (shell prompt returned)
    if echo "$output" | grep -qE '(❯|\$|>>>)\s*$'; then
      return 0
    fi

    sleep $interval
    elapsed=$((elapsed + interval))
  done
  return 1
}

wait_for_completion
```

### Step 4: Capture Output

```bash
# Capture full pane output (last 500 lines)
tmux -S "$SOCKET" capture-pane -p -t "$SESSION" -S -500
```

### Step 5: Cleanup

```bash
tmux -S "$SOCKET" kill-session -t "$SESSION"
rm -f "$SOCKET"
```

## To Monitor Manually

If you want to watch the session while it runs:

```bash
tmux -S "$SOCKET" attach -t "$SESSION"
```

Detach with `Ctrl+b d`.

## Success Criteria

- Codex review output is captured and displayed
- Tmux session is cleaned up
- No orphaned processes or sockets
