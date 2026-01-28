---
name: pytest-patterns
description: Python testing with pytest covering fixtures, parametrization, mocking, and test organization for reliable test suites
---

# Pytest Patterns - Comprehensive Testing Guide

A comprehensive skill for mastering Python testing with pytest. This skill covers everything from basic test structure to advanced patterns including fixtures, parametrization, mocking, test organization, coverage analysis, and CI/CD integration.

## When to Use This Skill

Use this skill when:

- Writing tests for Python applications (web apps, APIs, CLI tools, libraries)
- Setting up test infrastructure for a new Python project
- Refactoring existing tests to be more maintainable and efficient
- Implementing test-driven development (TDD) workflows
- Creating fixture patterns for database, API, or external service testing
- Organizing large test suites with hundreds or thousands of tests
- Debugging failing tests or improving test reliability
- Setting up continuous integration testing pipelines
- Measuring and improving code coverage
- Writing integration, unit, or end-to-end tests
- Testing async Python code
- Mocking external dependencies and services

## Core Concepts

### What is pytest?

pytest is a mature, full-featured Python testing framework that makes it easy to write simple tests, yet scales to support complex functional testing. It provides:

- **Simple syntax**: Use plain `assert` statements instead of special assertion methods
- **Powerful fixtures**: Modular, composable test setup and teardown
- **Parametrization**: Run the same test with different inputs
- **Plugin ecosystem**: Hundreds of plugins for extended functionality
- **Detailed reporting**: Clear failure messages and debugging information
- **Test discovery**: Automatic test collection following naming conventions

### pytest vs unittest

```python
# unittest (traditional)
import unittest

class TestMath(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(2 + 2, 4)

# pytest (simpler)
def test_addition():
    assert 2 + 2 == 4
```

### Test Discovery Rules

pytest automatically discovers tests by following these conventions:

1. **Test files**: `test_*.py` or `*_test.py`
2. **Test functions**: Functions prefixed with `test_`
3. **Test classes**: Classes prefixed with `Test` (no `__init__` method)
4. **Test methods**: Methods prefixed with `test_` inside Test classes

## Fixtures - The Heart of pytest

### What are Fixtures?

Fixtures provide a fixed baseline for tests to run reliably and repeatably. They handle setup, provide test data, and perform cleanup.

### Basic Fixture Pattern

```python
import pytest

@pytest.fixture
def sample_data():
    """Provides sample data for testing."""
    return {"name": "Alice", "age": 30}

def test_data_access(sample_data):
    assert sample_data["name"] == "Alice"
    assert sample_data["age"] == 30
```

### Fixture Scopes

Fixtures can have different scopes controlling how often they're created:

- **function** (default): Created for each test function
- **class**: Created once per test class
- **module**: Created once per test module
- **package**: Created once per test package
- **session**: Created once per test session

```python
@pytest.fixture(scope="session")
def database_connection():
    """Database connection created once for entire test session."""
    conn = create_db_connection()
    yield conn
    conn.close()  # Cleanup after all tests

@pytest.fixture(scope="module")
def api_client():
    """API client created once per test module."""
    client = APIClient()
    client.authenticate()
    yield client
    client.logout()

@pytest.fixture  # scope="function" is default
def temp_file():
    """Temporary file created for each test."""
    import tempfile
    f = tempfile.NamedTemporaryFile(mode='w', delete=False)
    yield f.name
    os.unlink(f.name)
```

### Fixture Dependencies

Fixtures can depend on other fixtures, creating a dependency graph:

```python
@pytest.fixture
def database():
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture
def user_repository(database):
    """Depends on database fixture."""
    return UserRepository(database)

@pytest.fixture
def sample_user(user_repository):
    """Depends on user_repository, which depends on database."""
    user = user_repository.create(name="Test User")
    yield user
    user_repository.delete(user.id)

def test_user_operations(sample_user):
    """Uses sample_user fixture (which uses user_repository and database)."""
    assert sample_user.name == "Test User"
```

### Autouse Fixtures

Fixtures that run automatically without being explicitly requested:

```python
@pytest.fixture(autouse=True)
def reset_database():
    """Runs before every test automatically."""
    clear_database()
    seed_test_data()

@pytest.fixture(autouse=True, scope="session")
def configure_logging():
    """Configure logging once for entire test session."""
    import logging
    logging.basicConfig(level=logging.DEBUG)
```

### Fixture Factories

Fixtures that return functions for creating test data:

```python
@pytest.fixture
def make_user():
    """Factory fixture for creating users."""
    users = []

    def _make_user(name, email=None):
        user = User(name=name, email=email or f"{name}@example.com")
        users.append(user)
        return user

    yield _make_user

    # Cleanup all created users
    for user in users:
        user.delete()

def test_multiple_users(make_user):
    user1 = make_user("Alice")
    user2 = make_user("Bob", email="bob@test.com")
    assert user1.name == "Alice"
    assert user2.email == "bob@test.com"
```

## Parametrization - Testing Multiple Cases

### Basic Parametrization

Run the same test with different inputs:

```python
import pytest

@pytest.mark.parametrize("input_value,expected", [
    (2, 4),
    (3, 9),
    (4, 16),
    (5, 25),
])
def test_square(input_value, expected):
    assert input_value ** 2 == expected
```

### Multiple Parameters

```python
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_combinations(x, y):
    """Runs 4 times: (0,2), (0,3), (1,2), (1,3)."""
    assert x < y
```

### Parametrizing with IDs

Make test output more readable:

```python
@pytest.mark.parametrize("test_input,expected", [
    pytest.param("3+5", 8, id="addition"),
    pytest.param("2*4", 8, id="multiplication"),
    pytest.param("10-2", 8, id="subtraction"),
])
def test_eval(test_input, expected):
    assert eval(test_input) == expected

# Output:
# test_eval[addition] PASSED
# test_eval[multiplication] PASSED
# test_eval[subtraction] PASSED
```

### Parametrizing Fixtures

Create fixture instances with different values:

```python
@pytest.fixture(params=["mysql", "postgresql", "sqlite"])
def database_type(request):
    """Test runs three times, once for each database."""
    return request.param

def test_database_connection(database_type):
    conn = connect_to_database(database_type)
    assert conn.is_connected()
```

### Combining Parametrization and Marks

```python
@pytest.mark.parametrize("test_input,expected", [
    ("valid@email.com", True),
    ("invalid-email", False),
    pytest.param("edge@case", True, marks=pytest.mark.xfail),
    pytest.param("slow@test.com", True, marks=pytest.mark.slow),
])
def test_email_validation(test_input, expected):
    assert is_valid_email(test_input) == expected
```

### Indirect Parametrization

Pass parameters through fixtures:

```python
@pytest.fixture
def database(request):
    """Create database based on parameter."""
    db_type = request.param
    db = Database(db_type)
    db.connect()
    yield db
    db.close()

@pytest.mark.parametrize("database", ["mysql", "postgres"], indirect=True)
def test_database_operations(database):
    """database fixture receives the parameter value."""
    assert database.is_connected()
    database.execute("SELECT 1")
```

## Mocking and Monkeypatching

### Using pytest's monkeypatch

The `monkeypatch` fixture provides safe patching that's automatically undone:

```python
def test_get_user_env(monkeypatch):
    """Test environment variable access."""
    monkeypatch.setenv("USER", "testuser")
    assert os.getenv("USER") == "testuser"

def test_remove_env(monkeypatch):
    """Test with missing environment variable."""
    monkeypatch.delenv("PATH", raising=False)
    assert os.getenv("PATH") is None

def test_modify_path(monkeypatch):
    """Test sys.path modification."""
    monkeypatch.syspath_prepend("/custom/path")
    assert "/custom/path" in sys.path
```

### Mocking Functions and Methods

```python
import requests

def get_user_data(user_id):
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

def test_get_user_data(monkeypatch):
    """Mock external API call."""
    class MockResponse:
        @staticmethod
        def json():
            return {"id": 1, "name": "Test User"}

    def mock_get(*args, **kwargs):
        return MockResponse()

    monkeypatch.setattr(requests, "get", mock_get)

    result = get_user_data(1)
    assert result["name"] == "Test User"
```

### Using unittest.mock

```python
from unittest.mock import Mock, MagicMock, patch, call

def test_with_mock():
    """Basic mock usage."""
    mock_db = Mock()
    mock_db.get_user.return_value = {"id": 1, "name": "Alice"}

    user = mock_db.get_user(1)
    assert user["name"] == "Alice"
    mock_db.get_user.assert_called_once_with(1)

def test_with_patch():
    """Patch during test execution."""
    with patch('mymodule.database.get_connection') as mock_conn:
        mock_conn.return_value = Mock()
        # Test code that uses database.get_connection()
        assert mock_conn.called

@patch('mymodule.send_email')
def test_notification(mock_email):
    """Patch as decorator."""
    send_notification("test@example.com", "Hello")
    mock_email.assert_called_once()
```

### Mock Return Values and Side Effects

```python
def test_mock_return_values():
    """Different return values for sequential calls."""
    mock_api = Mock()
    mock_api.fetch.side_effect = [
        {"status": "pending"},
        {"status": "processing"},
        {"status": "complete"}
    ]

    assert mock_api.fetch()["status"] == "pending"
    assert mock_api.fetch()["status"] == "processing"
    assert mock_api.fetch()["status"] == "complete"

def test_mock_exception():
    """Mock raising exceptions."""
    mock_service = Mock()
    mock_service.connect.side_effect = ConnectionError("Failed to connect")

    with pytest.raises(ConnectionError):
        mock_service.connect()
```

### Spy Pattern - Partial Mocking

```python
def test_spy_pattern(monkeypatch):
    """Spy on a function while preserving original behavior."""
    original_function = mymodule.process_data
    call_count = 0

    def spy_function(*args, **kwargs):
        nonlocal call_count
        call_count += 1
        return original_function(*args, **kwargs)

    monkeypatch.setattr(mymodule, "process_data", spy_function)

    result = mymodule.process_data([1, 2, 3])
    assert call_count == 1
    assert result is not None  # Original function executed
```

## Test Organization

### Directory Structure

```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── models.py
│       ├── services.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Shared fixtures
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   └── test_utils.py
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── conftest.py      # Integration-specific fixtures
│   │   └── test_services.py
│   └── e2e/
│       └── test_workflows.py
├── pytest.ini               # pytest configuration
└── setup.py
```

### conftest.py - Sharing Fixtures

The `conftest.py` file makes fixtures available to all tests in its directory and subdirectories:

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def database():
    """Database connection available to all tests."""
    db = Database()
    db.connect()
    yield db
    db.disconnect()

@pytest.fixture
def clean_database(database):
    """Reset database before each test."""
    database.clear_all_tables()
    return database

def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
```

### Using Markers

Markers allow categorizing and selecting tests:

```python
import pytest

@pytest.mark.slow
def test_slow_operation():
    """Marked as slow test."""
    time.sleep(5)
    assert True

@pytest.mark.integration
def test_api_integration():
    """Marked as integration test."""
    response = requests.get("https://api.example.com")
    assert response.status_code == 200

@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    """Skipped test."""
    pass

@pytest.mark.skipif(sys.version_info < (3, 8), reason="Requires Python 3.8+")
def test_python38_feature():
    """Conditionally skipped."""
    pass

@pytest.mark.xfail(reason="Known bug in dependency")
def test_known_failure():
    """Expected to fail."""
    assert False

@pytest.mark.parametrize("env", ["dev", "staging", "prod"])
@pytest.mark.integration
def test_environments(env):
    """Multiple markers on one test."""
    assert environment_exists(env)
```

Running tests with markers:

```bash
pytest -m slow                    # Run only slow tests
pytest -m "not slow"              # Skip slow tests
pytest -m "integration and not slow"  # Integration tests that aren't slow
pytest --markers                  # List all available markers
```

### Test Classes for Organization

```python
class TestUserAuthentication:
    """Group related authentication tests."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup for all tests in this class."""
        self.user_service = UserService()

    def test_login_success(self):
        result = self.user_service.login("user", "password")
        assert result.success

    def test_login_failure(self):
        result = self.user_service.login("user", "wrong")
        assert not result.success

    def test_logout(self):
        self.user_service.login("user", "password")
        assert self.user_service.logout()

class TestUserRegistration:
    """Group related registration tests."""

    def test_register_new_user(self):
        pass

    def test_register_duplicate_email(self):
        pass
```

## Coverage Analysis

### Installing Coverage Tools

```bash
pip install pytest-cov
```

### Running Coverage

```bash
# Basic coverage report
pytest --cov=mypackage tests/

# Coverage with HTML report
pytest --cov=mypackage --cov-report=html tests/
# Opens htmlcov/index.html

# Coverage with terminal report
pytest --cov=mypackage --cov-report=term-missing tests/

# Coverage with multiple formats
pytest --cov=mypackage --cov-report=html --cov-report=term tests/

# Fail if coverage below threshold
pytest --cov=mypackage --cov-fail-under=80 tests/
```

### Coverage Configuration

```ini
# pytest.ini or setup.cfg
[tool:pytest]
addopts =
    --cov=mypackage
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80

[coverage:run]
source = mypackage
omit =
    */tests/*
    */venv/*
    */__pycache__/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
```

### Coverage in Code

```python
def critical_function():  # pragma: no cover
    """Excluded from coverage."""
    pass

if sys.platform == 'win32':  # pragma: no cover
    # Platform-specific code excluded
    pass
```

## pytest Configuration

### pytest.ini

```ini
[pytest]
# Test discovery
testpaths = tests
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Output options
addopts =
    -ra
    --strict-markers
    --strict-config
    --showlocals
    --tb=short
    --cov=mypackage
    --cov-report=html
    --cov-report=term-missing

# Markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    smoke: marks tests as smoke tests
    regression: marks tests as regression tests

# Timeout for tests
timeout = 300

# Minimum Python version
minversion = 7.0

# Directories to ignore
norecursedirs = .git .tox dist build *.egg venv

# Warning filters
filterwarnings =
    error
    ignore::DeprecationWarning
```

### pyproject.toml Configuration

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
addopts = [
    "-ra",
    "--strict-markers",
    "--cov=mypackage",
    "--cov-report=html",
    "--cov-report=term-missing",
]
markers = [
    "slow: marks tests as slow",
    "integration: marks tests as integration tests",
]

[tool.coverage.run]
source = ["mypackage"]
omit = ["*/tests/*", "*/venv/*"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
]
```

## CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/test.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -e .[dev]
        pip install pytest pytest-cov pytest-xdist

    - name: Run tests
      run: |
        pytest --cov=mypackage --cov-report=xml --cov-report=term-missing -n auto

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true
```

### GitLab CI

```yaml
# .gitlab-ci.yml
image: python:3.11

stages:
  - test
  - coverage

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"

cache:
  paths:
    - .cache/pip
    - venv/

before_script:
  - python -m venv venv
  - source venv/bin/activate
  - pip install -e .[dev]
  - pip install pytest pytest-cov

test:
  stage: test
  script:
    - pytest --junitxml=report.xml --cov=mypackage --cov-report=xml
  artifacts:
    when: always
    reports:
      junit: report.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

coverage:
  stage: coverage
  script:
    - pytest --cov=mypackage --cov-report=html --cov-fail-under=80
  coverage: '/(?i)total.*? (100(?:\.0+)?\%|[1-9]?\d(?:\.\d+)?\%)$/'
  artifacts:
    paths:
      - htmlcov/
```

### Jenkins Pipeline

```groovy
// Jenkinsfile
pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                sh 'python -m venv venv'
                sh '. venv/bin/activate && pip install -e .[dev]'
                sh '. venv/bin/activate && pip install pytest pytest-cov pytest-html'
            }
        }

        stage('Test') {
            steps {
                sh '. venv/bin/activate && pytest --junitxml=results.xml --html=report.html --cov=mypackage'
            }
            post {
                always {
                    junit 'results.xml'
                    publishHTML([
                        allowMissing: false,
                        alwaysLinkToLastBuild: true,
                        keepAll: true,
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
    }
}
```

## Advanced Patterns

### Testing Async Code

```python
import pytest
import asyncio

@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.mark.asyncio
async def test_async_function():
    result = await async_fetch_data()
    assert result is not None

@pytest.mark.asyncio
async def test_async_with_timeout():
    with pytest.raises(asyncio.TimeoutError):
        await asyncio.wait_for(slow_async_operation(), timeout=1.0)

# Using pytest-asyncio plugin
# pip install pytest-asyncio
```

### Testing Database Operations

```python
@pytest.fixture(scope="session")
def database_engine():
    """Create database engine for test session."""
    engine = create_engine("postgresql://test:test@localhost/testdb")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture
def db_session(database_engine):
    """Create new database session for each test."""
    connection = database_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

def test_user_creation(db_session):
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert db_session.query(User).count() == 1
```

### Testing with Temporary Files

```python
@pytest.fixture
def temp_directory(tmp_path):
    """Create temporary directory with sample files."""
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    (data_dir / "config.json").write_text('{"debug": true}')
    (data_dir / "data.csv").write_text("name,value\ntest,42")

    return data_dir

def test_file_processing(temp_directory):
    config = load_config(temp_directory / "config.json")
    assert config["debug"] is True

    data = load_csv(temp_directory / "data.csv")
    assert len(data) == 1
```

### Caplog - Capturing Log Output

```python
import logging

def test_logging_output(caplog):
    """Test that function logs correctly."""
    with caplog.at_level(logging.INFO):
        process_data()

    assert "Processing started" in caplog.text
    assert "Processing completed" in caplog.text
    assert len(caplog.records) == 2

def test_warning_logged(caplog):
    """Test warning is logged."""
    caplog.set_level(logging.WARNING)
    risky_operation()

    assert any(record.levelname == "WARNING" for record in caplog.records)
```

### Capsys - Capturing stdout/stderr

```python
def test_print_output(capsys):
    """Test console output."""
    print("Hello, World!")
    print("Error message", file=sys.stderr)

    captured = capsys.readouterr()
    assert "Hello, World!" in captured.out
    assert "Error message" in captured.err

def test_progressive_output(capsys):
    """Test multiple output captures."""
    print("First")
    captured = capsys.readouterr()
    assert captured.out == "First\n"

    print("Second")
    captured = capsys.readouterr()
    assert captured.out == "Second\n"
```

## Test Examples

### Example 1: Basic Unit Test

```python
# test_calculator.py
import pytest
from calculator import add, subtract, multiply, divide

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 5) == -5

def test_multiply():
    assert multiply(3, 4) == 12
    assert multiply(-2, 3) == -6

def test_divide():
    assert divide(10, 2) == 5
    assert divide(7, 2) == 3.5

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)
```

### Example 2: Parametrized String Validation

```python
# test_validators.py
import pytest
from validators import is_valid_email, is_valid_phone, is_valid_url

@pytest.mark.parametrize("email,expected", [
    ("user@example.com", True),
    ("user.name+tag@example.co.uk", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("user@", False),
    ("", False),
])
def test_email_validation(email, expected):
    assert is_valid_email(email) == expected

@pytest.mark.parametrize("phone,expected", [
    ("+1-234-567-8900", True),
    ("(555) 123-4567", True),
    ("1234567890", True),
    ("123", False),
    ("abc-def-ghij", False),
])
def test_phone_validation(phone, expected):
    assert is_valid_phone(phone) == expected

@pytest.mark.parametrize("url,expected", [
    ("https://www.example.com", True),
    ("http://example.com/path?query=1", True),
    ("ftp://files.example.com", True),
    ("not a url", False),
    ("http://", False),
])
def test_url_validation(url, expected):
    assert is_valid_url(url) == expected
```

### Example 3: API Testing with Fixtures

```python
# test_api.py
import pytest
import requests
from api_client import APIClient

@pytest.fixture(scope="module")
def api_client():
    """Create API client for test module."""
    client = APIClient(base_url="https://api.example.com")
    client.authenticate(api_key="test-key")
    yield client
    client.close()

@pytest.fixture
def sample_user(api_client):
    """Create sample user for testing."""
    user = api_client.create_user({
        "name": "Test User",
        "email": "test@example.com"
    })
    yield user
    api_client.delete_user(user["id"])

def test_get_user(api_client, sample_user):
    user = api_client.get_user(sample_user["id"])
    assert user["name"] == "Test User"
    assert user["email"] == "test@example.com"

def test_update_user(api_client, sample_user):
    updated = api_client.update_user(sample_user["id"], {
        "name": "Updated Name"
    })
    assert updated["name"] == "Updated Name"

def test_list_users(api_client):
    users = api_client.list_users()
    assert isinstance(users, list)
    assert len(users) > 0

def test_user_not_found(api_client):
    with pytest.raises(requests.HTTPError) as exc:
        api_client.get_user("nonexistent-id")
    assert exc.value.response.status_code == 404
```

### Example 4: Database Testing

```python
# test_models.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import Base, User, Post

@pytest.fixture(scope="function")
def db_session():
    """Create clean database session for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)

    yield session

    session.close()

@pytest.fixture
def sample_user(db_session):
    """Create sample user."""
    user = User(username="testuser", email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user

def test_user_creation(db_session):
    user = User(username="newuser", email="new@example.com")
    db_session.add(user)
    db_session.commit()

    assert user.id is not None
    assert db_session.query(User).count() == 1

def test_user_posts(db_session, sample_user):
    post1 = Post(title="First Post", content="Content 1", user=sample_user)
    post2 = Post(title="Second Post", content="Content 2", user=sample_user)
    db_session.add_all([post1, post2])
    db_session.commit()

    assert len(sample_user.posts) == 2
    assert sample_user.posts[0].title == "First Post"

def test_user_deletion_cascades(db_session, sample_user):
    post = Post(title="Post", content="Content", user=sample_user)
    db_session.add(post)
    db_session.commit()

    db_session.delete(sample_user)
    db_session.commit()

    assert db_session.query(Post).count() == 0
```

### Example 5: Mocking External Services

```python
# test_notification_service.py
import pytest
from unittest.mock import Mock, patch
from notification_service import NotificationService, EmailProvider, SMSProvider

@pytest.fixture
def mock_email_provider():
    provider = Mock(spec=EmailProvider)
    provider.send.return_value = {"status": "sent", "id": "email-123"}
    return provider

@pytest.fixture
def mock_sms_provider():
    provider = Mock(spec=SMSProvider)
    provider.send.return_value = {"status": "sent", "id": "sms-456"}
    return provider

@pytest.fixture
def notification_service(mock_email_provider, mock_sms_provider):
    return NotificationService(
        email_provider=mock_email_provider,
        sms_provider=mock_sms_provider
    )

def test_send_email_notification(notification_service, mock_email_provider):
    result = notification_service.send_email(
        to="user@example.com",
        subject="Test",
        body="Test message"
    )

    assert result["status"] == "sent"
    mock_email_provider.send.assert_called_once()
    call_args = mock_email_provider.send.call_args
    assert call_args[1]["to"] == "user@example.com"

def test_send_sms_notification(notification_service, mock_sms_provider):
    result = notification_service.send_sms(
        to="+1234567890",
        message="Test SMS"
    )

    assert result["status"] == "sent"
    mock_sms_provider.send.assert_called_once_with(
        to="+1234567890",
        message="Test SMS"
    )

def test_notification_retry_on_failure(notification_service, mock_email_provider):
    mock_email_provider.send.side_effect = [
        Exception("Network error"),
        Exception("Network error"),
        {"status": "sent", "id": "email-123"}
    ]

    result = notification_service.send_email_with_retry(
        to="user@example.com",
        subject="Test",
        body="Test message",
        max_retries=3
    )

    assert result["status"] == "sent"
    assert mock_email_provider.send.call_count == 3
```

### Example 6: Testing File Operations

```python
# test_file_processor.py
import pytest
from pathlib import Path
from file_processor import process_csv, process_json, FileProcessor

@pytest.fixture
def csv_file(tmp_path):
    """Create temporary CSV file."""
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(
        "name,age,city\n"
        "Alice,30,New York\n"
        "Bob,25,Los Angeles\n"
        "Charlie,35,Chicago\n"
    )
    return csv_path

@pytest.fixture
def json_file(tmp_path):
    """Create temporary JSON file."""
    import json
    json_path = tmp_path / "data.json"
    data = {
        "users": [
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25}
        ]
    }
    json_path.write_text(json.dumps(data))
    return json_path

def test_process_csv(csv_file):
    data = process_csv(csv_file)
    assert len(data) == 3
    assert data[0]["name"] == "Alice"
    assert data[1]["age"] == "25"

def test_process_json(json_file):
    data = process_json(json_file)
    assert len(data["users"]) == 2
    assert data["users"][0]["name"] == "Alice"

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        process_csv("nonexistent.csv")

def test_file_processor_creates_backup(tmp_path):
    processor = FileProcessor(tmp_path)
    source = tmp_path / "original.txt"
    source.write_text("original content")

    processor.process_with_backup(source)

    backup = tmp_path / "original.txt.bak"
    assert backup.exists()
    assert backup.read_text() == "original content"
```

### Example 7: Testing Classes and Methods

```python
# test_shopping_cart.py
import pytest
from shopping_cart import ShoppingCart, Product

@pytest.fixture
def cart():
    """Create empty shopping cart."""
    return ShoppingCart()

@pytest.fixture
def products():
    """Create sample products."""
    return [
        Product(id=1, name="Book", price=10.99),
        Product(id=2, name="Pen", price=2.50),
        Product(id=3, name="Notebook", price=5.99),
    ]

def test_add_product(cart, products):
    cart.add_product(products[0], quantity=2)
    assert cart.total_items() == 2
    assert cart.subtotal() == 21.98

def test_remove_product(cart, products):
    cart.add_product(products[0], quantity=2)
    cart.remove_product(products[0].id, quantity=1)
    assert cart.total_items() == 1

def test_clear_cart(cart, products):
    cart.add_product(products[0])
    cart.add_product(products[1])
    cart.clear()
    assert cart.total_items() == 0

def test_apply_discount(cart, products):
    cart.add_product(products[0], quantity=2)
    cart.apply_discount(0.10)  # 10% discount
    assert cart.total() == pytest.approx(19.78, rel=0.01)

def test_cannot_add_negative_quantity(cart, products):
    with pytest.raises(ValueError, match="Quantity must be positive"):
        cart.add_product(products[0], quantity=-1)

class TestShoppingCartDiscounts:
    """Test various discount scenarios."""

    @pytest.fixture
    def cart_with_items(self, cart, products):
        cart.add_product(products[0], quantity=2)
        cart.add_product(products[1], quantity=3)
        return cart

    def test_percentage_discount(self, cart_with_items):
        original = cart_with_items.total()
        cart_with_items.apply_discount(0.20)
        assert cart_with_items.total() == original * 0.80

    def test_fixed_discount(self, cart_with_items):
        original = cart_with_items.total()
        cart_with_items.apply_fixed_discount(5.00)
        assert cart_with_items.total() == original - 5.00

    def test_cannot_apply_negative_discount(self, cart_with_items):
        with pytest.raises(ValueError):
            cart_with_items.apply_discount(-0.10)
```

### Example 8: Testing Command-Line Interface

```python
# test_cli.py
import pytest
from click.testing import CliRunner
from myapp.cli import cli

@pytest.fixture
def runner():
    """Create CLI test runner."""
    return CliRunner()

def test_cli_help(runner):
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Usage:' in result.output

def test_cli_version(runner):
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert '1.0.0' in result.output

def test_cli_process_file(runner, tmp_path):
    input_file = tmp_path / "input.txt"
    input_file.write_text("test data")

    result = runner.invoke(cli, ['process', str(input_file)])
    assert result.exit_code == 0
    assert 'Processing complete' in result.output

def test_cli_invalid_option(runner):
    result = runner.invoke(cli, ['--invalid-option'])
    assert result.exit_code != 0
    assert 'Error' in result.output
```

### Example 9: Testing Async Functions

```python
# test_async_operations.py
import pytest
import asyncio
from async_service import fetch_data, process_batch, AsyncWorker

@pytest.mark.asyncio
async def test_fetch_data():
    data = await fetch_data("https://api.example.com/data")
    assert data is not None
    assert 'results' in data

@pytest.mark.asyncio
async def test_process_batch():
    items = [1, 2, 3, 4, 5]
    results = await process_batch(items)
    assert len(results) == 5

@pytest.mark.asyncio
async def test_async_worker():
    worker = AsyncWorker()
    await worker.start()

    result = await worker.submit_task("process", data={"key": "value"})
    assert result["status"] == "completed"

    await worker.stop()

@pytest.mark.asyncio
async def test_concurrent_requests():
    async with AsyncWorker() as worker:
        tasks = [
            worker.submit_task("task1"),
            worker.submit_task("task2"),
            worker.submit_task("task3"),
        ]
        results = await asyncio.gather(*tasks)
        assert len(results) == 3
```

### Example 10: Fixture Parametrization

```python
# test_database_backends.py
import pytest
from database import DatabaseConnection

@pytest.fixture(params=['sqlite', 'postgresql', 'mysql'])
def db_connection(request):
    """Test runs three times, once for each database."""
    db = DatabaseConnection(request.param)
    db.connect()
    yield db
    db.disconnect()

def test_database_insert(db_connection):
    """Test insert operation on each database."""
    db_connection.execute("INSERT INTO users (name) VALUES ('test')")
    result = db_connection.execute("SELECT COUNT(*) FROM users")
    assert result[0][0] == 1

def test_database_transaction(db_connection):
    """Test transaction support on each database."""
    with db_connection.transaction():
        db_connection.execute("INSERT INTO users (name) VALUES ('test')")
        db_connection.rollback()

    result = db_connection.execute("SELECT COUNT(*) FROM users")
    assert result[0][0] == 0
```

### Example 11: Testing Exceptions

```python
# test_error_handling.py
import pytest
from custom_errors import ValidationError, AuthenticationError
from validator import validate_user_input
from auth import authenticate_user

def test_validation_error_message():
    with pytest.raises(ValidationError) as exc_info:
        validate_user_input({"email": "invalid"})

    assert "Invalid email format" in str(exc_info.value)
    assert exc_info.value.field == "email"

def test_multiple_validation_errors():
    with pytest.raises(ValidationError) as exc_info:
        validate_user_input({
            "email": "invalid",
            "age": -5
        })

    assert len(exc_info.value.errors) == 2

def test_authentication_error():
    with pytest.raises(AuthenticationError, match="Invalid credentials"):
        authenticate_user("user", "wrong_password")

@pytest.mark.parametrize("input_data,error_type", [
    ({"email": ""}, ValidationError),
    ({"email": None}, ValidationError),
    ({}, ValidationError),
])
def test_various_validation_errors(input_data, error_type):
    with pytest.raises(error_type):
        validate_user_input(input_data)
```

### Example 12: Testing with Fixtures and Mocks

```python
# test_payment_service.py
import pytest
from unittest.mock import Mock, patch
from payment_service import PaymentService, PaymentGateway
from models import Order, PaymentStatus

@pytest.fixture
def mock_gateway():
    gateway = Mock(spec=PaymentGateway)
    gateway.process_payment.return_value = {
        "transaction_id": "tx-12345",
        "status": "success"
    }
    return gateway

@pytest.fixture
def payment_service(mock_gateway):
    return PaymentService(gateway=mock_gateway)

@pytest.fixture
def sample_order():
    return Order(
        id="order-123",
        amount=99.99,
        currency="USD",
        customer_id="cust-456"
    )

def test_successful_payment(payment_service, mock_gateway, sample_order):
    result = payment_service.process_order(sample_order)

    assert result.status == PaymentStatus.SUCCESS
    assert result.transaction_id == "tx-12345"
    mock_gateway.process_payment.assert_called_once()

def test_payment_failure(payment_service, mock_gateway, sample_order):
    mock_gateway.process_payment.return_value = {
        "status": "failed",
        "error": "Insufficient funds"
    }

    result = payment_service.process_order(sample_order)

    assert result.status == PaymentStatus.FAILED
    assert "Insufficient funds" in result.error_message

def test_payment_retry_logic(payment_service, mock_gateway, sample_order):
    mock_gateway.process_payment.side_effect = [
        {"status": "error", "error": "Network timeout"},
        {"status": "error", "error": "Network timeout"},
        {"transaction_id": "tx-12345", "status": "success"}
    ]

    result = payment_service.process_order_with_retry(sample_order, max_retries=3)

    assert result.status == PaymentStatus.SUCCESS
    assert mock_gateway.process_payment.call_count == 3
```

### Example 13: Integration Test Example

```python
# test_integration_workflow.py
import pytest
from app import create_app
from database import db, User, Order

@pytest.fixture(scope="module")
def app():
    """Create application for testing."""
    app = create_app('testing')
    return app

@pytest.fixture(scope="module")
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture(scope="function")
def clean_db(app):
    """Clean database before each test."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield db
        db.session.remove()

@pytest.fixture
def authenticated_user(client, clean_db):
    """Create and authenticate user."""
    user = User(username="testuser", email="test@example.com")
    user.set_password("password123")
    clean_db.session.add(user)
    clean_db.session.commit()

    # Login
    response = client.post('/api/auth/login', json={
        'username': 'testuser',
        'password': 'password123'
    })
    token = response.json['access_token']

    return {'user': user, 'token': token}

def test_create_order_workflow(client, authenticated_user):
    """Test complete order creation workflow."""
    headers = {'Authorization': f'Bearer {authenticated_user["token"]}'}

    # Create order
    response = client.post('/api/orders',
        headers=headers,
        json={
            'items': [
                {'product_id': 1, 'quantity': 2},
                {'product_id': 2, 'quantity': 1}
            ]
        }
    )
    assert response.status_code == 201
    order_id = response.json['order_id']

    # Verify order was created
    response = client.get(f'/api/orders/{order_id}', headers=headers)
    assert response.status_code == 200
    assert len(response.json['items']) == 2

    # Update order status
    response = client.patch(f'/api/orders/{order_id}',
        headers=headers,
        json={'status': 'processing'}
    )
    assert response.status_code == 200
    assert response.json['status'] == 'processing'
```

### Example 14: Property-Based Testing

```python
# test_property_based.py
import pytest
from hypothesis import given, strategies as st
from string_utils import reverse_string, is_palindrome

@given(st.text())
def test_reverse_string_twice(s):
    """Reversing twice should return original string."""
    assert reverse_string(reverse_string(s)) == s

@given(st.lists(st.integers()))
def test_sort_idempotent(lst):
    """Sorting twice should be same as sorting once."""
    sorted_once = sorted(lst)
    sorted_twice = sorted(sorted_once)
    assert sorted_once == sorted_twice

@given(st.text(alphabet=st.characters(whitelist_categories=('Lu', 'Ll'))))
def test_palindrome_reverse(s):
    """If a string is a palindrome, its reverse is too."""
    if is_palindrome(s):
        assert is_palindrome(reverse_string(s))

@given(st.integers(min_value=1, max_value=1000))
def test_factorial_positive(n):
    """Factorial should always be positive."""
    from math import factorial
    assert factorial(n) > 0
```

### Example 15: Performance Testing

```python
# test_performance.py
import pytest
import time
from data_processor import process_large_dataset, optimize_query

@pytest.mark.slow
def test_large_dataset_processing_time():
    """Test that large dataset is processed within acceptable time."""
    start = time.time()
    data = list(range(1000000))
    result = process_large_dataset(data)
    duration = time.time() - start

    assert len(result) == 1000000
    assert duration < 5.0  # Should complete in under 5 seconds

@pytest.mark.benchmark
def test_query_optimization(benchmark):
    """Benchmark query performance."""
    result = benchmark(optimize_query, "SELECT * FROM users WHERE active=1")
    assert result is not None

@pytest.mark.parametrize("size", [100, 1000, 10000])
def test_scaling_performance(size):
    """Test performance with different data sizes."""
    data = list(range(size))
    start = time.time()
    result = process_large_dataset(data)
    duration = time.time() - start

    # Should scale linearly
    expected_max_time = size / 100000  # 1 second per 100k items
    assert duration < expected_max_time
```

## Best Practices

### Test Organization

1. **One test file per source file**: `mymodule.py` → `test_mymodule.py`
2. **Group related tests in classes**: Use `Test*` classes for logical grouping
3. **Use descriptive test names**: `test_user_login_with_invalid_credentials`
4. **Keep tests independent**: Each test should work in isolation
5. **Use fixtures for setup**: Avoid duplicate setup code

### Writing Effective Tests

1. **Follow AAA pattern**: Arrange, Act, Assert
   ```python
   def test_user_creation():
       # Arrange
       user_data = {"name": "Alice", "email": "alice@example.com"}

       # Act
       user = create_user(user_data)

       # Assert
       assert user.name == "Alice"
   ```

2. **Test one thing per test**: Each test should verify a single behavior
3. **Use descriptive assertions**: Make failures easy to understand
4. **Avoid test interdependencies**: Tests should not depend on execution order
5. **Test edge cases**: Empty lists, None values, boundary conditions

### Fixture Best Practices

1. **Use appropriate scope**: Minimize fixture creation cost
2. **Keep fixtures small**: Each fixture should have a single responsibility
3. **Use fixture factories**: For creating multiple test objects
4. **Clean up resources**: Use yield for teardown
5. **Share fixtures via conftest.py**: Make common fixtures available

### Coverage Guidelines

1. **Aim for high coverage**: 80%+ is a good target
2. **Focus on critical paths**: Prioritize important business logic
3. **Don't chase 100%**: Some code doesn't need tests (getters, setters)
4. **Use coverage to find gaps**: Not as a quality metric
5. **Exclude generated code**: Mark with `# pragma: no cover`

### CI/CD Integration

1. **Run tests on every commit**: Catch issues early
2. **Test on multiple Python versions**: Ensure compatibility
3. **Generate coverage reports**: Track coverage trends
4. **Fail on low coverage**: Maintain coverage standards
5. **Run tests in parallel**: Speed up CI pipeline

## Useful Plugins

- **pytest-cov**: Coverage reporting
- **pytest-xdist**: Parallel test execution
- **pytest-asyncio**: Async/await support
- **pytest-mock**: Enhanced mocking
- **pytest-timeout**: Test timeouts
- **pytest-randomly**: Randomize test order
- **pytest-html**: HTML test reports
- **pytest-benchmark**: Performance benchmarking
- **hypothesis**: Property-based testing
- **pytest-django**: Django testing support
- **pytest-flask**: Flask testing support

## Troubleshooting

### Tests Not Discovered

- Check file naming: `test_*.py` or `*_test.py`
- Check function naming: `test_*`
- Verify `__init__.py` files exist in test directories
- Run with `-v` flag to see discovery process

### Fixtures Not Found

- Check fixture is in `conftest.py` or same file
- Verify fixture scope is appropriate
- Check for typos in fixture name
- Use `--fixtures` flag to list available fixtures

### Test Failures

- Use `-v` for verbose output
- Use `--tb=long` for detailed tracebacks
- Use `--pdb` to drop into debugger on failure
- Use `-x` to stop on first failure
- Use `--lf` to rerun last failed tests

### Import Errors

- Ensure package is installed: `pip install -e .`
- Check PYTHONPATH is set correctly
- Verify `__init__.py` files exist
- Use `sys.path` manipulation if needed

## Resources

- pytest Documentation: https://docs.pytest.org/
- pytest GitHub: https://github.com/pytest-dev/pytest
- pytest Plugins: https://docs.pytest.org/en/latest/reference/plugin_list.html
- Real Python pytest Guide: https://realpython.com/pytest-python-testing/
- Test-Driven Development with Python: https://www.obeythetestinggoat.com/

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: Testing, Python, Quality Assurance, Test Automation
**Compatible With**: pytest 7.0+, Python 3.8+
