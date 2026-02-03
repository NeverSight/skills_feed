---
name: pm2-server-control
description: >-
  Start and stop a server with pm2 using `pm2 start ./my-server --name <name> --no-autorestart`,
  plus common supporting commands for status, logs, restart, and cleanup.
metadata:
  owner: local
  version: 1
---

# pm2-server-control

Use this skill when the task requires starting or stopping a local server via PM2,
specifically using `pm2 start ./my-server --name <name> --no-autorestart`, and when
you need to inspect status or logs, restart, or clean up the process.

## Required command pattern

Always start the server with:

```bash
pm2 start ./my-server --name <name> --no-autorestart
```

Replace `<name>` with a concise, unique name (e.g., `api-dev`, `web-preview`).

## Useful PM2 commands

Start:

```bash
pm2 start ./my-server --name <name> --no-autorestart
```

Stop:

```bash
pm2 stop <name>
```

Restart (if a fresh start is needed):

```bash
pm2 restart <name>
```

Delete (remove from PM2 list):

```bash
pm2 delete <name>
```

List all processes:

```bash
pm2 list
```

Show detailed info:

```bash
pm2 show <name>
```

Logs (stream):

```bash
pm2 logs <name>
```

Logs (last N lines):

```bash
pm2 logs <name> --lines 200
```

Flush logs (if they get noisy):

```bash
pm2 flush <name>
```

Save current process list (optional, if asked):

```bash
pm2 save
```

Resurrect saved processes (only if asked):

```bash
pm2 resurrect
```

## Safety and cleanup

- Prefer `pm2 stop <name>` for normal shutdowns.
- Use `pm2 delete <name>` when the process is no longer needed.
- Keep process names stable across start/stop cycles.
