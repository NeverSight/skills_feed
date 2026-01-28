---
name: n8n
description: Manage n8n workflows and troubleshoot executions. Use when user asks about n8n workflows, webhook triggers, execution errors, or wants to edit workflow nodes.
allowed-tools: Bash, Read, Write, Glob
license: MIT
---

# n8n Skill - Manage Workflows and Executions

## n8n Concepts

### Workflows
A workflow is an automation that connects multiple services/apps. It consists of:
- **Nodes** - Individual steps that perform actions (HTTP requests, code execution, integrations)
- **Connections** - Links between nodes defining data flow
- **Triggers** - How the workflow starts (webhook, schedule, manual, etc.)

### Node Types
- **Trigger nodes** - Start workflows (Webhook, Schedule, Manual)
- **Regular nodes** - Process data (HTTP Request, Set, IF, Switch)
- **Code nodes** - Custom JavaScript/Python logic
- **Integration nodes** - Connect to services (Slack, Discord, Notion, etc.)

### Executions
An execution is a single run of a workflow. States:
- **success** - Completed without errors
- **error** - Failed at some node
- **running** - Currently executing
- **waiting** - Paused, waiting for external event
- **canceled** - Manually stopped

### Execution Modes
- **webhook** - Triggered by HTTP request
- **trigger** - Triggered by schedule or event
- **manual** - Triggered manually from UI
- **retry** - Retried from a failed execution

### Webhooks
HTTP endpoints that trigger workflows:
- **Production webhook** - `/webhook/<path>` - Always active when workflow is active
- **Test webhook** - `/webhook-test/<path>` - For testing, shows data in UI

### Credentials
Stored authentication for services (API keys, OAuth tokens). Referenced by nodes but not exposed in workflow JSON.

## CLI Setup

The CLI is available via uvx (no installation needed):

```bash
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli --help
```

### Environment Variables

Required:
- `N8N_API_KEY` - API key from n8n (Settings → n8n API)
- `N8N_BASE_URL` - n8n instance URL (e.g., `https://your-instance.app.n8n.cloud`)

## CLI Reference

### List Workflows

```bash
# List all workflows
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli workflows

# Active workflows only
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli workflows --active

# JSON output
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli workflows --json
```

### Workflow Details

```bash
# Get workflow details
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli workflow <workflow_id>

# Full JSON output
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli workflow <workflow_id> --json
```

### Activate/Deactivate Workflows

```bash
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli activate <workflow_id>
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli deactivate <workflow_id>
```

### List Nodes in Workflow

```bash
# List all nodes (Code nodes marked with *)
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli nodes <workflow_id>
```

### View/Edit Nodes

```bash
# View node details
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli node <workflow_id> "node name"

# View Code node's JavaScript
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli node <workflow_id> "node name" --code

# Update Code node from file
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli node <workflow_id> "node name" --set-code script.js

# Rename a node
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli node <workflow_id> "old name" --rename "new name"

# Set node parameter (supports dot notation for nested keys)
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli node <workflow_id> "HTTP Request" --set-param url="https://api.example.com"
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli node <workflow_id> "Agent" --set-param options.systemMessage="You are helpful"

# Set multiple parameters at once
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli node <workflow_id> "Node" -p timeout=5000 -p retries=3

# Bulk update parameters from JSON (deep merged)
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli node <workflow_id> "Node" --set-param-json '{"options": {"systemMessage": "Hello"}}'
```

### Export/Import Code Nodes

Useful for editing Code node scripts in a proper editor:

```bash
# Export all Code nodes to files
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli export-code <workflow_id> ./nodes/

# Import updated scripts back
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli import-code <workflow_id> ./nodes/
```

### Trigger Workflows

```bash
# Trigger workflow by name via webhook
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli trigger "Workflow Name"

# With JSON payload
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli trigger "Workflow Name" --data '{"key": "value"}'

# With payload from file
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli trigger "Workflow Name" --file payload.json

# Use test webhook URL
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli trigger "Workflow Name" --test
```

### List Executions

```bash
# Recent executions
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli executions

# Filter by workflow
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli executions --workflow <workflow_id>

# Filter by status (error, success, running, waiting, canceled)
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli executions --status error

# Limit results
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli executions -n 100
```

### Execution Details

```bash
# Get execution details (shows error info for failed executions)
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli execution <execution_id>

# Include full execution data
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli execution <execution_id> --data

# JSON output
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli execution <execution_id> --data --json
```

### Retry Failed Execution

```bash
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli retry <execution_id>

# Use latest workflow version
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli retry <execution_id> --latest
```

### Credentials Management

**Note:** The n8n API does not allow reading credential values (security restriction). You can only list credentials metadata, create new credentials, and delete credentials. To update a credential, you must delete and recreate it.

```bash
# List all credentials (metadata only - id, name, type)
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli credentials

# Get schema for a credential type (shows required fields)
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli credential-schema httpHeaderAuth
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli credential-schema openAiApi --json

# Create a credential
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli create-credential --name "My API Key" --type httpHeaderAuth --data '{"name": "X-API-Key", "value": "secret"}'

# Create from file
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli create-credential --name "OpenAI" --type openAiApi --data-file credentials.json

# Delete a credential
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli delete-credential <credential_id>
```

## Common Workflows

### Troubleshoot Failed Executions

```bash
# 1. Find failed executions
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli executions --status error

# 2. Get error details
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli execution <id>

# 3. Get full data for debugging
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli execution <id> --data --json
```

### Edit Code Nodes

```bash
# 1. Export all Code nodes
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli export-code <workflow_id> ./nodes/

# 2. Edit scripts in your editor
# Files: ./nodes/node_name.js

# 3. Import changes back
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli import-code <workflow_id> ./nodes/
```

### Quick Node Update

```bash
# View current code
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli node <workflow_id> "node name" --code > script.js

# Edit script.js...

# Update node
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli node <workflow_id> "node name" --set-code script.js
```

### Test Webhook Workflow

```bash
# Trigger with test payload
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli trigger "Workflow Name" --test --file test_payload.json

# Check execution result
uvx --from git+https://github.com/pokgak/n8n-cli n8n-cli executions --workflow <id> -n 1
```

## Execution Data Structure

When debugging with `--data --json`, the execution contains:

```
execution
├── id                    # Execution ID
├── status                # success, error, running, etc.
├── mode                  # webhook, trigger, manual, retry
├── startedAt / stoppedAt # Timestamps
├── workflowData          # Snapshot of workflow at execution time
│   ├── name
│   ├── nodes[]
│   └── connections
└── data
    └── resultData
        ├── runData       # Output from each node
        │   └── [nodeName][]
        │       ├── data.main[][] # Node output items
        │       └── executionStatus
        ├── lastNodeExecuted
        └── error         # If failed
            ├── message
            ├── description
            └── node      # Which node failed
```

## Common Error Patterns

### Webhook Payload Issues
- Check `execution --data --json` and look at the Webhook node's output
- Payload is in `runData.Webhook[0].data.main[0][0].json.body`

### Code Node Errors
- Error message shows the JavaScript error
- Use `node <workflow_id> "node name" --code` to view the code
- Common: undefined variables, JSON parsing, missing fields

### Integration Failures
- Usually credential or API issues
- Check if the service is accessible
- Verify credential permissions
