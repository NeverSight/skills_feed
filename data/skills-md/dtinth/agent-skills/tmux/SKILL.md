---
name: tmux
description: Use this skill to run background processes or long running processes using tmux.
---

`tmux` lets you run commands in the background and check on them later. When you run a normal bash command, you have to wait for it to finish. With tmux, you can start a command, let it run in the background, and check its output whenever you want.

Key Terms:

- Session: A container that holds your tabs. Like a browser window.
- Tab: A place where one command runs. Like a browser tab. We call this a "window" in tmux.

# Step 1: Create or Use a Session

Always do this first:

```bash
# Create a new session
tmux new-session -d -s mysession
```

- Use the project name (e.g. working directory basename) as the session name.
- If it fails with "duplicate session", it means the session already exists. It may be created by a prior session. You can use it, but check its state before continuing.

```bash
# See what sessions exist
tmux ls

# Delete a session when done
tmux kill-session -t mysession
```

# Step 2: Create Tabs (Windows)

```bash
# Create a tab called "mytab" in session "mysession"
tmux new-window -t mysession -n mytab
```

- Always give your tab a name. Don't use numbers.
- Always specify the session name in the command line as there may be multiple tmux sessions active.

```bash
# See what tabs exist
tmux list-windows -t mysession

# Delete a tab
tmux kill-window -t mysession:mytab
```

# Step 3: Run a Command in a Tab

```bash
# Run "npm start" in the "server" tab
tmux send-keys -t mysession:server 'npm start' Enter
```

- Always end with `Enter` to actually run the command.

```bash
# Stop a running command: Send Ctrl+C
tmux send-keys -t mysession:server C-c
```

Common stop signals:
- `C-c` = Ctrl+C (interrupt)
- `C-d` = Ctrl+D (end input)

# Step 4: Check What Happened

```bash
# See what's on screen now
tmux capture-pane -t mysession:server -p
```

If you don't see the output you want yet, sleep and run again. If you don't know how long it will take, start at 15 seconds, doubling the sleep duration each time, but never sleep more than 4 minutes (240 seconds).
