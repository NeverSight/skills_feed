---
name: calling-frontend-from-tauri-rust
description: Guides developers through Tauri v2 event system for calling frontend from Rust, covering emit functions, event payloads, IPC channels, and JavaScript evaluation for bi-directional Rust-frontend communication.
---

# Calling Frontend from Tauri Rust

Tauri provides three mechanisms for Rust to communicate with the frontend: the event system, channels, and JavaScript evaluation.

## Event System Overview

The event system enables bi-directional communication between Rust and frontend. Best for small data transfers and multi-consumer patterns. Not designed for low latency or high throughput.

### Required Imports

```rust
use tauri::{AppHandle, Emitter, Manager, Listener, EventTarget};
use serde::Serialize;
```

```typescript
import { listen, once, emit } from '@tauri-apps/api/event';
import { getCurrentWebviewWindow } from '@tauri-apps/api/webviewWindow';
```

## Emitting Events from Rust

### Global Events (All Listeners)

Use `AppHandle::emit()` to broadcast to all listeners:

```rust
use tauri::{AppHandle, Emitter};

#[tauri::command]
fn download(app: AppHandle, url: String) {
    app.emit("download-started", &url).unwrap();
    for progress in [1, 15, 50, 80, 100] {
        app.emit("download-progress", progress).unwrap();
    }
    app.emit("download-finished", &url).unwrap();
}
```

### Webview-Specific Events

Target specific webviews with `emit_to()`:

```rust
use tauri::{AppHandle, Emitter};

#[tauri::command]
fn login(app: AppHandle, user: String, password: String) {
    let authenticated = user == "tauri-apps" && password == "tauri";
    let result = if authenticated { "loggedIn" } else { "invalidCredentials" };
    app.emit_to("login", "login-result", result).unwrap();
}
```

### Filtered Events (Multiple Webviews)

Use `emit_filter()` for conditional targeting:

```rust
use tauri::{AppHandle, Emitter, EventTarget};

#[tauri::command]
fn open_file(app: AppHandle, path: std::path::PathBuf) {
    app.emit_filter("open-file", path, |target| match target {
        EventTarget::WebviewWindow { label } => label == "main" || label == "file-viewer",
        _ => false,
    }).unwrap();
}
```

## Event Payloads

Custom payloads must implement `Serialize` and `Clone`:

```rust
use serde::Serialize;
use tauri::{AppHandle, Emitter};

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
struct DownloadProgress {
    download_id: usize,
    chunk_length: usize,
    total_size: usize,
}

#[tauri::command]
fn download(app: AppHandle, url: String) {
    app.emit("download-progress", DownloadProgress {
        download_id: 1,
        chunk_length: 150,
        total_size: 1000,
    }).unwrap();
}
```

## Listening in Frontend

### Global Event Listeners

```typescript
import { listen } from '@tauri-apps/api/event';

type DownloadStarted = {
    url: string;
    downloadId: number;
    contentLength: number;
};

listen<DownloadStarted>('download-started', (event) => {
    console.log(`downloading ${event.payload.contentLength} bytes from ${event.payload.url}`);
});
```

### Webview-Specific Listeners

```typescript
import { getCurrentWebviewWindow } from '@tauri-apps/api/webviewWindow';

const appWebview = getCurrentWebviewWindow();
appWebview.listen<string>('logged-in', (event) => {
    localStorage.setItem('session-token', event.payload);
});
```

### Managing Listeners

```typescript
import { listen, once } from '@tauri-apps/api/event';

// Unlisten to prevent memory leaks
const unlisten = await listen('download-started', (event) => {
    console.log('download started');
});
unlisten(); // Stop listening when done

// Listen once for one-time events
once('app-ready', (event) => {
    console.log('App is ready:', event.payload);
});
```

## Listening in Rust

### Global and Webview Listeners

```rust
use tauri::{Listener, Manager};

tauri::Builder::default()
    .setup(|app| {
        // Global listener
        app.listen("download-started", |event| {
            println!("event received: {}", event.payload());
        });

        // Webview-specific listener
        let webview = app.get_webview_window("main").unwrap();
        webview.listen("logged-in", |event| {
            println!("User logged in: {}", event.payload());
        });
        Ok(())
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application")
```

### Unlisten and Listen Once

```rust
use tauri::Listener;

// Store event ID to unlisten later
let event_id = app.listen("download-started", |event| {
    println!("download started");
});
app.unlisten(event_id);

// Conditional unlisten
let handle = app.handle().clone();
app.listen("status-changed", move |event| {
    if event.payload() == "\"ready\"" {
        handle.unlisten(event.id());
    }
});

// Listen once
app.once("ready", |event| {
    println!("app is ready: {}", event.payload());
});
```

## Channels (High-Throughput Streaming)

For better performance than events, use channels:

### Rust Channel Setup

```rust
use tauri::{AppHandle, ipc::Channel};
use serde::Serialize;

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase", tag = "event", content = "data")]
enum DownloadEvent<'a> {
    #[serde(rename_all = "camelCase")]
    Started { url: &'a str, download_id: usize, content_length: usize },
    #[serde(rename_all = "camelCase")]
    Progress { download_id: usize, chunk_length: usize },
    #[serde(rename_all = "camelCase")]
    Finished { download_id: usize },
}

#[tauri::command]
fn download(app: AppHandle, url: String, on_event: Channel<DownloadEvent>) {
    on_event.send(DownloadEvent::Started {
        url: &url,
        download_id: 1,
        content_length: 1000,
    }).unwrap();

    for _ in 0..10 {
        on_event.send(DownloadEvent::Progress {
            download_id: 1,
            chunk_length: 100,
        }).unwrap();
    }

    on_event.send(DownloadEvent::Finished { download_id: 1 }).unwrap();
}
```

### Frontend Channel Usage

```typescript
import { invoke, Channel } from '@tauri-apps/api/core';

type DownloadEvent =
    | { event: 'started'; data: { url: string; downloadId: number; contentLength: number } }
    | { event: 'progress'; data: { downloadId: number; chunkLength: number } }
    | { event: 'finished'; data: { downloadId: number } };

const onEvent = new Channel<DownloadEvent>();

onEvent.onmessage = (message) => {
    switch (message.event) {
        case 'started':
            console.log(`Download started: ${message.data.url}`);
            break;
        case 'progress':
            console.log(`Progress: ${message.data.chunkLength} bytes`);
            break;
        case 'finished':
            console.log('Download complete!');
            break;
    }
};

await invoke('download', { url: 'https://example.com/file.json', onEvent });
```

## JavaScript Evaluation

Execute JavaScript directly from Rust:

### Basic Evaluation

```rust
use tauri::Manager;

tauri::Builder::default()
    .setup(|app| {
        let webview = app.get_webview_window("main").unwrap();
        webview.eval("console.log('hello from Rust')")?;
        Ok(())
    })
```

### Evaluation with Data

```rust
use tauri::Manager;

#[tauri::command]
fn notify_frontend(app: tauri::AppHandle, message: String) {
    if let Some(webview) = app.get_webview_window("main") {
        let script = format!("window.showNotification('{}')", message);
        webview.eval(&script).unwrap();
    }
}
```

### Complex Data with serialize-to-javascript

```toml
# Cargo.toml
[dependencies]
serialize-to-javascript = "0.1"
```

```rust
use serialize_to_javascript::Serialized;
use tauri::Manager;

#[derive(serde::Serialize)]
struct AppState { user: String, logged_in: bool }

#[tauri::command]
fn sync_state(app: tauri::AppHandle) {
    let state = AppState { user: "john".to_string(), logged_in: true };
    if let Some(webview) = app.get_webview_window("main") {
        let serialized = Serialized::new(&state, &Default::default()).into_string();
        webview.eval(&format!("window.updateState({})", serialized)).unwrap();
    }
}
```

## Choosing the Right Method

| Method | Use Case | Performance |
|--------|----------|-------------|
| Events (`emit`) | Multi-consumer, broadcast | Moderate |
| Channels | High-throughput streaming, single consumer | High |
| JS Eval | Direct DOM manipulation, no response needed | Low overhead |

**Events**: Notifying multiple windows, loose coupling, simple status updates.

**Channels**: File downloads/uploads with progress, real-time streaming, high-frequency updates.

**JS Eval**: One-off DOM updates, triggering frontend functions directly.

## Complete Example: File Watcher

### Rust Side

```rust
use tauri::{AppHandle, Emitter};
use serde::Serialize;
use std::path::PathBuf;

#[derive(Clone, Serialize)]
#[serde(rename_all = "camelCase")]
struct FileChange { path: String, event_type: String }

#[tauri::command]
fn watch_directory(app: AppHandle, path: PathBuf) {
    std::thread::spawn(move || {
        loop {
            app.emit("file-changed", FileChange {
                path: path.to_string_lossy().to_string(),
                event_type: "modified".to_string(),
            }).unwrap();
            std::thread::sleep(std::time::Duration::from_secs(5));
        }
    });
}
```

### Frontend Side

```typescript
import { listen } from '@tauri-apps/api/event';
import { invoke } from '@tauri-apps/api/core';

type FileChange = { path: string; eventType: string };

await invoke('watch_directory', { path: '/some/directory' });

const unlisten = await listen<FileChange>('file-changed', (event) => {
    console.log(`File ${event.payload.eventType}: ${event.payload.path}`);
});

// Cleanup when component unmounts: unlisten();
```
