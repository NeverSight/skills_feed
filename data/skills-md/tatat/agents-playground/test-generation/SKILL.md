---
name: test-generation
description: Generate unit tests, integration tests, and test fixtures for code
---

# Test Generation

Generate comprehensive tests for code.

## Capabilities

- Generate unit tests for functions and classes
- Create integration tests for APIs and services
- Build test fixtures and mocks
- Cover edge cases and error conditions

## Test Structure

```python
import pytest

class TestClassName:
    """Tests for ClassName."""

    def test_method_success(self):
        """Test method with valid input."""
        result = function_under_test(valid_input)
        assert result == expected_output

    def test_method_edge_case(self):
        """Test method with edge case."""
        result = function_under_test(edge_case_input)
        assert result == edge_case_output

    def test_method_error(self):
        """Test method raises error on invalid input."""
        with pytest.raises(ValueError):
            function_under_test(invalid_input)
```

## Coverage Targets

| Type | Target |
|------|--------|
| Unit tests | 80%+ line coverage |
| Branch coverage | 70%+ |
| Critical paths | 100% |

## Test Categories

1. **Happy path** - Normal expected usage
2. **Edge cases** - Boundary values, empty inputs
3. **Error cases** - Invalid inputs, exceptions
4. **Integration** - Component interactions

## Fixtures Example

```python
@pytest.fixture
def sample_user():
    return User(name="Test User", email="test@example.com")

@pytest.fixture
def mock_database(mocker):
    return mocker.patch("app.db.connection")
```
