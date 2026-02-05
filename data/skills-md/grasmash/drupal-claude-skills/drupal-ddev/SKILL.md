---
name: drupal-ddev
description: DDEV local development environment patterns for Drupal, including configuration, commands, database management, debugging tools, and performance optimization.
---

# DDEV for Drupal Development

Comprehensive patterns for using DDEV as your local Drupal development environment, including setup, configuration, workflow optimization, and troubleshooting.

## When This Skill Activates

Activates when working with DDEV local development including:
- DDEV configuration (.ddev/config.yaml)
- Local environment setup and management
- Database import/export operations
- Drush integration
- Xdebug and debugging tools
- Performance optimization
- Multi-site and custom commands

---

## Available Topics

### Core Setup
- @references/installation.md - Installing and configuring DDEV
- @references/config-yaml.md - .ddev/config.yaml reference
- @references/commands.md - Essential DDEV commands

### Database Operations
- @references/database.md - Import, export, and snapshot workflows
- @references/drush.md - Using Drush with DDEV

### Development Tools
- @references/xdebug.md - Debugging with Xdebug
- @references/mailhog.md - Email testing with MailHog
- @references/solr.md - Local Solr search setup

### Advanced
- @references/custom-commands.md - Creating project-specific commands
- @references/hooks.md - Pre/post hooks automation
- @references/performance.md - Optimizing DDEV performance
- @references/multisite.md - Multi-site configuration

See `/references/` directory for complete documentation.

---

## Quick Reference

### Essential Commands

```bash
# Start project
ddev start

# Stop project
ddev stop

# Restart services
ddev restart

# SSH into web container
ddev ssh

# Run Drush commands
ddev drush cr
ddev drush status
ddev drush config:status

# Run Composer
ddev composer require drupal/module_name
ddev composer update

# Database operations
ddev import-db --file=backup.sql.gz
ddev export-db --file=backup.sql.gz
ddev snapshot

# View logs
ddev logs
ddev logs -f    # Follow mode

# Describe project
ddev describe

# Access URLs
ddev launch     # Open site in browser
```

### Basic .ddev/config.yaml

```yaml
name: myproject
type: drupal10
docroot: web
php_version: "8.3"
webserver_type: nginx-fpm
database:
  type: mariadb
  version: "10.6"
nodejs_version: "20"

# Additional services
additional_services:
  - solr

# Custom upload/execution limits
upload_dirs:
  - web/sites/default/files

# Performance settings
performance_mode: mutagen  # For macOS
```

---

## Common Workflows

### New Drupal Project

```bash
# Create project directory
mkdir myproject && cd myproject

# Initialize DDEV
ddev config --project-type=drupal10 --docroot=web --php-version=8.3

# Install Drupal via Composer
ddev composer create drupal/recommended-project

# Install Drush
ddev composer require drush/drush

# Start DDEV
ddev start

# Install Drupal
ddev drush site:install standard --site-name="My Site" --account-name=admin

# Launch site
ddev launch
```

### Import Existing Project

```bash
# Clone repository
git clone repo-url myproject && cd myproject

# Start DDEV (reads .ddev/config.yaml)
ddev start

# Install dependencies
ddev composer install

# Import database
ddev import-db --file=path/to/backup.sql.gz

# Import files (if needed)
ddev import-files --source=/path/to/files

# Run updates
ddev drush updb -y
ddev drush cr

# Launch
ddev launch
```

### Database Sync from Remote

```bash
# Get database backup from remote server
# Method 1: Via SSH and drush sql-dump
ssh user@remote.server "cd /path/to/drupal && drush sql-dump --gzip" > backup.sql.gz

# Method 2: Via platform-specific tools or download existing backup
# (depends on your hosting platform)

# Import to local DDEV
ddev import-db --file=backup.sql.gz

# Run updates
ddev drush updb -y
ddev drush cr

# Sanitize for local development (optional)
ddev drush sql-sanitize -y
```

### Daily Development Workflow

```bash
# Morning: Start project
ddev start

# Pull latest code
git pull origin main

# Update dependencies if needed
ddev composer install

# Clear cache
ddev drush cr

# Work on features...

# Create database snapshot before testing
ddev snapshot --name=before-testing

# Test changes...

# If needed, restore snapshot
ddev snapshot restore --name=before-testing

# Evening: Stop project
ddev stop
```

---

## Debugging with Xdebug

```bash
# Enable Xdebug
ddev xdebug on

# Run your debugger in IDE (PHPStorm, VSCode)
# Set breakpoints and refresh page

# Disable when done (improves performance)
ddev xdebug off

# Check Xdebug status
ddev xdebug status
```

**VSCode launch.json**:
```json
{
  "name": "Listen for Xdebug",
  "type": "php",
  "request": "launch",
  "port": 9003,
  "pathMappings": {
    "/var/www/html": "${workspaceFolder}"
  }
}
```

---

## Performance Optimization

### macOS Performance (Mutagen)

```yaml
# .ddev/config.yaml
performance_mode: mutagen
```

```bash
# Restart after config change
ddev restart
```

### NFS Mount (Alternative for macOS)

```yaml
# .ddev/config.yaml
nfs_mount_enabled: true
```

### Database Tuning

```yaml
# .ddev/config.yaml
database:
  type: mariadb
  version: "10.6"

# Create .ddev/mysql/my.cnf
[mysqld]
innodb_buffer_pool_size = 512M
innodb_log_file_size = 128M
```

---

## Custom Commands

Create project-specific commands in `.ddev/commands/web/`:

**Example**: `.ddev/commands/web/fresh-install`
```bash
#!/bin/bash
## Description: Fresh Drupal install from scratch
## Usage: fresh-install
## Example: ddev fresh-install

set -e

echo "Installing fresh Drupal site..."

# Drop existing database
drush sql-drop -y

# Install Drupal
drush site:install standard \
  --site-name="My Site" \
  --account-name=admin \
  --account-pass=admin \
  -y

# Import config if exists
if [ -d /var/www/html/config/default ]; then
  drush config:import -y
fi

# Clear cache
drush cr

echo "Fresh install complete!"
echo "Login: admin / admin"
```

Make it executable:
```bash
chmod +x .ddev/commands/web/fresh-install
ddev fresh-install
```

---

## Best Practices

1. **Commit .ddev/config.yaml** - Share config with team
2. **Use ddev composer** instead of local composer
3. **Don't commit database snapshots** - Too large
4. **Create snapshots before risky operations**
5. **Disable Xdebug when not debugging** - Performance impact
6. **Use mutagen on macOS** - Much faster file sync
7. **Regular ddev poweroff** - Free up system resources
8. **Version pin services** - PHP, database, Node.js
9. **Use hooks for automation** - Post-start tasks
10. **Document custom commands** - Help team members

---

## Common Issues

### Site Not Loading

```bash
# Restart project
ddev restart

# Check status
ddev describe

# View logs
ddev logs

# Clear Drupal cache
ddev drush cr
```

### Database Connection Error

```bash
# Check database is running
ddev describe

# Verify settings.php or settings.ddev.php exists
ddev ssh
ls web/sites/default/settings*.php
```

### Port Conflicts

```bash
# Stop all DDEV projects
ddev poweroff

# Check for port conflicts
lsof -i :80 -i :443

# Change router HTTP port if needed
ddev config --router-http-port=8080 --router-https-port=8443
```

### Slow Performance on macOS

```bash
# Enable mutagen
ddev config --performance-mode=mutagen
ddev restart

# Or use NFS
ddev config --nfs-mount-enabled=true
ddev restart
```

---

## Multi-Project Management

```bash
# List all projects
ddev list

# Stop all projects
ddev poweroff

# Remove stopped projects
ddev delete <project-name>

# Remove all project containers (keep files)
ddev delete --omit-snapshot --yes <project-name>
```

---

## Related Skills

- @drupal-config-mgmt - Config management workflows
- @drupal-contrib-mgmt - Module management with Composer
- @drupal-at-your-fingertips - General Drupal patterns

---

**Official Documentation**: https://ddev.readthedocs.io
**Drupal DDEV Quickstart**: https://ddev.readthedocs.io/en/stable/users/quickstart/
**Community Support**: https://discord.gg/5wjP76mBJD
