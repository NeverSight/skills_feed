---
name: go-table-driven-tests
description: Write Go table-driven tests following established patterns. Use when writing tests, creating test functions, adding test cases, or when the user mentions "test", "table-driven", "Go tests", or testing in Go codebases.
---

# Go Table-Driven Tests

Use this skill when writing or modifying Go table-driven tests. It ensures tests follow established patterns.

## Core Principles

- **One test function, many cases** - Define test cases in a slice and iterate with `t.Run()`
- **Explicit naming** - Each case has a `name` field that becomes the subtest name
- **Structured inputs** - Use struct fields for inputs, expected outputs, and configuration
- **Helper functions** - Use `t.Helper()` in test helpers for proper line reporting
- **Environment guards** - Skip integration tests when credentials are unavailable

## Table Structure Pattern

```go
func TestFunctionName(t *testing.T) {
    tests := []struct {
        name        string              // required: subtest name
        input       Type                // function input
        want        Type                // expected output
        wantErr     error               // expected error (nil for success)
        errCheck    func(error) bool    // optional: custom error validation
        setupEnv    func() func()       // optional: env setup, returns cleanup
    }{
        {
            name: "descriptive case name",
            input: "test input",
            want: "expected output",
        },
        // ... more cases
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // test implementation using tt fields
        })
    }
}
```

## Field Guidelines

| Field          | Required | Purpose                                              |
| -------------- | -------- | ---------------------------------------------------- |
| `name`         | Yes      | Subtest name - be descriptive and specific           |
| `input`/`args` | Varies   | Input values for the function under test             |
| `want`/`want*` | Varies   | Expected output values (e.g., `wantErr`, `wantResult`) |
| `errCheck`     | No       | Custom error validation function                     |
| `setupEnv`     | No       | Environment setup function returning cleanup         |

## Naming Conventions

- Test function: `Test<FunctionName>` or `Test<FunctionName>_<Scenario>`
- Subtest names: lowercase, descriptive, spaces allowed
- Input fields: match parameter names or use `input`/`args`
- Output fields: prefix with `want` (e.g., `want`, `wantErr`, `wantResult`)

## Common Patterns

### 1. Basic Table Test

```go
func TestWithRegion(t *testing.T) {
    tests := []struct {
        name   string
        region string
    }{
        {"auto region", "auto"},
        {"us-west-2", "us-west-2"},
        {"eu-central-1", "eu-central-1"},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            o := &Options{}
            WithRegion(tt.region)(o)

            if o.Region != tt.region {
                t.Errorf("Region = %v, want %v", o.Region, tt.region)
            }
        })
    }
}
```

### 2. Error Checking with `wantErr`

```go
func TestNew_errorCases(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        wantErr error
    }{
        {"empty input", "", ErrInvalidInput},
        {"invalid input", "!!!", ErrInvalidInput},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            _, err := Parse(tt.input)
            if !errors.Is(err, tt.wantErr) {
                t.Errorf("error = %v, want %v", err, tt.wantErr)
            }
        })
    }
}
```

### 3. Custom Error Validation with `errCheck`

```go
func TestNew_customErrors(t *testing.T) {
    tests := []struct {
        name     string
        setupEnv func() func()
        wantErr  error
        errCheck func(error) bool
    }{
        {
            name: "no bucket name returns ErrNoBucketName",
            setupEnv: func() func() { return func() {} },
            wantErr:  ErrNoBucketName,
            errCheck: func(err error) bool {
                return errors.Is(err, ErrNoBucketName)
            },
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            cleanup := tt.setupEnv()
            defer cleanup()

            _, err := New(context.Background())

            if tt.wantErr != nil {
                if tt.errCheck != nil {
                    if !tt.errCheck(err) {
                        t.Errorf("error = %v, want %v", err, tt.wantErr)
                    }
                }
            }
        })
    }
}
```

### 4. Environment Setup with `setupEnv`

```go
func TestNew_envVarOverrides(t *testing.T) {
    tests := []struct {
        name        string
        setupEnv    func() func()
        options     []Option
        wantErr     error
    }{
        {
            name: "bucket from env var",
            setupEnv: func() func() {
                os.Setenv("TIGRIS_STORAGE_BUCKET", "test-bucket")
                return func() { os.Unsetenv("TIGRIS_STORAGE_BUCKET") }
            },
            wantErr: nil,
        },
        {
            name: "bucket from option overrides env var",
            setupEnv: func() func() {
                os.Setenv("TIGRIS_STORAGE_BUCKET", "env-bucket")
                return func() { os.Unsetenv("TIGRIS_STORAGE_BUCKET") }
            },
            options: []Option{
                func(o *Options) { o.BucketName = "option-bucket" },
            },
            wantErr: nil,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            cleanup := tt.setupEnv()
            defer cleanup()

            _, err := New(context.Background(), tt.options...)

            if tt.wantErr != nil && !errors.Is(err, tt.wantErr) {
                t.Errorf("error = %v, want %v", err, tt.wantErr)
            }
        })
    }
}
```

## Integration Test Guards

For tests requiring real credentials, use a skip helper:

```go
// skipIfNoCreds skips the test if Tigris credentials are not set.
// Use this for integration tests that require real Tigris operations.
func skipIfNoCreds(t *testing.T) {
    t.Helper()
    if os.Getenv("TIGRIS_STORAGE_ACCESS_KEY_ID") == "" ||
        os.Getenv("TIGRIS_STORAGE_SECRET_ACCESS_KEY") == "" {
        t.Skip("skipping: TIGRIS_STORAGE_ACCESS_KEY_ID and TIGRIS_STORAGE_SECRET_ACCESS_KEY not set")
    }
}

func TestCreateBucket(t *testing.T) {
    tests := []struct {
        name    string
        bucket  string
        options []BucketOption
        wantErr error
    }{
        {
            name:    "create snapshot-enabled bucket",
            bucket:  "test-bucket",
            options: []BucketOption{WithEnableSnapshot()},
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            skipIfNoCreds(t)

            // test implementation
        })
    }
}
```

## Test Helpers

Use `t.Helper()` in helper functions for proper line number reporting:

```go
func setupTestBucket(t *testing.T, ctx context.Context, client *Client) string {
    t.Helper()
    skipIfNoCreds(t)

    bucket := "test-bucket-" + randomSuffix()
    err := client.CreateBucket(ctx, bucket)
    if err != nil {
        t.Fatalf("failed to create test bucket: %v", err)
    }
    return bucket
}

func cleanupTestBucket(t *testing.T, ctx context.Context, client *Client, bucket string) {
    t.Helper()
    err := client.DeleteBucket(ctx, bucket, WithForceDelete())
    if err != nil {
        t.Logf("warning: failed to cleanup test bucket %s: %v", bucket, err)
    }
}
```

## Checklist

When writing table-driven tests:

- [ ] Table struct has `name` field as first field
- [ ] Each test case has a descriptive name
- [ ] Input fields use clear naming (match parameters or use `input`)
- [ ] Expected output fields prefixed with `want`
- [ ] Iteration uses `t.Run(tt.name, func(t *testing.T) { ... })`
- [ ] Error checking uses `errors.Is()` for error comparison
- [ ] Environment setup includes cleanup in `defer`
- [ ] Integration tests use `skipIfNoCreds(t)` helper
- [ ] Test helpers use `t.Helper()` for proper line reporting
- [ ] Test file is `*_test.go` and lives next to the code it tests

## Best Practices

### Detailed Error Messages

Include both actual and expected values in error messages for clear failure diagnosis:

```go
t.Errorf("got %q, want %q", actual, expected)
```

**Note:** `t.Errorf` is not an assertion - the test continues after logging. This helps identify whether failures are systematic or isolated to specific cases.

### Maps for Test Cases

Consider using a map instead of a slice for test cases. Map iteration order is non-deterministic, which ensures test cases are truly independent:

```go
tests := map[string]struct {
    input string
    want  string
}{
    "empty string":       {input: "", want: ""},
    "single character":   {input: "x", want: "x"},
    "multi-byte glyph":   {input: "🎉", want: "🎉"},
}

for name, tt := range tests {
    t.Run(name, func(t *testing.T) {
        got := process(tt.input)
        if got != tt.want {
            t.Errorf("got %q, want %q", got, tt.want)
        }
    })
}
```

### Parallel Testing

Add `t.Parallel()` calls to run test cases in parallel. The loop variable is automatically captured per iteration:

```go
func TestFunction(t *testing.T) {
    tests := []struct {
        name string
        input string
    }{
        // ... test cases
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // marks this subtest as parallel
            // test implementation
        })
    }
}
```

## References

- [Go Wiki: TableDrivenTests](https://go.dev/wiki/TableDrivenTests) - Official Go community best practices for table-driven testing
- [Go Testing Package](https://pkg.go.dev/testing/) - Standard library testing documentation
- [Prefer Table Driven Tests](https://dave.cheney.net/2019/05/07/prefer-table-driven-tests) - Dave Cheney's guide on when and why to use table-driven tests over traditional test structures
