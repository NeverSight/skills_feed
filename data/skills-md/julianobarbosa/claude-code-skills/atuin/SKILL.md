---
name: atuin
description: Shell history management with Atuin. Use when configuring shell history, setting up history sync, searching command history, importing history from other shells, troubleshooting atuin issues, or optimizing history workflows. Covers installation, sync setup, search modes, statistics, and self-hosting.
---

# Atuin Skill

Magical shell history with encrypted sync across all your machines.

## Overview

Atuin replaces your shell history with a SQLite database and provides:
- Full-screen history search UI (Ctrl+R / Up arrow)
- End-to-end encrypted sync across machines
- Context logging (exit code, cwd, hostname, duration)
- Statistics and analytics
- Filter modes (session, directory, global)
- Quick navigation with Alt+number keys

## Supported Shells

| Shell | Support Level |
|-------|--------------|
| Zsh | Full |
| Bash | Full |
| Fish | Full |
| Nushell | Full |
| Xonsh | Full |

## Quick Start

### Installation

```bash
# Official installer (recommended)
curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh

# macOS (Homebrew)
brew install atuin

# Cargo
cargo install atuin

# Arch Linux
pacman -S atuin
```

### Shell Integration

**Zsh** (`~/.zshrc`):
```zsh
eval "$(atuin init zsh)"
```

**Bash** (`~/.bashrc`):
```bash
eval "$(atuin init bash)"
```

**Fish** (`~/.config/fish/config.fish`):
```fish
atuin init fish | source
```

**Nushell** (`config.nu`):
```nu
source ~/.local/share/atuin/init.nu
```

### First-Time Setup

```bash
# Import existing history
atuin import auto

# Optional: Register for sync
atuin register -u <USERNAME> -e <EMAIL>

# Verify setup
atuin doctor
```

## Search Modes

### Interactive Search (Ctrl+R)

| Key | Action |
|-----|--------|
| `Ctrl+R` | Open search UI |
| `Up/Down` | Navigate history |
| `Tab` | Select without executing |
| `Enter` | Execute command |
| `Alt+1-9` | Quick select item |
| `Ctrl+R` (in UI) | Cycle filter modes |

### Filter Modes

| Mode | Description |
|------|-------------|
| `global` | All history across machines |
| `host` | Current machine only |
| `session` | Current terminal session |
| `directory` | Current working directory |
| `workspace` | Git repository root |

### Search Modes

| Mode | Description |
|------|-------------|
| `prefix` | Match from start of command |
| `fulltext` | Substring match anywhere |
| `fuzzy` | Fuzzy matching (default) |
| `skim` | Skim-style fuzzy finder |

### Command Line Search

```bash
# Basic search
atuin search "git push"

# Filter by exit code (successful only)
atuin search --exit 0 "make"

# Time-based filtering
atuin search --after "yesterday 3pm" "docker"
atuin search --before "2024-01-01" "npm"

# Combine filters
atuin search --exit 0 --after "1 week ago" "kubectl"

# Directory filter
atuin search --cwd /path/to/project "test"
```

## Sync Setup

### Cloud Sync (Atuin Server)

```bash
# 1. Register account
atuin register -u <USERNAME> -e <EMAIL>

# 2. Login (creates session)
atuin login -u <USERNAME>

# 3. Import existing history
atuin import auto

# 4. Sync
atuin sync

# Check sync status
atuin status
```

### Self-Hosted Server

```bash
# Using Docker
docker run -d \
  -p 8888:8888 \
  -v $HOME/.atuin-server:/data \
  ghcr.io/atuinsh/atuin:latest \
  server start

# Configure client
atuin config set sync_address "http://localhost:8888"
```

### Sync v2 (Faster)

```toml
# ~/.config/atuin/config.toml
[sync]
records = true  # Enable sync v2
```

## Configuration

### Config File Location

```
~/.config/atuin/config.toml    # Main config
~/.local/share/atuin/history.db # History database
~/.local/share/atuin/key        # Encryption key
~/.local/share/atuin/session    # Server session
```

### Essential Settings

```toml
# ~/.config/atuin/config.toml

# Search behavior
search_mode = "fuzzy"           # prefix, fulltext, fuzzy, skim
filter_mode = "global"          # global, host, session, directory, workspace

# Shell key binding defaults
filter_mode_shell_up_key_binding = "session"  # Up arrow default

# UI settings
style = "compact"               # auto, full, compact
inline_height = 40              # Max lines (0 = full screen)
show_preview = true             # Show command preview
show_help = true                # Show keybind help
enter_accept = false            # true = execute immediately

# Sync settings
auto_sync = true                # Sync automatically
sync_frequency = "1h"           # How often to sync
sync_address = "https://api.atuin.sh"  # Server URL

# Privacy
secrets_filter = true           # Auto-filter sensitive data
store_failed = true             # Store failed commands
```

### Privacy Filters

```toml
# ~/.config/atuin/config.toml

# Regex patterns to exclude from history
history_filter = [
  "^password",
  "^secret",
  "^export.*API_KEY",
  ".*--password.*"
]

# Directories to exclude
cwd_filter = [
  "^/tmp",
  "^/private"
]

# Built-in secrets filter (AWS keys, tokens, etc.)
secrets_filter = true
```

### Key Bindings

```toml
# ~/.config/atuin/config.toml

# Vim-style navigation
keymap_mode = "vim-normal"      # emacs, vim-normal, vim-insert, auto

# Cursor style per mode
[keymap_cursor]
emacs = "blink-block"
vim_insert = "blink-bar"
vim_normal = "steady-block"
```

## Commands Reference

### Core Commands

```bash
# History operations
atuin history list              # List all history
atuin history list --cmd-only   # Commands only (no metadata)
atuin history prune             # Remove entries

# Search
atuin search [query]            # Interactive search
atuin search --interactive      # Force interactive mode

# Sync
atuin sync                      # Manual sync
atuin sync --force              # Force full sync
atuin status                    # Sync status

# Statistics
atuin stats                     # Usage statistics
atuin stats --count 20          # Top 20 commands

# Account
atuin register                  # Create account
atuin login                     # Login to sync server
atuin logout                    # Logout
atuin account delete            # Delete account

# Maintenance
atuin doctor                    # Diagnostic checks
atuin info                      # System information
atuin gen-completions           # Generate shell completions
```

### Import Commands

```bash
# Auto-detect and import
atuin import auto

# Specific shells
atuin import zsh
atuin import bash
atuin import fish
atuin import resh

# Import zsh_history file
atuin import zsh-hist-db
```

### Daemon Mode

```bash
# Start daemon (background sync)
atuin daemon

# Check daemon status
atuin daemon status
```

## Statistics

### View Stats

```bash
# Basic stats
atuin stats

# Top N commands
atuin stats --count 25

# Example output:
# Total commands: 50,234
# Unique commands: 12,456
#
# Top 10:
#  1. git status     (2,345)
#  2. cd             (1,890)
#  3. ls             (1,654)
#  4. git diff       (1,234)
#  ...
```

### Configure Stats

```toml
# ~/.config/atuin/config.toml

[stats]
# Commands where subcommands matter
common_subcommands = [
  "cargo",
  "git",
  "kubectl",
  "docker",
  "npm"
]

# Prefixes to strip from stats
common_prefix = [
  "sudo"
]
```

## Workflows

### Daily Development Workflow

```bash
# Morning: Sync history from other machines
atuin sync

# During work: Search across all history
# Press Ctrl+R, type query
# Use Ctrl+R to cycle: session → directory → global

# Find that command you ran last week
atuin search --after "1 week ago" "docker-compose"

# Check your patterns
atuin stats
```

### Multi-Machine Workflow

```bash
# On Machine A: Register and setup
atuin register -u myuser -e me@example.com
atuin import auto
atuin sync

# On Machine B: Login and sync
atuin login -u myuser
atuin sync

# History now shared between machines
# Search finds commands from both
```

### Troubleshooting Workflow

```bash
# Check installation
atuin doctor

# Verify shell integration
echo $ATUIN_SESSION  # Should be set

# Test search
atuin search "test"

# Check sync status
atuin status

# Force resync if needed
atuin sync --force
```

## Performance Tips

### Optimize Search Speed

```toml
# ~/.config/atuin/config.toml

# Use prefix mode for faster matching
search_mode = "prefix"

# Limit to session by default
filter_mode = "session"

# Reduce preview height
max_preview_height = 2
```

### Reduce Sync Traffic

```toml
# ~/.config/atuin/config.toml

# Sync less frequently
sync_frequency = "4h"

# Enable sync v2 (more efficient)
[sync]
records = true
```

### Daemon Mode (v18.3+)

```toml
# ~/.config/atuin/config.toml

[daemon]
enabled = true
sync_frequency = 300  # seconds
```

## Migration

### From fzf/history

```bash
# 1. Install atuin
curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh

# 2. Import existing history
atuin import auto

# 3. Add shell integration (replaces fzf Ctrl+R)
echo 'eval "$(atuin init zsh)"' >> ~/.zshrc

# 4. Remove fzf history binding (if any)
# Remove: bindkey '^R' fzf-history-widget
```

### From Other History Tools

```bash
# mcfly: Export first, then import
mcfly export > history.txt
# Manual import needed

# hstr: Standard history import works
atuin import auto
```

## Security

### Encryption

- All sync data is end-to-end encrypted
- Server cannot read your history
- Key stored locally (`~/.local/share/atuin/key`)

### Key Backup

```bash
# Backup your encryption key
cp ~/.local/share/atuin/key ~/atuin-key.backup

# Restore on new machine
cp ~/atuin-key.backup ~/.local/share/atuin/key
```

### Secrets Filtering

```toml
# ~/.config/atuin/config.toml

# Enable automatic secrets filtering
secrets_filter = true  # Blocks AWS keys, GitHub tokens, etc.

# Add custom patterns
history_filter = [
  ".*password=.*",
  ".*secret=.*",
  "^mysql.*-p.*"
]
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Ctrl+R not working | Check shell integration in rc file |
| Sync failing | Run `atuin doctor`, check network |
| Missing history | Run `atuin import auto` |
| Slow search | Switch to `prefix` search mode |
| Duplicate history | Check if imported multiple times |

### Diagnostic Commands

```bash
# Full diagnostics
atuin doctor

# System info
atuin info

# Check database
sqlite3 ~/.local/share/atuin/history.db "SELECT COUNT(*) FROM history"

# Debug mode
ATUIN_LOG=debug atuin sync
```

### Reset Everything

```bash
# Logout and clear local data
atuin logout
rm -rf ~/.local/share/atuin
rm -rf ~/.config/atuin

# Reinstall
curl --proto '=https' --tlsv1.2 -LsSf https://setup.atuin.sh | sh
```

## References

- [references/configuration.md](references/configuration.md) - Complete configuration reference
- [references/commands.md](references/commands.md) - Full CLI command reference
- [references/sync-setup.md](references/sync-setup.md) - Detailed sync configuration
- [references/troubleshooting.md](references/troubleshooting.md) - Common issues and fixes
- [references/workflows.md](references/workflows.md) - Advanced usage patterns

## External Links

- Official Docs: https://docs.atuin.sh
- GitHub: https://github.com/atuinsh/atuin
- Forum: https://forum.atuin.sh
- Discord: Community support
