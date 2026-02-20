---
name: tauri-v2-integration
description: Implement or adjust VMark frontend <-> Tauri v2 integration. Use when adding invoke/emit bridges, menu accelerators, or IPC-related UI behaviors.
---

# Tauri v2 Integration (VMark)

## Overview
Ensure Tauri v2 bridge patterns and IPC flows are consistent across frontend and Rust.

## Workflow
1) Identify the bridge direction:
   - Rust -> Webview: `window.emit()`/`app.emit()` + `listen()` on frontend.
   - Webview -> Rust: `invoke()`.
2) Update frontend hooks/plugins that manage IPC (`src/hooks/`, `src/plugins/`).
3) Update Rust commands or menu entries in `src-tauri/`.
4) Keep behavior consistent across WYSIWYG and Source modes.
5) If E2E behavior needs validation, use Tauri MCP tools.

## References
- `references/paths.md` for key files and patterns.
- Manual E2E: see `tauri-mcp-testing` skill for patterns.

## Related Skills
- **`tauri-app-dev`** — General Tauri 2.0 patterns (commands, state, plugins, security)
- **`tauri-mcp-testing`** — E2E testing via Tauri MCP tools
- **`rust-tauri-backend`** — VMark Rust backend implementation
