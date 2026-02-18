---
name: go-unit-tests
description: Generate comprehensive Go unit tests following testify patterns and best practices. Use when creating or updating Go test files, writing test suites for structs with dependencies, testing standalone functions, working with mocks, or when asked to add test coverage for Go code.
---

# Go Unit Tests

Generate comprehensive Go unit tests following testify patterns and the Arrange-Act-Assert methodology.

## Planning Phase

Before writing tests, identify:

1. **Test Structure**: Determine if test suite (for structs with dependencies) or individual test functions (for standalone functions) should be used
2. **Dependencies**: Identify dependencies or side effects requiring mocks or stubs
3. **Test Cases**: Define scenarios covering happy paths, edge cases, and error conditions
4. **Naming**: Number each test case clearly (e.g., `TestFunction_ValidInput_ReturnsExpectedResult`, `TestFunction_EmptyInput_ReturnsError`)

Show the code without explanations during planning.

## Implementation Patterns

### Pattern 1: Test Suites for Structs with Dependencies

Use `suite.Suite` from testify for structs with dependencies.

**Key Rules:**
- Create suite struct with `sut` (System Under Test) field
- Implement `SetupTest` method to initialize sut and dependencies
- Use constructor (typically `NewTypeName`) to create instances
- Always use `_test` suffix for package name
- Use `suite` methods for assertions (e.g., `suite.Equal(v, 10)`)
- Use `suite.Require()` for error assertions (e.g., `suite.Require().ErrorIs`, `suite.Require().Error`)
- Never use `.AssertExpectations(s.T())`

**Example:**

```go
package mypackage_test

import (
	"testing"

	"github.com/stretchr/testify/suite"
)

type MyStructTestSuite struct {
	suite.Suite
	sut *mypackage.MyStruct
}

func (s *MyStructTestSuite) SetupTest() {
	// Initialize sut and dependencies
	s.sut = mypackage.New()
}

func TestMyStructSuite(t *testing.T) {
	suite.Run(t, new(MyStructTestSuite))
}

func (s *MyStructTestSuite) TestSomeMethod() {
	// Arrange
	input := "test input"
	expected := "expected output"

	// Act
	result := s.sut.SomeMethod(input)

	// Assert
	s.Equal(expected, result)
}

func (s *MyStructTestSuite) TestSomeMethod_WithError() {
	// Arrange
	invalidInput := ""

	// Act
	result, err := s.sut.SomeMethodWithError(invalidInput)

	// Assert
	s.Require().Error(err)
	s.Empty(result)
}
```

**With Mocks:**

```go
package mypackage_test

import (
	"context"
	"testing"

	"github.com/stretchr/testify/mock"
	"github.com/stretchr/testify/suite"

	"github.com/example/project/test/mocks"
)

type UserServiceTestSuite struct {
	suite.Suite
	sut              *mypackage.UserService
	userRepoMock     *mocks.MockUserRepository
	tokenServiceMock *mocks.MockTokenService
}

func (s *UserServiceTestSuite) SetupTest() {
	// Initialize mocks
	s.userRepoMock = mocks.NewMockUserRepository(s.T())
	s.tokenServiceMock = mocks.NewMockTokenService(s.T())

	// Initialize sut with mocked dependencies
	s.sut = mypackage.NewUserService(
		s.userRepoMock,
		s.tokenServiceMock,
	)
}

func TestUserServiceSuite(t *testing.T) {
	suite.Run(t, new(UserServiceTestSuite))
}

func (s *UserServiceTestSuite) TestCreateUser_ValidInput_CreatesUser() {
	// Arrange
	ctx := context.Background()
	user := &mypackage.User{
		Email: "test@example.com",
		Name:  "Test User",
	}

	s.userRepoMock.On("Create", mock.Anything, user).Return(nil)

	// Act
	err := s.sut.CreateUser(ctx, user)

	// Assert
	s.Require().NoError(err)
}

func (s *UserServiceTestSuite) TestCreateUser_RepositoryError_ReturnsError() {
	// Arrange
	ctx := context.Background()
	user := &mypackage.User{
		Email: "test@example.com",
		Name:  "Test User",
	}
	expectedError := errors.New("repository error")

	s.userRepoMock.On("Create", mock.Anything, user).Return(expectedError)

	// Act
	err := s.sut.CreateUser(ctx, user)

	// Assert
	s.Require().ErrorIs(err, expectedError)
}

func (s *UserServiceTestSuite) TestGenerateToken_ValidUser_ReturnsToken() {
	// Arrange
	ctx := context.Background()
	userID := "user-123"
	expectedToken := "token-abc"

	s.tokenServiceMock.On(
		"Generate",
		mock.Anything,
		userID,
	).Return(expectedToken, nil)

	// Act
	token, err := s.sut.GenerateToken(ctx, userID)

	// Assert
	s.Require().NoError(err)
	s.Equal(expectedToken, token)
}
```

**Mock Rules:**
- Always pass `mock.Anything` for context parameters
- Mock naming follows pattern `MockType` (e.g., `MockUserRepository`, `MockTokenService`)
- Import mocks with aliases: `user_repository_mocks "github.com/project/internal/domain/repository/mocks"`

### Pattern 2: Tests for Standalone Functions

Use individual test functions with subtests for functions without instances.

**Key Rules:**
- Create test functions using `func TestXxx(t *testing.T)`
- Use `t.Run` for subtests covering different scenarios
- Use `require` for error assertions (e.g., `require.ErrorIs`, `require.Error`)

**Example:**

```go
package mypackage_test

import (
	"testing"

	"github.com/stretchr/testify/require"
)

func TestSomeFunction(t *testing.T) {
	t.Run("valid input returns expected result", func(t *testing.T) {
		// Arrange
		input := "test input"
		expected := "expected output"

		// Act
		result := SomeFunction(input)

		// Assert
		require.Equal(t, expected, result)
	})

	t.Run("empty input returns error", func(t *testing.T) {
		// Arrange
		input := ""

		// Act
		result, err := SomeFunctionWithError(input)

		// Assert
		require.Error(t, err)
		require.Empty(t, result)
	})

	t.Run("nil input returns error", func(t *testing.T) {
		// Arrange
		var input *string

		// Act
		result, err := SomeFunctionWithPointer(input)

		// Assert
		require.ErrorIs(t, err, ErrNilInput)
		require.Empty(t, result)
	})
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
- Aim for minimum test scenarios possible while maintaining at least 80% coverage

## Completion

When tests are complete, respond with: **Tests Done, Oh Yeah!**
