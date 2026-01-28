---
name: wezterm
description: Configure and customize WezTerm terminal emulator. Use for setting up WezTerm config, themes, keybindings, and advanced features.
---

# WezTerm Configuration

Configure the WezTerm terminal emulator.

## Prerequisites

```bash
# Install WezTerm
brew install --cask wezterm
```

Config location: `~/.wezterm.lua` or `~/.config/wezterm/wezterm.lua`

## Basic Configuration

### Minimal Config

```lua
-- ~/.wezterm.lua
local wezterm = require 'wezterm'
local config = wezterm.config_builder()

-- Font
config.font = wezterm.font('JetBrains Mono')
config.font_size = 14.0

-- Colors
config.color_scheme = 'Catppuccin Mocha'

-- Window
config.window_padding = {
  left = 10,
  right = 10,
  top = 10,
  bottom = 10,
}

return config
```

### Font Configuration

```lua
-- Single font
config.font = wezterm.font('JetBrains Mono')

-- Font with fallbacks
config.font = wezterm.font_with_fallback({
  'JetBrains Mono',
  'Fira Code',
  'Nerd Font Symbols',
})

-- Font with weight
config.font = wezterm.font('JetBrains Mono', { weight = 'Medium' })

-- Different font for bold
config.font_rules = {
  {
    intensity = 'Bold',
    font = wezterm.font('JetBrains Mono', { weight = 'Bold' }),
  },
}
```

### Color Schemes

```lua
-- Use built-in scheme
config.color_scheme = 'Catppuccin Mocha'

-- List available schemes
-- wezterm show-keys --lua

-- Custom colors
config.colors = {
  foreground = '#c0caf5',
  background = '#1a1b26',
  cursor_bg = '#c0caf5',
  selection_bg = '#33467c',
  ansi = {'#15161e', '#f7768e', '#9ece6a', '#e0af68', '#7aa2f7', '#bb9af7', '#7dcfff', '#a9b1d6'},
  brights = {'#414868', '#f7768e', '#9ece6a', '#e0af68', '#7aa2f7', '#bb9af7', '#7dcfff', '#c0caf5'},
}
```

## Key Bindings

### Custom Keybindings

```lua
config.keys = {
  -- Split panes
  { key = 'd', mods = 'CMD', action = wezterm.action.SplitHorizontal { domain = 'CurrentPaneDomain' } },
  { key = 'd', mods = 'CMD|SHIFT', action = wezterm.action.SplitVertical { domain = 'CurrentPaneDomain' } },

  -- Navigate panes
  { key = 'LeftArrow', mods = 'CMD', action = wezterm.action.ActivatePaneDirection 'Left' },
  { key = 'RightArrow', mods = 'CMD', action = wezterm.action.ActivatePaneDirection 'Right' },
  { key = 'UpArrow', mods = 'CMD', action = wezterm.action.ActivatePaneDirection 'Up' },
  { key = 'DownArrow', mods = 'CMD', action = wezterm.action.ActivatePaneDirection 'Down' },

  -- Tabs
  { key = 't', mods = 'CMD', action = wezterm.action.SpawnTab 'CurrentPaneDomain' },
  { key = 'w', mods = 'CMD', action = wezterm.action.CloseCurrentPane { confirm = true } },

  -- Font size
  { key = '=', mods = 'CMD', action = wezterm.action.IncreaseFontSize },
  { key = '-', mods = 'CMD', action = wezterm.action.DecreaseFontSize },
  { key = '0', mods = 'CMD', action = wezterm.action.ResetFontSize },
}
```

### Leader Key

```lua
-- Define leader key (like tmux prefix)
config.leader = { key = 'a', mods = 'CMD', timeout_milliseconds = 1000 }

config.keys = {
  -- Leader + c = new tab
  { key = 'c', mods = 'LEADER', action = wezterm.action.SpawnTab 'CurrentPaneDomain' },
  -- Leader + | = vertical split
  { key = '|', mods = 'LEADER', action = wezterm.action.SplitHorizontal { domain = 'CurrentPaneDomain' } },
  -- Leader + - = horizontal split
  { key = '-', mods = 'LEADER', action = wezterm.action.SplitVertical { domain = 'CurrentPaneDomain' } },
}
```

## Advanced Features

### Tab Bar Customization

```lua
config.use_fancy_tab_bar = false
config.tab_bar_at_bottom = true
config.hide_tab_bar_if_only_one_tab = true

-- Custom tab title
wezterm.on('format-tab-title', function(tab)
  local title = tab.tab_title
  if title and #title > 0 then
    return title
  end
  return tab.active_pane.title
end)
```

### Startup Actions

```lua
-- Start with specific layout
wezterm.on('gui-startup', function(cmd)
  local tab, pane, window = mux.spawn_window(cmd or {})
  -- Split right
  pane:split { direction = 'Right' }
end)
```

### SSH Domains

```lua
config.ssh_domains = {
  {
    name = 'my-server',
    remote_address = 'server.example.com',
    username = 'user',
  },
}

-- Connect with: wezterm connect my-server
```

### Multiplexer

```lua
-- Unix domain for persistent sessions
config.unix_domains = {
  { name = 'unix' },
}

-- Default to multiplexer
config.default_gui_startup_args = { 'connect', 'unix' }
```

## Useful Snippets

### Quick Theme Toggle

```lua
local function toggle_theme()
  local overrides = window:get_config_overrides() or {}
  if overrides.color_scheme == 'Catppuccin Latte' then
    overrides.color_scheme = 'Catppuccin Mocha'
  else
    overrides.color_scheme = 'Catppuccin Latte'
  end
  window:set_config_overrides(overrides)
end

config.keys = {
  { key = 't', mods = 'CMD|SHIFT', action = wezterm.action_callback(toggle_theme) },
}
```

### Background Image

```lua
config.window_background_image = '/path/to/image.png'
config.window_background_image_hsb = {
  brightness = 0.02,
  saturation = 0.5,
}
```

### Status Bar

```lua
wezterm.on('update-right-status', function(window, pane)
  window:set_right_status(wezterm.format({
    { Text = wezterm.strftime('%H:%M') },
  }))
end)
```

## Command Line

```bash
# Open with specific config
wezterm --config-file path/to/config.lua

# Connect to multiplexer
wezterm connect unix

# List color schemes
wezterm ls-colors

# Show key bindings
wezterm show-keys
wezterm show-keys --lua

# CLI utilities
wezterm cli list           # List panes
wezterm cli spawn          # Spawn new pane
wezterm cli split-pane     # Split current pane
```

## Best Practices

1. **Start simple** - Add features as needed
2. **Use config_builder** - Better error messages
3. **Test incrementally** - WezTerm reloads on save
4. **Backup your config** - Keep in dotfiles repo
5. **Use leader keys** - Avoid conflicts with apps
6. **Check logs** - `wezterm --config-file ~/.wezterm.lua` shows errors
