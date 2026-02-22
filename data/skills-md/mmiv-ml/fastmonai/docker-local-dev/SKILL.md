---
name: docker-local-dev
description: Generate Docker Compose and Dockerfile configurations for local development through interactive Q&A. Supports PHP/Laravel, WordPress, Drupal, Joomla, Node.js, and Python stacks with Nginx, Supervisor/PM2, databases, Redis, and email testing. Always asks clarifying questions before generating configurations.
author: Official
---

# Docker Local Development Environment Generator

## Overview

This skill helps you create optimized Docker development environments for your projects. It generates `docker-compose.yml`, `Dockerfile`, and related configurations through an interactive, question-driven workflow.

**When to use this skill:**
- Setting up a new Docker development environment
- Dockerizing an existing project for local development
- Adding services (database, Redis, email testing) to your Docker setup
- Updating or merging with existing Docker configurations

**Key Principle:** This skill ALWAYS asks questions before making decisions. You will be notified about each configuration choice and can adjust settings to match your exact needs.

## Important Notice

This skill uses an **interactive approach**. Before generating any files, I will:

1. Run auto-detection scripts to identify your tech stack (saves AI tokens)
2. Present the detection results for your confirmation
3. Ask 10-15 clarifying questions about your preferences
4. Show you a preview before creating or modifying files

**Why this approach?** Docker configurations are project-specific. Asking questions ensures the setup matches YOUR requirements, not generic defaults. This prevents issues and saves debugging time later.

## Quick Start

To generate a Docker development environment:
1. Navigate to your project root
2. Tell the AI: "Use the docker-local-dev skill to set up Docker"
3. Confirm or correct the auto-detected tech stack
4. Answer the configuration questions
5. Review and approve the generated files

## Supported Tech Stacks

| Stack | Framework/CMS | Process Manager | Notes |
|-------|--------------|-----------------|-------|
| PHP | Laravel 10/11/12 | Supervisor | Queue workers, scheduler |
| PHP | WordPress | WP-CLI | Debug plugins, error logging |
| PHP | Drupal 10/11 | Drush | Development services |
| PHP | Joomla 4/5 | - | CLI tools, debug mode |
| Node.js | Express, NestJS, Next.js | PM2 or Supervisor | Hot reload support |
| Python | Django, FastAPI, Flask | Celery, Supervisor | WSGI/ASGI servers |

**Unsupported Stack?** The skill will proceed with generic configuration and suggest contributing improvements. See `CONTRIBUTING.md` for details.

## Interactive Workflow

### Phase 0: Auto-Detection (Script-based)

**Before using AI**, run detection scripts to save tokens:

```bash
# The skill will run this automatically
./scripts/detect-stack.sh
```

**Detection checks:**
- `composer.json` → Laravel, PHP version
- `wp-config.php`, `wp-content/` → WordPress
- `core/`, `sites/default/` → Drupal
- `configuration.php`, `administrator/` → Joomla
- `package.json` → Node.js, framework, version
- `requirements.txt`, `pyproject.toml` → Python, framework
- `.env`, config files → Database type, Redis usage

**Present results to user:**
```
I detected: Laravel 11 + PHP 8.3 + MySQL + Redis

Is this correct?
- Yes → proceed with detected settings
- No → I'll analyze further using AI
```

**If stack is NOT officially supported:**
```
I detected [stack] but this is not in our supported list.
The Docker setup may not be optimal.

Proceeding with generic configuration...

If this works for you, please consider contributing to improve support!
See: CONTRIBUTING.md
```

### Phase 1: Initial Discovery

**Check for existing Docker files:**

1. Look for `docker-compose.yml`, `docker-compose.yaml`, `Dockerfile`
2. If found, ask:
   ```
   I found existing Docker files:
   - docker-compose.yml (modified 2 days ago)
   - Dockerfile

   How should I proceed?
   1. Merge (preserve your custom settings, add new services)
   2. Replace (backup existing, generate fresh)
   3. Cancel (let me review first)
   ```

**Backup strategy:**
- Timestamped backups: `docker-compose.yml.backup.2024-01-15-143022`
- Never overwrite without backup

### Phase 2: Tech Stack Confirmation

**If auto-detection succeeded:**
```
Detected configuration:
- Framework: Laravel 11
- PHP Version: 8.3
- Database: MySQL (from .env DB_CONNECTION)
- Redis: Yes (from .env REDIS_HOST)
- Queue: Yes (jobs table detected)

Please confirm or adjust these settings.
```

**If auto-detection failed or unclear:**
```
What is your primary tech stack?

1. PHP/Laravel
2. WordPress
3. Drupal
4. Joomla
5. Node.js (Express/NestJS/Next.js)
6. Python (Django/FastAPI/Flask)
7. Other (I'll try generic configuration)
```

### Phase 3: CMS-Specific Questions

**WordPress:**
```
WordPress Development Options:

1. Install debug plugins?
   - Query Monitor (SQL queries, hooks, conditionals)
   - Debug Bar (debug info in admin bar)

2. Enable WP_DEBUG and error logging?
   - WP_DEBUG = true
   - WP_DEBUG_LOG = true
   - SCRIPT_DEBUG = true
```

**Drupal:**
```
Drupal Development Options:

1. Install Drush globally in container?
2. Enable development services (verbose errors, twig debug)?
3. Disable caching for development?
```

**Joomla:**
```
Joomla Development Options:

1. Enable debug mode?
2. Install Joomla CLI tools?
```

### Phase 3.5: Existing Docker Images Scan

**Before suggesting service versions**, check locally available images to save disk space:

```bash
# The skill will run this automatically
./scripts/detect-images.sh
```

**Present results to user:**
```
I found these images already on your machine:

Databases:
- mysql:8.0.35 (2.3 GB)
- mariadb:11.2 (1.1 GB)

Using existing images saves disk space and download time.

Which database would you like to use?
1. mysql:8.0.35 (already downloaded - saves 2.3 GB)
2. mariadb:11.2 (already downloaded - saves 1.1 GB)
3. Different version (will download new image)
   → What version do you need for production compatibility?
```

**If no existing images found:**
```
No database images found locally.

Which database would you like to use?
1. MySQL 8.0 (recommended for Laravel/WordPress)
2. MariaDB 11 (MySQL-compatible, smaller)
3. PostgreSQL 16 (if your app requires it)
```

**Same approach for other services:**
- Check for existing Redis, PHP, Node, Nginx, Mailpit/MailHog images
- Suggest matching versions when available
- Always offer "different version" option for production compatibility

### Phase 4: Service Configuration (Smart Recommendations)

**IMPORTANT: Check actual usage before recommending services.**

Before suggesting any optional service, verify if it's actually being used in the project:

```bash
# Check .env for actual service usage
grep -E '^(CACHE_DRIVER|CACHE_STORE|SESSION_DRIVER|QUEUE_CONNECTION|MAIL_MAILER)=' .env
```

**Database Selection** (always needed, use images from Phase 3.5):
```
Which database would you like to use?

1. MySQL 8.0 (recommended for Laravel/WordPress)
2. MariaDB 11 (MySQL-compatible, lighter)
3. PostgreSQL 16 (required for some apps)
```

**Redis Configuration** (check actual usage first):

First, check if Redis is actually used:
```bash
grep -E '^(CACHE_DRIVER|SESSION_DRIVER|QUEUE_CONNECTION)=' .env
```

**If Redis is NOT in use** (CACHE_DRIVER=file, SESSION_DRIVER=file, QUEUE_CONNECTION=sync):
```
I noticed your .env configuration:
- CACHE_DRIVER=file (not using Redis for cache)
- SESSION_DRIVER=file (not using Redis for sessions)
- QUEUE_CONNECTION=sync (not using Redis for queues)

Redis is not currently used in your project.
Do you want to add Redis anyway?
1. No, skip Redis (recommended based on your config)
2. Yes, I plan to switch to Redis later
```

**If Redis IS in use** (any of the above = redis):
```
Do you need Redis?

1. Yes, for caching only
2. Yes, for caching + sessions
3. Yes, for caching + sessions + queues
4. No, I don't need Redis
```

**Email Testing** (check actual usage first):

First, check MAIL_MAILER setting:
```bash
grep -E '^MAIL_MAILER=' .env
```

**If using log or array mailer:**
```
Your MAIL_MAILER is set to 'log' (emails logged, not sent).
Do you want to add email testing service anyway?
1. No, skip email testing (recommended based on your config)
2. Yes, add Mailpit for testing
```

**If using smtp or other mailer:**
```
Which email testing service would you prefer?

1. Mailpit (modern, actively maintained, recommended)
   - Web UI: http://localhost:8025
   - SMTP: localhost:1025

2. MailHog (widely used, stable)
   - Web UI: http://localhost:8025
   - SMTP: localhost:1025

3. None (I'll configure email separately)
```

**Background Task Processing** (check actual usage first):

For Laravel, check if queues are actually used:
```bash
grep -E '^QUEUE_CONNECTION=' .env
# Also check if jobs table exists or queue jobs are defined
```

**If QUEUE_CONNECTION=sync:**
```
Your QUEUE_CONNECTION is set to 'sync' (no background processing).
Do you need background task processing anyway?
1. No, skip queue workers (recommended based on your config)
2. Yes, I plan to switch to async queues later
```

**If QUEUE_CONNECTION=database/redis:**
```
Do you need background task processing?

1. Queue workers only (Supervisor)
2. Scheduler only (cron replacement via Supervisor)
3. Both queue workers and scheduler
4. No background processing needed
```

For Node.js:
```
How do you want to manage Node.js processes?

1. PM2 (process manager with clustering, recommended)
2. Supervisor (simple process monitoring)
3. Direct node command (development only)
```

For Python:
```
Background task processing options:

1. Celery workers (for Django/FastAPI async tasks)
2. Supervisor for scheduled tasks (cron replacement)
3. Both Celery and scheduled tasks
4. No background processing needed
```

### Phase 5: Port Exposure & Configuration

**IMPORTANT: Ask about reverse proxy first before exposing ports.**

**Reverse Proxy Check:**
```
Are you using a reverse proxy (Nginx Proxy Manager, Traefik, Caddy)?

1. Yes, I'm using a reverse proxy
   → Ports will remain internal only
   → Services communicate via Docker network
   → You'll configure the proxy to route to containers

2. No, I want to expose ports directly
   → I'll help you choose which ports to expose
```

**If using reverse proxy (Option 1):**
```
Since you're using a reverse proxy, ports will be internal only.

Do you still want to expose the database port for external tools (DBeaver/DataGrip)?
1. Yes, expose database port (3306/5432) for SQL tools
2. No, keep everything internal
```

**If NOT using reverse proxy (Option 2), then ask port strategy:**
```
How do you want to expose ports?

1. Minimal (recommended for most projects)
   - Nginx: 8080 (web access)
   - Database: 3306/5432 (for SQL tools like DBeaver/DataGrip)

2. Full exposure (all services accessible)
   - Nginx: 8080
   - Database: 3306/5432
   - Redis: 6379
   - Mail UI: 8025
   - PHP-FPM: 9000 (if needed)
```

**Port Availability Check:**
```
Checking port availability...

Port 8080: Available
Port 3306: IN USE (another MySQL instance)
  → Suggesting 3307 instead

Port 6379: Available
```

**Configuration Storage:**
```
Where do you want to store configuration?

1. .env file (recommended)
   - Easier to change ports and settings
   - Keep secrets out of docker-compose.yml
   - Example: APP_PORT=8080, DB_PORT=3306

2. Directly in docker-compose.yml
   - Simpler for basic setups
   - All config in one place
   - Less flexible for different environments
```

### Phase 6: Network Configuration

**First, scan for existing Docker networks and reverse proxies:**

```bash
# The skill will run this automatically
./scripts/detect-network.sh
```

**If reverse proxy container detected (Nginx Proxy Manager, Traefik, Caddy):**
```
I scanned your Docker environment:

Reverse proxy found:
- Container: 'nginx-proxy-manager' on network: 'npm_default'

Do you want to connect this project to 'npm_default'?
1. Yes, use 'npm_default' for reverse proxy routing (recommended)
   → No port exposure needed
   → Configure routing in your proxy dashboard

2. No, use isolated network
   → I'll ask about port exposure
```

**If NO reverse proxy detected:**
```
No reverse proxy containers detected (Nginx Proxy Manager, Traefik, Caddy).

Available Docker networks:
- myapp_default
- shared_services

Do you want to:
1. Create isolated network for this project (recommended)
2. Use existing network: [select from list]
3. Create shared network for multiple projects
```

**Multiple Projects (if no proxy detected):**
```
Are you running multiple Docker projects on this machine?

1. Yes, I have multiple projects
   → Consider Nginx Proxy Manager for:
   - Custom domains (myapp.local, api.local)
   - Automatic SSL certificates
   - Centralized reverse proxy

2. No, this is my only Docker project
   → Use isolated project network
```

**Microservices/API Connection:**
```
Does this project need to connect to other Docker services?

1. Yes, I have other Docker services (APIs, microservices)
   → Create external shared network
   → Services can communicate via container names

2. No, this project is standalone
   → Use project-isolated network
```

### Phase 7: Volume Mount Strategy

**Always explain options:**
```
How would you like to mount your source code?

1. Bind mount (recommended for development)
   - Your local files sync to container immediately
   - Changes reflect instantly without rebuild
   - Best for: Active development, hot reload

2. Named volume (better performance)
   - Files copied into Docker volume
   - Faster file operations (especially on macOS)
   - Requires rebuild to see code changes
   - Best for: Testing, CI/CD

Note: Bind mounts have ~10-20% slower file I/O on macOS,
but the instant sync is worth it for development.
```

### Phase 8: Generation & Verification

**Docker Compose Version Note:**
- Do NOT include `version:` at the top of docker-compose.yml
- Docker Compose v2 deprecated this field
- Modern compose files don't need it

**File generation order:**
1. Create backup of existing files (if any)
2. Generate `.env.docker` or update `.env`
3. Generate `Dockerfile`
4. Generate `docker-compose.yml` (without version field)
5. Generate Nginx configuration
6. Generate Supervisor/PM2 configuration (if needed)
7. Create helper scripts

**After docker-compose up (AUTOMATIC):**

```bash
# These run automatically after containers start

# 1. Verify all ports are available
./scripts/port-check.sh

# 2. Health check all services
./scripts/health-check.sh

# 3. Test database with simple CRUD
./scripts/db-test.sh

# 4. Generate usage documentation
# Creates USAGE.md with commands for your stack
```

**Health Check Output:**
```
Docker Local Dev - Health Check
================================

Checking Nginx.............. OK
Checking PHP-FPM............ OK
Checking MySQL.............. OK
Checking Redis.............. OK
Checking Mailpit............ OK
Checking Queue Worker....... OK

Database CRUD Test:
- CREATE table............ OK
- INSERT data............. OK
- UPDATE data............. OK
- DELETE data............. OK
- DROP table.............. OK

All services are healthy!

Your development environment is ready:
- Web: http://localhost:8080
- Database: localhost:3306 (user: root, pass: secret)
- Mail UI: http://localhost:8025
```

### Phase 9: Documentation Generation

**Automatically creates USAGE.md:**
```markdown
# Docker Development Environment

## Quick Commands

Start containers:
docker compose up -d

Stop containers:
docker compose down

View logs:
docker compose logs -f

## Accessing Services

| Service | URL/Host | Credentials |
|---------|----------|-------------|
| Web | http://localhost:8080 | - |
| Database | localhost:3306 | root / secret |
| Redis | localhost:6379 | - |
| Mail UI | http://localhost:8025 | - |

## Container Networking (Important)

When the app runs inside Docker, `localhost` points to the app container. To connect to other services, use the Docker Compose service name (for example `db`, `redis`, `mailpit`) instead of `localhost`.

## Stack-Specific Commands

### Laravel
docker compose exec app php artisan migrate
docker compose exec app php artisan queue:work

### WordPress
docker compose exec app wp plugin list
docker compose exec app wp cache flush
```

## Merge Strategy

When merging with existing Docker files:

1. **Preserve user customizations:**
   - Custom environment variables
   - Volume mounts
   - Network configurations
   - Port mappings

2. **Add new services:**
   - Only add services that don't exist
   - Don't modify existing service definitions

3. **Show diff before applying:**
   ```diff
   + redis:
   +   image: redis:alpine
   +   volumes:
   +     - redis_data:/data

     services:
       app:
         # existing config preserved
   ```

4. **Require confirmation:**
   ```
   These changes will be applied:
   - Add Redis service
   - Add redis_data volume
   - Update app service to depend on Redis

   Proceed? [y/N]
   ```

## Health Check Protocol

Services are verified in this order:

1. **Database** (MySQL/PostgreSQL)
   - Connection test: `mysqladmin ping` or `pg_isready`
   - CRUD test: CREATE/INSERT/UPDATE/DELETE on test table

2. **Web Server** (Nginx)
   - HTTP request to localhost
   - Expect 200, 301, or 302 response

3. **Application**
   - Stack-specific checks
   - Laravel: `php artisan about`
   - WordPress: `wp core version`
   - Django: `python manage.py check`

4. **Redis** (if enabled)
   - `redis-cli ping` → expect PONG

5. **Queue Worker** (if enabled)
   - Process verification
   - Test job processing (optional)

6. **Email Service** (if enabled)
   - SMTP connection test
   - Web UI accessibility

## Troubleshooting

### Port Already in Use
```
Error: Port 3306 is already in use

Solutions:
1. Stop the conflicting service
2. Use a different port (skill will suggest alternatives)
3. Check: lsof -i :3306
```

### Database Connection Failed
```
Error: Cannot connect to MySQL

Check:
1. Is the container running? docker compose ps
2. Is the port exposed? docker compose port db 3306
3. Are credentials correct? Check .env or docker-compose.yml
```

### Permission Denied
```
Error: Permission denied on mounted volume

Solutions:
1. Check file ownership: ls -la
2. Match container user ID: Add user: "1000:1000" to service
3. Use :cached or :delegated mount options on macOS
```

## Reference Documentation

- [Tech Stack Detection](./references/tech-stack-detection.md)
- [Service Configuration Guide](./references/service-configuration-guide.md)
- [CMS Configuration Guide](./references/cms-configuration-guide.md)
- [Networking & Ports Guide](./references/networking-ports-guide.md)
- [Merge & Backup Strategy](./references/merge-backup-strategy.md)
- [Health Check Patterns](./references/health-check-patterns.md)

## Contributing

If your tech stack is not fully supported, please consider contributing!

See [CONTRIBUTING.md](./assets/templates/docs/CONTRIBUTING.md.template) for:
- How to add support for new tech stacks
- Template structure requirements
- Testing guidelines
