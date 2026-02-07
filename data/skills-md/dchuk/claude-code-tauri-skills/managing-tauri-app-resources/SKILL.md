---
name: managing-tauri-app-resources
description: Assists with managing Tauri application resources including app icons setup and generation, embedding static files and assets, accessing bundled resources at runtime, and implementing thread-safe state management patterns.
---

# Managing Tauri App Resources

## App Icons

### Icon Generation

Generate all platform-specific icons from a single source file:

```bash
cargo tauri icon              # Default: ./app-icon.png
cargo tauri icon ./custom.png -o ./icons  # Custom source/output
cargo tauri icon --ios-color "#000000"    # iOS background color
```

**Source requirements:** Squared PNG or SVG with transparency.

### Generated Formats

| Format | Platform |
|--------|----------|
| `icon.icns` | macOS |
| `icon.ico` | Windows |
| `*.png` | Linux, Android, iOS |

### Configuration

```json
{
  "bundle": {
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/128x128@2x.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ]
  }
}
```

### Platform Requirements

**Windows (.ico):** Layers for 16, 24, 32, 48, 64, 256 pixels.

**Android:** No transparency. Place in `src-tauri/gen/android/app/src/main/res/mipmap-*` folders. Each needs `ic_launcher.png`, `ic_launcher_round.png`, `ic_launcher_foreground.png`.

**iOS:** No transparency. Place in `src-tauri/gen/apple/Assets.xcassets/AppIcon.appiconset/`. Required sizes: 20, 29, 40, 60, 76, 83.5 pixels with 1x/2x/3x scales, plus 512x512@2x.

---

## Embedding Static Resources

### Configuration

**Array syntax** (preserves directory structure):

```json
{
  "bundle": {
    "resources": ["./file.txt", "folder/", "docs/**/*.md"]
  }
}
```

**Map syntax** (custom destinations):

```json
{
  "bundle": {
    "resources": {
      "path/to/source.json": "resources/dest.json",
      "docs/**/*.md": "website-docs/"
    }
  }
}
```

### Path Patterns

| Pattern | Behavior |
|---------|----------|
| `"dir/file.txt"` | Single file |
| `"dir/"` | Directory recursive |
| `"dir/*"` | Files non-recursive |
| `"dir/**/*"` | All files recursive |

### Accessing Resources - Rust

```rust
use tauri::Manager;
use tauri::path::BaseDirectory;

#[tauri::command]
fn load_resource(handle: tauri::AppHandle) -> Result<String, String> {
    let path = handle
        .path()
        .resolve("lang/de.json", BaseDirectory::Resource)
        .map_err(|e| e.to_string())?;
    std::fs::read_to_string(&path).map_err(|e| e.to_string())
}
```

### Accessing Resources - JavaScript

```javascript
import { resolveResource } from '@tauri-apps/api/path';
import { readTextFile } from '@tauri-apps/plugin-fs';

const resourcePath = await resolveResource('lang/de.json');
const content = await readTextFile(resourcePath);
const data = JSON.parse(content);
```

### Permissions

```json
{
  "permissions": [
    "fs:allow-read-text-file",
    "fs:allow-resource-read-recursive"
  ]
}
```

Use `$RESOURCE/**/*` scope for recursive access.

---

## State Management

### Basic Setup

```rust
use tauri::{Builder, Manager};

struct AppData {
    welcome_message: &'static str,
}

fn main() {
    Builder::default()
        .setup(|app| {
            app.manage(AppData {
                welcome_message: "Welcome!",
            });
            Ok(())
        })
        .run(tauri::generate_context!())
        .unwrap()
}
```

### Thread-Safe Mutable State

```rust
use std::sync::Mutex;
use tauri::{Builder, Manager};

#[derive(Default)]
struct AppState {
    counter: u32,
}

fn main() {
    Builder::default()
        .setup(|app| {
            app.manage(Mutex::new(AppState::default()));
            Ok(())
        })
        .run(tauri::generate_context!())
        .unwrap()
}
```

### Accessing State in Commands

```rust
use std::sync::Mutex;
use tauri::State;

#[tauri::command]
fn increase_counter(state: State<'_, Mutex<AppState>>) -> u32 {
    let mut state = state.lock().unwrap();
    state.counter += 1;
    state.counter
}

#[tauri::command]
fn get_counter(state: State<'_, Mutex<AppState>>) -> u32 {
    state.lock().unwrap().counter
}
```

### Async Commands with Tokio Mutex

```rust
use tokio::sync::Mutex;
use tauri::State;

#[tauri::command]
async fn increase_counter_async(
    state: State<'_, Mutex<AppState>>
) -> Result<u32, ()> {
    let mut state = state.lock().await;
    state.counter += 1;
    Ok(state.counter)
}
```

### Accessing State Outside Commands

```rust
use std::sync::Mutex;
use tauri::{Manager, Window, WindowEvent};

fn on_window_event(window: &Window, event: &WindowEvent) {
    let app_handle = window.app_handle();
    let state = app_handle.state::<Mutex<AppState>>();
    let mut state = state.lock().unwrap();
    state.counter += 1;
}
```

### Type Alias Pattern

Prevent runtime panics from type mismatches:

```rust
use std::sync::Mutex;

struct AppStateInner {
    counter: u32,
}

type AppState = Mutex<AppStateInner>;

#[tauri::command]
fn get_counter(state: State<'_, AppState>) -> u32 {
    state.lock().unwrap().counter
}
```

### Multiple State Types

```rust
use std::sync::Mutex;
use tauri::{Builder, Manager, State};

struct UserState { username: Option<String> }
struct AppSettings { theme: String }

fn main() {
    Builder::default()
        .setup(|app| {
            app.manage(Mutex::new(UserState { username: None }));
            app.manage(Mutex::new(AppSettings { theme: "dark".into() }));
            Ok(())
        })
        .run(tauri::generate_context!())
        .unwrap()
}

#[tauri::command]
fn login(user_state: State<'_, Mutex<UserState>>, username: String) {
    user_state.lock().unwrap().username = Some(username);
}

#[tauri::command]
fn set_theme(settings: State<'_, Mutex<AppSettings>>, theme: String) {
    settings.lock().unwrap().theme = theme;
}
```

### Key Points

- **Arc not required** - Tauri handles reference counting internally
- **Use std::sync::Mutex** for most cases; Tokio's mutex only for holding locks across await points
- **Type safety** - Wrong state types cause runtime panics, not compile errors; use type aliases

---

## Complete Example

**tauri.conf.json:**

```json
{
  "bundle": {
    "icon": [
      "icons/32x32.png",
      "icons/128x128.png",
      "icons/icon.icns",
      "icons/icon.ico"
    ],
    "resources": {
      "assets/config.json": "config.json",
      "assets/translations/": "lang/"
    }
  }
}
```

**src-tauri/src/main.rs:**

```rust
use std::sync::Mutex;
use serde::{Deserialize, Serialize};
use tauri::{Builder, Manager, State};
use tauri::path::BaseDirectory;

#[derive(Default)]
struct AppState { counter: u32, locale: String }
type ManagedState = Mutex<AppState>;

#[derive(Serialize, Deserialize)]
struct Config { app_name: String, version: String }

#[tauri::command]
fn increment(state: State<'_, ManagedState>) -> u32 {
    let mut s = state.lock().unwrap();
    s.counter += 1;
    s.counter
}

#[tauri::command]
fn load_config(handle: tauri::AppHandle) -> Result<Config, String> {
    let path = handle.path()
        .resolve("config.json", BaseDirectory::Resource)
        .map_err(|e| e.to_string())?;
    let content = std::fs::read_to_string(&path).map_err(|e| e.to_string())?;
    serde_json::from_str(&content).map_err(|e| e.to_string())
}

fn main() {
    Builder::default()
        .setup(|app| {
            app.manage(Mutex::new(AppState::default()));
            Ok(())
        })
        .invoke_handler(tauri::generate_handler![increment, load_config])
        .run(tauri::generate_context!())
        .unwrap()
}
```

**Frontend:**

```javascript
import { invoke } from '@tauri-apps/api/core';
import { resolveResource } from '@tauri-apps/api/path';
import { readTextFile } from '@tauri-apps/plugin-fs';

const newValue = await invoke('increment');
const config = await invoke('load_config');
const langPath = await resolveResource('lang/en.json');
const translations = JSON.parse(await readTextFile(langPath));
```

---

## Quick Reference

### Icon Commands
```bash
cargo tauri icon                    # Generate from ./app-icon.png
cargo tauri icon ./icon.png -o out  # Custom source/output
```

### Resource Patterns
```json
{ "resources": ["data.json"] }              // Single file
{ "resources": ["assets/"] }                // Directory recursive
{ "resources": { "src/x.json": "x.json" }}  // Custom destination
```

### State Patterns
```rust
app.manage(Config { ... });              // Immutable
app.manage(Mutex::new(State { ... }));   // Mutable
fn cmd(state: State<'_, Mutex<T>>)       // In command
app_handle.state::<Mutex<T>>()           // Via AppHandle
```
