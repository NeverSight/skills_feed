---
name: ddev
description: "DDEV local development environment guidance for Docker-based PHP/Node projects. Use when: (1) running CLI tools (composer, npm, wp, drush, artisan, console, etc.) in a DDEV project, (2) executing commands inside DDEV containers, (3) working in a subdirectory of a DDEV project (e.g., wp-content/plugins/my-plugin), (4) managing databases, snapshots, or project lifecycle with DDEV, (5) any task involving ddev exec, ddev ssh, or ddev start/stop."
---

# DDEV

DDEV is a Docker-based local development tool for PHP/Node projects. It wraps common CLI tools (composer, npm, wp, drush, etc.) so they run inside containers without requiring local installation. Full docs: https://docs.ddev.com

## CLI Syntactic Sugar

DDEV provides shortcut commands that proxy to container-internal tools. Use these instead of `ddev exec`:

```
ddev composer install          # runs composer inside the container
ddev npm run build             # runs npm inside the container
ddev wp plugin list            # runs wp-cli (WordPress only)
ddev drush cr                  # runs drush (Drupal only)
ddev artisan migrate           # runs artisan (Laravel only)
ddev console cache:clear       # runs bin/console (Symfony only)
ddev yarn add <pkg>            # runs yarn inside the container
ddev php -v                    # runs PHP inside the container
```

For the full list of shortcuts and their mappings, run `ddev help`.

## DDEV Commands Work from Any Subdirectory

DDEV automatically detects its project root from any subdirectory within the project tree. Most DDEV commands work out of the box regardless of where the shell is located:

```bash
ddev wp plugin list
ddev mailpit
ddev db
ddev composer show
ddev npm ls
ddev drush cr
ddev start
ddev describe
ddev ssh
```

No special flags or path resolution is needed for these commands.

## When `--dir` Scoping IS Required

The `--dir` flag is only needed when running **file-path-sensitive scripts** via `ddev exec` that must target a specific subdirectory inside the container. This applies when the command operates on files relative to the working directory (e.g., `composer install` reading a specific `composer.json`, or `npm install` reading a specific `package.json`).

### Step 1: Resolve the container path

Run the bundled resolve script to map the host subdirectory to a container path:

```bash
scripts/resolve-ddev-root.sh "$(pwd)"
```

Output (JSON):
```json
{
  "project_root": "/Users/you/Projects/mysite",
  "container_path": "/var/www/html/wp-content/plugins/my-plugin",
  "relative_path": "wp-content/plugins/my-plugin",
  "project_name": "mysite"
}
```

- `relative_path` **empty** -- working directory is the DDEV root, no `--dir` needed.
- `relative_path` **non-empty** -- use `--dir` with the `container_path` value for file-path-sensitive commands.

### Step 2: Execute the scoped command

If DDEV is not running, start it first with `ddev start`.

```bash
# Install dependencies scoped to a plugin subdirectory
ddev exec --dir="/var/www/html/wp-content/plugins/my-plugin" bash -c "composer install"
ddev exec --dir="/var/www/html/wp-content/plugins/my-plugin" bash -c "npm install"

# Run a script that reads files relative to the working directory
ddev exec --dir="/var/www/html/wp-content/plugins/my-plugin" bash -c "phpunit"
```

Without `--dir`, these commands run at the container docroot (`/var/www/html`) and operate on the wrong `composer.json`, `package.json`, or project context.

## Running Commands in Containers

Use `ddev exec` when no shortcut exists or when you need to target a specific container directory:

```bash
# Runs in web container at docroot
ddev exec ls -la

# Scope to a subdirectory for file-path-sensitive operations
ddev exec --dir="/var/www/html/wp-content/plugins/my-plugin" bash -c "composer install"

# Run in the database container
ddev exec -s db mysql -e "SHOW DATABASES"

# Shorthand alias
ddev . ls -la
```

## Subpath Mapping (for `ddev exec --dir`)

Path resolution is only needed when using `ddev exec --dir` to scope file-path-sensitive scripts to a subdirectory. Standard DDEV commands (`ddev wp`, `ddev mailpit`, `ddev db`, `ddev start`, etc.) do **not** require this -- they work from any subdirectory automatically.

### Resolving the DDEV Root

Use the bundled resolve script to find the DDEV project root and compute the container path:

```bash
# From any subdirectory within a DDEV project
scripts/resolve-ddev-root.sh /path/to/wp-content/plugins/my-plugin
```

The script walks up the directory tree looking for `.ddev/config.yaml`. If no argument is provided, it uses the current working directory.

### Manual Path Computation

If the script is unavailable, compute the path manually:

1. Find the directory containing `.ddev/config.yaml` (the DDEV project root)
2. Compute the relative path from that root to the current working directory
3. Prepend `/var/www/html/` to get the container path

## Project Information

Use `ddev describe` to get detailed information about the current DDEV project. Add the `-j` flag to get structured JSON output:

```bash
ddev describe -j
```

This provides useful details such as:
- **Project type** (wordpress, drupal, laravel, etc.)
- **Primary URL** and all project URLs
- **PHP version** and **Node.js version**
- **Database type and version** (mariadb, mysql, postgres)
- **Web server type** (nginx-fpm, apache-fpm)
- **Service status** for web, db, and additional services
- **Published ports** for host-to-container mapping

Example JSON output fields:
- `type` - Project type (wordpress, drupal, etc.)
- `primary_url` - Main project URL
- `urls` - Array of all project URLs (HTTP and HTTPS)
- `php_version` - PHP version in use
- `nodejs_version` - Node.js version in use
- `database_type` - Database type (mariadb, mysql, postgres)
- `webserver_type` - Web server (nginx-fpm, apache-fpm)
- `services` - Status and details for each service

## Resources

### scripts/
- **resolve-ddev-root.sh** - Walks up the directory tree to find the DDEV project root from any subdirectory. Returns JSON with project root, container path, relative path, and project name.

### references/
- **npm-projects.md** - Running npm/Node.js dev servers in DDEV, including port exposure, host binding, and framework-specific examples for Vite, Next.js, and Astro.
- **wordpress-multisite.md** - Setup guide for WordPress Multisite with DDEV, covering subdomains, different hostnames, and subdirectory configurations with WP-CLI commands.
