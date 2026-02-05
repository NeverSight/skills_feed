---
name: walker
description: |
  Walker - Multi-purpose launcher frontend for Elephant with GTK4 UI.
  Use when configuring Walker launcher, Elephant providers, custom menus, themes, keybinds, or dmenu replacement.
  Keywords: walker, elephant, launcher, gtk4, providers, themes, customization, keybinds, dmenu, menus, archlinux, systemd, configuration.
compatibility: Linux with GTK4, Elephant backend service required. Arch Linux (yay), Fedora (dnf copr), or manual compilation.
metadata:
  source: https://benz.gitbook.io/walker/sitemap-pages.xml
  total_docs: 10
  generated: 2026-02-01T13:52:00.000000000-03:00
---

# Walker

> Walker is a multi-purpose launcher frontend for Elephant. It provides a GTK4-based UI for interacting with various data providers like desktop applications, files, clipboard, websearch, and custom menus.

## Quick Start

```bash
# Install Walker and Elephant (Arch Linux)
yay -S walker elephant elephant-desktopapplications

# Enable and start Elephant service
elephant service enable
systemctl --user start elephant.service

# Launch Walker
walker
```

## Installation

### Arch Linux
```bash
yay -S walker
yay -S elephant elephant-desktopapplications
```

### Fedora
```bash
sudo dnf copr enable errornointernet/walker
sudo dnf install walker elephant
```

### Manual Compilation
```bash
# Dependencies
sudo zypper install git cargo gtk4-devel gtk4-layer-shell-devel libpoppler-glib-devel protobuf-devel cairo-devel go make

# Walker
git clone https://github.com/abenz1267/walker.git ~/Downloads/walker
cd ~/Downloads/walker && sudo make install

# Elephant
git clone https://github.com/abenz1267/elephant ~/Downloads/elephant
cd ~/Downloads/elephant && sudo make install
```

## Documentation

Complete documentation in `docs/`. See `docs/000-index.md` for detailed navigation.

### By Topic

| Topic | Files | Description |
|-------|-------|-------------|
| Installation & Setup | 002 | Package manager install, manual compilation, service setup |
| Architecture & Concepts | 003-004 | Walker/Elephant relationship, providers architecture |
| Configuration | 005, 008 | General config, provider actions, keybinds |
| Customization | 006-007 | Themes (GTK4 CSS/XML), custom menus (Lua scripts) |
| Usage | 009 | Dmenu replacement, CLI flags |
| Troubleshooting | 010 | Performance issues, NVIDIA GPU, systemd service |

### By Keyword

| Keyword | File |
|---------|------|
| launcher | 001-walker.md |
| frontend | 001-walker.md |
| elephant | 001-walker.md, 003-walker-walker-and-elephant.md |
| installation | 002-walker-installation-and-launching.md |
| gtk4 | 002-walker-installation-and-launching.md, 006-walker-customization-theme.md |
| systemd | 002-walker-installation-and-launching.md |
| optimization | 002-walker-installation-and-launching.md |
| providers | 003-walker-walker-and-elephant.md, 004-walker-providers.md |
| modular-design | 004-walker-providers.md |
| configuration | 005-walker-customization-general-config.md |
| keybinds | 005-walker-customization-general-config.md, 008-walker-customization-provider-actions.md |
| settings | 005-walker-customization-general-config.md |
| emergency-entries | 005-walker-customization-general-config.md |
| theme | 006-walker-customization-theme.md |
| customization | 006-walker-customization-theme.md |
| custom-menus | 007-walker-customization-custom-menus.md |
| lua-scripts | 007-walker-customization-custom-menus.md |
| menu-provider | 007-walker-customization-custom-menus.md |
| actions | 008-walker-customization-provider-actions.md |
| fallbacks | 008-walker-customization-provider-actions.md |
| dmenu | 009-walker-dmenu.md |
| command-line | 009-walker-dmenu.md |
| cli-tool | 009-walker-dmenu.md |
| performance | 010-walker-faq.md |
| troubleshooting | 010-walker-faq.md |
| nvidia | 010-walker-faq.md |
| gpu | 010-walker-faq.md |

### Learning Path

1. **Foundation**: Read 001 (introduction), complete 002 (installation)
2. **Core Understanding**: Learn architecture from 003-004, configure with 005
3. **Practical Application**: Customize themes (006), create menus (007)
4. **Advanced Usage**: Configure provider actions (008), use as dmenu (009)
5. **Reference**: Troubleshooting (010)

## Common Tasks

### Start Walker Service for Fast Startup
-> `docs/002-walker-installation-and-launching.md` (Keep Walker instance running with --gapplication-service for faster subsequent launches)

### Configure Default Providers
-> `docs/005-walker-customization-general-config.md` (Set which providers are queried by default in config.toml)

### Create Custom Theme
-> `docs/006-walker-customization-theme.md` (Create style.css, layout.xml in ~/.config/walker/themes/)

### Add Custom Menu
-> `docs/007-walker-customization-custom-menus.md` (Configure Elephant menu provider with Lua scripts)

### Configure Keybinds
-> `docs/005-walker-customization-general-config.md` (Global keybinds like next, prev, activate)

### Use Provider-Specific Actions
-> `docs/008-walker-customization-provider-actions.md` (Configure multiple actions per list item)

### Use as Dmenu Replacement
-> `docs/009-walker-dmenu.md` (CLI flags for dmenu-style usage)

### Fix NVIDIA Performance Issues
-> `docs/010-walker-faq.md` (Environment variable adjustments for GPU issues)

### Generate Provider Documentation
-> `docs/004-walker-providers.md` (Run `elephant generatedoc` to get config docs for installed providers)

## Default Providers

Walker implements these Elephant providers by default:
- bluetooth
- archlinux packages
- calc
- providerlist
- websearch
- desktopapplications
- files
- todo
- runner
- symbols
- unicode
- clipboard
- menus

## Configuration

Default config path: `~/.config/walker/config.toml`

Reference config: https://github.com/abenz1267/walker/blob/master/resources/config.toml
