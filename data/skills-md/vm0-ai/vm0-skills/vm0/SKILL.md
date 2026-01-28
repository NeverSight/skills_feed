---
name: vm0
description: VM0 API for running AI agents in secure sandboxes. Use this skill to execute agents, manage runs, and download outputs (artifacts) and inputs (volumes) via the VM0 platform API.
vm0_secrets:
  - VM0_API_KEY
---

# VM0 API

Execute AI agents in secure sandboxed environments and manage their inputs/outputs.

## When to Use

- Execute AI agents in isolated sandbox environments
- Monitor and manage agent runs (status, logs, metrics)
- List and download input files (volumes) provided to agents
- List and download output files (artifacts) created by agents

## Prerequisites

```bash
export VM0_API_KEY=vm0_live_your-api-key
```

### Get API Key

1. Install the VM0 CLI: https://docs.vm0.ai/docs/getting-started
2. Run `vm0 auth login` to authenticate
3. Run `vm0 auth setup-token` to view your API key
4. Copy the token starting with `vm0_live_`

> **Important:** When using `$VAR` in a command that pipes to another command, wrap only the curl command in `bash -c '...'`, then pipe to jq outside. Due to a Claude Code bug, environment variables are silently cleared when pipes are used directly.
> ```bash
> bash -c 'curl -s "https://api.vm0.ai/v1/agents" -H "Authorization: Bearer $VM0_API_KEY"' | jq '.data'
> ```

## Quick Start

### List Your Agents

```bash
bash -c 'curl -s "https://api.vm0.ai/v1/agents" -H "Authorization: Bearer $VM0_API_KEY"' | jq '.data[] | {id, name}'
```

### Run an Agent

Write to `/tmp/vm0_request.json`:

```json
{
  "agent": "my-agent",
  "prompt": "Hello, please introduce yourself"
}
```

Then run:

```bash
bash -c 'curl -s -X POST "https://api.vm0.ai/v1/runs" -H "Authorization: Bearer $VM0_API_KEY" -H "Content-Type: application/json" -d @/tmp/vm0_request.json' | jq '{id, status}'
```

### Check Run Status

Replace `<run-id>` with your run ID:

```bash
bash -c 'curl -s "https://api.vm0.ai/v1/runs/<run-id>" -H "Authorization: Bearer $VM0_API_KEY"' | jq '{id, status, error, execution_time_ms}'
```

### Get Run Logs

```bash
bash -c 'curl -s "https://api.vm0.ai/v1/runs/<run-id>/logs" -H "Authorization: Bearer $VM0_API_KEY"' | jq '.data[]'
```

## Core Operations

### Agents

List all agents:

```bash
bash -c 'curl -s "https://api.vm0.ai/v1/agents" -H "Authorization: Bearer $VM0_API_KEY"' | jq '.data'
```

Get agent details:

```bash
bash -c 'curl -s "https://api.vm0.ai/v1/agents/<agent-id>" -H "Authorization: Bearer $VM0_API_KEY"' | jq '{id, name, description}'
```

See [references/agents.md](references/agents.md) for version listing.

### Runs

Create a run with variables:

```bash
curl -s -X POST "https://api.vm0.ai/v1/runs" \
  -H "Authorization: Bearer $VM0_API_KEY" \
  -H "Content-Type: application/json" \
  -d @- << 'EOF'
{
  "agent": "my-agent",
  "prompt": "Process the data file",
  "variables": {
    "DEBUG": "true"
  },
  "volumes": {
    "input-data": "latest"
  }
}
EOF
```

Cancel a running execution:

```bash
bash -c 'curl -s -X POST "https://api.vm0.ai/v1/runs/<run-id>/cancel" -H "Authorization: Bearer $VM0_API_KEY"' | jq '{id, status}'
```

See [references/runs.md](references/runs.md) for events streaming, logs filtering, and metrics.

### Volumes (Input Storage)

List volumes:

```bash
bash -c 'curl -s "https://api.vm0.ai/v1/volumes" -H "Authorization: Bearer $VM0_API_KEY"' | jq '.data[] | {id, name}'
```

Download volume as tar.gz archive (follows 302 redirect):

```bash
curl -L -o volume.tar.gz "https://api.vm0.ai/v1/volumes/<volume-id>/download" \
  -H "Authorization: Bearer $VM0_API_KEY"
```

See [references/volumes.md](references/volumes.md) for version listing and download options.

### Artifacts (Output Storage)

List artifacts:

```bash
bash -c 'curl -s "https://api.vm0.ai/v1/artifacts" -H "Authorization: Bearer $VM0_API_KEY"' | jq '.data[] | {id, name}'
```

Download artifact as tar.gz archive (follows 302 redirect):

```bash
curl -L -o artifact.tar.gz "https://api.vm0.ai/v1/artifacts/<artifact-id>/download" \
  -H "Authorization: Bearer $VM0_API_KEY"
```

Extract downloaded archive:

```bash
tar -xzf artifact.tar.gz -C ./output/
```

See [references/artifacts.md](references/artifacts.md) for version listing and download options.

## Common Patterns

### Pagination

List endpoints support cursor-based pagination:

```bash
bash -c 'curl -s "https://api.vm0.ai/v1/runs?limit=10" -H "Authorization: Bearer $VM0_API_KEY"' | jq '{data, pagination}'
```

Response includes:
```json
{
  "pagination": {
    "has_more": true,
    "next_cursor": "abc123"
  }
}
```

Fetch next page:

```bash
bash -c 'curl -s "https://api.vm0.ai/v1/runs?limit=10&cursor=abc123" -H "Authorization: Bearer $VM0_API_KEY"' | jq '{data, pagination}'
```

### Error Handling

All errors return a consistent format:

```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "resource_not_found",
    "message": "No such agent: 'my-agent'",
    "param": "agent"
  }
}
```

| Error Type | Status | Description |
|------------|--------|-------------|
| `authentication_error` | 401 | Invalid or missing API key |
| `invalid_request_error` | 400 | Invalid parameters |
| `not_found_error` | 404 | Resource doesn't exist |
| `api_error` | 500 | Internal server error |

## Detailed References

- [Agents API](references/agents.md) - List agents and versions
- [Runs API](references/runs.md) - Execute agents, stream events, get logs and metrics
- [Artifacts API](references/artifacts.md) - List and download agent outputs
- [Volumes API](references/volumes.md) - List and download input files

## API Reference

- Documentation: https://docs.vm0.ai/docs/reference/api
- Base URL: `https://api.vm0.ai/v1/`
