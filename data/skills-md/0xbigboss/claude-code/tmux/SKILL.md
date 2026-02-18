---
name: tmux
description: Patterns for running long-lived processes in tmux. Use when starting dev servers, watchers, tilt, or any process expected to outlive the conversation.
---

# tmux Process Management

## Session Reuse Rules

These are **hard requirements**, not suggestions:

- **MUST** check `tmux has-session` before ever calling `tmux new-session`
- **MUST** derive session name from `git rev-parse --show-toplevel`, never hardcode
- **MUST** add windows to an existing project session, never create a parallel session
- **MUST** use `send-keys` to run commands, never pass inline commands to `new-session`
- **NEVER** create a new session if one already exists for the current project

One project = one tmux session. Multiple processes = multiple windows within that session.

## Interactive Shell Requirement

**Use send-keys pattern for reliable shell initialization.** Creating a session spawns an interactive shell automatically. Use `send-keys` to run commands within that shell, ensuring PATH, direnv, and other initialization runs properly.

```bash
# WRONG - inline command bypasses shell init, breaks PATH/direnv
tmux new-session -d -s "$SESSION" -n main 'tilt up'

# CORRECT - check for session, then use send-keys in interactive shell
if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux new-session -d -s "$SESSION" -n main
fi
tmux send-keys -t "$SESSION:main" 'tilt up' Enter
```

## Session Naming Convention

Always derive session name from the project:

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)
```

For multiple processes in one project, use windows not separate sessions:
- Session: `myapp`
- Windows: `server`, `tests`, `logs`

## Starting Processes

### Single Process

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux new-session -d -s "$SESSION" -n main
  tmux send-keys -t "$SESSION:main" '<command>' Enter
else
  echo "Session $SESSION already exists"
fi
```

### Adding a Window to Existing Session

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

# Add a new window if it doesn't exist
if ! tmux list-windows -t "$SESSION" -F '#{window_name}' | grep -q "^server$"; then
  tmux new-window -t "$SESSION" -n server
  tmux send-keys -t "$SESSION:server" 'npm run dev' Enter
else
  echo "Window 'server' already exists"
fi
```

### Multiple Processes (Windows)

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

# Create session if needed, then add windows
if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux new-session -d -s "$SESSION" -n server
  tmux send-keys -t "$SESSION:server" 'npm run dev' Enter
fi

# Add more windows (idempotent)
for win in tests logs; do
  if ! tmux list-windows -t "$SESSION" -F '#{window_name}' | grep -q "^${win}$"; then
    tmux new-window -t "$SESSION" -n "$win"
  fi
done
tmux send-keys -t "$SESSION:tests" 'npm run test:watch' Enter
tmux send-keys -t "$SESSION:logs" 'tail -f logs/app.log' Enter
```

## Monitoring Output

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

# Last 50 lines from first window
tmux capture-pane -p -t "$SESSION" -S -50

# From specific window
tmux capture-pane -p -t "$SESSION:server" -S -50

# Check for errors
tmux capture-pane -p -t "$SESSION" -S -100 | rg -i "error|fail|exception"

# Check for ready indicators
tmux capture-pane -p -t "$SESSION:server" -S -50 | rg -i "listening|ready|started"
```

## Lifecycle Management

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

# List all sessions (see what exists)
tmux ls

# List windows in current session
tmux list-windows -t "$SESSION"

# Kill only this project's session
tmux kill-session -t "$SESSION"

# Kill specific window
tmux kill-window -t "$SESSION:tests"

# Send keys to a window (e.g., Ctrl+C to stop)
tmux send-keys -t "$SESSION:server" C-c
```

## Isolation Rules

- **Never** use `tmux kill-server`
- **Never** kill sessions not matching current project
- **Always** derive session name from git root or pwd
- **Always** verify session name before kill operations
- Other Claude Code instances may have their own sessions running

## When to Use tmux

| Scenario | Use tmux? |
|----------|-----------|
| `tilt up` | Yes, always |
| Dev server (`npm run dev`, `rails s`) | Yes |
| File watcher (`npm run watch`) | Yes |
| Test watcher (`npm run test:watch`) | Yes |
| Database server | Yes |
| One-shot build (`npm run build`) | No |
| Quick command (<10s) | No |
| Need stdout directly in conversation | No |

## Checking Process Status

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

# Check session exists
tmux has-session -t "$SESSION" 2>/dev/null && echo "session exists" || echo "no session"

# List windows and their status
tmux list-windows -t "$SESSION" -F '#{window_name}: #{pane_current_command}'

# Check if specific window exists
tmux list-windows -t "$SESSION" -F '#{window_name}' | grep -q "^server$" && echo "server window exists"
```

## Restarting a Process

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

# Send Ctrl+C then restart command
tmux send-keys -t "$SESSION:server" C-c
sleep 1
tmux send-keys -t "$SESSION:server" 'npm run dev' Enter
```

## Common Patterns

### Start dev server if not running

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

if ! tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux new-session -d -s "$SESSION" -n server
  tmux send-keys -t "$SESSION:server" 'npm run dev' Enter
  echo "Started dev server in tmux session: $SESSION"
elif ! tmux list-windows -t "$SESSION" -F '#{window_name}' | grep -q "^server$"; then
  tmux new-window -t "$SESSION" -n server
  tmux send-keys -t "$SESSION:server" 'npm run dev' Enter
  echo "Added server window to session: $SESSION"
else
  echo "Server already running in session: $SESSION"
fi
```

### Wait for server ready

```bash
SESSION=$(basename $(git rev-parse --show-toplevel 2>/dev/null) || basename $PWD)

# Poll for ready message
for i in {1..30}; do
  if tmux capture-pane -p -t "$SESSION:server" -S -20 | rg -q "listening|ready"; then
    echo "Server ready"
    break
  fi
  sleep 1
done
```
