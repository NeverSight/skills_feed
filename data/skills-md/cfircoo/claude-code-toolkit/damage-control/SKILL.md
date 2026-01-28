---
name: damage-control
description: Install, configure, and manage Claude Code security hooks that block dangerous commands and protect sensitive files. Use when setting up security protection, blocking destructive commands (rm -rf, git reset --hard), protecting sensitive paths (.env, credentials), or managing PreToolUse hooks.
---

<objective>
Defense-in-depth protection system for Claude Code. Uses PreToolUse hooks to intercept and validate tool calls before execution, blocking dangerous commands and protecting sensitive files.
</objective>

<protection_levels>
| Level | Read | Write | Edit | Delete | Use Case |
|-------|------|-------|------|--------|----------|
| **zeroAccessPaths** | No | No | No | No | Secrets, credentials, .env files |
| **readOnlyPaths** | Yes | No | No | No | System configs, lock files, build artifacts |
| **noDeletePaths** | Yes | Yes | Yes | No | Important project files, .git/, LICENSE |
</protection_levels>

<how_it_works>
PreToolUse hooks intercept tool calls at three points:

1. **Bash Hook** - Evaluates commands against regex patterns and path restrictions
2. **Edit Hook** - Validates file paths before modifications
3. **Write Hook** - Checks paths before file creation

**Exit codes:**
- `0` = Allow operation
- `0` + JSON = Ask for confirmation (triggers dialog)
- `2` = Block operation (stderr fed back to Claude)

**Ask patterns:** Some operations trigger confirmation dialogs instead of blocking:
- `git checkout -- .` (discards changes)
- `git stash drop` (deletes stash)
- `DELETE FROM table WHERE id=X` (SQL with specific ID)
</how_it_works>

<quick_start>
**Interactive installation:**
```
/damage-control install
```

**Or ask Claude:**
> "Install damage control security hooks"
> "Set up protection for my project"
</quick_start>

<intake>
What would you like to do?

1. **Install** - Set up damage control hooks (global, project, or personal)
2. **Modify** - Add/remove protected paths or blocked commands
3. **Test** - Validate hooks are working correctly
4. **List** - View all active protections across all levels

**Wait for response before proceeding.**
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "install", "setup", "deploy" | [workflows/install.md](workflows/install.md) |
| 2, "modify", "add", "remove", "change" | [workflows/modify.md](workflows/modify.md) |
| 3, "test", "verify", "check" | [workflows/test.md](workflows/test.md) |
| 4, "list", "view", "show" | [workflows/list.md](workflows/list.md) |

**Direct command routing (skip menu):**
- "add ~/.credentials to zero access" → Execute directly, then restart reminder
- "block npm publish command" → Execute directly, then restart reminder
- "protect /secrets folder" → Execute directly, then restart reminder

**After reading the workflow, follow it exactly.**
</routing>

<blocked_commands_summary>
**Destructive file operations:**
- `rm -rf`, `rm --recursive`, `sudo rm`
- `chmod 777`, `chown -R root`

**Git destructive:**
- `git reset --hard`, `git push --force` (not --force-with-lease)
- `git clean -fd`, `git stash clear`, `git filter-branch`

**Cloud destructive:**
- AWS: `terminate-instances`, `delete-db-instance`, `delete-stack`
- GCP: `projects delete`, `instances delete`, `clusters delete`
- Docker: `system prune -a`, `volume rm`
- Kubernetes: `delete namespace`, `delete all --all`

**Database destructive:**
- `DELETE FROM table;` (no WHERE clause)
- `DROP TABLE`, `DROP DATABASE`, `TRUNCATE TABLE`
- `redis-cli FLUSHALL`, `dropdb`

See [scripts/patterns.yaml](scripts/patterns.yaml) for complete list.
</blocked_commands_summary>

<settings_locations>
| Level | Settings Path | Hooks Path | Scope |
|-------|--------------|------------|-------|
| Global | `~/.claude/settings.json` | `~/.claude/hooks/damage-control/` | All projects |
| Project | `.claude/settings.json` | `.claude/hooks/damage-control/` | Team-shared |
| Personal | `.claude/settings.local.json` | `.claude/hooks/damage-control/` | Just you |
</settings_locations>

<runtime_requirements>
**Python with UV (Recommended):**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**TypeScript with Bun (Alternative):**
```bash
# macOS/Linux
curl -fsSL https://bun.sh/install | bash && bun add yaml

# Windows
powershell -c "irm bun.sh/install.ps1 | iex" && bun add yaml
```
</runtime_requirements>

<critical_reminder>
**IMPORTANT:** After any installation or modification:

> **Restart your agent for changes to take effect.**

Hooks are only loaded at agent startup. Run `/hooks` after restart to verify.
</critical_reminder>

<workflows_index>
| Workflow | Purpose |
|----------|---------|
| [workflows/install.md](workflows/install.md) | Interactive installation at any settings level |
| [workflows/modify.md](workflows/modify.md) | Add/remove protected paths and blocked commands |
| [workflows/test.md](workflows/test.md) | Validate all hooks are working correctly |
| [workflows/list.md](workflows/list.md) | View all active protections |
</workflows_index>

<scripts_index>
| Script | Purpose |
|--------|---------|
| [scripts/bash-tool-damage-control.py](scripts/bash-tool-damage-control.py) | PreToolUse hook for Bash commands |
| [scripts/edit-tool-damage-control.py](scripts/edit-tool-damage-control.py) | PreToolUse hook for Edit tool |
| [scripts/write-tool-damage-control.py](scripts/write-tool-damage-control.py) | PreToolUse hook for Write tool |
| [scripts/test-damage-control.py](scripts/test-damage-control.py) | Test runner for hook validation |
| [scripts/patterns.yaml](scripts/patterns.yaml) | Security patterns and protected paths |
| [scripts/settings-template.json](scripts/settings-template.json) | Hook configuration template |
</scripts_index>

<success_criteria>
A working damage-control installation has:

- Hooks installed at chosen level (global/project/personal)
- `patterns.yaml` copied alongside hook scripts
- `settings.json` updated with PreToolUse hook configuration
- UV (or Bun) runtime installed
- Agent restarted to load hooks
- Verified with `/hooks` command showing damage-control hooks
- Tested with `rm -rf /tmp/test` (should be blocked)
</success_criteria>
