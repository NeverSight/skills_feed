---
name: golang-architect
description: Golang backend architecture expert. Use when designing Go services with Gin, implementing layered architecture, configuring sqlc with PostgreSQL/Supabase, or building API authentication.
---

# Golang Backend Architecture Expert

Expert assistant for Golang backend architecture with Gin Server, Layered Architecture, sqlc, PostgreSQL (Supabase), and API authentication.

## How It Works

1. Analyzes service requirements and existing codebase
2. Queries Gin documentation via Context7 (`/websites/gin-gonic_en`)
3. Applies layered architecture patterns (Handler → Service → Repository)
4. Provides implementation with proper error handling and testing

## Usage


### Initialize SQLC

```bash
bash /mnt/skills/user/golang-architect/scripts/sqlc-init.sh [project-dir] [db-engine]
```

**Arguments:**
- `project-dir` - Project directory (default: current directory)
- `db-engine` - Database engine: postgresql, mysql, sqlite3 (default: postgresql)

**Examples:**
```bash
bash /mnt/skills/user/golang-architect/scripts/sqlc-init.sh
bash /mnt/skills/user/golang-architect/scripts/sqlc-init.sh ./my-project postgresql
```

## Documentation Resources

**Context7 Library ID:** `/websites/gin-gonic_en` (117 snippets, Score: 90.8)

**Official Documentation:**
- Gin: `https://gin-gonic.com/en/docs/`
- sqlc: `https://docs.sqlc.dev/`
- Supabase: Use `mcp__supabase__*` tools
- go-symphony: `https://github.com/Tomlord1122/go-symphony`

## Layered Architecture Template

```
project/
├── cmd/
│   └── api/
│       └── main.go           # Entry point
├── internal/
│   ├── handler/              # HTTP handlers (Gin)
│   │   └── user_handler.go
│   ├── service/              # Business logic
│   │   └── user_service.go
│   ├── repository/           # Data access (sqlc)
│   │   └── user_repository.go
│   ├── middleware/           # Auth, logging, CORS
│   │   └── auth.go
│   └── dto/                  # Data Transfer Objects
│       └── user_dto.go
├── pkg/                      # Shared utilities
├── db/
│   ├── migrations/           # SQL migrations
│   └── queries/              # sqlc SQL files
├── sqlc.yaml
└── go.mod
```

## sqlc Configuration

```yaml
# sqlc.yaml
version: "2"
sql:
  - engine: "postgresql"
    queries: "db/queries/"
    schema: "db/migrations/"
    gen:
      go:
        package: "repository"
        out: "internal/repository"
        sql_package: "pgx/v5"
        emit_json_tags: true
        emit_interface: true
```

## Handler Pattern

```go
type UserHandler struct {
    service *service.UserService
}

func NewUserHandler(s *service.UserService) *UserHandler {
    return &UserHandler{service: s}
}

func (h *UserHandler) GetUser(c *gin.Context) {
    id := c.Param("id")
    user, err := h.service.GetUser(c.Request.Context(), id)
    if err != nil {
        c.JSON(http.StatusNotFound, gin.H{"error": err.Error()})
        return
    }
    c.JSON(http.StatusOK, user)
}
```

## Middleware Pattern

```go
func AuthMiddleware(jwtSecret string) gin.HandlerFunc {
    return func(c *gin.Context) {
        token := c.GetHeader("Authorization")
        if token == "" {
            c.AbortWithStatusJSON(401, gin.H{"error": "unauthorized"})
            return
        }
        // Validate token...
        c.Set("userID", claims.UserID)
        c.Next()
    }
}
```

## Error Handling

```go
// Custom error types
type AppError struct {
    Code    int    `json:"code"`
    Message string `json:"message"`
}

func (e *AppError) Error() string {
    return e.Message
}

// Error middleware
func ErrorHandler() gin.HandlerFunc {
    return func(c *gin.Context) {
        c.Next()
        if len(c.Errors) > 0 {
            err := c.Errors.Last().Err
            if appErr, ok := err.(*AppError); ok {
                c.JSON(appErr.Code, appErr)
                return
            }
            c.JSON(500, gin.H{"error": "internal server error"})
        }
    }
}
```

## Present Results to User

When providing Go backend solutions:
- Follow Go conventions (Effective Go, uber-go/guide)
- Use dependency injection for testability
- Provide complete error handling examples
- Include context propagation for cancellation
- Show corresponding tests when appropriate

## Troubleshooting

**"sqlc generate fails"**
- Verify PostgreSQL syntax in queries
- Check schema matches query expectations
- Run `sqlc vet` for detailed errors

**"Gin handler not receiving body"**
- Ensure `Content-Type: application/json` header
- Check if body was already read (bind only once)
- Use `ShouldBindJSON` instead of `BindJSON` for error control

**"Context cancelled"**
- Propagate context through all layers
- Check for long-running operations without timeout
