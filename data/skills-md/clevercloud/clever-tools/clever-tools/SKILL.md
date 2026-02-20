---
name: clever-tools
description: CLI to deploy and manage applications, add-ons, and configurations on Clever Cloud PaaS. Use when the user needs to deploy apps, view logs, manage environment variables, configure domains, or interact with Clever Cloud services.
license: Apache-2.0
metadata:
  author: CleverCloud
---

# Clever Tools

Clever Tools is the official CLI for Clever Cloud, a Platform-as-a-Service (PaaS) provider. It allows you to deploy applications, manage add-ons (databases, storage, etc.), configure environment variables, domains, and monitor your services.

Use this skill when the user wants to deploy code to Clever Cloud, manage their hosted applications, or interact with Clever Cloud services.

## Quick Start

```bash
# Login to Clever Cloud (opens browser for OAuth)
clever login

# For CI/CD, use token-based authentication
export CLEVER_TOKEN="your-token"
export CLEVER_SECRET="your-secret"

# Link an existing application to current directory
clever link <app-id>

# Or create a new application
clever create --type node myapp

# Deploy current directory
clever deploy
```

## Essential Commands

### Deployment

```bash
# Deploy current directory (git push to Clever Cloud)
clever deploy

# Deploy with specific commit or branch
clever deploy --branch main
clever deploy --commit HEAD~2

# Restart application
clever restart

# Stop application (scales to 0)
clever stop

# Check deployment status
clever status

# View deployment history
clever activity
clever activity --follow  # Live updates
```

### Logs

```bash
# Stream live logs
clever logs

# View logs from last hour
clever logs --since 1h

# View logs before a specific time
clever logs --before 2024-01-15T10:00:00

# Filter by deployment
clever logs --deployment-id <id>

# Access logs (HTTP requests)
clever accesslogs
clever accesslogs --since 1h
```

### Environment Variables

```bash
# List all environment variables
clever env

# Set a variable
clever env set MY_VAR "my value"

# Set multiple variables
clever env set VAR1=value1 VAR2=value2

# Remove a variable
clever env rm MY_VAR

# Import from .env file
clever env import .env

# Export for shell
clever env --format shell > .env
```

### Domains

```bash
# List domains
clever domain

# Add a custom domain
clever domain add myapp.example.com

# Remove a domain
clever domain rm myapp.example.com

# Favorite domain (used in logs, URLs)
clever domain favorite set myapp.example.com
```

### Add-ons (Databases, Storage, etc.)

```bash
# List your add-ons
clever addon

# List available add-on providers
clever addon providers

# Create a PostgreSQL database
clever addon create postgresql-addon mydb --plan dev

# Create Redis
clever addon create redis-addon myredis --plan s_mono

# Create S3-compatible storage (Cellar)
clever addon create cellar-addon mybucket

# Delete an add-on
clever addon delete <addon-id>

# Get add-on environment variables
clever addon env <addon-id>
```

### Services (Managed services like Keycloak, Matomo)

```bash
# Link add-on to application
clever service link-addon <addon-id>

# Unlink add-on
clever service unlink-addon <addon-id>
```

### Scaling

```bash
# View current scaling
clever scale

# Set instance size (flavor)
clever scale --flavor M

# Set number of instances
clever scale --instances 2

# Autoscaling
clever scale --min-instances 1 --max-instances 4
```

### SSH Access

```bash
# SSH into running instance
clever ssh

# Run a command
clever ssh --command "ls -la"
```

### Applications Management

```bash
# List all applications in organization
clever applications list

# List linked applications in current directory
clever applications

# Create new application
clever create --type <type> <name>
# Types: node, python, ruby, php, java, go, rust, docker, static...

# Delete application
clever delete
```

## Common Global Options

These options work with most commands:

```bash
--app <app-id|name>      # Target specific app (when multiple linked)
--alias <alias>          # Use app alias (from clever link --alias)
--org <org-id|name>      # Target specific organization
-F, --format <format>    # Output format: human, json, json-stream, shell
-y, --yes                # Skip confirmation prompts
```

JSON output is useful for scripting:
```bash
clever env --format json | jq '.MY_VAR'
clever applications list --format json
```

## Full Reference

For complete documentation of all commands, options, available runtimes, add-on providers, and deployment zones, see [references/full-documentation.md](references/full-documentation.md).
