---
name: wp-cli
description: WordPress CLI operations for database management, plugins, themes, users, content, and site configuration. Use for migrations, bulk updates, user audits, content imports, or any wp-cli commands.
---

# WP-CLI Skill

Use this skill for WordPress command-line operations including migrations, bulk updates, database management, user audits, content imports, and site configuration.

## Prerequisites Check

Always verify WP-CLI and WordPress installation before proceeding:

```bash
wp --version                  # Check WP-CLI is installed
wp core is-installed         # Verify WordPress is present
wp core version              # Check WordPress version
```

If working in a specific directory, use `--path=/path/to/wordpress` or `cd` to the WordPress root first.

## Safety Patterns

### Always Backup Before Destructive Operations

```bash
# Database backup before major changes
wp db export backup-$(date +%Y%m%d-%H%M%S).sql

# Full site backup (database + files)
tar -czf site-backup-$(date +%Y%m%d-%H%M%S).tar.gz wp-content/ backup-*.sql
```

### Use Dry-Run Flags When Available

```bash
wp plugin update --all --dry-run
wp search-replace 'old.com' 'new.com' --dry-run
```

### Dangerous Commands - Require Explicit Confirmation

These commands are destructive and should be used with extreme caution:

- `wp db reset` - Deletes entire database
- `wp db clean` - Removes tables
- `wp site delete` (multisite) - Removes site and content
- `wp user delete` without `--reassign` - Orphans content
- `wp post delete $(wp post list --post_type=page --format=ids)` - Bulk deletions

**Always confirm with the user before running these commands.**

## Performance Flags

Use these flags to optimize speed and output:

```bash
--format=json              # Machine-readable output (faster parsing)
--format=csv              # For spreadsheet imports
--format=ids              # Space-separated IDs (for piping)
--fields=ID,post_title    # Limit returned fields
--skip-plugins            # Bypass plugin loading (faster, but may break dependencies)
--skip-themes             # Bypass theme loading
--quiet                   # Suppress informational output
```

## Core Command Categories

WP-CLI commands are organized by functionality. See `references/commands.md` for detailed flag documentation.

### Database Operations
`wp db` - export, import, query, optimize, search-replace

### Core WordPress
`wp core` - install, update, verify-checksums, version

### Plugins & Themes
`wp plugin` / `wp theme` - list, install, activate, update, delete

### Users
`wp user` - create, list, delete, update, generate

### Content (Posts, Pages, Comments)
`wp post` / `wp comment` - create, list, update, delete, generate

### Options & Settings
`wp option` - get, update, delete, list

### Cache & Performance
`wp cache` / `wp transient` - flush, delete, set

### Cron & Maintenance
`wp cron` - event, schedule, run

### Configuration
`wp config` - create, get, set, shuffle-salts

### Multisite (Basic)
`wp site` - list, create, delete, empty

## Key Workflows

### Site Migration (Local → Production)

```bash
# 1. Export database from source
wp db export migration.sql

# 2. Search-replace URLs (dry-run first!)
wp search-replace 'http://localhost:8000' 'https://example.com' --dry-run
wp search-replace 'http://localhost:8000' 'https://example.com' --skip-columns=guid

# 3. Transfer files (use rsync, scp, or SFTP)
rsync -avz wp-content/ user@server:/var/www/html/wp-content/

# 4. Import database on destination
wp db import migration.sql

# 5. Flush cache and permalinks
wp cache flush
wp rewrite flush

# 6. Verify
wp option get siteurl
wp option get home
```

### Bulk Plugin Updates

```bash
# 1. Check available updates
wp plugin list --update=available

# 2. Backup database
wp db export backup-before-plugin-update.sql

# 3. Update all (or specific plugins)
wp plugin update --all --dry-run
wp plugin update --all

# 4. If issues arise, rollback
wp plugin install plugin-name --version=1.2.3 --force

# 5. Clear cache
wp cache flush
```

### User Audit & Cleanup

```bash
# 1. List all users with roles
wp user list --fields=ID,user_login,user_email,roles

# 2. Find inactive users (requires custom query or plugin)
wp user list --format=json | jq '.[] | select(.user_registered < "2023-01-01")'

# 3. Delete user (MUST reassign content!)
wp user delete <ID> --reassign=<new_author_id>

# 4. Generate test users (for dev environments)
wp user generate --count=10 --role=subscriber
```

## Remote Execution

### SSH Execution

```bash
ssh user@example.com "cd /var/www/html && wp plugin list"
```

### WP-CLI Aliases

Define aliases in `~/.wp-cli/config.yml`:

```yaml
@prod:
  ssh: user@example.com/var/www/html
@staging:
  ssh: user@staging.example.com/var/www/staging
```

Then use:

```bash
wp @prod plugin list
wp @staging db export
```

## Common Errors & Resolution

### Error: "The site you have requested is not installed"

- **Cause**: Not running from WordPress root or `wp-config.php` missing
- **Fix**: `cd` to WordPress root or use `--path=/path/to/wordpress`

### Error: "MySQL connection failed"

- **Cause**: Database credentials incorrect or MySQL not running
- **Fix**: Check `wp-config.php` credentials, verify MySQL is running

### Error: "Error: Can't select database"

- **Cause**: Database doesn't exist
- **Fix**: Create database first: `wp db create`

### Error: "PHP Fatal error: Allowed memory size exhausted"

- **Cause**: Large database operations or heavy plugins
- **Fix**: Increase PHP memory: `php -d memory_limit=512M $(which wp) db export`

### Error: "This does not seem to be a WordPress installation"

- **Cause**: WP-CLI can't find WordPress files
- **Fix**: Verify you're in the correct directory and WordPress is installed

### Warning: "The `guid` column is often used in WordPress for storing URLs but should not be updated"

- **Info**: This is expected. Use `--skip-columns=guid` to suppress the warning
- **Reason**: GUIDs are permanent identifiers and shouldn't be changed

## Best Practices

1. **Always test on staging first** - Never run untested commands on production
2. **Use version control for config changes** - Track `wp-config.php` changes when safe
3. **Monitor command output** - Don't ignore warnings or errors
4. **Document custom workflows** - Keep notes on multi-step processes
5. **Use `--format=json` for scripting** - Easier to parse programmatically
6. **Verify after major changes** - Check site functionality, test critical paths
7. **Keep WP-CLI updated** - `wp cli update` for latest features and fixes

## Additional Resources

- **Command reference**: See `references/commands.md` for detailed flag documentation
- **Workflow examples**: See `references/examples.md` for complete workflow scenarios
- **Official docs**: https://developer.wordpress.org/cli/commands/
