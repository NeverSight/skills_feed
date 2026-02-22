---
name: hammerspoon
description: Configure and manage Hammerspoon automation, app launching, and window switching. Use when working with ~/.config/hammerspoon config files, adding keybindings, modifying the leader modal, or troubleshooting Hammerspoon functionality. Window management is handled by AeroSpace.
---

# Hammerspoon configuration skill

## Overview

Manage Hammerspoon configuration for macOS automation including app launching, window switching, emoji/symbol pickers, and leader modal. Window management is handled by AeroSpace.

## Configuration locations

- Config directory: `~/.config/hammerspoon/`
- Symlink: `~/.hammerspoon` → `~/.config/hammerspoon/`
- CLI tool: `hs` (installed via `hs.ipc.cliInstall()` in init.lua)

## Current modules

### Core infrastructure

**hyper-key.lua** - Inline hyper key implementation
- No spoon dependencies
- Provides `HyperKey.new(mods)` constructor
- Binding methods: `bind(key):toFunction(name, fn)` and `bind(key):toApplication(app)`
- Tracks bindings in `self.bindings` table

**init.lua** - Main entry point
- Calls `hs.ipc.cliInstall()` to enable CLI access
- Defines `hyper` modifier: `{cmd, ctrl, alt, shift}`
- Loads window-switcher and sets up cmd+space and cmd+tab bindings
- Loads notch-clock with 4-minute offset
- Loads leader modal with emoji and symbol pickers

### Leader modal system

**leader-modal.lua** - Modal keybinding system
- Timeout-based modal (default 3000ms)
- Shows on-screen hints for available bindings
- Supports nested leader keys
- Sticky mode for repeated actions

**leader-dsl.lua** - DSL for defining leader bindings
- `Leader(key, description, bindings)` - Define leader menu
- `Bind(key, description, action, options)` - Define action
- Actions can be functions, shell commands, or mode transitions
- Automatically registers clues from `~/.config/hammerspoon/clues/` directory

**clues/*.lua** - Leader binding definitions
- `windows.lua` - Window management (moved to AeroSpace)
- `hammerspoon.lua` - Reload config, console, update apps, switcher
- `apps.lua` - App launching
- `system.lua` - System operations
- `cleanshot.lua` - CleanShot integration
- `emoji.lua` - Emoji picker
- `superwhisper.lua` - SuperWhisper integration

### Pickers

**emoji-picker.lua** - Emoji chooser
- Fuzzy-searchable emoji picker
- Categories and descriptions
- Inserts selected emoji via keystroke

**symbol-picker.lua** - Symbol chooser
- Special characters and symbols
- Categories: arrows, math, punctuation, currency, etc.
- Inserts selected symbol via keystroke

**chooser-style.lua** - Shared chooser styling
- Dark theme
- Consistent width and row count
- Applied to all choosers

### Window switcher

**window-switcher.lua** - Unified launcher/dispatcher modal
- Uses `hs.chooser` API with fuzzy matching
- Shows windows, apps, and commands
- Keybindings: `cmd+space` and `cmd+tab`
- Dark theme with 15 visible rows

**fuzzy.lua** - Dynamic programming fuzzy matching
- Subsequence matching with scoring bonuses
- Type priority: window (3), app (2), command (1)

**notch-clock.lua** - Clock in notch area
- Shows time in MacBook notch
- 4-minute offset configuration

## Common operations

### Using the hs CLI

The `hs` command-line tool provides direct interaction with Hammerspoon. It requires `hs.ipc.cliInstall()` to be called in init.lua (already configured).

**Check for errors and module status:**
```bash
echo "
local status = {modules_loaded = {}, errors = {}}
local modules = {'hyper-key', 'config-watch', 'window-hotkeys', 'quick-switch', 'window-switcher'}
for _, mod in ipairs(modules) do
  local ok, result = pcall(require, mod)
  if ok then
    table.insert(status.modules_loaded, mod)
  else
    table.insert(status.errors, mod .. ': ' .. tostring(result))
  end
end
return hs.json.encode(status, true)
" | hs -c ''
```

**View live console output:**
```bash
hs -C
```

**Execute Hammerspoon commands:**
```bash
echo "hs.alert.show('test')" | hs -c ''
echo 'hs.reload()' | hs -c ''
```

**Interactive Lua REPL:**
```bash
hs
```

**Mirror prints to console:**
```bash
hs -P
```

**Run a script:**
```bash
hs /path/to/script.lua
```

**Common flags:**
- `-A` - Auto-launch Hammerspoon if not running
- `-C` - Clone console prints to this terminal (best for checking errors)
- `-P` - Mirror prints to Hammerspoon console
- `-c` - Execute command and return result
- `-i` - Force interactive mode
- `-n` - Disable colorized output
- `-N` - Force colorized output
- `-q` - Quiet mode (errors and results only)

### Other operations

**Reload Hammerspoon:**
```bash
echo 'hs.reload()' | hs -c ''
# or via URL:
open -g hammerspoon://reload
```

**Check if running:**
```bash
ps aux | rg -i hammerspoon
```

**Open console window:**
```bash
open "hammerspoon://consoleWindow"
```

**Test configuration:**
Edit any `.lua` file in `~/.config/hammerspoon/` to trigger auto-reload


## Development patterns

### Adding new leader bindings

Create a file in `~/.config/hammerspoon/clues/`:

```lua
return Leader("key", "Description", {
  Bind("a", "Action 1", { fn = function() ... end }),
  Bind("b", "Action 2", { shell = "/path/to/script" }),
  Bind("c", "Action 3", { mode = "mode_name" }),
})
```

### Creating new modules

1. Create `~/.config/hammerspoon/module-name.lua`
2. Return module table or functionality
3. Require in `init.lua`: `local module = require("module-name")`

## App replacement status

Current Hammerspoon setup replaces:
- **AltTab**: Window switching via window-switcher.lua (cmd+space, cmd+tab)

Other macOS automation tools:
- **Karabiner-Elements**: Key remapping (caps lock to ctrl, etc.)
- **AeroSpace**: Window management (tiling, workspaces, monitor assignment)
- **CleanShot**: Screenshots (integrated via leader modal)

## Troubleshooting

### Check for errors
Use the `hs` CLI to check for module loading errors:
```bash
echo "
local status = {modules_loaded = {}, errors = {}}
local modules = {'hyper-key', 'config-watch', 'window-hotkeys', 'quick-switch', 'window-switcher'}
for _, mod in ipairs(modules) do
  local ok, result = pcall(require, mod)
  if ok then
    table.insert(status.modules_loaded, mod)
  else
    table.insert(status.errors, mod .. ': ' .. tostring(result))
  end
end
return hs.json.encode(status, true)
" | hs -c ''
```

Or view live console output: `hs -C`

### Config not loading
- Check symlink: `ls -la ~/.hammerspoon`
- Verify Hammerspoon is running: `ps aux | rg Hammerspoon`
- Reload manually: `echo 'hs.reload()' | hs -c ''`
- Check for errors: `hs -C` or `open "hammerspoon://consoleWindow"`

### Keybindings not working
- Check for conflicts with app shortcuts
- Verify modifier keys are correct
- Test with: `echo "hs.alert.show('test')" | hs -c ''`

### Auto-reload not triggering
- Verify `config-watch.lua` is loaded in `init.lua`
- Check file extension is `.lua`
- Restart Hammerspoon app

### CLI not working
If `hs` command not found, ensure `hs.ipc.cliInstall()` is called in init.lua

## Philosophy

### Zero spoons approach
- Inline functionality instead of external dependencies
- Only use spoons if absolutely necessary
- Keep implementation simple and maintainable

**Decision criteria for using spoons:**
- Must provide significant value that's hard to inline
- Must be actively maintained
- Must be worth the workflow complexity

**Future spoon management (not yet implemented):**
If spoons are needed, they will be managed via GitHub workflow:
1. Add spoon commit hash to `.github/workflows/versions.lua`
2. Create `.github/workflows/hammerspoon.yml` build workflow
3. Workflow clones spoons at specified revisions, bundles into tarball
4. Release as `hammerspoon-YYYY.MM.DD-darwin-arm64.tar.gz`
5. Only add spoons to config after workflow builds successfully

This ensures pinned, reproducible spoon dependencies similar to other tools in the repo.

### File organization
- One module per file
- Clear, descriptive names
- Require modules in `init.lua`
- Use XDG-style config directory

## Resources

- Hammerspoon API: https://www.hammerspoon.org/docs/
- Plan document: `~/.claude/plans/hammerspoon-consolidation.md`
- dbalatero dotfiles: https://github.com/dbalatero/dotfiles/tree/main/hammerspoon (reference only)
