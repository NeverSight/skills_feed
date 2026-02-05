---
name: backend-go
description: Go (Golang) backend development conventions. Use when working on Go projects.
---

# Backend Go Conventions

This skill provides specific conventions for Go backend development.

## When to Use
- Use this skill when working on Go projects
- Use this skill when creating new handlers, services, or repositories
- This skill builds upon `project-standards` skill

## Instructions

### 1. Project Layout (Standard Go Layout)

```
project/
├── cmd/
│   └── api/
│       └── main.go           # Entry point
├── internal/
│   ├── handler/              # HTTP handlers (Controllers)
│   ├── service/              # Business logic
│   ├── repository/           # Database access
│   ├── model/                # Domain models
│   └── dto/                  # Request/Response objects
├── pkg/                      # Shared libraries
├── api/                      # OpenAPI/Swagger specs
├── config/                   # Configuration
└── go.mod
```

### 2. Architecture (Clean/Hexagonal)

- **Handler (Controller):** Receives requests, validates, calls Service.
- **Service (Usecase):** Contains Business Logic.
- **Repository:** Interacts with the Database.

**Important:** Interfaces should be defined where they are USED (Consumer), not where they are provided (Producer).

```go
// In service package (consumer defines interface)
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*model.User, error)
    Create(ctx context.Context, user *model.User) error
}

type UserService struct {
    repo UserRepository
}

func NewUserService(repo UserRepository) *UserService {
    return &UserService{repo: repo}
}
```

### 3. Error Handling

#### No Panic
Only panic during app setup failure (e.g., db disconnect).

```go
// Bad - panicking in business logic
func GetUser(id string) User {
    user, err := repo.Find(id)
    if err != nil {
        panic(err) // Never do this!
    }
    return user
}

// Good - return errors
func GetUser(id string) (User, error) {
    user, err := repo.Find(id)
    if err != nil {
        return User{}, fmt.Errorf("get user %s: %w", id, err)
    }
    return user, nil
}
```

#### Wrap Errors
Use `fmt.Errorf` with `%w` to preserve context.

```go
if err != nil {
    return fmt.Errorf("create user failed: %w", err)
}
```

### 4. Naming Convention

- **Package:** Short, lowercase, no underscores (e.g., `user`, `auth`).
- **Interface:** Ends with `er` (e.g., `Reader`, `Writer`, `UserRepository`).
- **Variable:** camelCase, acronyms all uppercase (`userID`, `httpClient`).
- **Exported:** PascalCase for exported, camelCase for unexported.

```go
// Good
package user

type Repository interface {
    FindByID(ctx context.Context, id string) (*User, error)
}

var defaultTimeout = 30 * time.Second // unexported
var DefaultClient = &http.Client{}     // exported
```

### 5. Context Handling

Always pass context as the first parameter.

```go
func (s *UserService) GetUser(ctx context.Context, id string) (*User, error) {
    // Check context cancellation
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    default:
    }
    
    return s.repo.FindByID(ctx, id)
}
```

### 6. HTTP Handler Example

```go
func (h *UserHandler) GetUser(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")
    
    user, err := h.service.GetUser(r.Context(), id)
    if err != nil {
        if errors.Is(err, ErrNotFound) {
            h.respondError(w, http.StatusNotFound, "user not found")
            return
        }
        h.respondError(w, http.StatusInternalServerError, "internal error")
        return
    }
    
    h.respondJSON(w, http.StatusOK, Response{
        Success: true,
        Data:    user,
    })
}
```

### 7. Testing

Use table-driven tests.

```go
func TestUserService_GetUser(t *testing.T) {
    tests := []struct {
        name    string
        id      string
        want    *User
        wantErr bool
    }{
        {
            name: "valid user",
            id:   "123",
            want: &User{ID: "123", Email: "test@example.com"},
        },
        {
            name:    "not found",
            id:      "999",
            wantErr: true,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Test implementation
        })
    }
}
```

### 8. Dependencies

- **Framework:** Gin or Echo
- **ORM:** GORM or SQLC
- **Config:** Viper
- **Logger:** Zap or Zerolog
