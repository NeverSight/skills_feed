---
name: pyprland
description: |
  Pyprland - Desktop environment extensions for Hyprland and Niri.
  Use when configuring scratchpads, expose effect, wallpapers, monitors, magnify, menubar, or any Pyprland plugin.
  Keywords: pyprland, hyprland, scratchpads, expose, wallpapers, monitors, magnify, menubar, toggle-dpms, toggle-special, layout-center, lost-windows, shift-monitors, workspaces-follow-focus, toml-config.
compatibility: Python 3.10+, Hyprland or Niri compositor, pipx/pip installation
metadata:
  source: https://hyprland-community.github.io/pyprland/
  total_docs: 158
  generated: 2026-01-31T16:31:12.757799
---

# Pyprland

> Desktop environment extensions that enhance Hyprland/Niri with scratchpads, expose effect, wallpaper management, and more. Simple TOML configuration, high customization, fast and easy.

## Quick Start

```toml
# ~/.config/hypr/pyprland.toml

[pyprland]
plugins = ["scratchpads", "expose", "wallpapers"]

# Define a dropdown terminal scratchpad
[scratchpads.term]
animation = "fromTop"
command = "kitty --class kitty-dropterm"
class = "kitty-dropterm"
size = "75% 60%"
margin = 50

# Volume control scratchpad
[scratchpads.volume]
animation = "fromRight"
command = "pavucontrol"
class = "org.pulseaudio.pavucontrol"
size = "40% 90%"
unfocus = "hide"
lazy = true
```

```bash
# hyprland.conf keybindings
bind = $mainMod, A, exec, pypr toggle term
bind = $mainMod, V, exec, pypr toggle volume
bind = $mainMod, B, exec, pypr expose

# Style the exposed workspace
workspace = special:exposed,gapsout:60,gapsin:30,bordersize:5,border:true,shadow:false
```

## Installation

```bash
# Using pipx (recommended)
pipx install pyprland

# Or using pip
pip install pyprland

# Start pyprland (add to hyprland.conf exec-once)
exec-once = pypr
```

## Documentation

Full documentation in `docs/`. See `docs/000-index.md` for detailed navigation.

### By Topic

| Topic | Files | Description |
|-------|-------|-------------|
| Overview/Intro | 001 | What is Pyprland, features overview |
| Expose Effect | 002 | Show all windows on focused screen |
| Lost Windows | 003 | Bring unreachable windows to current workspace |
| Monitors | 004 | Relative monitor placement configuration |
| Scratchpads | 005, 010, 016 | Toggle-able dropdown windows |
| Wallpapers | 006, 021, 022 | Automated wallpaper cycling with templates |
| Fcitx5 Switcher | 007 | Input method switching per window |
| Layout Center | 008 | Centered window management |
| Menubar | 009 | Auto-managed menu bar |
| System Notifier | 011 | System notification daemon |
| Workspaces Follow | 012 | Workspace focus management |
| Fetch Client Menu | 013 | Menu-based window fetching |
| Text Filters | 014 | Sed-style text filtering |
| Magnify | 015 | Display zoom controls |
| Shift Monitors | 017 | Swap workspaces between screens |
| Shortcuts Menu | 018 | Customizable shortcut menus |
| Toggle DPMS | 019 | Display power management |
| Toggle Special | 020 | Special workspace toggling |

### By Keyword

| Keyword | File |
|---------|------|
| scratchpad | 005, 010, 016 |
| expose | 002 |
| wallpaper | 006, 021, 022 |
| monitors | 004 |
| magnify | 015 |
| zoom | 015 |
| dpms | 019 |
| toggle | 019, 020 |
| layout | 008 |
| menubar | 009 |
| lost-windows | 003 |
| workspaces | 012 |
| shift-monitors | 017 |
| fetch-client | 013 |
| shortcuts | 018 |
| filters | 014 |
| fcitx5 | 007 |
| system-notifier | 011 |
| animation | 005 |
| toml | 005, 006 |
| hyprland | 001-022 |
| niri | 009 |

### Version-Specific Docs

| Version | Files | Notes |
|---------|-------|-------|
| Current/Latest | 001-022 | Most up-to-date, recommended |
| v2.6.2 | 023-038 | Previous stable |
| v2.5.x | 039-054 | Legacy |
| v2.4.7 | 055-070 | Legacy |
| v2.4.6 | 071-086 | Legacy |
| v2.4.1 | 087-101 | Legacy |
| v2.4.0 | 102-117 | Legacy |
| v2.3.8 | 118-133 | Legacy |
| v2.3.6/7 | 134-148 | Legacy |
| v2.3.5 | 149-158 | Oldest |

### Learning Path

1. **Start**: `docs/001-pyprland-index.md` - Overview and features
2. **Core plugins**: `docs/002-006` - expose, lost-windows, monitors, scratchpads, wallpapers
3. **Configuration**: `docs/007-012` - Advanced setup and options
4. **Reference**: `docs/013-022` - All other plugins and features

## Common Tasks

### Configure a Dropdown Terminal
`docs/005-pyprland-scratchpads.md` (basic setup with animations)

### Show All Windows (Expose)
`docs/002-pyprland-expose.md` (macOS-like expose effect)

### Auto-Cycle Wallpapers
`docs/006-pyprland-wallpapers.md` (random wallpaper rotation)

### Generate Color Schemes from Wallpaper
`docs/022-pyprland-wallpapers-templates.md` (Pywal/Matugen-style theming)

### Setup Multi-Monitor Layout
`docs/004-pyprland-monitors.md` (relative monitor positioning)

### Zoom/Magnify Display
`docs/015-pyprland-magnify.md` (accessibility zoom feature)

### Toggle Display Power
`docs/019-pyprland-toggle-dpms.md` (turn monitors on/off)

### Fetch Window via Menu
`docs/013-pyprland-fetch-client-menu.md` (rofi/dmenu window picker)

### Advanced Scratchpad Config
`docs/016-pyprland-scratchpads-advanced.md` (fine-tuning, i3 compat)

### Troubleshoot Scratchpads
`docs/010-pyprland-scratchpads-nonstandard.md` (PWA, emacsclient issues)
