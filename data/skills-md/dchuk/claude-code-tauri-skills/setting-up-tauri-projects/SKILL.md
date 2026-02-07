---
name: setting-up-tauri-projects
description: Helps users create and initialize new Tauri v2 projects for building cross-platform desktop and mobile applications. Covers system prerequisites and setup requirements for macOS, Windows, and Linux. Guides through project creation using create-tauri-app or manual Tauri CLI initialization. Explains project directory structure and configuration files. Supports vanilla JavaScript, TypeScript, React, Vue, Svelte, Angular, SolidJS, and Rust-based frontends.
---

# Setting Up Tauri Projects

## What is Tauri?

Tauri is a framework for building tiny, fast binaries for all major desktop and mobile platforms. It combines any frontend that compiles to HTML/JS/CSS with Rust for the backend.

**Key characteristics:**
- Minimal apps can be under 600KB (uses system webview, not bundled browser)
- Built on Rust for memory, thread, and type safety
- Supports virtually any frontend framework
- Cross-platform: Windows, macOS, Linux, iOS, Android

## System Prerequisites

### macOS

```bash
# For desktop + iOS development
# Install Xcode from Mac App Store

# For desktop-only development (lighter option)
xcode-select --install
```

### Windows

1. **Microsoft C++ Build Tools**: Download from Visual Studio, select "Desktop development with C++"
2. **WebView2**: Pre-installed on Windows 10 v1803+ (install manually if needed)
3. **Rust toolchain**:
```powershell
winget install Rustlang.Rustup
rustup default stable-msvc
```

### Linux

**Debian/Ubuntu:**
```bash
sudo apt update
sudo apt install libwebkit2gtk-4.1-dev build-essential curl wget file \
  libxdo-dev libssl-dev libayatana-appindicator3-dev librsvg2-dev
```

**Arch Linux:**
```bash
sudo pacman -S webkit2gtk-4.1 base-devel curl wget file openssl \
  appmenu-gtk-module libappindicator-gtk3 librsvg xdotool
```

**Fedora:**
```bash
sudo dnf install webkit2gtk4.1-devel openssl-devel curl wget file \
  libappindicator-gtk3-devel librsvg2-devel libxdo-devel \
  @development-tools
```

### Rust (All Platforms)

```bash
# macOS/Linux
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Windows (PowerShell)
winget install Rustlang.Rustup
```

### Node.js

Required only for JavaScript/TypeScript frontends. Install LTS version from nodejs.org.

### Mobile Development (Optional)

**Android (all platforms):**
```bash
# Install Android Studio, then add Rust targets
rustup target add aarch64-linux-android armv7-linux-androideabi \
  i686-linux-android x86_64-linux-android
```

Set environment variables: `JAVA_HOME`, `ANDROID_HOME`, `NDK_HOME`

**iOS (macOS only):**
```bash
# Requires full Xcode (not just Command Line Tools)
rustup target add aarch64-apple-ios x86_64-apple-ios aarch64-apple-ios-sim

# Install Cocoapods
brew install cocoapods
```

## Creating a Project

### Method 1: create-tauri-app (Recommended)

Interactive scaffolding with framework templates.

```bash
# npm
npm create tauri-app@latest

# pnpm
pnpm create tauri-app

# yarn
yarn create tauri-app

# bun
bun create tauri-app

# cargo (no Node.js required)
cargo install create-tauri-app --locked
cargo create-tauri-app

# Shell scripts
sh <(curl https://create.tauri.app/sh)        # Bash
irm https://create.tauri.app/ps | iex         # PowerShell
```

**Prompts you'll see:**
1. Project name
2. Bundle identifier (e.g., `com.example.app`)
3. Frontend language: TypeScript/JavaScript, Rust, or .NET
4. Package manager
5. UI template: vanilla, Vue, Svelte, React, SolidJS, Angular, Preact, Yew, Leptos, Sycamore

**After scaffolding:**
```bash
cd your-project
npm install
npm run tauri dev
```

### Method 2: Manual Setup (Existing Projects)

Add Tauri to an existing frontend project.

```bash
# 1. In your existing project, install Tauri CLI
npm install -D @tauri-apps/cli@latest

# 2. Initialize Tauri (creates src-tauri directory)
npx tauri init
```

**tauri init prompts:**
- App name
- Window title
- Frontend dev server URL (e.g., `http://localhost:5173`)
- Frontend build output directory (e.g., `dist`)
- Frontend dev command (e.g., `npm run dev`)
- Frontend build command (e.g., `npm run build`)

```bash
# 3. Start development
npx tauri dev
```

## Project Structure

```
my-tauri-app/
├── package.json           # Frontend dependencies
├── index.html             # Frontend entry point
├── src/                   # Frontend source code
│   └── main.js
└── src-tauri/             # Rust backend
    ├── Cargo.toml         # Rust dependencies
    ├── Cargo.lock
    ├── build.rs           # Tauri build script
    ├── tauri.conf.json    # Main Tauri configuration
    ├── capabilities/      # Permission/capability definitions
    ├── icons/             # App icons (all formats)
    └── src/
        ├── lib.rs         # Main Rust code + mobile entry point
        └── main.rs        # Desktop entry point
```

### Key Files

**tauri.conf.json** - Primary configuration:
```json
{
  "productName": "my-app",
  "version": "0.1.0",
  "identifier": "com.example.my-app",
  "build": {
    "devUrl": "http://localhost:5173",
    "frontendDist": "../dist"
  },
  "app": {
    "windows": [{ "title": "My App", "width": 800, "height": 600 }]
  }
}
```

**src/lib.rs** - Rust application code:
```rust
#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

**src/main.rs** - Desktop entry point:
```rust
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

fn main() {
    app_lib::run();
}
```

**capabilities/** - Define what commands JavaScript can invoke:
```json
{
  "identifier": "main-capability",
  "windows": ["main"],
  "permissions": ["core:default"]
}
```

## Common Commands

```bash
# Development with hot reload
npm run tauri dev

# Build production binary
npm run tauri build

# Generate app icons from source image
npm run tauri icon path/to/icon.png

# Add Android target
npm run tauri android init

# Add iOS target
npm run tauri ios init

# Run on Android
npm run tauri android dev

# Run on iOS simulator
npm run tauri ios dev
```

## Quick Reference: Supported Frontend Templates

| Template | Languages | Notes |
|----------|-----------|-------|
| vanilla | JS, TS | No framework |
| react | JS, TS | Vite-based |
| vue | JS, TS | Vite-based |
| svelte | JS, TS | Vite-based |
| solid | JS, TS | Vite-based |
| angular | TS | Angular CLI |
| preact | JS, TS | Vite-based |
| yew | Rust | Rust WASM frontend |
| leptos | Rust | Rust WASM frontend |
| sycamore | Rust | Rust WASM frontend |
