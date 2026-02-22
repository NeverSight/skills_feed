---
name: pytest
description: Python testing mastery with pytest, fixtures, parametrize, mocking, and coverage. Use when user asks to "write tests", "add pytest fixtures", "mock a function", "parametrize tests", "run coverage", "debug failing test", "set up conftest", or any Python testing tasks.
---

# pytest

Complete Python testing toolkit with pytest.

## Running Tests

```bash
# Run all tests
pytest

# Run specific file/directory
pytest tests/test_api.py
pytest tests/

# Run specific test
pytest tests/test_api.py::test_login
pytest tests/test_api.py::TestUserClass::test_create

# Verbose output
pytest -v
pytest -vv  # Extra verbose

# Stop on first failure
pytest -x

# Run last failed
pytest --lf

# Run failed first, then rest
pytest --ff

# Show print output
pytest -s

# Parallel (requires pytest-xdist)
pytest -n auto
pytest -n 4
```

## Fixtures

```python
import pytest

# Basic fixture
@pytest.fixture
def user():
    return {"name": "Alice", "email": "alice@test.com"}

# Fixture with teardown
@pytest.fixture
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()

# Autouse fixture (runs for every test)
@pytest.fixture(autouse=True)
def reset_state():
    State.reset()
    yield
    State.cleanup()

# Scoped fixtures
@pytest.fixture(scope="module")
def expensive_resource():
    return load_heavy_thing()

# scope options: "function" (default), "class", "module", "package", "session"

# Fixture with params
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def db_engine(request):
    return create_engine(request.param)

# Using fixtures
def test_user_name(user):
    assert user["name"] == "Alice"
```

## Parametrize

```python
# Basic parametrize
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("world", 5),
])
def test_string_length(input, expected):
    assert len(input) == expected

# Multiple parameters
@pytest.mark.parametrize("x", [0, 1])
@pytest.mark.parametrize("y", [2, 3])
def test_combinations(x, y):
    pass  # Runs 4 times: (0,2), (0,3), (1,2), (1,3)

# With IDs
@pytest.mark.parametrize("input,expected", [
    pytest.param("admin", True, id="admin-user"),
    pytest.param("guest", False, id="guest-user"),
])
def test_is_admin(input, expected):
    assert is_admin(input) == expected
```

## Mocking

```python
from unittest.mock import Mock, patch, MagicMock

# patch decorator
@patch("myapp.services.send_email")
def test_registration(mock_send):
    register_user("alice@test.com")
    mock_send.assert_called_once_with("alice@test.com", subject="Welcome")

# patch as context manager
def test_api_call():
    with patch("myapp.client.requests.get") as mock_get:
        mock_get.return_value.json.return_value = {"status": "ok"}
        result = fetch_status()
        assert result == "ok"

# Mock fixture (pytest-mock)
def test_with_mocker(mocker):
    mock_db = mocker.patch("myapp.db.query")
    mock_db.return_value = [{"id": 1}]
    result = get_users()
    assert len(result) == 1

# Side effects
mock_func = Mock(side_effect=ValueError("boom"))
mock_func = Mock(side_effect=[1, 2, 3])  # Returns sequentially
mock_func = Mock(side_effect=lambda x: x * 2)

# Spec mocking (catches attribute errors)
mock_obj = Mock(spec=MyClass)
```

## Markers

```python
# Skip
@pytest.mark.skip(reason="Not implemented yet")
def test_future_feature():
    pass

# Skip conditionally
@pytest.mark.skipif(sys.platform == "win32", reason="Unix only")
def test_unix_permissions():
    pass

# Expected failure
@pytest.mark.xfail(reason="Known bug #123")
def test_known_bug():
    pass

# Custom markers
@pytest.mark.slow
def test_heavy_computation():
    pass

# Run by marker: pytest -m slow
# Run excluding: pytest -m "not slow"

# Register markers in pytest.ini or pyproject.toml
# [tool.pytest.ini_options]
# markers = ["slow: marks tests as slow"]
```

## Assertions

```python
# Basic
assert result == expected
assert item in collection
assert value is None

# Exception testing
with pytest.raises(ValueError):
    int("not_a_number")

with pytest.raises(ValueError, match="invalid literal"):
    int("not_a_number")

# Approximate
assert 0.1 + 0.2 == pytest.approx(0.3)
assert result == pytest.approx(expected, rel=1e-3)

# Warnings
with pytest.warns(DeprecationWarning):
    deprecated_function()
```

## Coverage

```bash
# Install
pip install pytest-cov

# Run with coverage
pytest --cov=myapp
pytest --cov=myapp --cov-report=html
pytest --cov=myapp --cov-report=term-missing
pytest --cov=myapp --cov-branch  # Branch coverage

# Minimum threshold
pytest --cov=myapp --cov-fail-under=80
```

## conftest.py

```python
# tests/conftest.py - Shared fixtures available to all tests

import pytest

@pytest.fixture
def app():
    """Create test application."""
    app = create_app(testing=True)
    yield app

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture
def auth_headers():
    """Create auth headers."""
    token = create_test_token()
    return {"Authorization": f"Bearer {token}"}
```

## pyproject.toml Config

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --tb=short --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: integration tests",
]
filterwarnings = [
    "ignore::DeprecationWarning",
]
```

## Reference

For advanced patterns, plugins, and async testing: `references/patterns.md`
