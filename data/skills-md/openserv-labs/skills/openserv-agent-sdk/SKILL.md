---
name: openserv-agent-sdk
description: Create autonomous AI agents using the OpenServ SDK (@openserv-labs/sdk). Use when building agents with capabilities, tasks, file operations, or integrations. Triggers on keywords like OpenServ, agent SDK, addCapability, workspace, or multi-agent systems.
---

# OpenServ Agent SDK

Build and deploy custom AI agents for the OpenServ platform using TypeScript.

**Reference files:**

- `reference.md` - Quick reference for common patterns
- `troubleshooting.md` - Common issues and solutions
- `examples/` - Complete code examples

## What's New in v2.1

- **Built-in Tunnel** - The `run()` function auto-connects to `agents-proxy.openserv.ai`
- **No Endpoint URL Needed** - Skip `endpointUrl` in `provision()` during development
- **Automatic Port Fallback** - If your port is busy, the agent finds an available one
- **Direct Credential Binding** - `provision()` can bind credentials directly to agent instance via `agent.instance`
- **`setCredentials()` Method** - Manually bind API key and auth token to agent

## Quick Start

### Installation

```bash
npm install @openserv-labs/sdk @openserv-labs/client zod openai
```

> **Note:** The SDK requires `openai@^5.x` as a peer dependency.

### Minimal Agent

See `examples/basic-agent.ts` for a complete runnable example.

The pattern is simple:

1. Create an `Agent` with a system prompt
2. Add capabilities with `agent.addCapability()`
3. Call `provision()` to register on the platform (pass `agent.instance` to bind credentials)
4. Call `run(agent)` to start

---

## Complete Agent Template

### File Structure

```
my-agent/
├── src/agent.ts
├── .env
├── .gitignore
├── package.json
└── tsconfig.json
```

### package.json

```json
{
  "name": "my-agent",
  "type": "module",
  "scripts": { "dev": "tsx src/agent.ts" },
  "dependencies": {
    "@openserv-labs/sdk": "^2.1.0",
    "@openserv-labs/client": "^1.1.4",
    "dotenv": "^16.4.5",
    "openai": "^5.0.1",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^20.14.9",
    "tsx": "^4.16.0",
    "typescript": "^5.5.2"
  }
}
```

### .env

```env
OPENAI_API_KEY=your-openai-key
# Auto-populated by provision():
WALLET_PRIVATE_KEY=
OPENSERV_API_KEY=
OPENSERV_AUTH_TOKEN=
PORT=7378
```

---

## Capabilities

Capabilities are functions your agent can execute. Each requires:

- `name` - Unique identifier
- `description` - What it does (helps AI decide when to use it)
- `schema` - Zod schema defining parameters
- `run` - Function returning a string

See `examples/capability-example.ts` for basic capabilities.

### Using Agent Methods

Access `this` in capabilities to use agent methods like `addLogToTask()`, `uploadFile()`, etc.

See `examples/capability-with-agent-methods.ts` for logging and file upload patterns.

---

## Agent Methods

### Task Management

```typescript
await agent.createTask({ workspaceId, assignee, description, body, input, dependencies })
await agent.updateTaskStatus({ workspaceId, taskId, status: 'in-progress' })
await agent.addLogToTask({ workspaceId, taskId, severity: 'info', type: 'text', body: '...' })
await agent.markTaskAsErrored({ workspaceId, taskId, error: 'Something went wrong' })
const task = await agent.getTaskDetail({ workspaceId, taskId })
const tasks = await agent.getTasks({ workspaceId })
```

### File Operations

```typescript
const files = await agent.getFiles({ workspaceId })
await agent.uploadFile({ workspaceId, path: 'output.txt', file: 'content', taskIds: [taskId] })
await agent.deleteFile({ workspaceId, fileId })
```

### Secrets & Integrations

```typescript
const secrets = await agent.getSecrets({ workspaceId })
const value = await agent.getSecretValue({ workspaceId, secretId })

await agent.callIntegration({
  workspaceId,
  integrationId: 'twitter-v2',
  details: { endpoint: '/2/tweets', method: 'POST', data: { text: 'Hello!' } }
})
```

---

## Action Context

The `action` parameter in capabilities contains request context:

```typescript
action.type // 'do-task'
action.task.id
action.task.description
action.task.input
action.workspace.id
action.workspace.goal
action.me.id // Current agent ID
action.integrations // Available integrations
```

---

## Trigger Types

```typescript
import { triggers } from '@openserv-labs/client'

triggers.webhook({ waitForCompletion: true, timeout: 180 })
triggers.x402({ name: '...', description: '...', price: '0.01' })
triggers.cron({ schedule: '0 9 * * *' })
triggers.manual()
```

---

## Deployment

### Local Development

```bash
npm run dev
```

The `run()` function automatically:

- Starts the agent HTTP server (port 7378, with automatic fallback)
- Connects via WebSocket to `agents-proxy.openserv.ai`
- Routes platform requests to your local machine

**No need for ngrok or other tunneling tools** - `run()` handles this seamlessly. Just call `run(agent)` and your local agent is accessible to the platform.

### Production

```typescript
await provision({
  agent: {
    name: 'my-agent',
    description: '...',
    endpointUrl: 'https://my-agent.example.com' // Required for production
  }
  // ...
})

await agent.start() // Start without tunnel
```

---

## DO NOT USE

- **`this.process()`** inside capabilities - Use direct OpenAI calls instead
- **`doTask` override** - The SDK handles task execution automatically
- **`this.completeTask()`** - Task completion is handled by the Runtime API

---

## Related Skills

- **openserv-client** - Full Platform Client API reference
- **openserv-multi-agent-workflows** - Multi-agent collaboration patterns
