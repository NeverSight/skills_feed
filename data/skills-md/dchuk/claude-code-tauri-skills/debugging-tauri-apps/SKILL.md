---
name: debugging-tauri-apps
description: Helps users debug Tauri v2 applications across VS Code, RustRover, IntelliJ, and Neovim. Covers console debugging, WebView DevTools, Rust backtrace, CrabNebula DevTools integration, and IDE-specific launch configurations.
---

# Debugging Tauri Applications

This skill covers debugging Tauri v2 applications including console debugging, WebView inspection, IDE configurations, and CrabNebula DevTools.

## Development-Only Code

Use conditional compilation to exclude debug code from production builds:

```rust
// Only runs during `tauri dev`
#[cfg(dev)]
{
    // Development-only code
}

// Runtime check
if cfg!(dev) {
    // tauri dev code
} else {
    // tauri build code
}

// Programmatic check
let is_dev: bool = tauri::is_dev();

// Debug builds and `tauri build --debug`
#[cfg(debug_assertions)]
{
    // Debug-only code
}
```

## Console Debugging

### Rust Print Macros

Print messages to the terminal where `tauri dev` runs:

```rust
println!("Message from Rust: {}", msg);
dbg!(&variable);  // Prints variable with file:line info
```

### Enable Backtraces

For detailed error information:

```bash
# Linux/macOS
RUST_BACKTRACE=1 tauri dev

# Windows PowerShell
$env:RUST_BACKTRACE=1
tauri dev
```

## WebView DevTools

### Opening DevTools

- Right-click and select "Inspect Element"
- `Ctrl + Shift + i` (Linux/Windows)
- `Cmd + Option + i` (macOS)

Platform-specific inspectors: WebKit (Linux), Safari (macOS), Edge DevTools (Windows).

### Programmatic Control

```rust
tauri::Builder::default()
    .setup(|app| {
        #[cfg(debug_assertions)]
        {
            let window = app.get_webview_window("main").unwrap();
            window.open_devtools();
            // window.close_devtools();
        }
        Ok(())
    })
```

### Production DevTools

Create a debug build for testing:

```bash
tauri build --debug
```

To permanently enable devtools in production, add to `src-tauri/Cargo.toml`:

```toml
[dependencies]
tauri = { version = "...", features = ["...", "devtools"] }
```

> WARNING: Using the devtools feature enables private macOS APIs that prevent App Store acceptance.

---

## VS Code Setup

### Required Extensions

| Extension | Platform | Purpose |
|-----------|----------|---------|
| [vscode-lldb](https://marketplace.visualstudio.com/items?itemName=vadimcn.vscode-lldb) | All | LLDB debugger |
| [C/C++](https://marketplace.visualstudio.com/items?itemName=ms-vscode.cpptools) | Windows | Visual Studio debugger |

### launch.json Configuration

Create `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "lldb",
      "request": "launch",
      "name": "Tauri Development Debug",
      "cargo": {
        "args": [
          "build",
          "--manifest-path=./src-tauri/Cargo.toml",
          "--no-default-features"
        ]
      },
      "preLaunchTask": "ui:dev"
    },
    {
      "type": "lldb",
      "request": "launch",
      "name": "Tauri Production Debug",
      "cargo": {
        "args": [
          "build",
          "--release",
          "--manifest-path=./src-tauri/Cargo.toml"
        ]
      },
      "preLaunchTask": "ui:build"
    }
  ]
}
```

### Windows Visual Studio Debugger

For faster Windows debugging with better enum support:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Launch App Debug",
      "type": "cppvsdbg",
      "request": "launch",
      "program": "${workspaceRoot}/src-tauri/target/debug/your-app-name.exe",
      "cwd": "${workspaceRoot}",
      "preLaunchTask": "dev"
    }
  ]
}
```

### tasks.json Configuration

Create `.vscode/tasks.json`:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "ui:dev",
      "type": "shell",
      "isBackground": true,
      "command": "npm",
      "args": ["run", "dev"]
    },
    {
      "label": "ui:build",
      "type": "shell",
      "command": "npm",
      "args": ["run", "build"]
    },
    {
      "label": "build:debug",
      "type": "cargo",
      "command": "build",
      "options": {
        "cwd": "${workspaceRoot}/src-tauri"
      }
    },
    {
      "label": "dev",
      "dependsOn": ["build:debug", "ui:dev"],
      "group": {
        "kind": "build"
      }
    }
  ]
}
```

### Debugging Workflow

1. Set breakpoints by clicking the line number margin in Rust files
2. Press `F5` or select debug configuration from Run menu
3. The `preLaunchTask` runs the dev server automatically
4. Debugger attaches and stops at breakpoints

> NOTE: LLDB bypasses the Tauri CLI, so `beforeDevCommand` and `beforeBuildCommand` must be configured as tasks.

---

## RustRover / IntelliJ Setup

### Project Configuration

If your project lacks a top-level `Cargo.toml`, create a workspace file:

```toml
[workspace]
members = ["src-tauri"]
```

Or attach `src-tauri/Cargo.toml` via the Cargo tool window.

### Run Configurations

Create two configurations in **Run | Edit Configurations**:

#### 1. Tauri App Configuration (Cargo)

- **Command**: `run`
- **Additional arguments**: `--no-default-features`

The `--no-default-features` flag is critical - it tells Tauri to load assets from the dev server instead of bundling them.

#### 2. Development Server Configuration

For Node-based projects:
- Create an npm Run Configuration
- Set package manager (npm/pnpm/yarn)
- Set script to `dev`

For Rust WASM (Trunk):
- Create a Shell Script configuration
- Command: `trunk serve`

### Debugging Workflow

1. Start the development server configuration first
2. Click Debug on the Tauri App configuration
3. RustRover halts at Rust breakpoints automatically
4. Inspect variables and step through code

---

## Neovim Setup

### Required Plugins

- **nvim-dap** - Debug Adapter Protocol client
- **nvim-dap-ui** - Debugger UI
- **nvim-nio** - Async dependency for nvim-dap-ui
- **overseer.nvim** (recommended) - Task management

### Prerequisites

Download `codelldb` from [GitHub releases](https://github.com/vadimcn/codelldb/releases) and note the installation path.

### DAP Configuration

Add to your Neovim config (init.lua or equivalent):

```lua
local dap = require("dap")

-- Configure codelldb adapter
dap.adapters.codelldb = {
  type = 'server',
  port = "${port}",
  executable = {
    command = '/path/to/codelldb/adapter/codelldb',
    args = {"--port", "${port}"},
  }
}

-- Launch configuration for Rust/Tauri
dap.configurations.rust = {
  {
    name = "Launch Tauri App",
    type = "codelldb",
    request = "launch",
    program = function()
      return vim.fn.input('Path to executable: ', vim.fn.getcwd() .. '/target/debug/', 'file')
    end,
    cwd = '${workspaceFolder}',
    stopOnEntry = false
  },
}
```

### UI Integration

```lua
local dapui = require("dapui")
dapui.setup()

-- Auto-open/close UI
dap.listeners.before.attach.dapui_config = function()
  dapui.open()
end
dap.listeners.before.launch.dapui_config = function()
  dapui.open()
end
dap.listeners.before.event_terminated.dapui_config = function()
  dapui.close()
end
dap.listeners.before.event_exited.dapui_config = function()
  dapui.close()
end
```

### Visual Indicators

```lua
vim.fn.sign_define('DapBreakpoint', {
  text = 'B',
  texthl = 'DapBreakpoint',
  linehl = '',
  numhl = ''
})
vim.fn.sign_define('DapStopped', {
  text = '>',
  texthl = 'DapStopped',
  linehl = 'DapStopped',
  numhl = ''
})
```

### Keybindings

```lua
vim.keymap.set('n', '<F5>', function() dap.continue() end)
vim.keymap.set('n', '<F6>', function() dap.disconnect({ terminateDebuggee = true }) end)
vim.keymap.set('n', '<F10>', function() dap.step_over() end)
vim.keymap.set('n', '<F11>', function() dap.step_into() end)
vim.keymap.set('n', '<F12>', function() dap.step_out() end)
vim.keymap.set('n', '<Leader>b', function() dap.toggle_breakpoint() end)
vim.keymap.set('n', '<Leader>o', function() overseer.toggle() end)
vim.keymap.set('n', '<Leader>R', function() overseer.run_template() end)
```

### Development Server Task

Create `.vscode/tasks.json` for overseer.nvim compatibility:

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "type": "process",
      "label": "dev server",
      "command": "npm",
      "args": ["run", "dev"],
      "isBackground": true,
      "presentation": {
        "revealProblems": "onProblem"
      },
      "problemMatcher": {
        "pattern": {
          "regexp": "^error:.*",
          "file": 1,
          "line": 2
        },
        "background": {
          "activeOnStart": false,
          "beginsPattern": ".*Rebuilding.*",
          "endsPattern": ".*listening.*"
        }
      }
    }
  ]
}
```

> NOTE: The development server does not start automatically when bypassing Tauri CLI. Use overseer.nvim or start it manually.

---

## CrabNebula DevTools

CrabNebula DevTools provides real-time application instrumentation including log inspection, performance monitoring, and Tauri event/command analysis.

### Features

- Inspect log events (including dependency logs)
- Monitor command execution performance
- Analyze Tauri events with payloads and responses
- Real-time visualization

### Installation

```bash
cargo add tauri-plugin-devtools@2.0.0
```

### Setup

Initialize DevTools as early as possible in `src-tauri/src/main.rs`:

```rust
fn main() {
    // Initialize DevTools only in debug builds
    #[cfg(debug_assertions)]
    let devtools = tauri_plugin_devtools::init();

    let mut builder = tauri::Builder::default();

    #[cfg(debug_assertions)]
    {
        builder = builder.plugin(devtools);
    }

    builder
        .run(tauri::generate_context!())
        .expect("error while running tauri application")
}
```

### Usage

When running `tauri dev`, DevTools automatically opens a web-based interface showing:
- Application logs with filtering
- IPC command calls with timing
- Event payloads and responses
- Performance spans

For full documentation, see [CrabNebula DevTools docs](https://docs.crabnebula.dev/devtools/get-started/).

---

## Quick Reference

| Task | Command/Action |
|------|----------------|
| Enable backtraces | `RUST_BACKTRACE=1 tauri dev` |
| Open WebView DevTools | `Ctrl+Shift+i` / `Cmd+Option+i` |
| Debug build | `tauri build --debug` |
| Add DevTools plugin | `cargo add tauri-plugin-devtools@2.0.0` |

### IDE Comparison

| Feature | VS Code | RustRover | Neovim |
|---------|---------|-----------|--------|
| Extension/Plugin | vscode-lldb | Built-in | nvim-dap + codelldb |
| Windows Alt | cppvsdbg | Built-in | codelldb |
| Task Runner | tasks.json | Run configs | overseer.nvim |
| Setup Complexity | Medium | Low | High |

### Common Issues

1. **Breakpoints not hit**: Ensure `--no-default-features` is set when building
2. **Dev server not starting**: Configure `preLaunchTask` or start manually
3. **App not loading frontend**: Dev server must be running before Tauri app starts
4. **Windows enum display issues**: Use cppvsdbg instead of LLDB
