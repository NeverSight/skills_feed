---
name: config-restore
description: This skill should be used when users want to restore, reload, or copy their Claude Code configuration files (commands, skills, agents) from a backup directory back to ~/.claude/. Triggered by phrases like "restore my claude config", "reload claude settings", "copy config back to ~/.claude/", "restore from backup", "recover claude configuration", "import commands and skills from backup", "I accidentally deleted my commands", "restore my old skills", "copy config from backup", or "I need to recover my claude settings from a backup".
version: 1.0.0
---

# Config Restore Skill

Restores Claude Code configuration files from a backup directory back to `~/.claude/`. Restores the `commands/`, `skills/`, and `agents/` directories with user confirmation before overwriting existing files.

## What Gets Restored

By default, this skill restores three directories to `~/.claude/`:
- **commands/** - All slash command definitions
- **skills/** - All agent skills and their resources
- **agents/** - All subagent definitions

These are the user-created configurations that define custom Claude Code behavior.

## When to Use This Skill

Use this skill to:
- Restore configurations from a previous backup
- Reload configurations after making changes
- Copy configurations from another machine or project
- Recover from accidental deletions or modifications
- Import configurations shared by others

## Restore Workflow

Follow this workflow when performing a restore:

### 1. Confirm Source Directory

Always confirm the source directory, even though the default is the current working directory. Ask this:

```
"Source directory: [current-working-directory]
Is this correct, or would you like to specify a different location?"
```

Wait for user confirmation before proceeding.

### 2. Select Directories to Restore

Ask the user which directories to restore. Present this interactive prompt:

```
"Which directories would you like to restore?
- commands/
- skills/
- agents/

Restore all three, or specify which ones?"
```

If the user doesn't specify, restore all three. If they specify a subset, only restore those.

### 3. Check for Conflicts

**Critical**: Before copying, check if target directories already exist in `~/.claude/`. If they do, ask for confirmation:

```
"⚠️ Target directory commands/ already exists with X files
❓ Overwrite commands/ in ~/.claude/?"
```

Wait for user response (yes/no) before proceeding. If user declines, skip that directory.

### 4. Execute the Restore Script

Use the restore script located at `scripts/restore.sh` within this skill directory. Execute it with appropriate parameters:

```bash
~/.claude/skills/config-restore/scripts/restore.sh [source-dir] [directories...]
```

Parameters:
- `source-dir`: Source directory containing backup (default: current directory if not specified)
- `directories...`: Space-separated list of directories to restore (commands, skills, agents)

The script will:
- Check that source directory exists
- Check that `~/.claude/` exists (error if not)
- Ask for confirmation before overwriting existing directories
- Use `rsync` if available (efficient copying), otherwise fallback to `cp -r`
- Preserve directory structure
- Skip directories if user declines confirmation

### 5. Report Results

After the restore completes, show the user a detailed list of what was restored:

```
✅ Restore complete!

Restored directories:
- commands/ (15 files)
- skills/ (8 directories, 42 files)
- agents/ (23 files)

Total: 80 files in 31 directories
Target: /Users/username/.claude
```

If any directories were skipped (either missing from source or declined by user), report them clearly.

## Error Handling

The restore script handles these scenarios:

### Source Directory Doesn't Exist
Exits with error message:
```
❌ Error: Source directory /path/to/source not found
```

### Target Directory Missing
If `~/.claude/` doesn't exist, the script exits with error:
```
❌ Error: Target directory ~/.claude not found. Claude Code may not be installed.
```

This prevents accidentally creating `~/.claude/` in unexpected situations.

### User Declines Overwrite
If user says "no" to overwrite confirmation, the directory is skipped:
```
❓ Overwrite commands/ in ~/.claude/? no
Skipping commands/
```

### Directory Not in Source
If a requested directory doesn't exist in the source backup:
```
⚠️ Skipping agents/ (not found in source)
```

### rsync Not Available
Automatically falls back to `cp -r` command. User sees:
```
⚠️ rsync not available, using cp instead
```

## Examples

Common restore patterns:
- "restore my claude config" - Restore all directories from current location
- "just restore commands and skills" - Selective restore of specific directories
- "restore from ~/backups/claude-config" - Custom source directory
- "I accidentally deleted my commands" - Recovery from accidental deletion

See `examples/restore-workflows.md` for detailed walkthroughs with complete dialogue.

## Best Practices

- **Always confirm source directory** before restoring
- **Check for conflicts** and ask before overwriting existing files
- **Show clear feedback** about what was restored so user knows operation succeeded
- **Handle errors gracefully** with helpful error messages
- **Never auto-overwrite** - always ask user for confirmation when conflicts exist
- **Use rsync when available** for efficient copying
- **Fail fast** if `~/.claude/` doesn't exist rather than creating it

## Technical Details

### Script Location
The restore script is at: `~/.claude/skills/config-restore/scripts/restore.sh`

### Copy Method
- Prefers `rsync -av` for efficient copying
- Falls back to `cp -rf` if rsync unavailable
- Always preserves permissions and timestamps
- Creates target directories as needed with `mkdir -p`

### Conflict Detection
- Checks if target directory exists before copying
- Counts files in target to show user what will be overwritten
- Prompts user for each directory with conflicts
- Respects user's choice to skip or overwrite

### Directory Structure
The restore preserves this structure:
```
source-dir/
├── commands/
│   ├── command1.md
│   └── command2.md
├── skills/
│   ├── skill1/
│   └── skill2/
└── agents/
    ├── agent1.md
    └── agent2.md
```

All files are copied to `~/.claude/` maintaining the same structure.

## See Also

- Troubleshooting common issues: `references/troubleshooting.md`
- Detailed restore workflow examples: `examples/restore-workflows.md`
- The restore script implementation: `scripts/restore.sh`
- Claude Code skill documentation for skill structure
- Related: config-backup skill for creating backups
