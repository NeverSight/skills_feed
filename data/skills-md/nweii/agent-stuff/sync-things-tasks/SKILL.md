---
name: sync-things-tasks
description: "Syncs tasks between Obsidian vault and Things 3. Adds tasks from notes, extracts action items from projects, reviews existing tasks. Use when managing todos from vault content."
metadata:
  author: nweii
  version: "1.1.0"
---

# Sync Things Tasks

Bridge thinking (Obsidian) and doing (Things 3) using the `things` CLI.

## Core Concepts

- **Thinking vs. Doing**: Use Obsidian for drafting ideas and planning. Use Things 3 for actionable todos with dates/deadlines.
- **CLI-First**: Use the `things` command to add tasks without leaving the chat.
- **Contextual Tasks**: When summarizing notes, proactively identify action items and offer to send them to Things.

## Auth Token

The CLI requires an auth token for update operations. The user should have `THINGS_AUTH_TOKEN` set in their shell profile.

## Common Workflows

### Adding Tasks from Notes

```bash
# Add to Today with Obsidian link
things add "Follow up with [Name]" --notes "Context: [Note Title](obsidian://open?vault=MyVault&file=Path%2FTo%2FNote)" --when today
```

### Project Task Extraction

When working on project notes, extract action items:

```bash
things add "Draft initial spec" --list "Project Name" --notes "Reference: [Project](obsidian://open?vault=MyVault&file=...)"
```

### Reviewing Tasks

```bash
things today              # What's on today
things areas             # Existing Areas
things projects          # Existing Projects
things show "Area Name"  # Contents of Area
things tasks --project "Project Name"  # Tasks in project
things search "query"    # Search for existing tasks
```

## Integration Principles

- **Discovery First**: Use `things areas` and `things projects` before creating new containers
- **Obsidian URIs**: Include clickable Obsidian links in Things notes: `[Note](obsidian://open?vault=MyVault&file=URL_ENCODED_PATH)`
- **Dry Run First**: Use `things --dry-run add "..."` for complex tasks
- **Things as Truth**: Things is the source of truth for "doing"; don't necessarily update Obsidian when tasks complete
