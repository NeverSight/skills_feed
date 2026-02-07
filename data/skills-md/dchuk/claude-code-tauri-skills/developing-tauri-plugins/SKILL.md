---
name: developing-tauri-plugins
description: Guides the user through Tauri plugin development, including creating plugin extensions, configuring permissions, and building mobile plugins for iOS and Android platforms.
---

# Developing Tauri Plugins

Tauri plugins extend application functionality through modular Rust crates with optional JavaScript bindings and native mobile implementations.

## Plugin Architecture

A complete plugin includes:
- **Rust crate** (`tauri-plugin-{name}`) - Core logic
- **JavaScript bindings** (`@scope/plugin-{name}`) - NPM package
- **Android library** (Kotlin) - Optional
- **iOS package** (Swift) - Optional

## Creating a Plugin

```bash
npx @tauri-apps/cli plugin new my-plugin              # Basic
npx @tauri-apps/cli plugin new my-plugin --android --ios  # With mobile
npx @tauri-apps/cli plugin android add                # Add to existing
npx @tauri-apps/cli plugin ios add
```

### Project Structure

```
tauri-plugin-my-plugin/
├── src/
│   ├── lib.rs, commands.rs, desktop.rs, mobile.rs, error.rs
├── permissions/          # Permission TOML files
├── guest-js/index.ts     # TypeScript API
├── android/, ios/        # Native mobile code
├── build.rs, Cargo.toml
```

## Plugin Implementation

### Main Plugin File (lib.rs)

```rust
use tauri::{plugin::{Builder, TauriPlugin}, Manager, Runtime};
mod commands;
mod error;
pub use error::{Error, Result};

#[cfg(desktop)] mod desktop;
#[cfg(mobile)] mod mobile;
#[cfg(desktop)] use desktop::MyPlugin;
#[cfg(mobile)] use mobile::MyPlugin;

pub struct MyPluginState<R: Runtime>(pub MyPlugin<R>);

pub fn init<R: Runtime>() -> TauriPlugin<R> {
    Builder::new("my-plugin")
        .invoke_handler(tauri::generate_handler![commands::do_something])
        .setup(|app, api| {
            app.manage(MyPluginState(MyPlugin::new(app, api)?));
            Ok(())
        })
        .build()
}
```

### Plugin with Configuration

```rust
use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct Config { pub timeout: Option<u64>, pub enabled: bool }

pub fn init<R: Runtime>() -> TauriPlugin<R, Config> {
    Builder::<R, Config>::new("my-plugin")
        .setup(|app, api| {
            let config = api.config();
            Ok(())
        })
        .build()
}
```

### Commands (commands.rs)

```rust
use tauri::{command, ipc::Channel, Runtime, State};
use crate::{MyPluginState, Result};

#[command]
pub async fn do_something<R: Runtime>(
    state: State<'_, MyPluginState<R>>, input: String,
) -> Result<String> {
    state.0.do_something(input).await
}

#[command]
pub async fn upload<R: Runtime>(path: String, on_progress: Channel<u32>) -> Result<()> {
    for i in 0..=100 { on_progress.send(i)?; }
    Ok(())
}
```

### Desktop Implementation (desktop.rs)

```rust
use tauri::{AppHandle, Runtime};
use crate::Result;

pub struct MyPlugin<R: Runtime> { app: AppHandle<R> }

impl<R: Runtime> MyPlugin<R> {
    pub fn new(app: &AppHandle<R>, _api: tauri::plugin::PluginApi<R, ()>) -> Result<Self> {
        Ok(Self { app: app.clone() })
    }
    pub async fn do_something(&self, input: String) -> Result<String> {
        Ok(format!("Desktop: {}", input))
    }
}
```

### Mobile Implementation (mobile.rs)

```rust
use tauri::{AppHandle, Runtime};
use serde::{Deserialize, Serialize};
use crate::Result;

#[derive(Serialize)] struct MobileRequest { value: String }
#[derive(Deserialize)] struct MobileResponse { result: String }

pub struct MyPlugin<R: Runtime> { app: AppHandle<R> }

impl<R: Runtime> MyPlugin<R> {
    pub fn new(app: &AppHandle<R>, _api: tauri::plugin::PluginApi<R, ()>) -> Result<Self> {
        Ok(Self { app: app.clone() })
    }
    pub async fn do_something(&self, input: String) -> Result<String> {
        let response: MobileResponse = self.app
            .run_mobile_plugin("doSomething", MobileRequest { value: input })
            .map_err(|e| crate::Error::Mobile(e.to_string()))?;
        Ok(response.result)
    }
}
```

### Error Handling (error.rs)

```rust
use serde::{Serialize, Serializer};

#[derive(Debug, thiserror::Error)]
pub enum Error {
    #[error("IO error: {0}")] Io(#[from] std::io::Error),
    #[error("Mobile error: {0}")] Mobile(String),
}

impl Serialize for Error {
    fn serialize<S>(&self, serializer: S) -> std::result::Result<S::Ok, S::Error>
    where S: Serializer { serializer.serialize_str(self.to_string().as_str()) }
}
pub type Result<T> = std::result::Result<T, Error>;
```

## Lifecycle Events

```rust
Builder::new("my-plugin")
    .setup(|app, api| { Ok(()) })                    // Plugin init
    .on_navigation(|window, url| url.scheme() != "dangerous")  // Block nav
    .on_webview_ready(|window| {})                   // Window created
    .on_event(|app, event| { match event { tauri::RunEvent::Exit => {} _ => {} }})
    .on_drop(|app| {})                               // Cleanup
    .build()
```

## JavaScript Bindings (guest-js/index.ts)

```typescript
import { invoke, Channel } from '@tauri-apps/api/core';

export async function doSomething(input: string): Promise<string> {
  return invoke('plugin:my-plugin|do_something', { input });
}

export async function upload(path: string, onProgress: (p: number) => void): Promise<void> {
  const channel = new Channel<number>();
  channel.onmessage = onProgress;
  return invoke('plugin:my-plugin|upload', { path, onProgress: channel });
}
```

## Plugin Permissions

### Permission File (permissions/default.toml)

```toml
[default]
description = "Default permissions"
permissions = ["allow-do-something"]

[[permission]]
identifier = "allow-do-something"
description = "Allows do_something command"
commands.allow = ["do_something"]

[[permission]]
identifier = "allow-upload"
description = "Allows upload command"
commands.allow = ["upload"]

[[set]]
identifier = "full-access"
description = "Full plugin access"
permissions = ["allow-do-something", "allow-upload"]
```

### Build Script (build.rs)

```rust
const COMMANDS: &[&str] = &["do_something", "upload"];
fn main() { tauri_plugin::Builder::new(COMMANDS).build(); }
```

### Scoped Permissions

```rust
use tauri::ipc::CommandScope;
use serde::Deserialize;

#[derive(Debug, Deserialize)]
pub struct PathScope { pub path: String }

#[command]
pub async fn read_file(path: String, scope: CommandScope<'_, PathScope>) -> Result<String> {
    let allowed = scope.allows().iter().any(|s| path.starts_with(&s.path));
    let denied = scope.denies().iter().any(|s| path.starts_with(&s.path));
    if denied || !allowed { return Err(Error::PermissionDenied); }
    // Read file...
}
```

## Android Plugin (Kotlin)

```kotlin
package com.example.myplugin

import android.app.Activity
import app.tauri.annotation.Command
import app.tauri.annotation.InvokeArg
import app.tauri.annotation.TauriPlugin
import app.tauri.plugin.Invoke
import app.tauri.plugin.JSObject
import app.tauri.plugin.Plugin
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch

@InvokeArg
class DoSomethingArgs {
    lateinit var value: String      // Required
    var optional: String? = null    // Optional
    var withDefault: Int = 42       // Default value
}

@TauriPlugin
class MyPlugin(private val activity: Activity) : Plugin(activity) {
    @Command
    fun doSomething(invoke: Invoke) {
        val args = invoke.parseArgs(DoSomethingArgs::class.java)
        CoroutineScope(Dispatchers.IO).launch {  // Use IO for blocking ops
            try {
                invoke.resolve(JSObject().apply { put("result", "Android: ${args.value}") })
            } catch (e: Exception) { invoke.reject(e.message) }
        }
    }
}
```

### Android Permissions

```kotlin
@TauriPlugin(permissions = [
    Permission(strings = [android.Manifest.permission.CAMERA], alias = "camera")
])
class MyPlugin(private val activity: Activity) : Plugin(activity) {
    @Command override fun checkPermissions(invoke: Invoke) { super.checkPermissions(invoke) }
    @Command override fun requestPermissions(invoke: Invoke) { super.requestPermissions(invoke) }
}
```

### Android Events & JNI

```kotlin
// Emit event
trigger("dataReceived", JSObject().apply { put("data", "value") })

// Lifecycle
override fun onNewIntent(intent: Intent) {
    trigger("newIntent", JSObject().apply { put("action", intent.action) })
}

// Call Rust via JNI
companion object { init { System.loadLibrary("my_plugin") } }
external fun processData(input: String): String  // Java_com_example_myplugin_MyPlugin_processData
```

## iOS Plugin (Swift)

```swift
import SwiftRs
import Tauri
import UIKit

class DoSomethingArgs: Decodable {
    let value: String       // Required
    var optional: String?   // Optional
}

class MyPlugin: Plugin {
    @objc public func doSomething(_ invoke: Invoke) throws {
        let args = try invoke.parseArgs(DoSomethingArgs.self)
        invoke.resolve(["result": "iOS: \(args.value)"])
    }
}

@_cdecl("init_plugin_my_plugin")
func initPlugin() -> Plugin { return MyPlugin() }
```

### iOS Permissions

```swift
import AVFoundation

class MyPlugin: Plugin {
    @objc override func checkPermissions(_ invoke: Invoke) {
        var result: [String: String] = [:]
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized: result["camera"] = "granted"
        case .denied, .restricted: result["camera"] = "denied"
        default: result["camera"] = "prompt"
        }
        invoke.resolve(result)
    }

    @objc override func requestPermissions(_ invoke: Invoke) {
        AVCaptureDevice.requestAccess(for: .video) { _ in self.checkPermissions(invoke) }
    }
}
```

### iOS Events & FFI

```swift
// Emit event
trigger("dataReceived", data: ["data": "value"])

// Call Rust via FFI
@_silgen_name("process_data_ffi")
private static func processDataFFI(_ input: UnsafePointer<CChar>) -> UnsafeMutablePointer<CChar>?

@objc public func hybrid(_ invoke: Invoke) throws {
    let args = try invoke.parseArgs(DoSomethingArgs.self)
    guard let ptr = MyPlugin.processDataFFI(args.value) else { invoke.reject("FFI failed"); return }
    invoke.resolve(["result": String(cString: ptr)])
    ptr.deallocate()
}
```

## Using the Plugin

### Register (src-tauri/src/lib.rs)

```rust
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_my_plugin::init())
        .run(tauri::generate_context!())
        .expect("error running application");
}
```

### Configure (tauri.conf.json)

```json
{ "plugins": { "my-plugin": { "timeout": 60, "enabled": true } } }
```

### Permissions (capabilities/default.json)

```json
{ "identifier": "default", "windows": ["main"], "permissions": ["my-plugin:default"] }
```

### Frontend Usage

```typescript
import { doSomething, upload } from '@myorg/plugin-my-plugin';
const result = await doSomething('hello');
await upload('/path/to/file', (p) => console.log(`${p}%`));
```

## Best Practices

- Separate platform code in `desktop.rs` and `mobile.rs`
- Use `thiserror` for structured error handling
- Use async for I/O operations; request only necessary permissions
- Android: Commands run on main thread - use coroutines for blocking work
- iOS: Clean up FFI resources properly; use `invoke.reject()`/`invoke.resolve()`

## Android 16KB Page Size

For NDK < 28, add to `.cargo/config.toml`:

```toml
[target.aarch64-linux-android]
rustflags = ["-C", "link-arg=-Wl,-z,max-page-size=16384"]
```
