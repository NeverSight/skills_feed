---
name: asciinema-recorder
description: Record Claude Code sessions with asciinema. TRIGGERS - record session, asciinema record, capture terminal, demo recording.
allowed-tools: Read, Bash, Glob, AskUserQuestion
---

# asciinema-recorder

Generate ready-to-copy commands for recording Claude Code sessions with asciinema. Dynamically creates filenames based on workspace and datetime.

> **Platform**: macOS, Linux (requires asciinema CLI)

## When to Use This Skill

Use this skill when:

- Starting a new terminal recording session
- Creating demos or documentation recordings
- Capturing Claude Code sessions for review or sharing
- Generating workspace-specific recording filenames

---

## Why This Skill?

This skill generates ready-to-copy recording commands with:

- Dynamic workspace-based filename
- Datetime stamp for uniqueness
- Saves to project's tmp/ folder (gitignored)

---

## Requirements

| Component         | Required | Installation             |
| ----------------- | -------- | ------------------------ |
| **asciinema CLI** | Yes      | `brew install asciinema` |

---

## Workflow Phases

### Phase 0: Preflight Check

**Purpose**: Verify asciinema is installed.

```bash
# Check asciinema CLI
which asciinema && asciinema --version
```

If asciinema is NOT installed, use AskUserQuestion:

- question: "asciinema not found. How would you like to proceed?"
  header: "Setup"
  multiSelect: false
  options:
  - label: "Install asciinema (Recommended)"
    description: "Run: brew install asciinema (macOS) or apt install asciinema (Linux)"
  - label: "Show manual instructions"
    description: "Display installation commands for all platforms"
  - label: "Cancel"
    description: "Exit without recording"

Based on selection:

- **"Install asciinema"** → Run appropriate install command based on OS:

  ```bash
  # macOS
  brew install asciinema

  # Linux (apt)
  sudo apt install asciinema

  # Linux (pip)
  pip install asciinema
  ```

  Then proceed to Phase 1.0.

- **"Show manual instructions"** → Display the commands above, then exit skill.

- **"Cancel"** → Exit skill without action.

---

### Phase 1.0: Recording Location

**Purpose**: Let user choose where to save the recording.

Use AskUserQuestion:

- question: "Where should the recording be saved?"
  header: "Location"
  multiSelect: false
  options:
  - label: "$PWD/tmp/ (Recommended)"
    description: "Project tmp directory (gitignored)"
  - label: "~/asciinema/"
    description: "Global recordings directory"
  - label: "Custom path"
    description: "Specify your own directory"

Based on selection:

- **"$PWD/tmp/"** → Set `OUTPUT_DIR="$PWD/tmp"`
- **"~/asciinema/"** → Set `OUTPUT_DIR="$HOME/asciinema"` and create if missing: `mkdir -p ~/asciinema`
- **"Custom path"** → Use user's "Other" input as `OUTPUT_DIR`

---

### Phase 1.1: Recording Options

**Purpose**: Let user configure recording behavior.

Use AskUserQuestion:

- question: "Which recording options would you like?"
  header: "Options"
  multiSelect: true
  options:
  - label: "Add title/description"
    description: "Include session title in recording metadata (-t flag)"
  - label: "Disable idle time limit"
    description: "Keep full pauses instead of 2s max (--idle-time-limit 0)"
  - label: "Quiet mode"
    description: "Suppress asciinema status messages (-q flag)"

Based on selections, build command flags:

- **"Add title"** → Continue to title selection question, add `-t "title"` flag
- **"Disable idle time limit"** → Add `--idle-time-limit 0` flag
- **"Quiet mode"** → Add `-q` flag

**If "Add title" was selected**, follow up with:

- question: "Enter a title for this recording:"
  header: "Title"
  multiSelect: false
  options:
  - label: "Use workspace name"
    description: "Title: ${WORKSPACE}"
  - label: "Use workspace + datetime"
    description: "Title: ${WORKSPACE} ${DATETIME}"
  - label: "Custom title"
    description: "Enter your own title"

Based on title selection:

- **"Use workspace name"** → Set `TITLE="${WORKSPACE}"`
- **"Use workspace + datetime"** → Set `TITLE="${WORKSPACE} ${DATETIME}"`
- **"Custom title"** → Use user's "Other" input as `TITLE`

---

### Phase 1.2: Detect Context & Generate Command

**Purpose**: Generate a copy-paste ready recording command.

#### Step 1.2.1: Detect Workspace

Extract workspace name from `$PWD`:

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF'
WORKSPACE=$(basename "$PWD")
echo "Workspace: $WORKSPACE"
SKILL_SCRIPT_EOF
```

#### Step 1.2.2: Generate Datetime

```bash
/usr/bin/env bash << 'SKILL_SCRIPT_EOF_2'
DATETIME=$(date +%Y-%m-%d_%H-%M)
echo "Datetime: $DATETIME"
SKILL_SCRIPT_EOF_2
```

#### Step 1.2.3: Ensure Output Directory Exists

Create the output directory selected in Phase 1.0:

```bash
mkdir -p "${OUTPUT_DIR}"
```

#### Step 1.2.4: Construct Command

Build the recording command using:

- `OUTPUT_DIR` from Phase 1.0 (location selection)
- Flags from Phase 1.1 (options selection)
- `TITLE` if "Add title" was selected

```bash
# Base command
CMD="asciinema rec"

# Add flags from Phase 1.1 options
# (Claude builds this based on user selections)

# Final command format:
asciinema rec ${FLAGS} "${OUTPUT_DIR}/${WORKSPACE}_${DATETIME}.cast"
```

**Example outputs:**

```bash
# Default (no options selected):
asciinema rec /home/user/projects/my-app/tmp/my-app_2025-12-21_14-30.cast

# With title + quiet mode:
asciinema rec -t "my-app Demo" -q /home/user/projects/my-app/tmp/my-app_2025-12-21_14-30.cast

# With all options:
asciinema rec -t "my-app 2025-12-21 14:30" -q --idle-time-limit 0 ~/asciinema/my-app_2025-12-21_14-30.cast
```

---

### Phase 2: User Guidance

**Purpose**: Explain the recording workflow step-by-step.

Present these instructions:

```markdown
## Recording Instructions

1. **Exit Claude Code** - Type `exit` or press `Ctrl+D`
2. **Copy the command** shown above
3. **Paste and run** in your terminal (starts a recorded shell)
4. **Run `claude`** to start Claude Code inside the recording
5. Work normally - everything is captured
6. **Exit Claude Code** - Type `exit` or press `Ctrl+D`
7. **Exit the recording shell** - Type `exit` or press `Ctrl+D` again

Your recording will be saved to:
`$PWD/tmp/{workspace}_{datetime}.cast`
```

---

### Phase 3: Additional Info

**Purpose**: Provide helpful tips for after recording.

```markdown
## Tips

- **Environment variable**: `ASCIINEMA_REC=1` is set during recording
- **Playback**: Use `asciinema-player` skill or `asciinema play file.cast`
- **Upload (optional)**: `asciinema upload file.cast` (requires account)
- **Markers**: Add `asciinema marker` during recording for navigation points
```

---

## TodoWrite Task Templates

### Template: Record Claude Code Session

```
1. [Preflight] Check asciinema CLI installed
2. [Preflight] Offer installation if missing
3. [Context] Detect current workspace from $PWD
4. [Context] Generate datetime slug
5. [Context] Ensure tmp/ directory exists
6. [Command] Construct full recording command
7. [Guidance] Display step-by-step instructions
8. [Guidance] Show additional tips (playback, upload)
9. Verify against Skill Quality Checklist
```

---

## Post-Change Checklist

After modifying this skill:

1. [ ] Command generation still uses `$PWD` (no hardcoded paths)
2. [ ] Guidance steps remain clear and platform-agnostic
3. [ ] TodoWrite template matches actual workflow
4. [ ] README.md entry remains accurate
5. [ ] Validate with quick_validate.py

---

## CLI Options Reference

| Option | Flag | Description                         |
| ------ | ---- | ----------------------------------- |
| Title  | `-t` | Recording title (for asciinema.org) |
| Quiet  | `-q` | Suppress status messages            |
| Append | `-a` | Append to existing recording        |

---

## Troubleshooting

### "Cannot record from within Claude Code"

**Cause**: asciinema must wrap the program, not be started from inside.

**Fix**: Exit Claude Code first, then run the generated command.

### "Recording file too large"

**Cause**: Long sessions produce large files.

**Fix**:

- Use `asciinema upload` to store online instead of locally
- Split long sessions into smaller recordings

### "Playback shows garbled output"

**Cause**: Terminal size mismatch.

**Fix**: Use `-r` flag during playback to resize terminal.

---

## Reference Documentation

- [asciinema CLI Documentation](https://docs.asciinema.org/manual/cli/)
- [asciinema Markers](https://docs.asciinema.org/manual/cli/markers/)
