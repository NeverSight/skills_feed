---
name: encore-go-infrastructure
description: Declare infrastructure with Encore Go.
---

# Encore Go Infrastructure Declaration

## Instructions

Encore Go uses declarative infrastructure - you define resources as package-level variables and Encore handles provisioning:

- **Locally** (`encore run`) - Encore runs infrastructure in Docker (Postgres, Redis, etc.)
- **Production** - Deploy via [Encore Cloud](https://encore.dev/cloud) to your AWS/GCP, or self-host using generated infrastructure config

### Critical Rule

**All infrastructure must be declared at package level, not inside functions.**

## Databases (PostgreSQL)

```go
package user

import "encore.dev/storage/sqldb"

// CORRECT: Package level
var db = sqldb.NewDatabase("userdb", sqldb.DatabaseConfig{
    Migrations: "./migrations",
})

// WRONG: Inside function
func setup() {
    db := sqldb.NewDatabase("userdb", sqldb.DatabaseConfig{...})
}
```

### Migrations

Create migrations in the `migrations/` directory:

```
user/
├── user.go
├── db.go
└── migrations/
    ├── 1_create_users.up.sql
    └── 2_add_email_index.up.sql
```

Migration naming: `{number}_{description}.up.sql`

## Pub/Sub

### Topics

```go
package events

import "encore.dev/pubsub"

type OrderCreatedEvent struct {
    OrderID string `json:"order_id"`
    UserID  string `json:"user_id"`
    Total   int    `json:"total"`
}

// Package level declaration
var OrderCreated = pubsub.NewTopic[*OrderCreatedEvent]("order-created", pubsub.TopicConfig{
    DeliveryGuarantee: pubsub.AtLeastOnce,
})
```

### Publishing

```go
msgID, err := events.OrderCreated.Publish(ctx, &events.OrderCreatedEvent{
    OrderID: "123",
    UserID:  "user-456",
    Total:   9999,
})
```

### Subscriptions

```go
package notifications

import (
    "context"
    "myapp/events"
    "encore.dev/pubsub"
)

var _ = pubsub.NewSubscription(events.OrderCreated, "send-confirmation-email",
    pubsub.SubscriptionConfig[*events.OrderCreatedEvent]{
        Handler: sendConfirmationEmail,
    },
)

func sendConfirmationEmail(ctx context.Context, event *events.OrderCreatedEvent) error {
    // Send email...
    return nil
}
```

## Cron Jobs

```go
package cleanup

import (
    "context"
    "encore.dev/cron"
)

// The cron job declaration
var _ = cron.NewJob("cleanup-sessions", cron.JobConfig{
    Title:    "Clean up expired sessions",
    Schedule: "0 * * * *",  // Every hour
    Endpoint: CleanupExpiredSessions,
})

//encore:api private
func CleanupExpiredSessions(ctx context.Context) error {
    // Cleanup logic
    return nil
}
```

### Schedule Formats

| Format | Example | Description |
|--------|---------|-------------|
| Cron expression | `"0 9 * * 1"` | 9am every Monday |
| Every interval | `"every 1h"` | Every hour |
| Every interval | `"every 30m"` | Every 30 minutes |

## Object Storage

```go
package uploads

import "encore.dev/storage/objects"

// Package level
var Uploads = objects.NewBucket("user-uploads", objects.BucketConfig{})

// Public bucket
var PublicAssets = objects.NewBucket("public-assets", objects.BucketConfig{
    Public: true,
})
```

### Operations

```go
// Upload
attrs, err := uploads.Uploads.Upload(ctx, "path/to/file.jpg", bytes.NewReader(data),
    objects.UploadOptions{
        ContentType: "image/jpeg",
    },
)

// Download
reader, err := uploads.Uploads.Download(ctx, "path/to/file.jpg")
defer reader.Close()
data, _ := io.ReadAll(reader)

// Check existence
attrs, err := uploads.Uploads.Attrs(ctx, "path/to/file.jpg")
// err == objects.ErrObjectNotFound if doesn't exist

// Delete
err := uploads.Uploads.Remove(ctx, "path/to/file.jpg")

// Public URL (only for public buckets)
url := uploads.PublicAssets.PublicURL("image.jpg")
```

## Secrets

```go
package email

import "encore.dev/config"

var secrets struct {
    SendGridAPIKey config.String
    SMTPPassword   config.String
}

func sendEmail() error {
    apiKey := secrets.SendGridAPIKey()
    // Use the secret...
}
```

Set secrets via CLI:
```bash
encore secret set --type prod SendGridAPIKey
```

## Config Values

```go
package myservice

import "encore.dev/config"

var cfg struct {
    MaxRetries config.Int
    BaseURL    config.String
    Debug      config.Bool
}

func doSomething() {
    if cfg.Debug() {
        log.Println("Debug mode enabled")
    }
}
```

## Guidelines

- Infrastructure declarations MUST be at package level
- Use descriptive names for resources
- Keep migrations sequential and numbered
- Subscription handlers must be idempotent (at-least-once delivery)
- Secrets are accessed by calling them as functions
- Cron endpoints should be `private` (internal only)
- Each service typically has its own database
