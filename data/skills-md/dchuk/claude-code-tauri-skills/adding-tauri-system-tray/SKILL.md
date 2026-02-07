---
name: adding-tauri-system-tray
description: Guides the user through implementing Tauri system tray functionality, including tray icon setup, tray menu creation, handling tray events, and updating the tray at runtime in the notification area.
---

# Tauri System Tray Implementation

This skill covers implementing system tray (notification area) functionality in Tauri v2 applications.

## Configuration

Enable the tray-icon feature in `src-tauri/Cargo.toml`:

```toml
[dependencies]
tauri = { version = "2", features = ["tray-icon"] }
```

## Basic Tray Setup

Create a tray icon in `src-tauri/src/lib.rs`:

```rust
use tauri::tray::TrayIconBuilder;

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            // Use TrayIconBuilder::with_id() to reference the tray later
            let tray = TrayIconBuilder::with_id(app, "main-tray")
                .icon(app.default_window_icon().unwrap().clone())
                .tooltip("My Tauri App")
                .build(app)?;
            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Tray Menu

### Basic Menu with Items

```rust
use tauri::{
    menu::{Menu, MenuItem},
    tray::TrayIconBuilder,
};

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let show_item = MenuItem::with_id(app, "show", "Show Window", true, None::<&str>)?;
            let hide_item = MenuItem::with_id(app, "hide", "Hide Window", true, None::<&str>)?;
            let quit_item = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>)?;

            let menu = Menu::with_items(app, &[&show_item, &hide_item, &quit_item])?;

            let tray = TrayIconBuilder::new()
                .icon(app.default_window_icon().unwrap().clone())
                .menu(&menu)
                .menu_on_left_click(false)  // Only show menu on right-click
                .build(app)?;

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Menu with Separators and Submenus

```rust
use tauri::{
    menu::{Menu, MenuItem, PredefinedMenuItem, Submenu},
    tray::TrayIconBuilder,
};

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let option1 = MenuItem::with_id(app, "option1", "Option 1", true, None::<&str>)?;
            let option2 = MenuItem::with_id(app, "option2", "Option 2", true, None::<&str>)?;
            let options_submenu = Submenu::with_items(app, "Options", true, &[&option1, &option2])?;

            let show_item = MenuItem::with_id(app, "show", "Show Window", true, None::<&str>)?;
            let separator = PredefinedMenuItem::separator(app)?;
            let quit_item = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>)?;

            let menu = Menu::with_items(
                app,
                &[&show_item, &options_submenu, &separator, &quit_item],
            )?;

            let tray = TrayIconBuilder::new()
                .icon(app.default_window_icon().unwrap().clone())
                .menu(&menu)
                .build(app)?;

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Handling Tray Events

### Menu Item Events

```rust
use tauri::{
    menu::{Menu, MenuItem},
    tray::TrayIconBuilder,
    Manager,
};

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let show_item = MenuItem::with_id(app, "show", "Show Window", true, None::<&str>)?;
            let hide_item = MenuItem::with_id(app, "hide", "Hide Window", true, None::<&str>)?;
            let quit_item = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>)?;
            let menu = Menu::with_items(app, &[&show_item, &hide_item, &quit_item])?;

            let tray = TrayIconBuilder::new()
                .icon(app.default_window_icon().unwrap().clone())
                .menu(&menu)
                .on_menu_event(|app, event| {
                    match event.id.as_ref() {
                        "show" => {
                            if let Some(window) = app.get_webview_window("main") {
                                let _ = window.show();
                                let _ = window.set_focus();
                            }
                        }
                        "hide" => {
                            if let Some(window) = app.get_webview_window("main") {
                                let _ = window.hide();
                            }
                        }
                        "quit" => app.exit(0),
                        _ => println!("Unhandled menu item: {:?}", event.id),
                    }
                })
                .build(app)?;

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Tray Icon Mouse Events

```rust
use tauri::{
    tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent},
    Manager,
};

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .setup(|app| {
            let tray = TrayIconBuilder::new()
                .icon(app.default_window_icon().unwrap().clone())
                .on_tray_icon_event(|tray, event| {
                    match event {
                        TrayIconEvent::Click {
                            button: MouseButton::Left,
                            button_state: MouseButtonState::Up,
                            ..
                        } => {
                            let app = tray.app_handle();
                            if let Some(window) = app.get_webview_window("main") {
                                let _ = window.unminimize();
                                let _ = window.show();
                                let _ = window.set_focus();
                            }
                        }
                        TrayIconEvent::DoubleClick { button: MouseButton::Left, .. } => {
                            let app = tray.app_handle();
                            if let Some(window) = app.get_webview_window("main") {
                                if window.is_visible().unwrap_or(false) {
                                    let _ = window.hide();
                                } else {
                                    let _ = window.show();
                                    let _ = window.set_focus();
                                }
                            }
                        }
                        TrayIconEvent::Enter { .. } => println!("Mouse entered tray"),
                        TrayIconEvent::Leave { .. } => println!("Mouse left tray"),
                        _ => {}
                    }
                })
                .build(app)?;

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

Note: `Enter`, `Move`, and `Leave` events are not supported on Linux.

## Updating Tray at Runtime

### Update Icon and Tooltip

```rust
use tauri::{image::Image, tray::TrayIconBuilder, Manager};

#[tauri::command]
fn update_tray_icon(app: tauri::AppHandle, icon_path: String) -> Result<(), String> {
    if let Some(tray) = app.tray_by_id("main-tray") {
        let icon = Image::from_path(&icon_path).map_err(|e| e.to_string())?;
        tray.set_icon(Some(icon)).map_err(|e| e.to_string())?;
    }
    Ok(())
}

#[tauri::command]
fn update_tray_tooltip(app: tauri::AppHandle, tooltip: String) -> Result<(), String> {
    if let Some(tray) = app.tray_by_id("main-tray") {
        tray.set_tooltip(Some(&tooltip)).map_err(|e| e.to_string())?;
    }
    Ok(())
}
```

### Update Menu Items Dynamically

```rust
use std::sync::Mutex;
use tauri::{
    menu::{Menu, MenuItem, MenuItemKind},
    tray::TrayIconBuilder,
    Manager,
};

struct AppState {
    menu: Mutex<Option<Menu<tauri::Wry>>>,
}

#[tauri::command]
fn toggle_menu_item(app: tauri::AppHandle, item_id: String, enabled: bool) -> Result<(), String> {
    let state = app.state::<AppState>();
    if let Some(menu) = state.menu.lock().unwrap().as_ref() {
        if let Some(MenuItemKind::MenuItem(item)) = menu.get(&item_id) {
            item.set_enabled(enabled).map_err(|e| e.to_string())?;
        }
    }
    Ok(())
}

#[tauri::command]
fn update_menu_text(app: tauri::AppHandle, item_id: String, text: String) -> Result<(), String> {
    let state = app.state::<AppState>();
    if let Some(menu) = state.menu.lock().unwrap().as_ref() {
        if let Some(MenuItemKind::MenuItem(item)) = menu.get(&item_id) {
            item.set_text(&text).map_err(|e| e.to_string())?;
        }
    }
    Ok(())
}
```

### Replace Entire Menu

```rust
use tauri::{menu::{Menu, MenuItem}, Manager};

#[tauri::command]
fn set_connected_menu(app: tauri::AppHandle) -> Result<(), String> {
    if let Some(tray) = app.tray_by_id("main-tray") {
        let disconnect = MenuItem::with_id(&app, "disconnect", "Disconnect", true, None::<&str>)
            .map_err(|e| e.to_string())?;
        let status = MenuItem::with_id(&app, "status", "Connected", false, None::<&str>)
            .map_err(|e| e.to_string())?;
        let quit = MenuItem::with_id(&app, "quit", "Quit", true, None::<&str>)
            .map_err(|e| e.to_string())?;

        let menu = Menu::with_items(&app, &[&status, &disconnect, &quit])
            .map_err(|e| e.to_string())?;
        tray.set_menu(Some(menu)).map_err(|e| e.to_string())?;
    }
    Ok(())
}
```

## Complete Example

```rust
use std::sync::Mutex;
use tauri::{
    menu::{Menu, MenuItem, PredefinedMenuItem},
    tray::{MouseButton, MouseButtonState, TrayIconBuilder, TrayIconEvent},
    Manager,
};

struct TrayState {
    is_paused: Mutex<bool>,
}

#[tauri::command]
fn get_tray_status(state: tauri::State<TrayState>) -> bool {
    *state.is_paused.lock().unwrap()
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .manage(TrayState { is_paused: Mutex::new(false) })
        .setup(|app| {
            let show = MenuItem::with_id(app, "show", "Show Window", true, None::<&str>)?;
            let hide = MenuItem::with_id(app, "hide", "Hide Window", true, None::<&str>)?;
            let sep = PredefinedMenuItem::separator(app)?;
            let pause = MenuItem::with_id(app, "pause", "Pause", true, None::<&str>)?;
            let quit = MenuItem::with_id(app, "quit", "Quit", true, None::<&str>)?;

            let menu = Menu::with_items(app, &[&show, &hide, &sep, &pause, &quit])?;

            let _tray = TrayIconBuilder::with_id(app, "main-tray")
                .icon(app.default_window_icon().unwrap().clone())
                .tooltip("My Tauri App - Running")
                .menu(&menu)
                .menu_on_left_click(false)
                .on_menu_event(|app, event| {
                    match event.id.as_ref() {
                        "show" => {
                            if let Some(w) = app.get_webview_window("main") {
                                let _ = w.show();
                                let _ = w.set_focus();
                            }
                        }
                        "hide" => {
                            if let Some(w) = app.get_webview_window("main") {
                                let _ = w.hide();
                            }
                        }
                        "pause" => {
                            let state = app.state::<TrayState>();
                            let mut paused = state.is_paused.lock().unwrap();
                            *paused = !*paused;
                            if let Some(tray) = app.tray_by_id("main-tray") {
                                let tip = if *paused { "Paused" } else { "Running" };
                                let _ = tray.set_tooltip(Some(tip));
                            }
                        }
                        "quit" => app.exit(0),
                        _ => {}
                    }
                })
                .on_tray_icon_event(|tray, event| {
                    if let TrayIconEvent::Click {
                        button: MouseButton::Left,
                        button_state: MouseButtonState::Up, ..
                    } = event {
                        let app = tray.app_handle();
                        if let Some(w) = app.get_webview_window("main") {
                            if w.is_visible().unwrap_or(false) {
                                let _ = w.hide();
                            } else {
                                let _ = w.show();
                                let _ = w.set_focus();
                            }
                        }
                    }
                })
                .build(app)?;

            Ok(())
        })
        .invoke_handler(tauri::generate_handler![get_tray_status])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

## Platform Notes

| Platform | Support |
|----------|---------|
| Windows | Full support for all tray events |
| macOS | Full support for all tray events |
| Linux | `Enter`, `Move`, `Leave` events not supported |

## Troubleshooting

**Tray icon not appearing:**
- Ensure `tray-icon` feature is enabled in `Cargo.toml`
- Verify the icon is valid and accessible
- Check that `build()` is called and result is stored

**Menu not showing:**
- Confirm menu is attached with `.menu(&menu)`
- Check `menu_on_left_click` setting
- Verify menu items are created correctly

**Events not firing:**
- Ensure event handlers are attached before `build()`
- Check pattern matching in event handlers
- Verify tray ID matches when using `tray_by_id()`
