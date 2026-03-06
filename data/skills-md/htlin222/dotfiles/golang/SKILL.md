---
name: golang
description: Write idiomatic Go with goroutines, channels, and interfaces. Use for Go development, concurrency, or performance.
---

# Go Development

Write clean, concurrent, idiomatic Go code.

## When to Use

- Writing Go code
- Concurrency patterns
- Performance optimization
- Interface design
- Go module management

## Go Patterns

### Concurrency

```go
// Worker pool pattern
func workerPool(jobs <-chan Job, results chan<- Result, workers int) {
    var wg sync.WaitGroup
    for i := 0; i < workers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                results <- process(job)
            }
        }()
    }
    wg.Wait()
    close(results)
}

// Context for cancellation
func fetchWithTimeout(ctx context.Context, url string) ([]byte, error) {
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    return io.ReadAll(resp.Body)
}
```

### Error Handling

```go
// Custom errors with context
type ValidationError struct {
    Field   string
    Message string
}

func (e *ValidationError) Error() string {
    return fmt.Sprintf("%s: %s", e.Field, e.Message)
}

// Error wrapping
if err != nil {
    return fmt.Errorf("failed to process user %d: %w", userID, err)
}
```

### Interfaces

```go
// Small, focused interfaces
type Reader interface {
    Read(p []byte) error
}

type Writer interface {
    Write(p []byte) error
}

// Composition
type ReadWriter interface {
    Reader
    Writer
}
```

## Project Structure

```
project/
├── cmd/
│   └── app/
│       └── main.go
├── internal/
│   ├── handler/
│   └── service/
├── pkg/
│   └── utils/
├── go.mod
└── go.sum
```

## Testing

```go
func TestProcess(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    string
        wantErr bool
    }{
        {"valid input", "hello", "HELLO", false},
        {"empty input", "", "", true},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := Process(tt.input)
            if (err != nil) != tt.wantErr {
                t.Errorf("error = %v, wantErr %v", err, tt.wantErr)
            }
            if got != tt.want {
                t.Errorf("got %v, want %v", got, tt.want)
            }
        })
    }
}
```

## Best Practices

- Prefer composition over inheritance
- Keep interfaces small (1-3 methods)
- Handle errors explicitly
- Use context for cancellation
- Avoid global state

## Examples

**Input:** "Add concurrency to this"
**Action:** Identify parallel work, add goroutines with proper sync, handle errors

**Input:** "Review this Go code"
**Action:** Check error handling, interface design, concurrency safety
