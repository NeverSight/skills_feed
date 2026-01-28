---
name: tmux
description: Control interactive CLIs (python, gdb, etc.) via tmux sessions - send keystrokes and scrape output
---

# tmux Skill

Use tmux to control interactive terminal applications by sending keystrokes and capturing output.

## When to Use

- Running interactive REPLs (python, node, psql)
- Debugging with gdb/lldb
- Any CLI that requires TTY interaction
- Remote execution where you need to observe output

## Core Pattern

```bash
# Create session
tmux new-session -d -s "$SESSION" -x 120 -y 40

# Send commands
tmux send-keys -t "$SESSION" "python3" Enter

# Capture output
tmux capture-pane -t "$SESSION" -p

# Wait for prompt (poll)
for i in {1..30}; do
  output=$(tmux capture-pane -t "$SESSION" -p)
  if echo "$output" | grep -q ">>>"; then break; fi
  sleep 0.5
done

# Cleanup
tmux kill-session -t "$SESSION"
```

## Remote Execution (Codespaces/SSH)

For mise-installed tools, wrap in zsh:

```bash
# Non-interactive (won't hang)
ssh host 'zsh -c "source ~/.zshrc; tmux new-session -d -s mysession; tmux send-keys -t mysession python Enter"'

# Interactive (for tmux attach) - needs TTY
ssh host -t 'zsh -ilc "tmux attach -t mysession"'
```

**Critical**: Use `zsh -c "source ~/.zshrc; ..."` not `zsh -lc` to avoid hangs.

## User Notification

After starting a session, ALWAYS print:
```
To monitor: tmux attach -t $SESSION
To capture: tmux capture-pane -t $SESSION -p
```

## Tips

- Use `-x 120 -y 40` for consistent pane size
- Poll with `capture-pane -p` rather than `wait-for`
- Send literal text with `-l` flag to avoid shell expansion
- Control keys: `C-c` (interrupt), `C-d` (EOF), `Escape`
- For Python REPL: set `PYTHON_BASIC_REPL=1` to avoid fancy console interference

## Helper Scripts

### [wait-for-text.sh](scripts/wait-for-text.sh)

Poll tmux pane for a text pattern with timeout:

```bash
scripts/wait-for-text.sh -t session:0.0 -p '^>>>' -T 15
```

### [find-sessions.sh](scripts/find-sessions.sh)

List tmux sessions, optionally filtered:

```bash
scripts/find-sessions.sh -q claude  # filter by name
scripts/find-sessions.sh --all      # all sessions
```
