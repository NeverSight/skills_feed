---
name: understanding-tauri-architecture
description: Teaches Claude about Tauri's core architecture, including the Rust backend, webview integration, Core-Shell design pattern, IPC mechanisms, and security model fundamentals.
---

# Tauri Architecture

Tauri is a polyglot toolkit for building desktop applications that combines a Rust backend with HTML/CSS/JavaScript rendered in a native webview. This document covers the fundamental architecture concepts.

## Architecture Overview

```
+------------------------------------------------------------------+
|                        TAURI APPLICATION                         |
+------------------------------------------------------------------+
|                                                                  |
|  +---------------------------+    +---------------------------+  |
|  |      FRONTEND (Shell)     |    |     BACKEND (Core)        |  |
|  |---------------------------|    |---------------------------|  |
|  |                           |    |                           |  |
|  |  HTML / CSS / JavaScript  |    |        Rust Code          |  |
|  |  (or any web framework)   |    |    (tauri crate + app)    |  |
|  |                           |    |                           |  |
|  |  - React, Vue, Svelte,    |    |  - System access          |  |
|  |    Solid, etc.            |    |  - File operations        |  |
|  |  - Standard web APIs      |    |  - Native features        |  |
|  |  - Tauri JS API           |    |  - Plugin system          |  |
|  |                           |    |                           |  |
|  +-------------+-------------+    +-------------+-------------+  |
|                |                                |                 |
|                |       IPC (Message Passing)    |                 |
|                +<------------------------------->+                |
|                |     Commands & Events          |                 |
|                                                                  |
|  +------------------------------------------------------------+  |
|  |                    WEBVIEW (TAO + WRY)                     |  |
|  |------------------------------------------------------------|  |
|  |  - Platform-native webview (not bundled)                   |  |
|  |  - Windows: WebView2 (Edge/Chromium)                       |  |
|  |  - macOS: WKWebView (Safari/WebKit)                        |  |
|  |  - Linux: WebKitGTK                                        |  |
|  +------------------------------------------------------------+  |
|                                                                  |
+------------------------------------------------------------------+
                                |
                                v
+------------------------------------------------------------------+
|                     OPERATING SYSTEM                             |
|  - Windows, macOS, Linux, iOS, Android                          |
+------------------------------------------------------------------+
```

## Core vs Shell Design

Tauri follows a **Core-Shell architecture** where the application is split into two distinct layers:

### The Core (Rust Backend)

The Core is the Rust-based backend that handles all system-level operations:

- **System access**: File system, network, processes
- **Native features**: Notifications, dialogs, clipboard
- **Security enforcement**: Permission validation, capability checking
- **Plugin management**: Extending functionality through plugins
- **App lifecycle**: Window management, updates, configuration

The Core NEVER exposes direct system access to the frontend. All interactions go through validated IPC channels.

### The Shell (Frontend)

The Shell is the user interface layer rendered in a webview:

- **Web technologies**: HTML, CSS, JavaScript/TypeScript
- **Framework agnostic**: Works with React, Vue, Svelte, Solid, or vanilla JS
- **Sandboxed execution**: Runs in the webview's security sandbox
- **Tauri API access**: Calls backend through `@tauri-apps/api`

## Key Ecosystem Components

### tauri Crate

The central orchestrator that:
- Reads `tauri.conf.json` at compile time
- Manages script injection into the webview
- Hosts the system interaction API
- Handles application updates
- Integrates runtimes, macros, and utilities

### tauri-runtime

The glue layer between Tauri and lower-level webview libraries. Abstracts platform-specific webview interactions so the rest of Tauri can remain platform-agnostic.

### tauri-macros and tauri-codegen

Generate compile-time code for:
- Command handlers (`#[tauri::command]`)
- Context and configuration parsing
- Asset embedding and compression

### TAO (Window Management)

Cross-platform window creation library (forked from Winit):
- Creates and manages application windows
- Handles menu bars and system trays
- Supports Windows, macOS, Linux, iOS, Android

### WRY (WebView Rendering)

Cross-platform WebView rendering library:
- Abstracts webview implementations per platform
- Handles webview-to-native communication
- Manages JavaScript evaluation and event bridging

## Webview Integration

Tauri uses the **operating system's native webview** rather than bundling a browser engine:

```
+-------------------+---------------------------+
|     Platform      |        WebView Engine     |
+-------------------+---------------------------+
| Windows           | WebView2 (Edge/Chromium)  |
| macOS             | WKWebView (Safari/WebKit) |
| Linux             | WebKitGTK                 |
| iOS               | WKWebView                 |
| Android           | Android WebView           |
+-------------------+---------------------------+
```

### Benefits of Native WebViews

1. **Smaller binary size**: No bundled browser engine (~600KB vs ~150MB)
2. **Security**: OS vendors patch webview vulnerabilities faster than app developers can rebuild
3. **Performance**: Native integration with the operating system
4. **Consistency**: Users see familiar rendering behavior

### Considerations

- Slight rendering differences between platforms
- Feature availability depends on OS webview version
- Testing should cover all target platforms

## Inter-Process Communication (IPC)

Tauri implements **Asynchronous Message Passing** for communication between frontend and backend. This is safer than shared memory because the Core can reject malicious requests.

### IPC Flow Diagram

```
+------------------+                      +------------------+
|    Frontend      |                      |   Rust Backend   |
|   (JavaScript)   |                      |     (Core)       |
+--------+---------+                      +--------+---------+
         |                                         |
         |  1. invoke('command', {args})           |
         +---------------------------------------->|
         |                                         |
         |     [Request serialized as JSON-RPC]    |
         |                                         |
         |                    2. Validate request  |
         |                    3. Check permissions |
         |                    4. Execute command   |
         |                                         |
         |  5. Return Result<T, E>                 |
         |<----------------------------------------+
         |                                         |
         |     [Response serialized as JSON]       |
         |                                         |
```

### Two IPC Primitives

#### Commands (Request-Response)

Type-safe, frontend-to-backend function calls:

```rust
// Rust backend
#[tauri::command]
fn greet(name: String) -> String {
    format!("Hello, {}!", name)
}

// Register in builder
tauri::Builder::default()
    .invoke_handler(tauri::generate_handler![greet])
```

```javascript
// JavaScript frontend
import { invoke } from '@tauri-apps/api/core';

const greeting = await invoke('greet', { name: 'World' });
console.log(greeting); // "Hello, World!"
```

Key characteristics:
- Built on JSON-RPC protocol
- All arguments must be JSON-serializable
- Returns a Promise that resolves with the result
- Supports async Rust functions
- Can access app state, window handle, etc.

#### Events (Fire-and-Forget)

Bidirectional, asynchronous notifications:

```javascript
// Frontend: emit event
import { emit } from '@tauri-apps/api/event';
emit('user-action', { action: 'clicked' });

// Frontend: listen for events
import { listen } from '@tauri-apps/api/event';
const unlisten = await listen('download-progress', (event) => {
    console.log(event.payload);
});
```

```rust
// Backend: listen for events
use tauri::Listener;

app.listen("user-action", |event| {
    println!("User action: {}", event.payload());
});

// Backend: emit events
app.emit("download-progress", 50)?;
```

Key characteristics:
- No return value (one-way)
- Both frontend and backend can emit/listen
- Best for lifecycle events and state changes
- Not type-checked at compile time

## Security Model Overview

Tauri implements multiple layers of security to protect both the application and the user's system.

### Trust Boundary Model

```
+------------------------------------------------------------------+
|                     UNTRUSTED ZONE                               |
|  +------------------------------------------------------------+  |
|  |                    WebView Frontend                        |  |
|  |  - JavaScript code (potentially from remote sources)       |  |
|  |  - User input                                              |  |
|  |  - Third-party libraries                                   |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
                              |
                    [TRUST BOUNDARY]
                    [IPC Layer validates all requests]
                              |
+------------------------------------------------------------------+
|                      TRUSTED ZONE                                |
|  +------------------------------------------------------------+  |
|  |                    Rust Backend                            |  |
|  |  - Your Rust code                                          |  |
|  |  - Tauri core                                              |  |
|  |  - System access (gated by permissions)                    |  |
|  +------------------------------------------------------------+  |
+------------------------------------------------------------------+
```

### Security Layers

1. **WebView Sandboxing**: Frontend code runs in the webview's security sandbox
2. **IPC Validation**: All messages crossing the trust boundary are validated
3. **Capabilities**: Define which permissions each window can access
4. **Permissions**: Fine-grained control over what operations are allowed
5. **Scopes**: Restrict command behavior (e.g., limit file access to specific directories)
6. **CSP**: Content Security Policy restricts what frontend code can do

### Capabilities System

Capabilities control which permissions are granted to specific windows:

```json
{
  "$schema": "../gen/schemas/desktop-schema.json",
  "identifier": "main-window-capability",
  "description": "Permissions for the main application window",
  "windows": ["main"],
  "permissions": [
    "core:path:default",
    "core:window:allow-set-title",
    "fs:read-files",
    "fs:scope-app-data"
  ]
}
```

Capabilities are defined in `src-tauri/capabilities/` as JSON or TOML files.

### Permission Structure

```
Capability
    |
    +-- windows: ["main", "settings"]  // Which windows
    |
    +-- permissions:                    // What's allowed
            |
            +-- "plugin:action"         // Allow specific action
            +-- "plugin:scope-xxx"      // Scope restrictions
```

### Default Security Posture

- **Deny by default**: Commands must be explicitly permitted
- **No remote access**: Only bundled code can access Tauri APIs by default
- **Window isolation**: Each window has its own capability set
- **Compile-time checks**: Many security configurations are validated at build time

## Rust Backend Structure

A typical Tauri backend follows this structure:

```
src-tauri/
+-- Cargo.toml              # Rust dependencies
+-- tauri.conf.json         # Tauri configuration
+-- capabilities/           # Permission definitions
|   +-- main.json
+-- src/
    +-- main.rs             # Entry point (desktop)
    +-- lib.rs              # Core app logic
    +-- commands/           # Command modules
    |   +-- mod.rs
    |   +-- file_ops.rs
    +-- state.rs            # App state management
```

### Entry Point Pattern

```rust
// src-tauri/src/lib.rs
mod commands;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![
            commands::greet,
            commands::read_file,
        ])
        .manage(AppState::default())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Command Patterns

```rust
// Basic command
#[tauri::command]
fn simple_command() -> String {
    "Hello".into()
}

// With arguments (camelCase from JS, snake_case in Rust)
#[tauri::command]
fn with_args(user_name: String, age: u32) -> String {
    format!("{} is {} years old", user_name, age)
}

// With error handling
#[tauri::command]
fn fallible() -> Result<String, String> {
    Ok("Success".into())
}

// Async command
#[tauri::command]
async fn async_command() -> Result<String, String> {
    tokio::time::sleep(Duration::from_secs(1)).await;
    Ok("Done".into())
}

// Accessing app state
#[tauri::command]
fn with_state(state: tauri::State<'_, AppState>) -> String {
    state.get_value()
}

// Accessing window
#[tauri::command]
fn with_window(window: tauri::WebviewWindow) -> String {
    window.label().to_string()
}
```

## No Runtime Bundled

Tauri does NOT ship a runtime. The final binary:
- Compiles Rust code directly into native machine code
- Embeds frontend assets in the binary
- Uses the system's native webview
- Results in small, fast executables

This makes reverse engineering Tauri apps non-trivial compared to Electron apps with bundled JavaScript.

## Summary

| Component | Role |
|-----------|------|
| **Core (Rust)** | System access, security, business logic |
| **Shell (Frontend)** | UI rendering, user interaction |
| **WebView (TAO+WRY)** | Platform-native rendering bridge |
| **IPC (Commands/Events)** | Safe message passing between layers |
| **Capabilities** | Permission control per window |

The architecture prioritizes:
1. **Security**: Multiple layers of protection, trust boundaries
2. **Performance**: Native code, no bundled runtime
3. **Size**: Minimal binary footprint
4. **Flexibility**: Any frontend framework, powerful Rust backend
