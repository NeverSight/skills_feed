---
name: mcp-dev
description: Build or update MCP server/client integrations for VMark. Use when configuring MCP servers, adding MCP tools, or updating MCP-related docs and settings.
---

# MCP Dev (VMark)

## Overview
Work on MCP configuration and integration for VMark (servers, tooling, docs).

## Workflow
1) Identify whether this is client or server work.
2) For server config, update `.mcp.json` (local-only) and any app settings if applicable.
3) For client behavior, update hooks/plugins that call MCP tools.
4) Validate against MCP plan docs in `dev-docs/` if available locally.
5) Keep config local unless asked to commit.

## References
- `references/paths.md` for MCP-related files.
