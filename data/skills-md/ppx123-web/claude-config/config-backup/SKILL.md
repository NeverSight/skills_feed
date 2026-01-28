---
name: config-backup
description: Use when users want to save, backup, copy, export, or version control their Claude Code configuration files (commands, skills, agents) from ~/.claude/ to another directory. Triggered by phrases like "save my claude settings", "backup my claude config", "sync claude configuration", "copy ~/.claude to somewhere", "export my commands and skills", or "archive claude settings before making changes".
version: 1.0.0
---

# Config Backup Skill

This skill helps users backup their Claude Code configuration files from `~/.claude/` to a specified target directory. It copies the `commands/`, `skills/`, and `agents/` directories with options for selective backup.

## What Gets Backed Up

By default, this skill backs up three directories from `~/.claude/`:
- **commands/** - All slash command definitions
- **skills/** - All agent skills and their resources
- **agents/** - All subagent definitions

These are the user-created configurations that define custom Claude Code behavior.

## When to Use This Skill

Use this skill when users want to:
- Backup Claude configurations before making changes
- Copy configurations to another machine or project
- Share custom setup with others
- Migrate to a new system
- Version control configurations

## Backup Workflow

Follow this workflow when performing a backup:

### 1. Confirm Target Directory

Always confirm the target directory, even though the default is the current working directory. Ask like this:

```
"Target directory: [current-working-directory]
Is this correct, or would you like to specify a different location?"
```

Wait for user confirmation before proceeding.

### 2. Select Directories to Backup

Ask the user which directories to include. Present this interactive prompt:

```
"Which directories would you like to backup?
- commands/
- skills/
- agents/

Backup all three, or specify which ones to include?"
```

If the user doesn't specify, backup all three. If they specify a subset, only backup those.

### 3. Execute the Backup Script

Use the backup script located at `scripts/backup.sh` within this skill directory. Execute it with appropriate parameters:

```bash
~/.claude/skills/config-backup/scripts/backup.sh [target-dir] [directories...]
```

Parameters:
- `target-dir`: Target directory (default: current directory if not specified)
- `directories...`: Space-separated list of directories to backup (commands, skills, agents)

The script will:
- Create target directory if it doesn't exist
- Use `rsync` if available (efficient copying), otherwise fallback to `cp -r`
- Overwrite existing files without prompting
- Preserve directory structure
- Exit with error if source `~/.claude/` doesn't exist

### 4. Report Results

After the backup completes, show the user a detailed list of what was copied:

```
✅ Backup complete!

Copied directories:
- commands/ (15 files)
- skills/ (8 directories, 42 files)
- agents/ (23 files)

Target: /path/to/target/directory
```

If any errors occurred during the backup (permission errors, missing source, etc.), report them clearly to the user.

## Error Handling

The backup script handles these scenarios:

### Target Directory Doesn't Exist
Creates the directory automatically. No user action needed.

### Source Directory Missing
If `~/.claude/` doesn't exist, the script exits with error message:
```
❌ Error: Source directory ~/.claude/ not found
```

### No Write Permissions
If target directory isn't writable, shows:
```
❌ Error: Permission denied writing to [target-dir]
```

### rsync Not Available
Automatically falls back to `cp -r` command. User sees:
```
⚠️ rsync not available, using cp instead
```

## Examples

### Example 1: Backup All Directories to Current Location

User: "save my claude settings"

Assistant: "I'll backup your Claude configurations.

Target directory: /Users/choi/work/claude-config
Is this correct, or would you like to specify a different location?

Which directories would you like to backup?
- commands/
- skills/
- agents/

Backup all three, or specify which ones to include?"

[User confirms]

[Executes backup, reports results]

### Example 2: Backup Only Commands and Skills

User: "backup my commands and skills"

[Asks about target directory, then only backs up commands/ and skills/]

### Example 3: Specify Custom Target

User: "copy ~/.claude to ~/backups/claude-config"

[Asks for confirmation, then backs up to ~/backups/claude-config]

## Best Practices

- **Always confirm target directory** before copying to avoid accidental overwrites
- **Show clear feedback** about what was copied so user knows backup succeeded
- **Handle errors gracefully** with helpful error messages
- **Use rsync when available** for efficient incremental backups
- **Preserve structure** so restore is straightforward
- **Overwrite without asking** per user requirements (user should confirm target upfront)

## Technical Details

### Script Location
The backup script is at: `~/.claude/skills/config-backup/scripts/backup.sh`

### Copy Method
- Prefers `rsync -av --delete` for efficient copying with deletion of orphaned files
- Falls back to `cp -rf` if rsync unavailable
- Always preserves permissions and timestamps
- Creates target directories as needed with `mkdir -p`

### Directory Structure
The backup preserves this structure:
```
target-dir/
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

## See Also

- Troubleshooting common issues: `references/troubleshooting.md`
- Detailed backup workflow examples: `examples/backup-workflows.md`
- The backup script implementation: `scripts/backup.sh`
- Claude Code skill documentation for skill structure
- Advanced usage: Pipe backup to tar for archiving, sync to remote with rsync over ssh
