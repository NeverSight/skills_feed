---
name: adding-tauri-splashscreen
description: Guides the user through adding a Tauri splashscreen, splash screen, loading screen, or startup screen to their application. Covers configuration, custom splash HTML, closing the splash when ready, and styling.
---

# Tauri Splashscreen Implementation

This skill covers implementing splash screens in Tauri v2 applications. A splash screen displays during application startup while the main window loads and initializes.

## Overview

The splash screen pattern involves:
1. Showing a splash window immediately on launch
2. Hiding the main window until ready
3. Performing initialization tasks (frontend and backend)
4. Closing splash and showing main window when complete

## Configuration

### Window Configuration

Configure both windows in `tauri.conf.json`:

```json
{
  "app": {
    "windows": [
      {
        "label": "main",
        "title": "My Application",
        "width": 1200,
        "height": 800,
        "visible": false
      },
      {
        "label": "splashscreen",
        "title": "Loading",
        "url": "splashscreen.html",
        "width": 400,
        "height": 300,
        "center": true,
        "resizable": false,
        "decorations": false,
        "transparent": true,
        "alwaysOnTop": true
      }
    ]
  }
}
```

Key settings:
- `"visible": false` on main window - hides it until ready
- `"url": "splashscreen.html"` - points to splash screen HTML
- `"decorations": false` - removes window chrome for cleaner look
- `"transparent": true` - enables transparent backgrounds
- `"alwaysOnTop": true` - keeps splash visible during loading

## Splash Screen HTML

Create `splashscreen.html` in your frontend source directory (e.g., `src/` or `public/`):

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Loading</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }

    html, body {
      height: 100%;
      overflow: hidden;
      background: transparent;
    }

    .splash-container {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100vh;
      background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
      border-radius: 12px;
      color: white;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }

    .logo {
      width: 80px;
      height: 80px;
      margin-bottom: 24px;
    }

    .app-name {
      font-size: 24px;
      font-weight: 600;
      margin-bottom: 16px;
    }

    .loading-spinner {
      width: 40px;
      height: 40px;
      border: 3px solid rgba(255, 255, 255, 0.3);
      border-top-color: #4f46e5;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    @keyframes spin {
      to { transform: rotate(360deg); }
    }

    .loading-text {
      margin-top: 16px;
      font-size: 14px;
      color: rgba(255, 255, 255, 0.7);
    }
  </style>
</head>
<body>
  <div class="splash-container">
    <!-- Replace with your logo -->
    <svg class="logo" viewBox="0 0 100 100" fill="none">
      <circle cx="50" cy="50" r="45" stroke="#4f46e5" stroke-width="4"/>
      <path d="M30 50 L45 65 L70 35" stroke="#4f46e5" stroke-width="4" fill="none"/>
    </svg>
    <div class="app-name">My Application</div>
    <div class="loading-spinner"></div>
    <div class="loading-text">Loading...</div>
  </div>
</body>
</html>
```

## Frontend Setup

### TypeScript/JavaScript Implementation

In your main entry file (e.g., `src/main.ts`):

```typescript
import { invoke } from '@tauri-apps/api/core';

// Helper function for delays
function sleep(seconds: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, seconds * 1000));
}

// Frontend initialization
async function initializeFrontend(): Promise<void> {
  // Perform frontend setup tasks here:
  // - Load configuration
  // - Initialize state management
  // - Set up routing
  // - Preload critical assets

  // Example: simulate initialization time
  await sleep(1);

  // Notify backend that frontend is ready
  await invoke('set_complete', { task: 'frontend' });
}

// Start initialization when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  initializeFrontend().catch(console.error);
});
```

### Alternative: Using Window Events

```typescript
import { invoke } from '@tauri-apps/api/core';
import { getCurrentWindow } from '@tauri-apps/api/window';

async function initializeFrontend(): Promise<void> {
  // Your initialization logic
  const config = await loadConfig();
  await setupRouter();
  await preloadAssets();

  // Signal completion
  await invoke('set_complete', { task: 'frontend' });
}

// Wait for window to be fully ready
getCurrentWindow().once('tauri://created', () => {
  initializeFrontend();
});
```

## Backend Setup

### Add Tokio Dependency

```bash
cargo add tokio --features time
```

### Rust Implementation

In `src-tauri/src/lib.rs`:

```rust
use std::sync::Mutex;
use tauri::{AppHandle, Manager, State};

// Track initialization state
struct SetupState {
    frontend_task: bool,
    backend_task: bool,
}

impl Default for SetupState {
    fn default() -> Self {
        Self {
            frontend_task: false,
            backend_task: false,
        }
    }
}

// Command to mark tasks complete
#[tauri::command]
async fn set_complete(
    app: AppHandle,
    state: State<'_, Mutex<SetupState>>,
    task: String,
) -> Result<(), String> {
    let mut state = state.lock().map_err(|e| e.to_string())?;

    match task.as_str() {
        "frontend" => state.frontend_task = true,
        "backend" => state.backend_task = true,
        _ => return Err(format!("Unknown task: {}", task)),
    }

    // Check if all tasks are complete
    if state.frontend_task && state.backend_task {
        // Close splash and show main window
        if let Some(splash) = app.get_webview_window("splashscreen") {
            splash.close().map_err(|e| e.to_string())?;
        }

        if let Some(main) = app.get_webview_window("main") {
            main.show().map_err(|e| e.to_string())?;
            main.set_focus().map_err(|e| e.to_string())?;
        }
    }

    Ok(())
}

// Backend initialization
async fn setup_backend(app: AppHandle) {
    // IMPORTANT: Use tokio::time::sleep, NOT std::thread::sleep
    // std::thread::sleep blocks the entire async runtime

    // Perform backend initialization:
    // - Database connections
    // - Load configuration
    // - Initialize services

    // Example: simulate work
    tokio::time::sleep(tokio::time::Duration::from_secs(2)).await;

    // Mark backend as complete
    if let Some(state) = app.try_state::<Mutex<SetupState>>() {
        let _ = set_complete(
            app.clone(),
            state,
            "backend".to_string(),
        ).await;
    }
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .manage(Mutex::new(SetupState::default()))
        .invoke_handler(tauri::generate_handler![set_complete])
        .setup(|app| {
            let handle = app.handle().clone();

            // Spawn backend initialization
            tauri::async_runtime::spawn(async move {
                setup_backend(handle).await;
            });

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Simple Implementation

For simpler cases where you only need to wait for the frontend:

### Configuration

```json
{
  "app": {
    "windows": [
      {
        "label": "main",
        "visible": false
      },
      {
        "label": "splashscreen",
        "url": "splashscreen.html",
        "width": 400,
        "height": 300,
        "decorations": false
      }
    ]
  }
}
```

### Frontend

```typescript
import { invoke } from '@tauri-apps/api/core';

async function init() {
  // Initialize your app
  await setupApp();

  // Close splash, show main
  await invoke('close_splashscreen');
}

document.addEventListener('DOMContentLoaded', init);
```

### Backend

```rust
use tauri::{AppHandle, Manager};

#[tauri::command]
async fn close_splashscreen(app: AppHandle) -> Result<(), String> {
    if let Some(splash) = app.get_webview_window("splashscreen") {
        splash.close().map_err(|e| e.to_string())?;
    }

    if let Some(main) = app.get_webview_window("main") {
        main.show().map_err(|e| e.to_string())?;
        main.set_focus().map_err(|e| e.to_string())?;
    }

    Ok(())
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![close_splashscreen])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Styling Variations

### Minimal Splash

```html
<style>
  .splash-container {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
    background: #ffffff;
  }

  .logo {
    width: 120px;
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(0.95); }
  }
</style>
```

### Progress Bar Splash

```html
<style>
  .progress-container {
    width: 200px;
    height: 4px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 2px;
    overflow: hidden;
    margin-top: 20px;
  }

  .progress-bar {
    height: 100%;
    background: #4f46e5;
    animation: progress 2s ease-in-out infinite;
  }

  @keyframes progress {
    0% { width: 0%; }
    50% { width: 70%; }
    100% { width: 100%; }
  }
</style>

<div class="progress-container">
  <div class="progress-bar"></div>
</div>
```

### Dark Theme with Glow

```html
<style>
  .splash-container {
    background: #0a0a0a;
    color: #ffffff;
  }

  .logo {
    filter: drop-shadow(0 0 20px rgba(79, 70, 229, 0.5));
  }

  .app-name {
    text-shadow: 0 0 20px rgba(79, 70, 229, 0.5);
  }
</style>
```

## Important Notes

1. **Async Sleep**: Always use `tokio::time::sleep` in async Rust code, never `std::thread::sleep`. The latter blocks the entire runtime.

2. **Window Labels**: Ensure window labels in code match those in `tauri.conf.json`.

3. **Error Handling**: The splash screen should handle errors gracefully. If initialization fails, show the main window anyway with an error state.

4. **Timing**: Keep splash screen visible long enough for branding but not so long it frustrates users. Aim for 1-3 seconds minimum.

5. **Transparent Windows**: When using `transparent: true`, ensure your HTML has `background: transparent` on `html` and `body` elements.

6. **Mobile Considerations**: On mobile platforms, splash screens work differently. Consider using platform-native splash screens for iOS and Android.

## Troubleshooting

**Splash screen doesn't appear:**
- Verify the URL path is correct in `tauri.conf.json`
- Check that the HTML file exists in the correct location

**Main window shows too early:**
- Ensure `visible: false` is set on the main window
- Verify the `set_complete` command is being called correctly

**Transparent background not working:**
- Set `transparent: true` in window config
- Set `background: transparent` in CSS for html and body
- On some platforms, you may need `decorations: false`

**Window position issues:**
- Use `center: true` for centered splash screens
- Or specify explicit `x` and `y` coordinates
