---
name: drupal-config-mgmt
description: Safe patterns for inspecting and syncing Drupal configuration across environments without accidentally importing changes.
---

# Drupal Configuration Management

Safe patterns for inspecting and syncing Drupal configuration across environments without accidentally importing changes.

## When This Skill Activates

Activates when working with Drupal configuration management including:
- Inspecting config differences between environments
- Syncing config from remote environments
- Using drush commands safely on remote servers
- Avoiding accidental config imports
- Manual config editing workflows

---

## Problem: Avoid Accidental Config Imports

**CRITICAL**: Some hosting platforms default drush commands to `--yes` (auto-confirm). Commands like `config:import` or `cim` may AUTO-CONFIRM and import configuration even when you only want to inspect differences.

### Dangerous vs Safe Patterns

❌ **DANGEROUS** - May auto-import without confirmation:
```bash
# Via SSH to remote
ssh user@remote.server "cd /path/to/drupal && drush cim --diff"
ssh user@remote.server "cd /path/to/drupal && drush config:import --diff"
```

✅ **SAFE** - Will show diff without importing:
```bash
# Via SSH with --no flag
ssh user@remote.server "cd /path/to/drupal && drush cim --no --diff"
ssh user@remote.server "cd /path/to/drupal && drush config:import --no --diff"
```

✅ **SAFEST** - Use read-only commands:
```bash
# Via SSH - read-only operations
ssh user@remote.server "cd /path/to/drupal && drush config:get config.name"
ssh user@remote.server "cd /path/to/drupal && drush config:status"
```

---

## Available Topics

Full documentation available in references:

- @references/full-guide.md - Complete configuration management guide
- @references/safe-inspection.md - Read-only config inspection patterns
- @references/manual-sync.md - Manual config editing workflow
- @references/examples.md - Common sync scenarios

---

## Quick Reference

### Get Config from Remote
```bash
# Via SSH
ssh user@remote.server "cd /path/to/drupal && drush config:get config.name --format=yaml"

# Via DDEV for local
ddev drush config:get config.name --format=yaml
```

### Compare Environments
```bash
# View import diff (safe with --no) via SSH
ssh user@remote.server "cd /path/to/drupal && drush cim --no --diff"

# Get specific config for manual comparison
ssh user@remote.server "cd /path/to/drupal && drush config:get config.name --format=yaml" > /tmp/remote.yml
diff -u config/default/config.name.yml /tmp/remote.yml
```

### Manual Edit Workflow
1. Get remote config via SSH: `ssh user@remote "cd /path/to/drupal && drush config:get config.name"`
2. Edit local file with Edit tool
3. Review: `git diff config/default/config.name.yml`
4. Commit: `git add config/default/config.name.yml && git commit`

---

## Best Practices

1. **Always use `--no` flag** with cim/cex on remote drush commands
2. **Manual edits preferred** over automated imports
3. **One config type per commit** for clean history
4. **Clear commit messages** referencing source environment
5. **Clean up temp files** after comparison operations

---

**Last updated**: 2024-11-05
