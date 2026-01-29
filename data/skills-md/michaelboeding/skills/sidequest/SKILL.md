---
name: sidequest
description: Spawn a new Claude Code session in a separate terminal to work on a different task, optionally with context from the current session. Use when you need to work on something else without losing your current progress.
triggers:
  - sidequest
  - new terminal
  - spawn session
  - parallel task
  - side task
  - branch off
---

# Sidequest: Spawn Parallel Claude Sessions

Launch a new Claude Code session in a separate terminal to work on a different task while keeping your current session active.

## Usage

```
/sidequest "Add a settings page with dark mode toggle"
/sidequest "Set up the database schema" --no-context
/sidequest  # Interactive prompt for task description
```

## What It Does

1. **Gathers context** (unless `--no-context`):
   - Current working directory
   - Current git branch
   - Brief summary of what's being worked on
   - Key files recently modified/read

2. **Opens new terminal tab/window**:
   - macOS Terminal.app or iTerm2 supported
   - Automatically detects which terminal is in use

3. **Starts Claude with context**:
   ```bash
   cd "<current_directory>" && claude -p "<context_prompt>"
   ```

4. **Returns control** to original session (user continues main task)

## Flags

| Flag | Description |
|------|-------------|
| `--no-context` | Start fresh without context from parent session |
| `--iterm` | Force use of iTerm (auto-detected by default) |
| `--terminal` | Force use of Terminal.app (auto-detected by default) |

## Implementation

When user invokes `/sidequest`, execute the following:

### Step 1: Parse Arguments

Check if the user provided:
- A task description (required, or prompt for it)
- `--no-context` flag (skip context entirely)

If no task description provided, ask the user what they want to work on.

### Step 2: Ask About Context (unless --no-context)

**IMPORTANT**: If `--no-context` was NOT specified, use the `AskUserQuestion` tool to ask:

```
Use AskUserQuestion with:
- question: "Include a summary of this chat in the sidequest?"
- header: "Context"
- options:
  1. "Yes, include summary" - "Pass context about current work to help the new session understand what you're doing"
  2. "No, start fresh" - "Start the sidequest with no context from this session"
```

### Step 3: Gather Context (if user chose to include summary)

If user selected "Yes, include summary":
1. Summarize the current conversation (what task is being worked on, key decisions made)
2. Get current git branch: `git branch --show-current`
3. Identify key files from recent tool calls
4. Note any relevant todos or blockers

If user selected "No, start fresh":
- Skip context gathering, proceed with just the task description

### Step 4: Build Context Prompt

Format the prompt for the new session:

**With context:**
```
SIDEQUEST from main task.

Main task context:
- Working directory: /path/to/project
- Git branch: feature/user-auth
- Was working on: <summary of current task>
- Key files: <recent files>
- Progress: <key progress and decisions made>

Your sidequest task: <user's task description>

This is separate from the main task. Focus only on this sidequest.
```

**Without context:**
```
SIDEQUEST MODE

Your task: <user's task description>

This is an independent task. Focus only on completing this sidequest.
```

### Step 5: Detect Terminal and Launch

```bash
# Detect terminal
if [[ -z "$TERMINAL_APP" ]]; then
  if [[ "$TERM_PROGRAM" == "iTerm.app" ]]; then
    TERMINAL_APP="iTerm"
  else
    TERMINAL_APP="Terminal"
  fi
fi

# Escape the prompt for shell
ESCAPED_PROMPT=$(echo "$CONTEXT_PROMPT" | sed 's/"/\\"/g')

# Launch based on terminal
if [[ "$TERMINAL_APP" == "iTerm" ]]; then
  osascript -e "tell application \"iTerm\"
    tell current window
      create tab with default profile
      tell current session
        write text \"cd '$PWD' && claude -p \\\"$ESCAPED_PROMPT\\\"\"
      end tell
    end tell
  end tell"
else
  osascript -e "tell application \"Terminal\"
    activate
    do script \"cd '$PWD' && claude -p \\\"$ESCAPED_PROMPT\\\"\"
  end tell"
fi
```

### Step 6: Confirm to User

After launching, inform the user:

```
Sidequest started in new terminal!
Task: <task description>
Continue your main quest here.
```

## Example Workflow

**Main terminal (building user authentication):**
```
You: Working on the login API endpoint...
You: /sidequest "Add a settings page with dark mode toggle"

Claude: [AskUserQuestion]
        Include a summary of this chat in the sidequest?

        > Yes, include summary
          No, start fresh

You: (selects "Yes, include summary")

Claude: Sidequest started in new terminal!
        Task: Add a settings page with dark mode toggle
        Context: Included summary of current auth work
        Continue your main quest here.

You: (continues auth work)
```

**New terminal (opens automatically):**
```
Claude: SIDEQUEST MODE
        Task: Add a settings page with dark mode toggle

        Context from main session:
        - Working on: Building user authentication with JWT
        - Branch: feature/user-auth
        - Key files: auth.ts, login.tsx, middleware.ts
        - Progress: Login endpoint complete, working on token refresh

        Let me look at the existing pages structure...
```

**Example without context:**
```
You: /sidequest "Set up CI/CD pipeline" --no-context
Claude: Sidequest started in new terminal!
        Task: Set up CI/CD pipeline
        (No context passed - starting fresh)
```

## Script Location

The sidequest shell script is located at:
```
${CLAUDE_PLUGIN_ROOT}/skills/sidequest/scripts/sidequest.sh
```

## Execution

To run a sidequest:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/sidequest/scripts/sidequest.sh" \
  --task "Your task description" \
  --context "Summary of current work" \
  --branch "$(git branch --show-current 2>/dev/null || echo 'N/A')" \
  --files "auth.ts,login.tsx"
```

Or without context:
```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/sidequest/scripts/sidequest.sh" \
  --task "Your task description" \
  --no-context
```

## Requirements

- macOS (uses osascript for terminal control)
- Terminal.app or iTerm2
- Claude Code CLI installed (`claude` command available)

## Notes

- The sidequest runs independently - changes in one session don't affect the other
- Both sessions share the same working directory and git state
- Be careful with conflicting file edits between sessions
- Use `git stash` if you need to switch context between sessions
