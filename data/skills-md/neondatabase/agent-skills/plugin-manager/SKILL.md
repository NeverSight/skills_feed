---
name: plugin-manager
description: Manage plugin structure and configuration for this repository across both Cursor and Claude Code. Use when creating, updating, or reviewing plugin folders under plugins/, wiring marketplace manifests, setting up skill symlinks, assigning per-plugin mcp.json files, or adding additional plugins while preserving repo conventions.
---

# Plugin Manager

Maintain plugin packaging for both ecosystems in a single repository, using a shared `plugins/` directory and a shared top-level `skills/` source of truth.

## Working Rules

- Keep each plugin self-contained in `plugins/<plugin-name>/`.
- Keep shared reusable skill content in top-level `skills/`.
- Expose shared skills per plugin via symlinks in `plugins/<plugin-name>/skills/`.
- Keep MCP config plugin-local at `plugins/<plugin-name>/mcp.json`.
- Keep both marketplace manifests at repo root:
  - `.claude-plugin/marketplace.json`
  - `.cursor-plugin/marketplace.json`

## Required Plugin Layout

For every plugin, ensure this layout exists:

```text
plugins/<plugin-name>/
  .claude-plugin/plugin.json
  .cursor-plugin/plugin.json
  skills/
    <skill-name> -> ../../../skills/<skill-name>   # symlink
  mcp.json
  assets/
```

## Create or Update a Plugin

1. Create `plugins/<plugin-name>/`.
2. Add both manifests:
   - `plugins/<plugin-name>/.claude-plugin/plugin.json`
   - `plugins/<plugin-name>/.cursor-plugin/plugin.json`
3. Add or update `plugins/<plugin-name>/mcp.json` for plugin-specific MCP servers.
4. Symlink required top-level skills into `plugins/<plugin-name>/skills/`.
5. Add `plugins/<plugin-name>/assets/logo.svg` for Cursor.
6. Register plugin in both marketplaces using `source: "./plugins/<plugin-name>"`.
7. Validate JSON and path references before finishing.

## Manifest Guidelines

- **Claude plugin manifest**
  - Path: `plugins/<plugin-name>/.claude-plugin/plugin.json`
  - Prefer plugin-local relative paths, for example:
    - `"skills": "./skills/"`
    - `"mcpServers": "./mcp.json"`
- **Cursor plugin manifest**
  - Path: `plugins/<plugin-name>/.cursor-plugin/plugin.json`
  - Prefer plugin-local relative paths, for example:
    - `"skills": "./skills/"`
    - `"mcpServers": "./mcp.json"`
    - `"logo": "assets/logo.svg"`
- **Marketplace manifests**
  - `.claude-plugin/marketplace.json` uses `source: "./plugins/<plugin-name>"`.
  - `.cursor-plugin/marketplace.json` uses `metadata.pluginRoot: "plugins"` and plugin entries with `source: "<plugin-name>"`.

## References

- For detailed examples and checklists, read `references/plugin-guidelines.md`.
