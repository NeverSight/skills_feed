---
name: pm2
description: >-
  Process management with PM2 — start, stop, restart, monitor long-running
  processes. Use when: keeping services alive, auto-restart on crash, managing
  daemon processes, ecosystem configs, log management, startup scripts, process
  monitoring. Triggers: pm2, process manager, keep alive, daemon, auto-restart,
  ecosystem config, process monitoring.
---

# PM2 — Process Manager

PM2 keeps processes alive, restarts them on crash, and provides monitoring/logging.
Use for long-running services, persistent agents, background workers.

> **Not for detached terminals** — use [holdpty](https://github.com/marcfargas/holdpty) when you need PTY output, attach/view, or interactive sessions.
> **Not for ephemeral tasks** — use `pi -p > file &` for quick fire-and-forget agent runs.

## Quick Reference

### Start a process

```bash
# Simple
pm2 start server.js --name myapp

# With interpreter
pm2 start script.py --interpreter python3 --name worker

# With arguments (use -- to separate pm2 args from script args)
pm2 start app.js --name api -- --port 3000 --env production

# From ecosystem file
pm2 start ecosystem.config.cjs
```

### Manage processes

```bash
pm2 list                    # List all processes (table)
pm2 jlist                   # List as JSON (for scripting)
pm2 info <name|id>          # Detailed process info
pm2 restart <name|id|all>   # Restart
pm2 stop <name|id|all>      # Stop (keeps in list)
pm2 delete <name|id|all>    # Stop + remove from list
pm2 restart <name> --update-env  # Restart with refreshed env vars
```

### Logs

```bash
pm2 logs                     # Tail all logs
pm2 logs <name> --lines 50   # Tail specific process, last 50 lines
pm2 flush                    # Clear all log files
```

Log files location: `~/.pm2/logs/<name>-out.log` and `<name>-error.log`.

### Monitoring

```bash
pm2 monit          # Real-time TUI: CPU, memory, logs
pm2 dash           # Dashboard with monitoring + logs
```

## Ecosystem Config

For reproducible multi-process setups, use an `ecosystem.config.cjs` file:

```javascript
// ecosystem.config.cjs
module.exports = {
  apps: [
    {
      name: "api",
      script: "dist/server.js",
      instances: 2,                // cluster mode
      exec_mode: "cluster",
      env: {
        NODE_ENV: "production",
        PORT: 3000,
      },
      max_memory_restart: "500M",
      log_date_format: "YYYY-MM-DD HH:mm:ss",
    },
    {
      name: "worker",
      script: "dist/worker.js",
      autorestart: true,
      max_restarts: 10,
      restart_delay: 5000,
      exp_backoff_restart_delay: 100,  // exponential backoff
      watch: false,
    },
  ],
};
```

```bash
pm2 start ecosystem.config.cjs           # Start all apps
pm2 start ecosystem.config.cjs --only api  # Start specific app
pm2 restart ecosystem.config.cjs          # Restart all
pm2 delete ecosystem.config.cjs           # Stop + remove all
```

### Useful ecosystem options

| Option | Type | Description |
|--------|------|-------------|
| `script` | string | Script to run (required) |
| `interpreter` | string | Override interpreter (default: `node`) |
| `args` | string or string[] | Script arguments |
| `cwd` | string | Working directory |
| `instances` | number | Number of instances (cluster mode) |
| `exec_mode` | string | `"fork"` (default) or `"cluster"` |
| `autorestart` | boolean | Auto-restart on exit (default: `true`) |
| `max_restarts` | number | Max consecutive restarts before stopping |
| `restart_delay` | number | Delay between restarts (ms) |
| `exp_backoff_restart_delay` | number | Exponential backoff base (ms) |
| `max_memory_restart` | string | Restart if memory exceeds (e.g. `"500M"`) |
| `cron_restart` | string | Cron-based restart schedule |
| `watch` | boolean or string[] | Watch for file changes |
| `ignore_watch` | string[] | Paths to ignore when watching |
| `env` | object | Environment variables |
| `log_date_format` | string | Timestamp format for logs |
| `error_file` | string | Custom stderr log path |
| `out_file` | string | Custom stdout log path |
| `merge_logs` | boolean | Merge cluster instance logs |
| `stop_exit_codes` | number[] | Exit codes that skip auto-restart |

## Persistence

```bash
pm2 save               # Save current process list
pm2 resurrect           # Restore saved process list
pm2 startup             # Generate OS startup script (auto-start on boot)
pm2 unstartup           # Remove startup script
```

After `pm2 startup`, run the command it outputs (may need admin/sudo).
Then `pm2 save` to snapshot current processes — they'll auto-start on reboot.

## Windows Gotchas

### `.cmd` wrapper resolution

PM2 tries to run `.cmd` files as Node.js scripts. **Never start a `.cmd` shim directly** with PM2.

```bash
# ❌ WRONG — resolves to pi.cmd, crashes
pm2 start pi -- -p "prompt"

# ✅ CORRECT — point to the actual .js entry point
pm2 start /path/to/cli.js --interpreter node -- -p "prompt"
```

For npm-installed CLIs, find the real script:

```bash
# Find where the .cmd shim points
cat "$(which pi)" | head -5
# → Look for the .js path, then use that with --interpreter node
```

In ecosystem configs, always use the resolved `.js` path:

```javascript
module.exports = {
  apps: [{
    name: "my-agent",
    // Resolve the actual cli.js, not the .cmd wrapper
    script: "C:\\path\\to\\node_modules\\package\\dist\\cli.js",
    interpreter: "node",
    args: ["--mode", "json"],
  }],
};
```

### Log paths

PM2 stores logs at `~/.pm2/logs/`. On Windows this is typically `C:\Users\<user>\.pm2\logs\`.

### Daemon

PM2 daemon runs as a background Node.js process. `pm2 kill` stops the daemon and all managed processes. `pm2 ping` checks if the daemon is running.

## Agent Patterns

### Launch a pi agent as a persistent service

First, find the actual `cli.js` path (see Windows Gotchas above):

```bash
# Find pi's real entry point
cat "$(which pi)" | head -5
# e.g. → /path/to/node_modules/@mariozechner/pi-coding-agent/dist/cli.js
```

```javascript
// ecosystem.config.cjs
module.exports = {
  apps: [{
    name: "my-agent",
    // Use the resolved cli.js path — NOT the .cmd wrapper
    script: "/path/to/node_modules/@mariozechner/pi-coding-agent/dist/cli.js",
    interpreter: "node",
    args: ["--mode", "json", "--cwd", "/path/to/project"],
    autorestart: true,
    max_restarts: 10,
    restart_delay: 5000,
  }],
};
```

> **Note**: `pi -p` to non-TTY only outputs final text. Use `--mode json` for full event streaming to PM2 logs.

### Check process health from an agent

```bash
# Structured output for parsing
pm2 jlist | node -e "
  const d = JSON.parse(require('fs').readFileSync('/dev/stdin','utf8'));
  d.forEach(p => console.log(p.name, p.pm2_env.status, 'restarts:', p.pm2_env.restart_time));
"
```

### Rotate logs

```bash
pm2 install pm2-logrotate        # Install log rotation module
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 5
```

## When NOT to Use PM2

- **Detached terminal sessions** → use [holdpty](https://github.com/marcfargas/holdpty) (PTY output, attach/view)
- **Ephemeral agent runs** → use `pi -p > file &` (fire-and-forget with output capture)
- **Containers** → the container runtime manages lifecycle; PM2 inside Docker is usually redundant
- **Systemd environments** → use systemd service units natively on Linux
