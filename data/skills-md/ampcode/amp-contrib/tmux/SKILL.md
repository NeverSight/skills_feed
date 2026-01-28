---
name: tmux
description: Instructions for using tmux to spawn multiple processes, inspect them, and capture their output. Useful for running servers or long-running tasks in the background.
allowed-tools:
  - Bash
---

# Tmux Skill

This skill empowers you to manage multiple concurrent processes (like servers, watchers, or long builds) using `tmux` directly from the `Bash` tool.

Since you are likely already running inside a tmux session, you can spawn new windows or panes to handle these tasks without blocking your main communication channel.

## 1. Verify Environment & Check Status

First, verify you are running inside tmux:

```bash
echo $TMUX
```

If this returns empty, you are not running inside tmux and these commands will not work as expected.

Once verified, check your current windows:

```bash
tmux list-windows
```

## 2. Spawn a Background Process

To run a command (e.g., a dev server) in a way that persists and can be inspected:

1.  **Create a new detached window** with a specific name. This keeps it isolated and easy to reference.

    ```bash
    tmux new-window -n "server-log" -d
    ```

    _(Replace "server-log" with a relevant name for your task)_

2.  **Send the command** to that window.
    ```bash
    tmux send-keys -t "server-log" "npm start" C-m
    ```
    _(`C-m` simulates the Enter key)_

## 3. Inspect Output (Read Logs)

You can read the output of that pane at any time without switching your context.

**Get the current visible screen:**

```bash
tmux capture-pane -p -t "server-log"
```

**Get the entire history (scrollback):**

```bash
tmux capture-pane -p -S - -t "server-log"
```

_Use this if the output might have scrolled off the screen._

## 4. Interact with the Process

If you need to stop or restart the process:

**Send Ctrl+C (Interrupt):**

```bash
tmux send-keys -t "server-log" C-c
```

**Kill the window (Clean up):**

```bash
tmux kill-window -t "server-log"
```

## 5. Advanced: Chaining Commands

You can chain multiple tmux commands in a single invocation using `';'` (note the quotes to avoid interpretation by the shell). This is faster and cleaner than running multiple `tmux` commands.

Example: Create window and start process in one go:

```bash
tmux new-window -n "server-log" -d ';' send-keys -t "server-log" "npm start" C-m
```

## Summary of Pattern

1. `tmux new-window -n "ID" -d`
2. `tmux send-keys -t "ID" "CMD" C-m`
3. `tmux capture-pane -p -t "ID"`
