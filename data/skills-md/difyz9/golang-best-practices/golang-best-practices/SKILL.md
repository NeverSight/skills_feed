---
name: golang-best-practices
description: Comprehensive Go/Golang development best practices covering project structure, error handling, concurrency, testing, performance optimization, and code quality. Use this skill when writing Go code, refactoring Go projects, setting up new Go applications, implementing Go patterns, optimizing Go performance, or reviewing Go codebases. Triggers include Go file extensions (.go), mentions of goroutines/channels, Go modules, or requests for Go-specific guidance.
---

# Golang Best Practices

## Overview

This skill provides battle-tested best practices for Go development, covering project organization, error handling, concurrency patterns, testing strategies, performance optimization, and code quality standards. Use these guidelines when writing, reviewing, or refactoring Go code.

## Project Structure

### Standard Layout
Follow the standard Go project layout:
```
project/
├── cmd/              # Main applications
│   └── myapp/
│       └── main.go
├── internal/         # Private application code
│   ├── config/
│   ├── handler/
│   └── service/
├── pkg/             # Public library code
├── api/             # API definitions (OpenAPI/gRPC)
├── web/             # Web assets
├── scripts/         # Build/deploy scripts
├── test/            # Additional test files
├── docs/            # Documentation
├── go.mod
├── go.sum
├── Makefile
└── README.md
```

### Key Principles
- Use `internal/` for code that shouldn't be imported by external projects
- Use `pkg/` for reusable library code
- Keep `cmd/` minimal - just initialization and wiring
- One package = one responsibility

## Error Handling

### Always Check Errors
```go
// ❌ BAD
data, _ := os.ReadFile("file.txt")

// ✅ GOOD
data, err := os.ReadFile("file.txt")
if err != nil {
    return fmt.Errorf("read file: %w", err)
}
```

### Error Wrapping
Use `%w` to wrap errors for error chain inspection:
```go
if err != nil {
    return fmt.Errorf("failed to process user %s: %w", userID, err)
}
```

### Custom Errors
Create sentinel errors and custom error types:
```go
var ErrNotFound = errors.New("resource not found")

type ValidationError struct {
    Field string
    Err   error
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("validation failed on %s: %v", e.Field, e.Err)
}
```

### Error Checking
```go
// Check for specific errors
if errors.Is(err, ErrNotFound) {
    // handle not found
}

// Check error type
var valErr *ValidationError
if errors.As(err, &valErr) {
    // handle validation error
}
```

## Concurrency

### Goroutine Best Practices

**Always handle goroutine lifecycle:**
```go
// ✅ Use context for cancellation
func worker(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            return
        default:
            // do work
        }
    }
}

// ✅ Use WaitGroup for synchronization
var wg sync.WaitGroup
for i := 0; i < 10; i++ {
    wg.Add(1)
    go func(id int) {
        defer wg.Done()
        // work
    }(i)
}
wg.Wait()
```

### Channel Patterns

**Producer-Consumer:**
```go
func producer(ch chan<- int) {
    defer close(ch)
    for i := 0; i < 10; i++ {
        ch <- i
    }
}

func consumer(ch <-chan int) {
    for val := range ch {
        fmt.Println(val)
    }
}
```

**Fan-out/Fan-in:**
```go
func fanOut(in <-chan int, workers int) []<-chan int {
    channels := make([]<-chan int, workers)
    for i := 0; i < workers; i++ {
        channels[i] = worker(in)
    }
    return channels
}

func fanIn(channels ...<-chan int) <-chan int {
    out := make(chan int)
    var wg sync.WaitGroup
    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for val := range c {
                out <- val
            }
        }(ch)
    }
    go func() {
        wg.Wait()
        close(out)
    }()
    return out
}
```

### Avoid Race Conditions
- Use `sync.Mutex` for shared state
- Use channels for communication
- Run tests with `-race` flag
- Prefer immutable data structures

## Interface Design

### Small Interfaces
```go
// ✅ Small, focused interfaces
type Reader interface {
    Read(p []byte) (n int, err error)
}

type Writer interface {
    Write(p []byte) (n int, err error)
}

// Compose when needed
type ReadWriter interface {
    Reader
    Writer
}
```

### Accept Interfaces, Return Structs
```go
// ✅ Accept interface for flexibility
func Process(r io.Reader) error {
    // implementation
}

// ✅ Return concrete type
func NewClient() *Client {
    return &Client{}
}
```

## Code Quality

### Naming Conventions
- Use `camelCase` for private, `PascalCase` for public
- Keep names short but descriptive
- Avoid stuttering: `user.UserID` → `user.ID`
- Use consistent naming: `Get`, `Set`, `New`, `Init`

### Function Design
- Keep functions small and focused
- Limit parameters (max 3-4)
- Use functional options for configuration:
```go
type Option func(*Server)

func WithTimeout(d time.Duration) Option {
    return func(s *Server) {
        s.timeout = d
    }
}

func NewServer(opts ...Option) *Server {
    s := &Server{timeout: 30 * time.Second}
    for _, opt := range opts {
        opt(s)
    }
    return s
}
```

### Constants and Enums
```go
// Use iota for enums
type Status int

const (
    StatusPending Status = iota
    StatusActive
    StatusInactive
)

// Group related constants
const (
    maxRetries    = 3
    retryDelay    = time.Second
    timeout       = 30 * time.Second
)
```

## Testing

### Table-Driven Tests
```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 2, 3, 5},
        {"negative", -2, -3, -5},
        {"mixed", -2, 3, 1},
    }
    
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("got %d, want %d", result, tt.expected)
            }
        })
    }
}
```

### Test Helpers
```go
func TestMain(m *testing.M) {
    // Setup
    code := m.Run()
    // Teardown
    os.Exit(code)
}

func setupTest(t *testing.T) func() {
    // Setup code
    return func() {
        // Cleanup code
    }
}

func TestSomething(t *testing.T) {
    cleanup := setupTest(t)
    defer cleanup()
    // test code
}
```

### Mocking
Use interfaces for dependencies to enable testing:
```go
type UserStore interface {
    Get(id string) (*User, error)
}

type Service struct {
    store UserStore
}

// In tests, provide mock implementation
type mockStore struct{}
func (m *mockStore) Get(id string) (*User, error) {
    return &User{ID: id}, nil
}
```

## Performance

### Memory Allocation
- Pre-allocate slices when size is known: `make([]int, 0, capacity)`
- Reuse buffers with `sync.Pool`
- Use pointers for large structs
- Avoid string concatenation in loops (use `strings.Builder`)

### Profiling
```go
import _ "net/http/pprof"

// CPU profiling
go func() {
    log.Println(http.ListenAndServe("localhost:6060", nil))
}()
```

Run profiling:
```bash
go test -cpuprofile cpu.prof -memprofile mem.prof -bench .
go tool pprof cpu.prof
```

### Benchmarking
```go
func BenchmarkFunction(b *testing.B) {
    for i := 0; i < b.N; i++ {
        Function()
    }
}

// With setup
func BenchmarkWithSetup(b *testing.B) {
    data := setupData()
    b.ResetTimer()
    for i := 0; i < b.N; i++ {
        Process(data)
    }
}
```

## Dependencies

### Module Management
```bash
go mod init github.com/user/project
go mod tidy
go mod vendor  # Optional: vendor dependencies
```

### Version Pinning
```bash
go get github.com/pkg/errors@v0.9.1
```

### Private Modules
```bash
export GOPRIVATE=github.com/myorg/*
```

## Documentation

### Package Documentation
```go
// Package mypackage provides utilities for X.
//
// This package includes:
//   - Feature A
//   - Feature B
package mypackage
```

### Function Documentation
```go
// ProcessData validates and transforms the input data.
// It returns an error if validation fails.
//
// Example:
//   result, err := ProcessData(input)
//   if err != nil {
//       log.Fatal(err)
//   }
func ProcessData(input string) (string, error) {
    // implementation
}
```

## Layered Architecture

### Three-Layer Pattern
Separate concerns into distinct layers:
- **Handler Layer**: HTTP request/response handling, input validation
- **Service Layer**: Business logic, orchestration, domain rules
- **Repository Layer**: Data access, database operations

Each layer depends only on interfaces from the layer below, enabling:
- Independent testing through mocking
- Easy replacement of implementations
- Clear separation of concerns

### Dependency Injection with Fx
Use Uber Fx for managing dependencies:
```go
// Define interface in service layer
type UserRepository interface {
    GetByID(ctx context.Context, id uint) (*User, error)
}

// Implement in repository layer
type userRepository struct {
    db *gorm.DB
}

// Inject via constructor
func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}
```

See **references/fx-architecture.md** for complete implementation examples.

## Resources

See the bundled references for detailed guides:
- **references/fx-architecture.md**: Complete Fx dependency injection architecture with handlers, services, GORM repositories, and configuration management
- **references/patterns.md**: Common Go design patterns and idioms
- **references/stdlib.md**: Essential standard library packages guide
- **references/tools.md**: Development tools and linters configuration
