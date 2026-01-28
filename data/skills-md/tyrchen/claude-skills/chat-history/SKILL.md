---
name: chat-history
description: Extract and organize Claude Code session history into project .chats directory. Use when users want to document their Claude sessions, export conversation inputs, or maintain a log of instructions given to Claude.
user_invocable: true
---

# Chat History Extractor

Extract user inputs from Claude Code session history (`~/.claude/projects/`) and organize them into a project's `.chats` directory with daily markdown files.

## When to Use This Skill

Use this skill when the user wants to:
- **Extract session history** from Claude Code sessions
- **Document conversations** for future reference
- **Create instruction logs** organized by date
- **Export user inputs** from `.jsonl` session files
- **Maintain a changelog** of Claude interactions

## How It Works

Claude Code stores session data in `~/.claude/projects/{project-path-encoded}/` as `.jsonl` files. Each file contains messages with:
- `type: "user"` - User messages
- `userType: "external"` - External user (not system/agent)
- `message.content` - The actual message content

This skill extracts meaningful user instructions (filtering out system commands, tool results, and session continuations) and organizes them by date into `.chats/{YYYYMMDD}.md` files.

## Instructions

### Step 1: Identify the Project Session Directory

The session directory is derived from the current working directory path:
- Replace `/` with `-` in the path
- Prefix with `-`
- Location: `~/.claude/projects/{encoded-path}/`

```bash
# Example: /Users/tchen/projects/tubi/titc
# Becomes: -Users-tchen-projects-tubi-titc
# Full path: ~/.claude/projects/-Users-tchen-projects-tubi-titc/
```

### Step 2: Find Session Files by Date

List session files and filter by modification date:

```bash
# List all main session files (excluding agent-* files) for a specific date
ls -la ~/.claude/projects/{project-dir}/*.jsonl | grep "Dec 25" | grep -v agent-
```

### Step 3: Extract User Inputs

Extract user messages from jsonl files using jq:

```bash
cat {session-file}.jsonl | jq -r '
  select(.type == "user" and .userType == "external" and (.isMeta | not)) |
  .message.content |
  if type == "string" then . else empty end
' | grep -v "^Caveat:" \
  | grep -v "^<command" \
  | grep -v "^<local-command" \
  | grep -v "^This session is being continued" \
  | grep -v "^<user-prompt-submit-hook>" \
  | grep -v "^Analysis:" \
  | grep -v "^$"
```

### Step 4: Create/Update .chats Files

Create markdown files in `.chats/` directory with format:

```markdown
# Instructions

## {task title}

{user instruction}

## {another task title}

{another user instruction}
```

### Step 5: Commit Changes

After creating/updating chat files, commit with:

```bash
git add .chats/*.md
git commit -m "docs(chats): add session history for {date range}"
```

## File Format

Each `.chats/{YYYYMMDD}.md` file should:
- Start with `# Instructions` header
- Use `##` for each major task/instruction
- Include the actual user input text
- Group related instructions under the same heading
- Preserve code blocks and formatting

## Example Output

`.chats/20251225.md`:
```markdown
# Instructions

## implement feature X

based on @specs/feature-x.md implement all phases entirely

commit the code and test

## fix bug Y

investigate why component Z is not working

use sub agents to analyze the issue in parallel
```

## Filtering Rules

**Include:**
- Direct user instructions and requests
- Questions about the codebase
- Task specifications and requirements

**Exclude:**
- System commands (`<command-name>`, `<local-command-stdout>`)
- Session continuation messages
- Tool results and agent responses
- Hook notifications (`<user-prompt-submit-hook>`)
- Empty lines and caveat messages

## Workflow Summary

1. Get current working directory
2. Compute encoded project path
3. Find session directory: `~/.claude/projects/{encoded-path}/`
4. List sessions grouped by date
5. For each date with sessions:
   - Extract user inputs from all sessions
   - Create `.chats/{YYYYMMDD}.md`
   - Organize inputs with descriptive headers
6. Create `.chats/` directory if it doesn't exist
7. Optionally commit the changes

## Helper Script

You can use this bash snippet to quickly find the project session directory:

```bash
# Get encoded project path
PROJECT_PATH=$(pwd | sed 's|/|-|g' | sed 's|^|/|' | sed 's|^/|-|')
SESSION_DIR="$HOME/.claude/projects/$PROJECT_PATH"

# Check if exists
if [ -d "$SESSION_DIR" ]; then
    echo "Session directory: $SESSION_DIR"
    echo "Sessions by date:"
    ls -la "$SESSION_DIR"/*.jsonl 2>/dev/null | grep -v agent- | awk '{print $6, $7}' | sort -u
else
    echo "No session directory found for this project"
fi
```

## Notes

- Session files named `agent-*.jsonl` are sub-agent sessions and typically don't contain direct user input
- Main session files have UUID-style names (e.g., `01e78099-de0e-4424-845c-518638c8241e.jsonl`)
- The `.message.content` field can be either a string (user text) or an array (tool results)
- Always verify the extracted content makes sense before committing
