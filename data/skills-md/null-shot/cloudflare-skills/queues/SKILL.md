---
name: queues
description: Asynchronous message queues for reliable background processing. Load when offloading background tasks, batch processing messages, implementing retry logic with dead letter queues, rate limiting upstream APIs, or decoupling producers from consumers.
---

# Cloudflare Queues

Build reliable asynchronous message processing on Cloudflare Workers using Queues for background tasks, batch operations, and retry handling.

## When to Use

- **Background Tasks** - Offload non-critical work from request handlers
- **Batch Processing** - Accumulate messages and process in batches to reduce upstream API calls
- **Retry Handling** - Automatic retries with configurable delays for transient failures
- **Decoupling** - Separate producers from consumers for scalability
- **Rate Limiting Upstream** - Control the rate of requests to external APIs
- **Dead Letter Queues** - Capture and inspect failed messages for debugging

## Quick Reference

| Task | API |
|------|-----|
| Send single message | `env.QUEUE_BINDING.send(payload)` |
| Send batch | `env.QUEUE_BINDING.sendBatch([msg1, msg2])` |
| Define consumer | `async queue(batch: MessageBatch, env: Env) { ... }` |
| Access message body | `batch.messages.map(msg => msg.body)` |
| Acknowledge message | Messages auto-ack unless handler throws |
| Retry message | `throw new Error()` in queue handler |
| Get batch size | `batch.messages.length` |

## FIRST: wrangler.jsonc Configuration

Queues require both producer and consumer configuration:

```jsonc
{
  "name": "request-logger-consumer",
  "main": "src/index.ts",
  "compatibility_date": "2025-02-11",
  "queues": {
    "producers": [{
      "name": "request-queue",
      "binding": "REQUEST_QUEUE"
    }],
    "consumers": [{
      "name": "request-queue",
      "dead_letter_queue": "request-queue-dlq",
      "retry_delay": 300,
      "max_batch_size": 100,
      "max_batch_timeout": 30,
      "max_retries": 3
    }]
  },
  "vars": {
    "UPSTREAM_API_URL": "https://api.example.com/batch-logs",
    "UPSTREAM_API_KEY": ""
  }
}
```

**Consumer Options:**
- `dead_letter_queue` - Queue name for failed messages (optional)
- `retry_delay` - Seconds to wait before retry (default: 0)
- `max_batch_size` - Max messages per batch (default: 10, max: 100)
- `max_batch_timeout` - Max seconds to wait for batch (default: 5, max: 30)
- `max_retries` - Max retry attempts (default: 3)

## Producer and Consumer Pattern

Complete example showing how to produce and consume messages:

```typescript
// src/index.ts
interface Env {
  REQUEST_QUEUE: Queue;
  UPSTREAM_API_URL: string;
  UPSTREAM_API_KEY: string;
}

export default {
  // Producer: Send messages to queue
  async fetch(request: Request, env: Env) {
    const info = {
      timestamp: new Date().toISOString(),
      method: request.method,
      url: request.url,
      headers: Object.fromEntries(request.headers),
    };
    
    await env.REQUEST_QUEUE.send(info);

    return Response.json({
      message: 'Request logged',
      requestId: crypto.randomUUID()
    });
  },

  // Consumer: Process messages in batches
  async queue(batch: MessageBatch<any>, env: Env) {
    const requests = batch.messages.map(msg => msg.body);

    const response = await fetch(env.UPSTREAM_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${env.UPSTREAM_API_KEY}`
      },
      body: JSON.stringify({
        timestamp: new Date().toISOString(),
        batchSize: requests.length,
        requests
      })
    });

    if (!response.ok) {
      // Throwing will retry the entire batch
      throw new Error(`Upstream API error: ${response.status}`);
    }
  }
};
```

## Batch Message Types

Send messages with different formats:

```typescript
// Send simple JSON payload
await env.QUEUE.send({ userId: 123, action: "login" });

// Send batch of messages
await env.QUEUE.sendBatch([
  { userId: 123, action: "login" },
  { userId: 456, action: "logout" },
  { userId: 789, action: "purchase" }
]);

// Send with typed body
interface UserEvent {
  userId: number;
  action: string;
  timestamp: string;
}

await env.QUEUE.send<UserEvent>({
  userId: 123,
  action: "login",
  timestamp: new Date().toISOString()
});
```

## Retry and Dead Letter Queues

Configure automatic retries and capture failed messages:

```jsonc
{
  "queues": {
    "consumers": [{
      "name": "main-queue",
      "dead_letter_queue": "main-queue-dlq",
      "retry_delay": 300,  // 5 minutes
      "max_retries": 3
    }]
  }
}
```

**Retry Behavior:**
1. Handler throws error → message is retried after `retry_delay` seconds
2. After `max_retries` attempts → message moves to dead letter queue
3. No DLQ configured → message is discarded after max retries
4. Handler succeeds → message is acknowledged and removed

**Processing Dead Letter Queue:**

```typescript
export default {
  // Main consumer
  async queue(batch: MessageBatch<any>, env: Env) {
    for (const message of batch.messages) {
      try {
        await processMessage(message.body);
      } catch (error) {
        console.error('Processing failed:', error);
        throw error; // Trigger retry
      }
    }
  }
};

// Separate worker for DLQ
export default {
  async queue(batch: MessageBatch<any>, env: Env) {
    // Log failed messages for debugging
    for (const message of batch.messages) {
      console.error('Dead letter message:', {
        body: message.body,
        attempts: message.attempts,
        timestamp: message.timestamp
      });
      
      // Optionally store in KV/D1 for inspection
      await env.FAILED_MESSAGES.put(
        message.id,
        JSON.stringify(message),
        { expirationTtl: 86400 * 7 } // 7 days
      );
    }
  }
};
```

## Batch Processing Patterns

### Pattern 1: All-or-Nothing Batch

Process entire batch as transaction—if any message fails, retry all:

```typescript
async queue(batch: MessageBatch<any>, env: Env) {
  // Throwing retries entire batch
  const response = await fetch(env.UPSTREAM_API_URL, {
    method: 'POST',
    body: JSON.stringify(batch.messages.map(m => m.body))
  });
  
  if (!response.ok) {
    throw new Error(`Batch failed: ${response.status}`);
  }
}
```

### Pattern 2: Individual Message Handling

Process messages individually with partial success:

```typescript
async queue(batch: MessageBatch<any>, env: Env) {
  const results = await Promise.allSettled(
    batch.messages.map(msg => processMessage(msg.body))
  );
  
  const failures = results.filter(r => r.status === 'rejected');
  
  if (failures.length > 0) {
    console.error(`${failures.length}/${batch.messages.length} messages failed`);
    // Throwing here retries the entire batch
    // Consider sending failed messages to a separate queue instead
  }
}
```

### Pattern 3: Partial Retry with Requeue

Requeue only failed messages:

```typescript
async queue(batch: MessageBatch<any>, env: Env) {
  const failedMessages = [];
  
  for (const message of batch.messages) {
    try {
      await processMessage(message.body);
    } catch (error) {
      failedMessages.push(message.body);
    }
  }
  
  // Requeue only failures
  if (failedMessages.length > 0) {
    await env.RETRY_QUEUE.sendBatch(failedMessages);
  }
  
  // Don't throw - successfully processed messages won't be retried
}
```

## Message Size Limits

- **Max message size**: 128 KB per message
- **Max batch size**: 100 messages per batch (configurable)
- **Max total batch size**: 256 MB

```typescript
// Handle large payloads
async function sendLargePayload(data: any, env: Env) {
  const serialized = JSON.stringify(data);
  
  if (serialized.length > 100_000) { // ~100KB
    // Option 1: Store in R2/KV, send reference
    const key = crypto.randomUUID();
    await env.LARGE_PAYLOADS.put(key, serialized);
    await env.QUEUE.send({ type: 'large', key });
  } else {
    await env.QUEUE.send(data);
  }
}
```

## Environment Interface

Type your queue bindings:

```typescript
interface Env {
  // Producer bindings
  REQUEST_QUEUE: Queue<RequestInfo>;
  EMAIL_QUEUE: Queue<EmailPayload>;
  
  // Environment variables
  UPSTREAM_API_URL: string;
  UPSTREAM_API_KEY: string;
  
  // Other bindings
  KV: KVNamespace;
  DB: D1Database;
}

interface RequestInfo {
  timestamp: string;
  method: string;
  url: string;
  headers: Record<string, string>;
}

interface EmailPayload {
  to: string;
  subject: string;
  body: string;
}
```

## Detailed References

- **[references/patterns.md](references/patterns.md)** - Advanced patterns: fan-out, priority queues, rate limiting
- **[references/error-handling.md](references/error-handling.md)** - Retry strategies, DLQ management, monitoring
- **[references/limits.md](references/limits.md)** - Message size, batch limits, retention, CPU constraints
- **[references/testing.md](references/testing.md)** - Vitest integration, createMessageBatch, getQueueResult, testing handlers

## Best Practices

1. **Use batch processing**: Reduce upstream API calls by processing messages in batches
2. **Configure retry_delay**: Set appropriate delays to avoid overwhelming failing services
3. **Always configure DLQ**: Capture failed messages for debugging and replay
4. **Type your messages**: Use generics for type-safe message bodies
5. **Monitor batch timeouts**: Adjust `max_batch_timeout` based on processing time
6. **Handle partial failures**: Don't throw on single message failure if others succeeded
7. **Size payloads appropriately**: Keep messages under 100KB; use R2/KV for large data
8. **Use separate queues for priorities**: Different queues for high/low priority messages
9. **Log DLQ messages**: Always log or store DLQ messages for later analysis
10. **Don't await send() in hot paths**: Queue operations are async but fast—fire and forget when appropriate
