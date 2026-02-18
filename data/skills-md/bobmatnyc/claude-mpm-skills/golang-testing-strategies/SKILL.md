---
name: golang-testing-strategies
description: "Comprehensive Go testing strategies including table-driven tests, testify assertions, gomock interface mocking, benchmark testing, and CI/CD integration"
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Master Go testing through table-driven patterns, testify assertions, gomock mocking, benchmarks, and CI integration for production-quality test suites"
    when_to_use: "Writing comprehensive test suites, setting up CI/CD testing pipelines, mocking external dependencies, performance benchmarking critical paths, ensuring race-free concurrent code"
    quick_start: "1. Structure tests with table-driven pattern 2. Use testify for assertions 3. Mock interfaces with gomock 4. Benchmark critical paths 5. Integrate coverage in CI/CD"
  token_estimate:
    entry: 150
    full: 4500
context_limit: 700
tags:
  - testing
  - golang
  - testify
  - gomock
  - benchmarks
  - table-driven-tests
requires_tools: []
---

# Go Testing Strategies

## Overview

Go provides a robust built-in testing framework (`testing` package) that emphasizes simplicity and developer productivity. Combined with community tools like testify and gomock, Go testing enables comprehensive test coverage with minimal boilerplate.

**Key Features:**
- 📋 **Table-Driven Tests**: Idiomatic pattern for testing multiple inputs
- ✅ **Testify**: Readable assertions and test suites
- 🎭 **Gomock**: Type-safe interface mocking
- ⚡ **Benchmarking**: Built-in performance testing
- 🔍 **Race Detector**: Concurrent code safety verification
- 📊 **Coverage**: Native coverage reporting and enforcement
- 🚀 **CI Integration**: Test caching and parallel execution

## When to Use This Skill

Activate this skill when:
- Writing test suites for Go libraries or applications
- Setting up testing infrastructure for new projects
- Mocking external dependencies (databases, APIs, services)
- Benchmarking performance-critical code paths
- Ensuring thread-safe concurrent implementations
- Integrating tests into CI/CD pipelines
- Migrating from other testing frameworks

## Core Testing Principles

### The Go Testing Philosophy

1. **Simplicity Over Magic**: Use standard library when possible
2. **Table-Driven Tests**: Test multiple scenarios with single function
3. **Subtests**: Organize related tests with `t.Run()`
4. **Interface-Based Mocking**: Mock dependencies through interfaces
5. **Test Files Colocate**: Place `*_test.go` files alongside code
6. **Package Naming**: Use `package_test` for external tests, `package` for internal

### Test Organization

**File Naming Convention:**
- Unit tests: `file_test.go`
- Integration tests: `file_integration_test.go`
- Benchmark tests: Prefix with `Benchmark` in same test file

**Package Structure:**
```
mypackage/
├── user.go
├── user_test.go              // Internal tests (same package)
├── user_external_test.go     // External tests (package mypackage_test)
├── integration_test.go       // Integration tests
└── testdata/                 // Test fixtures (ignored by go build)
    └── golden.json
```

## Table-Driven Test Pattern

### Basic Structure

The idiomatic Go testing pattern for testing multiple inputs:

```go
func TestUserValidation(t *testing.T) {
    tests := []struct {
        name    string
        input   User
        wantErr bool
        errMsg  string
    }{
        {
            name:    "valid user",
            input:   User{Name: "Alice", Age: 30, Email: "alice@example.com"},
            wantErr: false,
        },
        {
            name:    "empty name",
            input:   User{Name: "", Age: 30, Email: "alice@example.com"},
            wantErr: true,
            errMsg:  "name is required",
        },
        {
            name:    "invalid email",
            input:   User{Name: "Bob", Age: 25, Email: "invalid"},
            wantErr: true,
            errMsg:  "invalid email format",
        },
        {
            name:    "negative age",
            input:   User{Name: "Charlie", Age: -5, Email: "charlie@example.com"},
            wantErr: true,
            errMsg:  "age must be positive",
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := ValidateUser(tt.input)

            if (err != nil) != tt.wantErr {
                t.Errorf("ValidateUser() error = %v, wantErr %v", err, tt.wantErr)
                return
            }

            if tt.wantErr && err.Error() != tt.errMsg {
                t.Errorf("ValidateUser() error message = %v, want %v", err.Error(), tt.errMsg)
            }
        })
    }
}
```

### Parallel Test Execution

Enable parallel test execution for independent tests:

```go
func TestConcurrentOperations(t *testing.T) {
    tests := []struct {
        name string
        fn   func() int
        want int
    }{
        {"operation 1", func() int { return compute1() }, 42},
        {"operation 2", func() int { return compute2() }, 84},
        {"operation 3", func() int { return compute3() }, 126},
    }

    for _, tt := range tests {
        tt := tt // Capture range variable
        t.Run(tt.name, func(t *testing.T) {
            t.Parallel() // Run tests concurrently

            got := tt.fn()
            if got != tt.want {
                t.Errorf("got %v, want %v", got, tt.want)
            }
        })
    }
}
```

## Testify Framework

### Installation

```bash
go get github.com/stretchr/testify
```

### Assertions

Replace verbose error checking with readable assertions:

```go
import (
    "testing"
    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/require"
)

func TestCalculator(t *testing.T) {
    calc := NewCalculator()

    // assert: Test continues on failure
    assert.Equal(t, 5, calc.Add(2, 3))
    assert.NotNil(t, calc)
    assert.True(t, calc.IsReady())

    // require: Test stops on failure (for critical assertions)
    result, err := calc.Divide(10, 2)
    require.NoError(t, err) // Stop if error occurs
    assert.Equal(t, 5, result)
}

func TestUserOperations(t *testing.T) {
    user := &User{ID: 1, Name: "Alice", Email: "alice@example.com"}

    // Object matching
    assert.Equal(t, 1, user.ID)
    assert.Contains(t, user.Email, "@")
    assert.Len(t, user.Name, 5)

    // Partial matching
    assert.ObjectsAreEqual(user, &User{
        ID:    1,
        Name:  "Alice",
        Email: assert.AnythingOfType("string"),
    })
}
```

### Test Suites

Organize related tests with setup/teardown:

```go
import (
    "testing"
    "github.com/stretchr/testify/suite"
)

type UserServiceTestSuite struct {
    suite.Suite
    db      *sql.DB
    service *UserService
}

// SetupSuite runs once before all tests
func (s *UserServiceTestSuite) SetupSuite() {
    s.db = setupTestDatabase()
    s.service = NewUserService(s.db)
}

// TearDownSuite runs once after all tests
func (s *UserServiceTestSuite) TearDownSuite() {
    s.db.Close()
}

// SetupTest runs before each test
func (s *UserServiceTestSuite) SetupTest() {
    cleanDatabase(s.db)
}

// TearDownTest runs after each test
func (s *UserServiceTestSuite) TearDownTest() {
    // Cleanup if needed
}

// Test methods must start with "Test"
func (s *UserServiceTestSuite) TestCreateUser() {
    user := &User{Name: "Alice", Email: "alice@example.com"}

    err := s.service.Create(user)
    s.NoError(err)
    s.NotEqual(0, user.ID) // ID assigned
}

func (s *UserServiceTestSuite) TestGetUser() {
    // Setup
    user := &User{Name: "Bob", Email: "bob@example.com"}
    s.service.Create(user)

    // Test
    retrieved, err := s.service.GetByID(user.ID)
    s.NoError(err)
    s.Equal(user.Name, retrieved.Name)
}

// Run the suite
func TestUserServiceTestSuite(t *testing.T) {
    suite.Run(t, new(UserServiceTestSuite))
}
```

## Gomock Interface Mocking

### Installation

```bash
go install github.com/golang/mock/mockgen@latest
```

### Generate Mocks

```go
// user_repository.go
package repository

//go:generate mockgen -source=user_repository.go -destination=mocks/mock_user_repository.go -package=mocks

type UserRepository interface {
    GetByID(id int) (*User, error)
    Create(user *User) error
    Update(user *User) error
    Delete(id int) error
}
```

Generate mocks:
```bash
go generate ./...
# Or manually:
mockgen -source=user_repository.go -destination=mocks/mock_user_repository.go -package=mocks
```

### Using Mocks in Tests

```go
import (
    "testing"
    "github.com/golang/mock/gomock"
    "github.com/stretchr/testify/assert"
    "myapp/repository/mocks"
)

func TestUserService_GetUser(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    // Create mock
    mockRepo := mocks.NewMockUserRepository(ctrl)

    // Set expectations
    expectedUser := &User{ID: 1, Name: "Alice"}
    mockRepo.EXPECT().
        GetByID(1).
        Return(expectedUser, nil).
        Times(1)

    // Test
    service := NewUserService(mockRepo)
    user, err := service.GetUser(1)

    // Assertions
    assert.NoError(t, err)
    assert.Equal(t, expectedUser, user)
}

func TestUserService_CreateUser_Validation(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRepo := mocks.NewMockUserRepository(ctrl)

    // Expect Create to NOT be called (validation should fail first)
    mockRepo.EXPECT().Create(gomock.Any()).Times(0)

    service := NewUserService(mockRepo)
    err := service.CreateUser(&User{Name: ""}) // Invalid user

    assert.Error(t, err)
    assert.Contains(t, err.Error(), "name is required")
}
```

### Custom Matchers

```go
// Custom matcher for complex validation
type userMatcher struct {
    expectedEmail string
}

func (m userMatcher) Matches(x interface{}) bool {
    user, ok := x.(*User)
    if !ok {
        return false
    }
    return user.Email == m.expectedEmail
}

func (m userMatcher) String() string {
    return "matches user with email: " + m.expectedEmail
}

func UserWithEmail(email string) gomock.Matcher {
    return userMatcher{expectedEmail: email}
}

// Usage in test
func TestCustomMatcher(t *testing.T) {
    ctrl := gomock.NewController(t)
    defer ctrl.Finish()

    mockRepo := mocks.NewMockUserRepository(ctrl)

    mockRepo.EXPECT().
        Create(UserWithEmail("alice@example.com")).
        Return(nil)

    service := NewUserService(mockRepo)
    service.CreateUser(&User{Name: "Alice", Email: "alice@example.com"})
}
```

## Benchmark Testing

### Basic Benchmarks

```go
func BenchmarkAdd(b *testing.B) {
    calc := NewCalculator()

    for i := 0; i < b.N; i++ {
        calc.Add(2, 3)
    }
}

func BenchmarkStringConcatenation(b *testing.B) {
    b.Run("plus operator", func(b *testing.B) {
        for i := 0; i < b.N; i++ {
            _ = "hello" + "world"
        }
    })

    b.Run("strings.Builder", func(b *testing.B) {
        for i := 0; i < b.N; i++ {
            var sb strings.Builder
            sb.WriteString("hello")
            sb.WriteString("world")
            _ = sb.String()
        }
    })
}
```

### Running Benchmarks

```bash
# Run all benchmarks
go test -bench=.

# Run specific benchmark
go test -bench=BenchmarkAdd

# With memory allocation stats
go test -bench=. -benchmem

# Compare benchmarks
go test -bench=. -benchmem > old.txt
# Make changes
go test -bench=. -benchmem > new.txt
benchstat old.txt new.txt
```

### Benchmark Output Example

```
BenchmarkAdd-8                  1000000000      0.25 ns/op      0 B/op      0 allocs/op
BenchmarkStringBuilder-8        50000000        28.5 ns/op      64 B/op     1 allocs/op
```

Reading: `50000000` iterations, `28.5 ns/op` per operation, `64 B/op` bytes allocated per op, `1 allocs/op` allocations per op

## Advanced Testing Patterns

### httptest for HTTP Handlers

```go
import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestUserHandler(t *testing.T) {
    handler := http.HandlerFunc(UserHandler)

    req := httptest.NewRequest("GET", "/users/1", nil)
    rec := httptest.NewRecorder()

    handler.ServeHTTP(rec, req)

    assert.Equal(t, http.StatusOK, rec.Code)
    assert.Contains(t, rec.Body.String(), "Alice")
}

func TestHTTPClient(t *testing.T) {
    // Mock server
    server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        assert.Equal(t, "/api/users", r.URL.Path)
        w.WriteHeader(http.StatusOK)
        w.Write([]byte(`{"id": 1, "name": "Alice"}`))
    }))
    defer server.Close()

    // Test client against mock server
    client := NewAPIClient(server.URL)
    user, err := client.GetUser(1)

    assert.NoError(t, err)
    assert.Equal(t, "Alice", user.Name)
}
```

### Race Detector

Detect data races in concurrent code:

```bash
go test -race ./...
```

Example test for concurrent safety:

```go
func TestConcurrentMapAccess(t *testing.T) {
    cache := NewSafeCache()

    var wg sync.WaitGroup
    for i := 0; i < 100; i++ {
        wg.Add(1)
        go func(val int) {
            defer wg.Done()
            cache.Set(fmt.Sprintf("key%d", val), val)
        }(i)
    }

    wg.Wait()
    assert.Equal(t, 100, cache.Len())
}
```

### Golden File Testing

Test against expected output files:

```go
func TestRenderTemplate(t *testing.T) {
    output := RenderTemplate("user", User{Name: "Alice"})

    goldenFile := "testdata/user_template.golden"

    if *update {
        // Update golden file: go test -update
        os.WriteFile(goldenFile, []byte(output), 0644)
    }

    expected, err := os.ReadFile(goldenFile)
    require.NoError(t, err)

    assert.Equal(t, string(expected), output)
}

var update = flag.Bool("update", false, "update golden files")
```

## CI/CD Integration

### GitHub Actions Example

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Go
        uses: actions/setup-go@v4
        with:
          go-version: '1.23'

      - name: Run tests
        run: go test -v -race -coverprofile=coverage.out ./...

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.out

      - name: Check coverage threshold
        run: |
          go tool cover -func=coverage.out | grep total | awk '{print $3}' | sed 's/%//' | \
          awk '{if ($1 < 80) exit 1}'
```

### Coverage Enforcement

```bash
# Generate coverage report
go test -coverprofile=coverage.out ./...

# View coverage in terminal
go tool cover -func=coverage.out

# Generate HTML report
go tool cover -html=coverage.out -o coverage.html

# Check coverage threshold (fail if < 80%)
go test -coverprofile=coverage.out ./... && \
go tool cover -func=coverage.out | grep total | awk '{if (substr($3, 1, length($3)-1) < 80) exit 1}'
```

## Decision Trees

### When to Use Each Testing Tool

**Use Standard `testing` Package When:**
- Simple unit tests with few assertions
- No external dependencies to mock
- Performance benchmarking
- Minimal dependencies preferred

**Use Testify When:**
- Need readable assertions (`assert.Equal` vs verbose checks)
- Test suites with setup/teardown
- Multiple similar test cases
- Prefer expressive test code

**Use Gomock When:**
- Testing code with interface dependencies
- Need precise call verification (times, order)
- Complex mock behavior with multiple scenarios
- Type-safe mocking required

**Use Benchmarks When:**
- Optimizing performance-critical code
- Comparing algorithm implementations
- Detecting performance regressions
- Memory allocation profiling

**Use httptest When:**
- Testing HTTP handlers
- Mocking external HTTP APIs
- Integration testing HTTP clients
- Testing middleware chains

**Use Race Detector When:**
- Writing concurrent code
- Using goroutines and channels
- Shared state across goroutines
- CI/CD for all concurrent code

## Anti-Patterns to Avoid

❌ **Don't Mock Everything**
```go
// WRONG: Over-mocking makes tests brittle
mockLogger := mocks.NewMockLogger(ctrl)
mockConfig := mocks.NewMockConfig(ctrl)
mockMetrics := mocks.NewMockMetrics(ctrl)
// Too many mocks = fragile test
```

✅ **Do: Mock Only External Dependencies**
```go
// CORRECT: Mock only database, use real logger/config
mockRepo := mocks.NewMockUserRepository(ctrl)
service := NewUserService(mockRepo, realLogger, realConfig)
```

❌ **Don't Test Implementation Details**
```go
// WRONG: Testing internal state
assert.Equal(t, "processing", service.internalState)
```

✅ **Do: Test Public Behavior**
```go
// CORRECT: Test observable outcomes
user, err := service.GetUser(1)
assert.NoError(t, err)
assert.Equal(t, "Alice", user.Name)
```

❌ **Don't Ignore Error Cases**
```go
// WRONG: Only testing happy path
func TestGetUser(t *testing.T) {
    user, _ := service.GetUser(1) // Ignoring error!
    assert.NotNil(t, user)
}
```

✅ **Do: Test Error Conditions**
```go
// CORRECT: Test both success and error cases
func TestGetUser_NotFound(t *testing.T) {
    user, err := service.GetUser(999)
    assert.Error(t, err)
    assert.Nil(t, user)
    assert.Contains(t, err.Error(), "not found")
}
```

## Best Practices

1. **Colocate Tests**: Place `*_test.go` files alongside source code
2. **Use Subtests**: Organize related tests with `t.Run()`
3. **Parallel When Safe**: Enable `t.Parallel()` for independent tests
4. **Mock Interfaces**: Design for testability with interface dependencies
5. **Test Errors**: Verify both success and failure paths
6. **Benchmark Critical Paths**: Profile performance-sensitive code
7. **Run Race Detector**: Always use `-race` for concurrent code
8. **Enforce Coverage**: Set minimum thresholds in CI (typically 80%)
9. **Use Golden Files**: Test complex outputs with expected files
10. **Keep Tests Fast**: Mock slow operations, use `-short` flag for quick runs

## Resources

**Official Documentation:**
- Go Testing Package: https://pkg.go.dev/testing
- Table-Driven Tests: https://github.com/golang/go/wiki/TableDrivenTests
- Subtests and Sub-benchmarks: https://go.dev/blog/subtests

**Testing Frameworks:**
- Testify: https://github.com/stretchr/testify
- Gomock: https://github.com/golang/mock
- httptest: https://pkg.go.dev/net/http/httptest

**Recent Guides (2025):**
- "Go Unit Testing: Structure & Best Practices" (November 2025)
- Go Wiki: CommonMistakes in Testing
- Google Go Style Guide - Testing: https://google.github.io/styleguide/go/

**Related Skills:**
- **golang-engineer**: Core Go patterns and concurrency
- **verification-before-completion**: Testing as part of "done"
- **testing-anti-patterns**: Avoid common testing mistakes

## Quick Reference

### Run Tests
```bash
go test ./...                    # All tests
go test -v ./...                 # Verbose output
go test -short ./...             # Skip slow tests
go test -run TestUserCreate      # Specific test
go test -race ./...              # With race detector
go test -cover ./...             # With coverage
go test -coverprofile=c.out ./... # Coverage file
go test -bench=. -benchmem       # Benchmarks with memory
```

### Generate Mocks
```bash
go generate ./...                           # All //go:generate directives
mockgen -source=interface.go -destination=mock.go
```

### Coverage Analysis
```bash
go tool cover -func=coverage.out           # Coverage per function
go tool cover -html=coverage.out           # HTML report
```

---

**Token Estimate**: ~4,500 tokens (entry point + full content)
**Version**: 1.0.0
**Last Updated**: 2025-12-03
