---
name: Pytest Testing
description: Master test-driven development with pytest, fixtures, mocking, and CI/CD integration
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 04-testing-quality
bond_type: PRIMARY_BOND

# Skill Configuration
retry_strategy: exponential_backoff
observability:
  logging: true
  metrics: coverage_percent
---

# Pytest Testing

## Overview

Master software testing with pytest, Python's most popular testing framework. Learn test-driven development (TDD), write maintainable tests, and ensure code quality through comprehensive testing strategies.

## Learning Objectives

- Write unit, integration, and functional tests with pytest
- Use fixtures for test setup and teardown
- Mock external dependencies effectively
- Implement test-driven development (TDD)
- Measure and improve code coverage
- Integrate tests with CI/CD pipelines

## Core Topics

### 1. Pytest Basics
- Test discovery and naming conventions
- Assertions and comparison
- Test organization (files, classes, modules)
- Running tests (command-line options)
- Markers and test selection
- Parametrized tests

**Code Example:**
```python
# test_calculator.py
import pytest

def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Basic test
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

# Test exceptions
def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)

# Parametrized test
@pytest.mark.parametrize("a,b,expected", [
    (10, 2, 5),
    (20, 4, 5),
    (100, 10, 10),
    (-10, 2, -5),
])
def test_divide(a, b, expected):
    assert divide(a, b) == expected

# Test with marker
@pytest.mark.slow
def test_complex_operation():
    # This test takes a long time
    result = sum(range(1000000))
    assert result == 499999500000
```

### 2. Fixtures & Test Setup
- Fixture scopes (function, class, module, session)
- Fixture dependencies
- Parametrized fixtures
- Built-in fixtures (tmpdir, capsys, monkeypatch)
- conftest.py for shared fixtures

**Code Example:**
```python
# conftest.py
import pytest
import tempfile
from pathlib import Path

@pytest.fixture
def sample_data():
    """Provide sample data for tests"""
    return {
        'users': [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'},
        ]
    }

@pytest.fixture
def temp_file():
    """Create temporary file for testing"""
    with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
        f.write("Test data")
        temp_path = f.name
    yield temp_path
    # Cleanup
    Path(temp_path).unlink()

@pytest.fixture(scope='module')
def database_connection():
    """Module-scoped database connection"""
    db = DatabaseConnection('test.db')
    db.connect()
    yield db
    db.close()

# test_users.py
def test_user_count(sample_data):
    assert len(sample_data['users']) == 2

def test_user_names(sample_data):
    names = [user['name'] for user in sample_data['users']]
    assert 'Alice' in names
    assert 'Bob' in names

def test_file_operations(temp_file):
    content = Path(temp_file).read_text()
    assert content == "Test data"
```

### 3. Mocking & Test Doubles
- unittest.mock basics
- Mocking functions and methods
- Patching objects
- Mock assertions
- Side effects and return values
- Testing with external dependencies

**Code Example:**
```python
# api_client.py
import requests

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_user(self, user_id):
        response = requests.get(f"{self.base_url}/users/{user_id}")
        response.raise_for_status()
        return response.json()

    def create_user(self, user_data):
        response = requests.post(f"{self.base_url}/users", json=user_data)
        response.raise_for_status()
        return response.json()

# test_api_client.py
from unittest.mock import Mock, patch
import pytest

@patch('api_client.requests.get')
def test_get_user(mock_get):
    # Setup mock
    mock_response = Mock()
    mock_response.json.return_value = {'id': 1, 'name': 'Alice'}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Test
    client = APIClient('https://api.example.com')
    user = client.get_user(1)

    # Assertions
    assert user['name'] == 'Alice'
    mock_get.assert_called_once_with('https://api.example.com/users/1')

@patch('api_client.requests.post')
def test_create_user(mock_post):
    # Setup mock
    mock_response = Mock()
    mock_response.json.return_value = {'id': 3, 'name': 'Charlie'}
    mock_post.return_value = mock_response

    # Test
    client = APIClient('https://api.example.com')
    user_data = {'name': 'Charlie', 'email': 'charlie@example.com'}
    result = client.create_user(user_data)

    # Assertions
    assert result['id'] == 3
    mock_post.assert_called_once_with(
        'https://api.example.com/users',
        json=user_data
    )
```

### 4. Coverage & CI/CD Integration
- Measuring code coverage with pytest-cov
- Coverage reports (terminal, HTML, XML)
- Setting coverage thresholds
- GitHub Actions integration
- GitLab CI integration
- Pre-commit hooks

**Code Example:**
```python
# pytest.ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    --cov=myapp
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
    -v

# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install pytest pytest-cov
      - name: Run tests
        run: |
          pytest --cov=myapp --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

# Command line usage
# Run all tests
pytest

# Run with coverage
pytest --cov=myapp

# Generate HTML coverage report
pytest --cov=myapp --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run tests with marker
pytest -m slow

# Run tests with verbose output
pytest -v

# Stop on first failure
pytest -x
```

## Hands-On Practice

### Project 1: Calculator TDD
Build a calculator using test-driven development.

**Requirements:**
- Write tests BEFORE implementation
- Basic operations (add, subtract, multiply, divide)
- Error handling (division by zero)
- Scientific operations (power, sqrt, log)
- Test coverage > 90%

**Key Skills:** TDD workflow, parametrized tests, exception testing

### Project 2: API Testing Suite
Create comprehensive test suite for a REST API.

**Requirements:**
- Mock HTTP requests
- Test CRUD operations
- Error handling tests
- Authentication tests
- Integration tests
- CI/CD pipeline setup

**Key Skills:** Mocking, fixtures, integration testing

### Project 3: Database Testing
Test database operations with fixtures and transactions.

**Requirements:**
- Setup test database fixture
- Test CRUD operations
- Transaction rollback
- Data validation
- Performance tests
- Coverage report

**Key Skills:** Database fixtures, cleanup, performance testing

## Assessment Criteria

- [ ] Write clear, maintainable tests
- [ ] Use fixtures appropriately
- [ ] Mock external dependencies effectively
- [ ] Achieve >80% code coverage
- [ ] Follow TDD principles
- [ ] Integrate tests with CI/CD
- [ ] Write meaningful assertions

## Resources

### Official Documentation
- [Pytest Docs](https://docs.pytest.org/) - Official documentation
- [pytest-cov](https://pytest-cov.readthedocs.io/) - Coverage plugin
- [unittest.mock](https://docs.python.org/3/library/unittest.mock.html) - Mocking library

### Learning Platforms
- [Test-Driven Development with Python](https://www.obeythetestinggoat.com/) - TDD book
- [Python Testing with pytest](https://pragprog.com/titles/bopytest/) - Brian Okken's book
- [Real Python Testing](https://realpython.com/pytest-python-testing/) - Tutorials

### Tools
- [pytest-xdist](https://pytest-xdist.readthedocs.io/) - Parallel testing
- [pytest-mock](https://pytest-mock.readthedocs.io/) - Mocking helper
- [Hypothesis](https://hypothesis.readthedocs.io/) - Property-based testing
- [tox](https://tox.wiki/) - Testing automation

## Next Steps

After mastering pytest, explore:
- **Property-based testing** - Hypothesis library
- **Performance testing** - pytest-benchmark
- **Mutation testing** - mutmut
- **Load testing** - Locust, pytest-load
