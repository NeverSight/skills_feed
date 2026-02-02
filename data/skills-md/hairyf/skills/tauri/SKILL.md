---
name: tauri
description: Cross-platform app toolkit with Rust backend and WebView frontend. Use when building or maintaining Tauri apps, configuring IPC/security, or developing plugins.
metadata:
  author: hairy
  version: "2026.1.30"
  source: Generated from https://github.com/tauri-apps/tauri-docs, scripts located at https://github.com/antfu/skills
---

Tauri lets you build desktop (and mobile) apps with a Rust Core process and a frontend running in the OS WebView. Use these skills when scaffolding projects, wiring commands and events, configuring capabilities and permissions, or authoring plugins.

> The skill is based on Tauri v2, generated at 2026-01-30.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Architecture | Core crates, WRY/TAO, tooling, plugins | [core-architecture](references/core-architecture.md) |
| IPC | Events (fire-and-forget) vs Commands (invoke/response), when to use each | [core-ipc](references/core-ipc.md) |
| Process Model | Core process vs WebView processes, security implications | [core-process-model](references/core-process-model.md) |
| Project Structure | src-tauri layout, tauri.conf.json, capabilities, build flow | [core-project-structure](references/core-project-structure.md) |
| App Size | Why small, Cargo release profile (LTO, strip, opt-level) | [concept-size](references/concept-size.md) |
| IPC Patterns | Brownfield (default) vs Isolation (sandbox, encrypt) | [concept-ipc-patterns](references/concept-ipc-patterns.md) |

## Start

| Topic | Description | Reference |
|-------|-------------|-----------|
| Create Project | create-tauri-app vs tauri init, dev server URL | [start-create-project](references/start-create-project.md) |
| Prerequisites | System deps, Rust, Node, WebView2, mobile (Android/iOS) | [start-prerequisites](references/start-prerequisites.md) |
| Frontend | Static host model, Vite/Next/Nuxt/SvelteKit/Leptos/Trunk | [start-frontend](references/start-frontend.md) |
| Migrate | Upgrading from Tauri 1.x or 2 beta, migrate command | [start-migrate](references/start-migrate.md) |

## Develop

| Topic | Description | Reference |
|-------|-------------|-----------|
| Configuration Files | tauri.conf.json, platform overrides, Cargo.toml, package.json | [develop-configuration-files](references/develop-configuration-files.md) |
| Commands | #[tauri::command], invoke, args, errors, async, State, channels | [develop-commands](references/develop-commands.md) |
| Events and Channels | Emit/listen, global vs webview-specific, streaming with Channel | [develop-events-and-channels](references/develop-events-and-channels.md) |
| State Management | app.manage(), State\<T\> in commands, Mutex | [develop-state-management](references/develop-state-management.md) |
| Windows | Creating windows (config vs WebviewWindowBuilder), label, url, visible | [develop-windows](references/develop-windows.md) |
| Icons | tauri icon command, bundle.icon, platform formats | [develop-icons](references/develop-icons.md) |
| Resources | Bundled resources, resolve path, $RESOURCE, fs permissions | [develop-resources](references/develop-resources.md) |
| Sidecar | externalBin, shell plugin, spawn from Rust/JS, permissions | [develop-sidecar](references/develop-sidecar.md) |
| Debug | dev vs build, Rust console, WebView devtools, RUST_BACKTRACE | [develop-debug](references/develop-debug.md) |
| Tests | Mock runtime, WebDriver E2E, CI | [develop-tests](references/develop-tests.md) |
| Tests Mocking | mockIPC, mockWindows, clearMocks (frontend tests) | [develop-tests-mocking](references/develop-tests-mocking.md) |
| Tests WebDriver | tauri-driver, platform drivers, Selenium/WebdriverIO, CI | [develop-tests-webdriver](references/develop-tests-webdriver.md) |
| Updating Dependencies | npm/Cargo version sync, tauri and plugins | [develop-updating-dependencies](references/develop-updating-dependencies.md) |
| Plugins Mobile | Android (Kotlin), iOS (Swift), desktop vs mobile impl | [develop-plugins-mobile](references/develop-plugins-mobile.md) |

## Security

| Topic | Description | Reference |
|-------|-------------|-----------|
| Capabilities | Which permissions apply to which windows; capability files, remote, platforms | [security-capabilities](references/security-capabilities.md) |
| Permissions | Allow/deny commands, scopes, permission sets; plugin vs app permissions | [security-permissions](references/security-permissions.md) |
| Scopes | allow/deny per command or global, path/URL patterns | [security-scope](references/security-scope.md) |
| CSP | Content Security Policy config, script-src, style-src | [security-csp](references/security-csp.md) |
| HTTP Headers | CORS, COOP, Permissions-Policy for webview responses | [security-http-headers](references/security-http-headers.md) |
| Runtime Authority | Core enforces permissions on every invoke; denied = never run | [security-runtime-authority](references/security-runtime-authority.md) |

## Best Practices

| Topic | Description | Reference |
|-------|-------------|-----------|
| Security Lifecycle | Upstream, development, build, runtime; deps, audit, dev server | [best-practices-security-lifecycle](references/best-practices-security-lifecycle.md) |
| Writing Plugin Permissions | Autogenerated allow/deny, permission files, default set, scope schema | [best-practices-writing-plugin-permissions](references/best-practices-writing-plugin-permissions.md) |

## Features

| Topic | Description | Reference |
|-------|-------------|-----------|
| Plugins | Plugin development, lifecycle hooks, commands, permissions, state | [features-plugins](references/features-plugins.md) |
| Official Plugins Overview | dialog, fs, shell, store, updater, and others; when to use which | [features-official-plugins-overview](references/features-official-plugins-overview.md) |
| Deep Linking | Custom URL scheme, App/Universal Links, single-instance + argv | [features-deep-linking](references/features-deep-linking.md) |
| Updater | In-app updates — check, download, install, signing, static/dynamic endpoints | [features-updater](references/features-updater.md) |

## Distribute

| Topic | Description | Reference |
|-------|-------------|-----------|
| Packaging | build, bundle, installers (DMG, MSI, AppImage, etc.), signing overview | [distribute-packaging](references/distribute-packaging.md) |
| Signing | Code signing per platform (macOS, Windows, Linux, Android, iOS) | [distribute-signing](references/distribute-signing.md) |
| Pipelines | GitHub Actions (tauri-action), CI signing, CrabNebula Cloud | [distribute-pipelines](references/distribute-pipelines.md) |

## Learn

| Topic | Description | Reference |
|-------|-------------|-----------|
| Menus and Tray | Window menu, system tray, Menu/TrayIcon, predefined items | [learn-windows-menus-tray](references/learn-windows-menus-tray.md) |
| Window Customization | Custom titlebar, decorations, data-tauri-drag-region, transparent (macOS) | [learn-window-customization](references/learn-window-customization.md) |
| Splashscreen | Extra window, visible/hidden main, setup tasks, close when ready | [learn-splashscreen](references/learn-splashscreen.md) |
| Sidecar Node.js | Node app as binary (pkg), externalBin, shell plugin | [learn-sidecar-nodejs](references/learn-sidecar-nodejs.md) |
| Using Plugin Permissions | Add plugin, capability, allow commands, default permissions | [learn-using-plugin-permissions](references/learn-using-plugin-permissions.md) |
| Capabilities per Window/Platform | Different capabilities per window; platforms array | [learn-capabilities-windows-platforms](references/learn-capabilities-windows-platforms.md) |

## Reference

| Topic | Description | Reference |
|-------|-------------|-----------|
| CLI | dev, build, icon, init, migrate, bundle | [reference-cli](references/reference-cli.md) |
| Environment Variables | CI, config depth, signing, Apple/Windows/Linux, hook env | [reference-environment-variables](references/reference-environment-variables.md) |
| WebView Versions | WebView2 (Windows), WKWebView (macOS/iOS), WebKitGTK (Linux) | [reference-webview-versions](references/reference-webview-versions.md) |
| Core Permissions (ACL) | core:default, app, event, window, path, menu, tray, resources | [reference-acl-core-permissions](references/reference-acl-core-permissions.md) |
