---
name: chatgpt-app-creator
description: >-
  Builds ChatGPT Apps with the OpenAI Apps SDK. Use when:
  (1) Setting up MCP servers for ChatGPT integration,
  (2) Implementing OAuth provider endpoints (you ARE the provider, ChatGPT is the client),
  (3) Creating widgets with text/html+skybridge MIME type,
  (4) Using window.openai API for widget-ChatGPT communication,
  (5) Debugging OAuth, CORS, PKCE, CSP, or widget rendering issues,
  (6) Understanding ChatGPT Apps architecture (MCP + widgets + OAuth).
---

# ChatGPT App Creator

> Last verified: January 2026. Cross-reference with [official docs](https://developers.openai.com/apps-sdk/) for latest information.

## Quick Context

The ChatGPT Apps SDK enables developers to build interactive applications that run inside ChatGPT. Based on available documentation, apps consist of three components:

1. **MCP Server**: Exposes tools and resources via the Model Context Protocol
2. **Widgets**: HTML/JS UI components rendered in iframes within ChatGPT
3. **OAuth Provider**: Authentication where **you are the OAuth provider** (ChatGPT is the client)

**Critical Mental Model**: Unlike typical OAuth integrations where your app consumes someone else's OAuth (like "Sign in with Google"), ChatGPT Apps flip this around. You run the OAuth server, and ChatGPT is the OAuth client connecting to you. This is the #1 source of confusion based on developer reports.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                      ChatGPT                            │
│  ┌─────────────────┐         ┌───────────────────────┐  │
│  │   Chat Message  │         │   Widget (iframe)     │  │
│  │   with Tool     │◄───────►│   window.openai API   │  │
│  │   Results       │         │                       │  │
│  └────────┬────────┘         └───────────┬───────────┘  │
└───────────┼──────────────────────────────┼──────────────┘
            │                              │
            ▼                              ▼
┌───────────────────────┐      ┌───────────────────────┐
│    Your MCP Server    │      │   Your OAuth Server   │
│  - tools              │      │  /.well-known/...     │
│  - resources          │      │  /authorize, /token   │
│  - widget HTML        │      │  /register (DCR)      │
└───────────────────────┘      └───────────────────────┘
```

### Key Technical Details

- **Widgets** are served as resources with MIME type `text/html+skybridge`
- **PKCE S256** is mandatory for OAuth
- **Dynamic Client Registration (DCR)** generates fresh client credentials per session
- Tools should have descriptions starting with "Use this when..." for better discovery
- **Tool annotations** are required: `readOnlyHint`, `openWorldHint`, `destructiveHint`
- **Tool responses** use three-part structure:
  - `structuredContent`: Concise data for the model (keep small)
  - `content`: Text narration shown in chat
  - `_meta`: Widget-only data including `openai/outputTemplate` for widget rendering

## Common Tasks

### Creating an MCP Server

See `scripts/mcp-server.ts` (Node.js) or `scripts/mcp-server.py` (Python) for complete examples.

**Transport Modes** (critical for production):
- **stdio**: For local testing with MCP Inspector only
- **http**: For production with ChatGPT—exposes HTTP/SSE endpoints

```bash
# Local testing (stdio)
npx tsx mcp-server.ts

# Production (HTTP/SSE) - required for ChatGPT
MCP_TRANSPORT=http npx tsx mcp-server.ts
```

Key points:
- Use descriptive tool names and descriptions
- Return structured data for widgets to consume
- Handle CORS headers on the MCP endpoint (done automatically in http mode)
- Include resource references in tool responses to trigger widget rendering

### Implementing OAuth

See `references/oauth-setup.md` for comprehensive guide.

Required endpoints:
1. `/.well-known/oauth-protected-resource` - Declares your authorization server
2. `/.well-known/oauth-authorization-server` - OAuth server metadata
3. `/authorize` - User login and consent
4. `/token` - Token exchange (must handle Basic Auth headers)
5. `/register` - Dynamic Client Registration

### Widget Development

Widgets communicate via the `window.openai` API. See `references/window-openai-api.md` for full reference.

Key APIs:
- `window.openai.toolOutput` - Data from tool response
- `window.openai.widgetState` - Persistent state within a message
- `window.openai.callTool()` - Invoke MCP tools from widget
- `window.openai.setWidgetState()` - Update persistent state

## Critical Gotchas

Most issues developers encounter are already documented. Check `references/gotchas.md` first when debugging—it covers 20 common problems including OAuth role confusion, PKCE errors, widget caching, CSP violations, tool annotations, and more, each with code fixes.

## Debugging

Use the MCP Inspector to test your server:
```bash
npx @modelcontextprotocol/inspector
```

See `references/troubleshooting.md` for error diagnosis guide.

## Submission

Before submitting to the ChatGPT App Store:
- Ensure all tools have correct `annotations` (top rejection reason)
- Server must be on public HTTPS (no localhost/ngrok)
- Provide test credentials for authenticated apps
- Organization must be verified with Owner role

See `references/submission.md` for complete requirements and common rejection reasons.

## Reference Files

Load these for detailed information:

| File | Contents |
|------|----------|
| `references/window-openai-api.md` | Complete widget API reference |
| `references/oauth-setup.md` | Step-by-step OAuth implementation |
| `references/gotchas.md` | All documented issues with solutions |
| `references/troubleshooting.md` | Error diagnosis and debugging |
| `references/submission.md` | App submission requirements and review process |

## Script Files

Working code examples:

| File | Description |
|------|-------------|
| `scripts/mcp-server.ts` | Node.js/TypeScript MCP server |
| `scripts/mcp-server.py` | Python MCP server |
| `scripts/oauth-provider.ts` | OAuth provider implementation |

## Assets

Widget templates used by the MCP server examples:

| File | Description |
|------|-------------|
| `assets/widgets/search-results.html` | Product search results grid widget |
| `assets/widgets/order-tracker.html` | Order status tracking widget |

Run with:
```bash
# TypeScript
cd scripts && npm install && npx tsx mcp-server.ts

# Python
cd scripts && pip install -r requirements.txt && python mcp-server.py
```

## Quick Reference

**Widget MIME type:** `text/html+skybridge`

**Tool annotations** (all three required):
```
readOnlyHint: true     # Only reads data, no side effects
openWorldHint: false   # Only affects user's data, not external systems
destructiveHint: false # No irreversible changes
```

**Tool response structure:**
```
structuredContent  → Model reads this (keep concise)
content            → Shown in chat as narration
_meta              → Widget-only (model never sees)
  └─ "openai/outputTemplate": "widget://app/name"
```

**OAuth endpoints:**
```
/.well-known/oauth-protected-resource
/.well-known/oauth-authorization-server
/authorize
/token
/register
```

**Widget APIs:**
```javascript
window.openai.toolOutput          // Tool response data
window.openai.widgetState         // Persistent state
window.openai.theme               // 'light' or 'dark'
window.openai.setWidgetState()    // Update state
window.openai.callTool(name, args) // Call MCP tools
```

**Commands:**
```bash
# Test MCP server locally
npx @modelcontextprotocol/inspector

# Run TypeScript server (production)
MCP_TRANSPORT=http npx tsx mcp-server.ts

# Run Python server (production)
MCP_TRANSPORT=http python mcp-server.py
```

## Notes

- Cross-reference with [official docs](https://developers.openai.com/apps-sdk/) for latest changes
- Test incrementally: OAuth → MCP tools → Widgets
