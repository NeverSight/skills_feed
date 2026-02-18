---
name: golang-http-frameworks
description: "Go HTTP API development with net/http, Chi, Gin, Echo, and Fiber frameworks"
version: 1.0.0
category: toolchain
author: Claude MPM Team
license: MIT
progressive_disclosure:
  entry_point:
    summary: "Master Go HTTP frameworks from stdlib net/http to Chi, Gin, Echo, and Fiber for building production-ready REST APIs with middleware, validation, and client patterns"
    when_to_use: "Building RESTful APIs, choosing HTTP framework, implementing authentication middleware, designing REST endpoints, testing HTTP handlers, optimizing API performance"
    quick_start: "1. Choose framework (stdlib, Chi, Gin, Echo, Fiber) 2. Structure routes and middleware 3. Implement request validation 4. Design error handling 5. Test with httptest"
  token_estimate:
    entry: 160
    full: 5000
context_limit: 700
tags:
  - http
  - golang
  - chi
  - gin
  - echo
  - fiber
  - rest-api
  - middleware
requires_tools: []
---

# Go HTTP Frameworks & REST APIs

## Overview

Go provides exceptional HTTP capabilities starting with the standard library's `net/http` package. Go 1.22+ introduced enhanced pattern routing in `ServeMux`, making stdlib viable for many applications. For more complex needs, frameworks like Chi, Gin, Echo, and Fiber offer additional features while maintaining Go's simplicity and performance.

**Key Features:**
- 🌐 **net/http**: Production-ready standard library with Go 1.22+ routing
- 🎯 **Chi**: Lightweight, stdlib-compatible router with middleware chains
- ⚡ **Gin**: High-performance framework with binding and validation
- 🛡️ **Echo**: Type-safe, enterprise framework with OpenAPI support
- 🚀 **Fiber**: Express.js-inspired framework with WebSocket support
- 🔧 **Middleware**: Composable request/response processing
- ✅ **Validation**: Struct tag-based request validation
- 🧪 **Testing**: httptest.Server for comprehensive integration tests

## When to Use This Skill

Activate this skill when:
- Building RESTful APIs or web services
- Choosing appropriate HTTP framework for project requirements
- Implementing authentication or authorization middleware
- Designing REST endpoint patterns and validation
- Testing HTTP handlers and middleware chains
- Optimizing API performance and response times
- Migrating between HTTP frameworks

## Framework Selection Guide

### net/http (Standard Library) - Go 1.22+

**Use When:**
- Building simple to moderate complexity APIs
- Avoiding external dependencies is priority
- Need maximum compatibility and long-term stability
- Team prefers explicit over implicit patterns

**Strengths:**
- Zero dependencies, part of Go standard library
- Go 1.22+ pattern routing with path parameters
- Excellent performance and stability
- Extensive ecosystem compatibility
- No framework lock-in

**Limitations:**
- More verbose middleware composition
- Manual request validation
- No built-in binding or rendering

**Example:**
```go
package main

import (
    "encoding/json"
    "net/http"
    "log"
)

// Go 1.22+ pattern routing
func main() {
    mux := http.NewServeMux()

    // Path parameters with {param} syntax
    mux.HandleFunc("GET /users/{id}", getUserHandler)
    mux.HandleFunc("POST /users", createUserHandler)
    mux.HandleFunc("GET /users", listUsersHandler)

    // Middleware wrapping
    handler := loggingMiddleware(mux)

    log.Fatal(http.ListenAndServe(":8080", handler))
}

func getUserHandler(w http.ResponseWriter, r *http.Request) {
    id := r.PathValue("id") // Go 1.22+ path parameter extraction

    user := User{ID: id, Name: "John Doe"}

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(user)
}

func loggingMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        log.Printf("%s %s", r.Method, r.URL.Path)
        next.ServeHTTP(w, r)
    })
}

type User struct {
    ID   string `json:"id"`
    Name string `json:"name"`
}
```

### Chi - Lightweight Router

**Use When:**
- Want stdlib-compatible router with better ergonomics
- Need clean middleware composition
- Prefer explicit over magic patterns
- Building moderate to complex routing structures

**Strengths:**
- 100% compatible with `net/http`
- Excellent middleware ecosystem
- Route grouping and nesting
- Context-based parameter passing
- Minimal performance overhead

**Installation:**
```bash
go get -u github.com/go-chi/chi/v5
```

**Example:**
```go
package main

import (
    "encoding/json"
    "net/http"
    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"
)

func main() {
    r := chi.NewRouter()

    // Built-in middleware
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    r.Use(middleware.RequestID)

    // Route grouping
    r.Route("/api/v1", func(r chi.Router) {
        r.Route("/users", func(r chi.Router) {
            r.Get("/", listUsers)
            r.Post("/", createUser)

            r.Route("/{userID}", func(r chi.Router) {
                r.Use(UserContext) // Middleware for nested routes
                r.Get("/", getUser)
                r.Put("/", updateUser)
                r.Delete("/", deleteUser)
            })
        })
    })

    http.ListenAndServe(":8080", r)
}

func UserContext(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        userID := chi.URLParam(r, "userID")
        // Load user from database, set in context
        ctx := context.WithValue(r.Context(), "user", userID)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

func getUser(w http.ResponseWriter, r *http.Request) {
    userID := r.Context().Value("user").(string)
    // Return user data
    json.NewEncoder(w).Encode(map[string]string{"id": userID})
}
```

### Gin - High Performance Framework

**Use When:**
- Need maximum performance (8x faster than most frameworks)
- Want batteries-included experience
- Require built-in validation and binding
- Building JSON APIs with minimal boilerplate

**Strengths:**
- Extremely fast (fastest Go framework in benchmarks)
- Built-in JSON binding and validation
- Middleware ecosystem
- Group-based routing
- Custom error handling

**Installation:**
```bash
go get -u github.com/gin-gonic/gin
```

**Example:**
```go
package main

import (
    "net/http"
    "github.com/gin-gonic/gin"
)

type CreateUserRequest struct {
    Name  string `json:"name" binding:"required,min=3"`
    Email string `json:"email" binding:"required,email"`
    Age   int    `json:"age" binding:"required,gte=18"`
}

func main() {
    r := gin.Default() // Logger + Recovery middleware

    api := r.Group("/api/v1")
    {
        users := api.Group("/users")
        {
            users.GET("", listUsers)
            users.POST("", createUser)
            users.GET("/:id", getUser)
            users.PUT("/:id", updateUser)
            users.DELETE("/:id", deleteUser)
        }
    }

    r.Run(":8080")
}

func createUser(c *gin.Context) {
    var req CreateUserRequest

    // Automatic validation based on struct tags
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
        return
    }

    // Process user creation
    user := User{
        ID:    generateID(),
        Name:  req.Name,
        Email: req.Email,
        Age:   req.Age,
    }

    c.JSON(http.StatusCreated, user)
}

func getUser(c *gin.Context) {
    id := c.Param("id")

    // Return user
    c.JSON(http.StatusOK, gin.H{
        "id":   id,
        "name": "John Doe",
    })
}
```

### Echo - Enterprise Framework

**Use When:**
- Building enterprise applications
- Need OpenAPI/Swagger integration
- Want comprehensive middleware library
- Require type-safe routing and binding

**Strengths:**
- Type-safe routing with automatic parameter binding
- Built-in middleware for common patterns
- OpenAPI/Swagger generation support
- Excellent error handling middleware
- WebSocket support

**Installation:**
```bash
go get -u github.com/labstack/echo/v4
```

**Example:**
```go
package main

import (
    "net/http"
    "github.com/labstack/echo/v4"
    "github.com/labstack/echo/v4/middleware"
)

func main() {
    e := echo.New()

    // Middleware
    e.Use(middleware.Logger())
    e.Use(middleware.Recover())
    e.Use(middleware.CORS())

    // Routes
    e.GET("/users/:id", getUser)
    e.POST("/users", createUser)
    e.PUT("/users/:id", updateUser)
    e.DELETE("/users/:id", deleteUser)

    e.Logger.Fatal(e.Start(":8080"))
}

func getUser(c echo.Context) error {
    id := c.Param("id")

    user := User{ID: id, Name: "John Doe"}
    return c.JSON(http.StatusOK, user)
}

func createUser(c echo.Context) error {
    var user User

    if err := c.Bind(&user); err != nil {
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }

    if err := c.Validate(&user); err != nil {
        return echo.NewHTTPError(http.StatusBadRequest, err.Error())
    }

    return c.JSON(http.StatusCreated, user)
}

// Custom error handler
func customErrorHandler(err error, c echo.Context) {
    code := http.StatusInternalServerError
    message := "Internal Server Error"

    if he, ok := err.(*echo.HTTPError); ok {
        code = he.Code
        message = he.Message.(string)
    }

    c.JSON(code, map[string]string{"error": message})
}
```

### Fiber - Express.js Style

**Use When:**
- Team familiar with Express.js patterns
- Need WebSocket support out of the box
- Building real-time applications
- Want fastest route matching performance

**Strengths:**
- Express.js-inspired API (easy for Node.js developers)
- Fastest route matching (uses fasthttp)
- Built-in WebSocket support
- Template engine support
- File upload handling

**Limitations:**
- Uses fasthttp instead of net/http (less ecosystem compatibility)
- Not compatible with standard http.Handler interface
- Slightly less mature ecosystem

**Installation:**
```bash
go get -u github.com/gofiber/fiber/v2
```

**Example:**
```go
package main

import (
    "github.com/gofiber/fiber/v2"
    "github.com/gofiber/fiber/v2/middleware/logger"
    "github.com/gofiber/fiber/v2/middleware/cors"
)

func main() {
    app := fiber.New()

    // Middleware
    app.Use(logger.New())
    app.Use(cors.New())

    // Routes
    api := app.Group("/api/v1")

    users := api.Group("/users")
    users.Get("/", listUsers)
    users.Post("/", createUser)
    users.Get("/:id", getUser)
    users.Put("/:id", updateUser)
    users.Delete("/:id", deleteUser)

    app.Listen(":8080")
}

func getUser(c *fiber.Ctx) error {
    id := c.Params("id")

    return c.JSON(fiber.Map{
        "id":   id,
        "name": "John Doe",
    })
}

func createUser(c *fiber.Ctx) error {
    var user User

    if err := c.BodyParser(&user); err != nil {
        return c.Status(400).JSON(fiber.Map{"error": err.Error()})
    }

    return c.Status(201).JSON(user)
}
```

## Common HTTP Patterns

### Request Validation

**Struct Tag Validation:**
```go
import "github.com/go-playground/validator/v10"

type CreateUserRequest struct {
    Name     string `json:"name" validate:"required,min=3,max=50"`
    Email    string `json:"email" validate:"required,email"`
    Age      int    `json:"age" validate:"required,gte=18,lte=120"`
    Password string `json:"password" validate:"required,min=8"`
}

var validate = validator.New()

func validateRequest(req interface{}) error {
    return validate.Struct(req)
}

// Usage
func createUser(w http.ResponseWriter, r *http.Request) {
    var req CreateUserRequest

    if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
        http.Error(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    if err := validateRequest(&req); err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }

    // Process valid request
}
```

**Custom Validators:**
```go
import "github.com/go-playground/validator/v10"

var validate = validator.New()

func init() {
    validate.RegisterValidation("username", validateUsername)
}

func validateUsername(fl validator.FieldLevel) bool {
    username := fl.Field().String()
    // Custom validation logic
    return len(username) >= 3 && isAlphanumeric(username)
}

type SignupRequest struct {
    Username string `validate:"required,username"`
    Email    string `validate:"required,email"`
}
```

### Middleware Patterns

**Authentication Middleware:**
```go
func AuthMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        token := r.Header.Get("Authorization")

        if token == "" {
            http.Error(w, "Unauthorized", http.StatusUnauthorized)
            return
        }

        // Validate token
        userID, err := validateToken(token)
        if err != nil {
            http.Error(w, "Invalid token", http.StatusUnauthorized)
            return
        }

        // Add user to context
        ctx := context.WithValue(r.Context(), "userID", userID)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

**Rate Limiting Middleware:**
```go
import (
    "golang.org/x/time/rate"
    "sync"
)

type RateLimiter struct {
    limiters map[string]*rate.Limiter
    mu       sync.RWMutex
    rate     rate.Limit
    burst    int
}

func NewRateLimiter(r rate.Limit, b int) *RateLimiter {
    return &RateLimiter{
        limiters: make(map[string]*rate.Limiter),
        rate:     r,
        burst:    b,
    }
}

func (rl *RateLimiter) getLimiter(ip string) *rate.Limiter {
    rl.mu.Lock()
    defer rl.mu.Unlock()

    limiter, exists := rl.limiters[ip]
    if !exists {
        limiter = rate.NewLimiter(rl.rate, rl.burst)
        rl.limiters[ip] = limiter
    }

    return limiter
}

func (rl *RateLimiter) Middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        ip := r.RemoteAddr
        limiter := rl.getLimiter(ip)

        if !limiter.Allow() {
            http.Error(w, "Rate limit exceeded", http.StatusTooManyRequests)
            return
        }

        next.ServeHTTP(w, r)
    })
}
```

**CORS Middleware:**
```go
func CORSMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        w.Header().Set("Access-Control-Allow-Origin", "*")
        w.Header().Set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        w.Header().Set("Access-Control-Allow-Headers", "Content-Type, Authorization")

        if r.Method == "OPTIONS" {
            w.WriteHeader(http.StatusOK)
            return
        }

        next.ServeHTTP(w, r)
    })
}
```

### Error Handling Strategies

**Custom Error Types:**
```go
type APIError struct {
    Code    int    `json:"code"`
    Message string `json:"message"`
    Details string `json:"details,omitempty"`
}

func (e *APIError) Error() string {
    return e.Message
}

// Error constructors
func NewBadRequestError(msg string) *APIError {
    return &APIError{Code: http.StatusBadRequest, Message: msg}
}

func NewNotFoundError(msg string) *APIError {
    return &APIError{Code: http.StatusNotFound, Message: msg}
}

func NewInternalError(msg string) *APIError {
    return &APIError{Code: http.StatusInternalServerError, Message: msg}
}
```

**Error Response Middleware:**
```go
type APIHandler func(w http.ResponseWriter, r *http.Request) error

func ErrorHandlerMiddleware(h APIHandler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        err := h(w, r)
        if err == nil {
            return
        }

        // Handle different error types
        var apiErr *APIError
        if errors.As(err, &apiErr) {
            w.Header().Set("Content-Type", "application/json")
            w.WriteHeader(apiErr.Code)
            json.NewEncoder(w).Encode(apiErr)
            return
        }

        // Unknown error - log and return generic message
        log.Printf("Internal error: %v", err)
        w.WriteHeader(http.StatusInternalServerError)
        json.NewEncoder(w).Encode(APIError{
            Code:    http.StatusInternalServerError,
            Message: "Internal server error",
        })
    })
}

// Usage
func getUserHandler(w http.ResponseWriter, r *http.Request) error {
    id := r.PathValue("id")

    user, err := db.GetUser(id)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return NewNotFoundError("User not found")
        }
        return fmt.Errorf("database error: %w", err)
    }

    w.Header().Set("Content-Type", "application/json")
    return json.NewEncoder(w).Encode(user)
}

// Register with middleware
mux.Handle("GET /users/{id}", ErrorHandlerMiddleware(getUserHandler))
```

### REST API Design Patterns

**Resource Naming Conventions:**
```go
// Good: Plural nouns for collections
GET    /api/v1/users           // List users
POST   /api/v1/users           // Create user
GET    /api/v1/users/{id}      // Get user
PUT    /api/v1/users/{id}      // Update user (full)
PATCH  /api/v1/users/{id}      // Update user (partial)
DELETE /api/v1/users/{id}      // Delete user

// Nested resources
GET    /api/v1/users/{id}/posts        // User's posts
POST   /api/v1/users/{id}/posts        // Create post for user
GET    /api/v1/users/{id}/posts/{pid}  // Specific post

// Avoid: Verbs in URLs (use HTTP methods instead)
// Bad: POST /api/v1/users/create
// Bad: GET  /api/v1/users/get/{id}
```

**Pagination Pattern:**
```go
type PaginationParams struct {
    Page     int `json:"page" validate:"gte=1"`
    PageSize int `json:"page_size" validate:"gte=1,lte=100"`
}

type PaginatedResponse struct {
    Data       interface{} `json:"data"`
    Page       int         `json:"page"`
    PageSize   int         `json:"page_size"`
    TotalCount int         `json:"total_count"`
    TotalPages int         `json:"total_pages"`
}

func listUsers(w http.ResponseWriter, r *http.Request) {
    // Parse pagination params
    page, _ := strconv.Atoi(r.URL.Query().Get("page"))
    if page < 1 {
        page = 1
    }

    pageSize, _ := strconv.Atoi(r.URL.Query().Get("page_size"))
    if pageSize < 1 || pageSize > 100 {
        pageSize = 20
    }

    // Fetch data
    users, totalCount := db.GetUsers(page, pageSize)
    totalPages := (totalCount + pageSize - 1) / pageSize

    response := PaginatedResponse{
        Data:       users,
        Page:       page,
        PageSize:   pageSize,
        TotalCount: totalCount,
        TotalPages: totalPages,
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(response)
}
```

**Query Parameter Filtering:**
```go
type UserFilter struct {
    Status    string `json:"status"`
    Role      string `json:"role"`
    CreatedAt string `json:"created_at"`
    Search    string `json:"search"`
}

func parseFilters(r *http.Request) UserFilter {
    return UserFilter{
        Status:    r.URL.Query().Get("status"),
        Role:      r.URL.Query().Get("role"),
        CreatedAt: r.URL.Query().Get("created_at"),
        Search:    r.URL.Query().Get("search"),
    }
}

func listUsers(w http.ResponseWriter, r *http.Request) {
    filters := parseFilters(r)

    users := db.GetUsersWithFilters(filters)

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(users)
}

// Example request: GET /api/v1/users?status=active&role=admin&search=john
```

### HTTP Client Patterns

**Production-Ready HTTP Client:**
```go
import (
    "context"
    "net/http"
    "time"
)

func NewHTTPClient() *http.Client {
    return &http.Client{
        Timeout: 30 * time.Second,
        Transport: &http.Transport{
            MaxIdleConns:        100,
            MaxIdleConnsPerHost: 10,
            IdleConnTimeout:     90 * time.Second,
            DisableKeepAlives:   false,
        },
    }
}

// Making requests with context
func fetchUser(ctx context.Context, userID string) (*User, error) {
    client := NewHTTPClient()

    req, err := http.NewRequestWithContext(
        ctx,
        "GET",
        fmt.Sprintf("https://api.example.com/users/%s", userID),
        nil,
    )
    if err != nil {
        return nil, fmt.Errorf("create request: %w", err)
    }

    req.Header.Set("Accept", "application/json")
    req.Header.Set("Authorization", "Bearer "+getToken())

    resp, err := client.Do(req)
    if err != nil {
        return nil, fmt.Errorf("execute request: %w", err)
    }
    defer resp.Body.Close()

    if resp.StatusCode != http.StatusOK {
        return nil, fmt.Errorf("unexpected status: %d", resp.StatusCode)
    }

    var user User
    if err := json.NewDecoder(resp.Body).Decode(&user); err != nil {
        return nil, fmt.Errorf("decode response: %w", err)
    }

    return &user, nil
}
```

**Retry Logic with Exponential Backoff:**
```go
import (
    "context"
    "math"
    "time"
)

type RetryConfig struct {
    MaxRetries int
    BaseDelay  time.Duration
    MaxDelay   time.Duration
}

func DoWithRetry(ctx context.Context, cfg RetryConfig, fn func() error) error {
    var err error

    for attempt := 0; attempt <= cfg.MaxRetries; attempt++ {
        err = fn()
        if err == nil {
            return nil
        }

        if attempt < cfg.MaxRetries {
            // Exponential backoff
            delay := time.Duration(math.Pow(2, float64(attempt))) * cfg.BaseDelay
            if delay > cfg.MaxDelay {
                delay = cfg.MaxDelay
            }

            select {
            case <-ctx.Done():
                return ctx.Err()
            case <-time.After(delay):
                // Continue to next attempt
            }
        }
    }

    return fmt.Errorf("max retries exceeded: %w", err)
}

// Usage
err := DoWithRetry(ctx, RetryConfig{
    MaxRetries: 3,
    BaseDelay:  100 * time.Millisecond,
    MaxDelay:   2 * time.Second,
}, func() error {
    return makeAPIRequest()
})
```

## Testing HTTP Handlers

**Using httptest.Server:**
```go
import (
    "net/http"
    "net/http/httptest"
    "testing"
)

func TestGetUser(t *testing.T) {
    // Create test server
    ts := httptest.NewServer(http.HandlerFunc(getUserHandler))
    defer ts.Close()

    // Make request
    resp, err := http.Get(ts.URL + "/users/123")
    if err != nil {
        t.Fatal(err)
    }
    defer resp.Body.Close()

    // Assertions
    if resp.StatusCode != http.StatusOK {
        t.Errorf("expected status 200, got %d", resp.StatusCode)
    }

    var user User
    if err := json.NewDecoder(resp.Body).Decode(&user); err != nil {
        t.Fatal(err)
    }

    if user.ID != "123" {
        t.Errorf("expected user ID 123, got %s", user.ID)
    }
}
```

**Testing Middleware:**
```go
func TestAuthMiddleware(t *testing.T) {
    handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        userID := r.Context().Value("userID")
        if userID == nil {
            t.Error("userID not found in context")
        }
        w.WriteHeader(http.StatusOK)
    })

    wrapped := AuthMiddleware(handler)

    tests := []struct {
        name       string
        token      string
        wantStatus int
    }{
        {"Valid token", "valid-token-123", http.StatusOK},
        {"Missing token", "", http.StatusUnauthorized},
        {"Invalid token", "invalid", http.StatusUnauthorized},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest("GET", "/test", nil)
            if tt.token != "" {
                req.Header.Set("Authorization", tt.token)
            }

            rr := httptest.NewRecorder()
            wrapped.ServeHTTP(rr, req)

            if rr.Code != tt.wantStatus {
                t.Errorf("expected status %d, got %d", tt.wantStatus, rr.Code)
            }
        })
    }
}
```

## Performance Optimization

**Response Compression:**
```go
import (
    "compress/gzip"
    "io"
    "net/http"
    "strings"
)

type gzipResponseWriter struct {
    io.Writer
    http.ResponseWriter
}

func (w gzipResponseWriter) Write(b []byte) (int, error) {
    return w.Writer.Write(b)
}

func GzipMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        if !strings.Contains(r.Header.Get("Accept-Encoding"), "gzip") {
            next.ServeHTTP(w, r)
            return
        }

        w.Header().Set("Content-Encoding", "gzip")
        gz := gzip.NewWriter(w)
        defer gz.Close()

        gzw := gzipResponseWriter{Writer: gz, ResponseWriter: w}
        next.ServeHTTP(gzw, r)
    })
}
```

**Connection Pooling Configuration:**
```go
import (
    "net"
    "net/http"
    "time"
)

func NewProductionHTTPClient() *http.Client {
    return &http.Client{
        Timeout: 30 * time.Second,
        Transport: &http.Transport{
            Proxy: http.ProxyFromEnvironment,
            DialContext: (&net.Dialer{
                Timeout:   30 * time.Second,
                KeepAlive: 30 * time.Second,
            }).DialContext,
            ForceAttemptHTTP2:     true,
            MaxIdleConns:          100,
            MaxIdleConnsPerHost:   10,
            IdleConnTimeout:       90 * time.Second,
            TLSHandshakeTimeout:   10 * time.Second,
            ExpectContinueTimeout: 1 * time.Second,
        },
    }
}
```

## Decision Tree

```
Building HTTP API in Go?
│
├─ Simple API, few dependencies? → net/http (stdlib)
│  ├─ Go 1.22+? → Use new ServeMux pattern routing
│  └─ Go < 1.22? → Consider Chi for better routing
│
├─ Need stdlib compatibility + better ergonomics? → Chi
│  └─ Great for: Middleware chains, route grouping
│
├─ Maximum performance priority? → Gin
│  └─ Great for: JSON APIs, high throughput services
│
├─ Enterprise app with OpenAPI? → Echo
│  └─ Great for: Type safety, comprehensive middleware
│
└─ Team knows Express.js + need WebSockets? → Fiber
   └─ Note: Uses fasthttp, not stdlib-compatible
```

## Common Pitfalls

**Pitfall 1: Not Closing Response Bodies**
```go
// Bad: Memory leak
resp, _ := http.Get(url)
body, _ := io.ReadAll(resp.Body) // Never closed!

// Good: Always defer close
resp, err := http.Get(url)
if err != nil {
    return err
}
defer resp.Body.Close()
body, err := io.ReadAll(resp.Body)
```

**Pitfall 2: Not Using Context for Timeouts**
```go
// Bad: No timeout control
resp, _ := http.Get(url)

// Good: Use context with timeout
ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
defer cancel()

req, _ := http.NewRequestWithContext(ctx, "GET", url, nil)
resp, err := client.Do(req)
```

**Pitfall 3: Ignoring HTTP Status Codes**
```go
// Bad: Not checking status
resp, _ := http.Get(url)
defer resp.Body.Close()
json.NewDecoder(resp.Body).Decode(&result)

// Good: Always check status
resp, err := http.Get(url)
if err != nil {
    return err
}
defer resp.Body.Close()

if resp.StatusCode != http.StatusOK {
    return fmt.Errorf("unexpected status: %d", resp.StatusCode)
}
```

**Pitfall 4: Not Reusing HTTP Clients**
```go
// Bad: Creates new client per request (no connection pooling)
func makeRequest() {
    client := &http.Client{}
    resp, _ := client.Get(url)
}

// Good: Reuse client for connection pooling
var httpClient = &http.Client{
    Timeout: 30 * time.Second,
}

func makeRequest() {
    resp, _ := httpClient.Get(url)
}
```

## Related Skills

- **golang-testing-strategies**: Testing HTTP handlers and middleware
- **golang-database-patterns**: Integrating databases with HTTP APIs
- **toolchains-typescript-frameworks-nodejs-backend**: Comparison with Node.js patterns

## References

- [Go net/http Documentation](https://pkg.go.dev/net/http)
- [Chi Framework](https://go-chi.io/)
- [Gin Framework](https://gin-gonic.com/)
- [Echo Framework](https://echo.labstack.com/)
- [Fiber Framework](https://gofiber.io/)
- [Go HTTP Best Practices](https://golang.org/doc/effective_go#web_server)
