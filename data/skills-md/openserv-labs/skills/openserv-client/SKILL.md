---
name: openserv-client
description: Complete guide to using @openserv-labs/client for managing agents, workflows, triggers, and tasks on the OpenServ Platform. Covers provisioning, authentication, and the full Platform API.
---

# OpenServ Client

The `@openserv-labs/client` package provides a TypeScript client for the OpenServ Platform API.

**Reference files:**

- `reference.md` - Full API reference for all PlatformClient methods
- `troubleshooting.md` - Common issues and solutions
- `examples/` - Complete code examples

## Installation

```bash
npm install @openserv-labs/client
```

---

## Quick Start: Just `provision()` + `run()`

**The simplest deployment is just two calls: `provision()` and `run()`.** That's it.

See `examples/agent.ts` for a complete runnable example.

> **Key Point:** `provision()` is **idempotent**. Call it every time your app starts - no need to check `isProvisioned()` first.

### What `provision()` Does

1. Creates/retrieves an Ethereum wallet for authentication
2. Authenticates with the OpenServ platform
3. Creates or updates the agent (idempotent)
4. Generates API key and auth token
5. **Binds credentials to agent instance** (if `agent.instance` is provided)
6. Creates or updates the workflow with trigger and task
7. Creates workflow graph (edges linking trigger to task)
8. Activates trigger and sets workflow to running
9. Persists state to `.openserv.json`

### Agent Instance Binding (v1.1+)

Pass your agent instance to `provision()` for automatic credential binding:

```typescript
const agent = new Agent({ systemPrompt: '...' })

await provision({
  agent: {
    instance: agent, // Calls agent.setCredentials() automatically
    name: 'my-agent',
    description: '...'
  },
  workflow: { ... }
})

// agent now has apiKey and authToken set - ready for run()
await run(agent)
```

This eliminates the need to manually set `OPENSERV_API_KEY` environment variables.

### Provision Result

```typescript
interface ProvisionResult {
  agentId: number
  apiKey: string
  authToken?: string
  workflowId: number
  triggerId: string
  triggerToken: string
  paywallUrl?: string // For x402 triggers
  apiEndpoint?: string // For webhook triggers
}
```

---

## PlatformClient: Full API Access

For advanced use cases, use `PlatformClient` directly:

```typescript
import { PlatformClient } from '@openserv-labs/client'

// Using API key
const client = new PlatformClient({
  apiKey: process.env.OPENSERV_USER_API_KEY
})

// Or using wallet authentication
const client = new PlatformClient()
await client.authenticate(process.env.WALLET_PRIVATE_KEY)
```

See `reference.md` for full API documentation on:

- `client.agents.*` - Agent management
- `client.workflows.*` - Workflow management
- `client.triggers.*` - Trigger management
- `client.tasks.*` - Task management
- `client.integrations.*` - Integration connections
- `client.payments.*` - x402 payments
- `client.web3.*` - Credits top-up

---

## Triggers Factory

Use the `triggers` factory for type-safe trigger configuration:

```typescript
import { triggers } from '@openserv-labs/client'

// Webhook (free, public endpoint)
triggers.webhook({
  input: { query: { type: 'string', description: 'Search query' } },
  waitForCompletion: true,
  timeout: 180
})

// x402 (paid API with paywall)
triggers.x402({
  name: 'AI Research Assistant',
  description: 'Get comprehensive research reports on any topic',
  price: '0.01',
  input: {
    prompt: {
      type: 'string',
      title: 'Your Request',
      description: 'Describe what you would like the agent to do'
    }
  }
})

// Cron (scheduled)
triggers.cron({
  schedule: '0 9 * * *', // Daily at 9 AM
  timezone: 'America/New_York'
})

// Manual (platform UI only)
triggers.manual()
```

### Input Schema

Define fields for webhook/x402 paywall UI:

```typescript
triggers.x402({
  name: 'Content Writer',
  description: 'Generate polished content on any topic',
  price: '0.01',
  input: {
    topic: {
      type: 'string',
      title: 'Content Topic',
      description: 'Enter the subject you want covered'
    },
    style: {
      type: 'string',
      title: 'Writing Style',
      enum: ['formal', 'casual', 'humorous'],
      default: 'casual'
    }
  }
})
```

### Cron Expressions

```
┌───────────── minute (0-59)
│ ┌───────────── hour (0-23)
│ │ ┌───────────── day of month (1-31)
│ │ │ ┌───────────── month (1-12)
│ │ │ │ ┌───────────── day of week (0-6, Sunday=0)
* * * * *
```

Common: `0 9 * * *` (daily 9 AM), `*/5 * * * *` (every 5 min), `0 9 * * 1-5` (weekdays 9 AM)

---

## State Management

```typescript
import { getProvisionedInfo, clearProvisionedState } from '@openserv-labs/client'

// Get stored IDs and tokens
const info = getProvisionedInfo('my-agent', 'default')

// Clear state (forces fresh creation)
clearProvisionedState()
```

---

## Firing Triggers

### Webhook

```bash
curl -X POST https://api.openserv.ai/webhooks/trigger/TOKEN \
  -H "Content-Type: application/json" \
  -d '{"query": "hello world"}'
```

### x402 (Programmatic)

```typescript
const result = await client.payments.payWorkflow({
  triggerUrl: 'https://api.openserv.ai/webhooks/x402/trigger/TOKEN',
  input: { prompt: 'Hello world' }
})
```

---

## Environment Variables

| Variable                | Description                  | Required |
| ----------------------- | ---------------------------- | -------- |
| `OPENSERV_USER_API_KEY` | User API key (from platform) | Yes\*    |
| `WALLET_PRIVATE_KEY`    | Wallet for SIWE auth         | Yes\*    |
| `OPENSERV_API_URL`      | Custom API URL               | No       |

\*Either API key or wallet key required

---

## Cleanup

```typescript
await client.workflows.delete({ id: workflowId })
await client.agents.delete({ id: agentId })
clearProvisionedState()
```

---

## Updating This Skill

This skill may be outdated. The OpenServ team ships updates regularly—new features, API changes, and bug fixes won't be reflected here until you update. **If something isn't working as expected, or you want to make sure you have the latest information, update the skill before proceeding.**

```bash
# Check if updates are available
npx skills check

# Update all installed skills to latest versions
npx skills update
```

Or reinstall the OpenServ skills directly:

```bash
npx skills add openserv-labs/skills
```

---

## Related Skills

- **openserv-agent-sdk** - Building agents with capabilities
- **openserv-multi-agent-workflows** - Multi-agent collaboration patterns
- **openserv-launch** - Launch tokens on Base blockchain
- **openserv-ideaboard-api** - Find ideas and ship agent services on the Ideaboard
