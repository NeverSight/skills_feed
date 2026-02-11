---
name: clean-architecture-golang
description: Expert implementation guide for custom Clean Architecture pattern in Golang projects. Use when implementing features with domain-driven design, creating API endpoints, or working with this specific 4-layer architecture (Domain, Application, Integration, Infrastructure). NOT Uncle Bob's standard Clean Architecture - this is a specialized adaptation with strict dependency rules and specific conventions.
---

# Custom Clean Architecture Implementation Guide

Expert guidance for implementing features using this project's custom Clean Architecture pattern with Golang. This is NOT Uncle Bob's standard Clean Architecture - it's a specialized adaptation.

## Architecture Overview

Four layers with strict dependency rules:

```
Integration → Application → Domain ← Infrastructure
```

**Dependency Rule**: Inner layers NEVER depend on outer layers.

## 🚨 Critical Rules

### MUST DO
- **START with BDD feature file** - Never skip test-first development
- **Integration adapters MUST implement usecase interfaces** - Enable type casting
- **Use context.Context as first parameter** - Always
- **Convert at boundaries** - DTO↔Entity↔Model
- **Follow error code format** - PREFIX-XXYYYY
- **Type cast repositories to usecases** - In dependency injection

### NEVER DO
- **Skip BDD test creation** - Tests come first
- **Create adapters without usecase interfaces** - Will break dependency injection
- **Put business logic in controllers/repositories** - Only in services
- **Use DTOs in domain/application** - Only in integration layer
- **Access database from services** - Only through usecases
- **Create circular dependencies** - Dependencies flow inward only

## Implementation Workflow

### Step 1: Create BDD Test (MANDATORY)

Start here ALWAYS. Location: `/test/integration/features/`

```gherkin
Feature: Create entity functionality
  Scenario: Create entity success
    When I call "POST" "/v1/entities" with payload
    Then status should be 201
    And db should contain entity
```

### Step 2: Domain Layer

1. **Entity** (`/internal/domain/entity/`)
   - Simple structs, NO logic
   - Audit fields (CreatedAt, UpdatedAt)

2. **Errors** (`/internal/domain/error/`)
   - Format: `PREFIX-XXYYYY`
   - One error per file

3. **Enums** (`/internal/domain/enums/`)
   - String types
   - SCREAMING_SNAKE_CASE values

### Step 3: Application Layer

1. **Adapter Interface** (`/internal/application/adapter/`)
   - Service contracts
   - Use domain entities

2. **UseCase Interfaces** (`/internal/application/usecase/`)
   - Atomic operations
   - FindX, SaveX, UpdateX, DeleteX

3. **Service Implementation** (`/internal/application/service/`)
   - Business logic HERE
   - Orchestrate usecases

### Step 4: Integration Layer

1. **Adapter Interfaces** (`/internal/integration/adapter/`)
   ```go
   type Repository interface {
       usecase.Find    // MUST embed
       usecase.Save    // MUST embed
   }
   ```

2. **DTOs** (`/internal/integration/entrypoint/dto/`)
   - Request/Response structs
   - ToEntity() methods
   - Validation tags

3. **Controller** (`/internal/integration/entrypoint/controller/`)
   - Handle HTTP
   - DTO↔Entity conversion

4. **Model** (`/internal/integration/persistence/model/`)
   - GORM annotations
   - ToEntity() methods

5. **Repository** (`/internal/integration/persistence/`)
   - Implements usecase interfaces
   - Entity↔Model conversion

### Step 5: Infrastructure Layer

1. **Dependency Injection** (`/internal/infra/dependency/injector.go`)
   ```go
   // Type cast repository to usecase
   usecase.Find(i.GetRepository())
   ```

2. **Router** (`/internal/infra/server/router/router.go`)
   - Add routes
   - Validation middleware

### Step 6: Run Tests

```bash
make test-integration
```

## Quick Patterns

### Integration Adapter Pattern (CRITICAL)

```go
// Application defines need
type FindProduct interface {
    FindById(ctx, id) (*entity, error)
}

// Integration MUST implement
type ProductRepository interface {
    usecase.FindProduct  // EMBED!
}

// Type cast in DI
usecase.FindProduct(repository)
```

### Error Codes

- `CLI-01409` = Client conflict (409)
- `USR-01404` = User not found (404)
- `PRD-02500` = Product server error (500)

### Conversion Flow

```
Request → DTO → Entity → Model → DB
Response ← DTO ← Entity ← Model ← DB
```

## Reference Documentation

Detailed guides in references/:
- [Layer Implementation](references/layer-implementation.md) - Complete layer examples
- [Critical Patterns](references/critical-patterns.md) - Must-know patterns
- [Implementation Workflow](references/implementation-workflow.md) - Step-by-step guide

## Templates

Ready-to-use templates in assets/:
- `entity-template.go` - Domain entity template
- `service-template.go` - Application service template
- `repository-template.go` - Repository template

## Implementation Checklist

Before starting any feature:

- [ ] BDD feature file exists
- [ ] Domain entity defined
- [ ] Domain errors created
- [ ] Application adapter interface defined
- [ ] Application usecases created
- [ ] Application service implemented
- [ ] Integration adapters created WITH usecase interfaces
- [ ] DTOs with ToEntity() methods
- [ ] Controller handling HTTP
- [ ] Model with ToEntity() method
- [ ] Repository implementing usecases
- [ ] Dependencies wired in injector
- [ ] Routes added to router
- [ ] Tests passing

## Common Mistakes to Avoid

1. **Forgetting usecase interfaces on adapters** - Breaks type casting
2. **Business logic in wrong layer** - Only in services
3. **Wrong dependency direction** - Check imports
4. **Missing BDD test** - Always start with test
5. **Wrong error code format** - Use PREFIX-XXYYYY
6. **Not converting at boundaries** - DTO↔Entity↔Model

## Example Implementations

Study these existing implementations:
- Client: `/internal/{domain,application,integration}/*/client*.go`
- User: `/internal/{domain,application,integration}/*/user*.go`
- Forest: `/internal/{domain,application,integration}/*/forest*.go`
