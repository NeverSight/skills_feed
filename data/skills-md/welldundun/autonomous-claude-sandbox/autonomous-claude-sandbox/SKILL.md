---
name: autonomous-claude-sandbox
description: Deploy Claude Code on Cloudflare Sandboxes. Run autonomous AI coding tasks in isolated containers via a simple API.
---

# Autonomous Claude Sandbox Skill

Deploy Claude Code on Cloudflare Sandbox containers for autonomous AI task execution.

## When to Use This Skill

Activate when you see these patterns:

**Setup & Deployment:**
- "Setup autonomous claude sandbox"
- "Deploy claude on cloudflare"
- "Set up Claude Code on Cloudflare containers"

**Task Execution:**
- "Execute task in sandbox"
- "Run this in the sandbox"
- "Delegate to sandbox"
- "Send to autonomous claude"
- "Run claude code autonomously"

## Workflow Routing

Route to the appropriate workflow based on the request:

**Setup & Operations:**
- Set up new Cloudflare Sandbox deployment → `Workflows/Setup.md`
- Deploy/update existing deployment → `Workflows/Deploy.md`
- Troubleshoot issues → `Workflows/Troubleshoot.md`
- Upgrade SDK or dependencies → `Workflows/Upgrade.md`
- Monitor deployment health → `Workflows/Monitor.md`

**Task Execution:**
- Execute a task in the sandbox → `Workflows/Execute.md`

---

## Deterministic Tools

These scripts output JSON and use proper exit codes for AI agent consumption.

| Tool | Purpose | Usage |
|------|---------|-------|
| `Tools/execute-task.sh` | Execute task in sandbox | `./Tools/execute-task.sh <url> <token> <task>` |
| `Tools/check-prerequisites.sh` | Verify all requirements | `./Tools/check-prerequisites.sh` |
| `Tools/validate-config.sh` | Check project config | `./Tools/validate-config.sh [project-dir]` |
| `Tools/test-deployment.sh` | Test live deployment | `./Tools/test-deployment.sh <url> [token]` |
| `Tools/diagnose.sh` | Gather troubleshooting info | `./Tools/diagnose.sh [project-dir]` |
| `Tools/generate-token.sh` | Generate auth token | `./Tools/generate-token.sh` |

### Example: Execute Task

```bash
./Tools/execute-task.sh https://my-worker.workers.dev my-auth-token "Write a hello world script" | jq .
```

Output:
```json
{
  "success": true,
  "taskId": "a1b2c3d4-...",
  "stdout": "Created hello.py with print('Hello, World!')",
  "execution_time_ms": 8500
}
```

### Example: Check Prerequisites

```bash
./Tools/check-prerequisites.sh | jq .
```

Output:
```json
{
  "success": true,
  "checks": {
    "node": { "installed": true, "version": "20.10.0", "meets_requirement": true },
    "docker": { "installed": true, "running": true },
    "wrangler": { "installed": true, "authenticated": true }
  },
  "issues": []
}
```

### Example: Validate Config

```bash
./Tools/validate-config.sh /path/to/project | jq .
```

### Example: Test Deployment

```bash
./Tools/test-deployment.sh https://my-worker.workers.dev my-auth-token | jq .
```

---

## Quick Start

### Prerequisites

- Cloudflare account with Workers Paid plan ($5/month)
- Docker Desktop running locally
- Node.js 18+
- Claude MAX subscription

### Installation

```bash
# Clone reference implementation
git clone https://github.com/WellDunDun/claude-code-sandbox.git
cd claude-code-sandbox
npm install

# Authenticate with Cloudflare
npx wrangler login

# Create R2 bucket
npx wrangler r2 bucket create claude-results

# Set secrets
claude setup-token
npx wrangler secret put CLAUDE_CODE_OAUTH_TOKEN

openssl rand -hex 32
npx wrangler secret put SERVER_AUTH_TOKEN

# Configure and deploy
# Edit wrangler.jsonc with your account_id
npm run deploy
```

### Test

```bash
# Health check
curl https://YOUR-WORKER.workers.dev/health

# Execute task
curl -X POST https://YOUR-WORKER.workers.dev/execute \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"task": "What is 2 + 2?"}'
```

---

## API Reference

Formal specification of the Cloudflare Sandbox Worker API endpoints.

### GET /health

Health check endpoint. No authentication required.

**Request:**
```bash
curl https://YOUR-WORKER.workers.dev/health
```

**Response (200 OK):**
```json
{
  "status": "healthy",
  "platform": "cloudflare_sandboxes",
  "auth_method": "claude_subscription_setup_token"
}
```

### POST /execute

Execute a Claude Code task in an isolated sandbox container.

**Headers:**
| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | `Bearer <SERVER_AUTH_TOKEN>` |
| `Content-Type` | Yes | `application/json` |

**Request Body:**
```json
{
  "task": "string",      // Required: Task description for Claude
  "timeout": 300000      // Optional: Timeout in ms (default: 300000)
}
```

**Response (200 OK):**
```json
{
  "taskId": "uuid",
  "success": true,
  "stdout": "Task output...",
  "stderr": "",
  "output": "Task output..."
}
```

**Error Responses:**

| Code | Cause | Response |
|------|-------|----------|
| 400 | Missing task | `{"error": "Task is required"}` |
| 401 | Invalid token | `{"error": "Unauthorized"}` |
| 500 | Execution failed | `{"error": "Task execution failed", "details": "..."}` |

**Example:**
```bash
curl -X POST https://YOUR-WORKER.workers.dev/execute \
  -H "Authorization: Bearer YOUR_SERVER_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"task": "What is 2 + 2?", "timeout": 60000}'
```

### GET /tasks/:taskId/result

Retrieve stored task results from R2.

**Headers:**
| Header | Required | Description |
|--------|----------|-------------|
| `Authorization` | Yes | `Bearer <SERVER_AUTH_TOKEN>` |

**Response (200 OK):**
```json
{
  "taskId": "uuid",
  "success": true,
  "stdout": "...",
  "stderr": "...",
  "timestamp": "2024-01-28T00:00:00.000Z"
}
```

**Error Responses:**

| Code | Cause | Response |
|------|-------|----------|
| 401 | Invalid token | `{"error": "Unauthorized"}` |
| 404 | Task not found | `{"error": "Task result not found"}` |

---

## Critical Gotchas

These are hard-won lessons from actual deployment. **Read carefully.**

### 1. Base Image Must Be cloudflare/sandbox

```dockerfile
# CORRECT
FROM docker.io/cloudflare/sandbox:0.7.0

# WRONG - causes Error 1101
FROM node:20-slim
```

### 2. Use getSandbox() API

```typescript
// CORRECT
import { getSandbox } from "@cloudflare/sandbox";
const sandbox = getSandbox(env.Sandbox, "unique-id");

// WRONG - older API
const sandbox = await Sandbox.create(env.SANDBOX, {...});
```

### 3. Export the Sandbox Class

```typescript
// REQUIRED in index.ts
export { Sandbox } from "@cloudflare/sandbox";
```

### 4. Use --permission-mode, NOT --dangerously-skip-permissions

```typescript
// CORRECT - works in sandbox (runs as root)
const cmd = `claude -p "${task}" --permission-mode acceptEdits`;

// WRONG - fails because sandbox runs as root
const cmd = `claude --dangerously-skip-permissions -p "${task}"`;
```

### 5. Binding Name Must Match

```jsonc
// wrangler.jsonc
"durable_objects": {
  "bindings": [{ "class_name": "Sandbox", "name": "Sandbox" }]
}
```

```typescript
// index.ts - must match "name" above
interface Env {
  Sandbox: DurableObjectNamespace;
}
```

### 6. containers:write Permission Required

```bash
npx wrangler login
# Ensure containers:write is granted
```

---

## Required Configuration

### Dockerfile

```dockerfile
FROM docker.io/cloudflare/sandbox:0.7.0
RUN npm install -g @anthropic-ai/claude-code
ENV COMMAND_TIMEOUT_MS=300000
EXPOSE 3000
```

### wrangler.jsonc

```jsonc
{
  "containers": [{
    "class_name": "Sandbox",
    "image": "./Dockerfile",
    "instance_type": "standard-1",
    "max_instances": 5
  }],
  "durable_objects": {
    "bindings": [{ "class_name": "Sandbox", "name": "Sandbox" }]
  },
  "migrations": [{ "new_sqlite_classes": ["Sandbox"], "tag": "v1" }]
}
```

---

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| 1101 | Wrong base image | Use `cloudflare/sandbox:0.7.0` |
| containers:write | Missing permission | Re-run `wrangler login` |
| root privileges | Wrong flag | Use `--permission-mode acceptEdits` |
| 401 from Anthropic | Bad OAuth token | Re-run `claude setup-token` |

---

## Security Considerations

### Token Management

**SERVER_AUTH_TOKEN:**
- Generate with `./Tools/generate-token.sh` (256-bit entropy)
- Store securely - this grants full API access
- Rotate periodically (recommended: quarterly)
- Never commit to version control

**CLAUDE_CODE_OAUTH_TOKEN:**
- Generated via `claude setup-token`
- Tied to your Claude MAX subscription
- Expires and needs periodic refresh
- Set as Wrangler secret, never in code

### Token Rotation

```bash
# Rotate SERVER_AUTH_TOKEN
./Tools/generate-token.sh
npx wrangler secret put SERVER_AUTH_TOKEN
# Update all clients with new token

# Refresh CLAUDE_CODE_OAUTH_TOKEN
claude setup-token
npx wrangler secret put CLAUDE_CODE_OAUTH_TOKEN
npm run deploy
```

### Network Security

- All traffic is HTTPS (TLS 1.3)
- Cloudflare provides DDoS protection
- Worker validates auth before any sandbox access
- Containers are isolated per-task

### Data Handling

| Data Type | Storage | Retention |
|-----------|---------|-----------|
| Task input | Memory only | Request duration |
| Task output | R2 bucket | Until deleted |
| OAuth tokens | Wrangler secrets | Encrypted at rest |
| Logs | Cloudflare | 7 days default |

### Container Isolation

Each task runs in an isolated container:
- Fresh environment per execution
- No persistent state between tasks
- Resource limits enforced
- No network access to other containers

### Best Practices

1. **Least Privilege:** Only grant necessary permissions
2. **Token Rotation:** Rotate tokens quarterly
3. **Monitoring:** Watch for unusual auth failures
4. **Audit Logs:** Review Cloudflare logs regularly
5. **R2 Cleanup:** Delete old task results periodically

---

## Resources

- **Reference Implementation:** https://github.com/WellDunDun/claude-code-sandbox
- **Cloudflare Sandbox Docs:** https://developers.cloudflare.com/sandbox/
- **Sandbox SDK GitHub:** https://github.com/cloudflare/sandbox-sdk
- **Claude Code Tutorial:** https://developers.cloudflare.com/sandbox/tutorials/claude-code/

---

## Costs

| Component | Cost |
|-----------|------|
| Workers Paid | $5/month |
| Container CPU | ~$0.072/vCPU-hour |
| Container Memory | ~$0.009/GiB-hour |
| R2 Storage | First 10GB free |

Typical usage: $15-40/month (excluding Claude MAX subscription).
