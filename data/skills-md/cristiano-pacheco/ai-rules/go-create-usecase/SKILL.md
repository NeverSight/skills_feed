---
name: go-create-usecase
description: Generate Go use cases for modular architecture with Fx dependency injection, ports-based dependencies, OpenTelemetry tracing, input validation, and use-case metrics. Use when implementing business actions in internal/modules/<module>/usecase/ such as create, update, list, delete, status transitions, uploads, notifications, or any domain operation that orchestrates repositories/services.
---

# Go Create UseCase

Generate a use case that depends on ports (interfaces), not concrete implementations.

## Create the file

Create one file per operation in:
`internal/modules/<module>/usecase/<operation>_usecase.go`

Use:
- package: `usecase`
- struct name: `<Operation>UseCase`
- metric name: `<operation>` (lowercase snake case)
- span name: `"<Operation>UseCase.Execute"`

## Naming (CRITICAL)

Apply consistent naming for every use case.

Rules:
- file: `<operation>_usecase.go`
- input DTO: `<Operation>Input`
- output DTO: `<Operation>Output`
- use case struct: `<Operation>UseCase`
- constructor: `New<Operation>UseCase`
- metric: `<operation>` (snake case)
- span: `"<Operation>UseCase.Execute"`

Example (`contact_create`):
- file: `contact_create_usecase.go`
- input: `ContactCreateInput`
- output: `ContactCreateOutput`
- struct: `ContactCreateUseCase`
- constructor: `NewContactCreateUseCase`
- metric: `contact_create`
- span: `"ContactCreateUseCase.Execute"`

Example (`contact_list`, no input):
- file: `contact_list_usecase.go`
- output: `ContactListOutput`
- struct: `ContactListUseCase`
- constructor: `NewContactListUseCase`
- metric: `contact_list`
- span: `"ContactListUseCase.Execute"`

## Follow the structure CRITICAL

Implement this order in the file:
1. Input struct (skip when no parameters are needed)
2. Output struct
3. Use case struct with dependencies
4. Constructor `New<Operation>UseCase`
5. Public `Execute` method (metrics wrapper)
6. Private `execute` method (business logic + tracing)
7. Input and Output must not contain json tags, only validation tags when needed for input.

## Use this template

```go
package usecase

import (
	"context"
	"time"

	"github.com/cristiano-pacheco/bricks/pkg/logger"
	"github.com/cristiano-pacheco/bricks/pkg/otel/trace"
	"github.com/cristiano-pacheco/bricks/pkg/validator"
	"github.com/cristiano-pacheco/pingo/internal/modules/<module>/ports"
	"github.com/cristiano-pacheco/pingo/internal/shared/metrics"
)

type <Operation>Input struct {
	Field string `validate:"required,max=255"`
}

type <Operation>Output struct {
	Result string
}

type <Operation>UseCase struct {
	repo           ports.<Entity>Repository
	validator      validator.Validator
	logger         logger.Logger
	useCaseMetrics metrics.UseCaseMetrics
}

func New<Operation>UseCase(
	repo ports.<Entity>Repository,
	validator validator.Validator,
	logger logger.Logger,
	useCaseMetrics metrics.UseCaseMetrics,
) *<Operation>UseCase {
	return &<Operation>UseCase{
		repo:           repo,
		validator:      validator,
		logger:         logger,
		useCaseMetrics: useCaseMetrics,
	}
}

func (uc *<Operation>UseCase) Execute(ctx context.Context, input <Operation>Input) (<Operation>Output, error) {
	start := time.Now()
	output, err := uc.execute(ctx, input)

	uc.useCaseMetrics.ObserveDuration("<operation>", time.Since(start))
	if err != nil {
		uc.useCaseMetrics.IncError("<operation>")
		return output, err
	}

	uc.useCaseMetrics.IncSuccess("<operation>")
	return output, nil
}

func (uc *<Operation>UseCase) execute(ctx context.Context, input <Operation>Input) (<Operation>Output, error) {
	ctx, span := trace.Span(ctx, "<Operation>UseCase.Execute")
	defer span.End()

	output := <Operation>Output{}

	if err := uc.validator.Validate(input); err != nil {
		return output, err
	}

	// Add business orchestration here
	// - read/write via repositories
	// - call domain services
	// - map model to output DTO

	return output, nil
}
```

## Apply variants

### No-input use case

When no parameters are needed, remove input struct and use:

```go
func (uc *ContactListUseCase) Execute(ctx context.Context) (ContactListOutput, error)
func (uc *ContactListUseCase) execute(ctx context.Context) (ContactListOutput, error)
```

### No-validation use case

When validation is not required, remove `validator.Validator` from dependencies and skip `uc.validator.Validate(...)`.

### Multi-dependency orchestration

Inject multiple ports as interfaces (repositories, caches, services) in the use case struct and constructor.

## Apply common patterns

### Check existing record before create

```go
record, err := uc.repo.FindByX(ctx, input.Field)
if err != nil && !errors.Is(err, shared_errs.ErrRecordNotFound) {
	uc.logger.Error("error finding record", logger.Error(err))
	return output, err
}
if record.ID != 0 {
	return output, errs.ErrAlreadyExists
}
```

### Convert enum from input

```go
enumVal, err := enum.NewTypeEnum(input.Type)
if err != nil {
	return output, err
}
model.Type = enumVal.String()
```

### Map list response

```go
items, err := uc.repo.FindAll(ctx)
if err != nil {
	uc.logger.Error("error listing records", logger.Error(err))
	return output, err
}

output.Items = make([]ItemOutput, len(items))
for i, item := range items {
	output.Items[i] = ItemOutput{ID: item.ID, Name: item.Name}
}
```

## Wire with Fx

Add provider wiring in `internal/modules/<module>/fx.go`:

```go
fx.Provide(
	usecase.New<Operation>UseCase,
)
```

If another layer depends on an interface abstraction, annotate accordingly in module wiring.

## Enforce rules

1. Depend only on `ports.*` interfaces in use cases
2. Keep orchestration in use case; keep persistence in repositories
3. Wrap public `Execute` with metrics: `ObserveDuration`, `IncError`, `IncSuccess`
4. Start a span in private `execute` and always `defer span.End()`
5. Keep naming consistent across file, struct, metric, and span
6. Return typed output DTOs; do not leak persistence models directly

## Final checklist

1. Create `internal/modules/<module>/usecase/<operation>_usecase.go`
2. Add input/output DTOs for the operation
3. Inject logger, metrics, and required ports
4. Implement public metrics wrapper and private traced logic
5. Wire provider in `internal/modules/<module>/fx.go`
6. Create the unit tests using the go-unit-tests skill
7. Run `make test`
8. Run `make lint`
9. Run `make nilaway`
