---
name: integrating-tauri-rust-frontends
description: Guides the user through integrating Rust-based WASM frontend frameworks with Tauri v2, covering Leptos and Trunk setup, WASM compilation configuration, Cargo.toml dependencies, Trunk.toml bundler settings, and withGlobalTauri API access.
---

# Tauri Rust/WASM Frontend Integration

This skill covers integrating Rust-based frontend frameworks with Tauri v2 for building desktop and mobile applications with WASM.

## Supported Frameworks

| Framework | Description | Bundler |
|-----------|-------------|---------|
| Leptos | Reactive Rust framework for building web UIs | Trunk |
| Yew | Component-based Rust framework | Trunk |
| Dioxus | Cross-platform UI framework | Trunk |
| Sycamore | Reactive library for Rust | Trunk |

All Rust/WASM frontends use **Trunk** as the bundler/dev server.

## Critical Requirements

1. **Static Site Generation (SSG) Only** - Tauri does not support server-based solutions (SSR). Use SSG, SPA, or MPA approaches.
2. **withGlobalTauri** - Must be enabled for WASM frontends to access Tauri APIs via `window.__TAURI__` and `wasm-bindgen`.
3. **WebSocket Protocol** - Configure `ws_protocol = "ws"` for hot-reload on mobile development.

## Project Structure

```
my-tauri-app/
├── src/
│   ├── main.rs          # Rust frontend entry point
│   └── app.rs           # Application component
├── src-tauri/
│   ├── src/
│   │   └── main.rs      # Tauri backend
│   ├── Cargo.toml       # Tauri dependencies
│   └── tauri.conf.json  # Tauri configuration
├── index.html           # HTML entry point for Trunk
├── Cargo.toml           # Frontend dependencies
├── Trunk.toml           # Trunk bundler configuration
└── dist/                # Build output (generated)
```

## Configuration Files

### Tauri Configuration (src-tauri/tauri.conf.json)

```json
{
  "build": {
    "beforeDevCommand": "trunk serve",
    "devUrl": "http://localhost:1420",
    "beforeBuildCommand": "trunk build",
    "frontendDist": "../dist"
  },
  "app": {
    "withGlobalTauri": true
  }
}
```

**Key settings:**
- `beforeDevCommand`: Runs Trunk dev server before Tauri
- `devUrl`: URL where Trunk serves the frontend (default: 1420 for Leptos, 8080 for plain Trunk)
- `beforeBuildCommand`: Builds WASM bundle before packaging
- `frontendDist`: Path to built frontend assets
- `withGlobalTauri`: **Required for WASM** - Exposes `window.__TAURI__` for API access

### Trunk Configuration (Trunk.toml)

```toml
[build]
target = "./index.html"
dist = "./dist"

[watch]
ignore = ["./src-tauri"]

[serve]
port = 1420
open = false

[serve.ws]
ws_protocol = "ws"
```

**Key settings:**
- `target`: HTML entry point with Trunk directives
- `ignore`: Prevents watching Tauri backend changes
- `port`: Must match `devUrl` in tauri.conf.json
- `open = false`: Prevents browser auto-open (Tauri handles display)
- `ws_protocol = "ws"`: Required for mobile hot-reload

### Frontend Cargo.toml (Root)

```toml
[package]
name = "my-app-frontend"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib", "rlib"]

[dependencies]
# Core WASM dependencies
wasm-bindgen = "0.2"
wasm-bindgen-futures = "0.4"
js-sys = "0.3"
web-sys = { version = "0.3", features = ["Window", "Document"] }

# Tauri API bindings for WASM
tauri-wasm = { version = "2", features = ["all"] }

# Choose your framework:
# For Leptos:
leptos = { version = "0.6", features = ["csr"] }
# For Yew:
# yew = { version = "0.21", features = ["csr"] }
# For Dioxus:
# dioxus = { version = "0.5", features = ["web"] }

[profile.release]
opt-level = "z"
lto = true
codegen-units = 1
panic = "abort"
```

**Key settings:**
- `crate-type = ["cdylib", "rlib"]`: Required for WASM compilation
- `tauri-wasm`: Provides Rust bindings to Tauri APIs
- `features = ["csr"]`: Client-side rendering for framework
- Release profile optimized for small WASM binary size

### HTML Entry Point (index.html)

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>My Tauri App</title>
    <link data-trunk rel="css" href="styles.css" />
</head>
<body>
    <div id="app"></div>
    <link data-trunk rel="rust" href="." data-wasm-opt="z" />
</body>
</html>
```

**Trunk directives:**
- `data-trunk rel="css"`: Include CSS files
- `data-trunk rel="rust"`: Compile Rust crate to WASM
- `data-wasm-opt="z"`: Optimize for size

## Leptos Setup

### Leptos-Specific Cargo.toml

```toml
[package]
name = "my-leptos-app"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib", "rlib"]

[dependencies]
leptos = { version = "0.6", features = ["csr"] }
wasm-bindgen = "0.2"
wasm-bindgen-futures = "0.4"
console_error_panic_hook = "0.1"
tauri-wasm = { version = "2", features = ["all"] }

[profile.release]
opt-level = "z"
lto = true
```

### Leptos Main Entry (src/main.rs)

```rust
use leptos::*;

mod app;
use app::App;

fn main() {
    console_error_panic_hook::set_once();
    mount_to_body(|| view! { <App /> });
}
```

### Leptos App Component (src/app.rs)

```rust
use leptos::*;
use wasm_bindgen::prelude::*;
use wasm_bindgen_futures::spawn_local;

#[wasm_bindgen]
extern "C" {
    #[wasm_bindgen(js_namespace = ["window", "__TAURI__", "core"])]
    async fn invoke(cmd: &str, args: JsValue) -> JsValue;
}

#[component]
pub fn App() -> impl IntoView {
    let (message, set_message) = create_signal(String::new());

    let greet = move |_| {
        spawn_local(async move {
            let args = serde_json::json!({ "name": "World" });
            let args_js = serde_wasm_bindgen::to_value(&args).unwrap();
            let result = invoke("greet", args_js).await;
            let greeting: String = serde_wasm_bindgen::from_value(result).unwrap();
            set_message.set(greeting);
        });
    };

    view! {
        <main>
            <h1>"Welcome to Tauri + Leptos"</h1>
            <button on:click=greet>"Greet"</button>
            <p>{message}</p>
        </main>
    }
}
```

### Alternative: Using tauri-wasm Crate

```rust
use leptos::*;
use tauri_wasm::api::core::invoke;

#[component]
pub fn App() -> impl IntoView {
    let (message, set_message) = create_signal(String::new());

    let greet = move |_| {
        spawn_local(async move {
            let result: String = invoke("greet", &serde_json::json!({ "name": "World" }))
                .await
                .unwrap();
            set_message.set(result);
        });
    };

    view! {
        <main>
            <button on:click=greet>"Greet"</button>
            <p>{message}</p>
        </main>
    }
}
```

## Tauri Backend Command

In `src-tauri/src/main.rs`:

```rust
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![greet])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Development Commands

```bash
# Install Trunk
cargo install trunk

# Add WASM target
rustup target add wasm32-unknown-unknown

# Development (runs Trunk + Tauri)
cd src-tauri && cargo tauri dev

# Build for production
cd src-tauri && cargo tauri build

# Trunk only (for frontend debugging)
trunk serve --port 1420

# Build WASM only
trunk build --release
```

## Mobile Development

For mobile platforms, additional configuration is needed:

### Trunk.toml for Mobile

```toml
[serve]
port = 1420
open = false
address = "0.0.0.0"  # Listen on all interfaces for mobile

[serve.ws]
ws_protocol = "ws"   # Required for mobile hot-reload
```

### tauri.conf.json for Mobile

```json
{
  "build": {
    "beforeDevCommand": "trunk serve --address 0.0.0.0",
    "devUrl": "http://YOUR_LOCAL_IP:1420"
  }
}
```

Replace `YOUR_LOCAL_IP` with your machine's local IP (e.g., `192.168.1.100`).

## Accessing Tauri APIs from WASM

### Method 1: Direct wasm-bindgen (Recommended for control)

```rust
use wasm_bindgen::prelude::*;
use serde::{Serialize, Deserialize};

#[wasm_bindgen]
extern "C" {
    // Core invoke
    #[wasm_bindgen(js_namespace = ["window", "__TAURI__", "core"], catch)]
    async fn invoke(cmd: &str, args: JsValue) -> Result<JsValue, JsValue>;

    // Event system
    #[wasm_bindgen(js_namespace = ["window", "__TAURI__", "event"])]
    async fn listen(event: &str, handler: &Closure<dyn Fn(JsValue)>) -> JsValue;

    #[wasm_bindgen(js_namespace = ["window", "__TAURI__", "event"])]
    async fn emit(event: &str, payload: JsValue);
}

// Usage
async fn call_backend() -> Result<String, String> {
    let args = serde_wasm_bindgen::to_value(&serde_json::json!({
        "path": "/some/path"
    })).map_err(|e| e.to_string())?;

    let result = invoke("read_file", args)
        .await
        .map_err(|e| format!("{:?}", e))?;

    serde_wasm_bindgen::from_value(result)
        .map_err(|e| e.to_string())
}
```

### Method 2: Using tauri-wasm Crate

```rust
use tauri_wasm::api::{core, event, dialog, fs};

// Invoke command
let result: MyResponse = core::invoke("my_command", &my_args).await?;

// Listen to events
event::listen("my-event", |payload| {
    // Handle event
}).await;

// Emit events
event::emit("my-event", &payload).await;

// File dialogs
let file = dialog::open(dialog::OpenDialogOptions::default()).await?;

// File system (requires permissions)
let contents = fs::read_text_file("path/to/file").await?;
```

## Troubleshooting

### WASM not loading
- Verify `withGlobalTauri: true` in tauri.conf.json
- Check browser console for WASM errors
- Ensure `wasm32-unknown-unknown` target is installed

### Hot-reload not working on mobile
- Set `ws_protocol = "ws"` in Trunk.toml
- Use `address = "0.0.0.0"` for mobile access
- Verify firewall allows connections on dev port

### Tauri APIs undefined
- `withGlobalTauri` must be `true`
- Check `window.__TAURI__` exists in browser console
- Verify tauri-wasm version matches Tauri version

### Large WASM binary size
- Enable release profile optimizations
- Use `opt-level = "z"` for size optimization
- Enable LTO with `lto = true`
- Consider `wasm-opt` post-processing

### Trunk build fails
- Check Cargo.toml has `crate-type = ["cdylib", "rlib"]`
- Verify index.html has correct `data-trunk` directives
- Ensure no server-side features enabled in framework

## Version Compatibility

| Component | Version |
|-----------|---------|
| Tauri | 2.x |
| Trunk | 0.17+ |
| Leptos | 0.6+ |
| wasm-bindgen | 0.2.x |
| tauri-wasm | 2.x |

Always match `tauri-wasm` version with your Tauri version.
