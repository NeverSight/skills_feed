---
name: logseq-plugin-dev
description: "Comprehensive guide and resources for developing Logseq plugins. Use this skill when asked to: (1) Create a new Logseq plugin, (2) Implement features using the Logseq Plugin API (Editor, App, DB, UI), (3) Debug or refactor existing Logseq plugins, (4) Set up a development environment for Logseq plugins."
---

# Logseq Plugin Development

This skill helps you build high-quality plugins for Logseq using the `@logseq/libs` SDK.

## Core Concepts

Logseq plugins run in a sandboxed `iframe` and communicate with the main Logseq application via an RPC bridge.

- **Manifest**: Every plugin needs a `package.json` with a `logseq` field.
- **SDK**: Use `@logseq/libs` to interact with Logseq.
- **Lifecycle**: Use `logseq.ready(main)` to initialize your plugin.

## Getting Started

1. **Scaffold**: 
   - Basic TS: `assets/template/`
   - React + Vite: `assets/template-react/`
2. **Install Dependencies**: `npm install @logseq/libs`.
3. **Build**: Use Vite or a similar bundler to package your JS/TS code.
4. **Load**: In Logseq, go to `Settings -> Plugins -> Developer Mode`, then `Load unpacked plugin` and select your plugin directory.

## Common Workflows

### 1. Registering Commands
Use `logseq.Editor.registerSlashCommand` or `logseq.App.registerCommandPalette`.

### 2. Interacting with Content
- **Read**: `logseq.Editor.getCurrentPageBlocksTree()`
- **Write**: `logseq.Editor.insertBlock(parentBlockId, content)`
- **Query**: `logseq.DB.datascriptQuery(query)`

### 3. UI and Theming
- **UI**: Use `logseq.provideUI` to inject HTML or `logseq.showMainUI` to show a full-screen app.
- **Theming**: Use Logseq CSS variables (e.g., `--ls-primary-background-color`) for consistency.

## Resources

- **API Reference**: See [references/api.md](references/api.md) for a detailed list of available methods and examples.
- **Boilerplates**: 
  - [assets/template/](assets/template/) (Vanilla TS)
  - [assets/template-react/](assets/template-react/) (React + Vite)
- **Examples**: See [references/examples.md](references/examples.md) for common patterns like mind maps and slash commands.
