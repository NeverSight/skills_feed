---
name: shopify-bulk-sync
description: Use this skill when the user asks about "bulk operations", "mass update", "bulk mutation", "JSONL", "staged uploads", "large data sync", "tier launch", or any large-scale Shopify data operations. Provides Bulk Operations API patterns for processing thousands of items.
---

# Shopify Bulk Operations Best Practices

## Overview

Shopify Bulk Operations API allows processing thousands of items in a single async operation, bypassing rate limits entirely. Use for mass updates when regular API calls would exceed limits.

**Rate Limit Context:**
- Regular metafield API: **2 requests/second**, **40 requests/minute**
- Bulk Operations: **No rate limits** - runs server-side on Shopify

---

## When to Use Bulk Operations

| Customer Count | Approach | Why |
|---------------|----------|-----|
| 1-50 | Direct API calls | Fast, no overhead |
| 50-500 | Cloud Tasks with batching | Manageable with delays |
| **500+** | **Bulk Operations API** | Avoids rate limits entirely |
| **1000+** | **Bulk Operations (REQUIRED)** | Only viable approach |

**Use Cases:**
- Tier launch/relaunch (thousands of customers)
- Mass metafield sync (point balance, tier info)
- Bulk customer tag updates
- Mass product metafield updates
- Initial data migration

---

## File Size Limits & Chunking

**Critical Limits:**

| Limit | Value | Strategy |
|-------|-------|----------|
| Max JSONL file size | ~100MB | Chunk large operations |
| Max lines per chunk | **50,000** | Safe limit for metafields |
| Max metafields per line | 1 | One metafield per JSONL line |

---

## JSONL Format

Each line must be a valid JSON object with variables for your mutation:

**For metafieldsSet:**
```jsonl
{"metafields":{"key":"points","namespace":"loyalty","ownerId":"gid://shopify/Customer/123","value":"500","type":"number_integer"}}
{"metafields":{"key":"points","namespace":"loyalty","ownerId":"gid://shopify/Customer/456","value":"750","type":"number_integer"}}
```

**For customerUpdate (tags):**
```jsonl
{"input":{"id":"gid://shopify/Customer/123","tags":["vip","gold-tier"]}}
{"input":{"id":"gid://shopify/Customer/456","tags":["member","silver-tier"]}}
```

---

## Complete Flow

### Step 1: Create Staged Upload

```graphql
mutation {
  stagedUploadsCreate(input: [{
    resource: BULK_MUTATION_VARIABLES
    filename: "bulk-update.jsonl"
    mimeType: "text/jsonl"
    httpMethod: POST
  }]) {
    stagedTargets {
      url
      resourceUrl
      parameters { name value }
    }
    userErrors { field message }
  }
}
```

### Step 2: Upload JSONL File

```javascript
const formData = new FormData();

// Add all parameters from stagedTargets.parameters
stagedTarget.parameters.forEach(({name, value}) => {
  formData.append(name, value);
});

// Add the JSONL file
formData.append('file', Buffer.from(jsonlContent), {
  filename: 'bulk-update.jsonl',
  contentType: 'text/jsonl'
});

await fetch(stagedTarget.url, {method: 'POST', body: formData});

// Get the stagedUploadPath from the 'key' parameter
const stagedUploadPath = stagedTarget.parameters.find(p => p.name === 'key').value;
```

### Step 3: Run Bulk Mutation

```graphql
mutation {
  bulkOperationRunMutation(
    mutation: "mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) { metafieldsSet(metafields: $metafields) { metafields { id } userErrors { field message } } }",
    stagedUploadPath: "tmp/your-staged-upload-path"
  ) {
    bulkOperation { id status }
    userErrors { field message }
  }
}
```

### Step 4: Handle Completion Webhook

Subscribe to `BULK_OPERATIONS_FINISH` webhook:

```javascript
// When webhook fires, check if more chunks needed
if (hasMoreChunks) {
  await uploadNextChunk(syncId, nextOffset);
} else {
  await updateStatus('completed');
}
```

---

## Chunking Strategy

For datasets > 50K items, process in chunks:

```javascript
const CHUNK_SIZE = 50000;

async function processBulkUpdate(items) {
  const totalChunks = Math.ceil(items.length / CHUNK_SIZE);

  for (let i = 0; i < totalChunks; i++) {
    const chunk = items.slice(i * CHUNK_SIZE, (i + 1) * CHUNK_SIZE);

    // Prepare JSONL for this chunk
    const jsonl = chunk.map(item => JSON.stringify({
      metafields: {
        key: 'points',
        namespace: 'loyalty',
        ownerId: `gid://shopify/Customer/${item.customerId}`,
        value: String(item.points),
        type: 'number_integer'
      }
    })).join('\n');

    // Upload and run bulk operation
    const result = await runBulkOperation(jsonl);

    // Save state for webhook continuation
    await saveChunkState({
      bulkOperationId: result.id,
      currentChunk: i,
      totalChunks,
      nextOffset: (i + 1) * CHUNK_SIZE
    });

    // Wait for webhook before next chunk
    break;
  }
}
```

---

## Error Handling & Retry

```javascript
async function uploadWithRetry(stagedTarget, jsonl, maxRetries = 3) {
  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      await uploadJSONL(stagedTarget, jsonl);
      return; // Success
    } catch (error) {
      const isRetryable = [400, 429, 500, 502, 503, 504].includes(error.status);

      if (isRetryable && attempt < maxRetries - 1) {
        const backoffMs = Math.pow(2, attempt + 1) * 1000;
        await delay(backoffMs);
        continue;
      }

      throw error;
    }
  }
}
```

---

## Best Practices

### DO:

- Use bulk operations for 500+ items
- Chunk at 50K lines per operation
- Buffer writes to storage
- Track progress state for webhook continuation
- Use exponential backoff for retries
- Clean up storage files after completion

### DON'T:

- Use bulk operations for small batches (<100 items)
- Upload huge files without chunking (>100MB)
- Forget to handle `BULK_OPERATIONS_FINISH` webhook
- Write to storage on every iteration (buffer instead)
- Block waiting for bulk operation completion (use webhooks)

---

## Decision Guide

```
How many items to update?
├── 1-50: Direct API calls
├── 50-500: Cloud Tasks with batched API calls
└── 500+: Shopify Bulk Operations API

Is it time-sensitive?
├── Yes (real-time): Cloud Tasks with batching
└── No (can wait minutes): Bulk Operations

Triggered by?
├── User action (sync button): Bulk Operations
├── Webhook (order): Cloud Tasks
└── Cron job (scheduled sync): Bulk Operations
```

---

## Checklist

```
- Volume > 500 items? Use Bulk Operations
- JSONL files chunked at 50K lines max
- Staged uploads used (stagedUploadsCreate -> POST -> bulkOperationRunMutation)
- Storage buffering for large data collection
- Chunk state saved for webhook continuation
- BULK_OPERATIONS_FINISH webhook handler implemented
- Retry logic with exponential backoff
- Progress status saved for user visibility
- Cleanup: delete temp files after completion
```