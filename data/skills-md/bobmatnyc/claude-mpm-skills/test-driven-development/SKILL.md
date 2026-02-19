---
name: test-driven-development
description: Comprehensive TDD patterns and practices for all programming languages, eliminating redundant testing guidance per agent.
license: Apache-2.0
compatibility: claude-code
metadata:
  updated_at: 2025-10-30T17:00:00Z
tags: [testing, tdd, best-practices, quality-assurance]
progressive_disclosure:
  entry_point:
    summary: "Comprehensive TDD patterns and practices for all programming languages, eliminating redundant testing guidance per agent."
    when_to_use: "When writing tests, implementing test-driven-development, or ensuring code quality."
    quick_start: "1. Review the core concepts below. 2. Apply patterns to your use case. 3. Follow best practices for implementation."
  references:
    - anti-patterns.md
    - examples.md
    - integration.md
    - philosophy.md
    - workflow.md
---
# Test-Driven Development (TDD)

Comprehensive TDD patterns and practices for all programming languages. This skill eliminates ~500-800 lines of redundant testing guidance per agent.

## When to Use

Apply TDD for:
- New feature implementation
- Bug fixes (test the bug first)
- Code refactoring (tests ensure behavior preservation)
- API development (test contracts)
- Complex business logic

## TDD Workflow (Red-Green-Refactor)

### 1. Red Phase: Write Failing Test
```
Write a test that:
- Describes the desired behavior
- Fails for the right reason (not due to syntax errors)
- Is focused on a single behavior
```

### 2. Green Phase: Make It Pass
```
Write the minimum code to:
- Pass the test
- Not introduce regressions
- Follow existing patterns
```

### 3. Refactor Phase: Improve Code
```
While keeping tests green:
- Remove duplication
- Improve naming
- Simplify logic
- Extract functions/classes
```

## Test Structure Patterns

### Arrange-Act-Assert (AAA)
```
// Arrange: Set up test data and conditions
const user = createTestUser({ role: 'admin' });

// Act: Perform the action being tested
const result = await authenticateUser(user);

// Assert: Verify the outcome
expect(result.isAuthenticated).toBe(true);
expect(result.permissions).toContain('admin');
```

### Given-When-Then (BDD Style)
```
Given: A user with admin privileges
When: They attempt to access protected resource
Then: Access is granted with appropriate permissions
```

## Test Naming Conventions

### Pattern: `test_should_<expected_behavior>_when_<condition>`

**Examples:**
- `test_should_return_user_when_id_exists()`
- `test_should_raise_error_when_user_not_found()`
- `test_should_validate_email_format_when_creating_account()`

### Language-Specific Conventions

**Python (pytest):**
```python
def test_should_calculate_total_when_items_added():
    # Arrange
    cart = ShoppingCart()
    cart.add_item(Item("Book", 10.00))
    cart.add_item(Item("Pen", 1.50))

    # Act
    total = cart.calculate_total()

    # Assert
    assert total == 11.50
```

**JavaScript (Jest):**
```javascript
describe('ShoppingCart', () => {
  test('should calculate total when items added', () => {
    const cart = new ShoppingCart();
    cart.addItem({ name: 'Book', price: 10.00 });
    cart.addItem({ name: 'Pen', price: 1.50 });

    const total = cart.calculateTotal();

    expect(total).toBe(11.50);
  });
});
```

**Go:**
```go
func TestShouldCalculateTotalWhenItemsAdded(t *testing.T) {
    // Arrange
    cart := NewShoppingCart()
    cart.AddItem(Item{Name: "Book", Price: 10.00})
    cart.AddItem(Item{Name: "Pen", Price: 1.50})

    // Act
    total := cart.CalculateTotal()

    // Assert
    if total != 11.50 {
        t.Errorf("Expected 11.50, got %f", total)
    }
}
```

## Test Types and Scope

### Unit Tests
- **Scope:** Single function/method
- **Dependencies:** Mocked
- **Speed:** Fast (< 10ms per test)
- **Coverage:** 80%+ of code paths

### Integration Tests
- **Scope:** Multiple components
- **Dependencies:** Real or test doubles
- **Speed:** Moderate (< 1s per test)
- **Coverage:** Critical paths and interfaces

### End-to-End Tests
- **Scope:** Full user workflows
- **Dependencies:** Real (in test environment)
- **Speed:** Slow (seconds to minutes)
- **Coverage:** Core user journeys

## Mocking and Test Doubles

### When to Mock
- External APIs and services
- Database operations (for unit tests)
- File system operations
- Time-dependent operations
- Random number generation

### Mock Types

**Stub:** Returns predefined data
```python
def get_user_stub(user_id):
    return User(id=user_id, name="Test User")
```

**Mock:** Verifies interactions
```python
mock_service = Mock()
service.process_payment(payment_data)
mock_service.process_payment.assert_called_once_with(payment_data)
```

**Fake:** Working implementation (simplified)
```python
class FakeDatabase:
    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)
```

## Test Coverage Guidelines

### Target Coverage Levels
- **Critical paths:** 100%
- **Business logic:** 95%+
- **Overall project:** 80%+
- **UI components:** 70%+

### What to Test
- ✅ Business logic and algorithms
- ✅ Edge cases and boundary conditions
- ✅ Error handling and validation
- ✅ State transitions
- ✅ Public APIs and interfaces

### What NOT to Test
- ❌ Framework internals
- ❌ Third-party libraries
- ❌ Trivial getters/setters
- ❌ Generated code
- ❌ Configuration files

## Testing Best Practices

### 1. One Assertion Per Test (When Possible)
```python
# Good: Focused test
def test_should_validate_email_format():
    assert is_valid_email("user@example.com") is True

# Avoid: Multiple unrelated assertions
def test_validation():
    assert is_valid_email("user@example.com") is True
    assert is_valid_phone("123-456-7890") is True  # Different concept
```

### 2. Test Independence
```python
# Good: Each test is self-contained
def test_user_creation():
    user = create_user("test@example.com")
    assert user.email == "test@example.com"

# Avoid: Tests depending on execution order
shared_user = None

def test_create_user():
    global shared_user
    shared_user = create_user("test@example.com")

def test_update_user():  # Depends on previous test
    shared_user.name = "Updated"
```

### 3. Descriptive Test Failures
```python
# Good: Clear failure message
assert result.status == 200, f"Expected 200, got {result.status}: {result.body}"

# Avoid: Unclear failure
assert result.status == 200
```

### 4. Test Data Builders
```python
# Good: Reusable test data creation
def create_test_user(**overrides):
    defaults = {
        'email': 'test@example.com',
        'name': 'Test User',
        'role': 'user'
    }
    return User(**{**defaults, **overrides})

# Usage
admin = create_test_user(role='admin')
guest = create_test_user(email='guest@example.com')
```

## Testing Anti-Patterns to Avoid

### ❌ Testing Implementation Details
```python
# Bad: Tests internal structure
def test_user_storage():
    user = User("test@example.com")
    assert user._internal_cache is not None  # Implementation detail
```

### ❌ Fragile Tests
```python
# Bad: Breaks with harmless changes
assert user.to_json() == '{"name":"John","email":"john@example.com"}'

# Good: Tests behavior, not format
data = json.loads(user.to_json())
assert data['name'] == "John"
assert data['email'] == "john@example.com"
```

### ❌ Slow Tests in Unit Test Suite
```python
# Bad: Real HTTP calls in unit tests
def test_api_integration():
    response = requests.get("https://api.example.com/users")  # Slow!
    assert response.status_code == 200
```

### ❌ Testing Everything Through UI
```python
# Bad: Testing business logic through UI
def test_calculation():
    browser.click("#input1")
    browser.type("5")
    browser.click("#input2")
    browser.type("3")
    browser.click("#calculate")
    assert browser.find("#result").text == "8"

# Good: Test logic directly
def test_calculation():
    assert calculate(5, 3) == 8
```

## Quick Reference by Language

### Python (pytest)
```python
# Setup/Teardown
@pytest.fixture
def database():
    db = create_test_database()
    yield db
    db.cleanup()

# Parametrized tests
@pytest.mark.parametrize("input,expected", [
    ("user@example.com", True),
    ("invalid-email", False),
])
def test_email_validation(input, expected):
    assert is_valid_email(input) == expected
```

### JavaScript (Jest)
```javascript
// Setup/Teardown
beforeEach(() => {
  database = createTestDatabase();
});

afterEach(() => {
  database.cleanup();
});

// Async tests
test('should fetch user data', async () => {
  const user = await fetchUser(1);
  expect(user.name).toBe('John');
});
```

### Go
```go
// Table-driven tests
func TestEmailValidation(t *testing.T) {
    tests := []struct {
        input    string
        expected bool
    }{
        {"user@example.com", true},
        {"invalid-email", false},
    }

    for _, tt := range tests {
        result := IsValidEmail(tt.input)
        if result != tt.expected {
            t.Errorf("IsValidEmail(%s) = %v, want %v",
                tt.input, result, tt.expected)
        }
    }
}
```

## TDD Benefits Realized

- **Design Improvement:** Tests drive better API design
- **Documentation:** Tests serve as executable documentation
- **Confidence:** Refactoring becomes safe
- **Debugging:** Tests isolate issues quickly
- **Coverage:** Ensures comprehensive test coverage
- **Regression Prevention:** Catches bugs before deployment

## Related Skills

When using Test Driven Development, these skills enhance your workflow:
- **systematic-debugging**: Debug-first methodology when tests fail unexpectedly
- **react**: Testing React components, hooks, and context
- **django**: Testing Django models, views, and forms
- **fastapi-local-dev**: Testing FastAPI endpoints and dependency injection

[Full documentation available in these skills if deployed in your bundle]
