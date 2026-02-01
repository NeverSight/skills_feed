---
name: hubspot-whoami-nango
description: Find out who you are in HubSpot using Nango.
version: 2.0.0
author: agent-skills-workbench
mcp-servers: ["nango"]
depends-on: ["connect-to-nango-mcp"]
tags: [hubspot, nango, identity, portable]
---

# HubSpot WhoAmI via Nango

This skill identifies the current authenticated HubSpot user using the Nango integration.

## MCP Server Requirements

This skill depends on the **Nango** MCP server being correctly configured and connected.

**Required Tool:**
- `whoami`: Returns the authenticated HubSpot user's ID and email address.

**Connection Requirements:**
See the `connect-to-nango-mcp` skill for details on how to configure the Nango MCP server with the necessary authentication headers.

---

## Workflow

### Step 1: Ensure Nango is Connected
Verify if the Nango MCP server is connected and the `whoami` tool is available. If not, follow the `connect-to-nango-mcp` skill workflow to establish a connection for the **hubspot** provider. Identify the provider as `hubspot` immediately.

### Step 2: Call the whoami Tool
Execute the `whoami` tool provided by the Nango MCP server. This tool requires no arguments if the connection headers were correctly set during MCP initialization.

### Step 3: Present the Identity
Display the returned user information (ID and email) to the user in a friendly format.

---

## Example Output

```text
HubSpot Identity:
- User ID: 3768092
- Email: email@example.com
```

## Error Handling

- **Tool Not Found**: Ensure the Nango MCP server is connected and the provider is `hubspot`.
- **Authentication Error**: Refer to the troubleshooting section of the `connect-to-nango-mcp` skill.
- **Provider Mismatch**: Ensure you are using the `hubspot` provider config key when connecting to Nango.
