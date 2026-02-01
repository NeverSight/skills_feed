---
name: agent-hoppscotch
description: CLI tool for managing Hoppscotch API documentation. Use when user asks to document API, add API to Hoppscotch, update API docs, or manage API collections.
allowed-tools: Bash(agent-hoppscotch:*), AskUserQuestion
---

# Hoppscotch API Documentation with agent-hoppscotch

## Core workflow

1. **Check config**: `agent-hoppscotch auth status`
2. **If not configured**, ask user for:
   - Hoppscotch GraphQL endpoint URL
   - Session cookie (from browser DevTools → Application → Cookies)
3. **Configure**: Set endpoint, cookie, and defaults
4. **Work**: Create/update collections and requests

## Configuration (only if status shows "Not configured")

```bash
# Step 1: Set endpoint (ask user for their Hoppscotch URL)
agent-hoppscotch auth set-endpoint "<user_provided_url>/graphql"

# Step 2: Set cookie (ask user to copy from browser)
agent-hoppscotch auth set-cookie "<cookie_string>"

# Step 3: List teams and ask user to select
agent-hoppscotch team list
agent-hoppscotch auth set-default --team <selected_team_id>

# Step 4: List collections and ask user to select default
agent-hoppscotch collection list
agent-hoppscotch auth set-default --collection <selected_collection_id>
```

## Commands

### Auth
```bash
agent-hoppscotch auth status                        # Show configuration
agent-hoppscotch auth set-endpoint "<url>"          # Set GraphQL endpoint
agent-hoppscotch auth set-cookie "<cookie>"         # Set session cookie
agent-hoppscotch auth set-default --team <id> --collection <id>  # Set defaults
agent-hoppscotch auth clear                         # Remove all credentials
```

### Team
```bash
agent-hoppscotch team list                          # List all teams
agent-hoppscotch team find "<term>"                 # Search by name
agent-hoppscotch team get <id>                      # Get team details
```

### Collection
```bash
agent-hoppscotch collection list                    # List root collections (uses default team)
agent-hoppscotch collection list --team <id>        # List for specific team
agent-hoppscotch collection list --parent <id>      # List child collections
agent-hoppscotch collection find "<term>"           # Search (includes children)
agent-hoppscotch collection get <id>                # Get collection details
agent-hoppscotch collection create --title "..." [--team <id> | --parent <id>]
agent-hoppscotch collection delete <id>
agent-hoppscotch collection export --team <id>      # Export as JSON
```

### Request
```bash
agent-hoppscotch request list                       # List (uses default collection)
agent-hoppscotch request list --collection <id>     # List for specific collection
agent-hoppscotch request find "<term>"              # Search by title
agent-hoppscotch request get <id>                   # Get request details
agent-hoppscotch request create \
  --title "..." --method GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS \
  --url "..." [--collection <id>] [--team <id>] \
  [--headers '<json or array>'] [--body '<json>'] [--body-type application/json|multipart/form-data|application/x-www-form-urlencoded|text/plain|none] \
  [--form '[{"key":"k","value":"v","isFile":false}]'] \
  [--params '<json>'] [--auth-type bearer|basic|api-key|oauth2|inherit|none] \
  [--auth-token "..."] [--auth-username "..."] [--auth-password "..."] \
  [--auth-key "..."] [--auth-value "..."] [--auth-add-to header|query] \
  [--oauth-grant-type client_credentials|authorization_code] [--oauth-token-url "..."] \
  [--oauth-client-id "..."] [--oauth-client-secret "..."] [--oauth-scope "..."] \
  [--pre-request-script '<js>'] [--pre-request-script-file <path>] \
  [--test-script '<js>'] [--test-script-file <path>] [--variables '<json>'] \
  [--description '<text>'] [--description-file <path>] [--validate-body]
agent-hoppscotch request update <id> [--title] [--method] [--url] [--headers] [--body] [--body-type] [--form] \
  [--auth-type] [--auth-token] [--auth-username] [--auth-password] \
  [--auth-key] [--auth-value] [--auth-add-to] \
  [--oauth-grant-type] [--oauth-token-url] [--oauth-client-id] [--oauth-client-secret] [--oauth-scope] \
  [--pre-request-script '<js>'] [--pre-request-script-file <path>] \
  [--test-script '<js>'] [--test-script-file <path>] [--variables '<json>'] \
  [--description '<text>'] [--description-file <path>] [--validate-body]
agent-hoppscotch request delete <id>
agent-hoppscotch request move <id> --to <collectionId>
agent-hoppscotch request run <id> [--var key=value] [--body-only] [--status-only] [--include-headers] [--verbose]
```

### GraphQL
```bash
agent-hoppscotch graphql list --collection <id>    # List GraphQL requests
agent-hoppscotch graphql get <id>                  # Get request details
agent-hoppscotch graphql create \
  --title "..." --url "{{baseUrl}}/graphql" \
  --query 'query { users { id name } }' [--query-file <path>] \
  [--variables '<json>'] [--variables-file <path>] [--headers '<json>']
agent-hoppscotch graphql update <id> [--title] [--url] [--query] [--query-file] [--variables] [--variables-file] [--headers]
agent-hoppscotch graphql delete <id>
```

### Realtime (WebSocket, SSE, Socket.IO, MQTT)
```bash
agent-hoppscotch realtime list --collection <id> [--type websocket|sse|socketio|mqtt]
agent-hoppscotch realtime get <id>
agent-hoppscotch realtime create --type websocket --title "..." --url "wss://..." [--protocols '["proto"]'] [--headers '<json>']
agent-hoppscotch realtime create --type sse --title "..." --url "https://..." [--headers '<json>']
agent-hoppscotch realtime create --type socketio --title "..." --url "https://..." [--path '/socket.io'] [--version '4']
agent-hoppscotch realtime create --type mqtt --title "..." --url "mqtt://..." [--topic '...'] [--qos 0|1|2] [--client-id '...']
agent-hoppscotch realtime update <id> [--title] [--url] [--headers] [--protocols] [--path] [--topic] [--qos] [--client-id]
agent-hoppscotch realtime delete <id>
```

### Environment
```bash
agent-hoppscotch env list --team <id>               # List environments
agent-hoppscotch env get <id> --team <id>           # Get environment details
agent-hoppscotch env create --team <id> --name "..." --variables '[{"key":"k","value":"v","secret":false}]'
agent-hoppscotch env update <id> --team <id> [--name "..."] [--variables '<json>']
agent-hoppscotch env delete <id>
```

## Global Flags

| Flag | Description |
|------|-------------|
| `--json` | Machine-readable JSON output |
| `--verbose` | Show raw GraphQL queries/responses |
| `--cookie <str>` | Override stored cookie |
| `--endpoint <url>` | Override stored endpoint |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Auth error (not configured/expired) |
| 3 | Not found |
| 4 | Validation error |
