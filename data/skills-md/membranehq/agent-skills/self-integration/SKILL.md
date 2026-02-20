---
name: self-integration
description: Connect to any external app and perform actions on it. Use when the user wants to interact with external services like Slack, Linear, HubSpot, Salesforce, Jira, GitHub, Google Sheets, or any other app — send messages, create tasks, sync data, manage contacts, or perform any API operation.
license: MIT
metadata:
  author: Membrane Inc
  version: '1.2.0'
  homepage: https://getmembrane.com
  openclaw:
    requires:
      env:
        - MEMBRANE_TOKEN
    primaryEnv: MEMBRANE_TOKEN
    homepage: https://getmembrane.com
---

# Self-Integration

Connect to any external app and perform actions on it. Uses the [Membrane](https://getmembrane.com) CLI.

## Authentication

Authenticate with the Membrane CLI:

```bash
npx @membranehq/cli login --tenant
```

Alternatively, you can install the membrane CLI globally (`npm i -g @membranehq/cli@latest`) and use `membrane login --tenant` instead.

Always use `--tenant` to get a tenant-scoped token — this authenticates on behalf of a specific tenant (workspace + customer) in Membrane, so you don't need to pass `--workspaceKey` and `--tenantKey` on every subsequent command.

This will either open a browser for authentication or print an authorization URL to the console, depending on whether interactive mode is available. The user authenticates in Membrane, then selects a workspace and tenant (user inside workspace).

When login process is completed, the credentials are stored locally in `~/.membrane/credentials.json` and used in subsequent commands automatically.

### Non-interactive Authentication

If interactive browser login is not possible (e.g. remote/headless environment) the `membrane login` command will print an authorization URL to the terminal. The user can then open the URL in their browser and complete the login process.

If this is the case, ask the user to enter the code they see in the browser after completing the login process.

When user enters the code, complete the login process with:

```bash
npx @membranehq/cli login complete <code>
```

All commands below use `npx @membranehq/cli` (or just `membrane` if installed globally). Add `--json` to any command for machine-readable JSON output to stdout. Command without `--json` flag will print the result in a human-readable (and often shorter) format.

## Workflow

### Step 1: Get a Connection

A connection is an authenticated link to an external app (e.g. a user's Slack workspace, a HubSpot account). You need one before you can run actions.

#### 1a. Check for existing connections

```bash
npx @membranehq/cli connection list --json
```

Look for a connection matching the target app. Key fields: `id`, `name`, `connectorId`, `disconnected`.

If no connection is found, go to step 1b to find a connector.

If a connection is disconnected (`disconnected` is `true`), you can reconnect it using `connect --connectionId <existingId>` (step 1d) instead of creating a new connection from scratch.

If a matching connection exists and `disconnected` is `false`, skip to **Step 2**.

#### 1b. Find a connector

A connector is a pre-built adapter for an external app. Search by app name:

```bash
npx @membranehq/cli search slack --elementType connector --json
```

Look for results with `elementType: "Connector"`. Use `element.id` as `connectorId` in step 1d.

If nothing is found, go to step 1c to build a connector.

#### 1c. Build a connector (if none exists)

Create a Membrane Agent session to build a connector:

```bash
npx @membranehq/cli agent-session create --agent connection-building --message "Build a connector for Slack (https://slack.com)" --json
```

Adjust the message to describe the actual app you need. 

Poll until `state` is `"idle"` or `status` is `"completed"`:

```bash
npx @membranehq/cli agent-session get <sessionId> --wait --json
```

This command will wait until session is completed or up to a `--timeout` seconds and return the current state of the session.
Keep polling until session is in `idle` state - which means the agent is done with your request.

Key response fields:
- `state`: `busy` (still working) or `idle` (done with current request)
- `status`: `queued`, `starting`, `running`, `completed`, `failed`, or `cancelled`
- `summary`: description of what was done (available when idle)

You can send follow-up instructions or abort:

```bash
npx @membranehq/cli agent-session send <sessionId> --message "Also add OAuth2 support" --json
npx @membranehq/cli agent-session abort <sessionId> --json
```

After the connector is built get its id from the session summary or search for it again (step 1b) if it's not in the summary.

#### 1d. Create a connection

Use the following command to create a connection:

```bash
npx @membranehq/cli connect --connectorId <connectorId>
```

In interactive mode, this will open the browser, wait for the user to complete authentication, and print the connection ID on success.

If interactive mode is not available, add `--non-interactive` to print the URL instead of opening the browser. This will create a connection request and output a URL to the terminal. You need to ask the user to follow this URL to complete the connection process.

It will also output the connection request ID that you can then use to get the status of the connection request and the connection Id on success.

Then poll until the user completes authentication:

```bash
npx @membranehq/cli connection-request get abc123 --json
```

- `status: "pending"` — user hasn't completed yet, poll again.
- `status: "success"` — done. Use `resultConnectionId` as the connection ID going forward.
- `status: "error"` — failed. Check `resultError` for details.
- `status: "cancelled"` — user cancelled the connection flow.

### Step 2: Get an Action

An action is an operation you can perform on a connected app (e.g. "Create task", "Send message", "List contacts").

#### 2a. Search for actions

Search using a natural language description of what you want to do:

```bash
npx @membranehq/cli action list --connectionId abc123 --intent "send a message" --limit 10 --json
```

You should always search for actions in the context of a specific connection.

Each result includes `id`, `name`, `description`, `inputSchema` (what parameters the action accepts), and `outputSchema` (what it returns).

If no suitable action exists, go to step 2b.

#### 2b. Build an action (if none exists)

Use Membrane Agent. ALWAYS include the connection ID in the message:

```bash
npx @membranehq/cli agent-session create --agent action-building --message "Create an action to send a message in a channel for connection abc123" --json
```

Adjust the message to describe the actual action you need. Poll for completion the same way as step 1c. After the action is built, search for it again (step 2a).

### Step 3: Run an Action

Execute the action using the action ID from step 2 and the connection ID from step 1:

```bash
npx @membranehq/cli action run <actionId> --connectionId abc123 --input '{"channel": "#general", "text": "Hello!"}' --json
```

Provide `--input` matching the action's `inputSchema`.

The result is in the `output` field of the response.

## CLI Reference

All commands support `--json` for structured JSON output to stdout. Add `--workspaceKey <key>` and `--tenantKey <key>` to override project defaults.

### connection

```bash
npx @membranehq/cli connection list [--json]                # List all connections
npx @membranehq/cli connection get <id> [--json]           # Get a connection by ID
```

### connect (interactive)

```bash
npx @membranehq/cli connect --connectorId <id>                    # Create connection via browser OAuth
```

Opens a browser for the user to authenticate, waits for completion, and prints the result. Use `--non-interactive` to print the URL instead of opening the browser.

### connection-request

```bash
npx @membranehq/cli connection-request create [options] [--json]   # Create connection request
npx @membranehq/cli connection-request get <requestId> [--json]    # Check request status
```

Options for `create`: `--connectorId <id>`, `--integrationId <id>`, `--integrationKey <key>`, `--connectionId <id>` (reconnect), `--name <name>`

### action

```bash
npx @membranehq/cli action list [--connectionId <id>] [--intent <text>] [--limit <n>] [--json]   # List/search actions
npx @membranehq/cli action run <actionId> --connectionId <id> [--input <json>] [--json]      # Run an action
```

### search

```bash
npx @membranehq/cli search <query> [--elementType <type>] [--limit <n>] [--json]   # Search connectors, integrations, etc.
```

### agent-session

```bash
npx @membranehq/cli agent-session create --agent <agentName> --message <text> [--json]           # Create session
npx @membranehq/cli agent-session list [--json]                              # List sessions
npx @membranehq/cli agent-session get <id> [--wait] [--json]                 # Get status (--wait for long-poll)
npx @membranehq/cli agent-session send <id> --message <text> [--json]        # Send follow-up message
npx @membranehq/cli agent-session abort <id> [--json]                        # Abort session
npx @membranehq/cli agent-session messages <id> [--json]                     # Get session messages
```

## Fallback: Raw API

If the CLI is not available, you can make direct API requests.

Base URL: `https://api.getmembrane.com`
Auth header: `Authorization: Bearer $MEMBRANE_TOKEN`

Get the API token from the [Membrane dashboard](https://console.getmembrane.com).

| CLI Command                                                  | API Equivalent                                                      |
| ------------------------------------------------------------ | ------------------------------------------------------------------- |
| `connection list --json`                                     | `GET /connections`                                                  |
| `connection get <id> --json`                                 | `GET /connections/:id`                                              |
| `search <q> --json`                                          | `GET /search?q=<q>`                                                 |
| `connection-request create --connectorId <id> --json`        | `POST /connection-requests` with `{"connectorId": "<id>"}`          |
| `connection-request get <id> --json`                         | `GET /connection-requests/:id`                                      |
| `action list --connectionId <id> --intent <text> --json`     | `GET /actions?connectionId=<id>&intent=<text>`                      |
| `action run <id> --connectionId <cid> --input <json> --json` | `POST /actions/:id/run?connectionId=<cid>` with `{"input": <json>}` |
| `agent-session create --message <text> --json`               | `POST /agent/sessions` with `{"prompt": "<text>"}`                  |
| `agent-session get <id> --wait --json`                       | `GET /agent/sessions/:id?wait=true`                                 |
| `agent-session send <id> --message <text> --json`            | `POST /agent/sessions/:id/message` with `{"input": "<text>"}`       |
| `agent-session abort <id> --json`                            | `POST /agent/sessions/:id/interrupt`                                |

## External Endpoints

All requests go to the Membrane API. No other external services are contacted directly by this skill.

| Endpoint                                             | Data Sent                                                             |
| ---------------------------------------------------- | --------------------------------------------------------------------- |
| `https://api.getmembrane.com/*` | Auth credentials, connection parameters, action inputs, agent prompts |

## Security & Privacy

- All data is sent to the Membrane API over HTTPS.
- CLI credentials are stored locally in `~/.membrane/` with restricted file permissions.
- Connection authentication (OAuth, API keys) is handled by Membrane — credentials for external apps are stored by the Membrane service, not locally.
- Action inputs and outputs pass through the Membrane API to the connected external app.

By using this skill, data is sent to [Membrane](https://getmembrane.com). Only install if you trust Membrane with access to your connected apps.