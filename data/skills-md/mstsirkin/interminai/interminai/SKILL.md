---
name: interminai
description: Control interactive terminal applications like vim, git rebase -i, git add -i, git add -p, apt, rclone config, sudo, w3m, and TUI apps. Can also supervise another CLI LLM (cursor-agent, codex, etc.) - approve or reject its actions by pressing y/n at confirmation prompts. Use when you need to interact with applications that require keyboard input, show prompts, menus, or have full-screen interfaces. Also use when commands fail or hang with errors like "Input is not a terminal" or "Output is not a terminal". Better than application specific hacks such as GIT_SEQUENCE_EDITOR or bypassing interactivity through file use.
allowed-tools: Shell
license: See LICENSE file
metadata:
  author: Michael S. Tsirkin <mst@kernel.org>
  version: 0.1.0
  category: terminal
---

# 🌀 an Interactive Terminal for AI (interminai)

Author: Michael S. Tsirkin <mst@kernel.org>

A terminal proxy for interactive CLI applications. See [examples.md](examples.md) and [reference.md](reference.md) for details.

## When to Use

**Use for interactive commands** that wait for input, show menus/prompts, or use full-screen interfaces (vim, git rebase -i, htop, apt, w3m).

**Use if you get errors like this "Warning: Output is not to a terminal" or "Warning: Input is not from a terminal".

**Don't use** for simple commands that just run and exit - use Shell instead.

## Quick Start

```bash
# 1. Start session (prints socket path to use in subsequent commands)
./scripts/interminai start -- vim /tmp/test.txt
# Output:
#   PID: 12345
#   Socket: /tmp/interminai-aBc123/socket
#   Auto-generated: true

# 2. Use the socket path shown above for all subsequent commands
./scripts/interminai input --socket /tmp/interminai-aBc123/socket --text ':wq\r'

# 3. Check screen
./scripts/interminai output --socket /tmp/interminai-aBc123/socket

# 4. Clean up (always!)
./scripts/interminai stop --socket /tmp/interminai-aBc123/socket
```

Just read the socket path from the `start` output and use it directly - no need to parse into variables.

## Essential Commands

- `start -- COMMAND` - Start application (prints socket path on stdout)
- `input --socket PATH --text 'text'` - Send input (escapes: `\r` `\n` `\e` `\t` `\xHH` see also: "Pressing Enter")
- `output --socket PATH` - Get screen (80x25 by default, add `--cursor print` for cursor position)
- `status --socket PATH` - Check running state and activity flag
- `status --socket PATH --quiet` - Check if running (exit 0) or exited (exit 1, prints exit code)
- `wait --socket PATH` - Wait for activity (any output), prints activity and exit status
- `wait --socket PATH --quiet` - Wait for process to exit (prints exit code)
- `wait --socket PATH --line N` - Wait until line N changes (1-based)
- `wait --socket PATH --line N --not-contains PATTERN` - Wait until line N does NOT contain PATTERN
- `wait --socket PATH --line N --contains PATTERN` - Wait until line N contains PATTERN
- `stop --socket PATH` - Stop session (also cleans up auto-generated socket)

## Key Best Practices

1. **Auto-generated sockets**: Don't specify `--socket` on start, read the path from output
2. **Always clean up**: `stop` when done (auto-cleans socket)
3. **Check output after each input** - don't blindly chain commands
4. **Add delays**: `sleep 0.2` after input for processing
5. **Set GIT_EDITOR=vim** for git rebase -i, git commit, etc.
6. **If screen garbled**: Send `\f` (Ctrl+L) to redraw
7. **Wait for updates**: If screen isn't updating, use `timeout 10 interminai wait --socket PATH` instead of repeatedly calling `output`
8. **Output is limited**: No need to pipe to head/tail - output always ever gives you one screen. 25 lines by default.

## Checking Activity (Recommended for LLMs)

Use `status` to check if there's new terminal output without blocking. This is
useful if you are running e.g. LLMs like Claude or Codex and want to decide
whether to fetch new output or wait longer.

```bash
./scripts/interminai status --socket /tmp/interminai-xxx/socket
# Output:
#   Running: true
#   Activity: true
```

**Pattern for efficient polling:**

```bash
# After sending input, check if there's activity before fetching output
./scripts/interminai input --socket $SOCK --text 'make build\r'
sleep 0.5

# Check activity without blocking
./scripts/interminai status --socket $SOCK
# If Activity: true, fetch output
# If Activity: false, wait longer or send more input
```

This avoids repeatedly calling `output` when nothing has changed, saving context window
space and reducing noise. The activity flag is set when PTY output is received and
cleared by `status` or `wait`.

## Waiting for CLI LLM Idle State (cursor-agent, codex, etc.)

When supervising CLI LLMs like cursor-agent, you need to detect when they finish
processing and are waiting for input.

**Busy/Idle Indicators by CLI LLM:**

| CLI | Busy Pattern | Idle Pattern |
|-----|-------------|--------------|
| **cursor-agent** | `ctrl+c to stop` on input line | `→ Add a follow-up` |
| **codex** | `• Working (Ns • esc to interrupt)` | `›` prompt, "100% context left" |
| **gemini** | `⠋ <action> (esc to cancel, Ns)` | `>` in input box |
| **claude** | `✶ <word>… (ctrl+c to interrupt · Ns)` | `❯` prompt |

**Approval prompts:**
- **cursor-agent**: "Run this command?" dialog
- **codex**: Shows command and waits for y/n
- **gemini**: "Allow execution of: ..." modal with options
- **claude**: Permission prompts (unless using --dangerously-skip-permissions)

**Detection Strategy** (line-based wait):

1. Find the line number containing the input prompt (e.g., line with `ctrl+c to stop`)
2. Wait until that line no longer contains `ctrl+c to stop`

**Example: Supervising cursor-agent**

```bash
# Start cursor-agent
./scripts/interminai start --size 120x40 -- cursor-agent
# Output: Socket: /tmp/interminai-xxx/socket

SOCK=/tmp/interminai-xxx/socket

# Send a prompt
./scripts/interminai input --socket $SOCK --text 'Write hello world in Python'
sleep 0.1
./scripts/interminai input --socket $SOCK --text '\r'

# Find the line with ctrl+c to stop (the input prompt line during generation)
# This line number may vary based on screen content
./scripts/interminai output --socket $SOCK --no-color > /tmp/screen.txt
INPUT_LINE=$(grep -n 'ctrl+c to stop' /tmp/screen.txt | head -1 | cut -d: -f1)

# Wait for that line to no longer contain 'ctrl+c to stop'
timeout 120 ./scripts/interminai wait --socket $SOCK \
  --line $INPUT_LINE --not-contains 'ctrl+c to stop'

# Now cursor-agent is idle (or showing approval prompt), check output
SCREEN=$(./scripts/interminai output --socket $SOCK --no-color)

# Check what state we're in
if echo "$SCREEN" | grep -q 'Run this command?'; then
  # Approval prompt - approve with 'y' or skip with 'n'
  ./scripts/interminai input --socket $SOCK --text 'y'
else
  # Idle - ready for next command
  echo "cursor-agent is idle"
fi
```

**Why line-based?** The input line number stays relatively stable during generation.
Waiting for that specific line to change avoids false positives from pattern matches
elsewhere on screen.

## Terminal Size

Default terminal size is 80x24. If not enough context fits on screen, use `--size` on start or `resize` to increase the window. Don't go overboard to avoid filling your context with excessive output.

```bash
# Start with larger terminal
./scripts/interminai start --size 80x256 -- COMMAND

# Or resize during session (use socket path from start output)
./scripts/interminai resize --socket /tmp/interminai-xxx/socket --size 80x256
```

## Vim Navigation Tips

Exact counts for `h`/`j`/`k`/`l` are critical - cursor position after `dd` isn't always intuitive. Prefer:

- `:<number>` - Go to line directly (`:5\rdd`)
- `/<pattern>` - Search for text (`/goodbye\rdd`)
- `gg`/`G` - Anchor from known position
- `--cursor print` - Check position after operations
- `:%s/old/new/gc` - Search and replace with confirmation (`y`/`n` for each match)

## Complex Edits Shortcut

For complex multi-line edits, another option is to edit outside vim:

1. Use `output` to observe the file name
2. Use the Edit tool to modify the file directly
3. In vim, reload the file (`:e!\r`) or simply exit (`:q!\r`)

This avoids tricky vim navigation for large or intricate changes.

However, if editing is going to use sed anyway, using :%s/old/new/gc within vim
is more robust and more powerful as it shows you each change.

## Pressing Enter: `\n` vs `\r`

Traditional Unix apps accept either `\n` (LF) or `\r` (CR) for Enter because the
kernel TTY driver translates CR to LF when the ICRNL flag is set (default in
"cooked" mode). However, some modern apps (especially React/Ink-based TUIs like
cursor-agent) run in raw mode with ICRNL disabled, and only recognize `\r`.

**Best practice**: Always use `\r` for Enter/submit. It works universally:
- Traditional apps: kernel translates `\r` → `\n` (if ICRNL set)
- Raw-mode apps: receive `\r` directly as expected

Use `\n` only when you specifically want to add a newline to multiline input
(like continuing to type on a new line without submitting).

```bash
# Submit a command (use \r)
./scripts/interminai input --socket /tmp/interminai-xxx/socket --text 'hello world\r'

# Multiline input (use \n for newlines, \r to submit)
./scripts/interminai input --socket /tmp/interminai-xxx/socket --text 'line1\nline2\nline3\r'
```

## Menu prompts needing Enter

For git add -i/-p, the menu shown is not interactive, an action does not
take effect until you press enter. For example:

- Stage this hunk [y,n,q,a,d,K,j,J,g,/,e,?]?

Actually expects `y` followed by Enter and will not take effect until Enter is sent.

If you observe a tool is waiting for Enter once, it is safe to assume
it will be waiting for it next time, too.

## Modern TUI Apps (Ink/React-based)

Apps built with React/Ink (like cursor-agent) need a delay between typing text
and pressing Enter. Sending text and Enter in a single input call doesn't work
because React's internal state isn't ready for the Enter keystroke.

**Key finding**: Output polling alone is NOT sufficient. Even after text appears
on screen, React's state machine may not be ready. A time delay is required.

**Simple pattern (recommended)**:

```bash
# Send text, wait, then send Enter
./scripts/interminai input --socket /tmp/interminai-xxx/socket --text 'your prompt here'
sleep 0.1
./scripts/interminai input --socket /tmp/interminai-xxx/socket --text '\r'
```

**Why this works**: The 100ms delay gives React's event loop time to process the
input and update its internal state before receiving the Enter keystroke.

Use `debug` command to check if app is in raw mode (no ICRNL flag).

## Long lived shell sessions

It is possible to create a shell interminai session and pass commands to it.

**Tip**: Sudo caches credentials per-TTY. Each `interminai start` creates a new PTY,
so sudo prompts every time even if you recently authenticated elsewhere. Use a
long-lived shell session to run multiple sudo commands with a single password prompt.

```bash
GIT_EDITOR=vim ./scripts/interminai start -- bash
# Output shows: Socket: /tmp/interminai-xxx/socket

sleep 0.5
./scripts/interminai output --socket /tmp/interminai-xxx/socket
# ... send commands now, using the socket path from above ...
./scripts/interminai input --socket /tmp/interminai-xxx/socket --text 'vim foo.txt\r'
./scripts/interminai input --socket /tmp/interminai-xxx/socket --text ':wq\r'
./scripts/interminai input --socket /tmp/interminai-xxx/socket --text 'vim bar.txt\r'
./scripts/interminai input --socket /tmp/interminai-xxx/socket --text ':wq\r'
./scripts/interminai input --socket /tmp/interminai-xxx/socket --text 'exit\r'
./scripts/interminai wait --socket /tmp/interminai-xxx/socket
```

## Git Example

```bash
GIT_EDITOR=vim ./scripts/interminai start -- git rebase -i HEAD~3
# Output shows: Socket: /tmp/interminai-xxx/socket

sleep 0.5
./scripts/interminai output --socket /tmp/interminai-xxx/socket
# ... edit with input commands, using the socket path from above ...
./scripts/interminai input --socket /tmp/interminai-xxx/socket --text ':wq\r'
./scripts/interminai wait --socket /tmp/interminai-xxx/socket
```

**Piping output**: By default, output includes colors - do NOT use `--no-color` for normal viewing.
Only add `--no-color` when piping to grep/head/tail to avoid ANSI escape corruption:

```bash
# Normal viewing - no --no-color flag:
./scripts/interminai output --socket /tmp/interminai-xxx/socket

# Piping to grep/head/tail - add --no-color:
./scripts/interminai output --socket /tmp/interminai-xxx/socket --no-color | grep pattern
./scripts/interminai output --socket /tmp/interminai-xxx/socket --no-color | tail -5
```

See [reference.md](reference.md) for full command documentation.

## Password Input

When a command prompts for a password (sudo, ssh, etc.), **do not** try to handle the
password yourself. Instead, tell the user to run `interminai input --password` themselves:

```bash
./scripts/interminai start -- sudo apt update
# Output shows: Socket: /tmp/interminai-xxx/socket

sleep 0.5
./scripts/interminai output --socket /tmp/interminai-xxx/socket
# Shows: [sudo] password for user:

# IMPORTANT: Tell the user to run interminai input --password
echo "Password required. Please run: interminai input --socket /tmp/interminai-xxx/socket --password"
# User runs the command, types password, and it's sent to sudo

./scripts/interminai wait --socket /tmp/interminai-xxx/socket
```

The `--password` flag:
- Prompts user to type password and press Enter to submit (sent as `\r`)
- Reads input with echo disabled (password not visible)
