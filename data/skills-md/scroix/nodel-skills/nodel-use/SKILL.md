---
name: nodel-use
description: Interact with running Nodel instances via REST API - check node status, view console logs, invoke actions, debug nodes, manage deployments. Use when making curl commands, API calls, or troubleshooting Nodel.
---

# Interacting with Running Nodel Instances

## Quick Reference

**Default Base URL:** `http://localhost:8085`

```bash
# List all nodes
curl http://localhost:8085/REST/nodes

# Get node console logs
curl "http://localhost:8085/REST/nodes/My%20Node/console?from=0&max=50"

# Invoke an action
curl -X POST "http://localhost:8085/REST/nodes/My%20Node/actions/Power/call" \
  -H "Content-Type: application/json" -d '{"arg":"On"}'
```

**Important:** URL-encode node names with spaces (`%20`). See `references/rest-api.md` for all endpoints.

## REST API Endpoints

See `references/rest-api.md` for complete endpoint reference.

### Host-Level Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/REST/nodes` | GET | Map of all nodes |
| `/REST/allNodes` | GET | Discovered nodes on network |
| `/REST/discovery` | GET | Discovery service state |
| `/REST/nodeURLs` | GET | Advertised node URLs (`?filter=` optional) |
| `/REST/nodeURLsForNode` | GET | Advertised URLs for one node (`?name=`) |
| `/REST/started` | GET | Host startup timestamp |
| `/REST/logs` | GET | Framework logs |
| `/REST/diagnostics` | GET | System diagnostics |
| `/REST/recipes/list` | GET | Available node recipes |
| `/REST/toolkit` | GET | Python toolkit reference |

### Node-Level Endpoints

Base: `/REST/nodes/{nodeName}/`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/console` | GET | Console logs |
| `/logs` | GET | Action/event activity |
| `/actions` | GET | List actions |
| `/actions/{name}/call` | POST | Invoke action |
| `/events` | GET | List events |
| `/events/{name}` | GET | Event metadata + last value |
| `/params` | GET | Current parameters |
| `/script/raw` | GET | Script source |
| `/restart` | POST | Restart node |

## Debugging Workflows

### Check Node Health

```bash
# 1. Get console output
curl "http://localhost:8085/REST/nodes/My%20Node/console?from=0&max=100"

# 2. Look for error patterns in response
# Console levels: info (blue), out (gray), warn (orange), err (red)

# 3. Check action/event activity
curl "http://localhost:8085/REST/nodes/My%20Node/logs?from=0&max=50"

# 4. Inspect current parameters
curl http://localhost:8085/REST/nodes/My%20Node/params
```

### Live Log Tailing (Long-Polling)

```bash
# Initial fetch - note the highest 'seq' value in response
curl "http://localhost:8085/REST/nodes/My%20Node/console?from=0&max=50"

# Poll for new logs (waits up to 5 seconds)
curl "http://localhost:8085/REST/nodes/My%20Node/console?from=12345&max=50&timeout=5000"
```

Response format:
```json
[
  {"seq": 12346, "timestamp": "2024-01-15T10:30:00", "console": "info", "comment": "Connected"},
  {"seq": 12347, "timestamp": "2024-01-15T10:30:01", "console": "err", "comment": "Error message"}
]
```

### Inspect and Test Actions

```bash
# List available actions
curl http://localhost:8085/REST/nodes/My%20Node/actions

# Test action - string argument
curl -X POST "http://localhost:8085/REST/nodes/My%20Node/actions/Power/call" \
  -H "Content-Type: application/json" -d '{"arg":"On"}'
```

See `references/debugging.md` for complete debugging workflows.

### Evaluate Python Expressions

```bash
# Check variable value
curl "http://localhost:8085/REST/nodes/My%20Node/eval?expr=param_ipAddress"

# Check connection state (requires _isConnected variable set by TCP callbacks)
curl "http://localhost:8085/REST/nodes/My%20Node/eval?expr=_isConnected"

# Execute diagnostic code
curl -X POST "http://localhost:8085/REST/nodes/My%20Node/exec" \
  -H "Content-Type: application/json" \
  -d '{"code":"console.info(\"Connection state: %s\" % _isConnected)"}'
```

## Common Issues

### Node Not Responding

1. Check if node exists: `curl http://localhost:8085/REST/nodes`
2. Check console for startup errors
3. Verify parameters are configured
4. Check network connectivity to device

### Action Not Working

1. Check action exists: `curl .../actions`
2. Verify argument format matches schema
3. Check console for errors after calling
4. Test with simple action first (Refresh, Status)

### Connection Issues

1. Use `/eval` to check connection state
2. Look for "disconnected" in console logs
3. Verify IP/port parameters
4. Test network connectivity from Nodel host

## Node Management

### Create Node from Recipe

```bash
# List recipes (returns objects with 'path', 'modified', etc.)
curl http://localhost:8085/REST/recipes/list

# Create node from a recipe path
curl -X POST "http://localhost:8085/REST/newNode?base=nodel-official-recipes/PJLink" \
  -H "Content-Type: application/json" \
  -d '{"value":"New Node"}'
```

### Update Node Parameters

```bash
# Get current values
curl http://localhost:8085/REST/nodes/My%20Node/params

# Save new values
curl -X POST "http://localhost:8085/REST/nodes/My%20Node/params/save" \
  -H "Content-Type: application/json" \
  -d '{"ipAddress": "192.168.1.100", "port": 9999}'
```

### Restart/Rename/Delete

```bash
# Restart
curl -X POST "http://localhost:8085/REST/nodes/My%20Node/restart" \
  -H "Content-Type: application/json" \
  -d '{}'

# Rename
curl -X POST "http://localhost:8085/REST/nodes/My%20Node/rename?newName=New%20Name" \
  -H "Content-Type: application/json" \
  -d '{}'

# Delete (requires confirmation)
curl -X POST "http://localhost:8085/REST/nodes/My%20Node/remove?confirm=true" \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Tips

1. **URL-encode node names** - Spaces become `%20`
2. **Use `?trace` for debugging** - Adds stack traces to error responses
3. **POST payloads** - Send JSON for POST endpoints (`-d '{}'` if no explicit payload)
4. **Long-poll timeout** - Use 5000-10000ms for log tailing
5. **Check restart completion** - Use `/hasRestarted?timestamp={before}&timeout=5000`
