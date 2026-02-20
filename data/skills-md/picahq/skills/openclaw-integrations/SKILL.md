---
name: openclaw-integrations
description: Access 200+ third-party integrations (Gmail, Slack, HubSpot, Notion, Shopify, Linear, and more) from OpenClaw via your Pica account. Send emails, read messages, manage contacts, create tasks, and interact with any connected platform.
---

# OpenClaw Integrations (powered by Pica)

OpenClaw can interact with 200+ third-party platforms through Pica, a unified integration layer. Pica handles all OAuth, token refresh, rate limiting, and API normalization — you just connect your accounts once and OpenClaw can use them.

## Setup

Users need two things to use integrations:

1. **A Pica account** — Sign up free at https://app.picaos.com
2. **Connected platforms** — In the Pica dashboard, connect the services you want OpenClaw to access (Gmail, Slack, HubSpot, Notion, Shopify, etc.)

That's it. Once a platform is connected in Pica, OpenClaw can immediately interact with it. No API keys to manage, no OAuth flows to build — Pica handles everything.

## Links

- **Pica Dashboard** — https://app.picaos.com (manage connections and API keys)
- **Pica MCP Server** — https://github.com/picahq/mcp (the MCP server this skill uses under the hood)
- **Pica Docs** — https://docs.picaos.com
- **mcporter** — https://github.com/steipete/mcporter (the MCP client CLI that bridges OpenClaw to Pica)

---

## Implementation Guide (for developers setting up Pica in OpenClaw)

> **Critical:** OpenClaw does **NOT** support native MCP server configuration in `openclaw.json`. Keys like `mcp`, `agents.defaults.mcp`, or `mcp.servers` are **rejected** by OpenClaw's config validator and will crash the process with `Unrecognized key` errors. Instead, Pica integration works through **skills + mcporter CLI** — the agent calls mcporter as a shell command via its exec tool.

### Architecture

```
OpenClaw Agent
  └─ exec tool → shell command
       └─ mcporter call pica.<tool> --args '...' --config <path>
            └─ spawns Pica MCP server as child process (stdio)
                 └─ Pica API → Gmail, Slack, HubSpot, etc.
```

### Required Files

**1. `tools/package.json`** — mcporter + Pica MCP dependencies
```json
{
  "name": "pica-bridge",
  "version": "2.0.0",
  "type": "module",
  "dependencies": {
    "mcporter": "^0.7.3",
    "@picahq/mcp": "^2.0.4"
  }
}
```

**2. `tools/mcporter.json`** — MCP server registry (config for mcporter)
```json
{
  "mcpServers": {
    "pica": {
      "command": "node",
      "args": ["/home/node/tools/node_modules/@picahq/mcp/build/index.js"],
      "env": {
        "PICA_SECRET": "$env:PICA_SECRET"
      }
    }
  }
}
```

> **Important:** Use `node` with the absolute path to the installed module, not `npx`. Using `npx -y @picahq/mcp` causes slow cold-start downloads inside containers. The `$env:PICA_SECRET` syntax is mcporter's environment variable substitution — it reads from the container's environment at runtime.

**3. `openclaw.json`** — Must use `skills.load.extraDirs`, NOT `mcp`
```json
{
  "agents": {
    "defaults": {
      "workspace": "/home/node/workspace"
    }
  },
  "skills": {
    "load": {
      "extraDirs": ["/home/node/skills"]
    }
  }
}
```

**4. This SKILL.md** — Placed in the skills directory (e.g., `/home/node/skills/openclaw-integrations/SKILL.md`)

### Dockerfile Setup

```dockerfile
# Create directories
RUN mkdir -p /home/node/tools /home/node/skills

# Install mcporter + Pica MCP locally
COPY tools/package.json /home/node/tools/
RUN cd /home/node/tools && npm install

# mcporter config
COPY tools/mcporter.json /home/node/tools/config/mcporter.json

# Symlink mcporter to PATH so the agent can call it
RUN ln -s /home/node/tools/node_modules/.bin/mcporter /usr/local/bin/mcporter

# Copy skills
COPY skills/ /home/node/skills/
```

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `PICA_SECRET` | Yes | API key from https://app.picaos.com/settings/api-keys |
| `PICA_IDENTITY` | No | Scope connections to a user/team (e.g., `user_123`) |
| `PICA_IDENTITY_TYPE` | No | Identity type (e.g., `user`) |

### Common Pitfalls

1. **Do NOT add `mcp` to `openclaw.json`** — OpenClaw rejects it at any level (`root.mcp`, `agents.defaults.mcp`). The process exits with code 1 and the container restart-loops.
2. **Do NOT use `npx` in mcporter.json** — It downloads packages on every call inside containers. Use `node` with the absolute path to the pre-installed module.
3. **Do NOT install mcporter globally only** — The Pica MCP module needs to be locally installed so mcporter can find it at a known absolute path. Symlink the binary to PATH for convenience.
4. **Skills directory must exist before OpenClaw starts** — If `extraDirs` points to a missing path, OpenClaw may ignore it silently.

---

## What You Can Do

Examples of what's possible with connected platforms:

- **Gmail** — Read emails, send messages, manage drafts, organize labels
- **Slack** — Post messages, read channels, manage users
- **HubSpot** — List contacts, create deals, manage companies
- **Notion** — Create pages, query databases, update content
- **Shopify** — Manage orders, products, customers, inventory
- **Linear** — Create issues, update projects, track progress
- **Google Calendar** — List events, create meetings, manage schedules
- **GitHub** — Manage repos, issues, pull requests
- And 190+ more platforms

---

## How It Works (for the agent)

Integrations are accessed via `mcporter`, an MCP client CLI that connects to the Pica MCP server.

### mcporter Command Format

**IMPORTANT**: Always use `--args` with a JSON string for tool arguments. Do NOT use colon-delimited syntax (`key:value`) because global flags like `--json` get misinterpreted as tool arguments.

The correct format for every call is:

```bash
mcporter call pica.<tool_name> --args '<json>' --config /home/node/tools/config/mcporter.json
```

### Tools

| Tool | Purpose |
|------|---------|
| `list_pica_integrations` | See what platforms are connected |
| `search_pica_platform_actions` | Find available actions on a platform |
| `get_pica_action_knowledge` | Read docs for an action before using it |
| `execute_pica_action` | Run an action on a connected platform |

---

### Step 1: Check what's connected

```bash
mcporter call pica.list_pica_integrations --args '{}' --config /home/node/tools/config/mcporter.json
```

**Response structure:**
```json
{
  "connections": [
    { "platform": "gmail", "key": "test::gmail::default::abc123" },
    { "platform": "slack", "key": "test::slack::default::def456" }
  ],
  "available": [
    { "platform": "notion", "name": "Notion", "category": "Productivity" }
  ],
  "summary": { "connectedCount": 10, "availableCount": 205 }
}
```

- `connections[].key` is the `connectionKey` — you'll need it for step 4
- `connections[].platform` is the kebab-case platform name for steps 2-4
- `available` lists platforms that CAN be connected but aren't yet
- If the user's desired platform is in `available` (not `connections`), tell them to connect it at https://app.picaos.com

### Step 2: Find the right action

```bash
mcporter call pica.search_pica_platform_actions --args '{"platform":"gmail","query":"send email"}' --config /home/node/tools/config/mcporter.json
```

**Parameters:**
- `platform` (required): kebab-case platform name from step 1
- `query` (required): natural language description of what you want to do
- `agentType` (optional): `"execute"` when the user wants to perform an action, `"knowledge"` when they want info

**Response structure:**
```json
{
  "actions": [
    {
      "actionId": "conn_mod_def::GGXAjWkZO8U::uMc1LQIHTTKzeMm3rLL5gQ",
      "title": "Send Email",
      "method": "POST",
      "path": "/gmail/send-email"
    }
  ],
  "metadata": { "platform": "gmail", "query": "send email", "count": 5 }
}
```

- `actions[].actionId` is what you'll need for steps 3 and 4
- Up to 5 results are returned, ranked by relevance
- For Gmail, prefer actions with paths starting with `/gmail/` (these are "enhanced" actions with cleaner request/response formats) over raw API paths like `users/me/messages/...`

### Step 3: Read the action docs

```bash
mcporter call pica.get_pica_action_knowledge --args '{"actionId":"<id>","platform":"gmail"}' --config /home/node/tools/config/mcporter.json
```

**Parameters:**
- `actionId` (required): from step 2
- `platform` (required): kebab-case platform name

**You MUST call this before executing.** The response contains required parameters, optional parameters, request body schema, response format, and important caveats. Do not guess parameters — read the docs first.

### Step 4: Execute the action

```bash
mcporter call pica.execute_pica_action --args '{"platform":"gmail","actionId":"conn_mod_def::GGXAjWkZO8U::uMc1LQIHTTKzeMm3rLL5gQ","connectionKey":"test::gmail::default::abc123","data":{"to":"user@example.com","subject":"Hello","body":"Hi there"}}' --config /home/node/tools/config/mcporter.json
```

**Parameters:**
- `platform` (required): kebab-case platform name
- `actionId` (required): from step 2
- `connectionKey` (required): from step 1 (`connections[].key`)
- `data` (optional): request body object — contents depend on the action (see step 3)
- `queryParams` (optional): query string parameters object
- `pathVariables` (optional): URL path variable substitutions object
- `headers` (optional): additional HTTP headers object
- `isFormData` (optional): boolean, set true for multipart/form-data
- `isFormUrlEncoded` (optional): boolean, set true for URL-encoded form data

**All parameters go inside the `--args` JSON string**, including `data` as a nested object.

---

## Response Formatting

**Never dump raw JSON or tool output to the user.** Always parse and present a clean summary.

- **Listing integrations** — Show a clean list of connected platform names. Don't show connection keys or IDs.
  - Good: "You have **Gmail**, **Slack**, and **HubSpot** connected."
- **Search results** — Short numbered list with action titles only.
  - Good: "I found these Gmail actions:\n1. **Send Email**\n2. **List Emails**\n3. **Create Draft**"
- **Action docs** — Summarize required params in plain language.
  - Good: "To send an email, I need: recipient, subject, and body. I can also add CC/BCC."
- **Execution results** — One sentence describing what happened.
  - Good: "Done — email sent to alice@example.com."
- **Errors** — Explain in plain language and suggest a fix. No stack traces.

## Guidelines

- When a user first asks about integrations, call `list_pica_integrations` to show what's available
- If asked "what can you do with X?", search for actions on that platform and summarize the capabilities
- For Gmail, prefer the enhanced actions (paths starting with `/gmail/`) over raw API actions — they have simpler parameters and return decoded, human-readable data
- Always confirm destructive actions (delete, batch operations) with the user before executing
- Never expose connection keys, API secrets, or internal IDs in responses
- If something fails, explain clearly and suggest next steps (e.g., "That platform isn't connected yet — you can add it at https://app.picaos.com")
