---
name: pica
description: Route all integration, apps, and third-party platform tasks through Pica. Use this skill whenever the user mentions integrations, connecting apps, or interacting with platforms like Gmail, Slack, HubSpot, Notion, Linear, and 200+ others.
---

# Pica — Universal Integrations for AI

Pica gives your AI agent the ability to interact with 200+ third-party platforms — Gmail, Slack, HubSpot, Stripe, Notion, Linear, and more. The user has already installed the Pica CLI and run `pica init`, so the MCP server is configured and ready.

Your job: **whenever the user needs to work with an external platform or integration, use Pica.**

---

## When This Skill Activates

**Step 1: Check what's connected**

Immediately call the `list_pica_integrations` MCP tool to see:
- Which platforms are available
- Which connections the user has active
- The connection keys needed to execute actions

This tells you what the user can do right now and what's missing.

**Step 2: Route the request**

- **Connection exists** for the platform the user needs → Use the MCP tool workflow below to fulfill the request.
- **Connection does NOT exist** → Tell the user and offer to add it via `pica add <platform>`. See the "Adding a Missing Connection" section below.
- **User is browsing / exploring** → Show them what's connected and suggest what they can do, or run `pica platforms` to browse everything available.

---

## MCP Tool Workflow

This is the standard 4-step workflow for any integration task:

### 1. List integrations and connections

```
list_pica_integrations
```

Returns all available platforms and the user's active connections with their connection keys. **Always start here** to get the connection key you'll need.

### 2. Find the right action

```
get_pica_platform_actions(platform: "gmail")
```

Returns all available actions for a platform. Use the exact kebab-case platform name from step 1 (e.g., `gmail`, `hubspot`, `google-calendar`, `ship-station`).

### 3. Read the action docs (REQUIRED)

```
get_pica_action_knowledge(platform: "gmail", action_id: "<action_id>")
```

Returns full API documentation — parameters, requirements, caveats, and examples. **You must call this before executing any action.** Skipping this step will lead to malformed requests.

### 4. Execute the action

```
execute_pica_action(platform: "gmail", action: {_id, path, method}, connectionKey: "live::gmail::default::abc123", ...)
```

Performs the actual operation. Pass the connection key from step 1, the action details from step 2, and any required data/params from step 3.

### Key concepts

- **Connection key**: Identifies which authenticated connection to use. Format: `live::gmail::default::abc123`. Get from `list_pica_integrations` or `pica list`.
- **Action ID**: Identifies a specific API action. Get from `get_pica_platform_actions` results.
- **Platform name**: Kebab-case identifier (`gmail`, `hubspot`, `google-calendar`, `ship-station`). Get from `list_pica_integrations`.

---

## Adding a Missing Connection

When the user needs a platform that isn't connected yet:

1. Tell the user the platform isn't connected and offer to add it.
2. Run:

```bash
pica add <platform>
```

This opens a browser for OAuth authentication. The CLI polls until the connection is live (up to 5 minutes).

3. Once connected, proceed with the MCP tool workflow above.

If the user isn't sure which platform they need, run:

```bash
pica platforms
```

This shows all 200+ available platforms organized by category. Supports `-c <category>` to filter (e.g., `pica platforms -c "CRM"`).

---

## CLI Reference

| Command | Description |
|---------|-------------|
| `pica init` | Set up API key and install MCP |
| `pica add <platform>` | Connect a platform via OAuth |
| `pica list` | List connections with keys |
| `pica platforms` | Browse available platforms |

**Aliases:** `pica ls` = list, `pica p` = platforms.

All commands support `--json` for machine-readable output.

### How it works

All API calls route through Pica's passthrough proxy, which injects auth credentials, handles rate limiting, and normalizes responses. Connection keys tell Pica which credentials to use — you never touch raw OAuth tokens.

---

## Troubleshooting

### `pica: command not found`

Pica CLI is not installed or not in PATH.

```bash
npm install -g @picahq/cli
```

If it's installed but not found, add the npm global bin to PATH:

```bash
export PATH="$(npm prefix -g)/bin:$PATH"
```

### MCP tools not available

The agent needs to be restarted after MCP installation. For Claude Desktop, quit and reopen. For Claude Code, start a new session. If MCP was never installed, run `pica init`.

### `No connections found`

No apps have been connected yet. Run `pica add gmail` (or any platform) to connect one.

### Connection shows `failed` or `degraded`

The OAuth token expired or was revoked. Reconnect:

```bash
pica add <platform>
```

Or reconnect from the dashboard at https://app.picaos.com/connections.

### `Invalid API key`

The key is wrong, expired, or not a valid Pica key. Get a new one at https://app.picaos.com/settings/api-keys. Keys start with `sk_live_` or `sk_test_`. Run `pica init` to update.

---

## Links

| What | Where |
|------|-------|
| Pica Dashboard | https://app.picaos.com |
| Get API key | https://app.picaos.com/settings/api-keys |
| Manage connections | https://app.picaos.com/connections |
| Browse integrations | https://app.picaos.com/tools |
| Documentation | https://docs.picaos.com |
