---
name: obsidian-developer
description: Expert guide for inspecting and automating Obsidian using the obsidian-devtools MCP server.
tools:
  - obsidian_launch_debug
  - obsidian_eval
  - obsidian_inspect_dom
  - obsidian_discover_api
  - obsidian_get_frontmatter
  - obsidian_update_frontmatter
  - obsidian_create_canvas
  - obsidian_graph_zoom
---

# Obsidian Developer Skill

This skill transforms Claude into an expert Obsidian plugin developer and automation engineer. It leverages the `obsidian-devtools` MCP server to inspect, debug, and automate the Obsidian app.

## Quick Start

1. **Connect**: `obsidian_launch_debug()` — starts Obsidian with CDP enabled
2. **Discover**: `obsidian_discover_api("app.vault")` — explore available methods
3. **Execute**: `obsidian_eval("app.vault.getName()")` — run any JavaScript
4. **Automate**: Use patterns from `patterns/` for common tasks

## Workflow

1.  **Connect**: Ensure Obsidian is running with debug flags.
    -   Run `obsidian_launch_debug()` to start or attach.

2.  **Inspect**: Understand the current state.
    -   Use `obsidian_inspect_dom()` to see the UI structure.
    -   Use `obsidian_discover_api()` to explore internal APIs.
    -   Refer to `knowledge/dom-patterns.md` for class names.

3.  **Execute**: Run automation or queries.
    -   Use `obsidian_eval()` to interact with the `app` object.
    -   Refer to `knowledge/api-basics.md` for common API calls.
    -   Refer to `knowledge/cdp-protocol.md` for data passing rules.

4.  **Create**: Generate visual content.
    -   Use `obsidian_create_canvas()` for spatial layouts.
    -   Refer to `knowledge/canvas-api.md` for node/edge schemas.

## Knowledge Modules

| Module | Purpose |
|--------|---------|
| [API Basics](knowledge/api-basics.md) | `app.vault`, `app.workspace`, `app.plugins` |
| [SDK Reference](knowledge/sdk-reference.md) | Python SDK for programmatic access |
| [Canvas API](knowledge/canvas-api.md) | Creating and manipulating canvas files |
| [Graph View](knowledge/graph-view.md) | Graph data extraction and analysis |
| [CDP Protocol](knowledge/cdp-protocol.md) | `Runtime.evaluate` internals |
| [DOM Patterns](knowledge/dom-patterns.md) | CSS classes for UI automation |

## Pattern Library

Reusable scripts in `patterns/`:

| Pattern | Purpose |
|---------|---------|
| [plugin-audit.js](patterns/plugin-audit.js) | List enabled plugins with metadata |
| [theme-extract.js](patterns/theme-extract.js) | Dump CSS variables |
| [dataview-query.js](patterns/dataview-query.js) | Run Dataview queries via JS |
| [frontmatter-batch.js](patterns/frontmatter-batch.js) | Batch frontmatter operations |
| [canvas-generator.js](patterns/canvas-generator.js) | Generate canvases from vault data |

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `obsidian_launch_debug` | Start/attach to Obsidian with CDP |
| `obsidian_eval` | Execute JavaScript in Obsidian context |
| `obsidian_inspect_dom` | Get summarized DOM snapshot |
| `obsidian_discover_api` | Introspect object methods/properties |
| `obsidian_get_frontmatter` | Read file frontmatter |
| `obsidian_update_frontmatter` | Modify frontmatter key |
| `obsidian_create_canvas` | Create .canvas file |
| `obsidian_graph_zoom` | Control graph view zoom |

## Tips

-   **Async is Key**: Wrap code in `(async () => { ... })()` if using `await`.
-   **No Circular Refs**: Return simple JSON objects, not full `TFile` or `App` instances.
-   **Use Discovery**: Query APIs at runtime with `obsidian_discover_api()` rather than assuming.
-   **Security**: The server runs in Safe Mode. File system writes are blocked unless configured.
-   **Batch Operations**: Use `frontmatter-batch.js` patterns for vault-wide changes.

## Related

- [SKILLS-INDEX.md](../SKILLS-INDEX.md) — Master skill navigation
- [VERTEX-MAP.md](../VERTEX-MAP.md) — Cross-skill integration
