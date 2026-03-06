---
name: hook
description: Hook control - enable, disable, and manage Claude Code hooks. Use when you need to manage, debug, or monitor Claude Code hooks for the current session.
---

# Hook Management System

Manage Claude Code hooks for the current session.

## When to use

- When you need to check the status of Claude Code hooks
- When you want to temporarily disable a noisy or problematic hook
- When debugging hook behavior or performance issues
- When monitoring hook execution metrics

## Usage

```
/hook status                  # Show all hooks and their status
/hook list                    # List available hooks with descriptions
/hook disable [hook-name]     # Temporarily disable a hook
/hook enable [hook-name]      # Re-enable a disabled hook
/hook profile                 # Show hook performance metrics
/hook logs [hook-name]        # View recent logs for a hook
```

## Instructions

When this command is invoked:

### /hook status

1. Read `~/.claude/settings.json`
2. Parse the hooks configuration
3. Check `~/.claude/hooks/.disabled` for disabled hooks
4. Display in a formatted table:
   - Hook type (SessionStart, PreToolUse, PostToolUse, and others)
   - Matcher pattern
   - Command/Prompt
   - Status (enabled/disabled)

### /hook list

1. Scan `~/.claude/hooks/` directory
2. List each hook file with:
   - Filename
   - Description (from docstring)
   - Trigger type
   - Last modified

### /hook disable [hook-name]

1. Create/update `~/.claude/hooks/.disabled` file
2. Add the hook name to the disabled list
3. Hooks check this file before running
4. Note: Changes persist until re-enabled

### /hook enable [hook-name]

1. Read `~/.claude/hooks/.disabled` file
2. Remove the hook name from the disabled list
3. Confirm the hook is re-enabled

### /hook profile

1. Read `~/.claude/logs/hook_metrics.jsonl`
2. Calculate average execution time per hook
3. Show:
   - Hook name
   - Avg execution time (ms)
   - Total calls
   - Success rate
   - Token impact estimate

### /hook logs [hook-name]

1. Find log files in `~/.claude/logs/`
2. Filter by hook name
3. Show last 20 entries
4. Include timestamp, result, and any errors

## Examples

```bash
# Check current hook status
/hook status

# Disable noisy notifications temporarily
/hook disable notification

# Re-enable when ready
/hook enable notification

# Check performance impact
/hook profile

# Debug a specific hook
/hook logs post_tool_use
```

## Notes

- Disabled state uses `~/.claude/hooks/.disabled` file
- Performance data from `~/.claude/logs/hook_metrics.jsonl`
- Hooks check disabled state before executing
- Session-based disabling (resets on restart)
