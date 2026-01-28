---
name: flyctl
description: "Deploy and manage apps on Fly.io using flyctl CLI. Triggers on: fly deploy, fly.io, flyctl, deploy to fly. Handles launch, deploy, scale, secrets, volumes, databases."
---

# Fly.io Deployment (flyctl)

Deploy applications to Fly.io's global edge infrastructure.

## Quick Reference

| Task | Command |
|------|---------|
| New app | `fly launch` |
| Deploy | `fly deploy` |
| Status | `fly status` |
| Logs | `fly logs` |
| SSH | `fly ssh console` |
| Open | `fly apps open` |

## Core Workflows

### 1. New App Deployment

```bash
cd /path/to/project
fly launch              # Interactive setup
fly launch --now -y     # Accept defaults, deploy immediately
fly launch --no-deploy  # Configure only, deploy later
```

Creates: `fly.toml` (config), `Dockerfile` (if needed)

### 2. Subsequent Deploys

```bash
fly deploy                    # Standard deploy
fly deploy --strategy rolling # Rolling update (default)
fly deploy --local-only       # Build locally instead of remote
```

### 3. Secrets Management

```bash
fly secrets set KEY=value           # Set secret
fly secrets set K1=v1 K2=v2        # Multiple
fly secrets list                    # List (values hidden)
fly secrets unset KEY               # Remove
cat .env | fly secrets import       # Import from file
```

### 4. Scaling

```bash
fly scale show                      # Current config
fly scale vm shared-cpu-1x          # Change VM size
fly scale memory 512                # Set memory (MB)
fly scale count 3                   # Set instance count
fly scale count web=2 worker=1      # Per process group
```

VM sizes: `shared-cpu-1x`, `shared-cpu-2x`, `performance-1x`, `performance-2x`

### 5. Volumes (Persistent Storage)

```bash
fly volumes create mydata --size 10 --region ord  # Create 10GB
fly volumes list                                   # List volumes
fly volumes extend <id> --size 20                  # Resize
```

Mount in fly.toml:
```toml
[mounts]
source = "mydata"
destination = "/data"
```

### 6. Databases

**Managed Postgres (recommended):**
```bash
fly mpg create                      # Create managed postgres
fly mpg list                        # List clusters
```

**Unmanaged Postgres:**
```bash
fly postgres create                 # Create cluster
fly postgres attach <pg-app>        # Attach to app (sets DATABASE_URL)
fly postgres connect <pg-app>       # Connect via psql
```

**Redis (Upstash):**
```bash
fly redis create                    # Create instance
```

### 7. Monitoring

```bash
fly status                # App status
fly logs                  # Tail logs
fly logs -i <machine-id>  # Specific machine
fly checks list           # Health checks
fly dashboard             # Open web UI
```

### 8. SSH & Console

```bash
fly ssh console           # Interactive shell
fly ssh console -C "cmd"  # Run command
fly sftp shell            # SFTP access
```

## fly.toml Essentials

```toml
app = "my-app"
primary_region = "ord"

[env]
APP_ENV = "production"

[http_service]
internal_port = 8080
force_https = true
auto_stop_machines = "stop"
auto_start_machines = true
min_machines_running = 1

[[vm]]
memory = "512mb"
cpu_kind = "shared"
cpus = 1
```

## Framework-Specific

For Laravel apps: Read `reference/laravel.md`
For Dockerfile apps: Read `reference/dockerfile.md`

## Troubleshooting

```bash
fly doctor              # Diagnose issues
fly releases            # List releases
fly releases show <v>   # Release details
fly machine list        # List machines
fly machine restart <id> # Restart specific machine
```

## Common Flags

| Flag | Description |
|------|-------------|
| `-a <app>` | Specify app name |
| `-c <path>` | Config file path |
| `-r <region>` | Target region |
| `--yes` | Skip confirmations |
| `--verbose` | Verbose output |
