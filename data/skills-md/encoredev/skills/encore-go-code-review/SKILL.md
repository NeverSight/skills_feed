---
name: encore-go-code-review
description: Review Encore Go code for best practices.
---

# Encore Go Code Review

## Instructions

When reviewing Encore Go code, check for these common issues:

## Critical Issues

### 1. Infrastructure Inside Functions

```go
// WRONG: Infrastructure declared inside function
func setup() {
    db := sqldb.NewDatabase("mydb", sqldb.DatabaseConfig{...})
    topic := pubsub.NewTopic[*Event]("events", pubsub.TopicConfig{...})
}

// CORRECT: Package level declaration
var db = sqldb.NewDatabase("mydb", sqldb.DatabaseConfig{
    Migrations: "./migrations",
})

var topic = pubsub.NewTopic[*Event]("events", pubsub.TopicConfig{
    DeliveryGuarantee: pubsub.AtLeastOnce,
})
```

### 2. Missing Context Parameter

```go
// WRONG: Missing context
//encore:api public method=GET path=/users/:id
func GetUser(params *GetUserParams) (*User, error) {
    // ...
}

// CORRECT: Context as first parameter
//encore:api public method=GET path=/users/:id
func GetUser(ctx context.Context, params *GetUserParams) (*User, error) {
    // ...
}
```

### 3. SQL Injection Risk

```go
// WRONG: String interpolation
query := fmt.Sprintf("SELECT * FROM users WHERE email = '%s'", email)
rows, err := db.Query(ctx, query)

// CORRECT: Parameterized query
rows, err := sqldb.Query[User](ctx, db, `
    SELECT * FROM users WHERE email = $1
`, email)
```

### 4. Wrong Return Types

```go
// WRONG: Returning non-pointer struct
//encore:api public method=GET path=/users/:id
func GetUser(ctx context.Context, params *GetUserParams) (User, error) {
    // ...
}

// CORRECT: Return pointer to struct
//encore:api public method=GET path=/users/:id
func GetUser(ctx context.Context, params *GetUserParams) (*User, error) {
    // ...
}
```

### 5. Ignoring Errors

```go
// WRONG: Ignoring error
user, _ := sqldb.QueryRow[User](ctx, db, query, id)

// CORRECT: Handle error
user, err := sqldb.QueryRow[User](ctx, db, query, id)
if err != nil {
    return nil, err
}
```

## Warning Issues

### 6. Not Checking for ErrNoRows

```go
// RISKY: Returns nil without proper error
func getUser(ctx context.Context, id string) (*User, error) {
    user, err := sqldb.QueryRow[User](ctx, db, `
        SELECT * FROM users WHERE id = $1
    `, id)
    if err != nil {
        return nil, err  // ErrNoRows returns generic error
    }
    return user, nil
}

// BETTER: Check for not found specifically
import "errors"

func getUser(ctx context.Context, id string) (*User, error) {
    user, err := sqldb.QueryRow[User](ctx, db, `
        SELECT * FROM users WHERE id = $1
    `, id)
    if errors.Is(err, sqldb.ErrNoRows) {
        return nil, &errs.Error{
            Code:    errs.NotFound,
            Message: "user not found",
        }
    }
    if err != nil {
        return nil, err
    }
    return user, nil
}
```

### 7. Public Internal Endpoints

```go
// CHECK: Should this cron endpoint be public?
//encore:api public method=POST path=/internal/cleanup
func CleanupJob(ctx context.Context) error {
    // ...
}

// BETTER: Use private for internal endpoints
//encore:api private
func CleanupJob(ctx context.Context) error {
    // ...
}
```

### 8. Non-Idempotent Subscription Handlers

```go
// RISKY: Not idempotent (pubsub has at-least-once delivery)
var _ = pubsub.NewSubscription(OrderCreated, "process-order",
    pubsub.SubscriptionConfig[*OrderCreatedEvent]{
        Handler: func(ctx context.Context, event *OrderCreatedEvent) error {
            return chargeCustomer(ctx, event.OrderID)  // Could charge twice!
        },
    },
)

// SAFER: Check before processing
var _ = pubsub.NewSubscription(OrderCreated, "process-order",
    pubsub.SubscriptionConfig[*OrderCreatedEvent]{
        Handler: func(ctx context.Context, event *OrderCreatedEvent) error {
            order, err := getOrder(ctx, event.OrderID)
            if err != nil {
                return err
            }
            if order.Status != "pending" {
                return nil  // Already processed
            }
            return chargeCustomer(ctx, event.OrderID)
        },
    },
)
```

### 9. Not Closing Query Rows

```go
// WRONG: Rows not closed
func listUsers(ctx context.Context) ([]*User, error) {
    rows, err := sqldb.Query[User](ctx, db, `SELECT * FROM users`)
    if err != nil {
        return nil, err
    }
    // Missing: defer rows.Close()
    
    var users []*User
    for rows.Next() {
        users = append(users, rows.Value())
    }
    return users, nil
}

// CORRECT: Always close rows
func listUsers(ctx context.Context) ([]*User, error) {
    rows, err := sqldb.Query[User](ctx, db, `SELECT * FROM users`)
    if err != nil {
        return nil, err
    }
    defer rows.Close()
    
    var users []*User
    for rows.Next() {
        users = append(users, rows.Value())
    }
    return users, rows.Err()
}
```

## Review Checklist

- [ ] All infrastructure at package level
- [ ] All API endpoints have `context.Context` as first parameter
- [ ] SQL uses parameterized queries (`$1`, `$2`, etc.)
- [ ] Response types are pointers
- [ ] Errors are handled, not ignored
- [ ] `sqldb.ErrNoRows` checked where appropriate
- [ ] Internal endpoints use `private` not `public`
- [ ] Subscription handlers are idempotent
- [ ] Query rows are closed with `defer rows.Close()`
- [ ] Migrations follow naming convention (`1_name.up.sql`)

## Output Format

When reviewing, report issues as:

```
[CRITICAL] [file:line] Description of issue
[WARNING] [file:line] Description of concern  
[GOOD] Notable good practice observed
```
