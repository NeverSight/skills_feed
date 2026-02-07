---
name: migrating-tauri-apps
description: Assists users with migrating Tauri applications from v1 to v2 stable, and from v2 beta to v2 stable, covering breaking changes, configuration updates, API migrations, and plugin system changes.
---

# Tauri Migration Guide

This skill covers migrating Tauri applications to v2 stable from either v1 or v2 beta.

## Migration Paths

| Source Version | Target | Complexity |
|----------------|--------|------------|
| Tauri v1.x | v2 stable | High - significant breaking changes |
| Tauri v2 beta | v2 stable | Low - minor breaking changes |

---

## Automated Migration

Both migration paths support automated migration via the Tauri CLI:

```bash
# Install latest CLI first
npm install @tauri-apps/cli@latest

# Run migration
npm run tauri migrate
# or: yarn tauri migrate | pnpm tauri migrate | cargo tauri migrate
```

**IMPORTANT:** The migrate command automates most tasks but is NOT a complete substitute for manual review. Always verify changes after running.

---

## V1 to V2 Migration

### Configuration File Changes

#### BREAKING: Top-Level Structure Changes

**Before (v1):**
```json
{
  "package": {
    "productName": "my-app",
    "version": "1.0.0"
  },
  "tauri": {
    "bundle": { ... },
    "allowlist": { ... }
  }
}
```

**After (v2):**
```json
{
  "productName": "my-app",
  "version": "1.0.0",
  "mainBinaryName": "my-app",
  "identifier": "com.example.myapp",
  "app": { ... },
  "bundle": { ... }
}
```

#### Key Renames

| v1 Path | v2 Path |
|---------|---------|
| `package.productName` | `productName` (top-level) |
| `package.version` | `version` (top-level) |
| `tauri` | `app` |
| `tauri.bundle` | `bundle` (top-level) |
| `tauri.bundle.identifier` | `identifier` (top-level) |
| `tauri.systemTray` | `app.trayIcon` |
| `build.distDir` | `frontendDist` |
| `build.devPath` | `devUrl` |

#### BREAKING: New Required Field

Add `mainBinaryName` matching your `productName` - this is no longer automatic:

```json
{
  "productName": "My App",
  "mainBinaryName": "My App"
}
```

#### Bundle Configuration Reorganization

Platform-specific bundle configs moved under their platform key:

**Before:**
```json
{
  "tauri": {
    "bundle": {
      "dmg": { ... },
      "deb": { ... }
    }
  }
}
```

**After:**
```json
{
  "bundle": {
    "macOS": {
      "dmg": { ... }
    },
    "linux": {
      "deb": { ... }
    }
  }
}
```

#### Updater Configuration

If using the app updater, add to bundle config:

```json
{
  "bundle": {
    "createUpdaterArtifacts": "v1Compatible"
  }
}
```

Use `"v1Compatible"` for existing distributions to maintain backward compatibility.

---

### BREAKING: Allowlist Replaced with Capabilities

The v1 allowlist system is completely replaced with a capability-based ACL system.

#### Creating Capabilities

Create JSON files in `src-tauri/capabilities/`:

**src-tauri/capabilities/default.json:**
```json
{
  "identifier": "default",
  "description": "Default capabilities for the main window",
  "windows": ["main"],
  "permissions": [
    "core:default",
    "shell:allow-open",
    "dialog:allow-open",
    "fs:allow-read-text-file"
  ]
}
```

The `tauri migrate` command auto-generates capabilities from your v1 allowlist.

---

### Cargo.toml Changes

#### Removed Features

These features no longer exist in v2:
- `reqwest-client`
- `reqwest-native-tls-vendored`
- `process-command-api`
- `shell-open-api`
- `windows7-compat`
- `updater`
- `system-tray`

#### New Features

- `linux-protocol-body` - Custom protocol request body parsing support

### BREAKING: API Module Removal

The entire `api` module is removed. Functionality moved to plugins:

| v1 API | v2 Replacement |
|--------|----------------|
| `tauri::api::dialog` | `tauri-plugin-dialog` |
| `tauri::api::http` | `tauri-plugin-http` |
| `tauri::api::process` | `tauri-plugin-process` |
| `tauri::api::path` functions | `tauri::Manager::path` |

### BREAKING: Rust API Changes

#### Removed APIs

| v1 | v2 Alternative |
|----|----------------|
| `App::clipboard_manager` | `tauri-plugin-clipboard-manager` |
| `App::global_shortcut_manager` | `tauri-plugin-global-shortcut` |
| `App::get_cli_matches` | `tauri-plugin-cli` |
| `tauri::updater` | `tauri-plugin-updater` |

#### Renamed Types/Methods

| v1 | v2 |
|----|-----|
| `Window` | `WebviewWindow` |
| `Manager::get_window` | `Manager::get_webview_window` |

#### Menu API Changes

**Before:**
```rust
use tauri::{Menu, CustomMenuItem};
let menu = Menu::new()
    .add_item(CustomMenuItem::new("quit", "Quit"));
```

**After:**
```rust
use tauri::menu::{MenuBuilder, MenuItemBuilder};
let menu = MenuBuilder::new(app)
    .item(&MenuItemBuilder::with_id("quit", "Quit").build(app)?)
    .build()?;
```

#### Tray API Changes

**Before:**
```rust
use tauri::SystemTray;
SystemTray::new().with_menu(menu);
```

**After:**
```rust
use tauri::tray::TrayIconBuilder;
TrayIconBuilder::new()
    .menu(&menu)
    .on_menu_event(|app, event| { ... })
    .on_tray_icon_event(|tray, event| { ... })
    .build(app)?;
```

---

### BREAKING: JavaScript API Changes

#### Package Renames

| v1 | v2 |
|----|-----|
| `@tauri-apps/api/tauri` | `@tauri-apps/api/core` |
| `@tauri-apps/api/window` | `@tauri-apps/api/webviewWindow` |

#### Core API Reduction

The core `@tauri-apps/api` package now only includes:
- `core`
- `path`
- `event`
- `webviewWindow`

All other APIs require plugin packages.

---

### BREAKING: Plugin Migration

All formerly built-in APIs are now separate plugins:

| v1 Import | v2 Plugin Package |
|-----------|-------------------|
| `@tauri-apps/api/cli` | `@tauri-apps/plugin-cli` |
| `@tauri-apps/api/clipboard` | `@tauri-apps/plugin-clipboard-manager` |
| `@tauri-apps/api/dialog` | `@tauri-apps/plugin-dialog` |
| `@tauri-apps/api/fs` | `@tauri-apps/plugin-fs` |
| `@tauri-apps/api/global-shortcut` | `@tauri-apps/plugin-global-shortcut` |
| `@tauri-apps/api/http` | `@tauri-apps/plugin-http` |
| `@tauri-apps/api/notification` | `@tauri-apps/plugin-notification` |
| `@tauri-apps/api/os` | `@tauri-apps/plugin-os` |
| `@tauri-apps/api/process` | `@tauri-apps/plugin-process` |
| `@tauri-apps/api/shell` | `@tauri-apps/plugin-shell` |
| `@tauri-apps/api/updater` | `@tauri-apps/plugin-updater` |

#### Installing Plugins

```bash
# JavaScript
npm install @tauri-apps/plugin-fs

# Rust (add to Cargo.toml)
cargo add tauri-plugin-fs
```

Register plugins in your Rust code:

```rust
fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_fs::init())
        .run(tauri::generate_context!())
        .expect("error running app");
}
```

### BREAKING: File System Plugin Changes

Function renames in `@tauri-apps/plugin-fs`:

| v1 | v2 |
|----|-----|
| `createDir` | `mkdir` |
| `readBinaryFile` | `readFile` |
| `writeBinaryFile` | `writeFile` |
| `removeDir` | `remove` |
| `removeFile` | `remove` |
| `renameFile` | `rename` |
| `Dir` enum | `BaseDirectory` |

### BREAKING: Event System Changes

| v1 | v2 |
|----|-----|
| `emit()` | Broadcasts to ALL listeners (behavior change) |
| N/A | `emit_to()` - target specific event targets |
| `listen_global` | `listen_any` |

### BREAKING: Windows Origin URL

Production Windows apps now serve from `http://tauri.localhost` instead of `https://`.

**Impact:** IndexedDB and cookies will reset unless you preserve the old behavior:

```json
{
  "app": {
    "windows": [{
      "useHttpsScheme": true
    }]
  }
}
```

### BREAKING: Environment Variables

| v1 | v2 |
|----|-----|
| `TAURI_PRIVATE_KEY` | `TAURI_SIGNING_PRIVATE_KEY` |
| `TAURI_KEY_PASSWORD` | `TAURI_SIGNING_PRIVATE_KEY_PASSWORD` |
| `TAURI_DEV_SERVER_PORT` | `TAURI_CLI_PORT` |
| Platform variables | Now prefixed `TAURI_ENV_` |

### Mobile Support Setup

To target mobile alongside desktop:

**1. Update Cargo.toml:**
```toml
[lib]
name = "app_lib"
crate-type = ["staticlib", "cdylib", "rlib"]
```

**2. Rename src/main.rs to src/lib.rs:**
```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .run(tauri::generate_context!())
        .expect("error running app");
}
```

**3. Create new src/main.rs:**
```rust
fn main() {
    app_lib::run();
}
```

---

## V2 Beta to V2 Stable Migration

### BREAKING: Core Permission Prefix

All core permissions now require the `"core:"` prefix:

**Before (beta):**
```json
{
  "permissions": [
    "path:default",
    "event:default",
    "window:default"
  ]
}
```

**After (stable):**
```json
{
  "permissions": [
    "core:path:default",
    "core:event:default",
    "core:window:default"
  ]
}
```

**Simplified alternative:** Use `"core:default"` to include all default core permissions:

```json
{
  "permissions": ["core:default"]
}
```

---

### BREAKING: Mobile Dev Server Configuration

The mobile development server no longer exposes across networks. Traffic tunnels directly from local machine to devices.

**Before (beta):**
```javascript
const mobile = !!/android|ios/.exec(process.env.TAURI_ENV_PLATFORM);
export default {
  server: {
    host: mobile ? '0.0.0.0' : false
  }
};
```

**After (stable):**
```javascript
const host = process.env.TAURI_DEV_HOST;
export default {
  server: {
    host: host || false
  }
};
```

Remove dependency on the `internal-ip` NPM package if previously used.

**iOS Device Development:** Requires additional steps. Use:
```bash
tauri ios dev --force-ip-prompt
```
Select the device's TUN address when prompted.

---

## Migration Checklist

### V1 to V2

- [ ] Run `npm run tauri migrate`
- [ ] Verify config structure changes (package -> top-level)
- [ ] Add `mainBinaryName` field
- [ ] Update bundle config structure
- [ ] Replace allowlist with capabilities
- [ ] Install required plugins
- [ ] Update Rust imports (Window -> WebviewWindow)
- [ ] Update JS imports (@tauri-apps/api/tauri -> core)
- [ ] Update FS function names if using fs plugin
- [ ] Update environment variable names
- [ ] Test event system behavior
- [ ] Verify Windows origin URL handling (IndexedDB/cookies)
- [ ] Update menu/tray code if used
- [ ] Remove deprecated Cargo features

### V2 Beta to V2 Stable

- [ ] Run `npm run tauri migrate`
- [ ] Add `core:` prefix to permission identifiers (or use `core:default`)
- [ ] Update mobile dev server configuration
- [ ] Remove `internal-ip` package dependency if present
- [ ] Test iOS device development with `--force-ip-prompt`

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Permission denied errors | Check `src-tauri/capabilities/` files for required permissions |
| IndexedDB/localStorage lost (Windows) | Set `useHttpsScheme: true` in window config |
| Plugin not found | Add to Cargo.toml, register with `.plugin()`, install npm package |
| Mobile build fails | Verify `[lib]` section in Cargo.toml and `src/lib.rs` with mobile entry point |
