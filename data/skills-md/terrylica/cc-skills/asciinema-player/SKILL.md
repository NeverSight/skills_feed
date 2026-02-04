---
name: asciinema-player
description: Play .cast terminal recordings in iTerm2. TRIGGERS - asciinema play, .cast file, play recording, recording playback.
allowed-tools: Read, Bash, Glob, AskUserQuestion
---

# asciinema-player

Play terminal session recordings (.cast files) in a dedicated iTerm2 window with full playback controls. Opens a **clean window** (bypasses default arrangements) for distraction-free viewing.

> **Platform**: macOS only (requires iTerm2)

## When to Use This Skill

Use this skill when:

- Playing back .cast recordings in iTerm2
- Reviewing session recordings without browser limitations
- Handling large recordings (>100MB) that crash browser players
- Demoing or reviewing terminal sessions

---

## Why iTerm2 Instead of Browser?

| Aspect               | Browser Player          | iTerm2 CLI        |
| -------------------- | ----------------------- | ----------------- |
| Large files (>100MB) | Crashes (memory limit)  | Streams from disk |
| Memory usage         | 2-4GB for 700MB file    | Minimal           |
| Startup time         | Slow (download + parse) | Instant           |
| Native feel          | Web-based               | True terminal     |

**Decision**: iTerm2 CLI is the only reliable method for large recordings.

---

## Requirements

| Component         | Required | Installation                 |
| ----------------- | -------- | ---------------------------- |
| **iTerm2**        | Yes      | `brew install --cask iterm2` |
| **asciinema CLI** | Yes      | `brew install asciinema`     |

> **Note**: This skill is macOS-only. Linux users should run `asciinema play` directly in their terminal.

---

## Workflow Phases (ALL MANDATORY)

**IMPORTANT**: All phases are MANDATORY. Do NOT skip any phase. AskUserQuestion MUST be used at each decision point.

### Phase 0: Preflight Checks

**Purpose**: Verify iTerm2 and asciinema are installed.

#### Step 0.1: Check Dependencies

```bash
# Check iTerm2 is installed
ls -d /Applications/iTerm.app 2>/dev/null && echo "iTerm2: OK" || echo "iTerm2: MISSING"

# Check asciinema CLI
which asciinema && asciinema --version
```

#### Step 0.2: Report Status and Ask for Installation

**MANDATORY AskUserQuestion** if any dependency is missing:

```
Question: "Required dependencies are missing. Install them?"
Header: "Setup"
Options:
  - Label: "Install all (Recommended)"
    Description: "Will install: {list of missing: iTerm2, asciinema}"
  - Label: "Cancel"
    Description: "Abort - cannot proceed without dependencies"
```

#### Step 0.3: Install Missing Dependencies (if confirmed)

```bash
# Install iTerm2
brew install --cask iterm2

# Install asciinema CLI
brew install asciinema
```

---

### Phase 1: File Selection (MANDATORY)

**Purpose**: Discover and select the recording to play.

#### Step 1.1: Discover Recordings

```bash
# Search for .cast files in common locations
fd -e cast . --max-depth 5 2>/dev/null | head -20

# Also check common locations
ls -lh ~/scripts/tmp/*.cast 2>/dev/null
ls -lh ~/.local/share/asciinema/*.cast 2>/dev/null
ls -lh ./tmp/*.cast 2>/dev/null
```

#### Step 1.2: Get File Info

```bash
# Get file size and line count for selected file
ls -lh {file_path}
wc -l {file_path}
```

#### Step 1.3: Present File Selection (MANDATORY AskUserQuestion)

**If user provided path directly**, confirm:

```
Question: "Play this recording?"
Header: "Confirm"
Options:
  - Label: "Yes, play {filename}"
    Description: "{size}, {line_count} events"
  - Label: "Choose different file"
    Description: "Browse for other recordings"
```

**If no path provided**, discover and present options:

```
Question: "Which recording would you like to play?"
Header: "Recording"
Options:
  - Label: "{filename} ({size})"
    Description: "{line_count} events"
  - ... (up to 4 most recent)
```

---

### Phase 2: Playback Settings (MANDATORY)

**Purpose**: Configure playback options before launching iTerm2.

#### Step 2.1: Ask Playback Speed (MANDATORY AskUserQuestion)

```
Question: "Select playback speed:"
Header: "Speed"
Options:
  - Label: "2x (fast)"
    Description: "Good for review, see everything"
  - Label: "6x (very fast)"
    Description: "Quick scan of long sessions"
  - Label: "16x (ultra fast)"
    Description: "Rapid skim for 700MB+ files"
  - Label: "Custom"
    Description: "Enter your own speed multiplier"
```

**If "Custom" selected**, ask for speed value (use Other option for numeric input).

#### Step 2.2: Ask Additional Options (MANDATORY AskUserQuestion)

```
Question: "Select additional playback options:"
Header: "Options"
multiSelect: true
Options:
  - Label: "Limit idle time (2s)"
    Description: "Cap pauses to 2 seconds max (recommended)"
  - Label: "Loop playback"
    Description: "Restart automatically when finished"
  - Label: "Resize terminal"
    Description: "Match terminal size to recording dimensions"
  - Label: "Pause on markers"
    Description: "Auto-pause at marked points (for demos)"
```

---

### Phase 3: Launch in iTerm2

**Purpose**: Open clean iTerm2 window and start playback.

#### Step 3.1: Build Command

Construct the `asciinema play` command based on user selections:

```bash
# Example with all options
asciinema play -s 6 -i 2 -l -r /path/to/recording.cast
```

**Option flags:**

- `-s {speed}` - Playback speed
- `-i 2` - Idle time limit (if selected)
- `-l` - Loop (if selected)
- `-r` - Resize terminal (if selected)
- `-m` - Pause on markers (if selected)

#### Step 3.2: Launch iTerm2 Window

Use AppleScript to open a **clean window** (bypasses default arrangements):

```bash
osascript -e 'tell application "iTerm2"
    create window with default profile
    tell current window
        tell current session
            write text "asciinema play -s {speed} {options} {file_path}"
        end tell
    end tell
end tell'
```

#### Step 3.3: Display Controls Reference

```markdown
## Playback Started

**Recording:** `{filename}`
**Speed:** {speed}x
**Options:** {options_summary}

### Keyboard Controls

| Key      | Action                            |
| -------- | --------------------------------- |
| `Space`  | Pause / Resume                    |
| `Ctrl+C` | Stop playback                     |
| `.`      | Step forward (when paused)        |
| `]`      | Skip to next marker (when paused) |

### Tips

- Press `Space` to pause anytime
- Use `.` to step through frame by frame
- `Ctrl+C` to exit when done
```

---

## TodoWrite Task Template (MANDATORY)

**Load this template into TodoWrite before starting**:

```
1. [Preflight] Check iTerm2 installed
2. [Preflight] Check asciinema CLI installed
3. [Preflight] AskUserQuestion: install missing deps (if needed)
4. [Preflight] Install dependencies (if confirmed)
5. [Selection] Get file info (size, events)
6. [Selection] AskUserQuestion: confirm file selection
7. [Settings] AskUserQuestion: playback speed
8. [Settings] AskUserQuestion: additional options (multi-select)
9. [Launch] Build asciinema play command
10. [Launch] Execute AppleScript to open iTerm2
11. [Launch] Display controls reference
```

---

## CLI Options Reference

| Option     | Flag | Values              | Description                      |
| ---------- | ---- | ------------------- | -------------------------------- |
| Speed      | `-s` | 0.5, 1, 2, 6, 16... | Playback speed multiplier        |
| Idle limit | `-i` | seconds (e.g., 2)   | Cap idle/pause time              |
| Loop       | `-l` | (flag)              | Continuous loop                  |
| Resize     | `-r` | (flag)              | Match terminal to recording size |
| Markers    | `-m` | (flag)              | Auto-pause at markers            |
| Quiet      | `-q` | (flag)              | Suppress info messages           |

---

## AppleScript Reference

### Open Clean iTerm2 Window (No Default Arrangement)

```applescript
tell application "iTerm2"
    create window with default profile
    tell current window
        tell current session
            write text "your command here"
        end tell
    end tell
end tell
```

**Why this works**: `create window with default profile` creates a fresh window, bypassing any saved window arrangements.

### One-liner for Bash

```bash
osascript -e 'tell application "iTerm2"
    create window with default profile
    tell current window
        tell current session
            write text "asciinema play -s 6 -i 2 /path/to/file.cast"
        end tell
    end tell
end tell'
```

---

## Troubleshooting

### "Device not configured" error

**Cause**: Running `asciinema play` from a non-TTY context (e.g., Claude Code's Bash tool)

**Fix**: Use AppleScript to open a real iTerm2 window (this skill does this automatically)

### Recording plays too fast/slow

**Fix**: Use the speed AskUserQuestion to select appropriate speed:

- 2x for careful review
- 6x for quick scan
- 16x for ultra-fast skim of very long recordings

### iTerm2 not opening

**Cause**: iTerm2 not installed or AppleScript permissions not granted

**Fix**:

1. Install iTerm2: `brew install --cask iterm2`
2. Grant permissions: System Settings → Privacy & Security → Automation → Allow Terminal/Claude to control iTerm2

### Large file (>500MB) considerations

The CLI player streams from disk, so file size doesn't cause memory issues. However:

- Very long recordings may benefit from higher speeds (6x, 16x)
- Use `-i 2` to skip idle time
- Consider splitting very long recordings

---

## Post-Change Checklist

After modifying this skill:

1. [ ] Preflight checks verify iTerm2 and asciinema
2. [ ] AskUserQuestion phases use proper multiSelect where applicable
3. [ ] AppleScript uses heredoc wrapper for bash compatibility
4. [ ] Speed options match CLI capability (-s flag)
5. [ ] TodoWrite template matches actual workflow phases

---

## Reference Documentation

- [asciinema play Usage](https://docs.asciinema.org/manual/cli/)
- [asciinema CLI Options](https://man.archlinux.org/man/extra/asciinema/asciinema-play.1.en)
- [iTerm2 AppleScript Documentation](https://iterm2.com/documentation-scripting.html)
- [asciinema Markers](https://docs.asciinema.org/manual/cli/markers/)
