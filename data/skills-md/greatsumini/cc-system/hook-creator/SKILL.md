---
name: hook-creator
description: Create and configure Claude Code hooks for customizing agent behavior. Use when the user wants to (1) create a new hook, (2) configure automatic formatting, logging, or notifications, (3) add file protection or custom permissions, (4) set up pre/post tool execution actions, or (5) asks about hook events like PreToolUse, PostToolUse, Notification, etc.
---

# Hook Creator

Create Claude Code hooks that execute shell commands at specific lifecycle events.

## Hook Creation Workflow

1. **Identify the use case** - Determine what the hook should accomplish
2. **Select the appropriate event** - Choose from available hook events (see references/hook-events.md)
3. **Design the hook command** - Write shell command that processes JSON input from stdin
4. **Configure the matcher** - Set tool/event filter (use `*` for all, or specific tool names like `Bash`, `Edit|Write`)
5. **Choose storage location** - User settings (`~/.claude/settings.json`) or project (`.claude/settings.json`)
6. **Test the hook** - Verify behavior with a simple test case

## Hook Configuration Structure

```json
{
  "hooks": {
    "<EventName>": [
      {
        "matcher": "<ToolPattern>",
        "hooks": [
          {
            "type": "command",
            "command": "<shell-command>"
          }
        ]
      }
    ]
  }
}
```

## Common Patterns

### Reading Input Data

Hooks receive JSON via stdin. Use `jq` to extract fields:

```bash
# Extract tool input field
jq -r '.tool_input.file_path'

# Extract with fallback
jq -r '.tool_input.description // "No description"'

# Conditional processing
jq -r 'if .tool_input.file_path then .tool_input.file_path else empty end'
```

### Exit Codes for PreToolUse

- `0` - Allow the tool to proceed
- `2` - Block the tool and provide feedback to Claude

### Matcher Patterns

- `*` - Match all tools
- `Bash` - Match only Bash tool
- `Edit|Write` - Match Edit or Write tools
- `Read` - Match Read tool

## Quick Examples

**Log all bash commands:**
```bash
jq -r '"\(.tool_input.command)"' >> ~/.claude/bash-log.txt
```

**Auto-format TypeScript after edit:**
```bash
jq -r '.tool_input.file_path' | { read f; [[ "$f" == *.ts ]] && npx prettier --write "$f"; }
```

**Block edits to .env files:**
```bash
python3 -c "import json,sys; p=json.load(sys.stdin).get('tool_input',{}).get('file_path',''); sys.exit(2 if '.env' in p else 0)"
```

## Resources

- **Hook Events Reference**: See `references/hook-events.md` for detailed event documentation with input/output schemas
- **Example Configurations**: See `references/examples.md` for complete, tested hook configurations
