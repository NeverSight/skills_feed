---
name: writing-go
description: Idiomatic Go 1.25+ development. Use when writing Go code, designing APIs, discussing Go patterns, or reviewing Go implementations. Emphasizes stdlib, concrete types, simple error handling, and minimal dependencies.
user-invocable: false
context: fork
agent: go-engineer
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

# Go Development (1.25+)

## Core Philosophy

1. **Stdlib and Mature Libraries First**
   - Always prefer Go stdlib solutions
   - External deps only when stdlib is insufficient
   - Choose mature, well-maintained libs when needed
   - Don't reinvent the wheel—use existing solutions

2. **Concrete Types Over `any`**
   - Never use `interface{}` or `any` when concrete type works
   - Generics for reusable utilities, concrete types for business logic
   - Accept interfaces, return structs

3. **Private Interfaces at Consumer**
   - Define interfaces private (lowercase) where used
   - Decouples code, enables testing
   - Implementation returns concrete types

4. **Flat Control Flow**
   - Early returns, guard clauses
   - No nested IFs—max 2 levels
   - Switch for multi-case logic

5. **Explicit Error Handling**
   - Always wrap with context
   - Use `errors.Is()`/`errors.As()`
   - No bare `return err`

## Quick Patterns

### Private Interface at Consumer

```go
// service/user.go - private interface where it's USED
type userStore interface {
    Get(ctx context.Context, id string) (*User, error)
}

type Service struct {
    store userStore  // accepts interface
}

// repo/postgres.go - returns concrete type
func NewPostgresStore(db *sql.DB) *PostgresStore {
    return &PostgresStore{db: db}
}
```

### Flat Control Flow (No Nesting)

```go
// GOOD: guard clauses, early returns
func process(user *User) error {
    if user == nil {
        return ErrNilUser
    }
    if user.Email == "" {
        return ErrMissingEmail
    }
    if !isValidEmail(user.Email) {
        return ErrInvalidEmail
    }
    return doWork(user)
}

// BAD: nested conditions
func process(user *User) error {
    if user != nil {
        if user.Email != "" {
            if isValidEmail(user.Email) {
                return doWork(user)
            }
        }
    }
    return nil
}
```

### Error Handling

```go
if err := doThing(); err != nil {
    return fmt.Errorf("do thing: %w", err)  // always wrap
}

// Sentinel errors
if errors.Is(err, ErrNotFound) {
    return http.StatusNotFound
}
```

### Concrete Types (Avoid `any`)

```go
// GOOD: concrete types
func ProcessUsers(users []User) error { ... }
func GetUserByID(id string) (*User, error) { ... }

// BAD: unnecessary any
func ProcessItems(items []any) error { ... }
func GetByID(id any) (any, error) { ... }
```

### Table-Driven Tests

```go
tests := []struct {
    name    string
    input   string
    want    string
    wantErr bool
}{
    {"valid", "hello", "HELLO", false},
    {"empty", "", "", true},
}
for _, tt := range tests {
    t.Run(tt.name, func(t *testing.T) {
        got, err := Process(tt.input)
        if tt.wantErr {
            require.Error(t, err)
            return
        }
        require.NoError(t, err)
        assert.Equal(t, tt.want, got)
    })
}
```

## Go 1.25 Features

- **testing/synctest**: Deterministic concurrent testing
- **encoding/json/v2**: 3-10x faster (GOEXPERIMENT=jsonv2)
- **runtime/trace.FlightRecorder**: Production trace capture
- **Container-aware GOMAXPROCS**: Auto-detects cgroup limits

## References

- [PATTERNS.md](PATTERNS.md) - Detailed code patterns
- [TESTING.md](TESTING.md) - Testing with testify/mockery
- [CLI.md](CLI.md) - CLI application patterns

## Tooling

```bash
go build ./...           # Build
go test -race ./...      # Test with race detector
golangci-lint run        # Lint
mockery --all            # Generate mocks
```
