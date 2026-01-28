---
name: vercel-workflow
description: Best practices for using Vercel Workflow DevKit. Use when creating, modifying, or debugging workflows, steps, hooks, webhooks, or any durable function using the Workflow DevKit. Ensures proper usage of directives, error handling, serialization, streaming, and workflow patterns.
---

# Workflow Best Practices

Enforces proper usage of Vercel Workflow DevKit patterns for durable, resumable workflows.

## Core Concepts

### Directives

Two fundamental directives define execution context:

**`"use workflow"`** - Marks orchestration functions that coordinate steps:
```typescript
export async function processOrder(orderId: string) {
  'use workflow';
  
  const order = await fetchOrder(orderId);  // Step
  await sleep('1h');                         // Suspend
  return await chargePayment(order);        // Step
}
```

**`"use step"`** - Marks atomic operations with full runtime access:
```typescript
async function fetchOrder(orderId: string) {
  'use step';
  
  // Full Node.js access: database, APIs, file I/O
  return await db.orders.findUnique({ where: { id: orderId } });
}
```

**Critical Rules**:
- Workflow functions must be **deterministic** - same inputs always produce same outputs
- Workflows run in a **sandboxed environment** without Node.js API access
- Steps have full runtime access and **automatic retries** on failure
- All parameters must be **serializable** (no functions, class instances, closures)

### Execution Model

Workflows suspend and resume through:
1. **Step calls** - Workflow yields while step executes
2. **`sleep()`** - Pause for duration without consuming resources
3. **Hooks/Webhooks** - Wait for external events

During replay, workflows re-execute using cached step results from the event log.

## Structure Patterns

### Organization

```
workflows/{feature-name}/
├── index.ts           # Workflow orchestration
├── steps/             # Step functions
│   ├── {action}.ts
│   └── ...
└── hooks/             # Hook definitions
    └── {event}.ts
```

### Workflow Function

```typescript
import { sleep, createHook } from 'workflow';
import { processData } from './steps/process-data';
import { sendEmail } from './steps/send-email';

export async function myWorkflow(userId: string) {
  'use workflow';
  
  const result = await processData(userId);
  
  await sleep('5m');
  
  await sendEmail({ userId, result });
  
  return { status: 'completed', result };
}
```

**Rules**:
- ONE workflow export per file (main entry point)
- Orchestrate steps - don't do work directly
- Use language primitives: `Promise.all`, `for...of`, `try/catch`
- NO Node.js APIs: `fs`, `http`, `crypto`, `process`
- NO side effects: database calls, API requests, mutations
- Parameters and returns must be serializable

### Step Functions

```typescript
type ProcessDataArgs = {
  userId: string;
  options?: { retry?: boolean };
};

export async function processData(params: ProcessDataArgs) {
  'use step';
  
  // Full Node.js access
  const user = await db.users.findUnique({ where: { id: params.userId } });
  const result = await externalApi.process(user);
  
  return { processed: true, data: result };
}
```

**Rules**:
- ONE step per file is preferred for clarity
- Use typed parameters (object or single value)
- Return serializable values only
- Mutations happen here - not in workflows
- Can throw errors for automatic retry
- Use `getStepMetadata()` for idempotency keys

## Error Handling

### Automatic Retries

Steps retry automatically (default: 3 attempts):

```typescript
async function fetchData(url: string) {
  'use step';
  
  // Throws Error - will retry
  const response = await fetch(url);
  if (!response.ok) throw new Error('Fetch failed');
  
  return response.json();
}
```

### Fatal Errors (No Retry)

```typescript
import { FatalError } from 'workflow';

async function validateUser(userId: string) {
  'use step';
  
  if (!userId) {
    // Don't retry invalid input
    throw new FatalError('User ID is required');
  }
  
  return await db.users.findUnique({ where: { id: userId } });
}
```

### Retryable with Delay

```typescript
import { RetryableError } from 'workflow';

async function callRateLimitedApi() {
  'use step';
  
  const response = await fetch('https://api.example.com');
  
  if (response.status === 429) {
    // Retry after 10 seconds
    throw new RetryableError('Rate limited', { delay: '10s' });
  }
  
  return response.json();
}
```

### Workflow Error Handling

```typescript
export async function resilientWorkflow(orderId: string) {
  'use workflow';
  
  try {
    const order = await fetchOrder(orderId);
    await processPayment(order);
  } catch (error) {
    // Log and handle at workflow level
    await logError({ orderId, error: String(error) });
    throw error; // Workflow will fail
  }
}
```

## Serialization

### Allowed Types

Primitives, objects, arrays, Date, URL, Headers, Request, Response, ReadableStream, WritableStream.

### Pass-by-Value

Parameters are **copied**, not referenced:

```typescript
// ❌ WRONG - mutations not visible
export async function badWorkflow() {
  'use workflow';
  
  let counter = 0;
  await updateCounter(counter);
  console.log(counter); // Still 0!
}

async function updateCounter(count: number) {
  'use step';
  count++; // Only mutates the copy
}
```

```typescript
// ✅ CORRECT - return modified values
export async function goodWorkflow() {
  'use workflow';
  
  let counter = 0;
  counter = await updateCounter(counter);
  console.log(counter); // 1
}

async function updateCounter(count: number) {
  'use step';
  return count + 1;
}
```

### Forbidden Types

NO functions, class instances, symbols, WeakMaps, closures:

```typescript
// ❌ WRONG
async function badStep(callback: () => void) {
  'use step';
  callback(); // ERROR: Cannot serialize functions
}

// ✅ CORRECT - use configuration
type Config = { shouldLog: boolean };

async function goodStep(config: Config) {
  'use step';
  if (config.shouldLog) console.log('Done');
}
```

## Hooks & Webhooks

### Type-Safe Hooks

```typescript
import { defineHook } from 'workflow';
import { z } from 'zod';

const approvalHook = defineHook({
  schema: z.object({
    approved: z.boolean(),
    approvedBy: z.string(),
    comment: z.string(),
  }),
});

export async function documentWorkflow(docId: string) {
  'use workflow';
  
  const hook = approvalHook.create({
    token: `approval:${docId}`,
  });
  
  const result = await hook;
  
  return result.approved ? 'approved' : 'rejected';
}
```

### Iterating Over Events

```typescript
import { createHook } from 'workflow';

export async function monitoringWorkflow(channelId: string) {
  'use workflow';
  
  const hook = createHook<{ message: string }>({
    token: `messages:${channelId}`,
  });
  
  for await (const event of hook) {
    await processMessage(event.message);
    
    if (event.message === 'stop') break;
  }
}
```

### Webhooks

```typescript
import { createWebhook } from 'workflow';

export async function paymentWorkflow(orderId: string) {
  'use workflow';
  
  const webhook = createWebhook({
    respondWith: new Response('Payment received', { status: 200 }),
  });
  
  await sendPaymentLink({ orderId, webhookUrl: webhook.url });
  
  const request = await webhook;
  const payload = await request.json();
  
  return { paid: true, transactionId: payload.id };
}
```

## Streaming

### Writing to Streams (Steps Only)

```typescript
import { getWritable } from 'workflow';

export async function progressWorkflow() {
  'use workflow';
  
  const writable = getWritable<{ progress: number }>();
  
  await processWithProgress(writable);
  await finalizeStream(writable);
}

async function processWithProgress(writable: WritableStream) {
  'use step';
  
  const writer = writable.getWriter();
  
  try {
    for (let i = 0; i <= 100; i += 10) {
      await writer.write({ progress: i });
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  } finally {
    writer.releaseLock();
  }
}

async function finalizeStream(writable: WritableStream) {
  'use step';
  await writable.close();
}
```

**Critical**: Workflows can GET streams but NOT interact with them. Steps must do all writing/closing.

### Namespaced Streams

```typescript
export async function multiStreamWorkflow() {
  'use workflow';
  
  const defaultStream = getWritable();
  const logStream = getWritable({ namespace: 'logs' });
  
  await writeToStreams(defaultStream, logStream);
}

async function writeToStreams(
  defaultStream: WritableStream,
  logStream: WritableStream
) {
  'use step';
  
  const writer1 = defaultStream.getWriter();
  const writer2 = logStream.getWriter();
  
  try {
    await writer1.write({ data: 'main' });
    await writer2.write({ log: 'processing' });
  } finally {
    writer1.releaseLock();
    writer2.releaseLock();
  }
}
```

## Common Patterns

### Sequential Steps

```typescript
export async function sequentialWorkflow(data: unknown) {
  'use workflow';
  
  const validated = await validateData(data);
  const processed = await processData(validated);
  const stored = await storeData(processed);
  
  return stored;
}
```

### Parallel Steps

```typescript
export async function parallelWorkflow(userId: string) {
  'use workflow';
  
  const [user, orders, payments] = await Promise.all([
    fetchUser(userId),
    fetchOrders(userId),
    fetchPayments(userId),
  ]);
  
  return { user, orders, payments };
}
```

### Conditional Steps

```typescript
export async function conditionalWorkflow(orderId: string) {
  'use workflow';
  
  const order = await fetchOrder(orderId);
  
  if (order.isPaid) {
    await fulfillOrder(order);
  } else {
    await sendPaymentReminder(order);
  }
}
```

### Loops with Steps

```typescript
export async function batchWorkflow(items: string[]) {
  'use workflow';
  
  for (const item of items) {
    await processItem(item);
  }
  
  return { processed: items.length };
}
```

### Timeout Pattern

```typescript
import { sleep } from 'workflow';

export async function timeoutWorkflow(taskId: string) {
  'use workflow';
  
  const result = await Promise.race([
    processTask(taskId),
    sleep('30s').then(() => 'timeout' as const),
  ]);
  
  if (result === 'timeout') {
    throw new Error('Task timed out after 30 seconds');
  }
  
  return result;
}
```

### Rollback Pattern

```typescript
export async function rollbackWorkflow(orderId: string) {
  'use workflow';
  
  const rollbacks: Array<() => Promise<void>> = [];
  
  try {
    await reserveInventory(orderId);
    rollbacks.push(() => releaseInventory(orderId));
    
    await chargePayment(orderId);
    rollbacks.push(() => refundPayment(orderId));
    
    await fulfillOrder(orderId);
  } catch (error) {
    // Execute rollbacks in reverse order
    for (const rollback of rollbacks.reverse()) {
      await rollback();
    }
    throw error;
  }
}
```

## Idempotency

### Using Step IDs

```typescript
import { getStepMetadata } from 'workflow';

async function chargeUser(userId: string, amount: number) {
  'use step';
  
  const { stepId } = getStepMetadata();
  
  return await stripe.charges.create(
    { amount, currency: 'usd', customer: userId },
    { idempotencyKey: `charge:${stepId}` }
  );
}
```

**Rules**:
- Always use `stepId` for external API idempotency
- `stepId` is stable across retries
- Never use attempt numbers or timestamps

## Testing Workflows

```typescript
import { start } from 'workflow/api';
import { myWorkflow } from './workflows/my-workflow';

// Start workflow
const run = await start(myWorkflow, ['arg1']);

// Check status
console.log(await run.status); // 'running' | 'completed' | 'failed'

// Wait for completion
const result = await run.returnValue;

// Stream output
const stream = run.readable;
```

## Anti-Patterns

### ❌ Direct Node.js API in Workflow

```typescript
export async function badWorkflow() {
  'use workflow';
  
  // ERROR: fs not available in workflow context
  const data = fs.readFileSync('file.txt');
}
```

### ❌ Non-Deterministic Logic

```typescript
export async function badWorkflow() {
  'use workflow';
  
  // ERROR: Date.now() will change on replay
  if (Date.now() > someTimestamp) { /* ... */ }
  
  // ERROR: Math.random() will change on replay
  if (Math.random() > 0.5) { /* ... */ }
}
```

### ❌ Mutating Parameters

```typescript
export async function badWorkflow(data: { count: number }) {
  'use workflow';
  
  await incrementCount(data);
  console.log(data.count); // Still original value!
}

async function incrementCount(data: { count: number }) {
  'use step';
  data.count++; // Only mutates the copy
}
```

### ❌ Stream Interaction in Workflow

```typescript
export async function badWorkflow() {
  'use workflow';
  
  const writable = getWritable();
  const writer = writable.getWriter(); // ERROR!
  await writer.write('data'); // ERROR!
}
```

### ❌ Missing Directive

```typescript
// ERROR: No "use step" - won't be retried
async function fetchData() {
  return await db.query('SELECT * FROM users');
}
```

## Quick Reference

**Workflow Functions**:
- Orchestrate steps
- Must be deterministic
- No Node.js APIs
- Sandboxed environment

**Step Functions**:
- Execute work
- Full Node.js access
- Automatic retries
- Can throw errors

**Serialization**:
- Pass-by-value (copy)
- Return modified values
- No functions/closures

**Error Handling**:
- `Error` - Retry automatically
- `FatalError` - No retry
- `RetryableError` - Retry with delay

**Streaming**:
- Get stream in workflow
- Interact in steps only
- Always release locks
- Close when done

**Hooks**:
- Use `defineHook` for type safety
- Custom tokens for determinism
- Iterate with `for await...of`

**Idempotency**:
- Use `stepId` for keys
- Apply to external APIs
- Steps are already idempotent
