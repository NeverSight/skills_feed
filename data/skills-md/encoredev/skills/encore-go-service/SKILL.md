---
name: encore-go-service
description: Structure services with Encore Go.
---

# Encore Go Service Structure

## Instructions

In Encore Go, **each package with an API endpoint is automatically a service**. No special configuration needed.

### Creating a Service

Simply create a package with at least one `//encore:api` endpoint:

```go
// user/user.go
package user

import "context"

type User struct {
    ID    string `json:"id"`
    Email string `json:"email"`
    Name  string `json:"name"`
}

//encore:api public method=GET path=/users/:id
func GetUser(ctx context.Context, params *GetUserParams) (*User, error) {
    // This makes "user" a service
}
```

### Minimal Service Structure

```
user/
├── user.go          # API endpoints
├── db.go            # Database (if needed)
└── migrations/      # SQL migrations
    └── 1_create_users.up.sql
```

## Application Patterns

### Single Service (Recommended Start)

Best for new projects - start simple, split later if needed:

```
my-app/
├── encore.app
├── go.mod
├── api.go           # All endpoints
├── db.go            # Database
└── migrations/
    └── 1_initial.up.sql
```

### Multi-Service

For distributed systems with clear domain boundaries:

```
my-app/
├── encore.app
├── go.mod
├── user/
│   ├── user.go
│   ├── db.go
│   └── migrations/
├── order/
│   ├── order.go
│   ├── db.go
│   └── migrations/
└── notification/
    └── notification.go
```

### Large Application (System-based)

Group related services into systems:

```
my-app/
├── encore.app
├── go.mod
├── commerce/
│   ├── order/
│   │   └── order.go
│   ├── cart/
│   │   └── cart.go
│   └── payment/
│       └── payment.go
├── identity/
│   ├── user/
│   │   └── user.go
│   └── auth/
│       └── auth.go
└── comms/
    ├── email/
    │   └── email.go
    └── push/
        └── push.go
```

## Service-to-Service Calls

Just import and call the function directly - Encore handles the RPC:

```go
package order

import (
    "context"
    "myapp/user"  // Import the user service
)

//encore:api auth method=GET path=/orders/:id
func GetOrderWithUser(ctx context.Context, params *GetOrderParams) (*OrderWithUser, error) {
    order, err := getOrder(ctx, params.ID)
    if err != nil {
        return nil, err
    }
    
    // This becomes an RPC call - Encore handles it
    orderUser, err := user.GetUser(ctx, &user.GetUserParams{ID: order.UserID})
    if err != nil {
        return nil, err
    }
    
    return &OrderWithUser{Order: order, User: orderUser}, nil
}
```

## When to Split Services

Split when you have:

| Signal | Action |
|--------|--------|
| Different scaling needs | Split (e.g., auth vs analytics) |
| Different deployment cycles | Split |
| Clear domain boundaries | Split |
| Shared database tables | Keep together |
| Tightly coupled logic | Keep together |
| Just organizing code | Use sub-packages, not services |

## Internal Helpers (Non-Service Packages)

Create packages without `//encore:api` endpoints for shared code:

```
my-app/
├── user/
│   └── user.go       # Service (has API)
├── order/
│   └── order.go      # Service (has API)
└── internal/
    ├── util/
    │   └── util.go   # Not a service (no API)
    └── validation/
        └── validate.go
```

## Guidelines

- A package becomes a service when it has `//encore:api` endpoints
- Services cannot be nested within other services
- Start with one service, split when there's a clear reason
- Cross-service calls look like regular function calls
- Each service can have its own database
- Package names should be lowercase, descriptive
- Don't create services just for code organization - use sub-packages instead
