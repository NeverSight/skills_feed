---
name: connect-to-nango-mcp
description: Connect agents to external platforms (HubSpot, Salesforce, etc.) via Nango using header authentication.
version: 8.0.0
author: agent-skills-workbench
mcp-servers: ["nango"]
tags: [nango, mcp, integration, hubspot, salesforce, portable]
---

# Nango MCP Integration Skill

This skill enables agents to connect to third-party SaaS platforms (HubSpot, Salesforce, etc.) through Nango's proxy and MCP server.

## MCP Server Requirements

This skill requires the **Nango** MCP server.

**Connection Details:**
- **URL**: `https://api.nango.dev/mcp`
- **Transport**: HTTP

**Authentication:**
The Nango MCP server uses header-based authentication at connection time.

**Required Headers:**
- `Authorization`: `Bearer <NANGO_SECRET_KEY>`
- `connection-id`: `<connectionId from Step 3>`
- `provider-config-key`: `<provider name>`

**Available Tools (vary by provider):**
- HubSpot: `whoami`, `list_contacts`, `create_contact`, `query`
- Salesforce: `query`, `create_record`, `whoami`

## Prerequisites

### Credentials
- `NANGO_SECRET_KEY`: Your Nango secret key from nango.dev.
- `NANGO_DEFAULT_USER_ID`: The end-user identifier for the connection.

### Runtime
- Node.js 18+ (for bundled scripts using built-in fetch)

---

## Workflow

### Phase 1: Check Connection Status
First, determine if the Nango MCP server is already connected. If Nango-specific tools (like `whoami` or `list_contacts`) are already available in your environment, you can skip to normal usage.

### Phase 2: Handle Authentication
If tools are not available, you must obtain a `connectionId`.

1. **Identify Provider**: Determine which provider the user wants to connect to (e.g., `hubspot`, `salesforce`) by checking the original request or current skill context. Only ask the user if the provider is not mentioned and cannot be inferred.
2. **Get Secret Key**: Attempt to retrieve the `NANGO_SECRET_KEY` from the environment variables (e.g., via platform tools or direct environment access). Do NOT ask the user for this key if it is already available.
3. **Run the authentication script**: Execute `scripts/check-auth.js` passing the inferred provider and the retrieved secret key.
   ```bash
   node scripts/check-auth.js <provider> <secret_key>
   ```
4. **Handle Response**:
   - **Success**: The script returns a `connectionId`. Proceed immediately to configure the MCP server.
   - **Needs Auth**: The script returns an `authUrl`. Present this URL to the user and wait for them to confirm completion. Once confirmed, re-run the script to get the `connectionId`.
   - **Error**: Report the error to the user.

### Phase 3: Configure and Use MCP Server
Once you have the `connectionId`, **IMMEDIATELY PROCEED** with the following steps without pausing:

**Step 3.1 - Provision Authentication Headers:**
Configure the Nango MCP server with these three required headers (use your platform's credential storage mechanism):
- **Server identifier**: `nango-mcp-server` (or similar)
- **Server URL**: `https://api.nango.dev/mcp`
- **Headers to configure** (provision all three):
  1. `Authorization`: `Bearer <NANGO_SECRET_KEY>`
  2. `connection-id`: `<connectionId>` (from Phase 2)
  3. `provider-config-key`: `<provider>` (e.g., "hubspot", "salesforce")

*Platform-specific notes:*
- Some platforms may require separate calls to provision each header
- Others may accept all headers in a single configuration call
- Use whatever credential/header provisioning tool your platform provides

**Step 3.2 - Connect to MCP Server:**
Establish connection to the Nango MCP server. The server will validate your headers and return available tools based on the provider.

*For agents that support programmatic MCP connections and use the MCP SDK:* Use the reference script `scripts/connect-direct.js` which demonstrates the connection pattern using the MCP SDK. See the "scripts/connect-direct.js" section below for details.

*For agents that suppport programmatic MCP connections but do not use the MCP SDK: They can use the following pattern:*

Regardless of vendor, an MCP HTTP server will:

Accept POST requests with JSON-RPC 2.0

Stream responses as text/event-stream

Support standard MCP methods:

initialize (sometimes implicit)
tools/list
tools/call
resources/list (optional)
prompts/list (optional)

That’s all we rely on.

1️⃣ Open a generic MCP stream

This is the universal way to connect.

```bash
curl -N http://MCP_SERVER_URL \
  -H "Accept: text/event-stream" \
  -H "Content-Type: application/json"
```

If the server is alive, you’ll usually see something like:

event: ready
data: {"jsonrpc":"2.0","method":"server/ready"}

(Some servers skip ready; that’s okay.)

2️⃣ (Optional) Initialize the client

Some MCP servers expect an explicit initialize.

```bash
curl -N http://MCP_SERVER_URL \
  -H "Accept: text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "init-1",
    "method": "initialize",
    "params": {
      "clientInfo": {
        "name": "curl-mcp-client",
        "version": "0.1"
      }
    }
  }'
```

Typical response:

```json
{
  "jsonrpc":"2.0",
  "id":"init-1",
  "result":{
    "capabilities":{
      "tools":true
    }
  }
}
```

3️⃣ List tools (universally supported)
```bash
curl -N http://MCP_SERVER_URL \
  -H "Accept: text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "tools-1",
    "method": "tools/list"
  }'
```

Response:
```json
{
  "jsonrpc":"2.0",
  "id":"tools-1",
  "result":{
    "tools":[
      {
        "name":"example.search",
        "description":"Search something",
        "inputSchema":{...}
      }
    ]
  }
}
```
4️⃣ Call a tool (generic invocation)
```bash
curl -N http://MCP_SERVER_URL \
  -H "Accept: text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": "call-1",
    "method": "tools/call",
    "params": {
      "name": "example.search",
      "arguments": {
        "query": "hello world"
      }
    }
  }'
```

Streamed result:
```json
{
  "jsonrpc":"2.0",
  "id":"call-1",
  "result":{
    "content":[
      { "type":"text", "text":"Result here" }
    ]
  }
}
```
5️⃣ Handling streaming correctly (important)

MCP servers may emit:
partial messages
multiple content chunks
a final done event

Always:
curl -N

And treat each data: line as incremental.

6️⃣ Minimal MCP client mental model

You only need to implement:

POST JSON-RPC
↓
Read SSE lines
↓
Parse JSON
↓
Match `id`
↓
Handle result/error

7️⃣ One-liner MCP request template

Save this mentally:
```bash
curl -N MCP_URL \
  -H "Accept: text/event-stream" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc":"2.0",
    "id":"X",
    "method":"METHOD",
    "params":{...}
  }'
```
If a server requires auth, headers are just decoration on top of this.

**Step 3.3 - List Available Tools:**
Query the MCP server to discover which tools are now available (e.g., `whoami`, `list_contacts`, `query`, etc.). This confirms authentication succeeded.

**Step 3.4 - Execute User's Request:**
Use the appropriate tool(s) to fulfill the user's original request immediately.

**[CRITICAL - DO NOT STOP]**:
- Execute steps 3.1 through 3.4 **in sequence without pausing**
- Do NOT ask for permission between steps
- Do NOT report "I've configured the headers" and stop
- The user should see the final result (e.g., the HubSpot data), not intermediate status messages
- If authentication fails, report the error with details

---

## Bundled Scripts

### scripts/check-auth.js
Checks Nango authentication status and initiates the authentication flow if needed.

**Usage:**
`node check-auth.js <provider> <secret_key>`

**Output:** JSON with `status` (success, needs_auth, error) and relevant data.

### scripts/config-helper.js
Utility to help generate configuration snippets for various agent platforms.

### scripts/connect-direct.js
Reference script showing how to programmatically connect to the Nango MCP server in a one-off manner.

**When to Use:**
- For agents that support creating MCP client connections programmatically using the MCP SDK
- When you need a direct connection without configuration file setup
- As a reference implementation for custom agent integrations
- When the agent doesn't know how to add MCP servers on the fly via configuration

**Requirements:**
- `@modelcontextprotocol/sdk` package installed
- Node.js 18+
- Environment variables from authentication step

**Usage:**
```bash
# Set required environment variables
export NANGO_SECRET_KEY="your-secret-key"
export CONNECTION_ID="connection-id-from-check-auth"
export INTEGRATION_ID="hubspot"  # or other provider

# Run the script
node connect-direct.js
```

**Environment Variables:**
- `NANGO_SECRET_KEY` or `NANGO_SECRET_KEY_DEV` (required): Your Nango secret key
- `CONNECTION_ID` (required): The connection ID from OAuth (obtain via `check-auth.js`)
- `INTEGRATION_ID` or `PROVIDER_CONFIG_KEY` (required): Provider name (e.g., 'hubspot', 'salesforce')
- `NANGO_MCP_URL` (optional): MCP server URL (defaults to 'https://api.nango.dev/mcp')

**Output:** JSON to stdout with connection status and available tools

**Note:** This is a reference implementation using ES modules. Agents should adapt this pattern to their specific runtime environment and requirements. The script demonstrates the core connection pattern that can be integrated into agent workflows.

---

## Troubleshooting

- **Authentication failed**: Verify the `NANGO_SECRET_KEY` and ensure the provider is configured in your Nango account.
- **Tools not appearing**: Ensure the headers are correctly sent during the MCP connection handshake.
- **Connection-id not found**: The user may need to complete the authentication flow via the provided `authUrl`.
