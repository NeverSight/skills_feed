---
name: cleanup
description: Weekly Claude Code maintenance - cleans debug logs, shell snapshots, and old todo files to free up disk space. Run this weekly to keep Claude Code lean.
---

# Claude Code Weekly Cleanup

Performs maintenance cleanup of safe-to-delete Claude Code files.

## What Gets Cleaned

| Directory | Purpose | Safe to Delete |
|-----------|---------|----------------|
| `~/.claude/debug/*` | Debug logs | Yes |
| `~/.claude/shell-snapshots/*` | Shell state snapshots | Yes |
| `~/.claude/todos/*` | Old todo list files | Yes |

## Cleanup Process

1. Show current disk usage before cleanup
2. Remove safe-to-delete files
3. Show disk usage after cleanup
4. Report space freed

## Execute Cleanup

Run these commands:

```bash
# Show before size
echo "Before cleanup:"
du -sh ~/.claude/

# Clean safe directories
rm -rf ~/.claude/debug/* ~/.claude/shell-snapshots/* ~/.claude/todos/*

# Show after size
echo "After cleanup:"
du -sh ~/.claude/
```

## What Is NOT Cleaned (Important Data)

- `projects/` - Session data and history
- `plugins/` - Installed plugins
- `skills/` - Your custom skills
- `history.jsonl` - Conversation history
- `settings.json` - Your settings
- `CLAUDE.md` - Global instructions
