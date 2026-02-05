---
name: workflows
description: Durable, long-running workflows with automatic retries and state persistence. Load when building multi-step async processes, implementing human-in-the-loop approval flows, coordinating API calls with retry logic, or creating reliable background jobs that survive restarts.
---

# Cloudflare Workflows

Build durable, long-running workflows that survive restarts and handle retries automatically using Cloudflare Workflows.

## When to Use

Workflows are ideal for:

- **Multi-step async tasks** - Break complex processes into retriable steps
- **Human-in-the-loop workflows** - Pause execution waiting for external input
- **Reliable background jobs** - Automatic retries with exponential backoff
- **Long-running processes** - Minutes to hours of execution with state persistence
- **Coordinated API calls** - Chain multiple API calls with retry logic

**Don't use Workflows for**:
- Simple request/response handlers (use Workers)
- Real-time operations requiring <100ms response (use Workers)
- Tasks that complete in <1 second (use Workers directly)

## Quick Reference

| Operation | API |
|-----------|-----|
| Define workflow | `class MyWorkflow extends WorkflowEntrypoint<Env, Params>` |
| Execute step | `await step.do('name', async () => { ... })` |
| Sleep/pause | `await step.sleep('wait', '1 minute')` |
| Step with retries | `await step.do('name', { retries: { limit: 5 } }, async () => {})` |
| Create instance | `await env.MY_WORKFLOW.create({ id, params })` |
| Get instance | `await env.MY_WORKFLOW.get(id)` |
| Check status | `await instance.status()` |

## FIRST: wrangler.jsonc Configuration

Add workflow binding to your configuration:

```jsonc
{
  "name": "my-project",
  "main": "src/index.ts",
  "compatibility_date": "2025-02-11",
  "workflows": [
    {
      "name": "workflows-starter",
      "binding": "MY_WORKFLOW",
      "class_name": "MyWorkflow"
    }
  ]
}
```

**Key points**:
- `binding` - Environment variable name to access workflow
- `class_name` - Must match your exported Workflow class name exactly
- Multiple workflows can be defined in the array

## Critical Limits to Know

**Per-Step State Limit: 1 MiB**
- Each step's return value must be under 1 MiB (1,048,576 bytes)
- If exceeded, the step fails
- **Workaround**: Store large data in R2/KV and return a reference

```typescript
// ✅ Good: Store large data externally
const dataRef = await step.do('process large file', async () => {
  const response = await fetch('https://api.example.com/large-dataset');
  const data = await response.text();
  
  const key = crypto.randomUUID();
  await this.env.BUCKET.put(key, data); // Store in R2
  
  return { key }; // Small reference (<1 KiB)
});
```

**Total Instance State**: 100 MB (Free) / 1 GB (Paid)
- Sum of all step return values across the workflow

**Concurrency**: Only `running` instances count toward limits
- `waiting` instances (sleeping, retrying, waiting for events) do NOT count
- You can have millions sleeping simultaneously

See [references/limits.md](references/limits.md) for complete limits documentation.

## Basic Workflow Example

```typescript
import { WorkflowEntrypoint, WorkflowStep, WorkflowEvent } from 'cloudflare:workers';

type Env = {
  MY_WORKFLOW: Workflow;
  // Add your bindings here (KV, D1, R2, etc.)
};

// User-defined params passed to your workflow
type Params = {
  email: string;
  metadata: Record<string, string>;
};

export class MyWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    // Access bindings via this.env
    // Access params via event.payload
    
    const files = await step.do('fetch files', async () => {
      // This step's result is persisted
      return {
        files: [
          'doc_7392_rev3.pdf',
          'report_x29_final.pdf',
          'memo_2024_05_12.pdf',
        ],
      };
    });

    // Access previous step results
    const apiResponse = await step.do('call api', async () => {
      let resp = await fetch('https://api.cloudflare.com/client/v4/ips');
      return await resp.json<any>();
    });

    // Pause execution for a duration
    await step.sleep('wait on something', '1 minute');

    // Step with retry and timeout configuration
    await step.do(
      'write to storage',
      {
        retries: {
          limit: 5,
          delay: '5 second',
          backoff: 'exponential',
        },
        timeout: '15 minutes',
      },
      async () => {
        // Use results from previous steps
        console.log('Files from step 1:', files.files.length);
        
        if (Math.random() > 0.5) {
          throw new Error('Simulated failure - will retry');
        }
      },
    );
  }
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    let url = new URL(req.url);

    if (url.pathname.startsWith('/favicon')) {
      return Response.json({}, { status: 404 });
    }

    // Get status of existing instance
    let id = url.searchParams.get('instanceId');
    if (id) {
      let instance = await env.MY_WORKFLOW.get(id);
      return Response.json({
        status: await instance.status(),
      });
    }

    const data = await req.json();

    // Create new workflow instance
    let instance = await env.MY_WORKFLOW.create({
      id: crypto.randomUUID(),
      params: data, // Available on WorkflowEvent in run()
    });

    return Response.json({
      id: instance.id,
      details: await instance.status(),
    });
  },
};
```

## Critical Rules for Workflows

Before diving into patterns, understand these essential rules (see [references/rules.md](references/rules.md) for details):

1. **Always `await` steps** - Forgetting `await` causes lost state and swallowed errors
2. **Don't store state outside steps** - In-memory variables are lost on hibernation; only step returns persist
3. **Ensure idempotency** - Steps may retry; check if operations already completed
4. **Keep steps granular** - One API call per step for better durability
5. **Name steps deterministically** - No timestamps/random values; names are cache keys
6. **Don't mutate events** - Changes to `event.payload` aren't persisted
7. **Wrap side effects in steps** - `Math.random()`, workflow creation, etc. must be in `step.do`
8. **Keep returns under 1 MiB** - Store large data in R2/KV, return references

## Step Patterns

### Basic Step Execution

```typescript
const result = await step.do('step name', async () => {
  // Step logic here
  return { data: 'persisted result' };
});

// Use result in subsequent steps
console.log(result.data);
```

**Key rules**:
- Always `await` step.do() calls
- Step results are automatically persisted
- Steps are idempotent - re-running uses cached result
- Step names must be unique within a workflow instance

### Step with Retries

```typescript
await step.do(
  'api call with retries',
  {
    retries: {
      limit: 5,              // Max retry attempts
      delay: '5 second',     // Initial delay between retries
      backoff: 'exponential', // 'exponential', 'linear', or 'constant'
    },
  },
  async () => {
    const response = await fetch('https://api.example.com/data');
    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }
    return await response.json();
  },
);
```

### Step with Timeout

```typescript
await step.do(
  'long running operation',
  {
    timeout: '15 minutes', // Max execution time for this step
  },
  async () => {
    // Long-running work here
  },
);
```

### Sleep for Duration

```typescript
// Pause workflow execution
await step.sleep('wait for processing', '5 minutes');

// Supported formats: '30 second', '5 minute', '2 hour'
```

**Use sleep for**:
- Rate limiting between API calls
- Waiting for external systems to process
- Human-in-the-loop delays

## Instance Management

### Creating Workflow Instances

```typescript
// Create with auto-generated ID
const instance = await env.MY_WORKFLOW.create({
  params: { email: 'user@example.com' },
});

// Create with custom ID (must be unique)
const instance = await env.MY_WORKFLOW.create({
  id: crypto.randomUUID(),
  params: { email: 'user@example.com', metadata: {} },
});
```

### Getting Instance Status

```typescript
// Retrieve existing instance
const instance = await env.MY_WORKFLOW.get('instance-id');

// Check current status
const status = await instance.status();
console.log(status);
// Returns: { status: 'running' | 'complete' | 'errored', ... }
```

### Passing Parameters

Parameters passed to `create()` are available in the workflow's `run()` method:

```typescript
// In Worker
await env.MY_WORKFLOW.create({
  params: {
    userId: '123',
    action: 'process',
    options: { priority: 'high' },
  },
});

// In Workflow class
export class MyWorkflow extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    const userId = event.payload.userId;
    const action = event.payload.action;
    // Use params...
  }
}
```

**Type safety**: Define `Params` type and pass as generic to `WorkflowEntrypoint<Env, Params>`

## Integration with Workers

Workflows are triggered from Workers and can access all Worker bindings:

```typescript
type Env = {
  MY_WORKFLOW: Workflow;
  DB: D1Database;
  KV: KVNamespace;
  AI: Ai;
};

export class DataProcessor extends WorkflowEntrypoint<Env, Params> {
  async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
    // Access D1
    const user = await step.do('fetch user', async () => {
      return await this.env.DB
        .prepare('SELECT * FROM users WHERE id = ?')
        .bind(event.payload.userId)
        .first();
    });

    // Access KV
    await step.do('cache result', async () => {
      await this.env.KV.put(
        `user:${event.payload.userId}`,
        JSON.stringify(user),
        { expirationTtl: 3600 },
      );
    });

    // Access Workers AI
    await step.do('generate summary', async () => {
      const response = await this.env.AI.run('@cf/meta/llama-3-8b-instruct', {
        prompt: `Summarize: ${user.bio}`,
      });
      return response;
    });
  }
}
```

## Testing Workflows

Use Vitest with workflow introspection to test workflows with mocked steps, events, and timing:

```typescript
import { env, introspectWorkflowInstance } from 'cloudflare:test';
import { it, expect } from 'vitest';

it('should complete with mocked steps', async () => {
  // Use 'await using' for automatic disposal (required for test isolation)
  await using instance = await introspectWorkflowInstance(env.MY_WORKFLOW, 'test-123');
  
  // Configure test behavior
  await instance.modify(async (m) => {
    await m.disableSleeps(); // Make sleeps instant
    await m.mockStepResult({ name: 'fetch-data' }, { value: 'mocked' });
    await m.mockEvent({ type: 'approval', payload: { approved: true } });
  });
  
  // Execute workflow
  await env.MY_WORKFLOW.create({ id: 'test-123', params: { userId: '123' } });
  
  // Assert results
  await instance.waitForStatus('complete');
  const output = await instance.getOutput();
  expect(output.success).toBe(true);
});
```

**Key testing capabilities**:
- Disable sleeps for instant tests
- Mock step results without external dependencies
- Mock events for human-in-the-loop workflows
- Force errors/timeouts to test retry logic
- Proper test isolation with `isolatedStorage: true`

See [references/testing.md](references/testing.md) for complete testing guide.

## Detailed References

- **[references/steps.md](references/steps.md)** - Step API details, retry strategies, error handling, timeouts
- **[references/management.md](references/management.md)** - Instance lifecycle, status monitoring, integration patterns
- **[references/testing.md](references/testing.md)** - Vitest integration, workflow introspection, mocking, test isolation
- **[references/rules.md](references/rules.md)** - Comprehensive guide to building resilient workflows (12 critical rules)
- **[references/limits.md](references/limits.md)** - CPU limits, state limits, concurrency, rate limits, retention

## Best Practices

1. **Name steps descriptively** - Step names appear in logs and status
2. **Keep steps focused** - Each step should do one logical unit of work (see [rules.md](references/rules.md))
3. **Use retries for flaky operations** - Network calls, external APIs
4. **Configure appropriate timeouts** - Prevent steps from hanging indefinitely
5. **Type your params** - Use TypeScript generics for type safety
6. **Always await steps** - Forgetting await breaks step persistence
7. **Access bindings via this.env** - Not via global scope
8. **Design for idempotency** - Steps may be re-executed on retry (see [rules.md](references/rules.md))
9. **Keep step returns under 1 MiB** - Store large data in R2/KV and return references (see [limits.md](references/limits.md))
10. **Don't store state outside steps** - In-memory state is lost on hibernation (see [rules.md](references/rules.md))
11. **Test with Vitest** - Use workflow introspection for reliable tests (see [testing.md](references/testing.md))

## Common Patterns

### Human-in-the-Loop

```typescript
async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
  // Do automated work
  await step.do('process data', async () => { /* ... */ });
  
  // Wait for human approval (check via external system)
  await step.sleep('wait for approval', '1 hour');
  
  // Check approval status
  const approved = await step.do('check approval', async () => {
    // Query approval system
    return true;
  });
  
  if (approved) {
    await step.do('finalize', async () => { /* ... */ });
  }
}
```

### Fan-out Processing

```typescript
async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
  const items = await step.do('fetch items', async () => {
    return ['item1', 'item2', 'item3'];
  });
  
  // Process each item in separate steps
  for (let i = 0; i < items.length; i++) {
    await step.do(`process-${items[i]}`, async () => {
      // Process individual item
      return { processed: items[i] };
    });
  }
}
```

### Graceful Degradation

```typescript
async run(event: WorkflowEvent<Params>, step: WorkflowStep) {
  const result = await step.do(
    'try primary service',
    { 
      retries: { limit: 3, delay: '5 second' },
      timeout: '30 second',
    },
    async () => {
      return await fetch('https://primary-api.com/data');
    },
  ).catch(() => null); // Catch step failure
  
  if (!result) {
    // Fallback to secondary service
    await step.do('fallback service', async () => {
      return await fetch('https://fallback-api.com/data');
    });
  }
}
```
