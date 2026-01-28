---
name: vault-status
description: Show current vault status using Obsidian MCP tools. Displays structure overview, recent changes, file counts, and vault health. Use when orienting to a vault, checking what's changed, or getting a quick overview. Requires Obsidian MCP server.
---

# Vault Status

Display vault status and recent activity.

## Workflow

1. Get vault overview
   - Use `obsidian_list_files_in_vault` for top-level structure
   - Count files by folder
   - Identify vault size

2. Check recent changes
   - Use `obsidian_get_recent_changes` for recently modified files
   - Summarize what's been active

3. Check periodic notes
   - Use `obsidian_get_periodic_note` for today's daily note
   - Note if periodic notes are configured

4. Summarize vault health
   - Total file count
   - Active areas (recently modified)
   - Any obvious issues

## MCP Tools Used

```typescript
// List vault structure
obsidian_list_files_in_vault()

// List specific directory
obsidian_list_files_in_dir({ dirpath: "Projects/Active" })

// Get recent changes
obsidian_get_recent_changes({ limit: 10, days: 7 })

// Check today's daily note
obsidian_get_periodic_note({ period: "daily" })
```

## Output Format

```
## Vault Status

**Total Files**: {count}
**Last Modified**: {timestamp}

### Structure
{folder}: {count} files
{folder}: {count} files
...

### Recent Activity (7 days)
- {file} ({date})
- {file} ({date})
...

### Today
- Daily note: {exists/missing}
- {any relevant status}
```

## Parameters

- `$ARGUMENTS` (optional): Specific folder to focus on

## Example

User: `/vault-status`

Response:
"## Vault Status

**Total Files**: 847
**Last Modified**: 2 hours ago

### Structure
- Projects/: 124 files (Active: 45, Backlog: 32, Completed: 47)
- Areas/: 203 files
- Resources/: 312 files
- Archive/: 156 files
- Planner/: 52 files

### Recent Activity (7 days)
- `Projects/Active/AI Ready Vault/AI Ready Vault.md` (today)
- `Areas/AI/Memory/Strategic/2025-01-08 - Product Vision.md` (today)
- `Planner/2025/01-January/2025-01-08.md` (today)
- `Areas/Career/Job Search.md` (yesterday)

### Today
- Daily note: Present (`Planner/2025/01-January/2025-01-08.md`)
- 4 files modified today"
