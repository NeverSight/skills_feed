---
name: typo3-ddev
description: Best practices for TYPO3 local development with DDEV, including configuration, database management, multi-version testing, and common workflows for v13/v14.
version: 2.1.0
typo3_compatibility: "13.0 - 14.x"
triggers:
  - ddev
  - local
  - development
  - docker
  - environment
  - multi-version
---

# TYPO3 DDEV Local Development

> **Compatibility:** TYPO3 v13.x and v14.x (v14 preferred)
> All configurations in this skill support both TYPO3 v13 and v14.

## Container Priority

**Always check for existing containers first:**

1. Check `.ddev/` exists → use `ddev exec`
2. Check `docker-compose.yml` exists → use `docker compose exec`
3. Only use system tools if no container environment

> **Critical**: Use the project's configured PHP version, not system PHP.

## 1. Project Initialization

### New TYPO3 Project (v14 - Preferred)

```bash
# Create project directory
mkdir my-typo3-project && cd my-typo3-project

# Initialize DDEV with TYPO3 preset
ddev config --project-type=typo3 --docroot=public --php-version=8.3

# Start the environment
ddev start

# Install TYPO3 v14 (preferred)
ddev composer create "typo3/cms-base-distribution:^14"

# Run TYPO3 setup
ddev typo3 setup
```

### New TYPO3 Project (v13 LTS)

```bash
# Create project directory
mkdir my-typo3-project && cd my-typo3-project

# Initialize DDEV with TYPO3 preset
ddev config --project-type=typo3 --docroot=public --php-version=8.2

# Start the environment
ddev start

# Install TYPO3 v13 LTS
ddev composer create "typo3/cms-base-distribution:^13"

# Run TYPO3 setup
ddev typo3 setup
```

### Existing TYPO3 Project

```bash
# Clone repository
git clone git@github.com:org/project.git
cd project

# Configure DDEV (if not already)
ddev config --project-type=typo3 --docroot=public --php-version=8.3

# Start and install dependencies
ddev start
ddev composer install

# Import database (see Database Operations)
```

## 2. Recommended Configuration

### `.ddev/config.yaml` (v13/v14 Compatible)

```yaml
name: my-typo3-project
type: typo3
docroot: public
php_version: "8.3"    # 8.2 minimum for v13, 8.3 recommended for v14
webserver_type: nginx-fpm
database:
  type: mariadb
  version: "10.11"    # 10.11+ or 11.x recommended for both v13/v14

# Fixed port for external tools (MySQL MCP, etc.)
host_db_port: "33060"
host_webserver_port: "8080"
host_https_port: "8443"

# Enable Mailpit for email testing (replaced Mailhog in newer DDEV)
mailpit_http_port: "8025"

# PHP settings
web_environment:
  - TYPO3_CONTEXT=Development
  - PHP_IDE_CONFIG=serverName=my-typo3-project.ddev.site

# Additional services
hooks:
  post-start:
    - exec: composer install --no-interaction
```

### `.ddev/config.local.yaml` (Personal Overrides)

```yaml
# Personal machine-specific overrides (gitignored)
host_db_port: "33061"  # If 33060 conflicts
```

### PHP Version Matrix

| TYPO3 Version | Minimum PHP | Recommended PHP | MariaDB |
|---------------|-------------|-----------------|---------|
| v13.4 LTS     | 8.2         | 8.3             | 10.11+  |
| v14.x         | 8.2         | 8.3 / 8.4       | 10.11+  |

## 3. Database Operations

### Import Database

```bash
# From SQL file
ddev import-db --file=dump.sql

# From gzipped file
ddev import-db --file=dump.sql.gz

# From remote (via SSH)
ssh user@server "mysqldump -u root dbname | gzip" | gunzip | ddev import-db
```

### Export Database

```bash
# Standard export
ddev export-db --file=backup.sql.gz

# Without gzip
ddev export-db --gzip=false --file=backup.sql
```

### Database Snapshots

```bash
# Create snapshot before risky operation
ddev snapshot --name=before-upgrade

# List snapshots
ddev snapshot --list

# Restore snapshot
ddev snapshot restore before-upgrade

# Delete snapshot
ddev snapshot delete before-upgrade
```

### Direct MySQL Access

```bash
# MySQL CLI
ddev mysql

# Execute query
ddev mysql -e "SELECT uid, title FROM pages WHERE hidden = 0"

# Connect from external tool (e.g., TablePlus, DBeaver)
# Host: 127.0.0.1
# Port: 33060 (or your configured host_db_port)
# User: db
# Password: db
# Database: db
```

## 4. TYPO3 CLI Commands

### Console Commands

```bash
# List all commands
ddev typo3 list

# Clear all caches
ddev typo3 cache:flush

# Clear specific cache
ddev typo3 cache:flush --group=pages

# Update database schema
ddev typo3 database:updateschema

# Reference index
ddev typo3 referenceindex:update

# Scheduled tasks
ddev typo3 scheduler:run

# Run upgrade wizards (after version update)
ddev typo3 upgrade:list
ddev typo3 upgrade:run
```

### Extension Management

```bash
# Install extension from TER
ddev composer require typo3/cms-seo

# Install extension from Packagist
ddev composer require vendor/extension-name

# Setup extensions (generate PackageStates.php)
ddev typo3 extension:setup

# Activate extension
ddev typo3 extension:activate my_extension

# Deactivate extension
ddev typo3 extension:deactivate my_extension
```

## 5. Composer Operations

```bash
# Install dependencies
ddev composer install

# Update all dependencies
ddev composer update

# Update single package
ddev composer update typo3/cms-core --with-dependencies

# Require new package (with v13/v14 dual compatibility)
ddev composer require "vendor/package:^1.0"

# Remove package
ddev composer remove vendor/package

# Clear Composer cache
ddev composer clear-cache
```

### Dual-Version Development

For extensions supporting both v13 and v14:

```bash
# Set version constraint in extension's composer.json
ddev composer require "typo3/cms-core:^13.0 || ^14.0" --no-update
```

## 6. File Operations

### SSH into Container

```bash
# Web container (as www-data)
ddev ssh

# Web container (as root)
ddev ssh -s web -u root

# Database container
ddev ssh -s db
```

### File Sync

```bash
# Copy file into container
ddev exec cp /path/in/container /other/path

# Copy from host to container
docker cp localfile.txt ddev-myproject-web:/var/www/html/

# Download file from container
ddev exec cat /var/www/html/somefile > localfile
```

## 7. Debugging with Xdebug

### Enable/Disable

```bash
# Enable Xdebug
ddev xdebug on

# Disable Xdebug (faster performance)
ddev xdebug off

# Check status
ddev xdebug status
```

### IDE Configuration (PhpStorm/Cursor)

1. Set breakpoint in PHP file
2. Start listening for connections (PhpStorm: "Start Listening")
3. Enable Xdebug: `ddev xdebug on`
4. Trigger request in browser
5. Debugger should connect

### Xdebug Environment

```yaml
# .ddev/config.yaml
web_environment:
  - XDEBUG_MODE=debug,develop
  - XDEBUG_CONFIG=client_host=host.docker.internal
```

## 8. Multi-Site Configuration

### Additional Hostnames

```yaml
# .ddev/config.yaml
additional_hostnames:
  - site1
  - site2
additional_fqdns:
  - site1.myproject.ddev.site
  - site2.myproject.ddev.site
```

### Site Configuration

```bash
# Create site configuration
mkdir -p config/sites/site1
```

```yaml
# config/sites/site1/config.yaml
base: 'https://site1.myproject.ddev.site/'
rootPageId: 1
languages:
  - title: English
    languageId: 0
    locale: en_US.UTF-8
```

## 9. Services and Add-ons

### Common Add-ons

```bash
# Redis (for caching)
ddev get ddev/ddev-redis

# Elasticsearch
ddev get ddev/ddev-elasticsearch

# Solr
ddev get ddev/ddev-solr
```

### Custom Services

```yaml
# .ddev/docker-compose.redis.yaml
services:
  redis:
    image: redis:7-alpine
    container_name: ddev-${DDEV_SITENAME}-redis
    command: redis-server --appendonly yes
    volumes:
      - redis-data:/data
    labels:
      com.ddev.site-name: ${DDEV_SITENAME}
      com.ddev.approot: $DDEV_APPROOT

volumes:
  redis-data:
```

### Redis Caching Configuration (v13/v14)

```php
<?php
// config/system/additional.php
$GLOBALS['TYPO3_CONF_VARS']['SYS']['caching']['cacheConfigurations']['hash']['backend'] 
    = \TYPO3\CMS\Core\Cache\Backend\RedisBackend::class;
$GLOBALS['TYPO3_CONF_VARS']['SYS']['caching']['cacheConfigurations']['hash']['options'] = [
    'hostname' => 'redis',
    'port' => 6379,
    'database' => 0,
];
```

## 10. Troubleshooting

### Common Issues

```bash
# Restart everything
ddev restart

# Full reset (keeps database)
ddev stop && ddev start

# Nuclear option (removes containers **and database volume**)
ddev delete -O && ddev start

# View logs
ddev logs

# View specific service logs
ddev logs -s web
ddev logs -s db
```

### Port Conflicts

```bash
# Check what's using a port
lsof -i :80

# Use different ports in config.yaml
router_http_port: "8080"
router_https_port: "8443"
```

### Permission Issues

```bash
# Fix file permissions
ddev exec chmod -R g+w var/
ddev exec chmod -R g+w public/fileadmin/
ddev exec chmod -R g+w public/typo3temp/
```

## 11. Environment Variables

### TYPO3 Context

```bash
# Development (default in DDEV)
TYPO3_CONTEXT=Development

# Production testing
TYPO3_CONTEXT=Production

# Sub-contexts
TYPO3_CONTEXT=Development/Docker
```

### Custom Variables

```yaml
# .ddev/config.yaml
web_environment:
  - MY_API_KEY=secret123
  - FEATURE_FLAG=enabled
```

Access in TYPO3:

```php
<?php
$apiKey = getenv('MY_API_KEY');
// or
$apiKey = $_ENV['MY_API_KEY'];
```

## 12. Best Practices

### Performance

1. **Disable Xdebug** when not debugging (`ddev xdebug off`)
2. **Use snapshots** instead of full imports for quick state changes
3. **Mount with Mutagen** on macOS for better file sync performance
4. **Use PHP 8.3** for best performance on v13/v14

### Team Workflow

1. **Commit** `.ddev/config.yaml` to repository
2. **Gitignore** `.ddev/config.local.yaml` for personal overrides
3. **Document** additional setup steps in `README.md`
4. **Share** database snapshots for consistent development data

### Security

1. **Never expose** DDEV ports publicly
2. **Don't use** DDEV in production
3. **Rotate** any sensitive data in development databases

## 13. Multi-Version Testing (Extension Development)

When developing extensions that need to work across multiple TYPO3 versions:

### Setup for Multi-Version Testing

```yaml
# .ddev/config.yaml
name: my-extension
type: php
docroot: ""
php_version: "8.3"

additional_hostnames:
  - v13
  - v14
```

### Install Multiple TYPO3 Versions

```bash
# Create version-specific directories
mkdir -p v13 v14

# Install TYPO3 v13
cd v13
ddev composer create "typo3/cms-base-distribution:^13"
cd ..

# Install TYPO3 v14
cd v14
ddev composer create "typo3/cms-base-distribution:^14"
cd ..

# Symlink extension
ln -s ../../../ v13/packages/my_extension
ln -s ../../../ v14/packages/my_extension
```

### Access URLs

| Environment | URL |
|-------------|-----|
| TYPO3 v13 | `https://v13.my-extension.ddev.site/typo3/` |
| TYPO3 v14 | `https://v14.my-extension.ddev.site/typo3/` |

**Default Credentials**: admin / Joh316!

### Version-Specific Commands

```bash
# Run tests on v13
ddev exec -d /var/www/html/v13 vendor/bin/phpunit

# Run tests on v14
ddev exec -d /var/www/html/v14 vendor/bin/phpunit

# Clear cache for specific version
ddev exec -d /var/www/html/v13 vendor/bin/typo3 cache:flush
```

---

## Credits & Attribution

This skill is based on the excellent TYPO3 best practices and methodology developed by
**[Netresearch DTT GmbH](https://www.netresearch.de/)**.

Original repository: https://github.com/netresearch/typo3-ddev-skill

**Copyright (c) Netresearch DTT GmbH** - Methodology and best practices  
Adapted by webconsulting.at for this skill collection
