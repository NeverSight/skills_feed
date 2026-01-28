---
name: obsidian-devtools
description: Inspect and automate Obsidian using Chrome DevTools Protocol
tools:
  - obsidian_launch_debug
  - obsidian_eval
  - obsidian_inspect_dom
  - obsidian_read_console
---

# Obsidian DevTools Skill

Enables deep inspection of the Obsidian application state via the Chrome DevTools Protocol.

## Capabilities
- Execute arbitrary JavaScript in the Obsidian context (`app.vault.getFiles()`)
- Read console logs for debugging plugins
- Inspect the DOM to understand UI state

## Setup
This skill requires the `obsidian-devtools` MCP server to be running or available.
The tools usually auto-launch Obsidian with `--remote-debugging-port=9222`.

## Tools

### `obsidian_launch_debug`
Launches or connects to Obsidian with remote debugging enabled.
- `restart`: (bool) Force restart Obsidian to enable debugging (default: False)

### `obsidian_eval`
Executes JavaScript code in the Obsidian app context.
- `expression`: (str) JavaScript code to run
- `await_promise`: (bool) Wait for promises to resolve (default: True)

### `obsidian_inspect_dom`
Gets a simplified snapshot of the DOM structure.
- `selector`: (str) CSS selector for root element (default: "body")

### `obsidian_read_console`
(Experimental) Reads console logs. Currently requires persistent listener mode.

## Examples

**Get Vault Name:**
```javascript
app.vault.getName()
```

**List Plugins:**
```javascript
Object.keys(app.plugins.manifests)
```

**Get Active File:**
```javascript
app.workspace.getActiveFile()?.path
```
