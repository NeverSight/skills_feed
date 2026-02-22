---
name: tensorpm-agentic-pm
description: 'Agentic project management powered by TensorPM. Manage projects, action items, and workspaces through MCP tools and A2A protocol. Context-driven AI project management for agents.'
compatibility: Requires the TensorPM desktop app to be running for MCP tool access and A2A communication. Available on macOS, Windows, and Linux.
---

# TensorPM Skill

Use this skill for AI-powered, context-driven project management inside a running TensorPM desktop app.
TensorPM itself is free. For AI capabilities outside MCP (A2A), use your own API key (BYOK) or create an account.

## When To Use

- You need to list, create, or update TensorPM projects or action items.
- You need to switch/list workspaces.
- You need to set AI provider keys through TensorPM (`set_api_key`).
- You need conversational project-level changes via A2A (`message/send`).

## When Not To Use

- The request is only about website/account/billing pages.

## Installation (Agent CLI)

Use one of these agent-friendly CLI install methods:

```bash
# macOS
brew install --cask neo552/tensorpm/tensorpm
```

```powershell
# Windows (PowerShell)
winget install --id Neo552.TensorPM --exact --accept-package-agreements --accept-source-agreements
```

```bash
# macOS / Linux fallback installer script
curl -fsSL https://raw.githubusercontent.com/Neo552/TensorPM/main/scripts/install.sh | bash
```

```powershell
# Windows fallback installer script
irm https://raw.githubusercontent.com/Neo552/TensorPM/main/scripts/install.ps1 | iex
```

## Runtime Prerequisites

1. Start TensorPM desktop app.
2. For MCP usage with external AI clients: ensure client integration is installed once (via **Settings -> Integrations** or A2A `POST /integrations/mcp/install`).
3. For A2A usage: verify local endpoint `http://localhost:37850`.

## MCP vs A2A Routing

| Task                                        | Use                  | Why                              |
| ------------------------------------------- | -------------------- | -------------------------------- |
| Structured action-item CRUD                 | MCP tools            | Direct typed operations          |
| Set provider API keys                       | MCP `set_api_key`    | Dedicated secure write-only tool |
| Project-wide/contextual changes             | A2A `message/send`   | Managed by project manager agent |
| HTTP-based automation/client integration    | A2A REST/JSON-RPC    | Endpoint-first integration path  |
| Multi-turn planning with conversation state | A2A with `contextId` | Native conversation continuity   |

Rule of thumb:

- Prefer MCP for explicit CRUD operations.
- Prefer A2A for high-level intent and context-aware planning.

## Minimal Workflow

1. Verify TensorPM is running.
2. Choose MCP vs A2A via the routing table above.
3. Execute operation.
4. Read back result (`list_*`, `get_project`, or A2A read endpoint) to confirm state.
5. Summarize applied changes and any follow-up action.

## References

- [MCP Tools](MCP-TOOLS.md): tool catalog and usage boundaries.
- [A2A API](A2A-API.md): discovery, JSON-RPC methods, REST endpoints, examples.
- [Action Items & Dependencies](ACTION-ITEMS.md): fields, dependency types, payload examples.

## Notes

- IDs are UUIDs.
- Dates use ISO format (`YYYY-MM-DD`).
- `propose_updates` requires human approval before apply.
- MCP and A2A operate on the same local TensorPM data.
- Release notes: <https://github.com/Neo552/TensorPM-Releases/releases/latest>
