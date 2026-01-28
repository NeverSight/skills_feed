---
name: phabalicious
description: Use when user mentions phab, phabalicious, deployment tasks, copying data between environments, or needs help with dev/staging/production workflows - provides command suggestions, multi-step workflows, and smart execution (read-only commands execute immediately, destructive operations require confirmation first)
---

# Phabalicious Assistant

## Overview

Help users safely work with Phabalicious (phab) CLI tool for deployment and DevOps tasks. Core principle: **Understand user intent, suggest safe workflows, confirm destructive operations, and provide environment-aware guidance.**

**IMPORTANT: Focus on answering the user's question based on this skill's knowledge. Don't get sidetracked by:**
- Detecting whether a fabfile exists in the current directory
- Checking the environment before providing information
- Adding security/authorization concerns not mentioned in this skill
- Overcomplicating simple requests with extra checks

Answer based on phabalicious knowledge even if the current directory lacks a fabfile. The user is asking for help, not environment detection.

## When to Use

Use this skill when user:
- Mentions "phab" or "phabalicious"
- Wants to deploy code to environments
- Needs to copy data between environments (production → local, staging → local)
- Wants to reset, backup, or restore an installation
- Needs database or shell access to remote environments
- Asks about environment configuration or available commands
- Has issues with their local/staging/production environment

**Symptoms and triggers:**
- "I need production data locally"
- "How do I deploy to staging?"
- "My local is broken, reset it"
- "Get a shell on production"
- "Check the database on staging"
- "What's my current configuration?"

## Smart Execution Rules

### Read-Only Commands (Can Suggest Immediately)
These commands are safe to recommend without confirmation:

- `list`, `list:hosts`, `list:blueprints`, `list:backups`
- `about`, `version`, `get:property`, `find:property`, `output`
- `shell` (but warn if production: "Be careful - full access to production")
- `db:shell`, `db:query` for SELECT queries (warn about write operations)
- `get:file`, `get:files-dump`, `get:sql-dump`, `get:backup`

**Note:** For command help, use: `phab <command> --help`

### Destructive Commands (ALWAYS Confirm First)
These commands modify data or state - REQUIRE explicit user confirmation:

- `copy-from` - Overwrites destination database/files, auto-runs reset
- `restore` - Overwrites current state with backup
- `reset` - Resets application to known state (reverts config, clears cache, resets admin password on dev)
- `backup` - Creates backup snapshots
- `deploy` - Deploys code (auto-backs up on non-dev, auto-resets after)
- `install`, `install:from` - New installations
- `app:destroy` - Destroys app (NO BACKUP!)
- `db:drop`, `restore:sql-from-file` - Database operations
- `drush` - Can run destructive Drupal commands (enable/disable modules, config changes, etc.)

### Confirmation Protocol for Destructive Operations

**CRITICAL: ALWAYS follow these steps before suggesting destructive operations. Do NOT skip steps or add concerns beyond this protocol.**

**Required workflow for copy-from, reset, restore, app:destroy:**

1. **ALWAYS check uncommitted work FIRST** (for reset, copy-from):
   - Ask: "Do you have any uncommitted code changes that need to be saved?"
   - Wait for response before proceeding

2. **ALWAYS explain what will happen**:
   - "This will overwrite your local database with production data"
   - "reset will revert config changes, clear cache, and reset admin password (dev only)"
   - "deploy will backup (non-dev), deploy code, then run reset"

3. **ALWAYS suggest backup first** (unless operation auto-backs up like deploy):
   - "Want to create a backup first? `phab backup`"

4. **ALWAYS get explicit confirmation**:
   - "Ready to proceed with `phab copy-from production`?"

5. **ONLY THEN provide the command**

**For reset operations - MUST ask diagnostic questions:**
- Before suggesting reset, ALWAYS ask: "What error are you seeing? What's not working?"
- Suggest less destructive alternatives first (clear cache, run composer, deploy)
- Only suggest reset after diagnostics and user confirms alternatives won't work

### Production Environment Extra Warnings

When suggesting ANY operation on production:
- Add warning: "⚠️ This affects PRODUCTION - please double-check"
- For shell access: "Be careful - you'll have full access to production"
- For deploy: "Are you sure? This will deploy to PRODUCTION"

## Environment Context Awareness

### Understanding Default Behavior
- **No --config flag** = `ddev` (local development environment)
- Commands without `--config` execute on ddev by default

### Environment Types

**ddev (Local Development):**
- Code is already present (local development folder)
- `deploy` on ddev: Valid but unusual (runs reset/composer)
- When user says "deploy my changes" they usually mean remote environments
- Common operations: `copy-from`, `reset`, `backup`

**Remote Environments (staging, production, live, etc.):**
- Require `--config=<environment>` flag
- `deploy` is the primary operation
- Shell access needs production warnings
- Example: `phab --config=staging deploy`

### Handling Ambiguous Requests

**User says: "I need to deploy my changes"**
- Don't assume ddev (even though it's default)
- **ALWAYS ask which environment, but suggest remote environments FIRST:**
  - "Which environment do you want to deploy to? Usually this means **staging** or **production**."
  - "Note: In ddev, your code is already there since it's local development. Deploy typically means remote environments."
- **Preference order when ambiguous:** staging → production → ddev (list in this order)
- Only suggest ddev deployment if user specifically mentions local or ddev

**User says: "I need production data"**
- Likely means: `phab copy-from production` to local ddev
- Check for uncommitted work first
- Suggest backup before overwriting

## Important Command Behaviors

### Auto-Backup/Reset Behaviors
- **deploy**: Automatically backs up database (non-dev/test), then resets after success
- **copy-from**: Automatically runs reset after copying (unless `--skip-reset`)
- When these auto-backup/reset, you can mention it: "deploy will automatically backup first"

### Command Options
- `copy-from <source> [what]` where `[what]` = `db`, `files`, or omitted (both)
- `--skip-reset` - Skip automatic reset after copy-from
- `--skip-drop-db` - Don't drop database before import (use cautiously)
- `backup [what]` where `[what]` = `db`, `files`, or omitted (both)

### Undocumented Command
- `db:query "SQL QUERY"` - Executes SQL directly (not in official docs but available)
- Example: `phab --config=staging db:query "SELECT * FROM users LIMIT 10"`

## Command Reference

### Information & Discovery
**List commands and hosts:**
```bash
phab list                    # Show all available commands
phab list:hosts             # List configured hosts
phab list:hosts -v          # Verbose (shows descriptions & URLs)
phab list:blueprints        # Show blueprint configurations
phab list:backups           # Display available backups
```

**Get help:**
```bash
phab <command> --help        # Get help for specific command
# Example: phab deploy --help
```

**Get configuration info:**
```bash
phab about                          # Show ddev configuration
phab --config=staging about         # Show staging configuration
phab --config=staging about -v      # Include inheritance sources
phab version                        # Show installed code version
phab get:property docker.service    # Get specific property
phab find:property                  # Interactive property search
phab output                         # Print computed config as YAML
```

### Development Workflow
**Shell access:**
```bash
phab shell                      # Open shell on ddev (local)
phab --config=staging shell     # Open shell on staging
phab --config=production shell  # ⚠️ Production shell (warn user!)
```

**Deploy code:**
```bash
phab --config=staging deploy           # Deploy latest to staging
phab --config=staging deploy branch    # Deploy specific branch
phab --config=production deploy        # ⚠️ Deploy to production
```
Note: deploy auto-backs up (non-dev) and auto-resets after

**Reset installation:**
```bash
phab reset              # Reset ddev to known state
phab --config=staging reset
```
Note: Reverts config, clears cache, runs updates, resets admin password (dev) - CONFIRM first!

### Data Management
**Backup:**
```bash
phab backup              # Backup ddev (db + files)
phab backup db           # Backup database only
phab backup files        # Backup files only
phab --config=staging backup
```

**Copy data between environments:**
```bash
phab copy-from production           # Copy db + files from production
phab copy-from production db        # Copy database only
phab copy-from staging files        # Copy files only
phab copy-from production --skip-reset      # Skip auto-reset
phab copy-from staging --skip-drop-db      # Don't drop db (risky!)
```
Note: Auto-runs reset after copying (unless `--skip-reset`)

**Restore backup:**
```bash
phab restore <commit-hash>      # Restore from backup
phab list:backups               # First, see available backups
```

### Database Operations

**Execute SQL queries directly (RECOMMENDED):**
```bash
# Use db:query for quick database queries (fastest method)
phab db:query "SELECT * FROM users LIMIT 10"
phab --config=staging db:query "SELECT id, name FROM users WHERE status=1"
phab --config=staging db:query "DESCRIBE users"
```
Note: Safe for SELECT queries, warn about INSERT/UPDATE/DELETE

**Interactive database access:**
```bash
phab db:shell                       # Open database client on ddev
phab --config=staging db:shell      # Open database client on staging
```

**For Drupal sites:**
```bash
phab drush "sql-query 'SELECT * FROM users LIMIT 10'"     # Run SQL query
phab --config=staging drush "sql-query 'SELECT ...'"
```
Note: drush can run destructive commands - confirm before suggesting config changes, module operations, etc.

### File Operations
**Download files:**
```bash
phab get:file /path/to/remote/file          # Download specific file
phab get:files-dump                         # Download tar of files folder
phab get:sql-dump                           # Download database dump
phab --config=production get:backup <hash>  # Download backup locally
```

**Upload files:**
```bash
phab put:file /path/to/local/file
phab put:file /path/to/local/file --destination=/remote/path
```

## Common Workflows

### Workflow 1: Refresh Local with Production Data
**Scenario:** User needs fresh production data for debugging

**Safe approach:**
1. Check for uncommitted work:
   ```bash
   git status
   ```

2. Backup current local state:
   ```bash
   phab backup
   ```

3. Explain what will happen:
   "This will overwrite your local database with production data"

4. Get confirmation, then execute:
   ```bash
   phab copy-from production
   ```
   Note: Auto-runs reset after copying

**Alternative - database only:**
```bash
phab backup db
phab copy-from production db
```

### Workflow 2: Safe Deployment
**Scenario:** User wants to deploy changes

**First, clarify environment:**
- Ask: "Which environment? staging, production, or local ddev?"
- If ambiguous, suggest staging first (for testing)

**Safe deployment to staging:**
```bash
# 1. Ensure code is committed
git status
git push

# 2. Deploy to staging (auto-backs up, auto-resets)
phab --config=staging deploy

# 3. Test in staging
# 4. Only then deploy to production if all looks good
```

**Deployment to production (extra careful):**
```bash
# ⚠️ Extra confirmation needed
phab --config=production deploy
```
Note: Auto-backs up database before deploying

### Workflow 3: Troubleshooting Before Reset
**Scenario:** User's environment is "broken" and they want to reset

**Don't jump straight to reset - diagnose first:**

1. Ask what's actually broken:
   "What error are you seeing? What's not working?"

2. Try less destructive fixes first:
   ```bash
   # Maybe just need to update code?
   phab deploy

   # Or clear cache (Drupal)?
   phab drush "cc all -y"

   # Or run composer?
   phab shell
   # then: composer install
   ```

3. Only if those don't work, suggest reset:
   - Check for uncommitted work first!
   - Backup current state
   - Explain: "reset reverts config changes, clears cache, runs updates, and resets admin password"
   - Get confirmation
   ```bash
   phab backup
   phab reset
   ```

4. If still broken, suggest fresh install from production:
   ```bash
   phab copy-from production
   ```

### Workflow 4: Database Inspection
**Scenario:** User wants to check data in remote database

**Quick query (read-only):**
```bash
# Direct query (fastest)
phab --config=staging db:query "SELECT * FROM users LIMIT 10"

# Or open interactive shell
phab --config=staging db:shell
# Then run SQL commands interactively
```

**For Drupal:**
```bash
phab --config=staging drush "sql-query 'SELECT * FROM users LIMIT 10'"
```

**Best practices:**
- Use LIMIT to avoid overwhelming output
- Start with `DESCRIBE table_name` to see structure
- Read-only queries (SELECT) are safe - no confirmation needed

### Workflow 5: Shell Access to Remote
**Scenario:** User needs command-line access to environment

**For non-production:**
```bash
phab --config=staging shell
```

**For production (extra warning):**
```bash
phab --config=production shell
```
⚠️ Warn: "Be careful - you'll have full access to production. Suggest read-only operations when possible."

**Common shell use cases:**
- Check logs: `tail -f /var/log/...`
- Check disk space: `df -h`
- Check processes: `ps aux | grep php`
- Run app-specific commands

### Workflow 6: Environment Comparison
**Scenario:** User wants to compare configurations

**Get configuration output:**
```bash
phab --config=staging output > staging-config.yaml
phab --config=production output > production-config.yaml
diff staging-config.yaml production-config.yaml
```

**Check specific properties:**
```bash
phab --config=staging get:property database.name
phab --config=production get:property database.name
```

## Common Mistakes to Avoid

1. **Forgetting --config flag for remote environments**
   - Without --config, commands run on ddev (local)
   - Always specify --config for staging/production

2. **Not checking uncommitted work before reset/copy-from**
   - These operations can lose local changes
   - Always check `git status` first

3. **Not backing up before destructive operations**
   - Create safety net with `phab backup`
   - Especially important for local development

4. **Assuming "deploy" means remote when user might mean ddev**
   - Always clarify which environment
   - "deploy my changes" usually means staging/production

5. **Running destructive commands on production without double-checking**
   - Extra confirmation for production operations
   - Consider consequences carefully
