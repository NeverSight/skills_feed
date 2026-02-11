---
name: bench-commands
description: Frappe Bench CLI command reference for site management, app management, development, and production operations. Use when running bench commands, managing sites, migrations, builds, or deployments.
---

# Bench CLI Commands Reference

Complete reference for the Frappe Bench command-line interface for managing Frappe/ERPNext installations.

## When to Use This Skill

- Running bench commands for development
- Managing Frappe sites
- Installing and updating apps
- Running migrations and builds
- Setting up production environments
- Troubleshooting common issues

## Bench Directory Structure

```
frappe-bench/
├── apps/                   # Frappe apps
│   ├── frappe/            # Core framework
│   ├── erpnext/           # ERPNext (if installed)
│   └── my_app/            # Custom apps
├── sites/                  # Sites directory
│   ├── common_site_config.json
│   ├── apps.txt           # List of installed apps
│   └── my_site.local/     # Individual site
│       ├── site_config.json
│       ├── private/
│       └── public/
├── config/                 # Configuration files
├── logs/                   # Log files
├── env/                    # Python virtual environment
└── node_modules/          # Node.js dependencies
```

## Site Management

### Create Site
```bash
# Create new site
bench new-site mysite.local

# With specific database
bench new-site mysite.local --db-name mysite_db

# With MariaDB root password
bench new-site mysite.local --mariadb-root-password mypassword

# With admin password
bench new-site mysite.local --admin-password admin123

# From SQL file
bench new-site mysite.local --source_sql /path/to/backup.sql

# Skip creating default user
bench new-site mysite.local --no-mariadb-socket
```

### Use Site
```bash
# Set default site
bench use mysite.local

# Run command on specific site
bench --site mysite.local migrate

# Run on all sites
bench --site all migrate
```

### Site Operations
```bash
# List all sites
bench list-sites

# Drop site (delete)
bench drop-site mysite.local

# Drop with force
bench drop-site mysite.local --force

# Set site maintenance mode
bench --site mysite.local set-maintenance-mode on
bench --site mysite.local set-maintenance-mode off

# Disable scheduler
bench --site mysite.local disable-scheduler
bench --site mysite.local enable-scheduler
```

### Backup & Restore
```bash
# Backup site
bench --site mysite.local backup

# Backup with files
bench --site mysite.local backup --with-files

# Backup all sites
bench --site all backup

# Restore from backup
bench --site mysite.local restore /path/to/backup.sql.gz

# Restore with files
bench --site mysite.local restore /path/to/backup.sql.gz \
  --with-private-files /path/to/private.tar \
  --with-public-files /path/to/public.tar
```

## App Management

### Get Apps
```bash
# Get app from GitHub
bench get-app https://github.com/frappe/erpnext

# Get specific branch
bench get-app https://github.com/frappe/erpnext --branch version-14

# Get specific tag
bench get-app https://github.com/frappe/erpnext --tag v14.0.0

# Get from local path
bench get-app /path/to/my_app

# Get and install on all sites
bench get-app erpnext --install-all
```

### Install/Uninstall Apps
```bash
# Install app on site
bench --site mysite.local install-app erpnext

# Install app on all sites
bench --site all install-app my_app

# Uninstall app
bench --site mysite.local uninstall-app my_app

# Uninstall with force (removes data)
bench --site mysite.local uninstall-app my_app --yes --force
```

### Create New App
```bash
# Create new app
bench new-app my_app

# App will be created in apps/ directory with:
# - my_app/my_app/
# - hooks.py
# - modules.txt
# - patches.txt
# - requirements.txt
```

### Update Apps
```bash
# Update all apps
bench update

# Update without migrations
bench update --no-migrations

# Update specific app
bench update --apps erpnext

# Update without pulling
bench update --no-pull

# Update without building assets
bench update --no-build

# Reset to fresh install
bench update --reset
```

### Remove App
```bash
# Remove app from bench (not from sites)
bench remove-app my_app

# Remove from site first
bench --site mysite.local uninstall-app my_app
bench remove-app my_app
```

## Development Commands

### Start Development Server
```bash
# Start development server (web + redis + scheduler)
bench start

# Start with specific workers
bench start --procfile Procfile.dev

# Start only web server
bench serve

# Start on specific port
bench serve --port 8001
```

### Build Assets
```bash
# Build assets (JS/CSS)
bench build

# Build specific app
bench build --app my_app

# Build with verbose output
bench build --verbose

# Build production assets
bench build --production

# Build and minify
bench build --make-copy

# Watch for changes
bench watch
```

### Migrate
```bash
# Run migrations
bench --site mysite.local migrate

# Migrate all sites
bench --site all migrate

# Migrate specific app
bench --site mysite.local migrate --app my_app

# Skip failing patches
bench --site mysite.local migrate --skip-failing
```

### Clear Cache
```bash
# Clear cache
bench --site mysite.local clear-cache

# Clear all cache including redis
bench --site mysite.local clear-website-cache

# Clear redis cache
bench clear-redis-cache
```

### Console
```bash
# Open Python console
bench --site mysite.local console

# In console:
# >>> doc = frappe.get_doc("Customer", "CUST-001")
# >>> doc.customer_name
# >>> frappe.db.sql("SELECT * FROM tabCustomer")

# Run Python script
bench --site mysite.local execute myapp.scripts.my_function

# Execute with arguments
bench --site mysite.local execute myapp.scripts.my_function --args='["arg1", "arg2"]'
```

### MariaDB Console
```bash
# Open MariaDB console
bench --site mysite.local mariadb

# Run SQL query
bench --site mysite.local mariadb -e "SELECT * FROM tabCustomer LIMIT 5"
```

### Run Tests
```bash
# Run all tests
bench --site mysite.local run-tests

# Run tests for specific app
bench --site mysite.local run-tests --app my_app

# Run specific test
bench --site mysite.local run-tests --module my_app.my_module.doctype.my_doctype.test_my_doctype

# Run with coverage
bench --site mysite.local run-tests --coverage

# Run specific test class
bench --site mysite.local run-tests --doctype "My DocType"

# Run parallel tests
bench --site mysite.local run-tests --parallel

# Skip test setup
bench --site mysite.local run-tests --skip-setup
```

### Translation
```bash
# Update translation files
bench --site mysite.local update-translations

# Export translations
bench --site mysite.local export-translations

# Import translations
bench --site mysite.local import-translations /path/to/translations.csv
```

## Production Setup

### Setup Production
```bash
# Setup for production (systemd, nginx, supervisor)
sudo bench setup production frappe-user

# Setup supervisor
bench setup supervisor

# Setup systemd
bench setup systemd

# Setup nginx
bench setup nginx

# Setup Redis
bench setup redis

# Setup fail2ban
bench setup fail2ban
```

### SSL/Let's Encrypt
```bash
# Setup Let's Encrypt SSL
sudo bench setup lets-encrypt mysite.local

# Renew certificates
sudo bench renew-lets-encrypt
```

### Restart Services
```bash
# Restart supervisor
sudo supervisorctl restart all

# Restart specific
sudo supervisorctl restart frappe-bench-web:*
sudo supervisorctl restart frappe-bench-workers:*

# Restart systemd
sudo systemctl restart frappe-bench-web
sudo systemctl restart frappe-bench-schedule

# Check status
sudo supervisorctl status
```

## Scheduler & Workers

### Scheduler
```bash
# Enable scheduler
bench --site mysite.local enable-scheduler

# Disable scheduler
bench --site mysite.local disable-scheduler

# Check scheduler status
bench --site mysite.local show-scheduler-status

# Run specific scheduled job
bench --site mysite.local execute frappe.tasks.run_daily
```

### Background Jobs
```bash
# Show queued jobs
bench --site mysite.local show-pending-jobs

# Clear failed jobs
bench --site mysite.local clear-website-cache

# Run specific queue
bench worker --queue default
bench worker --queue short
bench worker --queue long

# Purge jobs
bench --site mysite.local purge-jobs
```

## Configuration

### Site Config
```bash
# Show site config
bench --site mysite.local show-config

# Set config value
bench --site mysite.local set-config key value

# Set config with JSON value
bench --site mysite.local set-config limits '{"users": 10}'

# Set common config (all sites)
bench set-config key value

# Remove config
bench --site mysite.local remove-config key
```

### Common Configurations
```python
# site_config.json
{
    "db_name": "mysite_db",
    "db_password": "password",
    "db_type": "mariadb",
    "encryption_key": "xxxxx",
    "developer_mode": 0,
    "maintenance_mode": 0,
    "pause_scheduler": 0,
    "mail_server": "smtp.gmail.com",
    "mail_port": 587,
    "use_tls": 1,
    "mail_login": "user@gmail.com",
    "mail_password": "password",
    "auto_email_id": "noreply@mysite.com",
    "mute_emails": 0,
    "enable_scheduler": 1,
    "limits": {
        "users": 10,
        "emails": 500,
        "space": 5120
    }
}
```

### Bench Config
```bash
# Show bench config
bench config list

# Set bench config
bench config set serve_port 8001
bench config set redis_cache_port 13000

# Common bench configs
bench config set developer_mode 1
bench config set webserver_port 8000
bench config set background_workers 1
```

## Troubleshooting Commands

### Logs
```bash
# View logs
tail -f logs/frappe.log
tail -f logs/web.error.log
tail -f logs/worker.error.log
tail -f logs/scheduler.error.log

# Site-specific logs
tail -f sites/mysite.local/logs/frappe.log
```

### Debug
```bash
# Check site health
bench --site mysite.local doctor

# Show database stats
bench --site mysite.local show-db-size

# Show table sizes
bench --site mysite.local --db-type mariadb execute \
  "SELECT table_name, data_length FROM information_schema.tables WHERE table_schema = 'mysite_db'"

# Check scheduled jobs
bench --site mysite.local show-scheduler-status

# Reset password
bench --site mysite.local set-admin-password newpassword

# Add system manager
bench --site mysite.local add-system-manager user@example.com
```

### Fix Common Issues
```bash
# Rebuild search index
bench --site mysite.local build-search-index

# Reset desk customizations
bench --site mysite.local reset-perms

# Clear all locks
bench --site mysite.local clear-locks

# Reinstall
bench --site mysite.local reinstall --yes

# Partial restore
bench --site mysite.local partial-restore /path/to/backup.sql
```

## Version Management

```bash
# Check versions
bench version

# Switch branch
bench switch-to-branch version-14 frappe erpnext

# Switch to develop
bench switch-to-branch develop --upgrade

# Set version
bench set-bench-version 5.x
```

## Multi-Tenancy

```bash
# Setup multi-tenancy
bench config dns_multitenant on

# Add domain to site
bench --site mysite.local add-domain newdomain.com

# Remove domain
bench --site mysite.local remove-domain newdomain.com

# Setup wildcard SSL
sudo certbot certonly --webroot -w /var/www/letsencrypt -d *.mydomain.com
```

## Common Workflows

### Fresh Install
```bash
# Install bench
pip install frappe-bench

# Initialize bench
bench init frappe-bench
cd frappe-bench

# Get ERPNext
bench get-app erpnext

# Create site
bench new-site mysite.local

# Install ERPNext
bench --site mysite.local install-app erpnext

# Start development server
bench start
```

### Daily Development
```bash
# Pull latest changes
bench update --no-backup

# Or step by step:
cd apps/frappe && git pull
cd apps/erpnext && git pull
bench update --no-pull

# Clear cache after code changes
bench --site mysite.local clear-cache

# Build assets
bench build --app my_app
```

### Deploy Update
```bash
# On production server
cd /home/frappe/frappe-bench

# Set maintenance mode
bench --site mysite.local set-maintenance-mode on

# Backup
bench --site mysite.local backup --with-files

# Update
bench update

# Migrate
bench --site mysite.local migrate

# Build assets
bench build --production

# Clear cache
bench --site mysite.local clear-cache

# Restart
sudo supervisorctl restart all

# Disable maintenance mode
bench --site mysite.local set-maintenance-mode off
```
