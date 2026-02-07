---
name: configuring-tauri-apps
description: Guides developers through Tauri v2 configuration including tauri.conf.json structure, Cargo.toml settings, environment-specific configs, and common configuration options for desktop and mobile applications.
---

# Tauri Configuration Files

Tauri v2 applications use three primary configuration files to manage application behavior, dependencies, and build processes.

## Configuration File Overview

| File | Purpose | Format |
|------|---------|--------|
| `tauri.conf.json` | Tauri-specific settings | JSON, JSON5, or TOML |
| `Cargo.toml` | Rust dependencies and metadata | TOML |
| `package.json` | Frontend dependencies and scripts | JSON |

## tauri.conf.json

The main configuration file located in `src-tauri/`. Defines application metadata, window behavior, bundling options, and plugin settings.

### Supported Formats

- **JSON** (default): `tauri.conf.json`
- **JSON5**: `tauri.conf.json5` (requires `config-json5` Cargo feature)
- **TOML**: `Tauri.toml` (requires `config-toml` Cargo feature)

### Complete Configuration Structure

```json
{
  "$schema": "https://schema.tauri.app/config/2",
  "productName": "MyApp",
  "version": "1.0.0",
  "identifier": "com.company.myapp",
  "mainBinaryName": "my-app",
  "build": {
    "devUrl": "http://localhost:3000",
    "frontendDist": "../dist",
    "beforeDevCommand": "npm run dev",
    "beforeBuildCommand": "npm run build",
    "features": ["custom-feature"],
    "removeUnusedCommands": true
  },
  "app": {
    "withGlobalTauri": false,
    "macOSPrivateApi": false,
    "windows": [
      {
        "title": "My Application",
        "width": 1200,
        "height": 800,
        "minWidth": 800,
        "minHeight": 600,
        "resizable": true,
        "fullscreen": false,
        "center": true,
        "visible": true,
        "decorations": true,
        "transparent": false,
        "alwaysOnTop": false,
        "focus": true,
        "url": "index.html"
      }
    ],
    "security": {
      "capabilities": [],
      "assetProtocol": {
        "enable": true,
        "scope": ["$APPDATA/**"]
      },
      "pattern": { "use": "brownfield" },
      "freezePrototype": false
    },
    "trayIcon": {
      "id": "main-tray",
      "iconPath": "icons/tray.png",
      "iconAsTemplate": true
    }
  },
  "bundle": {
    "active": true,
    "targets": "all",
    "icon": ["icons/32x32.png", "icons/128x128.png", "icons/icon.icns", "icons/icon.ico"],
    "resources": ["assets/**/*"],
    "copyright": "Copyright 2024",
    "category": "Utility",
    "shortDescription": "A short app description",
    "longDescription": "A longer description",
    "licenseFile": "../LICENSE",
    "windows": {
      "certificateThumbprint": null,
      "timestampUrl": "http://timestamp.digicert.com",
      "nsis": { "license": "../LICENSE", "installerIcon": "icons/icon.ico", "installMode": "currentUser" }
    },
    "macOS": {
      "minimumSystemVersion": "10.13",
      "signingIdentity": null,
      "dmg": { "appPosition": { "x": 180, "y": 170 }, "applicationFolderPosition": { "x": 480, "y": 170 } }
    },
    "linux": {
      "appimage": { "bundleMediaFramework": false },
      "deb": { "depends": ["libwebkit2gtk-4.1-0"] },
      "rpm": { "depends": ["webkit2gtk4.1"] }
    },
    "android": { "minSdkVersion": 24 },
    "iOS": { "minimumSystemVersion": "13.0" }
  },
  "plugins": {
    "updater": {
      "pubkey": "YOUR_PUBLIC_KEY",
      "endpoints": ["https://releases.example.com/{{target}}/{{arch}}/{{current_version}}"]
    }
  }
}
```

### Root-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `productName` | string | No | Application display name |
| `version` | string | No | Semver version or path to package.json |
| `identifier` | string | Yes | Reverse domain identifier (e.g., `com.tauri.example`) |
| `mainBinaryName` | string | No | Override the main binary filename |

### Build Configuration Fields

| Field | Type | Description |
|-------|------|-------------|
| `devUrl` | string | Development server URL for hot-reload |
| `frontendDist` | string | Path to built frontend assets or remote URL |
| `beforeDevCommand` | string | Script to run before `tauri dev` |
| `beforeBuildCommand` | string | Script to run before `tauri build` |
| `features` | string[] | Cargo features to enable during build |
| `removeUnusedCommands` | boolean | Strip unused plugin commands from binary |

### Window Configuration Options

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `title` | string | `"Tauri"` | Window title |
| `width` / `height` | number | `800` / `600` | Window dimensions in pixels |
| `minWidth` / `minHeight` | number | - | Minimum dimensions |
| `maxWidth` / `maxHeight` | number | - | Maximum dimensions |
| `x` / `y` | number | - | Window position |
| `resizable` | boolean | `true` | Allow window resizing |
| `fullscreen` | boolean | `false` | Start in fullscreen |
| `center` | boolean | `false` | Center window on screen |
| `visible` | boolean | `true` | Window visibility on start |
| `decorations` | boolean | `true` | Show window decorations |
| `transparent` | boolean | `false` | Enable window transparency |
| `alwaysOnTop` | boolean | `false` | Keep window above others |
| `url` | string | `"index.html"` | Initial URL to load |

### Security Configuration

| Field | Type | Description |
|-------|------|-------------|
| `capabilities` | string[] | Permission capabilities for the application |
| `assetProtocol.enable` | boolean | Enable custom asset protocol |
| `assetProtocol.scope` | string[] | Allowed paths for asset protocol |
| `pattern.use` | string | Security pattern (`"brownfield"` default) |
| `freezePrototype` | boolean | Prevent prototype mutation |

### Bundle Targets by Platform

| Platform | Targets |
|----------|---------|
| Windows | `nsis`, `msi` |
| macOS | `app`, `dmg` |
| Linux | `appimage`, `deb`, `rpm` |
| Android | `apk`, `aab` |
| iOS | `app` |

## Platform-Specific Configuration

Create platform-specific files that override base configuration using JSON Merge Patch (RFC 7396).

| Platform | Filename |
|----------|----------|
| Linux | `tauri.linux.conf.json` |
| Windows | `tauri.windows.conf.json` |
| macOS | `tauri.macos.conf.json` |
| Android | `tauri.android.conf.json` |
| iOS | `tauri.ios.conf.json` |

Example `src-tauri/tauri.windows.conf.json`:

```json
{
  "app": {
    "windows": [{ "title": "My App - Windows Edition" }]
  },
  "bundle": {
    "windows": { "nsis": { "installMode": "perMachine" } }
  }
}
```

Example `src-tauri/tauri.macos.conf.json`:

```json
{
  "app": { "macOSPrivateApi": true },
  "bundle": {
    "macOS": { "minimumSystemVersion": "11.0", "entitlements": "entitlements.plist" }
  }
}
```

## CLI Configuration Override

```bash
# Development with custom config
tauri dev --config src-tauri/tauri.dev.conf.json

# Build with beta configuration
tauri build --config src-tauri/tauri.beta.conf.json

# Inline configuration override
tauri build --config '{"bundle":{"identifier":"com.company.myapp.beta"}}'
```

## Cargo.toml Configuration

Located in `src-tauri/Cargo.toml`, manages Rust dependencies.

```toml
[package]
name = "my-app"
version = "1.0.0"
edition = "2021"

[build-dependencies]
tauri-build = { version = "2.0", features = [] }

[dependencies]
serde = { version = "1.0", features = ["derive"] }
serde_json = "1.0"
tauri = { version = "2.0", features = [] }
tauri-plugin-shell = "2.0"
tauri-plugin-opener = "2.0"

[features]
default = ["custom-protocol"]
custom-protocol = ["tauri/custom-protocol"]
```

### Common Tauri Features

```toml
[dependencies]
tauri = { version = "2.0", features = [
  "config-json5",      # Enable JSON5 config format
  "config-toml",       # Enable TOML config format
  "devtools",          # Enable WebView devtools
  "macos-private-api", # Enable macOS private APIs
  "tray-icon",         # Enable system tray support
  "image-png",         # PNG image support
  "image-ico",         # ICO image support
  "protocol-asset"     # Custom asset protocol
] }
```

### Version Management

```toml
tauri = { version = "2.0" }       # Semver-compatible (recommended)
tauri = { version = "=2.0.0" }    # Exact version
tauri = { version = "~2.0.0" }    # Patch updates only
```

## package.json Integration

```json
{
  "name": "my-tauri-app",
  "version": "1.0.0",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "tauri": "tauri"
  },
  "dependencies": { "@tauri-apps/api": "^2.0.0" },
  "devDependencies": { "@tauri-apps/cli": "^2.0.0" }
}
```

## Environment-Specific Configurations

### Development (`src-tauri/tauri.dev.conf.json`)

```json
{
  "build": { "devUrl": "http://localhost:5173" },
  "app": {
    "withGlobalTauri": true,
    "windows": [{ "title": "My App [DEV]" }]
  }
}
```

### Production (`src-tauri/tauri.prod.conf.json`)

```json
{
  "build": { "frontendDist": "../dist", "removeUnusedCommands": true },
  "bundle": { "active": true, "targets": "all" }
}
```

### Beta (`src-tauri/tauri.beta.conf.json`)

```json
{
  "identifier": "com.company.myapp.beta",
  "productName": "MyApp Beta",
  "plugins": {
    "updater": {
      "endpoints": ["https://beta-releases.example.com/{{target}}/{{arch}}/{{current_version}}"]
    }
  }
}
```

## TOML Configuration Format

When using `Tauri.toml`, configuration uses kebab-case:

```toml
[build]
dev-url = "http://localhost:3000"
before-dev-command = "npm run dev"
before-build-command = "npm run build"

[app]
with-global-tauri = false

[[app.windows]]
title = "My Application"
width = 1200
height = 800
resizable = true
center = true

[app.security]
freeze-prototype = false

[app.security.asset-protocol]
enable = true
scope = ["$APPDATA/**"]

[bundle]
active = true
targets = "all"
icon = ["icons/32x32.png", "icons/128x128.png", "icons/icon.icns", "icons/icon.ico"]

[plugins.updater]
pubkey = "YOUR_PUBLIC_KEY"
endpoints = ["https://releases.example.com/{{target}}/{{arch}}/{{current_version}}"]
```

## Common Configuration Patterns

### Multi-Window Application

```json
{
  "app": {
    "windows": [
      { "label": "main", "title": "Main Window", "width": 1200, "height": 800, "url": "index.html" },
      { "label": "settings", "title": "Settings", "width": 600, "height": 400, "url": "settings.html", "visible": false }
    ]
  }
}
```

### System Tray Application

```json
{
  "app": {
    "trayIcon": { "id": "main-tray", "iconPath": "icons/tray.png", "iconAsTemplate": true },
    "windows": [{ "visible": false }]
  }
}
```

### Plugin Configuration

```json
{
  "plugins": {
    "updater": {
      "pubkey": "YOUR_PUBLIC_KEY",
      "endpoints": ["https://releases.example.com/{{target}}/{{arch}}/{{current_version}}"],
      "windows": { "installMode": "passive" }
    },
    "shell": {
      "open": true,
      "scope": [{ "name": "open-url", "cmd": "open", "args": [{ "validator": "\\S+" }] }]
    },
    "deep-link": {
      "mobile": ["myapp"],
      "desktop": { "schemes": ["myapp"] }
    }
  }
}
```

## Lock Files

Commit lock files for reproducible builds:

| File | Purpose |
|------|---------|
| `Cargo.lock` | Locks Rust dependency versions |
| `package-lock.json` | Locks npm dependency versions |
| `yarn.lock` | Locks Yarn dependency versions |
| `pnpm-lock.yaml` | Locks pnpm dependency versions |

## Configuration Validation

Use the JSON schema for editor autocompletion:

```json
{ "$schema": "https://schema.tauri.app/config/2" }
```

Run `tauri info` to verify configuration and environment setup.
