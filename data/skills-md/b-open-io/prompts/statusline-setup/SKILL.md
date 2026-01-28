---
name: statusline-setup
description: This skill should be used when the user asks to "create a status line", "customize status line", "set up statusline", "configure Claude Code status bar", "install ccstatusline", "add project colors to status line", "show git branch in status", "display token usage", or mentions Peacock colors, powerline, or status line configuration.
version: 0.0.1
allowed-tools: Bash, Read, Write, Edit, AskUserQuestion
---

# Status Line Setup

Create and customize Claude Code status lines to display contextual information like model name, git branch, token usage, project colors, and more.

## Overview

Claude Code supports custom status lines displayed at the bottom of the interface, similar to terminal prompts (PS1) in shells like Oh-my-zsh. Status lines update when conversation messages change, running at most every 300ms.

## Interactive Setup Flow

When setting up a status line, first check for existing configuration and use AskUserQuestion to gather preferences.

### Pre-Check: Existing Status Line

Before making changes, check for existing configuration:

```bash
# Check for existing status line in settings
if [[ -f ~/.claude/settings.json ]]; then
    EXISTING=$(jq -r '.statusLine // empty' ~/.claude/settings.json)
    if [[ -n "$EXISTING" ]]; then
        # User has existing status line - ask about backup
    fi
fi

# Check for existing script
if [[ -f ~/.claude/statusline.sh ]]; then
    # Existing custom script found
fi
```

### Question 0: Existing Configuration (if found)
```
header: "Existing config"
question: "You have an existing status line configuration. What would you like to do?"
options:
  - label: "Back up and replace"
    description: "Save current config before making changes"
  - label: "View current config"
    description: "Show what's currently configured"
  - label: "Start fresh"
    description: "Replace without backup"
```

If user chooses backup, run:
```bash
~/.claude/plugins/cache/.../scripts/install-statusline.sh --backup-only
# Or manually:
cp ~/.claude/settings.json ~/.claude/settings.json.backup.$(date +%Y%m%d%H%M%S)
cp ~/.claude/statusline.sh ~/.claude/statusline.sh.backup.$(date +%Y%m%d%H%M%S) 2>/dev/null
```

### Question 1: Approach
```
header: "Setup method"
question: "How would you like to create your status line?"
options:
  - label: "Custom script (Recommended)"
    description: "Full control with bash/python/node script"
  - label: "ccstatusline"
    description: "Widget-based TUI tool with easy configuration"
  - label: "Simple inline"
    description: "Quick one-liner for basic info"
```

### Question 2: Features (if custom script)
```
header: "Features"
question: "What information do you want to display?"
multiSelect: true
options:
  - label: "Git branch"
    description: "Current branch with dirty indicator"
  - label: "Project colors"
    description: "Peacock/VSCode theme colors"
  - label: "Token usage"
    description: "Context window consumption"
  - label: "Session cost"
    description: "API cost tracking"
```

### Question 3: Style (if custom script)
```
header: "Style"
question: "What visual style do you prefer?"
options:
  - label: "Powerline"
    description: "Arrow separators with colored segments"
  - label: "Minimal"
    description: "Simple brackets and text"
  - label: "Match terminal"
    description: "Reproduce your shell prompt style"
```

### Question 4: Editor Integration
```
header: "Editor"
question: "Which editor do you use for clickable file links?"
options:
  - label: "Cursor"
    description: "cursor:// protocol"
  - label: "VS Code"
    description: "vscode:// protocol"
  - label: "Sublime"
    description: "subl:// protocol"
  - label: "None"
    description: "No clickable links"
```

## Two Approaches

### 1. Manual Script (Full Control)

Create a shell script that receives JSON data via stdin and outputs a single line with ANSI colors.

**Quick setup:**
```bash
# Create simple status line
cat > ~/.claude/statusline.sh << 'EOF'
#!/bin/bash
input=$(cat)
MODEL=$(echo "$input" | jq -r '.model.display_name')
DIR=$(basename "$(echo "$input" | jq -r '.workspace.current_dir')")
echo "[$MODEL] $DIR"
EOF
chmod +x ~/.claude/statusline.sh
```

**Configure in settings:**
```json
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 0
  }
}
```

### 2. ccstatusline (Widget-Based)

Use the third-party [ccstatusline](https://github.com/sirmalloc/ccstatusline) for a widget-based approach with TUI configuration.

**Quick setup:**
```bash
# Run interactive configuration
bunx ccstatusline@latest

# Or configure in settings directly
```

**Configure in settings:**
```json
{
  "statusLine": "bunx ccstatusline@latest"
}
```

## JSON Input Structure

The status line command receives structured JSON via stdin:

| Field | Description |
|-------|-------------|
| `model.id` | Model identifier (e.g., "claude-opus-4-1") |
| `model.display_name` | Human-readable name (e.g., "Opus") |
| `workspace.current_dir` | Current working directory |
| `workspace.project_dir` | Original project directory |
| `cwd` | Current working directory (legacy) |
| `cost.total_cost_usd` | Session cost in USD |
| `cost.total_duration_ms` | Total session duration |
| `cost.total_lines_added` | Lines added in session |
| `cost.total_lines_removed` | Lines removed in session |
| `context_window.context_window_size` | Max context size (e.g., 200000) |
| `context_window.current_usage` | Current token usage object |
| `transcript_path` | Path to session transcript JSON |
| `session_id` | Unique session identifier |
| `version` | Claude Code version |

See `references/json-input-schema.md` for complete schema documentation.

## Common Patterns

### Git Branch Display

```bash
if git rev-parse --git-dir > /dev/null 2>&1; then
    BRANCH=$(git branch --show-current 2>/dev/null)
    DIRTY=""
    git diff --quiet HEAD 2>/dev/null || DIRTY="*"
    echo "[$MODEL] $BRANCH$DIRTY"
fi
```

### Context Usage Percentage

```bash
USAGE=$(echo "$input" | jq '.context_window.current_usage')
if [ "$USAGE" != "null" ]; then
    TOKENS=$(echo "$USAGE" | jq '.input_tokens + .cache_creation_input_tokens + .cache_read_input_tokens')
    SIZE=$(echo "$input" | jq -r '.context_window.context_window_size')
    PERCENT=$((TOKENS * 100 / SIZE))
    echo "Context: ${PERCENT}%"
fi
```

### Peacock Project Colors

Read colors from `.vscode/settings.json`:

```bash
SETTINGS=".vscode/settings.json"
if [[ -f "$SETTINGS" ]]; then
    COLOR=$(jq -r '.["peacock.color"] // empty' "$SETTINGS")
    # Convert hex to RGB for ANSI
fi
```

### Clickable File Links (OSC 8)

```bash
FILE_URL="vscode://file${LAST_FILE}"
echo -e "\033]8;;${FILE_URL}\a${FILENAME}\033]8;;\a"
```

See `references/scripting-patterns.md` for complete patterns including:
- True color (24-bit) ANSI codes
- Powerline arrow separators
- Project root detection
- Lint status display
- iTerm2 tab color integration

## ccstatusline Widgets

The ccstatusline tool provides pre-built widgets:

| Widget | Description |
|--------|-------------|
| Model Name | Active Claude model |
| Git Branch | Current branch name |
| Git Changes | Uncommitted changes |
| Session Clock | Current time |
| Session Cost | Session expenses |
| Block Timer | 5-hour block progress |
| Tokens Input/Output | Token counts |
| Context Percentage | Context usage % |
| Custom Command | Run shell commands |
| Custom Text | Static text/emojis |

**Configuration stored at:** `~/.config/ccstatusline/settings.json`

See `references/ccstatusline-guide.md` for complete widget documentation.

## Advanced Features

### Multi-Project Awareness

Track both the CWD project and currently-edited project:

```bash
# Find project root by walking up directory tree
find_project_root() {
    local current="$1"
    while [[ "$current" != "/" ]]; do
        if [[ -d "$current/.git" ]] || [[ -f "$current/package.json" ]]; then
            echo "$current"
            return
        fi
        current=$(dirname "$current")
    done
}
```

### Transcript Parsing

Extract last-edited file from transcript:

```bash
if [[ -f "$TRANSCRIPT" ]]; then
    LAST_FILE=$(tail -200 "$TRANSCRIPT" | \
        grep -o '"file_path":"[^"]*"' | tail -1 | \
        sed 's/"file_path":"//; s/"$//')
fi
```

### Terminal Title

Set terminal title alongside status line:

```bash
echo -ne "\033]0;${PROJECT_NAME}\007" >&2
```

### iTerm2 Tab Colors

Set tab color to match project theme:

```bash
if [[ "$TERM_PROGRAM" == "iTerm.app" ]]; then
    echo -ne "\033]6;1;bg;red;brightness;${R}\007" >&2
    echo -ne "\033]6;1;bg;green;brightness;${G}\007" >&2
    echo -ne "\033]6;1;bg;blue;brightness;${B}\007" >&2
fi
```

## Best Practices

1. **Keep it concise** - Status line should fit on one line
2. **Use colors sparingly** - Make information scannable, not overwhelming
3. **Cache expensive operations** - Git status can be slow on large repos
4. **Test manually first** - Pipe mock JSON to script before configuring
5. **Use jq for parsing** - Reliable JSON extraction in bash
6. **Handle missing data** - Fields may be null or missing
7. **Output to stdout only** - Status line reads first line of stdout

## Testing

Test scripts with mock JSON:

```bash
echo '{"model":{"display_name":"Opus"},"workspace":{"current_dir":"/test"}}' | ./statusline.sh
```

## Examples

Working examples in `examples/`:
- **`simple-statusline.sh`** - Minimal git-aware status line
- **`peacock-statusline.sh`** - Full Peacock color integration
- **`ccstatusline-config.json`** - Sample ccstatusline configuration

## Installation Script

Use `scripts/install-statusline.sh` to:
- Copy status line script to `~/.claude/`
- Update settings.json
- Create backup of existing configuration

## Restore Previous Configuration

Backups are created with timestamps in `~/.claude/`:

```bash
# List available backups
ls -la ~/.claude/*.backup.*

# Example output:
# settings.json.backup.20240115143022
# statusline.sh.backup.20240115143022
```

**Restore using the restore script:**
```bash
~/.claude/plugins/cache/.../scripts/restore-statusline.sh
# Or with specific backup:
~/.claude/plugins/cache/.../scripts/restore-statusline.sh 20240115143022
```

**Manual restore:**
```bash
# Find most recent backup
LATEST=$(ls -t ~/.claude/settings.json.backup.* 2>/dev/null | head -1)

# Restore settings
if [[ -n "$LATEST" ]]; then
    cp "$LATEST" ~/.claude/settings.json
    echo "Restored settings from $LATEST"
fi

# Restore script if exists
SCRIPT_BACKUP=$(ls -t ~/.claude/statusline.sh.backup.* 2>/dev/null | head -1)
if [[ -n "$SCRIPT_BACKUP" ]]; then
    cp "$SCRIPT_BACKUP" ~/.claude/statusline.sh
    echo "Restored script from $SCRIPT_BACKUP"
fi
```

**Remove status line entirely:**
```bash
# Remove statusLine from settings
jq 'del(.statusLine)' ~/.claude/settings.json > /tmp/settings.json && \
    mv /tmp/settings.json ~/.claude/settings.json
```

## Additional Resources

### Reference Files

- **`references/json-input-schema.md`** - Complete JSON input documentation
- **`references/scripting-patterns.md`** - Bash/Python/Node patterns and color codes
- **`references/ccstatusline-guide.md`** - Third-party tool configuration

### External Links

- [Claude Code Status Line Docs](https://docs.anthropic.com/en/docs/claude-code/statusline)
- [ccstatusline GitHub](https://github.com/sirmalloc/ccstatusline)
- [Powerline Fonts](https://github.com/powerline/fonts)
