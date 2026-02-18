---
name: encore-go-database
description: Database queries and migrations with Encore Go.
---

# Encore Go Database Operations

## Instructions

### Database Setup

```go
package user

import "encore.dev/storage/sqldb"

var db = sqldb.NewDatabase("userdb", sqldb.DatabaseConfig{
    Migrations: "./migrations",
})
```

## Query Methods

Encore provides type-safe query methods using generics.

### `Query` - Multiple Rows

```go
type User struct {
    ID    string
    Email string
    Name  string
}

func listActiveUsers(ctx context.Context) ([]*User, error) {
    rows, err := sqldb.Query[User](ctx, db, `
        SELECT id, email, name FROM users WHERE active = true
    `)
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

### `QueryRow` - Single Row

```go
func getUser(ctx context.Context, id string) (*User, error) {
    user, err := sqldb.QueryRow[User](ctx, db, `
        SELECT id, email, name FROM users WHERE id = $1
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

### `Exec` - No Return Value

For INSERT, UPDATE, DELETE operations:

```go
func createUser(ctx context.Context, email, name string) error {
    _, err := sqldb.Exec(ctx, db, `
        INSERT INTO users (id, email, name)
        VALUES ($1, $2, $3)
    `, generateID(), email, name)
    return err
}

func updateUser(ctx context.Context, id, name string) error {
    _, err := sqldb.Exec(ctx, db, `
        UPDATE users SET name = $1 WHERE id = $2
    `, name, id)
    return err
}

func deleteUser(ctx context.Context, id string) error {
    _, err := sqldb.Exec(ctx, db, `
        DELETE FROM users WHERE id = $1
    `, id)
    return err
}
```

## Migrations

### File Structure

```
user/
└── migrations/
    ├── 1_create_users.up.sql
    ├── 2_add_posts.up.sql
    └── 3_add_indexes.up.sql
```

### Naming Convention

- Start with a number (1, 2, etc.)
- Followed by underscore and description
- End with `.up.sql`
- Numbers must be sequential

### Example Migration

```sql
-- migrations/1_create_users.up.sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
```

## Transactions

```go
func transferFunds(ctx context.Context, fromID, toID string, amount int) error {
    tx, err := db.Begin(ctx)
    if err != nil {
        return err
    }
    defer tx.Rollback()  // No-op if committed
    
    _, err = tx.Exec(ctx, `
        UPDATE accounts SET balance = balance - $1 WHERE id = $2
    `, amount, fromID)
    if err != nil {
        return err
    }
    
    _, err = tx.Exec(ctx, `
        UPDATE accounts SET balance = balance + $1 WHERE id = $2
    `, amount, toID)
    if err != nil {
        return err
    }
    
    return tx.Commit()
}
```

## Struct Mapping

Query results map to struct fields by name (case-insensitive) or `sql` tag:

```go
type User struct {
    ID        string    `sql:"id"`
    Email     string    `sql:"email"`
    Name      string    `sql:"name"`
    CreatedAt time.Time `sql:"created_at"`
}

// Columns: id, email, name, created_at
// Will map correctly to struct fields
```

## SQL Injection Protection

Always use parameterized queries:

```go
// SAFE - values are parameterized
user, err := sqldb.QueryRow[User](ctx, db, `
    SELECT * FROM users WHERE email = $1
`, email)

// WRONG - SQL injection risk
query := fmt.Sprintf("SELECT * FROM users WHERE email = '%s'", email)
```

## Error Handling

```go
import (
    "errors"
    "encore.dev/storage/sqldb"
    "encore.dev/beta/errs"
)

func getUser(ctx context.Context, id string) (*User, error) {
    user, err := sqldb.QueryRow[User](ctx, db, `
        SELECT id, email, name FROM users WHERE id = $1
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

## Guidelines

- Always use parameterized queries (`$1`, `$2`, etc.)
- Use generics with `sqldb.Query[T]` and `sqldb.QueryRow[T]`
- Check for `sqldb.ErrNoRows` when expecting a single row
- Migrations are applied automatically on startup
- Database names should be lowercase, descriptive
- Each service typically has its own database
- Use transactions for operations that must be atomic
