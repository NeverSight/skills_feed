---
name: aident-skill
description: |
  Access Aident's 1000+ integrations and automation platform.
  Prefer MCP tools if available; otherwise use HTTPS API fallback.
author: Aident
homepage: https://aident.ai
repository: https://github.com/aident-ai/aident-skill
tags:
  - automation
  - integrations
  - skills
  - workflows
  - mcp
categories:
  - productivity
  - development
  - automation
compatibility: MCP-capable clients (preferred) and skill-capable agents (REST fallback)
version: 0.1.0
license: MIT
---

# Aident (Dual-mode: MCP preferred, HTTPS fallback)

Access 1k+ integrations (Gmail, Slack, GitHub, Firecrawl, Exa, etc.), create and manage automation playbooks, discover templates, and monitor all running automations from a command center dashboard.

## What this skill does

- Search and execute 1000+ integration skills (email, messaging, project management, web scraping, etc.)
- Generate, execute, and manage automation playbooks from natural language
- Browse and instantiate pre-built playbook templates
- Monitor active automations and track execution results
- Connect new third-party integrations on-the-fly

It supports two execution modes:
1. **MCP mode (preferred)**: use MCP tools from the `aident` server.
2. **REST API fallback mode**: call `POST /api/mcp/rest` with `{ tool, arguments }` when MCP tools are unavailable.

## Decide which mode to use

Use **MCP mode** if the client has MCP tools available named like:
- `skill_search`, `skill_list`, `skill_get_info`, `skill_execute`
- `playbook_list`, `playbook_generate`, `playbook_execute`
- `template_search`, `template_list`, `template_instantiate`
- `integration_status`, `integration_connect`
- `dashboard_active_playbooks`, `execution_list`

Otherwise use **REST API fallback**.

### MCP mode (preferred)

**When:** The client is connected to the Aident MCP server and can call tools like `skill_search`, `playbook_list`, etc.

**Setup:** See [references/mcp.md](references/mcp.md) for client configuration.

**Workflow:**
1. Collect required inputs from the user.
2. Call the relevant tool(s) directly.
3. Handle errors:
   - If auth error: call `auth_logout`, delete `~/.aident/credentials.json`, then reconnect via OOB flow.
   - If missing integration: call `integration_connect` to connect it, then retry.
4. Return results in a clean format.

### REST API fallback mode

**When:** No Aident MCP tools are available in the client.

#### Credentials file

Authentication is persisted in `~/.aident/credentials.json` so tokens survive across sessions:

```json
{
  "base_url": "https://app.aident.ai",
  "client_id": "<oauth_client_id>",
  "access_token": "<bearer_token>",
  "refresh_token": "<refresh_token>",
  "expires_at": "<ISO8601_timestamp>"
}
```

#### Step 1: Load credentials

1. Check if `AIDENT_TOKEN` env var is set. If yes, use it directly as the Bearer token and skip to **Step 3**. (This is an advanced override -- do not ask the user for it.)
2. Read `~/.aident/credentials.json`. If the file exists and has a non-empty `access_token`:
   - If `expires_at` is in the past and `refresh_token` is present, go to **Step 2b** (refresh).
   - Otherwise skip to **Step 3**.
3. If the file does not exist or has no `access_token`, go to **Step 2a** (first-time setup).

#### Step 2a: First-time authentication (OOB flow)

Run these steps automatically -- never ask the user to provide a token manually.

1. Resolve the base URL: use `AIDENT_BASE_URL` env if set, otherwise `https://app.aident.ai`.
2. Create the credentials directory if it does not exist: `mkdir -p ~/.aident`
3. Register an OAuth client:
   ```bash
   curl -s -X POST $BASE_URL/api/mcp/oauth/register \
     -H "Content-Type: application/json" \
     -d '{
       "redirect_uris": ["'"$BASE_URL"'/mcp/oob"],
       "client_name": "aident-skill-cli",
       "grant_types": ["authorization_code", "refresh_token"],
       "response_types": ["code"],
       "token_endpoint_auth_method": "none"
     }'
   ```
   Save `client_id` from the JSON response.
4. Open the authorization URL in the user's browser:
   ```
   $BASE_URL/api/mcp/oauth/authorize?response_type=code&client_id=$CLIENT_ID&redirect_uri=$BASE_URL/mcp/oob
   ```
   Use `open` (macOS), `xdg-open` (Linux), or `start` (Windows) to launch the browser.
5. Tell the user: "I've opened Aident in your browser. Please log in and click **Approve**, then paste the access token shown on screen back here."
6. When the user pastes the token, write `~/.aident/credentials.json`:
   ```json
   {
     "base_url": "$BASE_URL",
     "client_id": "$CLIENT_ID",
     "access_token": "<pasted_token>",
     "refresh_token": "",
     "expires_at": ""
   }
   ```
7. Proceed to **Step 3**.

#### Step 2b: Refresh an expired token

```bash
curl -s -X POST $BASE_URL/api/mcp/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=refresh_token&client_id=$CLIENT_ID&refresh_token=$REFRESH_TOKEN"
```

If refresh succeeds, update `access_token`, `refresh_token`, and `expires_at` in `~/.aident/credentials.json`. If refresh fails (e.g. token revoked or expired), delete the credentials file and go back to **Step 2a**.

#### Step 3: Call tools

Use the `access_token` from the credentials file (or `AIDENT_TOKEN` env) and `base_url` (or `AIDENT_BASE_URL` env, default `https://app.aident.ai`):

```bash
curl -s -X POST $BASE_URL/api/mcp/rest \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -d '{ "tool": "<tool_name>", "arguments": { ... } }'
```

Parse the `result` field from the JSON response.

**On HTTP 401:** The token has expired. Go to **Step 2b** to refresh, then retry the request. If refresh also fails, go to **Step 2a**.

## Available Tools (22)

### Auth (2)
- **auth_status** -- Check authentication status (always accessible)
- **auth_logout** -- Revoke access token and log out. After calling this, delete `~/.aident/credentials.json` so the next request triggers a fresh OOB flow.

### Skills (4)
- **skill_search** -- Search skills by query, tags, or type using hybrid search
- **skill_list** -- List available skills with pagination
- **skill_get_info** -- Get detailed metadata including input/output schemas and required integrations
- **skill_execute** -- Execute a skill with validated input; prompts for missing integrations

### Integrations (2)
- **integration_status** -- Check which integrations are connected
- **integration_connect** -- Initiate connection to a third-party service via OAuth

### Playbooks (6)
- **playbook_list** -- List your playbooks with status and trigger info
- **playbook_get_info** -- Get playbook details including content and trigger configuration
- **playbook_generate** -- Generate a new playbook from a natural language description
- **playbook_execute** -- Execute a playbook (returns execution ID for tracking), or send a follow-up message to an existing execution via `executionSessionId`
- **playbook_update_trigger** -- Enable or disable playbook triggers
- **playbook_execution_history** -- Get execution history for a specific playbook

### Templates (4)
- **template_search** -- Search for playbook templates by keyword or category
- **template_list** -- List available templates with optional category filtering
- **template_get_info** -- Get detailed template information
- **template_instantiate** -- Create a new playbook from a template

### Dashboard (4)
- **dashboard_active_playbooks** -- List playbooks with active triggers or running executions
- **execution_get_details** -- Get execution details including status and messages
- **execution_list** -- List recent executions across all playbooks
- **execution_get_messages** -- Get simplified chat messages for progress polling

## Safety & privacy

- Never request secrets in plain text if the platform has secret storage.
- If the user pastes a token, suggest they rotate it and store it securely.
- Only send necessary fields to the service.
- All tokens are scoped -- request only the permissions you need.

## Examples

### Example 1: MCP mode

User: "Find skills for sending emails and send a meeting summary to team@example.com"

Assistant workflow:
1. Call `skill_search` with `{ "query": "send email" }`
2. Review results, pick best match (e.g. `gmail_send_email`)
3. Call `skill_execute` with the skill and input
4. Present confirmation to user

### Example 2: REST fallback, first-time user

User: "Send an email to team@example.com with today's meeting notes"

Assistant workflow (no `~/.aident/credentials.json` found):
1. Register OAuth client with the Aident server
2. Open browser to authorization page
3. Tell user: "I've opened Aident in your browser. Please log in and click Approve, then paste the access token shown on screen back here."
4. User pastes token
5. Save credentials to `~/.aident/credentials.json`
6. Call `skill_search` for email skills via REST
7. Call `skill_execute` to send the email via REST
8. Confirm to user

### Example 3: REST fallback, returning user

User: "List my playbooks"

Assistant workflow (reads existing `~/.aident/credentials.json`):
1. Load `access_token` and `base_url` from credentials file
2. POST to `$BASE_URL/api/mcp/rest` with `{ "tool": "playbook_list", "arguments": {} }`
3. Parse the `result` field from response
4. Present playbook list to user

## Security

- **OAuth 2.1 + PKCE**: Industry-standard authentication with automatic token refresh
- **Scoped Access**: Category-based permissions (skills, integrations, playbooks, templates, dashboard)
- **Revocable**: Revoke access anytime from Settings
- **Integration-Aware**: Missing integrations prompt for connection rather than failing silently

## Documentation

- Setup Guide: https://docs.aident.ai/documentation/mcp-server-setup
- API Reference: https://docs.aident.ai/documentation/mcp-api-reference
- Troubleshooting: [references/troubleshooting.md](references/troubleshooting.md)

## Support

- Email: help@aident.ai
- Discord: https://discord.gg/hxtEYHuW26
- Documentation: https://docs.aident.ai

## License

MIT License - See LICENSE file for details
