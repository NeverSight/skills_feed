---
name: coolify-manager
description: Manage and troubleshoot Coolify deployments using the official CLI and API. Use this skill when the user needs help with Coolify server management, WordPress troubleshooting on Coolify, debugging service issues, checking SSL certificates, accessing containers, or managing applications and databases through Coolify. Particularly useful for diagnosing down services, fixing .htaccess issues, REST API problems, and performing deployment operations.
---

# Coolify Manager

## Overview

This skill enables management of Coolify deployments through both the official CLI and direct API access. It provides workflows for diagnosing service issues, fixing common WordPress problems, managing containers, and performing deployment operations across self-hosted and cloud Coolify instances.

## Quick Start

### Prerequisites Check

Before proceeding, verify:
1. User has access to a Coolify instance (self-hosted or cloud)
2. User can obtain an API token from their Coolify dashboard at `/security/api-tokens`
3. User knows their Coolify instance URL

### When to Use This Skill

Invoke this skill when the user:
- Mentions Coolify by name
- Needs to debug a down WordPress site hosted on Coolify
- Wants to check service health, logs, or status
- Needs to access a container terminal
- Wants to manage deployments, services, or applications
- Has SSL certificate issues on Coolify-hosted sites
- Needs to fix .htaccess or PHP configuration issues
- Wants to manage environment variables or configurations

## Installation & Setup

### Step 1: Install Coolify CLI

If the CLI is not already installed, use the bundled installation script:

```bash
bash scripts/install_coolify_cli.sh
```

This installs to `~/.local/bin/coolify`. Ensure this directory is in the user's PATH:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

Add this line to the user's shell configuration file (`~/.bashrc`, `~/.zshrc`, etc.) for persistence.

### Step 2: Configure Context

Add the user's Coolify instance:

```bash
coolify context add <context-name> <coolify-url> <api-token>
```

Example:
```bash
coolify context add production https://coolify.example.com YOUR_API_TOKEN
```

### Step 3: Verify Connection

```bash
coolify context verify
```

This confirms successful authentication and connectivity.

### Health Check

Run the bundled health check script:

```bash
bash scripts/check_health.sh
```

This displays:
- CLI version
- Configured contexts
- Connection status
- Available resources
- Server status

## Diagnosing Issues

### Workflow Decision Tree

When a user reports an issue:

1. **Is it service availability?**
   - Site is down → Check service status
   - Container not responding → Check logs
   - Deploy failed → Check deployment history

2. **Is it WordPress-specific?**
   - 500 error after .htaccess change → Fix .htaccess
   - REST API warnings → Diagnose REST API
   - PHP limits → Update PHP configuration
   - SSL issues → Check certificates

3. **Is it performance/configuration?**
   - Need to change env vars → Manage environment
   - Need to scale → Manage resources
   - Need to deploy → Trigger deployment

### Check Service Status

```bash
# List all resources with status
coolify resource list

# Get detailed service info
coolify service get SERVICE_UUID

# Check specific application
coolify app get APP_UUID
```

Status indicators:
- `running:healthy` - Service is operational
- `running:unhealthy` - Service has issues (check logs)
- `stopped` - Service is not running
- `deploying` - Deployment in progress

### Check Logs

```bash
# Application logs
coolify app logs APP_UUID

# Get more lines
coolify app logs APP_UUID --lines 500
```

For services with multiple components (like WordPress with database), get the service details first to identify component UUIDs:

```bash
coolify service get SERVICE_UUID --format json
```

Then extract application/database UUIDs from the JSON output.

### Using the API Directly

When CLI doesn't provide needed functionality, use direct API calls. Reference: `references/api_endpoints.md`

Example - Get detailed service configuration:
```bash
curl -H "Authorization: Bearer API_TOKEN" \
  https://coolify-instance.com/api/v1/services/SERVICE_UUID
```

## Managing Services

### Start/Stop/Restart

```bash
# Services
coolify service start SERVICE_UUID
coolify service stop SERVICE_UUID
coolify service restart SERVICE_UUID

# Applications
coolify app start APP_UUID
coolify app stop APP_UUID
coolify app restart APP_UUID

# Databases
coolify database start DB_UUID
coolify database stop DB_UUID
coolify database restart DB_UUID
```

### Deploy Applications

```bash
# Deploy by UUID
coolify deploy APP_UUID

# Check deployment status
coolify deploy list APP_UUID
```

### Manage Environment Variables

```bash
# List env vars
coolify app env list APP_UUID

# Add/update env var
coolify app env set APP_UUID VAR_NAME "value"

# Delete env var
coolify app env delete APP_UUID VAR_NAME

# Restart to apply changes
coolify app restart APP_UUID
```

## WordPress Troubleshooting

For WordPress-specific issues, reference: `references/wordpress_fixes.md`

### Accessing WordPress Container

**Via Coolify Web Terminal** (Recommended):
1. Navigate to Coolify dashboard
2. Go to WordPress service
3. Click "Terminal" in sidebar
4. Select "wordpress" container

**Via Docker** (if SSH access available):
```bash
docker exec -it CONTAINER_NAME bash
```

WordPress files are located at: `/var/www/html/`

### Common WordPress Issues

#### Site Down After .htaccess Edit

This is a critical issue that requires immediate action:

1. Access the container terminal (see above)
2. Check the .htaccess file:
   ```bash
   cd /var/www/html
   cat .htaccess
   ```
3. Identify problematic line (usually last added line)
4. Remove problematic line:
   ```bash
   sed -i '$d' /var/www/html/.htaccess
   ```
5. Service should recover immediately

#### PHP Configuration Limits

To increase PHP limits (max_input_vars, upload limits, etc.):

**Correct syntax** (no `=` sign, use space):
```bash
echo "php_value max_input_vars 3000" >> /var/www/html/.htaccess
echo "php_value upload_max_filesize 64M" >> /var/www/html/.htaccess
echo "php_value post_max_size 128M" >> /var/www/html/.htaccess
echo "php_value memory_limit 256M" >> /var/www/html/.htaccess
```

Verify:
```bash
tail -5 /var/www/html/.htaccess
```

#### REST API False Positives

If Site Health reports REST API unavailable but the site works normally:

1. Test REST API externally:
   ```bash
   curl https://site.com/wp-json/
   ```

2. If JSON returns, it's a **false positive** - the API works fine

3. Common cause: Site Health loopback test is blocked, not the actual API

4. Verify HTTP_AUTHORIZATION in .htaccess:
   ```bash
   grep "HTTP_AUTHORIZATION" /var/www/html/.htaccess
   ```

   Should contain:
   ```
   RewriteRule .* - [E=HTTP_AUTHORIZATION:%{HTTP:Authorization}]
   ```

For detailed WordPress troubleshooting steps, load `references/wordpress_fixes.md` into context.

### SSL Certificate Issues

Check certificate status:
```bash
echo | openssl s_client -servername domain.com -connect domain.com:443 2>/dev/null | openssl x509 -noout -dates -subject -issuer
```

Coolify uses Traefik with Let's Encrypt for automatic SSL. Certificates auto-renew before expiration.

If certificate is invalid:
1. Check Coolify dashboard → Service → Domains
2. Regenerate SSL certificate
3. Verify Traefik labels in service configuration

## Advanced Operations

### Working with Multiple Contexts

Switch between Coolify instances:

```bash
# List contexts
coolify context list

# Switch context
coolify context use staging

# Perform operations
coolify deploy APP_UUID

# Switch back
coolify context use production
```

### Batch Operations with JSON Output

Use `--format json` with tools like `jq`:

```bash
# Get all unhealthy services
coolify resource list --format json | jq '.[] | select(.status | contains("unhealthy"))'

# Get all running applications
coolify resource list --format json | jq '.[] | select(.type=="application" and .status=="running")'

# Extract service UUIDs
coolify service list --format json | jq -r '.[].uuid'
```

### Server Management

```bash
# List servers with IPs/ports
coolify server list -s

# Validate server connection
coolify server validate SERVER_UUID

# Get server domains
coolify server domains SERVER_UUID
```

### Backup and Recovery

```bash
# List databases
coolify database list

# Backup database
coolify database backup DB_UUID

# List backups
coolify database backups DB_UUID
```

## References

This skill includes comprehensive reference documentation:

### CLI Commands Reference
Load `references/cli_commands.md` when the user needs detailed CLI command syntax, flags, or examples.

### API Endpoints Reference
Load `references/api_endpoints.md` when performing direct API calls or when CLI doesn't support the needed operation.

### WordPress Fixes Reference
Load `references/wordpress_fixes.md` when troubleshooting WordPress-specific issues like .htaccess problems, PHP configuration, REST API issues, or SSL certificates.

## Common Patterns

### Pattern: Service is Down

1. Check status: `coolify resource list`
2. Get details: `coolify service get UUID`
3. Check logs: `coolify app logs APP_UUID`
4. Identify issue from logs
5. Fix (restart, update config, fix files)
6. Verify: `coolify resource list`

### Pattern: WordPress Site Issues

1. Access container terminal (via Coolify dashboard)
2. Navigate to `/var/www/html`
3. Check `.htaccess` for syntax errors
4. Test REST API: `curl https://site.com/wp-json/`
5. Check PHP configuration if needed
6. Restart service if changes made

### Pattern: Deployment Issues

1. List recent deployments: `coolify deploy list APP_UUID`
2. Get deployment details: `coolify deploy get DEPLOY_UUID`
3. Check application logs: `coolify app logs APP_UUID`
4. Fix identified issues (env vars, config, code)
5. Trigger new deployment: `coolify deploy APP_UUID`

## Troubleshooting This Skill

### CLI Not Found

Ensure `~/.local/bin` is in PATH:
```bash
echo $PATH | grep ".local/bin"
```

If not found:
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Add to shell config for persistence.

### Connection Failures

1. Verify API token is valid (check Coolify dashboard)
2. Check Coolify instance URL is correct
3. Test manual connection:
   ```bash
   curl -H "Authorization: Bearer TOKEN" https://instance.com/api/v1/version
   ```
4. Re-configure context if needed

### Permission Issues

Ensure API token has required permissions:
- Read access for status/logs
- Write access for deployments/restarts
- Deploy access for triggering deployments

Check token permissions in Coolify dashboard at `/security/api-tokens`.
