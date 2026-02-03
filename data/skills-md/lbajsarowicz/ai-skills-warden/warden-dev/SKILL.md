---
name: warden-dev
description: Manage Docker-based local development environments with Warden. Use when setting up PHP/Node projects (Magento, Laravel, Symfony, WordPress, Drupal), importing databases, running shell commands, debugging with Xdebug, or managing Docker services. Triggers on "warden", "local environment", "docker-compose wrapper", "database import", "shell access".
license: MIT
metadata:
  author: lbajsarowicz
  version: '1.0.0'
---

# Warden Agent Skill

Warden is a local wrapper for docker-compose that automates DNS (dnsmasq), reverse proxy (Traefik), and webmail (Mailpit). Project `.env` drives ephemeral `docker-compose.yml` generation. Preview with `warden env config`.

## Quick Start

```bash
warden env-init myproject magento2   # Initialize project
warden svc up -d                     # Start global services (Traefik, DNS, Mailpit)
warden env up -d                     # Start project containers
warden shell                        # Interactive shell in php-fpm
```

## Environment Lifecycle

| Command | Purpose | Example |
|---------|---------|---------|
| `warden env-init` | Initialize new project | `warden env-init mystore magento2` |
| `warden env up` | Start environment | `warden env up -d` |
| `warden env down` | Stop environment | `warden env down` |
| `warden env config` | Preview docker-compose | `warden env config` |
| `warden env ps` | List containers | `warden env ps` |
| `warden env pull` | Pull images | `warden env pull` |
| `warden env logs -f nginx` | Follow logs | `warden env logs -f nginx` |
| `warden env exec php-fpm bash` | Exec into container | `warden env exec php-fpm bash` |

## Database Operations

| Command | Purpose | Example |
|---------|---------|---------|
| `warden db connect` | Interactive MySQL | `warden db connect` |
| `warden db import` | Import SQL dump | See patterns below |
| `warden db dump` | Export database | `warden db dump > backup.sql` |
| `warden db upgrade` | Upgrade MariaDB/MySQL | `warden db upgrade` |

**Import patterns (preferred for large dumps):**

```bash
pv dump.sql.gz | gzip -d | warden db import
gzip -dc dump.sql.gz | warden db import
warden db import < database.sql
```

## Shell Access

| Command | Purpose |
|---------|---------|
| `warden shell` | PHP-FPM container shell (default: bash) |
| `warden debug` | Xdebug-enabled shell (use for debugging) |
| `warden blackfire` | Blackfire profiler: `warden blackfire run php script.php` |
| `warden spx` | PHP SPX profiler |

**Important:** Use `warden debug` (not `warden shell`) when debugging with Xdebug.

## Service Management

| Command | Purpose |
|---------|---------|
| `warden svc up -d` | Start global services |
| `warden svc down` | Stop global services |
| `warden svc ps` | List global services |
| `warden status` | List running environments |

## File Sync (macOS)

| Command | Purpose |
|---------|---------|
| `warden sync start` | Start Mutagen sync |
| `warden sync monitor` | Monitor sync status |
| `warden sync flush` | Flush sync |
| `warden sync reset` | Reset sync |

## Redis / Valkey

```bash
warden redis              # Interactive Redis CLI
warden redis FLUSHALL      # Execute command
warden valkey              # Valkey (Redis alternative)
```

## Environment Types

Supported: `magento2`, `magento1`, `laravel`, `symfony`, `wordpress`, `drupal`, `shopware`, `cakephp`, `local`. See `references/environments.md`.

## Key .env Variables

Project `.env` controls services and versions. See `references/env-variables.md` for full reference.

| Variable | Description |
|----------|-------------|
| `WARDEN_ENV_NAME` | Unique project identifier |
| `WARDEN_ENV_TYPE` | Environment type |
| `TRAEFIK_DOMAIN` | Base domain (default: `{name}.test`) |
| `PHP_VERSION` | PHP version (7.4, 8.1–8.4) |
| `WARDEN_DB`, `WARDEN_REDIS`, etc. | Service toggles (1/0) |
| `MYSQL_DISTRIBUTION_VERSION` | MariaDB/MySQL version |

## Service Name Mapping

| .env Variable | Container Name(s) |
|---------------|-------------------|
| `WARDEN_DB=1` | `db` |
| `WARDEN_REDIS=1` | `redis` |
| `WARDEN_OPENSEARCH=1` | `opensearch` |
| `WARDEN_ELASTICSEARCH=1` | `elasticsearch` |
| `WARDEN_VARNISH=1` | `varnish` |
| `WARDEN_RABBITMQ=1` | `rabbitmq` |
| `WARDEN_NGINX=1` | `nginx` |
| `PHP_VERSION` | `php-fpm`, `php-debug` |

## Global Services & URLs

Default domain: `warden.test`. Configure in `~/.warden/.env` (`WARDEN_SERVICE_DOMAIN`).

| Service | URL |
|---------|-----|
| Traefik Dashboard | `https://traefik.warden.test` |
| Webmail (Mailpit) | `https://webmail.warden.test` |
| Portainer | `https://portainer.warden.test` |
| phpMyAdmin | `https://phpmyadmin.warden.test` |

**Email (Mailpit):** No SMTP config needed. Warden routes sendmail to Mailpit. All emails at `https://webmail.warden.test`.

## Framework Compatibility

For "match Magento 2.4.8 requirements" requests:

1. Search official docs for system requirements
2. Map to `.env`: PHP → `PHP_VERSION`, DB → `MYSQL_DISTRIBUTION_VERSION`, etc.
3. Update `.env` with matched versions

## Agent Behavior Examples

**Generate service table:** Read `.env`, map `WARDEN_*` variables to service status, output table (Service | Status | Version).

**Verify PHP running:** Run `warden env ps`, check for `php-fpm`, `php-debug`, `php-blackfire`.

**Troubleshoot non-loading site:** `warden svc ps` → `warden env ps` → `ping app.{project}.test` → `warden env logs nginx`.

**Xdebug not working:** Use `warden debug`, verify IDE server name `{project}-docker`, port 9003, XDEBUG_SESSION cookie.

## References

- `references/commands.md` – Full command reference
- `references/environments.md` – Environment types
- `references/env-variables.md` – .env variable reference
- `references/global-services.md` – Service URLs and config
- `references/troubleshooting.md` – Common issues and solutions
- `examples/workflows.md` – Workflow examples
