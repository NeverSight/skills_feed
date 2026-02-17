---
name: encore-infrastructure
description: Declare databases, Pub/Sub, cron jobs, and secrets with Encore.ts.
---

# Encore Infrastructure Declaration

## Instructions

Encore.ts uses declarative infrastructure - you define resources in code and Encore handles provisioning:

- **Locally** (`encore run`) - Encore runs infrastructure in Docker (Postgres, Redis, etc.)
- **Production** - Deploy via [Encore Cloud](https://encore.dev/cloud) to your AWS/GCP, or self-host using generated infrastructure config

### Critical Rule

**All infrastructure must be declared at package level (top of file), not inside functions.**

## Databases (PostgreSQL)

```typescript
import { SQLDatabase } from "encore.dev/storage/sqldb";

// CORRECT: Package level
const db = new SQLDatabase("mydb", {
  migrations: "./migrations",
});

// WRONG: Inside function
async function setup() {
  const db = new SQLDatabase("mydb", { migrations: "./migrations" });
}
```

### Migrations

Create migrations in the `migrations/` directory:

```
service/
├── encore.service.ts
├── api.ts
├── db.ts
└── migrations/
    ├── 001_create_users.up.sql
    └── 002_add_email_index.up.sql
```

Migration naming: `{number}_{description}.up.sql`

## Pub/Sub

### Topics

```typescript
import { Topic } from "encore.dev/pubsub";

interface OrderCreatedEvent {
  orderId: string;
  userId: string;
  total: number;
}

// Package level declaration
export const orderCreated = new Topic<OrderCreatedEvent>("order-created", {
  deliveryGuarantee: "at-least-once",
});
```

### Publishing

```typescript
await orderCreated.publish({
  orderId: "123",
  userId: "user-456",
  total: 99.99,
});
```

### Subscriptions

```typescript
import { Subscription } from "encore.dev/pubsub";

const _ = new Subscription(orderCreated, "send-confirmation-email", {
  handler: async (event) => {
    await sendEmail(event.userId, event.orderId);
  },
});
```

## Cron Jobs

```typescript
import { CronJob } from "encore.dev/cron";
import { api } from "encore.dev/api";

// The endpoint to call
export const cleanupExpiredSessions = api(
  { expose: false },
  async (): Promise<void> => {
    // Cleanup logic
  }
);

// Package level cron declaration
const _ = new CronJob("cleanup-sessions", {
  title: "Clean up expired sessions",
  schedule: "0 * * * *",  // Every hour
  endpoint: cleanupExpiredSessions,
});
```

### Schedule Formats

| Format | Example | Description |
|--------|---------|-------------|
| `every` | `"1h"`, `"30m"` | Simple interval (must divide 24h evenly) |
| `schedule` | `"0 9 * * 1"` | Cron expression (9am every Monday) |

## Object Storage

```typescript
import { Bucket } from "encore.dev/storage/objects";

// Package level
export const uploads = new Bucket("user-uploads", {
  versioned: false,
});

// Public bucket
export const publicAssets = new Bucket("public-assets", {
  public: true,
  versioned: false,
});
```

### Operations

```typescript
// Upload
await uploads.upload("path/to/file.jpg", buffer, {
  contentType: "image/jpeg",
});

// Download
const data = await uploads.download("path/to/file.jpg");

// Check existence
const exists = await uploads.exists("path/to/file.jpg");

// Delete
await uploads.remove("path/to/file.jpg");

// Public URL (only for public buckets)
const url = publicAssets.publicUrl("image.jpg");
```

## Secrets

```typescript
import { secret } from "encore.dev/config";

// Package level
const stripeKey = secret("StripeSecretKey");

// Usage (call as function)
const key = stripeKey();
```

Set secrets via CLI:
```bash
encore secret set --type prod StripeSecretKey
```

## Guidelines

- Infrastructure declarations MUST be at package level
- Use descriptive names for resources
- Keep migrations sequential and numbered
- Subscription handlers must be idempotent (at-least-once delivery)
- Secrets are accessed by calling the secret as a function
- Cron endpoints should be `expose: false` (internal only)
