---
name: golang
description: >-
  Comprehensive Go 1.26 development skill enforcing idiomatic patterns, error wrapping
  with fmt.Errorf %w, small interfaces, table-driven tests. Triggers on "go", "golang",
  ".go file", "write go", "go function", "go struct", "go interface", "go method",
  "go error handling", "errors.Is", "errors.As", "fmt.Errorf", "go concurrency",
  "goroutine", "channel", "sync.Mutex", "errgroup", "context.Context", "go mod",
  "go.mod", "go.sum", "go test", "go build", "go run", "golangci-lint", "go fmt",
  "gofmt", "go vet", "go generate", "go embed", "go template", "http handler",
  "gin", "echo", "chi", "fiber", "gorm", "sqlx", "go project", "go package",
  "go module", "defer", "panic recover", "go slice", "go map", "go pointer".
  PROACTIVE: MUST invoke when writing ANY .go file.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ABOUTME: Go 1.26 idiomatic development skill with automated quality gates
# ABOUTME: Enforces 2025 best practices, pre-commit hooks, and golangci-lint

# Go 1.26 Idiomatic Development

## Quick Reference

| Principle | Rule |
|-----------|------|
| Simplicity | Start with simplest solution; justify every abstraction |
| Explicitness | Clear code paths; no magic |
| Composition | Small interfaces; embedding over inheritance |
| Errors | Values, not exceptions; always wrap with context |
| Functions | ≤50 lines, ≤4 params, single responsibility |
| Duplication | Rule of Three before abstracting |

## 🛑 FILE OPERATION CHECKPOINT (BLOCKING)

**Before EVERY `Write` or `Edit` tool call on a `.go` file:**

```
╔══════════════════════════════════════════════════════════════════╗
║  🛑 STOP - GO SKILL CHECK                                        ║
║                                                                  ║
║  You are about to modify a .go file.                             ║
║                                                                  ║
║  QUESTION: Is /golang skill currently active?                    ║
║                                                                  ║
║  If YES → Proceed with the edit                                  ║
║  If NO  → STOP! Invoke /golang FIRST, then edit                  ║
║                                                                  ║
║  This check applies to:                                          ║
║  ✗ Write tool with file_path ending in .go                       ║
║  ✗ Edit tool with file_path ending in .go                        ║
║  ✗ ANY Go file, regardless of conversation topic                 ║
║                                                                  ║
║  Examples that REQUIRE this skill:                               ║
║  - "add error handling" (edits .go file)                         ║
║  - "fix the test" (edits _test.go file)                          ║
║  - "update the handler" (edits handler.go)                       ║
╚══════════════════════════════════════════════════════════════════╝
```

**Why this matters:** Go code without proper error wrapping (`fmt.Errorf %w`) loses
context. The skill ensures idiomatic patterns and golangci-lint compliance.

## 🔄 RESUMED SESSION CHECKPOINT

**When a session is resumed from context compaction, verify Go development state:**

```
┌─────────────────────────────────────────────────────────────┐
│  SESSION RESUMED - GO SKILL VERIFICATION                    │
│                                                             │
│  Before continuing Go implementation:                       │
│                                                             │
│  1. Was I in the middle of writing Go code?                 │
│     → Check summary for "implementing", "writing", ".go"    │
│                                                             │
│  2. Did I follow all Go skill guidelines?                   │
│     → Explicit error handling with wrapping                 │
│     → Small interfaces defined by consumer                  │
│     → Functions ≤50 lines, ≤4 params                        │
│     → ABOUTME headers on new files                          │
│                                                             │
│  3. Check code quality before continuing:                   │
│     → Run: go build ./...                                   │
│     → Run: golangci-lint run                                │
│                                                             │
│  If implementation was in progress:                         │
│  → Review the partial code for completeness                 │
│  → Ensure all errors are handled and wrapped                │
│  → Verify golangci-lint passes with no warnings             │
│  → Re-invoke /golang if skill context was lost              │
└─────────────────────────────────────────────────────────────┘
```

## Core Philosophy

### The Five Pillars

1. **Simplicity over cleverness** - Start with the simplest solution
2. **Explicit over implicit** - Clear code paths, no magic
3. **Composition over inheritance** - Use interfaces and embedding
4. **Small interfaces** - "The bigger the interface, the weaker the abstraction"
5. **Errors are values** - Handle errors explicitly; don't panic

---

## Abstraction Rules

### Rule 1: Principle of Least Abstraction

**1.1 Default to a Single Function**
- Solve the problem within a single function first
- Do NOT create helper functions, new types, or new packages prematurely

**1.2 Justify Every Abstraction**
- Before creating a new function, struct, or package, justify its existence
- If there's no strong reason to abstract, don't

### Rule 2: Function Design

| Constraint | Limit | Action if Exceeded |
|------------|-------|-------------------|
| Lines | 50 | Decompose into private helpers |
| Parameters | 4 | Group into config struct |
| Return values | 2 | Use named result struct |

**2.1 Single Responsibility**
- If you cannot describe what a function does in one simple sentence, it's doing too much

**2.2 Return Values**
```go
// 1-2 values: return directly
func Parse(s string) (int, error)

// 3+ related values: use struct
type ParseResult struct {
    Value    int
    Consumed int
    Warnings []string
}
func ParseDetailed(s string) (ParseResult, error)
```

### Rule 3: Duplication vs. Abstraction

**3.1 The Rule of Three**
- Do NOT refactor duplicated code on first or second appearance
- Only consider abstraction on third instance

**3.2 Verify True Duplication**
- Confirm duplicated code represents the same core logic
- If similar by coincidence but different business rules, keep separate

### Rule 4: Package and Interface Philosophy

**4.1 Packages Have a Singular Purpose**
- Package should represent a single concept
- DO NOT create "utility", "common", or "helpers" packages

**4.2 Interfaces Defined by Consumer**
- Do NOT define large, monolithic interfaces on producer side
- Consumer defines small interface describing only required behavior

**4.3 Keep Interfaces Small**
```go
// GOOD: Single-method interface
type Reader interface {
    Read(p []byte) (n int, err error)
}

// BAD: Kitchen-sink interface
type DataManager interface {
    Read() ([]byte, error)
    Write([]byte) error
    Delete() error
    List() ([]string, error)
    // ... more methods
}
```

---

## Go 1.26 Features

### Generic Type Constraints

```go
// Use generics when type safety matters across multiple types
func Min[T cmp.Ordered](a, b T) T {
    if a < b {
        return a
    }
    return b
}

// Use constraints for custom types
type Number interface {
    ~int | ~int64 | ~float64
}
```

**When to use generics:**
- Collection operations (slices, maps)
- Type-safe data structures
- Avoiding interface{} with type assertions

**When NOT to use generics:**
- Single concrete type suffices
- Interface polymorphism is clearer
- Adding complexity without benefit

### Standard Library Packages

```go
import (
    "cmp"
    "maps"
    "slices"
)

// slices package
sorted := slices.Clone(items)
slices.Sort(sorted)
idx, found := slices.BinarySearch(sorted, target)
slices.Reverse(items)

// maps package
maps.Clone(m)
maps.DeleteFunc(m, func(k, v string) bool {
    return v == ""
})

// cmp package
result := cmp.Compare(a, b)  // -1, 0, or 1
cmp.Or(a, b, c)  // first non-zero value
```

### Structured Logging (log/slog)

```go
import "log/slog"

// Create logger with handler
logger := slog.New(slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
}))

// Structured logging
logger.Info("request processed",
    slog.String("method", r.Method),
    slog.String("path", r.URL.Path),
    slog.Duration("latency", elapsed),
    slog.Int("status", status),
)

// With context
logger.InfoContext(ctx, "operation completed",
    slog.String("operation", op),
)

// Group related attributes
logger.Info("user action",
    slog.Group("user",
        slog.String("id", user.ID),
        slog.String("role", user.Role),
    ),
)
```

### Context Patterns

```go
// context.AfterFunc for cleanup
ctx, cancel := context.WithCancel(parentCtx)
stop := context.AfterFunc(ctx, func() {
    cleanup()
})
// stop() to prevent callback if not needed

// Always propagate context
func ProcessItem(ctx context.Context, item Item) error {
    select {
    case <-ctx.Done():
        return ctx.Err()
    default:
    }
    // process...
}
```

### Range-over-func Iterators

```go
// Define an iterator
func (s *Set[T]) All() iter.Seq[T] {
    return func(yield func(T) bool) {
        for v := range s.items {
            if !yield(v) {
                return
            }
        }
    }
}

// Use with range
for item := range mySet.All() {
    process(item)
}
```

---

## Error Handling

### Wrapping Errors

```go
// ALWAYS add context when wrapping
if err != nil {
    return fmt.Errorf("failed to process user %s: %w", userID, err)
}

// Sentinel errors for expected conditions
var (
    ErrNotFound     = errors.New("resource not found")
    ErrUnauthorized = errors.New("unauthorized")
)

// Custom error types for rich context
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on %s: %s", e.Field, e.Message)
}
```

### Error Checking

```go
// errors.Is for sentinel errors
if errors.Is(err, ErrNotFound) {
    return http.StatusNotFound, nil
}

// errors.As for error types
var validErr *ValidationError
if errors.As(err, &validErr) {
    return http.StatusBadRequest, validErr
}

// Multiple wrapped errors (Go 1.20+)
err := errors.Join(err1, err2, err3)
```

### Anti-Patterns to Avoid

```go
// BAD: No context
if err != nil {
    return err
}

// BAD: Logging and returning (double handling)
if err != nil {
    log.Printf("error: %v", err)
    return err
}

// BAD: Ignoring errors
result, _ := riskyOperation()

// BAD: Panic in library code
func ParseConfig(s string) Config {
    // Don't do this in libraries!
    if s == "" {
        panic("empty config")
    }
}
```

---

## Concurrency Patterns

### Worker Pool with Bounded Concurrency

```go
func Process(ctx context.Context, items []Item, workers int) error {
    g, ctx := errgroup.WithContext(ctx)
    sem := make(chan struct{}, workers)

    for _, item := range items {
        item := item  // capture for Go < 1.22; still good practice
        g.Go(func() error {
            select {
            case sem <- struct{}{}:
                defer func() { <-sem }()
            case <-ctx.Done():
                return ctx.Err()
            }
            return processItem(ctx, item)
        })
    }
    return g.Wait()
}
```

### Channel Ownership

```go
// Producer owns the channel; producer closes
func Generate(ctx context.Context) <-chan int {
    ch := make(chan int)
    go func() {
        defer close(ch)  // Producer closes
        for i := 0; ; i++ {
            select {
            case ch <- i:
            case <-ctx.Done():
                return
            }
        }
    }()
    return ch
}
```

### sync.Once for Lazy Initialization

```go
type Client struct {
    once   sync.Once
    conn   *Connection
    connErr error
}

func (c *Client) getConn() (*Connection, error) {
    c.once.Do(func() {
        c.conn, c.connErr = dial()
    })
    return c.conn, c.connErr
}
```

### When NOT to Use Channels

```go
// Use mutex for simple shared state
type Counter struct {
    mu    sync.Mutex
    value int
}

func (c *Counter) Inc() {
    c.mu.Lock()
    c.value++
    c.mu.Unlock()
}

// Use atomic for single values
var counter atomic.Int64
counter.Add(1)
```

---

## Testing

### Table-Driven Tests

```go
func TestParseConfig(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    Config
        wantErr bool
    }{
        {
            name:  "valid config",
            input: `{"port": 8080}`,
            want:  Config{Port: 8080},
        },
        {
            name:    "invalid json",
            input:   `{invalid}`,
            wantErr: true,
        },
        {
            name:    "empty input",
            input:   "",
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseConfig(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("ParseConfig() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if !tt.wantErr && got != tt.want {
                t.Errorf("ParseConfig() = %v, want %v", got, tt.want)
            }
        })
    }
}
```

### Parallel Tests

```go
func TestIndependentOperations(t *testing.T) {
    t.Parallel()  // Mark test as parallel-safe

    tests := []struct{...}

    for _, tt := range tests {
        tt := tt  // capture
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel()  // Subtests can also be parallel
            // ...
        })
    }
}
```

### Test Cleanup

```go
func TestWithResource(t *testing.T) {
    db := setupTestDB(t)
    t.Cleanup(func() {
        db.Close()  // Runs after test completes
    })
    // Use db...
}

// Helper that registers cleanup
func setupTestDB(t *testing.T) *DB {
    t.Helper()
    db, err := NewDB(":memory:")
    if err != nil {
        t.Fatal(err)
    }
    t.Cleanup(func() { db.Close() })
    return db
}
```

---

## AST-Grep Anti-Pattern Detection

### Problematic Defer

```go
// WRONG: Arguments evaluated immediately
defer require.NoError(t, failpoint.Disable("path"))

// CORRECT: Wrap in anonymous function
defer func() {
    require.NoError(t, failpoint.Disable("path"))
}()
```

Detection rule:
```yaml
id: problematic-defer
language: go
rule:
  kind: defer_statement
  pattern: 'defer $A.$B(t, failpoint.$M($$))'
```

### JSON Tag Security Issue

```go
// WRONG: Field can still be unmarshaled with "-" key
type User struct {
    IsAdmin bool `json:"-,omitempty"`
}

// CORRECT: Properly omits field
type User struct {
    IsAdmin bool `json:"-"`
}
```

Detection rule:
```yaml
id: unmarshal-tag-is-dash
language: go
rule:
  pattern: '`$TAG`'
  inside:
    kind: field_declaration
constraints:
  TAG:
    regex: 'json:"-,.*"'
```

---

## Documentation Standards

```go
// Package user provides user management functionality.
// It handles user creation, authentication, and profile management.
package user

// User represents a registered user in the system.
// Zero value is not useful; use NewUser to create instances.
type User struct {
    ID        string    // Unique identifier
    Email     string    // Validated email address
    CreatedAt time.Time // UTC timestamp
}

// NewUser creates a new User with the given email.
// It returns an error if the email format is invalid.
//
// Example:
//
//	user, err := NewUser("alice@example.com")
//	if err != nil {
//	    return fmt.Errorf("creating user: %w", err)
//	}
func NewUser(email string) (*User, error) {
    if !isValidEmail(email) {
        return nil, &ValidationError{Field: "email", Message: "invalid format"}
    }
    return &User{
        ID:        generateID(),
        Email:     email,
        CreatedAt: time.Now().UTC(),
    }, nil
}
```

---

## Project Setup

```bash
# Initialize new Go 1.26 module
go mod init github.com/org/project

# Verify go.mod contains: go 1.26

# Install development tools
go install github.com/golangci/golangci-lint/cmd/golangci-lint@v1.62.0
go install golang.org/x/tools/cmd/goimports@latest

# Set up pre-commit hook
cp ~/.claude/skills/golang/scripts/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit

# Copy linter config
cp ~/.claude/skills/golang/resources/.golangci.yml .golangci.yml
cp ~/.claude/skills/golang/resources/.editorconfig .editorconfig
```

---

## Anti-Patterns Checklist

| Anti-Pattern | Detection | Fix |
|--------------|-----------|-----|
| Empty error handling | `return err` without context | Wrap with `fmt.Errorf` |
| Naked returns | `return` without values | Always use explicit values |
| Global mutable state | Package-level `var` | Pass as dependency |
| Overuse of `init()` | Multiple init functions | Explicit initialization |
| Ignoring context | No `ctx` parameter | Propagate context always |
| Interface pollution | Unused interfaces | Define at consumer site |
| Premature channels | Channel for simple mutex case | Use `sync.Mutex` |
| Panic in libraries | `panic()` in exported funcs | Return errors |

---

## Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `pre-commit` | Git hook for all checks | Copy to `.git/hooks/` |
| `lint.sh` | Run golangci-lint | `./scripts/lint.sh` |
| `fmt-check.sh` | Verify formatting | `./scripts/fmt-check.sh` |

Run setup:
```bash
~/.claude/skills/golang/scripts/lint.sh --help
```
