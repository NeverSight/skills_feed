---
name: iterm2-layout
description: Configure iTerm2 workspace layouts with TOML. TRIGGERS - iTerm2 layout, workspace tabs, layout.toml, AutoLaunch.
---

# iTerm2 Layout Configuration

<!-- ADR: /docs/adr/2025-12-15-iterm2-layout-config.md -->

Configure iTerm2 workspace layouts with proper separation of concerns: private paths in TOML config, publishable code in Python script.

## When to Use This Skill

Use this skill when:

- Configuring iTerm2 workspace layouts
- Adding, removing, or modifying workspace tabs
- Setting up AutoLaunch scripts for iTerm2
- Configuring git worktree tab auto-discovery

## Configuration Overview

### File Locations

| File             | Location                               | Purpose                |
| ---------------- | -------------------------------------- | ---------------------- |
| Config (private) | `~/.config/iterm2/layout.toml`         | User's workspace paths |
| Script (public)  | `~/scripts/iterm2/default-layout.py`   | Layout logic           |
| Template         | `~/scripts/iterm2/layout.example.toml` | Example config         |

### Config File Format

```toml
# ~/.config/iterm2/layout.toml

[layout]
left_pane_ratio = 0.20    # 0.0 to 1.0
settle_time = 0.3         # seconds

[commands]
left = "br --sort-by-type-dirs-first"
right = "zsh"

[worktrees]
# Optional: Enable git worktree discovery
# main_repo_root = "~/projects/my-project"
# worktree_pattern = "my-project.worktree-*"

[[tabs]]
name = "home"
dir = "~"

[[tabs]]
name = "projects"
dir = "~/projects"

[[tabs]]
dir = "~/Documents"  # name defaults to "Documents"
```

## Setup Instructions

### First-Time Setup

```bash
/usr/bin/env bash << 'CONFIG_EOF'
# 1. Ensure config directory exists
mkdir -p ~/.config/iterm2

# 2. Copy template
cp ~/scripts/iterm2/layout.example.toml ~/.config/iterm2/layout.toml

# 3. Edit with your workspace paths
# Add [[tabs]] entries for each workspace

# 4. Restart iTerm2 to test
CONFIG_EOF
```

### Adding a New Tab

Add a `[[tabs]]` entry to `~/.config/iterm2/layout.toml`:

```toml
[[tabs]]
name = "MyProject"  # Tab display name (optional)
dir = "~/path/to/project"
```

**Name field**:

- If omitted, uses directory basename
- Custom names useful for abbreviations (e.g., "AF" instead of "alpha-forge")

### Removing a Tab

Delete or comment out the `[[tabs]]` entry:

```toml
# [[tabs]]
# name = "OldProject"
# dir = "~/old/project"
```

## Configuration Schema

| Section       | Key                | Type   | Default        | Description               |
| ------------- | ------------------ | ------ | -------------- | ------------------------- |
| `[layout]`    | `left_pane_ratio`  | float  | 0.20           | Left pane width (0.0-1.0) |
| `[layout]`    | `settle_time`      | float  | 0.3            | Wait after cd (seconds)   |
| `[commands]`  | `left`             | string | br...          | Left pane command         |
| `[commands]`  | `right`            | string | zsh            | Right pane command        |
| `[worktrees]` | `alpha_forge_root` | string | null           | Worktree root (optional)  |
| `[worktrees]` | `worktree_pattern` | string | `*.worktree-*` | Glob pattern              |
| `[[tabs]]`    | `dir`              | string | **required**   | Directory path            |
| `[[tabs]]`    | `name`             | string | basename       | Tab display name          |

## Troubleshooting

### Error: "Layout configuration not found"

**Symptom**: Script Console shows error about missing config

**Solution**:

```bash
# Create config from template
cp ~/scripts/iterm2/layout.example.toml ~/.config/iterm2/layout.toml
```

### Error: "Invalid TOML syntax"

**Symptom**: Script Console shows TOML parse error

**Solution**:

1. Check TOML syntax (quotes, brackets)
2. Validate with: `python3 -c "import tomllib; tomllib.load(open('~/.config/iterm2/layout.toml', 'rb'))"`

### Tabs Not Appearing

**Symptom**: iTerm2 opens but no custom tabs created

**Causes**:

1. No `[[tabs]]` entries in config
2. Config file in wrong location
3. Script not in AutoLaunch

**Solution**:

```bash
# Verify config location
ls -la ~/.config/iterm2/layout.toml

# Verify AutoLaunch symlink
ls -la ~/Library/Application\ Support/iTerm2/Scripts/AutoLaunch/

# Check Script Console for errors
# iTerm2 > Scripts > Manage > Console
```

### Directory Does Not Exist Warning

**Symptom**: Tab skipped with warning in Script Console

**Solution**: Verify directory path exists or create it:

```bash
mkdir -p ~/path/to/missing/directory
```

## Error Handling Behavior

The script uses "print + early return" pattern:

1. **Missing config**: Logs instructions to Script Console, exits cleanly
2. **Invalid TOML**: Logs parse error with details, exits cleanly
3. **Missing directory**: Logs warning, skips tab, continues with others

**Viewing errors**: Scripts > Manage > Console in iTerm2

## Git Worktree Detection (Optional)

Enable dynamic tab creation for git worktrees:

```toml
[worktrees]
main_repo_root = "~/projects/my-project"
worktree_pattern = "my-project.worktree-*"
```

**How it works**:

1. Script globs for `~/projects/my-project.worktree-*` directories
2. Validates each against `git worktree list`
3. Generates acronym-based tab names (e.g., `AF-ssv` for `sharpe-statistical-validation`)
4. Inserts worktree tabs after main project tab

## References

- [iTerm2 Python API](https://iterm2.com/python-api/)
- [TOML Specification](https://toml.io/)
- [XDG Base Directory Spec](https://specifications.freedesktop.org/basedir-spec/basedir-spec-latest.html)
- [ADR: iTerm2 Layout Config](/docs/adr/2025-12-15-iterm2-layout-config.md)
