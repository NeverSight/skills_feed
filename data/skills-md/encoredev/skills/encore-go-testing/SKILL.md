---
name: encore-go-testing
description: Test APIs and services with Encore Go.
---

# Testing Encore Go Applications

## Instructions

Encore Go uses standard Go testing with `encore test`.

### Run Tests

```bash
# Run all tests with Encore (recommended)
encore test ./...

# Run tests for a specific package
encore test ./user/...

# Run with verbose output
encore test -v ./...
```

Using `encore test` instead of `go test` is recommended because it:
- Sets up test databases automatically
- Provides isolated infrastructure per test
- Handles service dependencies

### Test an API Endpoint

```go
// hello/hello_test.go
package hello

import (
    "context"
    "testing"
)

func TestHello(t *testing.T) {
    ctx := context.Background()
    
    resp, err := Hello(ctx)
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    
    if resp.Message != "Hello, World!" {
        t.Errorf("expected 'Hello, World!', got '%s'", resp.Message)
    }
}
```

### Test with Request Parameters

```go
// user/user_test.go
package user

import (
    "context"
    "testing"
)

func TestGetUser(t *testing.T) {
    ctx := context.Background()
    
    user, err := GetUser(ctx, &GetUserParams{ID: "123"})
    if err != nil {
        t.Fatalf("unexpected error: %v", err)
    }
    
    if user.ID != "123" {
        t.Errorf("expected ID '123', got '%s'", user.ID)
    }
}
```

### Test Database Operations

Encore provides isolated test databases:

```go
// user/user_test.go
package user

import (
    "context"
    "testing"
    
    "encore.dev/storage/sqldb"
)

func TestCreateUser(t *testing.T) {
    ctx := context.Background()
    
    // Clean up
    _, _ = sqldb.Exec(ctx, db, "DELETE FROM users")
    
    // Create user
    created, err := CreateUser(ctx, &CreateUserParams{
        Email: "test@example.com",
        Name:  "Test User",
    })
    if err != nil {
        t.Fatalf("failed to create user: %v", err)
    }
    
    // Retrieve and verify
    retrieved, err := GetUser(ctx, &GetUserParams{ID: created.ID})
    if err != nil {
        t.Fatalf("failed to get user: %v", err)
    }
    
    if retrieved.Email != "test@example.com" {
        t.Errorf("expected email 'test@example.com', got '%s'", retrieved.Email)
    }
}
```

### Test Service-to-Service Calls

```go
// order/order_test.go
package order

import (
    "context"
    "testing"
)

func TestCreateOrder(t *testing.T) {
    ctx := context.Background()
    
    // Service calls work normally in tests
    order, err := CreateOrder(ctx, &CreateOrderParams{
        UserID: "user-123",
        Items: []OrderItem{
            {ProductID: "prod-1", Quantity: 2},
        },
    })
    if err != nil {
        t.Fatalf("failed to create order: %v", err)
    }
    
    if order.Status != "pending" {
        t.Errorf("expected status 'pending', got '%s'", order.Status)
    }
}
```

### Test Error Cases

```go
package user

import (
    "context"
    "errors"
    "testing"
    
    "encore.dev/beta/errs"
)

func TestGetUser_NotFound(t *testing.T) {
    ctx := context.Background()
    
    _, err := GetUser(ctx, &GetUserParams{ID: "nonexistent"})
    if err == nil {
        t.Fatal("expected error, got nil")
    }
    
    // Check error code
    var e *errs.Error
    if errors.As(err, &e) {
        if e.Code != errs.NotFound {
            t.Errorf("expected NotFound, got %v", e.Code)
        }
    } else {
        t.Errorf("expected errs.Error, got %T", err)
    }
}
```

### Test Pub/Sub

```go
// notifications/notifications_test.go
package notifications

import (
    "context"
    "testing"
    
    "myapp/events"
)

func TestPublishOrderCreated(t *testing.T) {
    ctx := context.Background()
    
    msgID, err := events.OrderCreated.Publish(ctx, &events.OrderCreatedEvent{
        OrderID: "order-123",
        UserID:  "user-456",
        Total:   9999,
    })
    if err != nil {
        t.Fatalf("failed to publish: %v", err)
    }
    
    if msgID == "" {
        t.Error("expected message ID, got empty string")
    }
}
```

### Test Cron Jobs

Test the underlying function, not the cron schedule:

```go
// cleanup/cleanup_test.go
package cleanup

import (
    "context"
    "testing"
)

func TestCleanupExpiredSessions(t *testing.T) {
    ctx := context.Background()
    
    // Create some expired sessions first
    createExpiredSession(ctx)
    
    // Call the endpoint directly
    err := CleanupExpiredSessions(ctx)
    if err != nil {
        t.Fatalf("cleanup failed: %v", err)
    }
    
    // Verify cleanup happened
    count := countSessions(ctx)
    if count != 0 {
        t.Errorf("expected 0 sessions, got %d", count)
    }
}
```

### Table-Driven Tests

```go
func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name    string
        email   string
        wantErr bool
    }{
        {"valid email", "user@example.com", false},
        {"missing @", "userexample.com", true},
        {"empty", "", true},
        {"valid with subdomain", "user@mail.example.com", false},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := validateEmail(tt.email)
            if (err != nil) != tt.wantErr {
                t.Errorf("validateEmail(%q) error = %v, wantErr %v", tt.email, err, tt.wantErr)
            }
        })
    }
}
```

### Test with Subtests

```go
func TestUserCRUD(t *testing.T) {
    ctx := context.Background()
    var userID string
    
    t.Run("create", func(t *testing.T) {
        user, err := CreateUser(ctx, &CreateUserParams{
            Email: "test@example.com",
            Name:  "Test",
        })
        if err != nil {
            t.Fatalf("create failed: %v", err)
        }
        userID = user.ID
    })
    
    t.Run("read", func(t *testing.T) {
        user, err := GetUser(ctx, &GetUserParams{ID: userID})
        if err != nil {
            t.Fatalf("read failed: %v", err)
        }
        if user.Email != "test@example.com" {
            t.Errorf("wrong email: %s", user.Email)
        }
    })
    
    t.Run("delete", func(t *testing.T) {
        err := DeleteUser(ctx, &DeleteUserParams{ID: userID})
        if err != nil {
            t.Fatalf("delete failed: %v", err)
        }
    })
}
```

### Guidelines

- Use `encore test` to run tests with infrastructure setup
- Each test gets access to real infrastructure (databases, Pub/Sub)
- Test API endpoints by calling them directly as functions
- Service-to-service calls work normally in tests
- Use table-driven tests for testing multiple cases
- Don't mock Encore infrastructure - use the real thing
- Mock external dependencies (third-party APIs, email services, etc.)
