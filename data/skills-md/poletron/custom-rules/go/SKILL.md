---
name: go
description: >
  Go best practices, effective patterns, and API development.
  Trigger: When writing Go code, APIs, or microservices.
license: Apache-2.0
metadata:
  author: poletron
  version: "1.0"
  scope: [root]
  auto_invoke: "Working with go"

## When to Use

Use this skill when:
- Writing Go applications or services
- Building REST APIs or gRPC services
- Implementing concurrent patterns
- Following Go idioms and conventions

---

## Critical Patterns

### Error Handling (REQUIRED)

```go
// ✅ ALWAYS: Explicit error handling
result, err := doSomething()
if err != nil {
    return fmt.Errorf("doSomething failed: %w", err)
}

// ❌ NEVER: Ignore errors
result, _ := doSomething()
```

### Naming Conventions (REQUIRED)

```go
// ✅ ALWAYS: Short, clear names
func (u *User) Name() string { return u.name }

// Package-level: unexported unless needed
type userService struct { ... }  // internal
type UserService struct { ... }  // exported

// ❌ NEVER: Java-style names
func (user *User) GetUserName() string { ... }
```

### Context Propagation (REQUIRED)

```go
// ✅ ALWAYS: Pass context as first parameter
func GetUser(ctx context.Context, id string) (*User, error) {
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    default:
        return db.FindUser(ctx, id)
    }
}
```

---

## Decision Tree

```
Need to share state?        → Use channels, not shared memory
Need cancellation?          → Use context.Context
Need cleanup?               → Use defer
Need interface?             → Define where used, not implemented
Need configuration?         → Use functional options
```

---

## Code Examples

### Functional Options

```go
type ServerOption func(*Server)

func WithPort(port int) ServerOption {
    return func(s *Server) {
        s.port = port
    }
}

func NewServer(opts ...ServerOption) *Server {
    s := &Server{port: 8080}
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage
server := NewServer(WithPort(9000))
```

### Goroutines with Error Group

```go
import "golang.org/x/sync/errgroup"

g, ctx := errgroup.WithContext(ctx)

g.Go(func() error {
    return fetchUsers(ctx)
})

g.Go(func() error {
    return fetchOrders(ctx)
})

if err := g.Wait(); err != nil {
    return err
}
```

---

## Commands

```bash
go mod init myapp            # Initialize module
go run .                     # Run application
go build -o bin/app .        # Build binary
go test ./...                # Run all tests
go test -race ./...          # Race detection
golangci-lint run            # Linting
```

---

## Resources

- **API Best Practices**: [api-best-practices.md](api-best-practices.md)
- **Effective Go**: [effective-go.md](effective-go.md)
- **Microservices**: [microservices.md](microservices.md)
