---
name: tauri
description: "Comprehensive Tauri v2 development skill for building cross-platform desktop applications with Rust backends and web frontends. This skill should be used when creating new Tauri apps, adding commands and IPC communication, developing plugins, managing application state, or integrating Rust with JavaScript/TypeScript frontends. Triggers on tasks involving #[tauri::command], invoke(), Tauri plugins, desktop app development, or Rust-WebView integration."
---

# Tauri Development

## Overview

Tauri is a framework for building lightweight, secure desktop applications using web technologies for the frontend and Rust for the backend. This skill provides guidance for Tauri v2 development including:

- Creating and registering commands (Rust-to-JS communication)
- Event system for background operations
- State management across commands
- Plugin development with permissions
- Best practices for security and performance

## Quick Reference

### Project Structure

```
my-app/
├── src/                    # Frontend (React/Vue/Svelte/etc.)
├── src-tauri/
│   ├── src/
│   │   ├── lib.rs          # App setup, command registration
│   │   ├── main.rs         # Binary entry point
│   │   └── commands/       # Command modules (recommended)
│   │       ├── mod.rs
│   │       └── feature.rs
│   ├── Cargo.toml
│   ├── tauri.conf.json     # App configuration
│   └── capabilities/       # Permission definitions
└── package.json
```

### Essential Imports

**Rust:**
```rust
use tauri::{command, AppHandle, State, Emitter, Runtime};
use serde::{Deserialize, Serialize};
```

**JavaScript/TypeScript:**
```typescript
import { invoke } from '@tauri-apps/api/core';
import { listen } from '@tauri-apps/api/event';
```

## Creating Commands

### Basic Command

```rust
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}!", name)
}
```

Register in `lib.rs`:
```rust
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

Call from frontend:
```typescript
const result = await invoke('greet', { name: 'World' });
```

### Async Commands

Use async for I/O operations, database queries, or network requests:

```rust
#[tauri::command]
async fn fetch_data(url: String) -> Result<String, String> {
    reqwest::get(&url)
        .await
        .map_err(|e| e.to_string())?
        .text()
        .await
        .map_err(|e| e.to_string())
}
```

**Important:** Async commands cannot use borrowed types (`&str`). Convert to owned types:

```rust
// Won't compile:
async fn bad(name: &str) -> String { ... }

// Use this instead:
async fn good(name: String) -> String { ... }
```

### Commands with AppHandle

Access application-wide functionality:

```rust
#[tauri::command]
async fn save_file(app: tauri::AppHandle, content: String) -> Result<(), String> {
    let app_dir = app.path().app_data_dir().map_err(|e| e.to_string())?;
    std::fs::write(app_dir.join("data.txt"), content).map_err(|e| e.to_string())
}
```

### Commands with WebviewWindow

Access the calling window:

```rust
#[tauri::command]
fn get_window_label(window: tauri::WebviewWindow) -> String {
    window.label().to_string()
}
```

## Error Handling

### Simple String Errors

```rust
#[tauri::command]
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("cannot divide by zero".to_string())
    } else {
        Ok(a / b)
    }
}
```

### Custom Error Types (Recommended)

```rust
use thiserror::Error;
use serde::Serialize;

#[derive(Debug, Error)]
pub enum AppError {
    #[error("database error: {0}")]
    Database(#[from] rusqlite::Error),
    #[error("file not found: {0}")]
    NotFound(String),
    #[error("permission denied")]
    PermissionDenied,
}

impl Serialize for AppError {
    fn serialize<S>(&self, serializer: S) -> Result<S::Ok, S::Error>
    where
        S: serde::ser::Serializer,
    {
        serializer.serialize_str(self.to_string().as_ref())
    }
}

type Result<T> = std::result::Result<T, AppError>;

#[tauri::command]
fn load_config() -> Result<Config> {
    // Errors auto-convert via From trait
}
```

Frontend error handling:
```typescript
try {
    const result = await invoke('load_config');
} catch (error) {
    console.error('Command failed:', error);
}
```

## State Management

Share data across commands using managed state:

```rust
use std::sync::Mutex;

struct AppState {
    counter: Mutex<i32>,
    config: Config,
}

#[tauri::command]
fn increment(state: tauri::State<AppState>) -> i32 {
    let mut counter = state.counter.lock().unwrap();
    *counter += 1;
    *counter
}

#[tauri::command]
fn get_config(state: tauri::State<AppState>) -> Config {
    state.config.clone()
}

pub fn run() {
    tauri::Builder::default()
        .manage(AppState {
            counter: Mutex::new(0),
            config: Config::default(),
        })
        .invoke_handler(tauri::generate_handler![increment, get_config])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**Async commands with state** require owned access:

```rust
#[tauri::command]
async fn async_with_state(state: tauri::State<'_, AppState>) -> Result<String, String> {
    // Clone what you need before async operations
    let config = state.config.clone();
    // Now safe to await
    Ok(format!("{:?}", config))
}
```

## Event System

Emit events from Rust to notify frontend of background operations:

### Emitting Events

```rust
use tauri::Emitter;

#[tauri::command]
async fn long_running_task(app: AppHandle) -> Result<(), String> {
    app.emit("task-started", ()).map_err(|e| e.to_string())?;

    for i in 0..100 {
        // Do work...
        app.emit("task-progress", i).map_err(|e| e.to_string())?;
    }

    app.emit("task-complete", "done").map_err(|e| e.to_string())?;
    Ok(())
}
```

### Listening in Frontend

```typescript
import { listen } from '@tauri-apps/api/event';

const unlisten = await listen('task-progress', (event) => {
    console.log('Progress:', event.payload);
});

// Clean up when done
unlisten();
```

### Typed Event Payloads

```rust
#[derive(Clone, Serialize)]
struct ProgressPayload {
    step: usize,
    total: usize,
    message: String,
}

app.emit("progress", ProgressPayload {
    step: 50,
    total: 100,
    message: "Processing...".to_string(),
})?;
```

## Organizing Commands

For larger applications, organize commands in modules:

**src-tauri/src/commands/mod.rs:**
```rust
pub mod files;
pub mod database;
pub mod auth;
```

**src-tauri/src/commands/files.rs:**
```rust
use tauri::command;

#[command]
pub fn read_file(path: String) -> Result<String, String> {
    std::fs::read_to_string(&path).map_err(|e| e.to_string())
}

#[command]
pub fn write_file(path: String, content: String) -> Result<(), String> {
    std::fs::write(&path, content).map_err(|e| e.to_string())
}
```

**src-tauri/src/lib.rs:**
```rust
mod commands;

pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            commands::files::read_file,
            commands::files::write_file,
            commands::database::query,
            commands::auth::login,
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Performance Optimization

### Large Data Returns

Bypass JSON serialization for binary data:

```rust
use tauri::ipc::Response;

#[tauri::command]
fn read_binary_file(path: String) -> Result<Response, String> {
    let data = std::fs::read(&path).map_err(|e| e.to_string())?;
    Ok(Response::new(data))
}
```

### Streaming with Channels

For real-time data streaming:

```rust
use tauri::ipc::Channel;

#[tauri::command]
fn stream_logs(channel: Channel<String>) {
    std::thread::spawn(move || {
        loop {
            let log_line = get_next_log();
            if channel.send(log_line).is_err() {
                break; // Frontend closed channel
            }
        }
    });
}
```

## Plugin Development

### Plugin Structure

Initialize with: `npx @tauri-apps/cli plugin new my-plugin`

```
tauri-plugin-my-plugin/
├── src/
│   ├── lib.rs          # Plugin entry point
│   ├── commands.rs     # Plugin commands
│   ├── error.rs        # Error types
│   └── models.rs       # Data structures
├── permissions/        # Permission definitions
├── guest-js/           # TypeScript bindings
└── Cargo.toml
```

### Basic Plugin

**src/lib.rs:**
```rust
use tauri::{
    plugin::{Builder, TauriPlugin},
    Manager, Runtime,
};

mod commands;
mod error;

pub fn init<R: Runtime>() -> TauriPlugin<R> {
    Builder::new("my-plugin")
        .invoke_handler(tauri::generate_handler![
            commands::do_something
        ])
        .setup(|app, api| {
            // Initialize plugin state
            Ok(())
        })
        .build()
}
```

**src/commands.rs:**
```rust
use tauri::{command, AppHandle, Runtime};

#[command]
pub async fn do_something<R: Runtime>(app: AppHandle<R>) -> Result<String, String> {
    Ok("done".to_string())
}
```

### Using Plugins

```rust
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_my_plugin::init())
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Plugin Permissions

Define in `permissions/default.toml`:
```toml
[default]
description = "Default permissions for my-plugin"
permissions = ["allow-do-something"]

[[permission]]
identifier = "allow-do-something"
description = "Allows the do_something command"
commands.allow = ["do_something"]
```

See `references/plugin-development.md` for comprehensive plugin guidance.

## Security Best Practices

1. **Validate all input** from frontend before processing
2. **Use capabilities** to explicitly allow commands in `tauri.conf.json`
3. **Never trust paths** - validate and sanitize file paths
4. **Avoid shell commands** when possible; use Rust APIs
5. **Define granular permissions** for plugin commands
6. **Use the isolation pattern** for applications with untrusted content

## Resources

### References

- `references/commands-reference.md` - Detailed command patterns and examples
- `references/plugin-development.md` - Complete plugin development guide

### Official Documentation

- [Tauri v2 Docs](https://v2.tauri.app/)
- [Calling Rust from Frontend](https://v2.tauri.app/develop/calling-rust/)
- [Plugin Development](https://v2.tauri.app/develop/plugins/)
- [IPC Concepts](https://v2.tauri.app/concept/inter-process-communication/)
