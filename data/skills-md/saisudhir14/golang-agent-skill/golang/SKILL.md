---
name: golang
description: Best practices for writing production Go code. Use when writing, reviewing, or refactoring Go code. Covers error handling, concurrency, naming conventions, testing patterns, performance optimization, generics, and common pitfalls. Based on Google Go Style Guide, Uber Go Style Guide, Effective Go, and Go Code Review Comments. Updated for Go 1.25.
---

# Go Best Practices

Battle-tested patterns from Google, Uber, and the Go team. These are practices proven in large-scale production systems, updated for modern Go (1.25).

## Core Principles

Readable code prioritizes these attributes in order:

1. **Clarity**: purpose and rationale are obvious to the reader
2. **Simplicity**: accomplishes the goal in the simplest way
3. **Concision**: high signal to noise ratio
4. **Maintainability**: easy to modify correctly
5. **Consistency**: matches surrounding codebase

---

## Error Handling

### Return Errors, Do Not Panic

Production code must avoid panics. Return errors and let callers decide how to handle them.

```go
// Wrong
func run(args []string) {
    if len(args) == 0 {
        panic("an argument is required")
    }
}

// Correct
func run(args []string) error {
    if len(args) == 0 {
        return errors.New("an argument is required")
    }
    return nil
}

func main() {
    if err := run(os.Args[1:]); err != nil {
        fmt.Fprintln(os.Stderr, err)
        os.Exit(1)
    }
}
```

### Error Wrapping

Use `%w` when callers need to inspect the underlying error with `errors.Is` or `errors.As`. Use `%v` when you want to hide implementation details or at system boundaries.

```go
// Preserve error chain for programmatic inspection
if err != nil {
    return fmt.Errorf("load config: %w", err)
}

// Hide internal details at API boundaries
if err != nil {
    return fmt.Errorf("database unavailable: %v", err)
}
```

Keep context succinct. Avoid phrases like "failed to" that pile up as errors propagate.

```go
// Wrong: produces "failed to x: failed to y: failed to create store: the error"
return fmt.Errorf("failed to create new store: %w", err)

// Correct: produces "x: y: new store: the error"
return fmt.Errorf("new store: %w", err)
```

### Joining Multiple Errors (Go 1.20+)

Use `errors.Join` when multiple operations can fail independently.

```go
func validateUser(u User) error {
    var errs []error
    if u.Name == "" {
        errs = append(errs, errors.New("name required"))
    }
    if u.Email == "" {
        errs = append(errs, errors.New("email required"))
    }
    return errors.Join(errs...)
}

// Checking joined errors
if err := validateUser(u); err != nil {
    if errors.Is(err, ErrNameRequired) {
        // handles even when joined with other errors
    }
}
```

### Error Types

Choose based on caller needs:

| Caller needs to match? | Message type | Approach |
|------------------------|--------------|----------|
| No | Static | `errors.New("something bad")` |
| No | Dynamic | `fmt.Errorf("file %q not found", file)` |
| Yes | Static | Exported `var ErrNotFound = errors.New("not found")` |
| Yes | Dynamic | Custom error type with `Error()` method |

### Sentinel Errors and errors.Is

Define sentinel errors for conditions callers need to check.

```go
var (
    ErrNotFound    = errors.New("not found")
    ErrInvalidUser = errors.New("invalid user")
)

// Checking wrapped errors
if errors.Is(err, ErrNotFound) {
    // handles ErrNotFound even when wrapped
}

// Custom error types use errors.As
var pathErr *os.PathError
if errors.As(err, &pathErr) {
    fmt.Println("failed path:", pathErr.Path)
}
```

### Error Naming

Exported error variables use `Err` prefix. Custom error types use `Error` suffix.

```go
var (
    ErrNotFound    = errors.New("not found")
    ErrInvalidUser = errors.New("invalid user")
)

type NotFoundError struct {
    Resource string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s not found", e.Resource)
}
```

### Handle Errors Once

Do not log an error and also return it. The caller will likely log it again.

```go
// Wrong: logs and returns, causing duplicate logs
if err != nil {
    log.Printf("could not get user %q: %v", id, err)
    return err
}

// Correct: wrap and return, let caller decide
if err != nil {
    return fmt.Errorf("get user %q: %w", id, err)
}

// Also correct: log and degrade gracefully without returning error
if err := emitMetrics(); err != nil {
    log.Printf("could not emit metrics: %v", err)
}
```

### Error Strings

Do not capitalize error strings or end with punctuation. They often appear mid-sentence in logs.

```go
// Wrong
fmt.Errorf("Something bad happened.")

// Correct
fmt.Errorf("something bad happened")
```

### Indent Error Flow

Keep the happy path at minimal indentation. Handle errors first.

```go
// Wrong
if err != nil {
    // error handling
} else {
    // normal code
}

// Correct
if err != nil {
    return err
}
// normal code continues
```

---

## Concurrency

### Channel Size

Channels should have size zero (unbuffered) or one. Any other size requires justification about what prevents filling under load.

```go
// Wrong: arbitrary buffer
c := make(chan int, 64)

// Correct
c := make(chan int)    // unbuffered: synchronous handoff
c := make(chan int, 1) // buffered: allows one pending send
```

### Goroutine Lifetimes

Document when and how goroutines exit. Goroutines blocked on channels will not be garbage collected even if the channel is unreachable.

```go
// Document exit conditions
func (w *Worker) Run(ctx context.Context) error {
    for {
        select {
        case <-ctx.Done():
            return ctx.Err()
        case job := <-w.jobs:
            w.process(job)
        }
    }
}
```

### Use errgroup for Concurrent Operations

Prefer `errgroup.Group` over manual `sync.WaitGroup` for error-returning goroutines.

```go
import "golang.org/x/sync/errgroup"

func processItems(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)
    
    for _, item := range items {
        g.Go(func() error {
            return process(ctx, item)
        })
    }
    
    return g.Wait() // returns first error, cancels others via ctx
}

// With concurrency limit
func processItemsLimited(ctx context.Context, items []Item) error {
    g, ctx := errgroup.WithContext(ctx)
    g.SetLimit(10) // max 10 concurrent goroutines
    
    for _, item := range items {
        g.Go(func() error {
            return process(ctx, item)
        })
    }
    
    return g.Wait()
}
```

### Prefer Synchronous Functions

Synchronous functions are easier to reason about and test. Let callers add concurrency when needed.

```go
// Wrong: forces concurrency on caller
func Fetch(url string) <-chan Result

// Correct: caller can wrap in goroutine if needed
func Fetch(url string) (Result, error)
```

### Zero Value Mutexes

The zero value of `sync.Mutex` is valid. Do not use pointers to mutexes or embed them in exported structs.

```go
// Wrong
mu := new(sync.Mutex)

// Wrong: exposes Lock/Unlock in API
type SMap struct {
    sync.Mutex
    data map[string]string
}

// Correct
type SMap struct {
    mu   sync.Mutex
    data map[string]string
}
```

### Atomic Operations (Go 1.19+)

Use the standard library's typed atomics. External packages are no longer necessary.

```go
import "sync/atomic"

type Counter struct {
    value atomic.Int64
}

func (c *Counter) Inc() {
    c.value.Add(1)
}

func (c *Counter) Value() int64 {
    return c.value.Load()
}

// Also available: atomic.Bool, atomic.Pointer[T], atomic.Uint32, etc.
```

### sync.Map Performance (Go 1.24+)

The `sync.Map` implementation was significantly improved in Go 1.24. Modifications of disjoint sets of keys are much less likely to contend on larger maps, and there is no longer any ramp-up time required to achieve low-contention loads.

---

## Naming

### MixedCaps Always

Go uses MixedCaps, never underscores. This applies even when it breaks other language conventions.

```go
// Wrong
MAX_LENGTH, max_length, HTTP_Server

// Correct
MaxLength, maxLength, HTTPServer
```

### Initialisms

Initialisms maintain consistent case: URL not Url, ID not Id, HTTP not Http.

```go
// Wrong
xmlHttpRequest, serverId, apiUrl

// Correct
xmlHTTPRequest, serverID, apiURL
```

### Short Variable Names

Variables should be short, especially with limited scope. The further from declaration a name is used, the more descriptive it needs to be.

```go
// Good for local scope
for i, v := range items { }
r := bufio.NewReader(f)

// Global or struct fields need more context
var DefaultTimeout = 30 * time.Second
```

### Receiver Names

Use one or two letter abbreviations of the type. Be consistent across methods. Do not use generic names like `this`, `self`, or `me`.

```go
// Wrong
func (this *Client) Get() {}
func (c *Client) Get() {}
func (cl *Client) Post() {} // inconsistent

// Correct
func (c *Client) Get() {}
func (c *Client) Post() {}
```

### Pointer vs Value Receivers

| Use pointer receiver when | Use value receiver when |
|---------------------------|-------------------------|
| Method modifies the receiver | Struct is small and immutable |
| Struct is large (avoid copying) | Method doesn't modify state |
| Consistency with other methods | Receiver is a map, func, or chan |
| Struct contains sync.Mutex | Basic types (int, string, etc.) |

```go
// Pointer: modifies state
func (s *Server) Shutdown() error {
    s.running = false
    return s.listener.Close()
}

// Value: small, read-only
func (p Point) Distance(q Point) float64 {
    return math.Hypot(p.X-q.X, p.Y-q.Y)
}
```

### Package Names

Package names are lowercase, single words. Avoid util, common, misc, api, types. The package name becomes part of the identifier at call sites.

```go
// Wrong
package chubby
type ChubbyFile struct{}  // chubby.ChubbyFile is redundant

// Correct
package chubby
type File struct{}  // chubby.File reads well
```

### Avoid Repetition in Names

Do not repeat package or receiver names in function names.

```go
// Wrong
package http
func HTTPServe() {}  // http.HTTPServe is redundant

func (c *Config) WriteConfigTo(w io.Writer) {}  // Config repeated

// Correct
package http
func Serve() {}  // http.Serve

func (c *Config) WriteTo(w io.Writer) {}
```

---

## Imports

### Grouping

Organize imports in three groups separated by blank lines: standard library, external packages, internal packages.

```go
import (
    "context"
    "fmt"
    "os"

    "github.com/google/uuid"
    "golang.org/x/sync/errgroup"

    "yourcompany/internal/config"
    "yourcompany/internal/metrics"
)
```

### Avoid Renaming

Rename imports only to avoid collisions. Prefer renaming the most local import.

### Avoid Import Dot

The dot import (`import . "pkg"`) makes code harder to read. Use only in test files with circular dependencies.

### Blank Imports

Import for side effects (`import _ "pkg"`) only in main packages or tests.

---

## Module Management

### Tool Directives (Go 1.24+)

Go modules can now track executable dependencies using tool directives in go.mod. This removes the need for the previous workaround of adding tools as blank imports to a file conventionally named "tools.go".

```go
// go.mod
module example.com/myproject

go 1.24

tool (
    golang.org/x/tools/cmd/stringer
    github.com/golangci/golangci-lint/cmd/golangci-lint
)
```

```bash
# Add a tool dependency
go get -tool golang.org/x/tools/cmd/stringer

# Run a tool
go tool stringer -type=Status

# Update all tools
go get tool

# Install all tools to GOBIN
go install tool
```

---

## Structs

### Use Field Names in Initialization

Always use field names. Positional arguments break when fields are added.

```go
// Wrong: breaks if fields change
k := User{"John", "john@example.com", true}

// Correct
k := User{
    Name:   "John",
    Email:  "john@example.com",
    Active: true,
}
```

### Omit Zero Value Fields

Do not initialize fields to their zero values.

```go
// Wrong
user := User{
    Name:   "John",
    Active: false,  // false is zero value
    Count:  0,      // 0 is zero value
}

// Correct
user := User{
    Name: "John",
}
```

### Embedding

Do not embed types in public structs. Embedding exposes methods and fields to the public API unintentionally.

```go
// Wrong: Lock and Unlock become part of SMap's API
type SMap struct {
    sync.Mutex
    data map[string]string
}

// Correct
type SMap struct {
    mu   sync.Mutex
    data map[string]string
}
```

### Use var for Zero Value Structs

```go
// Correct
var user User

// Also acceptable
user := User{}
```

---

## Slices and Maps

### Nil Slice Declaration

Prefer nil slices over empty slices. They are functionally equivalent but nil is the preferred style.

```go
// Preferred
var t []string

// Use only when JSON must encode as [] instead of null
t := []string{}
```

### Copy at Boundaries

Slices and maps hold references. Copy them when storing or returning to prevent mutation.

```go
// Wrong: caller can modify internal state
func (d *Driver) SetTrips(trips []Trip) {
    d.trips = trips
}

// Correct
func (d *Driver) SetTrips(trips []Trip) {
    d.trips = make([]Trip, len(trips))
    copy(d.trips, trips)
}

// For maps
func (d *Driver) SetMetadata(m map[string]string) {
    d.metadata = maps.Clone(m)
}
```

### Specify Capacity

Preallocate when size is known. This reduces allocations.

```go
// Wrong
var result []Item
for _, v := range input {
    result = append(result, transform(v))
}

// Correct
result := make([]Item, 0, len(input))
for _, v := range input {
    result = append(result, transform(v))
}
```

### Use slices and maps Packages

Prefer standard library functions for common operations.

```go
import (
    "cmp"
    "maps"
    "slices"
)

// Sorting
slices.Sort(numbers)
slices.SortFunc(users, func(a, b User) int {
    return cmp.Compare(a.Name, b.Name)
})

// Searching
idx, found := slices.BinarySearch(sorted, target)

// Cloning
copy := slices.Clone(original)
mapCopy := maps.Clone(original)

// Comparison
if slices.Equal(a, b) { }
if maps.Equal(m1, m2) { }
```

---

## Generics (Go 1.18+)

### When to Use Generics

Use generics when you find yourself writing the same code for different types.

```go
// Generic helper functions
func Filter[T any](slice []T, predicate func(T) bool) []T {
    result := make([]T, 0, len(slice))
    for _, v := range slice {
        if predicate(v) {
            result = append(result, v)
        }
    }
    return result
}

func Map[T, U any](slice []T, transform func(T) U) []U {
    result := make([]U, len(slice))
    for i, v := range slice {
        result[i] = transform(v)
    }
    return result
}

// Usage
adults := Filter(users, func(u User) bool { return u.Age >= 18 })
names := Map(users, func(u User) string { return u.Name })
```

### Type Constraints

Use constraints for type safety.

```go
import "cmp"

// cmp.Ordered covers all comparable types
func Max[T cmp.Ordered](a, b T) T {
    if a > b {
        return a
    }
    return b
}

// Custom constraints
type Number interface {
    ~int | ~int64 | ~float64
}

func Sum[T Number](values []T) T {
    var total T
    for _, v := range values {
        total += v
    }
    return total
}
```

### Generic Type Aliases (Go 1.24+)

Type aliases can now be parameterized like defined types.

```go
// Generic type alias
type Set[T comparable] = map[T]struct{}

// Usage
var s Set[string]
s = make(Set[string])
s["hello"] = struct{}{}

// With constraints
type OrderedSlice[T cmp.Ordered] = []T
```

### Avoid Over-Generalization

Do not use generics when a concrete type or interface suffices.

```go
// Wrong: unnecessary generic
func PrintAll[T fmt.Stringer](items []T) {
    for _, item := range items {
        fmt.Println(item.String())
    }
}

// Correct: interface is sufficient
func PrintAll(items []fmt.Stringer) {
    for _, item := range items {
        fmt.Println(item.String())
    }
}
```

---

## Iterators (Go 1.23+)

### Range Over Functions

Go 1.23 introduced range-over-func, allowing custom iterators.

```go
// Iterator function signature
type Seq[V any] func(yield func(V) bool)
type Seq2[K, V any] func(yield func(K, V) bool)

// Custom iterator
func Backward[T any](s []T) func(yield func(int, T) bool) {
    return func(yield func(int, T) bool) {
        for i := len(s) - 1; i >= 0; i-- {
            if !yield(i, s[i]) {
                return
            }
        }
    }
}

// Usage
for i, v := range Backward(items) {
    fmt.Println(i, v)
}
```

### String and Bytes Iterators (Go 1.24+)

New iterator functions for efficient string and byte processing.

```go
import "strings"

// Iterate over lines (includes newline characters)
text := "line1\nline2\nline3"
for line := range strings.Lines(text) {
    fmt.Print(line)
}

// Split by delimiter (iterator, no slice allocation)
csvData := "apple,banana,cherry"
for value := range strings.SplitSeq(csvData, ",") {
    fmt.Println(value)
}

// Split after delimiter
for part := range strings.SplitAfterSeq(csvData, ",") {
    fmt.Println(part) // "apple," "banana," "cherry"
}

// Equivalent functions exist in bytes package
```

---

## Structured Logging (Go 1.21+)

### Use slog for New Code

The standard library now includes structured logging.

```go
import "log/slog"

// Basic usage
slog.Info("user created", "id", userID, "email", email)
slog.Error("request failed", "err", err, "method", r.Method)

// With context
logger := slog.With("service", "auth", "version", "1.0")
logger.Info("starting")

// JSON output for production
handler := slog.NewJSONHandler(os.Stdout, &slog.HandlerOptions{
    Level: slog.LevelInfo,
})
slog.SetDefault(slog.New(handler))
```

### slog.DiscardHandler (Go 1.24+)

Use the built-in discard handler for suppressing logs in tests.

```go
// Before Go 1.24
log := slog.New(slog.NewJSONHandler(io.Discard, nil))

// Go 1.24+
log := slog.New(slog.DiscardHandler)
```

### Structured Logging Best Practices

```go
// Use consistent key names
slog.Info("request completed",
    "method", r.Method,
    "path", r.URL.Path,
    "status", statusCode,
    "duration_ms", duration.Milliseconds(),
)

// Group related fields
slog.Info("user action",
    slog.Group("user",
        "id", user.ID,
        "role", user.Role,
    ),
    slog.Group("request",
        "method", r.Method,
        "path", r.URL.Path,
    ),
)
```

---

## Performance

### Prefer strconv Over fmt

strconv is faster for primitive conversions.

```go
// Slower
s := fmt.Sprintf("%d", n)

// Faster
s := strconv.Itoa(n)
```

### Avoid Repeated String to Byte Conversions

```go
// Wrong: converts on every iteration
for i := 0; i < n; i++ {
    w.Write([]byte("hello"))
}

// Correct
data := []byte("hello")
for i := 0; i < n; i++ {
    w.Write(data)
}
```

### Specify Map Capacity

```go
// Wrong
m := make(map[string]int)

// Correct when size is known
m := make(map[string]int, len(items))
```

### Use strings.Builder for Concatenation

```go
// Wrong: creates many allocations
var s string
for _, part := range parts {
    s += part
}

// Correct
var b strings.Builder
b.Grow(totalLen) // optional: preallocate
for _, part := range parts {
    b.WriteString(part)
}
s := b.String()
```

---

## Testing

### Table Driven Tests with Parallel Execution

Use table driven tests to avoid code duplication. Run subtests in parallel when safe.

```go
func TestSplit(t *testing.T) {
    tests := []struct {
        name  string
        input string
        sep   string
        want  []string
    }{
        {
            name:  "simple",
            input: "a/b/c",
            sep:   "/",
            want:  []string{"a", "b", "c"},
        },
        {
            name:  "empty",
            input: "",
            sep:   "/",
            want:  []string{""},
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // run subtests concurrently
            
            got := strings.Split(tt.input, tt.sep)
            if diff := cmp.Diff(tt.want, got); diff != "" {
                t.Errorf("Split() mismatch (-want +got):\n%s", diff)
            }
        })
    }
}
```

### T.Context and T.Chdir (Go 1.24+)

New helper methods for test context and working directory.

```go
func TestWithContext(t *testing.T) {
    // T.Context returns a context canceled after test completes
    // but before cleanup functions run
    ctx := t.Context()
    
    result, err := doWork(ctx)
    if err != nil {
        t.Fatal(err)
    }
    // ...
}

func TestWithChdir(t *testing.T) {
    // T.Chdir changes working directory for duration of test
    // and automatically restores it after
    t.Chdir("testdata")
    
    // Now in testdata directory
    data, err := os.ReadFile("input.txt")
    // ...
}
```

### Benchmark with b.Loop (Go 1.24+)

Use `b.Loop()` for cleaner, more accurate benchmarks.

```go
// Old way - error prone
func BenchmarkOld(b *testing.B) {
    input := setupInput() // counted in benchmark time!
    b.ResetTimer()        // easy to forget
    for i := 0; i < b.N; i++ {
        process(input)    // compiler might optimize away
    }
}

// Go 1.24+ - preferred
func BenchmarkNew(b *testing.B) {
    input := setupInput() // setup runs once, excluded from timing
    for b.Loop() {
        process(input)    // compiler cannot optimize away
    }
}
```

Benefits of `b.Loop()`:
- Setup code runs exactly once per `-count`, automatically excluded from timing
- No need to call `b.ResetTimer()`
- Function call parameters and results are kept alive, preventing compiler optimization

### Testing Concurrent Code with synctest (Go 1.25+)

The `testing/synctest` package provides deterministic testing for concurrent code using synthetic time.

```go
import "testing/synctest"

func TestTimeout(t *testing.T) {
    synctest.Test(t, func(t *testing.T) {
        ctx, cancel := context.WithTimeout(t.Context(), 5*time.Second)
        defer cancel()
        
        // Inside the "bubble", time is synthetic
        // This sleep completes instantly in real time
        time.Sleep(4 * time.Second)
        
        // Context should not be expired yet
        if err := ctx.Err(); err != nil {
            t.Fatalf("unexpected timeout: %v", err)
        }
        
        // Advance past the timeout
        time.Sleep(2 * time.Second)
        
        // Now it should be expired
        if ctx.Err() != context.DeadlineExceeded {
            t.Fatal("expected deadline exceeded")
        }
    })
}
```

Key concepts:
- `synctest.Test` creates an isolated "bubble" with synthetic time
- Time only advances when all goroutines in the bubble are blocked
- Initial time is midnight UTC 2000-01-01
- `synctest.Wait()` waits for all goroutines to be durably blocked

```go
func TestConcurrentCounter(t *testing.T) {
    synctest.Test(t, func(t *testing.T) {
        var counter atomic.Int64
        var wg sync.WaitGroup
        
        // Start concurrent workers
        for i := 0; i < 10; i++ {
            wg.Add(1)
            go func() {
                defer wg.Done()
                counter.Add(1)
            }()
        }
        
        // Wait for all goroutines to complete
        wg.Wait()
        
        // Counter is now deterministically 10
        if got := counter.Load(); got != 10 {
            t.Errorf("got %d, want 10", got)
        }
    })
}

// Example with time-based operations
func TestPeriodicTask(t *testing.T) {
    synctest.Test(t, func(t *testing.T) {
        var count atomic.Int64
        ctx, cancel := context.WithCancel(t.Context())
        
        // Start a periodic task
        go func() {
            ticker := time.NewTicker(100 * time.Millisecond)
            defer ticker.Stop()
            for {
                select {
                case <-ctx.Done():
                    return
                case <-ticker.C:
                    count.Add(1)
                }
            }
        }()
        
        // Advance synthetic time by 350ms
        time.Sleep(350 * time.Millisecond)
        synctest.Wait() // wait for goroutine to process
        
        cancel()
        synctest.Wait() // wait for goroutine to exit
        
        // Should have ticked 3 times (at 100ms, 200ms, 300ms)
        if got := count.Load(); got != 3 {
            t.Errorf("got %d ticks, want 3", got)
        }
    })
}
```

**Important restrictions in synctest bubbles:**
- Do not call `t.Run()`, `t.Parallel()`, or `t.Deadline()`
- Channels created outside the bubble behave differently
- External I/O operations are not durably blocking

### Use go-cmp for Comparisons

Prefer `github.com/google/go-cmp/cmp` over `reflect.DeepEqual`.

```go
import "github.com/google/go-cmp/cmp"

// Clear diff output on failure
if diff := cmp.Diff(want, got); diff != "" {
    t.Errorf("mismatch (-want +got):\n%s", diff)
}

// With options for custom comparison
if diff := cmp.Diff(want, got, cmpopts.IgnoreUnexported(User{})); diff != "" {
    t.Errorf("mismatch (-want +got):\n%s", diff)
}
```

### Useful Test Failures

Include: what was wrong, inputs, actual result, expected result.

```go
// Wrong
if got != want {
    t.Error("wrong result")
}

// Correct
if got != want {
    t.Errorf("Foo(%q) = %d; want %d", input, got, want)
}
```

### Use t.Fatal for Setup Failures

```go
f, err := os.CreateTemp("", "test")
if err != nil {
    t.Fatal("failed to set up test")
}
```

### Interfaces Belong to Consumers

Define interfaces in the package that uses them, not the package that implements them.

```go
// Wrong: defining interface in producer
package producer
type Thinger interface { Thing() bool }
func NewThinger() Thinger { return &thinger{} }

// Correct: producer returns concrete type
package producer
type Thinger struct{}
func (t *Thinger) Thing() bool { return true }
func NewThinger() *Thinger { return &Thinger{} }

// Consumer defines interface it needs
package consumer
type Thinger interface { Thing() bool }
func Process(t Thinger) { }
```

---

## Resource Management

### runtime.AddCleanup (Go 1.24+)

Prefer `runtime.AddCleanup` over `runtime.SetFinalizer` for cleanup operations.

```go
import "runtime"

type Resource struct {
    handle uintptr
}

func NewResource() *Resource {
    r := &Resource{handle: allocHandle()}
    
    // AddCleanup is more flexible than SetFinalizer:
    // - Multiple cleanups can be attached to one object
    // - Works with interior pointers
    // - Doesn't cause leaks with cycles
    // - Doesn't delay freeing the object
    runtime.AddCleanup(r, func(handle uintptr) {
        freeHandle(handle)
    }, r.handle)
    
    return r
}
```

Key advantages over `SetFinalizer`:
- Multiple cleanups per object
- Works with interior pointers
- No cycle-related leaks
- Object freed promptly (single GC cycle)

### Weak Pointers (Go 1.24+)

The `weak` package provides weak references that don't prevent garbage collection.

```go
import "weak"

// Create a weak pointer from a strong pointer
type ExpensiveResource struct {
    data []byte
}

func NewCache() *Cache {
    return &Cache{
        items: make(map[string]weak.Pointer[ExpensiveResource]),
    }
}

type Cache struct {
    mu    sync.Mutex
    items map[string]weak.Pointer[ExpensiveResource]
}

func (c *Cache) Get(key string) *ExpensiveResource {
    c.mu.Lock()
    defer c.mu.Unlock()
    
    if wp, ok := c.items[key]; ok {
        // Value returns the original pointer, or nil if collected
        if r := wp.Value(); r != nil {
            return r
        }
        // Resource was garbage collected, remove stale entry
        delete(c.items, key)
    }
    return nil
}

func (c *Cache) Set(key string, r *ExpensiveResource) {
    c.mu.Lock()
    defer c.mu.Unlock()
    // Make creates a weak pointer from a strong pointer
    c.items[key] = weak.Make(r)
}
```

Use cases for weak pointers:
- Caches that shouldn't prevent garbage collection
- Canonicalization maps (interning)
- Observer patterns where observers may be collected

### Secure Directory Access with os.Root (Go 1.24+)

The `os.Root` type provides safe, scoped file system access that prevents path traversal attacks.

```go
import "os"

func ServeUserFiles(userDir string) http.HandlerFunc {
    return func(w http.ResponseWriter, r *http.Request) {
        // OpenRoot opens a directory as a root for safe access
        root, err := os.OpenRoot(userDir)
        if err != nil {
            http.Error(w, "directory not found", http.StatusNotFound)
            return
        }
        defer root.Close()
        
        // Open is safe: paths are resolved relative to root
        // Attempts to escape (like "../etc/passwd") are rejected
        filename := r.URL.Query().Get("file")
        f, err := root.Open(filename)
        if err != nil {
            http.Error(w, "file not found", http.StatusNotFound)
            return
        }
        defer f.Close()
        
        io.Copy(w, f)
    }
}

// Available methods on os.Root:
// - Open(name) - open file for reading
// - Create(name) - create or truncate file
// - OpenFile(name, flag, perm) - open with flags
// - Mkdir(name, perm) - create directory
// - Remove(name) - remove file or empty directory
// - Stat(name), Lstat(name) - file info
// - ReadDir(name) - list directory contents
```

Key benefits:
- Prevents path traversal vulnerabilities ("../" attacks)
- Symlinks cannot escape the root directory
- Race-condition safe (uses openat2 on Linux)
- Drop-in replacement for typical file operations

---

## Patterns

### Functional Options

Use functional options for configurable constructors with many optional parameters.

```go
type Server struct {
    addr    string
    timeout time.Duration
    logger  *slog.Logger
}

type Option func(*Server)

func WithTimeout(d time.Duration) Option {
    return func(s *Server) { s.timeout = d }
}

func WithLogger(l *slog.Logger) Option {
    return func(s *Server) { s.logger = l }
}

func NewServer(addr string, opts ...Option) *Server {
    s := &Server{
        addr:    addr,
        timeout: 30 * time.Second,
        logger:  slog.Default(),
    }
    for _, opt := range opts {
        opt(s)
    }
    return s
}

// Usage
srv := NewServer("localhost:8080",
    WithTimeout(60*time.Second),
    WithLogger(logger),
)
```

### Verify Interface Compliance

Use compile time checks to verify interface implementations.

```go
type Handler struct{}

var _ http.Handler = (*Handler)(nil)

func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {}
```

### Defer for Cleanup

Use defer to clean up resources. The small overhead is worth the readability and safety.

```go
p.Lock()
defer p.Unlock()

if p.count < 10 {
    return p.count
}
p.count++
return p.count
```

### Graceful Shutdown Pattern

Production servers need graceful shutdown to drain connections.

```go
func main() {
    srv := &http.Server{Addr: ":8080", Handler: handler}

    // Start server in goroutine
    go func() {
        if err := srv.ListenAndServe(); err != http.ErrServerClosed {
            slog.Error("server error", "err", err)
        }
    }()

    // Wait for interrupt signal
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit

    // Graceful shutdown with timeout
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    
    if err := srv.Shutdown(ctx); err != nil {
        slog.Error("shutdown error", "err", err)
    }
    slog.Info("server stopped")
}
```

### Start Enums at One

Zero values should represent invalid or unset state.

```go
type Operation int

const (
    OperationUnknown Operation = iota // 0 = invalid
    OperationAdd                      // 1
    OperationSubtract                 // 2
)
```

### Use time Package for Time

Do not use integers for time. Use `time.Time` for instants and `time.Duration` for periods.

```go
// Wrong
func poll(delay int) {
    time.Sleep(time.Duration(delay) * time.Millisecond)
}
poll(10) // is this seconds or milliseconds?

// Correct
func poll(delay time.Duration) {
    time.Sleep(delay)
}
poll(10 * time.Second)
```

### Handle Type Assertions

Always use the two value form to avoid panics.

```go
// Wrong: panics on wrong type
t := i.(string)

// Correct
t, ok := i.(string)
if !ok {
    // handle error
}
```

### Context as First Parameter

Context should be the first parameter, named ctx. Do not store context in structs.

```go
func (s *Service) Process(ctx context.Context, req *Request) (*Response, error) {
    // ...
}
```

### Avoid Mutable Globals

Use dependency injection instead of modifying global state.

```go
// Wrong
var db *sql.DB

func init() {
    db, _ = sql.Open("postgres", os.Getenv("DSN"))
}

// Correct
type Server struct {
    db *sql.DB
}

func NewServer(db *sql.DB) *Server {
    return &Server{db: db}
}
```

### Avoid init()

Prefer explicit initialization in main. init() makes code harder to reason about and test.

### Embed Static Files (Go 1.16+)

Use `//go:embed` for static assets.

```go
import "embed"

//go:embed templates/*
var templates embed.FS

//go:embed config.json
var configData []byte
```

### Use Field Tags in Marshaled Structs

Explicit field names protect against accidental contract changes from refactoring.

```go
type User struct {
    Name  string `json:"name"`
    Email string `json:"email"`
}
```

---

## Container and Runtime Considerations

### Container-Aware GOMAXPROCS (Go 1.25+)

Go 1.25 automatically adjusts GOMAXPROCS based on container CPU limits.

```go
// On Linux with cgroups, GOMAXPROCS now considers:
// - CPU bandwidth limits (CPU limit in Kubernetes)
// - Changes dynamically if limits change

// The runtime periodically updates GOMAXPROCS if:
// - Number of logical CPUs changes
// - cgroup CPU bandwidth limit changes

// Automatic behavior is disabled if you set GOMAXPROCS explicitly:
// - Via GOMAXPROCS environment variable
// - Via runtime.GOMAXPROCS() call
```

This means Go programs in containers should now perform better out-of-the-box without manual GOMAXPROCS tuning.

---

## Common Gotchas

### Loop Variable Capture (Fixed in Go 1.22+)

Prior to Go 1.22, loop variables were reused. This is no longer an issue.

```go
// Pre-Go 1.22: All goroutines see last value
for _, v := range values {
    go func() {
        process(v) // Wrong: captures loop variable
    }()
}

// Fix for pre-Go 1.22
for _, v := range values {
    v := v // shadow the loop variable
    go func() {
        process(v)
    }()
}

// Go 1.22+: Loop variables are per-iteration (no fix needed)
for _, v := range values {
    go func() {
        process(v) // Safe: v is unique per iteration
    }()
}
```

### Defer Argument Evaluation

Defer evaluates arguments immediately, not when deferred function runs.

```go
// Wrong: always prints 0
for i := 0; i < 5; i++ {
    defer fmt.Println(i) // i evaluated when defer is called
}
// Prints: 4 3 2 1 0

// Gotcha with file handles
for _, f := range files {
    defer f.Close() // All defer the same f!
}

// Fix: capture in closure
for _, f := range files {
    f := f
    defer f.Close()
}
```

### Nil Interface vs Nil Pointer

An interface containing a nil pointer is not nil.

```go
type MyError struct{}
func (e *MyError) Error() string { return "error" }

func returnsError() error {
    var e *MyError = nil
    return e // Returns non-nil interface containing nil pointer!
}

if err := returnsError(); err != nil {
    fmt.Println("error is not nil!") // This prints
}

// Fix: return nil explicitly
func returnsError() error {
    var e *MyError = nil
    if e == nil {
        return nil
    }
    return e
}
```

### Use Result Before Checking Error (Go 1.25 Fix)

Go 1.25 fixed a compiler bug where using a result before checking for error sometimes didn't panic. Your code should always check errors first.

```go
// Wrong: uses f before checking err
f, err := os.Open("file.txt")
fmt.Println(f.Name()) // May panic if f is nil
if err != nil {
    return err
}

// Correct: always check error first
f, err := os.Open("file.txt")
if err != nil {
    return err
}
fmt.Println(f.Name()) // Safe: err was nil, so f is valid
```

In Go 1.21-1.24, a compiler bug sometimes suppressed the panic. Go 1.25 correctly panics, so ensure your code follows the proper pattern.

### Map Iteration Order

Map iteration order is randomized. Do not depend on it.

```go
// Wrong: results vary between runs
for k, v := range m {
    results = append(results, v)
}

// Correct: sort keys first if order matters
keys := slices.Sorted(maps.Keys(m))
for _, k := range keys {
    results = append(results, m[k])
}
```

### Slice Append Gotcha

Append may or may not allocate new backing array.

```go
a := []int{1, 2, 3}
b := a[:2]
b = append(b, 4)
// a is now [1, 2, 4]! They share backing array

// Fix: use full slice expression to limit capacity
b := a[:2:2] // len=2, cap=2
b = append(b, 4) // forces new allocation
// a is still [1, 2, 3]
```

---

## Experimental Features

### encoding/json/v2 (Go 1.25, Experimental)

A new JSON engine is available with improved performance and streaming support.

```go
// Enable with: GOEXPERIMENT=jsonv2

import (
    "encoding/json/jsontext"
    "encoding/json/v2"
)

// The v2 API offers:
// - Better performance
// - Streaming-friendly jsontext package  
// - Custom marshalers/unmarshalers per call
// - Existing encoding/json can use v2 engine internally
```

This is experimental and subject to change.

---

## Documentation

### Comment Sentences

Comments documenting declarations should be full sentences starting with the name being described.

```go
// Request represents a request to run a command.
type Request struct{}

// Encode writes the JSON encoding of req to w.
func Encode(w io.Writer, req *Request) error {}
```

### Package Comments

Package comments appear before the package declaration with no blank line.

```go
// Package math provides basic constants and mathematical functions.
package math
```

---

## References

1. [Google Go Style Guide](https://google.github.io/styleguide/go/)
2. [Uber Go Style Guide](https://github.com/uber-go/guide)
3. [Effective Go](https://go.dev/doc/effective_go)
4. [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments)
5. [Go 1.23 Release Notes](https://go.dev/doc/go1.23)
6. [Go 1.24 Release Notes](https://go.dev/doc/go1.24)
7. [Go 1.25 Release Notes](https://go.dev/doc/go1.25)
