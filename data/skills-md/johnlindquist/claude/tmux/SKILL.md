---
name: tmux
description: Manage tmux sessions for background processes. Use to run long-running commands, manage multiple terminals, and capture output from background processes.
---

# Tmux Session Manager

Run and manage background processes using tmux.

## Prerequisites

Install tmux:
```bash
brew install tmux
# or
apt install tmux
```

## CLI Reference

### Create Session
```bash
# Basic session
tmux new-session -d -s mysession

# With window name
tmux new-session -d -s mysession -n mywindow

# With working directory
tmux new-session -d -s mysession -c /path/to/dir

# With initial command
tmux new-session -d -s mysession "npm run dev"

# Combined
tmux new-session -d -s dev -n server -c /project "npm run dev"
```

### List Sessions
```bash
# List all sessions
tmux list-sessions

# Short format
tmux ls

# With format
tmux list-sessions -F "#{session_name}: #{session_windows} windows"
```

### Send Keys to Session
```bash
# Send command
tmux send-keys -t mysession "npm test" Enter

# Send to specific window
tmux send-keys -t mysession:mywindow "command" Enter

# Send without Enter
tmux send-keys -t mysession "partial command"

# Send special keys
tmux send-keys -t mysession C-c        # Ctrl+C
tmux send-keys -t mysession C-d        # Ctrl+D
tmux send-keys -t mysession Escape     # Escape
tmux send-keys -t mysession Up         # Arrow up
```

### Capture Output
```bash
# Capture visible pane
tmux capture-pane -t mysession -p

# Capture with history (last N lines)
tmux capture-pane -t mysession -p -S -100

# Capture all history
tmux capture-pane -t mysession -p -S -

# Save to file
tmux capture-pane -t mysession -p > output.txt
```

### Kill Session
```bash
# Kill specific session
tmux kill-session -t mysession

# Kill all sessions
tmux kill-server
```

### Attach to Session
```bash
# Attach
tmux attach -t mysession

# Attach or create
tmux new-session -A -s mysession
```

### Window Management
```bash
# New window
tmux new-window -t mysession -n windowname

# Select window
tmux select-window -t mysession:windowname

# Kill window
tmux kill-window -t mysession:windowname

# List windows
tmux list-windows -t mysession
```

### Pane Management
```bash
# Split horizontally
tmux split-window -t mysession -h

# Split vertically
tmux split-window -t mysession -v

# Select pane
tmux select-pane -t mysession:0.1

# Kill pane
tmux kill-pane -t mysession:0.1
```

## Workflow Patterns

### Run Dev Server in Background
```bash
# Start server
tmux new-session -d -s devserver -c /project "npm run dev"

# Check output
tmux capture-pane -t devserver -p -S -50

# Stop server
tmux send-keys -t devserver C-c
tmux kill-session -t devserver
```

### Run Tests with Output Capture
```bash
# Start tests
tmux new-session -d -s tests "npm test"

# Wait and capture output
sleep 30
tmux capture-pane -t tests -p -S - > test-output.txt

# Cleanup
tmux kill-session -t tests
```

### Multiple Services
```bash
# Create session with multiple windows
tmux new-session -d -s services -n frontend
tmux new-window -t services -n backend
tmux new-window -t services -n database

# Start each service
tmux send-keys -t services:frontend "npm run dev" Enter
tmux send-keys -t services:backend "go run main.go" Enter
tmux send-keys -t services:database "docker-compose up db" Enter

# Check all services
for win in frontend backend database; do
  echo "=== $win ==="
  tmux capture-pane -t services:$win -p -S -10
done
```

### Long-Running Process
```bash
# Start process
tmux new-session -d -s build "npm run build:production"

# Monitor progress
watch -n 5 "tmux capture-pane -t build -p -S -20"

# Or periodic check
while tmux has-session -t build 2>/dev/null; do
  sleep 10
  echo "Still running..."
done
echo "Build complete"
```

## Socket Mode (for Agents)

When running in agent context, use a dedicated socket:

```bash
SOCKET_PATH="/tmp/agent-tmux-$$"

# Create session with socket
tmux -S $SOCKET_PATH new-session -d -s agent "command"

# Send keys via socket
tmux -S $SOCKET_PATH send-keys -t agent "input" Enter

# Capture via socket
tmux -S $SOCKET_PATH capture-pane -t agent -p

# Cleanup
tmux -S $SOCKET_PATH kill-server
rm -f $SOCKET_PATH
```

## Best Practices

1. **Name sessions descriptively** - Easy to identify later
2. **Use `-d` for detached** - Don't block the terminal
3. **Capture output regularly** - Before killing sessions
4. **Set working directory** - Use `-c /path` for context
5. **Clean up sessions** - Kill when done
6. **Use sockets for isolation** - Prevent conflicts between agents
