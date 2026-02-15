---
name: vhs
description: >-
  Record terminal sessions as GIF/MP4/WebM using VHS (Charm.sh).
  Use when: create demo GIF, record terminal, terminal recording, demo video,
  tape file, animate CLI, screencast terminal, showcase command output,
  README demo, document CLI tool, generate terminal animation.
---

# VHS — Terminal Recorder

[VHS](https://github.com/charmbracelet/vhs) records terminal sessions from declarative `.tape` files.
Produces GIF, MP4, or WebM. No screen recording needed — deterministic and reproducible.

## Install

```bash
scoop install vhs    # Windows
brew install vhs     # macOS
```

Requires `ffmpeg` (for video encoding). `scoop install ffmpeg` if missing.

## Quick Start

```bash
# Create example tape
vhs new demo.tape

# Record
vhs demo.tape

# Validate without running
vhs validate demo.tape

# Publish to vhs.charm.sh (get shareable URL)
vhs publish demo.gif
```

## Tape File Syntax

### Output

```tape
Output demo.gif                    # GIF (default, best for READMEs)
Output demo.mp4                    # MP4 video
Output demo.webm                   # WebM video
```

Multiple `Output` lines = multiple formats from one tape.

### Settings

```tape
Set Shell "bash"                   # Shell to use
Set FontSize 14                    # Font size (default 22 — too large for most)
Set FontFamily "JetBrains Mono"    # Font family
Set Width 1200                     # Terminal width in pixels
Set Height 600                     # Terminal height in pixels
Set Padding 15                     # Padding around terminal
Set TypingSpeed 50ms               # Delay between keystrokes (default 50ms)
Set Theme "Dracula"                # Color theme (see Themes below)
Set Framerate 30                   # GIF framerate
Set PlaybackSpeed 1.0              # Playback speed multiplier
Set LoopOffset 80%                 # Where GIF loop restarts (% from end)
Set WindowBar "Colorful"           # Window bar: Rings, RingsRight, Colorful, ColorfulRight
Set WindowBarSize 40               # Window bar height in pixels
Set BorderRadius 8                 # Terminal border radius
Set MarginFill "#1a1a2e"           # Background color outside terminal
Set Margin 20                      # Margin size (needs MarginFill)
```

### Commands

```tape
Type "echo hello"                  # Type characters
Type@100ms "slow typing"           # Type with custom speed
Enter                              # Press Enter
Enter 3                            # Press Enter 3 times
Sleep 2s                           # Wait 2 seconds
Sleep 500ms                        # Wait 500 milliseconds

# Special keys
Backspace 5                        # Delete 5 chars
Tab                                # Tab completion
Ctrl+C                             # Interrupt
Ctrl+L                             # Clear screen
Up                                 # Arrow up (history)
Down                               # Arrow down
Left 3                             # Move cursor left 3
Right 3                            # Move cursor right 3
Escape                             # Escape key
Space                              # Space key
PageUp                             # Page up
PageDown                           # Page down

# Visibility
Hide                               # Hide commands from output
Show                               # Show commands again
```

### Require

```tape
Require git                        # Fail if git not in PATH
Require node
```

## Windows: Use `Set Shell "cmd"`

VHS's default `bash` resolves to WSL bash on Windows — a separate environment with no access to Windows-installed tools (node, scoop packages, etc.). **Always use `cmd`** on Windows:

```tape
Set Shell "cmd"
```

This gives VHS the full Windows PATH so all installed CLIs work.

## Recommended Defaults

For README demos and documentation:

```tape
Output demo.gif
Set Shell "cmd"                    # Windows — use "bash" on Linux/macOS
Set FontSize 14
Set Width 1100
Set Height 600
Set Theme "Dracula"
Set TypingSpeed 30ms
Set Padding 15
Set WindowBar "Colorful"
Set BorderRadius 8
```

## Patterns

### Simple command showcase

```tape
Output demo.gif
Set Shell "bash"
Set FontSize 14
Set Width 1100
Set Height 600
Set Theme "Dracula"
Set TypingSpeed 30ms
Set Padding 15

Type "my-tool --help"
Enter
Sleep 3s

Type "my-tool run --input data.json"
Enter
Sleep 5s
```

### Complex commands (use a wrapper script)

VHS tape files don't support shell quoting well. For complex commands
with quotes, pipes, or multi-line args, write a helper script:

```bash
# demo-run.sh
#!/bin/bash
echo "Running analysis..."
my-tool analyze --format json | jq '.results[] | .name'
```

```tape
Type "bash demo-run.sh"
Enter
Sleep 10s
```

### Hide setup, show the interesting part

```tape
# Setup (hidden from recording)
Hide
Type "cd /tmp/demo-project"
Enter
Type "export DEMO_MODE=1"
Enter
Sleep 1s
Show

# Visible demo starts here
Type "my-tool init"
Enter
Sleep 3s
```

### Before/after comparison

```tape
Type "# Before:"
Enter
Type "cat config.yaml"
Enter
Sleep 3s

Type "# After running fix:"
Enter
Type "my-tool fix config.yaml"
Enter
Sleep 3s

Type "cat config.yaml"
Enter
Sleep 3s
```

### Recording live (interactive)

```bash
# Record your terminal actions into a tape file
vhs record > my-session.tape
# Then edit the tape to clean up timing, add sleeps, etc.
vhs my-session.tape
```

### Recording TUI apps with holdpty

Use [holdpty](https://github.com/marcfargas/holdpty) to record full-color TUI applications — apps that need a real PTY for colors, take time to start, or are already running. holdpty provides the PTY, VHS captures the output.

**Why this matters:**

- TUI apps (pi, htop, k9s, lazygit) need a real PTY for colors and layout
- Slow-starting apps (AI agents, servers) can be ready before recording begins
- Already-running processes can be recorded on demand for monitoring/sharing

**The pattern:**

```bash
# Step 1: Launch the app in holdpty (or it's already running)
holdpty launch --bg --name demo -- my-tui-app

# Step 2: Wait for it to be ready (or it already is)
sleep 5

# Step 3: Record with VHS
vhs record-demo.tape

# Step 4: Clean up (or leave it running)
holdpty stop demo
```

**Tape file — attach to a running session:**

```tape
Output demo.gif
Output demo.mp4
Set Shell "cmd"
Set FontSize 14
Set Width 1200
Set Height 700
Set Theme "Dracula"
Set Padding 15
Set WindowBar "Colorful"
Set BorderRadius 8

# Attach to the running holdpty session
Type "holdpty attach demo"
Enter
Sleep 2s

# Interact with the app (VHS types, app responds with full TUI)
Type "your input here"
Enter
Sleep 15s
```

**Tape file — view-only snapshot of a running process:**

```tape
Output snapshot.gif
Set Shell "cmd"
Set FontSize 14
Set Width 1200
Set Height 700
Set Theme "Dracula"
Set Padding 15

# View is read-only — just captures current output
Type "holdpty view demo"
Enter
Sleep 10s
Ctrl+C
```

**Use cases:**

- **README demos** — launch app, let it start, record the interesting part
- **Monitoring snapshots** — capture what a running service looks like right now
- **Bug reports** — record a live reproduction with full colors
- **Agent recordings** — capture an AI agent working with its full TUI (thinking indicators, tool calls, colored output)

> On Windows, use `node.exe <path/to/cli.js>` instead of CLI names when launching via holdpty — see the [holdpty skill](https://github.com/marcfargas/holdpty) for the `.cmd` wrapper gotcha.

## Themes

Popular themes for demos:

| Theme | Style |
|-------|-------|
| `Dracula` | Dark purple — high contrast, popular |
| `Catppuccin Mocha` | Dark warm — modern, easy on eyes |
| `Tokyo Night` | Dark blue — clean |
| `Nord` | Dark muted — professional |
| `Gruvbox Dark` | Dark warm/retro |
| `Solarized Dark` | Classic |
| `GitHub Dark` | Familiar to devs |
| `One Dark` | VS Code-like |

List all: `vhs themes`

## Tips

1. **FontSize 14** — default 22 is way too large for most demos
2. **TypingSpeed 25-40ms** — 50ms default feels slow; 25ms is snappy
3. **Sleep after Enter** — always add `Sleep` after commands to let output render
4. **Long commands** — use wrapper scripts, VHS quoting is fragile
5. **GIF size** — keep under 5MB for GitHub READMEs; reduce Framerate, Height, or duration
6. **Multiple outputs** — one tape can produce `.gif` + `.mp4` simultaneously
7. **Publish** — `vhs publish demo.gif` gives a shareable URL on vhs.charm.sh
8. **Validate first** — `vhs validate demo.tape` catches syntax errors without recording

## Gotchas

- **Windows: `Set Shell "bash"` uses WSL** — VHS resolves `bash` to WSL bash, not Git Bash. Use `Set Shell "cmd"` to get the full Windows PATH. Custom shell paths (`Set Shell "C:/path/to/bash.exe"`) are rejected.
- **No shell expansion in Type** — `Type "echo $HOME"` types the literal string; variable expansion happens when bash executes it, not in the tape
- **Quoting** — avoid nested quotes in Type. Use wrapper scripts for complex commands
- **Windows paths** — use forward slashes in Type strings (`C:/dev/...` not `C:\dev\...`)
- **Long recordings** — GIFs get huge fast. Keep demos under 30 seconds. Use `Set PlaybackSpeed 2.0` to compress
- **Terminal size** — if output wraps weird, increase Width or reduce FontSize
- **TUI apps without holdpty** — apps that need a real PTY for colors (pi, htop, lazygit) will render without colors if launched directly from VHS. Use the holdpty pattern above.
