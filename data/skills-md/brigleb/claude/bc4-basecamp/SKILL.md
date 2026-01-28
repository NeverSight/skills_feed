---
name: bc4-basecamp
description: Manages Basecamp todos, cards, messages, and projects using the bc4 CLI tool. Use when the user mentions Basecamp, asks about todos or tasks on a card table, wants to create or update Basecamp items, or references team project management.
---

# BC4 Basecamp Integration

Claude can interact with Basecamp via the `bc4` command-line tool, enabling management of:

- **Todos**: Create, view, check/uncheck, edit, and organize todos
- **Cards**: Manage kanban-style card tables for workflow tracking
- **Messages**: Post announcements and updates to projects
- **Campfires**: Team chat functionality
- **Comments**: Add comments to any Basecamp resource

## Quick Reference

### Check Authentication & Context
```bash
bc4 auth status          # Verify authentication
bc4 profile              # Show current user
bc4 project list         # List available projects
bc4 project select       # Interactively select default project
```

### Todos
```bash
bc4 todo lists                    # List all todo lists in project
bc4 todo list "List Name"         # View todos in a specific list
bc4 todo list --grouped           # Show todos grouped by sections
bc4 todo view <id>                # View todo details
bc4 todo add "Task description"   # Create a new todo
bc4 todo check <id>               # Mark complete
bc4 todo uncheck <id>             # Mark incomplete
bc4 todo edit <id>                # Edit a todo
```

### Cards (Kanban Boards)
```bash
bc4 card list                     # List card tables in project
bc4 card table "Table Name"       # View cards in a table
bc4 card view <id>                # View card details with steps
bc4 card add "Card title"         # Quick card creation
bc4 card move <id> --column "Col" # Move card to column
bc4 card assign <id>              # Assign people to card
bc4 card step list <card-id>      # List steps on a card
```

### Messages & Campfire
```bash
bc4 message post                  # Post a message (interactive)
bc4 campfire post "Update"        # Quick team chat message
```

### Comments
```bash
bc4 comment add <resource-type> <id> "Comment text"
```

## Global Flags

These flags work with any bc4 command:
- `--json` - Output in JSON format (useful for parsing)
- `--project <id>` - Override default project
- `--account <id>` - Override default account
- `--verbose` - Enable debug output
- `--no-color` - Disable colored output

## Workflow Guidelines

1. **Always verify context first**: Run `bc4 project list` or check authentication if unsure about the current project
2. **Use descriptive names**: When creating todos or cards, include clear, actionable descriptions
3. **Check before acting**: View items with `bc4 todo view` or `bc4 card view` before editing
4. **JSON output**: Use `--json` flag when you need to parse or process the output programmatically

## Common Patterns

When the user asks to:
- **See what's on a card**: Use `bc4 card view <id>` to see full details including steps
- **Complete a task**: Use `bc4 todo check <id>` to mark it done
- **Update a card's status**: Use `bc4 card move <id> --column "Done"`
- **Add a comment**: Use `bc4 comment add card <id> "Comment text"`
- **Find a specific todo/card**: Use `bc4 todo list` or `bc4 card table` with grep if needed

For detailed command documentation, see [commands.md](mdc:commands.md).
For workflow examples, see [examples.md](mdc:examples.md).
