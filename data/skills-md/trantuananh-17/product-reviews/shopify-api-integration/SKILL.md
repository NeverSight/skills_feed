---
name: shopify-api-integration
description: Use this skill when the user asks about "Shopify GraphQL", "Admin API", "metafields", "webhooks", "rate limiting", "pagination", "App Bridge", or any Shopify API integration work. Provides Shopify API patterns, rate limit handling, and best practices.
---

# Shopify API Best Practices

## API Version Check (CRITICAL)

**Always verify API version before implementing!**

Shopify deprecates API versions regularly. Check:
1. Current API version in `shopify.app.toml` or app config
2. Shopify release notes for breaking changes
3. Use Shopify MCP tools to verify current schema

```javascript
// Check what version your app uses
// shopify.app.toml
[api]
api_version = "2024-10"  // Verify this matches your implementation
```

---

## API Selection Guide

| Need | Solution |
|------|----------|
| Customize checkout UI | Checkout UI Extension |
| Apply discounts | Discount Function |
| Validate cart | Cart Validation Function |
| React to events | Webhooks |
| Read/write data | GraphQL Admin API |
| Sync large data | Bulk Operations |
| Store custom data | Metafields/Metaobjects |

---

## GraphQL Admin API

### Basic Query

```javascript
const query = `
  query getProduct($id: ID!) {
    product(id: $id) {
      id
      title
      handle
      variants(first: 10) {
        nodes {
          id
          price
        }
      }
    }
  }
`;

const response = await shopify.graphql(query, { id: productId });
```

### Pagination

```javascript
async function getAllProducts(shopify) {
  const products = [];
  let hasNextPage = true;
  let cursor = null;

  while (hasNextPage) {
    const query = `
      query getProducts($cursor: String) {
        products(first: 50, after: $cursor) {
          pageInfo { hasNextPage }
          edges {
            cursor
            node { id title }
          }
        }
      }
    `;

    const response = await shopify.graphql(query, { cursor });
    const { edges, pageInfo } = response.products;

    products.push(...edges.map(e => e.node));
    hasNextPage = pageInfo.hasNextPage;
    cursor = edges[edges.length - 1]?.cursor;
  }

  return products;
}
```

---

## Bulk Operations (ALWAYS Consider First)

**Before implementing any Shopify data sync, ask: "Can this hit API limits?"**

**Rate Limits Context:**
- Regular metafield API: **2 requests/second**, **40 requests/minute**
- Bulk Operations: **No rate limits** - runs server-side on Shopify

### Volume Decision Guide

| Volume | Strategy |
|--------|----------|
| < 50 items | Regular GraphQL |
| 50-500 items | Batch with Cloud Tasks + rate limiting |
| **500+ items** | **Bulk Operations API** |

**For detailed bulk mutation patterns, see:** `shopify-bulk-operations` skill

---

## Rate Limiting

### Cloud Tasks (Recommended for Rate Limits)

```javascript
// BAD: In-function sleep wastes CPU time
await sleep(60000); // 60s sleep = 60s CPU billed

// GOOD: Schedule retry with Cloud Tasks
async function scheduleRetry(payload, delaySeconds) {
  await client.createTask({
    parent: client.queuePath(project, location, 'shopify-retry'),
    task: {
      httpRequest: {
        url: `${baseUrl}/api/retry-shopify`,
        body: Buffer.from(JSON.stringify(payload)).toString('base64'),
        headers: { 'Content-Type': 'application/json' }
      },
      scheduleTime: {
        seconds: Math.floor(Date.now() / 1000) + delaySeconds
      }
    }
  });
}
```

---

## Metafields

### Set Metafields (Batch)

```javascript
const mutation = `
  mutation metafieldsSet($metafields: [MetafieldsSetInput!]!) {
    metafieldsSet(metafields: $metafields) {
      metafields { id key value }
      userErrors { field message }
    }
  }
`;

await shopify.graphql(mutation, {
  metafields: [
    {
      ownerId: customerId,
      namespace: 'loyalty',
      key: 'points',
      type: 'number_integer',
      value: '500'
    },
    {
      ownerId: customerId,
      namespace: 'loyalty',
      key: 'tier',
      type: 'single_line_text_field',
      value: 'Gold'
    }
  ]
});
```

---

## Webhooks

### Response Time (CRITICAL)

**Must respond within 5 seconds!**

```javascript
// BAD: Heavy processing (may timeout)
app.post('/webhooks/orders/create', async (req, res) => {
  await calculatePoints(req.body);
  await updateCustomer(req.body);
  await syncToShopify(req.body);
  res.status(200).send('OK');
});

// GOOD: Queue and respond fast
app.post('/webhooks/orders/create', async (req, res) => {
  // Quick validation
  if (!verifyHmac(req)) {
    return res.status(401).send('Unauthorized');
  }

  // Queue for background processing
  await webhookQueueRef.add({
    type: 'orders/create',
    payload: req.body
  });

  // Respond immediately
  res.status(200).send('OK');
});
```

### HMAC Verification

```javascript
import crypto from 'crypto';

function verifyHmac(req) {
  const hmac = req.get('X-Shopify-Hmac-Sha256');
  const body = req.rawBody;
  const secret = process.env.SHOPIFY_WEBHOOK_SECRET;

  const hash = crypto
    .createHmac('sha256', secret)
    .update(body, 'utf8')
    .digest('base64');

  return crypto.timingSafeEqual(
    Buffer.from(hmac),
    Buffer.from(hash)
  );
}
```

---

## App Bridge (Direct API)

### When to Use

| Scenario | Use App Bridge | Use Firebase API |
|----------|---------------|------------------|
| Simple Shopify CRUD | Yes | No |
| Need Firestore data | No | Yes |
| Complex business logic | No | Yes |
| Background processing | No | Yes |

### Direct API Call

```javascript
import { authenticatedFetch } from '@shopify/app-bridge/utilities';

async function fetchProducts(app) {
  const response = await authenticatedFetch(app)(
    '/admin/api/2024-04/graphql.json',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        query: `{ products(first: 10) { nodes { id title } } }`
      })
    }
  );

  return response.json();
}
```

**Benefits:**
- Faster (no Firebase roundtrip)
- Lower cost (no function invocation)
- Uses shop's session directly