---
name: go-create-chi-router
description: Generate Chi router implementations following GO modular architechture conventions (Chi router from bricks package, Fx DI with chi.Route interface, REST endpoints). Use when creating HTTP route registration for resources in internal/modules/<module>/http/chi/router/ including REST routes (GET, POST, PUT, DELETE) for CRUD operations, custom endpoints, versioned APIs, and route groups.
---

# Go Create Chi Router

Generate Chi router implementations for Go backend HTTP transport layer.

## Router File Structure

**Location**: `internal/modules/<module>/http/chi/router/<resource>_router.go`

## Router Implementation

```go
package router

import (
	"github.com/cristiano-pacheco/bricks/pkg/http/server/chi"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/http/chi/handler"
)

type ResourceRouter struct {
	handler *handler.ResourceHandler
}

func NewResourceRouter(h *handler.ResourceHandler) *ResourceRouter {
	return &ResourceRouter{handler: h}
}

func (r *ResourceRouter) Setup(server *chi.Server) {
	router := server.Router()
	router.Get("/api/v1/resources", r.handler.ListResources)
	router.Get("/api/v1/resources/:id", r.handler.GetResource)
	router.Post("/api/v1/resources", r.handler.CreateResource)
	router.Put("/api/v1/resources/:id", r.handler.UpdateResource)
	router.Delete("/api/v1/resources/:id", r.handler.DeleteResource)
}
```

## Router Patterns

### Basic CRUD Routes

```go
func (r *ResourceRouter) Setup(server *chi.Server) {
	router := server.Router()
	router.Get("/api/v1/resources", r.handler.ListResources)
	router.Get("/api/v1/resources/:id", r.handler.GetResource)
	router.Post("/api/v1/resources", r.handler.CreateResource)
	router.Put("/api/v1/resources/:id", r.handler.UpdateResource)
	router.Delete("/api/v1/resources/:id", r.handler.DeleteResource)
}
```

### Custom Endpoints

```go
func (r *ResourceRouter) Setup(server *chi.Server) {
	router := server.Router()
	
	// Standard CRUD
	router.Get("/api/v1/resources", r.handler.ListResources)
	router.Post("/api/v1/resources", r.handler.CreateResource)
	
	// Custom actions
	router.Post("/api/v1/resources/:id/activate", r.handler.ActivateResource)
	router.Post("/api/v1/resources/:id/deactivate", r.handler.DeactivateResource)
	
	// Nested resources
	router.Get("/api/v1/resources/:id/items", r.handler.ListResourceItems)
	router.Post("/api/v1/resources/:id/items", r.handler.AddResourceItem)
}
```

### Route Groups (with middleware)

```go
func (r *ResourceRouter) Setup(server *chi.Server) {
	router := server.Router()
	
	// Public routes
	router.Get("/api/v1/resources", r.handler.ListResources)
	router.Get("/api/v1/resources/:id", r.handler.GetResource)
	
	// Protected routes (if auth middleware needed)
	router.Group(func(r chi.Router) {
		// r.Use(middleware.Auth) // Example if auth middleware exists
		r.Post("/api/v1/resources", r.handler.CreateResource)
		r.Put("/api/v1/resources/:id", r.handler.UpdateResource)
		r.Delete("/api/v1/resources/:id", r.handler.DeleteResource)
	})
}
```

### Multiple Handlers

```go
type ResourceRouter struct {
	resourceHandler *handler.ResourceHandler
	itemHandler     *handler.ItemHandler
}

func NewResourceRouter(
	resourceHandler *handler.ResourceHandler,
	itemHandler *handler.ItemHandler,
) *ResourceRouter {
	return &ResourceRouter{
		resourceHandler: resourceHandler,
		itemHandler:     itemHandler,
	}
}

func (r *ResourceRouter) Setup(server *chi.Server) {
	router := server.Router()
	
	// Resource routes
	router.Get("/api/v1/resources", r.resourceHandler.ListResources)
	router.Post("/api/v1/resources", r.resourceHandler.CreateResource)
	
	// Item routes (related resource)
	router.Get("/api/v1/items", r.itemHandler.ListItems)
	router.Post("/api/v1/items", r.itemHandler.CreateItem)
}
```

## Fx Wiring

**Add to `internal/modules/<module>/fx.go`**:

```go
fx.Provide(
	fx.Annotate(
		router.NewResourceRouter,
		fx.As(new(chi.Route)),
		fx.ResultTags(`group:"routes"`),
	),
),
```

**Multiple routers in same module**:

```go
fx.Provide(
	fx.Annotate(
		router.NewResourceRouter,
		fx.As(new(chi.Route)),
		fx.ResultTags(`group:"routes"`),
	),
	fx.Annotate(
		router.NewItemRouter,
		fx.As(new(chi.Route)),
		fx.ResultTags(`group:"routes"`),
	),
),
```

## HTTP Methods & Semantics

Follow REST conventions:
- `GET`: Retrieve resources (list or single)
- `POST`: Create new resources
- `PUT`: Update existing resources (full update)
- `PATCH`: Partial update (if needed)
- `DELETE`: Remove resources

## URL Path Conventions

- **Version prefix**: `/api/v1/`
- **Resource names**: Plural nouns (`/resources`, `/contacts`, `/monitors`)
- **Resource ID**: Use `:id` param (`/resources/:id`)
- **Nested resources**: `/resources/:id/items`
- **Actions**: Use verbs for non-CRUD (`/resources/:id/activate`)

## Critical Rules

1. **Struct**: Holds handler(s) only
2. **Constructor**: MUST return pointer `*ResourceRouter`
3. **Setup method**: MUST be named `Setup` and take `*chi.Server`
4. **Router access**: Get router via `server.Router()`
5. **Route format**: Always start with `/api/v1/` prefix
6. **Resource naming**: Use plural nouns for resources
7. **Handler naming**: Match handler method names to actions (e.g., `ListResources`, `CreateResource`)
8. **Fx wiring**: MUST use `fx.As(new(chi.Route))` and `fx.ResultTags(\`group:"routes"\`)`
9. **No comments**: Do not add redundant comments above methods
10. **Imports**: Only import `bricks/pkg/http/server/chi` and handler package
11. **Dependencies**: Handlers are injected via constructor
12. **Validation**: Run `make lint` after generation

## Router Naming

- **Struct**: `<Resource>Router` (PascalCase)
- **Constructor**: `New<Resource>Router`
- **File**: `<resource>_router.go` (snake_case)

## Workflow

1. Create router file in `internal/modules/<module>/http/chi/router/<resource>_router.go`
2. Define struct with handler dependency
3. Implement constructor
4. Implement `Setup(server *chi.Server)` method with routes
5. Add Fx wiring to module's `fx.go`
6. Run `make lint` to verify

## Common Route Patterns

### List with filters
```go
router.Get("/api/v1/resources", r.handler.ListResources) // query params in handler
```

### Nested resource access
```go
router.Get("/api/v1/resources/:resourceId/items/:itemId", r.handler.GetResourceItem)
```

### Bulk operations
```go
router.Post("/api/v1/resources/bulk", r.handler.BulkCreateResources)
router.Delete("/api/v1/resources/bulk", r.handler.BulkDeleteResources)
```
