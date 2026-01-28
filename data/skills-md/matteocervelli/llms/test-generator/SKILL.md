---
name: test-generator
description: Generate test scaffolding for modules with proper structure, fixtures,
  and mock configurations.
allowed-tools: Read, Write, Edit
---

# Test Generator Skill

## Purpose

This skill provides comprehensive test scaffolding and templates for quickly setting up unit and integration tests with proper structure, fixtures, and mocking configurations. It guides the creation of well-structured, maintainable tests following best practices.

## Activation

**On-demand via command:** `/generate-tests <file-path>`

Example:
```bash
/generate-tests src/tools/example/core.py
```

## When to Use

- Starting tests for a new module
- Need test structure quickly
- Adding tests to existing code
- Setting up test fixtures and mocks
- Creating integration test scaffolding
- Following pytest or Jest best practices

## Resources

### testing-templates/unit-test.py
Complete pytest unit test template with:
- Proper import structure
- Fixture definitions (sample data, temp files, mocks)
- Test function templates (Arrange-Act-Assert pattern)
- Test class templates
- Parametrize examples
- Mock/patch configurations
- Common assertion patterns

### testing-templates/integration-test.py
Complete integration test template with:
- Service integration patterns
- Database integration examples
- File system test patterns
- End-to-end workflow examples
- Cleanup patterns (tmp_path, fixtures)
- Real dependency testing (not mocked)

## Provides

### Test File Scaffolding
- Proper file structure and organization
- Naming conventions (`test_*.py` or `*_test.py`)
- Import statements
- Test class/function structure

### Fixture Setup
- **pytest**: Sample fixtures for common use cases
- **Jest**: Mock implementations and spy configurations
- Reusable test data fixtures
- Setup/teardown patterns

### Mock Configurations
- **unittest.mock**: Mock and patch examples
- **pytest-mock**: pytest-specific mocking
- **Jest**: Mock modules and functions
- Spy and stub patterns

### Coverage Analysis Helpers
- Test organization for better coverage
- Edge case identification
- Boundary testing patterns

## Usage Examples

### Example 1: Generate Unit Tests for Module

```bash
/generate-tests src/tools/doc_fetcher/core.py
```

**Provides:**
- `tests/test_doc_fetcher_core.py` structure
- Fixtures for test data
- Test cases for each public function
- Mock configurations for external dependencies

### Example 2: Generate Integration Tests for API

```bash
/generate-tests src/api/endpoints.py
```

**Provides:**
- `tests/integration/test_endpoints.py` structure
- API client fixtures
- Request/response test patterns
- End-to-end workflow tests

### Example 3: TypeScript/Jest Tests

```bash
/generate-tests src/components/Button.tsx
```

**Provides:**
- `src/components/Button.test.tsx` structure
- Jest mock configurations
- Component testing patterns
- Snapshot testing examples

## Test Structure Patterns

### Arrange-Act-Assert (AAA) Pattern

```python
def test_function_name_condition_expected():
    """Test description."""
    # Arrange - Set up test data and conditions
    input_data = {"key": "value"}
    expected = "result"

    # Act - Execute the function under test
    result = function_under_test(input_data)

    # Assert - Verify the outcome
    assert result == expected
```

### Test Class Organization

```python
class TestClassName:
    """Tests for ClassName."""

    @pytest.fixture
    def instance(self):
        """Create test instance."""
        return ClassName()

    def test_method_success(self, instance):
        """Test successful method execution."""
        result = instance.method()
        assert result is not None

    def test_method_error_handling(self, instance):
        """Test method handles errors."""
        with pytest.raises(ValueError):
            instance.method(invalid_input)
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("test1", "result1"),
    ("test2", "result2"),
    ("test3", "result3"),
])
def test_function_with_parameters(input, expected):
    """Test function with multiple inputs."""
    result = function_under_test(input)
    assert result == expected
```

## Mocking Patterns

### Mock External Dependencies

```python
from unittest.mock import Mock, patch

@patch('module.external_service')
def test_with_mocked_service(mock_service):
    """Test with mocked external service."""
    # Configure mock
    mock_service.return_value = "mocked_response"

    # Test function that uses service
    result = function_that_calls_service()

    # Verify
    assert result == "expected"
    mock_service.assert_called_once()
```

### Fixture-Based Mocks

```python
@pytest.fixture
def mock_database():
    """Mock database connection."""
    db = Mock()
    db.query.return_value = [{"id": 1, "name": "test"}]
    return db

def test_database_query(mock_database):
    """Test database query."""
    result = get_data(mock_database)
    assert len(result) == 1
    mock_database.query.assert_called()
```

## Integration Test Patterns

### API Integration Testing

```python
def test_api_endpoint_integration(client):
    """Test API endpoint with real client."""
    # Arrange
    payload = {"data": "test"}

    # Act
    response = client.post("/api/endpoint", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["status"] == "success"
```

### Database Integration Testing

```python
def test_database_integration(db_session):
    """Test database operations."""
    # Arrange
    record = Model(name="test", value=123)

    # Act
    db_session.add(record)
    db_session.commit()

    # Assert
    result = db_session.query(Model).filter_by(name="test").first()
    assert result is not None
    assert result.value == 123
```

## Coverage Considerations

### Testing Requirements
- Aim for 80%+ test coverage
- Test all public functions and methods
- Test edge cases and boundary conditions
- Test error handling paths
- Test integration points

### Coverage Tools

```bash
# Python with pytest-cov
pytest --cov=src --cov-report=html

# JavaScript with Jest
jest --coverage

# View coverage report
open htmlcov/index.html  # Python
open coverage/lcov-report/index.html  # JavaScript
```

## Best Practices

### Test Naming
- Use descriptive names: `test_function_condition_expected`
- Example: `test_process_data_invalid_input_raises_error`

### Test Organization
- One test file per source file
- Group related tests in classes
- Use fixtures for common setup

### Test Independence
- Tests should not depend on each other
- Each test should set up its own data
- Clean up resources after tests

### Test Readability
- Clear test descriptions
- Simple, focused test cases
- Readable assertions

### Mock Judiciously
- Mock external dependencies
- Test real code paths when possible
- Verify mock interactions

## Notes

- **Guidance Only**: This skill provides templates and guidance. It does not automatically generate test files.
- **Language Support**: Primary support for Python (pytest) and TypeScript/JavaScript (Jest).
- **Customization**: Templates should be adapted to specific project needs.
- **Best Practices**: Follow project-specific testing conventions and standards.

## Used When

- Starting test implementation for a new module
- Need quick test structure setup
- Learning test patterns for the project
- Ensuring consistent test organization
- Setting up complex fixtures or mocks
- Creating integration test scaffolding