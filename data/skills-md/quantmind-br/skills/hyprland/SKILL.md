---
name: hyprland
description: |
  Hyprland - Dynamic tiling Wayland compositor with stunning animations and GPU-accelerated effects.
  Use when configuring Hyprland window manager, keybinds, monitors, workspaces, animations, window rules, or working with the Hypr ecosystem tools.
  Keywords: hyprland, wayland, compositor, tiling, window-manager, keybinds, dispatchers, monitors, workspaces, animations, window-rules, hyprctl, hyprlang, nvidia, xwayland, plugins, gestures, decorations.
compatibility: Linux with Wayland support. Officially supports Arch and NixOS. Requires wlroots-based compositor dependencies.
metadata:
  source: https://wiki.hypr.land/
  total_docs: 92
  generated: 2026-02-01T12:29:02.316Z
---

# Hyprland

> Hyprland is a dynamic tiling Wayland compositor that doesn't sacrifice on its looks. It provides the latest Wayland features, is highly customizable, has all the eyecandy, and comes with powerful plugins.

## Quick Start

```bash
# Config location
~/.config/hypr/hyprland.conf

# Launch Hyprland from TTY
start-hyprland

# Basic keybinds (default config)
SUPER + Q          # Launch terminal (kitty)
SUPER + C          # Close window
SUPER + M          # Exit Hyprland
SUPER + E          # File manager
SUPER + V          # Toggle floating
SUPER + R          # App launcher
SUPER + 1-9        # Switch workspace
SUPER + SHIFT + 1-9 # Move window to workspace

# Control Hyprland via CLI
hyprctl dispatch exec kitty
hyprctl keyword general:border_size 3
hyprctl reload
```

## Installation

```bash
# Arch Linux (recommended)
sudo pacman -S hyprland

# NixOS - add to configuration.nix
programs.hyprland.enable = true;

# Install default terminal
sudo pacman -S kitty
```

## Documentation

Complete documentation in `docs/`. Consult `docs/000-index.md` for navigation.

### By Topic

| Topic | Files | Description |
|-------|-------|-------------|
| Getting Started | 001, 034-036 | Installation, tutorials, preconfigured setups |
| Configuration | 003-025 | Animations, binds, layouts, monitors, variables |
| Window Management | 005-006, 012, 022-023 | Dispatchers, dwindle/master layouts, rules |
| Input & Gestures | 010, 021 (input section) | Touchpad, keyboard, gestures |
| Hypr Ecosystem | 037-058 | hypridle, hyprlock, hyprpaper, hyprcursor, etc. |
| Nix Integration | 062-069 | NixOS, Home Manager, Cachix, plugins |
| Plugins | 071-077 | Development, using plugins, event hooks |
| Utilities | 079-091 | Status bars, launchers, clipboard, wallpapers |
| Troubleshooting | 032-033, 070 | Crashes, bugs, FAQ, Nvidia |

### By Keyword

| Keyword | File |
|---------|------|
| animation | 003, 021 |
| keybinds / binds | 004 |
| dispatchers | 005 |
| dwindle-layout | 006 |
| master-layout | 012 |
| environment-variables | 007 |
| monitors | 013 |
| multi-gpu | 014 |
| performance | 015 |
| window-rules | 022 |
| workspace-rules | 023 |
| xwayland | 024 |
| hyprctl | 020 |
| hyprlang | 043 |
| hypridle | 040 |
| hyprlock | 045 |
| hyprpaper | 046 |
| hyprcursor | 038 |
| nvidia | 070 |
| plugins | 071-077 |
| ipc / sockets | 009, 061 |
| gestures | 010 |
| tearing | 018 |
| screensharing | 087 |
| status-bars / waybar | 088 |
| app-launchers | 080 |
| clipboard | 081 |
| uwsm / systemd | 089 |

### Learning Path

1. **Foundation**: Read 034 (Installation), 035 (Master Tutorial), 036 (Getting Started)
2. **Configuration Basics**: 017 (Config Start), 021 (Variables), 004 (Binds)
3. **Window Management**: 005 (Dispatchers), 006/012 (Layouts), 022 (Window Rules)
4. **Visual Customization**: 003 (Animations), 013 (Monitors), 021 (Decorations section)
5. **Ecosystem Tools**: 040 (hypridle), 045 (hyprlock), 046 (hyprpaper)
6. **Advanced**: 071-077 (Plugins), 061 (IPC), 009 (Automation)

## Common Tasks

### Configure monitors
-> `docs/013-Configuring-Monitors.md` (resolution, position, scaling, rotation, VRR, HDR)

### Set up keybinds
-> `docs/004-Configuring-Binds.md` (basic binds, mouse binds, submaps, global shortcuts)

### Create window rules
-> `docs/022-Configuring-Window-Rules.md` (match by class/title, float, opacity, workspace)

### Configure animations
-> `docs/003-Configuring-Animations.md` (animation tree, bezier curves, speed, style)

### Set up idle/lock screen
-> `docs/040-Hypr-Ecosystem-hypridle.md` + `docs/045-Hypr-Ecosystem-hyprlock.md`

### Configure Nvidia GPU
-> `docs/070-Nvidia.md` (drivers, environment variables, troubleshooting)

### Use hyprctl commands
-> `docs/020-Configuring-Using-hyprctl.md` (dispatch, keyword, reload, clients)

### Debug crashes
-> `docs/032-Crashes-and-Bugs.md` (logs, crash reports, coredumps, bisect)

### Screen sharing setup
-> `docs/087-Useful-Utilities-Screen-Sharing.md` (PipeWire, xdg-desktop-portal)

### Set up status bar
-> `docs/088-Useful-Utilities-Status-Bars.md` (Waybar, AGS, Eww configurations)
