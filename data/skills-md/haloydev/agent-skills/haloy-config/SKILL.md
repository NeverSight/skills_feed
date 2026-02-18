---
name: haloy-config
description: Create a haloy.yaml configuration file for deploying applications with haloy. Use when the user says "create haloy config", "add haloy.yaml", "configure for haloy", "set up haloy deployment", or "prepare for haloy". Supports single-target and multi-target deployments with optional self-hosted databases. Not for creating Dockerfiles (use the dockerize skill), multi-environment deployments, or docker-compose/Kubernetes setups.
---

# Haloy Configuration

Create `haloy.yaml` configuration files for deploying applications with [haloy](https://haloy.dev).

If no Dockerfile exists and the user needs one, inform them:

> "No Dockerfile found in this project. Haloy deploys Docker containers, so you'll need a Dockerfile first. Would you like me to create one using the `dockerize` skill?"

## How It Works

1. **Check for Dockerfile** - Verify the project can be containerized
2. **Check for configured haloy servers** - Look for existing server configurations
3. **Detect the project type** by examining:
   - `package.json` with framework dependencies (Next.js, TanStack Start, Express, etc.)
   - `pyproject.toml`, `requirements.txt`, `Pipfile` (Python/Django/FastAPI)
   - `go.mod` (Go)
   - `Cargo.toml` (Rust)
   - `Gemfile` (Ruby/Rails)
   - `composer.json` (PHP/Laravel)
4. **Detect database dependencies** (Prisma, Drizzle, pg, SQLAlchemy, etc.)
5. **Infer defaults** for app name, port, and health check path
6. **Ask the user** for server (from configured list or manual entry) and domain
7. **If database detected**, ask if they want self-hosted or external
8. **Generate haloy.yaml** with appropriate configuration
9. **Provide next steps** for validation and deployment

## Project Detection

Detect the framework to determine the default port:

| Framework | Indicator | Default Port |
|-----------|-----------|--------------|
| Next.js | `next` in package.json dependencies | 3000 |
| TanStack Start | `@tanstack/react-start` in package.json | 3000 |
| Express/Node.js | `express` in package.json or generic Node | 3000 |
| Vite | `vite` in package.json | 5173 (dev) / 3000 (prod) |
| Django | `django` in requirements.txt or pyproject.toml | 8000 |
| FastAPI | `fastapi` in requirements.txt or pyproject.toml | 8000 |
| Flask | `flask` in requirements.txt or pyproject.toml | 5000 |
| Go | `go.mod` present | 8080 |
| Rust | `Cargo.toml` present | 8080 |
| Ruby/Rails | `rails` in Gemfile | 3000 |
| PHP/Laravel | `laravel` in composer.json | 8000 |
| Default | Unknown framework | 8080 |

Also check the Dockerfile for `EXPOSE` directives which override framework defaults.

## Database Detection

Scan for database dependencies to determine if the project uses a database:

| Indicator | Database Type |
|-----------|---------------|
| `@prisma/client`, `prisma` in package.json | Check schema for provider |
| `drizzle-orm` in package.json | Check config for driver |
| `pg`, `postgres` in package.json | PostgreSQL |
| `mysql2` in package.json | MySQL |
| `better-sqlite3`, `sqlite3` in package.json | SQLite (no service needed) |
| `sequelize`, `typeorm` in package.json | Check config for dialect |
| `psycopg2`, `asyncpg` in requirements.txt | PostgreSQL |
| `sqlalchemy` in requirements.txt | Check config for driver |
| `django` in requirements.txt | Check settings for database |
| `prisma/schema.prisma` file exists | Check `provider` in datasource block |

**Prisma schema example** - look for the provider:
```prisma
datasource db {
  provider = "postgresql"  // or "mysql", "sqlite"
  url      = env("DATABASE_URL")
}
```

## Decision Flow

Use defaults unless a critical value is missing. Only ask the user when necessary.

### App Name
- **First choice**: `name` field in `package.json`
- **Second choice**: Project folder name
- **Ask if**: Name contains invalid characters or is generic (e.g., "app", "project")

### Server URL

Check for configured servers in `~/.config/haloy/client.yaml`:

```yaml
# Example client.yaml structure
servers:
  example.haloy.dev:
    token_env: HALOY_API_TOKEN_example_HALOY_DEV
  prod.mycompany.com:
    token_env: HALOY_API_TOKEN_PROD
```

**Decision flow:**

1. **If servers found**: Present them as options and let the user choose. The server keys (e.g., `example.haloy.dev`) are the values to use in the config.
   > "I found these configured haloy servers. Which one would you like to deploy to?"
   > - example.haloy.dev
   > - prod.mycompany.com
   > - Enter a different server

2. **If no servers found**: Check if haloy CLI is installed by running `which haloy` or `haloy --version`
   - **If haloy is installed**: Ask for the server URL manually
     > "What is your haloy server URL? (e.g., haloy.yourserver.com)"
   - **If haloy is not installed**: Inform the user they need to install and configure the CLI first
     > "No haloy servers configured. To deploy with haloy, you'll need to install the CLI and add a server. See: https://haloy.dev/docs/client-installation"

### Domain
- **Always ask** - Required for web applications
- Example prompt: "What domain should this app be accessible at? (e.g., myapp.example.com)"
- If user says "none" or "skip", omit the domains section

### Domain Aliases
- **Ask after domain**: Once the user provides a domain, ask if they want to add any aliases
- Example prompt: "Would you like to add any domain aliases? (e.g., www.myapp.example.com)"
- Common alias: `www.` prefix of the main domain
- If user says "none" or "skip", omit the aliases

### DNS Reminder
After gathering domain information, remind the user to configure DNS:

> "Remember to configure DNS with your domain provider. Point your domain(s) to your haloy server's IP address using an A record, or use a CNAME record if your server has a domain name."

### Port
- **Use framework default** from the table above
- **Check Dockerfile** for `EXPOSE` directive which takes precedence
- **Ask only if**: Multiple ports exposed or no clear default

### Health Check Path
- **Search for existing endpoints**: `/health`, `/healthz`, `/api/health`, `/_health`
- **If found**: Use the existing health endpoint
- **If not found**: Use `/` (root path)
- Do NOT ask - haloy will use `/` by default which works for most apps

### Database
If database dependencies are detected (see Database Detection section):

1. **Ask the user**:
   > "I detected database dependencies ([detected type]). Would you like to add a self-hosted database service, or will you use an external provider (Supabase, Neon, RDS, etc.)?"
   > - Add self-hosted database
   > - Use external provider (I'll configure DATABASE_URL myself)

2. **If self-hosted**:
   - Generate multi-target config with database service + app target
   - Use the `database` preset for the database target
   - Add appropriate environment variables with placeholder values
   - Add volume for data persistence
   - Database defaults by type:

   | Database | Image | Port | Volume Path |
   |----------|-------|------|-------------|
   | PostgreSQL | `postgres:17` | 5432 | `/var/lib/postgresql/data` |
   | MySQL | `mysql:8` | 3306 | `/var/lib/mysql` |

3. **If external provider**:
   - Generate single-target config as usual
   - Remind user: "Remember to set the `DATABASE_URL` environment variable for your external database."

## Configuration Reference

Haloy supports two modes:

1. **Single Deployment**: No `targets` defined, root configuration is the deployment target
2. **Multi-Target**: `targets` defined, root acts as base/default configuration

### Minimal Configuration (Single Deployment)

```yaml
name: "my-app"
server: "haloy.yourserver.com"
```

### With Domain and Port

```yaml
name: "my-app"
server: "haloy.yourserver.com"
domains:
  - domain: "my-app.example.com"
    aliases:
      - "www.my-app.example.com"
port: "3000"
health_check_path: "/health"
```

### With Environment Variables

```yaml
name: "my-app"
server: "haloy.yourserver.com"
domains:
  - domain: "my-app.example.com"
port: "3000"
env:
  - name: "NODE_ENV"
    value: "production"
  - name: "DATABASE_URL"
    value: "postgres://user:pass@db:5432/myapp"
```

### With Volumes (for persistent data)

```yaml
name: "my-app"
server: "haloy.yourserver.com"
domains:
  - domain: "my-app.example.com"
volumes:
  - "app-data:/app/data"
```

### With Self-Hosted Database (Multi-Target)

```yaml
server: "haloy.yourserver.com"
env:
  - name: POSTGRES_USER
    value: "postgres"
  - name: POSTGRES_PASSWORD
    value: "change-me-in-production"
  - name: POSTGRES_DB
    value: "my_app"

targets:
  postgres:
    preset: database
    image:
      repository: postgres:17
    port: 5432
    volumes:
      - postgres-data:/var/lib/postgresql/data

  my-app:
    domains:
      - domain: "my-app.example.com"
    port: 3000
    env:
      - name: DATABASE_URL
        value: "postgres://postgres:change-me-in-production@postgres:5432/my_app"
      - name: NODE_ENV
        value: "production"
```

### Multi-Target Example

```yaml
# Base settings inherited by all targets
image:
  repository: "my-app"
  tag: "latest"
port: "3000"

targets:
  production:
    server: "prod.haloy.com"
    domains:
      - domain: "my-app.com"
    replicas: 2
  staging:
    server: "staging.haloy.com"
    domains:
      - domain: "staging.my-app.com"
    replicas: 1
```

### Full Reference

For all configuration options, see: https://haloy.dev/docs/configuration-reference

Key options:
- `name` - Application name (required for single deployment)
- `server` - Haloy server URL (required)
- `image` - Docker image configuration (repository, tag)
- `domains` - Array of domain objects with `domain` and optional `aliases`
- `port` - Container port (default: "8080")
- `health_check_path` - Health check endpoint (default: "/")
- `env` - Environment variables as name/value pairs
- `volumes` - Volume mounts for persistent data
- `replicas` - Number of container instances (default: 1)
- `deployment_strategy` - "rolling" (default) or "replace"
- `targets` - Define multiple deployment targets (multi-target mode)
- `preset` - Apply preset configuration ("database" or "service")

## Output Format

After gathering information, create the `haloy.yaml` file and provide:

1. **The haloy.yaml file** - Written to the project root
2. **Update .dockerignore** - Add `haloy.yaml` to `.dockerignore` if not already present. This improves Docker layer caching since changes to `haloy.yaml` won't invalidate the build cache.
3. **Validation command**:
   ```bash
   haloy validate-config
   ```
4. **Deployment command**:
   ```bash
   haloy deploy
   ```
5. **If haloy CLI is not installed**, show installation options:
   ```bash
   # Shell script
   curl -fsSL https://sh.haloy.dev/install-haloy.sh | sh

   # Homebrew
   brew install haloydev/tap/haloy

   # npm/pnpm/bun
   npm install -g haloy
   pnpm add -g haloy
   bun add -g haloy
   ```

## Example Interactions

See `references/examples.md` for detailed interaction examples covering:
- Deploying with configured servers
- Database detection and self-hosted database setup
- Handling missing server configuration
