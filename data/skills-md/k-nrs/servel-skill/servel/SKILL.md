---
name: servel
description: Self-hosted deployment platform via Docker Swarm. Deploys applications, manages 45+ infrastructure types (databases, queues, caches, platforms), handles secrets, domains, backups, and server operations. Triggers on deploy, infrastructure, postgres, redis, supabase, backup, restore, logs, secrets, SSL, domains, dev mode, CI/CD, alerts, traefik, routing, or server management.
---

# Servel

Deploy applications and infrastructure to Docker Swarm with Vercel-like simplicity. Auto-detects project type, provisions SSL, zero-downtime rolling updates.

## Decision Tree

```
Task → What are you trying to do?
│
├─ Deploy app → servel deploy
│   ├─ Need database? → servel add postgres --name db && servel deploy --link-infra db
│   ├─ Preview/PR? → servel deploy --preview --ttl 24h
│   └─ Multi-env? → servel deploy --env production
│
├─ Add infrastructure → servel add <type> --name <name>
│   ├─ Bundle? → servel add redis,postgres --prefix app
│   ├─ High-availability? → servel add postgres --name db --ha
│   └─ Link to app? → servel link myapp --infra db
│
├─ Debug/inspect → servel logs <name> -f | servel exec <name> sh
│   └─ Infra? → Use @ prefix: servel logs @mydb -f | servel exec @mydb --service rails sh
│
├─ Dev mode → servel dev
│   └─ Team sync? → servel dev --team
│
├─ Manage server → servel server status | servel ssh <server>
│
├─ Routing issues → servel traefik status | servel verify dns <domain>
│
└─ Backup/restore → servel infra backup <name> | servel infra restore <name> <file>
```

## Service Addressing (Symbol Prefixes)

Most commands that target a service (exec, logs, inspect, stats, restart, stop, start, scale, env, remove) support symbol prefixes:

| Prefix | Type | Resolves to | Example |
|--------|------|-------------|---------|
| `name` | Deployment | `servel-name-*` | `servel logs myapp -f` |
| `@name` | Infrastructure | `servel-infra-name-*` | `servel logs @mydb -f` |
| `~name` | System | `servel-system-name` | `servel logs ~traefik` |

For multi-service infrastructure (chatwoot, supabase, etc.), use `--service`:
```bash
servel exec @chatwoot --service rails sh
servel logs @supabase --service postgres -f
servel restart @chatwoot --service sidekiq
```

## Quick Reference

### Deploy

```bash
servel deploy                         # Auto-detect & deploy
servel deploy --preview --ttl 24h     # Preview with cleanup
servel deploy --link-infra db,redis   # Link infrastructure
servel deploy --dry-run               # Show plan only
servel deploy --no-registry           # Skip registry (single-node)
servel deploy --env staging           # Multi-environment
servel deploy --verbose               # Full build output
servel deploy --rebuild               # Force rebuild, skip cache
servel deploy --memory 1g --cpu 0.5   # Resource limits
servel ps                             # List deployments
servel ps --all-servers               # List across all servers
servel ps --tree                      # Tree view with dependencies
servel logs <name> -f                 # Follow logs
servel watch <name>                   # Watch deploy progress (TUI)
servel rm <name>                      # Remove
servel rollback <name>                # Rollback version
servel scale <name> 3                 # Scale replicas
servel restart <name>                 # Restart deployment
servel stop <name>                    # Stop deployment
servel start <name>                   # Start stopped deployment
servel rename <old> <new>             # Rename deployment
servel exec <name> sh                 # Shell into container
servel exec <name> -- cmd args        # Run command in container
servel inspect <name>                 # Detailed deployment info
servel history <name>                 # Deployment history
servel versions <name>                # Available versions
```

**Detection priority:** `servel.yaml` → `docker-compose.yml` → `Dockerfile` → preset → Nixpacks

**Smart mode (default):** Detects what changed → config-only (~8s), static-only (~10s), or full build.

**Key flags:**
- `--name, -n` — Deployment name
- `--domain, -d` — Domain for routing
- `--preview` — Preview environment
- `--ttl` — Preview lifetime (1h, 6h, 1d, 7d, 2w)
- `--link-infra` — Link infrastructure (comma-separated)
- `--no-registry` — Skip registry push
- `--rebuild` — Force rebuild
- `--no-smart` — Disable smart detection
- `--verbose` — Show full build output
- `--env` — Target environment
- `--build-on <node>` — Build on specific node
- `--local-build` — Build locally, push to registry

### Deploy Aliases

Define deployment presets in `servel.yaml`:
```yaml
deploy:
  aliases:
    preview:
      ttl: "0"
      domain: "{branch}.preview.myapp.com"
      no_index: true
    quick:
      fast: true
      local: true
    staging:
      env: staging
      domain: "staging.myapp.com"
```
Usage: `servel deploy preview`, `servel deploy quick`
- If a directory exists with that name → deploys directory
- Otherwise → applies alias settings

### Infrastructure (45+ types)

| Category | Types |
|----------|-------|
| Database | postgres, mysql, mongodb, clickhouse, redis, libsql + HA variants (postgres-ha, mysql-ha, mongodb-ha, redis-ha) |
| Queue | rabbitmq |
| Search | meilisearch, typesense |
| Platform | supabase, supabase-ha, chatwoot, typebot, convex, affine, forgejo, clawdbot, maily, surfsense |
| Analytics | plausible, umami, openreplay |
| Monitoring | prometheus, grafana, loki, promtail, uptimekuma, gatus, peekaping |
| Realtime | livekit, livekit-egress, hocuspocus, y-sweet |
| Storage | minio |
| Email | posteio |
| CI | woodpecker, woodpecker-agent |
| Blockchain | bitcoin, ipfs, lnd |

```bash
servel add postgres --name db         # Create
servel add redis,postgres --prefix app # Bundle multiple
servel add postgres --name db --ha    # High-availability
servel add supabase --name supa       # Full platform stack
servel add chatwoot --var Domain=chat.example.com  # Auto-init on first deploy
servel infra status                   # Health check all
servel infra vars db                  # View env vars
servel logs @db -f                    # Follow infra logs (@ prefix)
servel logs @chatwoot --service rails -f  # Multi-service infra logs
servel infra backup db                # Backup
servel infra restore db backup.sql.gz # Restore
servel infra rotate db                # Rotate credentials
servel infra restart db --force       # Force restart
servel infra start db                 # Start
servel infra stop db                  # Stop
servel infra rename old new           # Rename
servel infra rm db                    # Remove
servel link myapp --infra db          # Link → injects DATABASE_URL
servel unlink myapp --infra db        # Unlink
servel deps myapp                     # Show dependencies
servel connect db                     # Quick connect to infra
```

**Linking injects:** DATABASE_URL, REDIS_URL, MONGODB_URI, etc. based on infrastructure type.

**Lifecycle hooks:** Some templates auto-run setup commands on first deploy (e.g., Chatwoot runs `db:chatwoot_prepare`).

**Node pinning:**
- `--node hostname` — By hostname
- `--alias db-node` — By alias
- `--label storage=ssd` — By node label

### Server Management

```bash
servel ssh <server>                   # SSH into server
servel server status                  # Cluster health (CPU, memory, disk)
servel server add <name> user@host    # Add server
servel server list                    # List servers
servel server use <name>              # Switch default server
servel server remove <name>           # Remove server
servel server provision               # Automated setup
servel server domain set example.com  # Set primary domain
servel server keys add <name> --key-file pubkey.pub # Add deploy key
servel node ls                        # List swarm nodes
servel node add worker user@host      # Add node to cluster
servel node remove <name>             # Remove node
servel node promote <name>            # Promote to manager
servel node health <name>             # Check node health
servel node specs <name>              # Node specifications
servel df                             # Disk usage
servel df --volumes                   # Volume usage by category
servel df --nodes                     # Per-node usage
servel doctor                         # Diagnose issues
servel cleanup                        # Remove expired environments
servel cleanup --force                # No confirmation
servel prune                          # Remove dangling images/containers
servel prune --all                    # Remove unused images/networks/cache
servel prune --all --volumes          # ⚠️ DATA LOSS: removes unused volumes
```

### Secrets

```bash
servel secrets set API_KEY            # Set (prompted input)
servel secrets set API_KEY "value"    # Set with value
servel secrets list                   # List keys
servel secrets get API_KEY            # Get value
servel secrets rm API_KEY             # Remove
servel secrets rotate API_KEY         # Rotate
servel secrets backup                 # Backup all secrets
servel secrets scan                   # Scan for exposed secrets
servel deploy --migrate-secrets       # Auto-detect *_KEY, *_SECRET, *_PASSWORD
```

### Domains & Routing

```bash
servel domains add myapp app.com      # Add domain (auto-SSL)
servel domains ls                     # List all domains
servel domains rm myapp app.com       # Remove domain
servel domains redirect old.com new.com # Create redirect
servel domains remove-redirect old.com # Remove redirect
servel domains list-redirects         # List redirects
servel routes <name>                  # Show deployment routes
```

### Traefik (Routing Layer)

```bash
servel traefik status                 # Router status
servel traefik logs                   # Traefik logs
servel traefik routes <name>          # Detailed route info
servel traefik certs                  # SSL certificate info
servel traefik test <domain>          # Test domain routing
servel traefik restart                # Restart Traefik
```

### Verification

```bash
servel verify <name>                  # Full verification
servel verify config                  # Verify configuration
servel verify health <name>           # Check service health
servel verify ssl <domain>            # Check SSL certificates
servel verify dns <domain>            # Check DNS configuration
servel verify routing <name>          # Check Traefik routing
servel verify dependencies <name>     # Check dependencies
servel verify resources               # Check resource availability
```

### Dev Mode

```bash
servel dev                            # Start dev session
servel dev --team                     # Bidirectional sync (collaboration)
servel dev --port 3001                # Custom port
servel dev --domain staging.app.com   # Custom domain
servel dev --no-sync                  # One-time upload only
servel dev --conflict-policy newer-wins # Sync conflict resolution
servel dev list                       # Active sessions
servel dev logs <id> -f               # Follow session logs
servel dev stop <id>                  # Stop session
servel tunnel                         # Expose localhost publicly
servel tunnel start <port>            # Start tunnel on port
servel tunnel list                    # List active tunnels
servel tunnel stop <id>               # Stop tunnel
servel port-forward db 5432           # Forward remote port locally
```

**Conflict policies:** remote-wins, local-wins, newer-wins, backup

### Environment Variables

```bash
servel env set <name> KEY=VALUE       # Set env var
servel env vars <name>                # Show env vars
servel env list                       # List environments
servel config show <name>             # Show deployment config
servel config sync <name>             # Sync config to servel.yaml
servel config sync --dry-run          # Preview sync
```

### Alerts

```bash
servel alerts setup                   # Interactive wizard
servel alerts add telegram            # Add Telegram channel
servel alerts add slack               # Add Slack channel
servel alerts add discord             # Add Discord channel
servel alerts add webhook             # Add webhook
servel alerts test                    # Test notifications
servel alerts status                  # Show alert status
servel alerts history                 # View alert history
servel alerts pause 2h                # Maintenance mode (pause alerts)
```

### CI/CD

```bash
servel ci init github                 # Initialize GitHub Actions
servel ci init gitlab                 # Initialize GitLab CI
servel ci list                        # List pipelines
servel ci run <config>                # Run built-in CI
servel ci status <run-id>             # Check run status
servel ci logs <run-id>               # View CI logs
servel ci recent                      # Recent runs
servel ci cancel <run-id>             # Cancel run
servel ci retry <run-id>              # Retry run
```

### Access Control

```bash
servel auth login                     # User authentication
servel auth logout                    # Logout
servel auth whoami                    # Current user info
servel auth enable <name>             # Enable basic auth
servel auth disable <name>            # Disable basic auth
servel access user                    # User management
servel access role                    # Role management
```

### Advanced

```bash
servel detect                         # Detect project build type
servel detect --verbose               # Detailed detection info
servel init                           # Initialize servel.yaml
servel validate                       # Validate servel.yaml
servel upgrade                        # Self-upgrade CLI
servel upgrade-servers                # Upgrade server binaries
servel audit list                     # View audit logs
servel audit stats                    # Audit statistics
servel tag <name> <tag>               # Add tags to deployment
servel untag <name> <tag>             # Remove tags
```

## Common Workflows

### Deploy with Database

```bash
servel add postgres --name mydb
servel deploy --link-infra mydb
# App receives DATABASE_URL, DB_HOST, DB_PORT, DB_PASSWORD
```

### Preview Deployments

```bash
servel deploy --preview --ttl 24h
# Returns: https://myapp-pr42.example.com
```

### Multi-Environment

```bash
servel deploy --env production
servel deploy --env staging
servel deploy --preview
```

### Debug Container

```bash
servel logs myapp -f                  # View logs
servel exec myapp sh                  # Shell into container
servel exec myapp -- cat /app/.env    # Run command
servel logs @mydb -f                  # View infra logs (@ prefix)
servel exec @chatwoot --service rails sh  # Multi-service infra
```

### Backup & Restore

```bash
servel infra backup mydb
servel infra restore mydb backup-2024-01-15.sql.gz
```

### CI/CD Deploy Keys

```bash
servel server keys add prod --name github-actions --key-file pubkey.pub
```

### Troubleshoot Routing

```bash
servel verify dns app.example.com     # Check DNS
servel verify ssl app.example.com     # Check SSL
servel traefik test app.example.com   # Test routing
servel traefik logs                   # View Traefik logs
```

## Configuration (servel.yaml)

```yaml
name: myapp
domain: app.example.com

build:
  preset: bun                         # bun, node, python, go
  dockerfile: Dockerfile
  buildCommand: bun run build
  startCommand: bun run start

env:
  NODE_ENV: production

secrets:
  - API_KEY
  - DB_PASSWORD

resources:
  memory: 512M
  cpus: 0.5

replicas: 2

healthcheck:
  type: http                          # http, tcp, cmd, none
  path: /health
  interval: 30s
  timeout: 10s
  retries: 3

update:
  order: start-first                  # start-first, stop-first
  failure_action: rollback            # rollback, pause, continue

infra:
  - name: mydb
    prefix: DB                        # → DB_HOST, DB_PORT, DB_PASSWORD

routes:
  - type: http
    domain: app.example.com
    port: 3000
  - type: http
    domain: api.example.com
    path: /v1/*
    port: 3001

persist:
  - /app/data
  - /app/uploads

dev:
  command: bun run dev
  port: 3000
  sync:
    ignore:
      - "*.log"
      - ".cache"

environments:
  production:
    domain: myapp.com
    replicas: 5
  staging:
    domain: staging.myapp.com
  preview:
    ttl: 7d
```

## Aliases

| Command | Aliases |
|---------|---------|
| deploy | d, push |
| remove | rm, delete |
| logs | log |
| exec | x, run |
| rollback | rb |
| inspect | i, info |
| ps | ls, list |
| verify | v, check |
| doctor | dr |
| port-forward | pf |
| watch | w |
| server | srv |
| infra | infrastructure |
| domains | dom |
| alerts | alert, alrt |
| connect | conn |
| tunnel | tun |
| rename | mv, move |
| add | create, new |
| stats | stat |
| access | acl |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Build fails | `servel logs <name>`, try `--verbose` |
| Port conflict | Use `--port` flag |
| Domain not working | `servel verify dns <domain>` |
| SSL issues | `servel verify ssl <domain>` |
| Container exits | Check start command and port |
| Smart mode wrong | Use `--no-smart` for full rebuild |
| Routing broken | `servel traefik test <domain>` |
| Health check fails | `servel verify health <name>` |

**Diagnostic commands:**
```bash
servel doctor                         # System check
servel verify health <name>           # Health check
servel verify dns <domain>            # DNS check
servel verify ssl <domain>            # SSL check
servel traefik status                 # Routing status
servel logs <name>                    # View logs
servel inspect <name>                 # Deployment details
```

## Reference Files

- [Template Building Guide](references/TEMPLATES.md) - Create custom infrastructure types
- Full docs: https://servel.dev/docs
- Infrastructure Hub: https://hub.servel.dev
