---
name: golang-database-patterns
description: "Go database integration patterns using sqlx, pgx, and migration tools like golang-migrate"
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Master Go database patterns with sqlx, pgx, and golang-migrate for type-safe queries, migrations, and production-ready data access layers"
    when_to_use: "Building CRUD operations, managing schema evolution, implementing repository patterns, handling transactions, optimizing connection pools, testing database code"
    quick_start: "1. Choose library (database/sql, sqlx, pgx) 2. Set up connection pooling 3. Implement repository pattern 4. Handle transactions with context 5. Manage migrations with golang-migrate"
  token_estimate:
    entry: 150
    full: 4800
context_limit: 700
tags:
  - database
  - golang
  - sqlx
  - pgx
  - migrations
  - repository-pattern
  - sql
requires_tools: []
---

# Go Database Patterns

## Overview

Go's database ecosystem provides multiple layers of abstraction for SQL database integration. From the standard library's `database/sql` to enhanced libraries like `sqlx` and PostgreSQL-optimized `pgx`, developers can choose the right tool for their performance and ergonomics needs.

**Key Features:**
- 🔌 **database/sql**: Standard interface for any SQL database
- 🚀 **sqlx**: Convenience methods with struct scanning and named queries
- 🐘 **pgx**: PostgreSQL-native driver with maximum performance
- 📦 **Repository Pattern**: Interface-based data access for testability
- 🔄 **Migrations**: Schema versioning with golang-migrate
- ⚡ **Connection Pooling**: Production-ready connection management
- 🔒 **Transaction Safety**: Context-aware transaction handling

## When to Use This Skill

Activate this skill when:
- Building CRUD operations with type safety
- Implementing data access layers for web services
- Managing database schema evolution across environments
- Optimizing database connection pooling for production
- Testing database code with mock repositories
- Handling concurrent database access patterns
- Migrating from ORMs to SQL-first approaches
- Integrating PostgreSQL-specific features (COPY, LISTEN/NOTIFY)

## Core Database Libraries

### Decision Tree: Choosing Your Database Library

```
┌─────────────────────────────────────┐
│ What database are you using?       │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
PostgreSQL            Other SQL DB
    │                     │
    ▼                     ▼
┌─────────────────┐   Use database/sql
│ Need max perf?  │   + sqlx for convenience
└─────┬───────────┘
      │
   ┌──┴──┐
  Yes    No
   │      │
  pgx   sqlx + pq driver
```

**Use database/sql when:**
- Working with any SQL database (MySQL, SQLite, PostgreSQL, etc.)
- Need database portability
- Want standard library stability with no dependencies

**Use sqlx when:**
- Want convenience methods (Get, Select, StructScan)
- Need named parameter queries
- Using IN clause expansion
- Prefer less boilerplate than database/sql

**Use pgx when:**
- PostgreSQL-only application
- Need maximum performance (30-50% faster than lib/pq)
- Want advanced PostgreSQL features (COPY, LISTEN/NOTIFY, prepared statement caching)
- Building high-throughput systems

### database/sql: The Standard Foundation

**Core Concepts:**

```go
package main

import (
    "context"
    "database/sql"
    "time"

    _ "github.com/lib/pq" // PostgreSQL driver
)

func setupDB(dsn string) (*sql.DB, error) {
    db, err := sql.Open("postgres", dsn)
    if err != nil {
        return nil, err
    }

    // Connection pooling configuration
    db.SetMaxOpenConns(25)                 // Max open connections
    db.SetMaxIdleConns(5)                  // Max idle connections
    db.SetConnMaxLifetime(5 * time.Minute) // Max connection lifetime
    db.SetConnMaxIdleTime(1 * time.Minute) // Max idle time

    // Verify connection
    ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
    defer cancel()

    if err := db.PingContext(ctx); err != nil {
        return nil, err
    }

    return db, nil
}
```

**Key Patterns:**

```go
// Query single row
func GetUserByID(ctx context.Context, db *sql.DB, id int) (*User, error) {
    var user User
    query := `SELECT id, name, email, created_at FROM users WHERE id = $1`

    err := db.QueryRowContext(ctx, query, id).Scan(
        &user.ID, &user.Name, &user.Email, &user.CreatedAt,
    )

    if err == sql.ErrNoRows {
        return nil, ErrUserNotFound // Custom error
    }
    if err != nil {
        return nil, fmt.Errorf("query user: %w", err)
    }

    return &user, nil
}

// Query multiple rows
func ListActiveUsers(ctx context.Context, db *sql.DB) ([]User, error) {
    query := `SELECT id, name, email, created_at FROM users WHERE active = true`

    rows, err := db.QueryContext(ctx, query)
    if err != nil {
        return nil, fmt.Errorf("query users: %w", err)
    }
    defer rows.Close() // CRITICAL: Always close rows

    var users []User
    for rows.Next() {
        var user User
        if err := rows.Scan(&user.ID, &user.Name, &user.Email, &user.CreatedAt); err != nil {
            return nil, fmt.Errorf("scan user: %w", err)
        }
        users = append(users, user)
    }

    // Check for errors during iteration
    if err := rows.Err(); err != nil {
        return nil, fmt.Errorf("iterate users: %w", err)
    }

    return users, nil
}
```

### sqlx: Ergonomic Extensions

**Installation:**
```bash
go get github.com/jmoiron/sqlx
```

**Core Features:**

```go
package main

import (
    "context"

    "github.com/jmoiron/sqlx"
    _ "github.com/lib/pq"
)

type User struct {
    ID        int       `db:"id"`
    Name      string    `db:"name"`
    Email     string    `db:"email"`
    CreatedAt time.Time `db:"created_at"`
}

// Get single struct
func GetUserByID(ctx context.Context, db *sqlx.DB, id int) (*User, error) {
    var user User
    query := `SELECT id, name, email, created_at FROM users WHERE id = $1`

    err := db.GetContext(ctx, &user, query, id)
    if err == sql.ErrNoRows {
        return nil, ErrUserNotFound
    }
    return &user, err
}

// Select multiple structs
func ListUsers(ctx context.Context, db *sqlx.DB, limit int) ([]User, error) {
    var users []User
    query := `SELECT id, name, email, created_at FROM users LIMIT $1`

    err := db.SelectContext(ctx, &users, query, limit)
    return users, err
}

// Named queries
func FindUsersByName(ctx context.Context, db *sqlx.DB, name string) ([]User, error) {
    var users []User
    query := `SELECT * FROM users WHERE name LIKE :name || '%'`

    nstmt, err := db.PrepareNamedContext(ctx, query)
    if err != nil {
        return nil, err
    }
    defer nstmt.Close()

    err = nstmt.SelectContext(ctx, &users, map[string]interface{}{"name": name})
    return users, err
}

// IN clause expansion
func GetUsersByIDs(ctx context.Context, db *sqlx.DB, ids []int) ([]User, error) {
    var users []User
    query, args, err := sqlx.In(`SELECT * FROM users WHERE id IN (?)`, ids)
    if err != nil {
        return nil, err
    }

    // Rebind for PostgreSQL ($1, $2, ...) vs MySQL (?, ?, ...)
    query = db.Rebind(query)

    err = db.SelectContext(ctx, &users, query, args...)
    return users, err
}
```

### pgx: PostgreSQL-Native Performance

**Installation:**
```bash
go get github.com/jackc/pgx/v5
go get github.com/jackc/pgx/v5/pgxpool
```

**Connection Pool Setup:**

```go
package main

import (
    "context"
    "fmt"

    "github.com/jackc/pgx/v5/pgxpool"
)

func setupPgxPool(ctx context.Context, dsn string) (*pgxpool.Pool, error) {
    config, err := pgxpool.ParseConfig(dsn)
    if err != nil {
        return nil, fmt.Errorf("parse config: %w", err)
    }

    // Connection pool tuning
    config.MaxConns = 25
    config.MinConns = 5
    config.MaxConnLifetime = 1 * time.Hour
    config.MaxConnIdleTime = 30 * time.Minute
    config.HealthCheckPeriod = 1 * time.Minute

    pool, err := pgxpool.NewWithConfig(ctx, config)
    if err != nil {
        return nil, fmt.Errorf("create pool: %w", err)
    }

    // Verify connectivity
    if err := pool.Ping(ctx); err != nil {
        return nil, fmt.Errorf("ping: %w", err)
    }

    return pool, nil
}
```

**Query Patterns:**

```go
// Query single row
func GetUser(ctx context.Context, pool *pgxpool.Pool, id int) (*User, error) {
    var user User
    query := `SELECT id, name, email, created_at FROM users WHERE id = $1`

    err := pool.QueryRow(ctx, query, id).Scan(
        &user.ID, &user.Name, &user.Email, &user.CreatedAt,
    )

    if err == pgx.ErrNoRows {
        return nil, ErrUserNotFound
    }
    return &user, err
}

// Batch operations (pgx-specific optimization)
func BatchInsertUsers(ctx context.Context, pool *pgxpool.Pool, users []User) error {
    batch := &pgx.Batch{}
    query := `INSERT INTO users (name, email) VALUES ($1, $2)`

    for _, user := range users {
        batch.Queue(query, user.Name, user.Email)
    }

    results := pool.SendBatch(ctx, batch)
    defer results.Close()

    for range users {
        _, err := results.Exec()
        if err != nil {
            return fmt.Errorf("batch insert: %w", err)
        }
    }

    return nil
}

// COPY for bulk inserts (10x faster than INSERT)
func BulkCopyUsers(ctx context.Context, pool *pgxpool.Pool, users []User) error {
    _, err := pool.CopyFrom(
        ctx,
        pgx.Identifier{"users"},
        []string{"name", "email"},
        pgx.CopyFromSlice(len(users), func(i int) ([]interface{}, error) {
            return []interface{}{users[i].Name, users[i].Email}, nil
        }),
    )
    return err
}
```

## Repository Pattern Implementation

### Interface-Based Design

```go
package repository

import (
    "context"
    "database/sql"
)

// UserRepository defines data access interface
type UserRepository interface {
    Create(ctx context.Context, user *User) error
    GetByID(ctx context.Context, id int) (*User, error)
    GetByEmail(ctx context.Context, email string) (*User, error)
    Update(ctx context.Context, user *User) error
    Delete(ctx context.Context, id int) error
    List(ctx context.Context, filters ListFilters) ([]User, error)
}

// PostgresUserRepository implements UserRepository
type PostgresUserRepository struct {
    db *sqlx.DB
}

func NewPostgresUserRepository(db *sqlx.DB) *PostgresUserRepository {
    return &PostgresUserRepository{db: db}
}

func (r *PostgresUserRepository) Create(ctx context.Context, user *User) error {
    query := `
        INSERT INTO users (name, email, password_hash)
        VALUES ($1, $2, $3)
        RETURNING id, created_at
    `

    err := r.db.QueryRowContext(
        ctx, query,
        user.Name, user.Email, user.PasswordHash,
    ).Scan(&user.ID, &user.CreatedAt)

    if err != nil {
        return fmt.Errorf("insert user: %w", err)
    }
    return nil
}

func (r *PostgresUserRepository) GetByID(ctx context.Context, id int) (*User, error) {
    var user User
    query := `SELECT id, name, email, created_at, updated_at FROM users WHERE id = $1`

    err := r.db.GetContext(ctx, &user, query, id)
    if err == sql.ErrNoRows {
        return nil, ErrUserNotFound
    }
    if err != nil {
        return nil, fmt.Errorf("get user: %w", err)
    }
    return &user, nil
}

func (r *PostgresUserRepository) Update(ctx context.Context, user *User) error {
    query := `
        UPDATE users
        SET name = $1, email = $2, updated_at = NOW()
        WHERE id = $3
        RETURNING updated_at
    `

    err := r.db.QueryRowContext(
        ctx, query,
        user.Name, user.Email, user.ID,
    ).Scan(&user.UpdatedAt)

    if err == sql.ErrNoRows {
        return ErrUserNotFound
    }
    return err
}

func (r *PostgresUserRepository) Delete(ctx context.Context, id int) error {
    query := `DELETE FROM users WHERE id = $1`
    result, err := r.db.ExecContext(ctx, query, id)
    if err != nil {
        return fmt.Errorf("delete user: %w", err)
    }

    rows, err := result.RowsAffected()
    if err != nil {
        return err
    }

    if rows == 0 {
        return ErrUserNotFound
    }
    return nil
}
```

### Testing with Mock Repository

```go
package repository_test

import (
    "context"
    "testing"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
)

// MockUserRepository for testing
type MockUserRepository struct {
    mock.Mock
}

func (m *MockUserRepository) GetByID(ctx context.Context, id int) (*User, error) {
    args := m.Called(ctx, id)
    if args.Get(0) == nil {
        return nil, args.Error(1)
    }
    return args.Get(0).(*User), args.Error(1)
}

func TestUserService_GetUser(t *testing.T) {
    mockRepo := new(MockUserRepository)
    service := NewUserService(mockRepo)

    expectedUser := &User{ID: 1, Name: "Alice", Email: "alice@example.com"}
    mockRepo.On("GetByID", mock.Anything, 1).Return(expectedUser, nil)

    user, err := service.GetUser(context.Background(), 1)

    assert.NoError(t, err)
    assert.Equal(t, expectedUser, user)
    mockRepo.AssertExpectations(t)
}
```

## Transaction Handling

### Basic Transaction Pattern

```go
func (r *PostgresUserRepository) UpdateWithHistory(ctx context.Context, user *User) error {
    tx, err := r.db.BeginTxx(ctx, nil)
    if err != nil {
        return fmt.Errorf("begin tx: %w", err)
    }
    defer tx.Rollback() // Safe to call even after commit

    // Update user
    query := `UPDATE users SET name = $1, email = $2 WHERE id = $3`
    _, err = tx.ExecContext(ctx, query, user.Name, user.Email, user.ID)
    if err != nil {
        return fmt.Errorf("update user: %w", err)
    }

    // Insert history record
    historyQuery := `INSERT INTO user_history (user_id, name, email, changed_at) VALUES ($1, $2, $3, NOW())`
    _, err = tx.ExecContext(ctx, historyQuery, user.ID, user.Name, user.Email)
    if err != nil {
        return fmt.Errorf("insert history: %w", err)
    }

    if err := tx.Commit(); err != nil {
        return fmt.Errorf("commit tx: %w", err)
    }

    return nil
}
```

### Transaction Isolation Levels

```go
func (r *PostgresUserRepository) TransferBalance(ctx context.Context, fromID, toID int, amount float64) error {
    // Use serializable isolation for financial transactions
    txOpts := &sql.TxOptions{
        Isolation: sql.LevelSerializable,
        ReadOnly:  false,
    }

    tx, err := r.db.BeginTxx(ctx, txOpts)
    if err != nil {
        return err
    }
    defer tx.Rollback()

    // Deduct from sender
    _, err = tx.ExecContext(ctx,
        `UPDATE accounts SET balance = balance - $1 WHERE user_id = $2 AND balance >= $1`,
        amount, fromID,
    )
    if err != nil {
        return fmt.Errorf("deduct balance: %w", err)
    }

    // Add to receiver
    _, err = tx.ExecContext(ctx,
        `UPDATE accounts SET balance = balance + $1 WHERE user_id = $2`,
        amount, toID,
    )
    if err != nil {
        return fmt.Errorf("add balance: %w", err)
    }

    return tx.Commit()
}
```

### Retry Logic for Serialization Failures

```go
func WithRetry(ctx context.Context, maxRetries int, fn func() error) error {
    for i := 0; i < maxRetries; i++ {
        err := fn()
        if err == nil {
            return nil
        }

        // Check for serialization error (PostgreSQL error code 40001)
        var pgErr *pgconn.PgError
        if errors.As(err, &pgErr) && pgErr.Code == "40001" {
            // Exponential backoff
            time.Sleep(time.Duration(i+1) * 100 * time.Millisecond)
            continue
        }

        return err // Non-retryable error
    }
    return fmt.Errorf("max retries exceeded")
}

// Usage
err := WithRetry(ctx, 3, func() error {
    return r.TransferBalance(ctx, fromID, toID, amount)
})
```

## Database Migrations

### Decision Tree: Migration Tools

```
┌─────────────────────────────────────┐
│ Migration tool selection            │
└──────────────┬──────────────────────┘
               │
    ┌──────────┴──────────┐
    │                     │
Simple SQL           Complex logic
migrations          (Go code needed)
    │                     │
    ▼                     ▼
golang-migrate         goose
(SQL only)        (Go + SQL migrations)
```

**Use golang-migrate when:**
- Pure SQL migrations (no custom Go logic)
- Need CLI tool for manual migrations
- Want clean separation of schema and application
- Industry standard (most popular)

**Use goose when:**
- Need Go code in migrations (data transformations)
- Want flexibility of both SQL and Go
- Need custom migration logic

**Use sql-migrate when:**
- Using sqlx already
- Want embedded migrations in binary
- Need programmatic migration control

### golang-migrate Setup

**Installation:**
```bash
# CLI tool
go install -tags 'postgres' github.com/golang-migrate/migrate/v4/cmd/migrate@latest

# Library
go get -u github.com/golang-migrate/migrate/v4
go get -u github.com/golang-migrate/migrate/v4/database/postgres
go get -u github.com/golang-migrate/migrate/v4/source/file
```

**Migration Files:**

```bash
# Create migration
migrate create -ext sql -dir migrations -seq create_users_table

# Generates:
# migrations/000001_create_users_table.up.sql
# migrations/000001_create_users_table.down.sql
```

**000001_create_users_table.up.sql:**
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

**000001_create_users_table.down.sql:**
```sql
DROP INDEX IF EXISTS idx_users_email;
DROP TABLE IF EXISTS users;
```

**Programmatic Migration:**

```go
package main

import (
    "fmt"

    "github.com/golang-migrate/migrate/v4"
    _ "github.com/golang-migrate/migrate/v4/database/postgres"
    _ "github.com/golang-migrate/migrate/v4/source/file"
)

func runMigrations(databaseURL, migrationsPath string) error {
    m, err := migrate.New(
        fmt.Sprintf("file://%s", migrationsPath),
        databaseURL,
    )
    if err != nil {
        return fmt.Errorf("create migrate instance: %w", err)
    }
    defer m.Close()

    if err := m.Up(); err != nil && err != migrate.ErrNoChange {
        return fmt.Errorf("run migrations: %w", err)
    }

    version, dirty, err := m.Version()
    if err != nil {
        return err
    }

    fmt.Printf("Migration complete. Version: %d, Dirty: %v\n", version, dirty)
    return nil
}
```

**CLI Usage:**
```bash
# Apply all up migrations
migrate -path migrations -database "postgres://user:pass@localhost:5432/db?sslmode=disable" up

# Rollback one migration
migrate -path migrations -database $DATABASE_URL down 1

# Go to specific version
migrate -path migrations -database $DATABASE_URL goto 5

# Check current version
migrate -path migrations -database $DATABASE_URL version
```

## NULL Handling

### Using sql.Null* Types

```go
type User struct {
    ID        int            `db:"id"`
    Name      string         `db:"name"`
    Email     string         `db:"email"`
    Phone     sql.NullString `db:"phone"`     // Nullable string
    Age       sql.NullInt64  `db:"age"`       // Nullable int
    UpdatedAt sql.NullTime   `db:"updated_at"` // Nullable timestamp
}

func (r *PostgresUserRepository) GetUser(ctx context.Context, id int) (*User, error) {
    var user User
    err := r.db.GetContext(ctx, &user, `SELECT * FROM users WHERE id = $1`, id)
    if err != nil {
        return nil, err
    }

    // Access nullable fields
    if user.Phone.Valid {
        fmt.Println("Phone:", user.Phone.String)
    }

    return &user, nil
}

// Setting NULL values
func (r *PostgresUserRepository) UpdatePhone(ctx context.Context, userID int, phone *string) error {
    var nullPhone sql.NullString
    if phone != nil {
        nullPhone = sql.NullString{String: *phone, Valid: true}
    }
    // If phone is nil, nullPhone.Valid is false, SQL writes NULL

    query := `UPDATE users SET phone = $1 WHERE id = $2`
    _, err := r.db.ExecContext(ctx, query, nullPhone, userID)
    return err
}
```

### Custom Nullable Types (Preferred Pattern)

```go
// Custom nullable type with JSON marshaling
type NullString struct {
    sql.NullString
}

func (ns NullString) MarshalJSON() ([]byte, error) {
    if !ns.Valid {
        return []byte("null"), nil
    }
    return json.Marshal(ns.String)
}

func (ns *NullString) UnmarshalJSON(data []byte) error {
    if string(data) == "null" {
        ns.Valid = false
        return nil
    }

    var s string
    if err := json.Unmarshal(data, &s); err != nil {
        return err
    }

    ns.String = s
    ns.Valid = true
    return nil
}
```

## Anti-Patterns to Avoid

### ❌ N+1 Query Problem

**Wrong:**
```go
func GetUsersWithPosts(ctx context.Context, db *sqlx.DB) ([]UserWithPosts, error) {
    var users []User
    db.SelectContext(ctx, &users, `SELECT * FROM users`)

    for i, user := range users {
        var posts []Post
        // N+1: One query per user!
        db.SelectContext(ctx, &posts, `SELECT * FROM posts WHERE user_id = $1`, user.ID)
        users[i].Posts = posts
    }
    return users, nil
}
```

**Correct:**
```go
func GetUsersWithPosts(ctx context.Context, db *sqlx.DB) ([]UserWithPosts, error) {
    // Single query with JOIN
    query := `
        SELECT u.id, u.name, p.id as post_id, p.title, p.content
        FROM users u
        LEFT JOIN posts p ON p.user_id = u.id
        ORDER BY u.id
    `

    rows, err := db.QueryContext(ctx, query)
    if err != nil {
        return nil, err
    }
    defer rows.Close()

    usersMap := make(map[int]*UserWithPosts)
    for rows.Next() {
        var userID int
        var userName string
        var postID sql.NullInt64
        var title, content sql.NullString

        rows.Scan(&userID, &userName, &postID, &title, &content)

        if _, exists := usersMap[userID]; !exists {
            usersMap[userID] = &UserWithPosts{ID: userID, Name: userName}
        }

        if postID.Valid {
            usersMap[userID].Posts = append(usersMap[userID].Posts, Post{
                ID:      int(postID.Int64),
                Title:   title.String,
                Content: content.String,
            })
        }
    }

    result := make([]UserWithPosts, 0, len(usersMap))
    for _, user := range usersMap {
        result = append(result, *user)
    }
    return result, nil
}
```

### ❌ Missing Connection Pool Configuration

**Wrong:**
```go
db, _ := sql.Open("postgres", dsn)
// Uses defaults: unlimited connections, no timeouts
```

**Correct:**
```go
db, _ := sql.Open("postgres", dsn)

// Production-ready pool settings
db.SetMaxOpenConns(25)                      // Limit total connections
db.SetMaxIdleConns(5)                       // Limit idle connections
db.SetConnMaxLifetime(5 * time.Minute)      // Recycle old connections
db.SetConnMaxIdleTime(1 * time.Minute)      // Close idle connections
```

### ❌ Ignoring Context Cancellation

**Wrong:**
```go
func SlowQuery(db *sql.DB) error {
    // No context - query runs until completion even if client disconnects
    rows, err := db.Query("SELECT * FROM huge_table")
    // ...
}
```

**Correct:**
```go
func SlowQuery(ctx context.Context, db *sql.DB) error {
    // Context cancellation propagates to database
    rows, err := db.QueryContext(ctx, "SELECT * FROM huge_table")
    // If ctx is canceled, query is terminated
}
```

### ❌ Not Closing Rows

**Wrong:**
```go
func GetUsers(db *sql.DB) ([]User, error) {
    rows, _ := db.Query("SELECT * FROM users")
    // Missing rows.Close() - connection leak!
    var users []User
    for rows.Next() {
        // ...
    }
    return users, nil
}
```

**Correct:**
```go
func GetUsers(db *sql.DB) ([]User, error) {
    rows, err := db.Query("SELECT * FROM users")
    if err != nil {
        return nil, err
    }
    defer rows.Close() // CRITICAL: Always defer Close

    var users []User
    for rows.Next() {
        // ...
    }
    return users, rows.Err() // Check for iteration errors
}
```

### ❌ SQL Injection Vulnerability

**Wrong:**
```go
func FindUser(db *sql.DB, email string) (*User, error) {
    // NEVER concatenate user input into SQL!
    query := fmt.Sprintf("SELECT * FROM users WHERE email = '%s'", email)
    // Vulnerable to: ' OR '1'='1
    row := db.QueryRow(query)
    // ...
}
```

**Correct:**
```go
func FindUser(db *sql.DB, email string) (*User, error) {
    // Use parameterized queries
    query := "SELECT * FROM users WHERE email = $1"
    row := db.QueryRow(query, email) // Safe
    // ...
}
```

### ❌ Ignoring Transaction Errors

**Wrong:**
```go
func UpdateUser(db *sql.DB, user *User) error {
    tx, _ := db.Begin()
    tx.Exec("UPDATE users SET name = $1 WHERE id = $2", user.Name, user.ID)
    tx.Commit() // Ignores errors - data may not be committed!
    return nil
}
```

**Correct:**
```go
func UpdateUser(db *sql.DB, user *User) error {
    tx, err := db.Begin()
    if err != nil {
        return err
    }
    defer tx.Rollback() // Rollback if commit not reached

    _, err = tx.Exec("UPDATE users SET name = $1 WHERE id = $2", user.Name, user.ID)
    if err != nil {
        return err
    }

    return tx.Commit() // Check commit error
}
```

## Connection Pooling Best Practices

### Tuning Parameters

```go
func OptimizeDatabasePool(db *sql.DB, config PoolConfig) {
    // MaxOpenConns: Total connections (in-use + idle)
    // Rule of thumb: (CPU cores * 2) + disk spindles
    // Cloud databases often limit connections (e.g., AWS RDS: 100-5000)
    db.SetMaxOpenConns(config.MaxOpen) // Example: 25 for small app

    // MaxIdleConns: Idle connections ready for reuse
    // Should be lower than MaxOpenConns
    // Too low: frequent reconnections (slow)
    // Too high: wasted resources
    db.SetMaxIdleConns(config.MaxIdle) // Example: 5-10

    // ConnMaxLifetime: Maximum age of any connection
    // Prevents stale connections to load balancers
    // Recommended: 5-15 minutes
    db.SetConnMaxLifetime(config.MaxLifetime)

    // ConnMaxIdleTime: Close idle connections after this duration
    // Saves resources during low traffic
    // Recommended: 1-5 minutes
    db.SetConnMaxIdleTime(config.MaxIdleTime)
}

type PoolConfig struct {
    MaxOpen      int
    MaxIdle      int
    MaxLifetime  time.Duration
    MaxIdleTime  time.Duration
}

// Example configurations
var (
    // Development: Low resource usage
    DevConfig = PoolConfig{
        MaxOpen:     10,
        MaxIdle:     2,
        MaxLifetime: 10 * time.Minute,
        MaxIdleTime: 2 * time.Minute,
    }

    // Production: High throughput
    ProdConfig = PoolConfig{
        MaxOpen:     25,
        MaxIdle:     10,
        MaxLifetime: 5 * time.Minute,
        MaxIdleTime: 1 * time.Minute,
    }

    // High-traffic API: Maximum performance
    HighTrafficConfig = PoolConfig{
        MaxOpen:     50,
        MaxIdle:     20,
        MaxLifetime: 5 * time.Minute,
        MaxIdleTime: 30 * time.Second,
    }
)
```

### Monitoring Connection Pool

```go
func MonitorConnectionPool(db *sql.DB) {
    stats := db.Stats()

    fmt.Printf("Connection Pool Stats:\n")
    fmt.Printf("  Open Connections: %d\n", stats.OpenConnections)
    fmt.Printf("  In Use: %d\n", stats.InUse)
    fmt.Printf("  Idle: %d\n", stats.Idle)
    fmt.Printf("  Wait Count: %d\n", stats.WaitCount)          // Queries waited for connection
    fmt.Printf("  Wait Duration: %s\n", stats.WaitDuration)    // Total wait time
    fmt.Printf("  Max Idle Closed: %d\n", stats.MaxIdleClosed) // Connections closed due to idle
    fmt.Printf("  Max Lifetime Closed: %d\n", stats.MaxLifetimeClosed)

    // Alert if too many waits (need more connections)
    if stats.WaitCount > 100 {
        fmt.Println("WARNING: High wait count - consider increasing MaxOpenConns")
    }

    // Alert if many idle closures (pool too large)
    if stats.MaxIdleClosed > 1000 {
        fmt.Println("INFO: Many idle closures - consider reducing MaxIdleConns")
    }
}
```

## Testing Database Code

### Using sqlmock for Unit Tests

**Installation:**
```bash
go get github.com/DATA-DOG/go-sqlmock
```

**Example:**

```go
package repository_test

import (
    "context"
    "testing"

    "github.com/DATA-DOG/go-sqlmock"
    "github.com/jmoiron/sqlx"
    "github.com/stretchr/testify/assert"
)

func TestGetUserByID(t *testing.T) {
    // Create mock database
    db, mock, err := sqlmock.New()
    assert.NoError(t, err)
    defer db.Close()

    sqlxDB := sqlx.NewDb(db, "postgres")
    repo := NewPostgresUserRepository(sqlxDB)

    // Expected query and result
    rows := sqlmock.NewRows([]string{"id", "name", "email"}).
        AddRow(1, "Alice", "alice@example.com")

    mock.ExpectQuery("SELECT (.+) FROM users WHERE id = \\$1").
        WithArgs(1).
        WillReturnRows(rows)

    // Execute
    user, err := repo.GetByID(context.Background(), 1)

    // Assert
    assert.NoError(t, err)
    assert.Equal(t, "Alice", user.Name)
    assert.Equal(t, "alice@example.com", user.Email)
    assert.NoError(t, mock.ExpectationsWereMet())
}

func TestGetUserByID_NotFound(t *testing.T) {
    db, mock, err := sqlmock.New()
    assert.NoError(t, err)
    defer db.Close()

    sqlxDB := sqlx.NewDb(db, "postgres")
    repo := NewPostgresUserRepository(sqlxDB)

    mock.ExpectQuery("SELECT (.+) FROM users WHERE id = \\$1").
        WithArgs(999).
        WillReturnError(sql.ErrNoRows)

    user, err := repo.GetByID(context.Background(), 999)

    assert.Nil(t, user)
    assert.ErrorIs(t, err, ErrUserNotFound)
    assert.NoError(t, mock.ExpectationsWereMet())
}
```

### Integration Tests with Real Database

```go
// +build integration

package repository_test

import (
    "context"
    "testing"

    "github.com/jmoiron/sqlx"
    _ "github.com/lib/pq"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/suite"
)

type UserRepositoryIntegrationSuite struct {
    suite.Suite
    db   *sqlx.DB
    repo *PostgresUserRepository
}

func (s *UserRepositoryIntegrationSuite) SetupSuite() {
    // Connect to test database
    db, err := sqlx.Connect("postgres", "postgres://test:test@localhost/testdb?sslmode=disable")
    s.Require().NoError(err)
    s.db = db
    s.repo = NewPostgresUserRepository(db)
}

func (s *UserRepositoryIntegrationSuite) TearDownSuite() {
    s.db.Close()
}

func (s *UserRepositoryIntegrationSuite) SetupTest() {
    // Clean database before each test
    _, err := s.db.Exec("TRUNCATE users RESTART IDENTITY CASCADE")
    s.Require().NoError(err)
}

func (s *UserRepositoryIntegrationSuite) TestCreateUser() {
    user := &User{Name: "Alice", Email: "alice@example.com"}

    err := s.repo.Create(context.Background(), user)

    s.NoError(err)
    s.NotZero(user.ID)
    s.NotZero(user.CreatedAt)
}

func (s *UserRepositoryIntegrationSuite) TestGetUserByID() {
    // Insert test data
    user := &User{Name: "Bob", Email: "bob@example.com"}
    s.repo.Create(context.Background(), user)

    // Test retrieval
    retrieved, err := s.repo.GetByID(context.Background(), user.ID)

    s.NoError(err)
    s.Equal(user.Name, retrieved.Name)
    s.Equal(user.Email, retrieved.Email)
}

func TestUserRepositoryIntegration(t *testing.T) {
    suite.Run(t, new(UserRepositoryIntegrationSuite))
}
```

**Run integration tests:**
```bash
# Skip integration tests by default
go test ./...

# Run only integration tests
go test -tags=integration ./...
```

## Resources and Further Reading

### Official Documentation
- [database/sql Tutorial](https://go.dev/doc/database/sql) - Official Go database guide (2024)
- [sqlx Documentation](https://jmoiron.github.io/sqlx/) - Illustrated guide to sqlx
- [pgx Documentation](https://github.com/jackc/pgx) - PostgreSQL driver and toolkit
- [golang-migrate](https://github.com/golang-migrate/migrate) - Database migration tool

### Best Practices
- [Go Database Best Practices](https://www.alexedwards.net/blog/organising-database-access) - Alex Edwards (2024)
- [Connection Pool Tuning](https://www.alexedwards.net/blog/configuring-sqldb) - Production configuration guide
- [Repository Pattern in Go](https://threedots.tech/post/repository-pattern-in-go/) - Three Dots Labs

### Migration Tools
- [golang-migrate CLI](https://github.com/golang-migrate/migrate/tree/master/cmd/migrate) - Command-line tool
- [goose](https://github.com/pressly/goose) - Alternative with Go and SQL migrations
- [sql-migrate](https://github.com/rubenv/sql-migrate) - Migration tool with sqlx integration

### Testing
- [go-sqlmock](https://github.com/DATA-DOG/go-sqlmock) - SQL mock for unit tests
- [testcontainers-go](https://github.com/testcontainers/testcontainers-go) - Docker containers for integration tests
- [dockertest](https://github.com/ory/dockertest) - Ephemeral databases for testing

### Advanced Topics
- [Handling Database Errors](https://www.alexedwards.net/blog/working-with-database-nulls) - NULL handling patterns
- [PostgreSQL LISTEN/NOTIFY with pgx](https://github.com/jackc/pgx/wiki/PG-Notify-Example) - Real-time notifications
- [Query Builders](https://github.com/Masterminds/squirrel) - Dynamic SQL generation
- [GORM](https://gorm.io/) - Full-featured ORM (alternative approach)

## Summary

Go database patterns prioritize simplicity, type safety, and performance:

**Library Selection:**
- Start with `database/sql` for portability
- Add `sqlx` for convenience and reduced boilerplate
- Use `pgx` for PostgreSQL-specific high-performance applications

**Core Patterns:**
- Repository pattern for testable data access layers
- Context-aware queries for cancellation and timeouts
- Proper transaction handling with defer rollback
- Connection pooling tuned for production workloads

**Migration Strategy:**
- Use `golang-migrate` for version-controlled schema evolution
- Separate up/down migrations for safe rollbacks
- Run migrations programmatically or via CLI

**Avoid Common Pitfalls:**
- N+1 queries (use JOINs or batching)
- Missing connection pool configuration
- SQL injection (always use parameterized queries)
- Not closing rows (defer rows.Close())
- Ignoring context cancellation

**Testing:**
- Unit tests with sqlmock for business logic
- Integration tests with real databases for critical paths
- Repository interfaces for dependency injection

By following these patterns, you'll build robust, performant, and maintainable database layers in Go.
