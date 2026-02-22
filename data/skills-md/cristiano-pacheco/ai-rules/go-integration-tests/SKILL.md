---
name: go-integration-tests
description: Generate comprehensive Go integration tests using testify suite patterns with real database and infrastructure dependencies. Use when creating or updating integration test files, testing use cases against real databases, verifying end-to-end flows, or when asked to add integration test coverage for Go code.
---

# Go Integration Tests

Generate comprehensive Go integration tests using testify suite patterns with real database and infrastructure dependencies.

## Planning Phase

Before writing tests, identify:

1. **Test Location**: Tests go in `test/integration/` mirroring the source path from `internal/`
   - Example: `internal/modules/identity/usecase/user/user_register_usecase.go` → `test/integration/modules/identity/usecase/user/user_register_usecase_test.go`
2. **Dependencies**: Identify which real dependencies (database, redis) vs mocked dependencies (email, external APIs)
3. **Test Cases**: Define scenarios covering happy paths, edge cases, and error conditions
4. **Naming**: Number each test case clearly (e.g., `TestExecute_ValidInput_ReturnsUser`, `TestExecute_DuplicateEmail_ReturnsError`)

Show the code without explanations during planning.

## Implementation Patterns

### Pattern: Integration Test Suite

Use `suite.Suite` from testify with itestkit for containerized infrastructure.

**Key Rules:**
- Create suite struct with `sut` (System Under Test), `kit` (ITestKit), and `db` fields
- Implement `SetupSuite` to start containers and run migrations (runs once)
- Implement `TearDownSuite` to stop containers (runs once)
- Implement `SetupTest` to truncate tables and initialize sut (runs before each test)
- Use `//go:build integration` build tag at the top of the file
- Always use `_test` suffix for package name
- Use `suite` methods for assertions (e.g., `suite.Equal(v, 10)`)
- Use `suite.Require()` for error assertions (e.g., `suite.Require().ErrorIs`, `suite.Require().Error`)
- Never use `.AssertExpectations(s.T())`

**Example:**

```go
//go:build integration

package user_test

import (
	"context"
	"testing"

	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/suite"

	"github.com/cristiano-pacheco/bricks/pkg/itestkit"
	"github.com/cristiano-pacheco/bricks/pkg/validator"
	"github.com/cristiano-pacheco/pingo/internal/modules/identity/repository"
	"github.com/cristiano-pacheco/pingo/internal/modules/identity/usecase/user"
	"github.com/cristiano-pacheco/pingo/internal/shared/config"
	"github.com/cristiano-pacheco/pingo/internal/shared/database"
	"github.com/cristiano-pacheco/pingo/test/mocks"
)

func TestMain(m *testing.M) {
	itestkit.TestMain(m)
}

type UserRegisterUseCaseTestSuite struct {
	suite.Suite
	kit            *itestkit.ITestKit
	db             *database.PingoDB
	sut            *user.UserRegisterUseCase
	emailSender    *mocks.MockEmailSender
	cfg            config.Config
}

func TestUserRegisterUseCaseSuite(t *testing.T) {
	suite.Run(t, new(UserRegisterUseCaseTestSuite))
}

func (s *UserRegisterUseCaseTestSuite) SetupSuite() {
	s.kit = itestkit.New(itestkit.Config{
		PostgresImage:  "postgres:16-alpine",
		RedisImage:     "redis:7-alpine",
		MigrationsPath: "file://migrations",
		Database:       "pingo_test",
		User:           "pingo_test",
		Password:       "pingo_test",
	})

	err := s.kit.StartPostgres()
	s.Require().NoError(err)

	err = s.kit.RunMigrations()
	s.Require().NoError(err)

	s.db = &database.PingoDB{DB: s.kit.DB()}
}

func (s *UserRegisterUseCaseTestSuite) TearDownSuite() {
	if s.kit != nil {
		s.kit.StopPostgres()
	}
}

func (s *UserRegisterUseCaseTestSuite) SetupTest() {
	s.kit.TruncateTables(s.T())

	s.emailSender = mocks.NewMockEmailSender(s.T())
	s.cfg = s.createTestConfig()
	s.sut = s.createTestUseCase()
}

func (s *UserRegisterUseCaseTestSuite) createTestConfig() config.Config {
	return config.Config{
		App: config.AppConfig{
			BaseURL: "http://test.example.com",
		},
	}
}

func (s *UserRegisterUseCaseTestSuite) createTestUseCase() *user.UserRegisterUseCase {
	log := new(mocks.MockLogger)

	v, err := validator.New()
	s.Require().NoError(err)

	userRepo := repository.NewUserRepository(s.db)

	return user.NewUserRegisterUseCase(
		userRepo,
		s.emailSender,
		v,
		s.cfg,
		log,
	)
}

func (s *UserRegisterUseCaseTestSuite) TestExecute_ValidInput_ReturnsUser() {
	// Arrange
	ctx := context.Background()
	input := user.UserRegisterInput{
		Email:     "test@example.com",
		Password:  "Password123!",
		FirstName: "John",
		LastName:  "Doe",
	}

	// Act
	output, err := s.sut.Execute(ctx, input)

	// Assert
	s.Require().NoError(err)
	s.NotZero(output.ID)
	s.Equal(input.Email, output.Email)

	var savedUser model.UserModel
	err = s.db.DB.Where("id = ?", output.ID).First(&savedUser).Error
	s.Require().NoError(err)
	s.Equal(input.Email, savedUser.Email)
}

func (s *UserRegisterUseCaseTestSuite) TestExecute_DuplicateEmail_ReturnsError() {
	// Arrange
	ctx := context.Background()
	input := user.UserRegisterInput{
		Email:     "test@example.com",
		Password:  "Password123!",
		FirstName: "John",
		LastName:  "Doe",
	}

	// Act - First registration
	_, err := s.sut.Execute(ctx, input)
	s.Require().NoError(err)

	// Act - Second registration with same email
	_, err = s.sut.Execute(ctx, input)

	// Assert
	s.Require().Error(err)
	s.ErrorIs(err, errs.ErrDuplicateEmail)
}
```

### Mock Rules for Integration Tests

- Mock external services (email, SMS, external APIs) that cannot run locally
- Use real database connections (via itestkit)
- Use real Redis connections when testing cache (via itestkit)
- Mock metrics and logger dependencies with `.Maybe()` to allow optional calls
- Always pass `mock.Anything` for context parameters

**Example with Mocks:**

```go
func (s *UserRegisterUseCaseTestSuite) SetupTest() {
	s.kit.TruncateTables(s.T())

	s.emailSender = mocks.NewMockEmailSender(s.T())
	s.tokenGenerator = mocks.NewMockTokenGenerator(s.T())

	// Setup optional mock expectations
	s.emailSender.On("Send", mock.Anything, mock.Anything, mock.Anything, mock.Anything).
		Return(nil).Maybe()
	s.tokenGenerator.On("GenerateToken").Return("test-token", nil).Maybe()

	s.sut = s.createTestUseCase()
}
```

## Test Structure Requirements

### (CRITICAL) Arrange-Act-Assert Pattern

Every test must follow AAA pattern with explicit comments:

```go
// Arrange
// Act
// Assert
```

### Code Style

- Never use inline struct construction; always create variable first
- Maximum 120 characters per line
- Test names must clearly indicate what is being tested
- Add comments for complex test setups or assertions

### Test Coverage

- Include happy path scenarios
- Include edge cases
- Include error handling
- Verify database state after operations
- Test data persistence and retrieval

## Test File Location

Integration tests mirror the source structure under `test/integration/`:

| Source File | Integration Test File |
|-------------|----------------------|
| `internal/modules/identity/usecase/user/user_register_usecase.go` | `test/integration/modules/identity/usecase/user/user_register_usecase_test.go` |
| `internal/modules/monitor/usecase/metric_usecase.go` | `test/integration/modules/monitor/usecase/metric_usecase_test.go` |

## Running Integration Tests

```bash
# Run all integration tests
make test-integration
```

## Completion

When tests are complete, respond with: **Integration Tests Done, Oh Yeah!**
