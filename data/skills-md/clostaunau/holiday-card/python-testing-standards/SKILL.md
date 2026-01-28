---
name: python-testing-standards
description: Comprehensive Python testing best practices, pytest conventions, test structure patterns (AAA, Given-When-Then), fixture usage, mocking strategies, code coverage standards, and common anti-patterns. Essential reference for code reviews, test writing, and ensuring high-quality Python test suites with pytest, unittest.mock, and pytest-cov.
allowed-tools: Read, Write, Grep, Glob
---

# Python Testing Standards

## Purpose

This skill provides comprehensive testing standards and best practices for Python projects using pytest. It serves as a reference guide during code reviews to ensure test quality, maintainability, and adherence to Python testing conventions.

**When to use this skill:**
- Conducting code reviews of Python test files
- Writing new test suites
- Refactoring existing tests
- Evaluating test coverage and quality
- Teaching testing best practices to team members

## Context

High-quality tests are essential for maintaining reliable Python applications. This skill documents industry-standard testing practices using pytest, the de facto testing framework for modern Python development. These standards emphasize:

- **Clarity**: Tests should be easy to read and understand
- **Maintainability**: Tests should be easy to update as code evolves
- **Reliability**: Tests should be deterministic and fast
- **Coverage**: Tests should cover behavior, not just lines of code
- **Isolation**: Tests should be independent and not affect each other

This skill is designed to be referenced by the `uncle-duke-python` agent during code reviews and by developers when writing tests.

## Prerequisites

**Required Knowledge:**
- Python fundamentals
- Basic understanding of testing concepts
- Familiarity with pytest (or willingness to learn)

**Required Tools:**
- pytest (`pip install pytest`)
- pytest-cov for coverage (`pip install pytest-cov`)
- pytest-mock for mocking (`pip install pytest-mock`)
- unittest.mock (built into Python 3.3+)

**Expected Project Structure:**
```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       └── module.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── unit/
│   │   └── test_module.py
│   └── integration/
│       └── test_integration.py
├── pytest.ini
└── requirements-dev.txt
```

---

## Instructions

### Task 1: Verify pytest Conventions

#### 1.1 Test File Naming

**Rule:** Test files MUST follow one of these patterns:
- `test_*.py` (preferred)
- `*_test.py`

**Examples:**

✅ **Good:**
```python
# File: test_user_service.py
# File: test_authentication.py
# File: user_service_test.py  # acceptable but less common
```

❌ **Bad:**
```python
# File: user_tests.py  # missing 'test_' prefix
# File: test-user-service.py  # hyphens instead of underscores
# File: TestUserService.py  # CamelCase instead of snake_case
```

**Why:** pytest discovers test files by these patterns. Non-standard names won't be automatically discovered.

#### 1.2 Test Function Naming

**Rule:** Test functions MUST start with `test_` and describe the scenario being tested.

**Pattern:** `test_<what>_<when>_<expected_behavior>`

✅ **Good:**
```python
def test_user_login_with_valid_credentials_returns_token():
    """Test that valid credentials return an auth token."""
    pass

def test_user_login_with_invalid_password_raises_authentication_error():
    """Test that invalid password raises AuthenticationError."""
    pass

def test_calculate_total_with_empty_cart_returns_zero():
    """Test that empty cart returns zero total."""
    pass
```

❌ **Bad:**
```python
def test_login():  # Too vague
    pass

def test_user_service():  # Doesn't describe what's being tested
    pass

def testLogin():  # Missing underscore, CamelCase
    pass

def test_1():  # Non-descriptive
    pass
```

**Why:** Descriptive test names serve as documentation. When a test fails, the name should immediately tell you what broke.

#### 1.3 Test Class Naming

**Rule:** Test classes MUST start with `Test` (no `_test` suffix).

✅ **Good:**
```python
class TestUserAuthentication:
    """Tests for user authentication functionality."""

    def test_login_with_valid_credentials_succeeds(self):
        pass

    def test_login_with_invalid_credentials_fails(self):
        pass

class TestShoppingCart:
    """Tests for shopping cart operations."""

    def test_add_item_increases_count(self):
        pass
```

❌ **Bad:**
```python
class UserAuthenticationTests:  # Missing 'Test' prefix
    pass

class Test_UserAuth:  # Unnecessary underscore
    pass

class testUserAuth:  # Lowercase 'test'
    pass
```

**Why:** pytest discovers test classes by the `Test` prefix. Classes provide logical grouping of related tests.

**When to use classes vs functions:**
- Use classes when tests share setup/teardown logic or fixtures
- Use functions for simple, independent tests
- Don't use classes just for grouping without shared behavior

#### 1.4 Test Organization and Structure

**Directory Structure:**

```
tests/
├── __init__.py              # Makes tests a package
├── conftest.py              # Shared fixtures and configuration
├── unit/                    # Unit tests (fast, isolated)
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/             # Integration tests (slower, external deps)
│   ├── __init__.py
│   ├── test_database.py
│   └── test_api_endpoints.py
└── e2e/                     # End-to-end tests (slowest)
    ├── __init__.py
    └── test_user_workflows.py
```

**File Organization:**

Within a test file, organize tests logically:

```python
"""Tests for user authentication service."""

import pytest
from myapp.auth import AuthenticationService

# Fixtures at the top
@pytest.fixture
def auth_service():
    """Fixture providing authentication service instance."""
    return AuthenticationService()

# Test classes grouped by functionality
class TestUserLogin:
    """Tests for user login functionality."""

    def test_login_with_valid_credentials_succeeds(self, auth_service):
        pass

    def test_login_with_invalid_password_fails(self, auth_service):
        pass

class TestUserLogout:
    """Tests for user logout functionality."""

    def test_logout_invalidates_session(self, auth_service):
        pass

# Standalone functions for simple tests
def test_password_hashing_is_deterministic():
    """Test that same password always produces same hash."""
    pass
```

### Task 2: Apply Test Structure Patterns

#### 2.1 Arrange-Act-Assert (AAA) Pattern

**Rule:** Structure all tests using the AAA pattern with clear separation.

**Pattern:**
1. **Arrange**: Set up test data and preconditions
2. **Act**: Execute the behavior being tested
3. **Assert**: Verify the expected outcome

✅ **Good:**
```python
def test_calculate_total_with_discount_applies_correctly():
    """Test that discount is correctly applied to cart total."""
    # Arrange
    cart = ShoppingCart()
    cart.add_item(Item(name="Widget", price=100.00))
    cart.add_item(Item(name="Gadget", price=50.00))
    discount = Discount(percentage=10)

    # Act
    total = cart.calculate_total(discount=discount)

    # Assert
    assert total == 135.00  # (100 + 50) * 0.9
```

✅ **Good (with comments):**
```python
def test_user_registration_creates_new_user():
    """Test that user registration creates a new user record."""
    # Arrange
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "SecurePass123!"
    }
    user_service = UserService()

    # Act
    user = user_service.register(user_data)

    # Assert
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.id is not None
    assert user.password_hash != user_data["password"]  # Hashed
```

❌ **Bad:**
```python
def test_user_operations():
    # Everything mixed together
    user_service = UserService()
    user = user_service.register({"username": "test", "email": "test@example.com"})
    assert user.username == "test"
    user.update_email("new@example.com")
    assert user.email == "new@example.com"
    user_service.delete(user.id)
    assert user_service.get(user.id) is None
```

**Why bad:** Tests multiple behaviors, hard to debug when it fails, violates single responsibility.

#### 2.2 Given-When-Then (BDD Pattern)

**Alternative to AAA:** Given-When-Then is equivalent but uses BDD terminology.

**Pattern:**
1. **Given**: Preconditions and setup (same as Arrange)
2. **When**: Action being tested (same as Act)
3. **Then**: Expected outcome (same as Assert)

✅ **Good:**
```python
def test_withdraw_with_sufficient_balance_succeeds():
    """
    Given an account with a balance of $100
    When withdrawing $30
    Then the withdrawal succeeds and balance is $70
    """
    # Given
    account = Account(balance=100.00)

    # When
    result = account.withdraw(30.00)

    # Then
    assert result is True
    assert account.balance == 70.00
```

**Usage:** Use Given-When-Then for behavior-driven tests, especially in integration/e2e tests. Use AAA for unit tests. Be consistent within a project.

#### 2.3 Test Isolation

**Rule:** Each test MUST be completely independent and not rely on execution order.

✅ **Good:**
```python
@pytest.fixture
def clean_database():
    """Provide a clean database for each test."""
    db = Database()
    db.clear()
    yield db
    db.clear()  # Cleanup after test

def test_create_user_adds_to_database(clean_database):
    """Test user creation adds record to database."""
    user = User(username="test")
    clean_database.save(user)

    assert clean_database.count() == 1

def test_delete_user_removes_from_database(clean_database):
    """Test user deletion removes record from database."""
    user = User(username="test")
    clean_database.save(user)
    clean_database.delete(user.id)

    assert clean_database.count() == 0
```

❌ **Bad:**
```python
# Tests depend on execution order
db = Database()

def test_1_create_user():
    """This test must run first."""
    user = User(username="test")
    db.save(user)
    assert db.count() == 1

def test_2_delete_user():
    """This test depends on test_1 running first."""
    # Assumes user from test_1 exists
    users = db.get_all()
    db.delete(users[0].id)
    assert db.count() == 0
```

**Why bad:** Tests are brittle, fail when run in isolation or different order, hard to debug.

#### 2.4 Test Data Management

**Rule:** Use fixtures, factories, or builders for test data. Avoid magic values.

✅ **Good:**
```python
@pytest.fixture
def sample_user():
    """Provide a sample user for testing."""
    return User(
        username="john_doe",
        email="john@example.com",
        age=30,
        is_active=True
    )

@pytest.fixture
def user_factory():
    """Provide a factory for creating test users."""
    def _create_user(**kwargs):
        defaults = {
            "username": "test_user",
            "email": "test@example.com",
            "age": 25,
            "is_active": True
        }
        defaults.update(kwargs)
        return User(**defaults)
    return _create_user

def test_user_validation_with_invalid_age(user_factory):
    """Test that invalid age raises validation error."""
    user = user_factory(age=-5)

    with pytest.raises(ValidationError):
        user.validate()
```

❌ **Bad:**
```python
def test_user_creation():
    # Magic values scattered throughout
    user = User("john", "john@example.com", 30, True)
    assert user.username == "john"

def test_user_update():
    # Same magic values repeated
    user = User("john", "john@example.com", 30, True)
    user.update_age(31)
    assert user.age == 31
```

**Why bad:** Hard to maintain, unclear what values mean, violates DRY principle.

### Task 3: Implement Fixture Best Practices

#### 3.1 Fixture Scopes

**Rule:** Choose the appropriate scope based on fixture cost and state.

**Available Scopes:**
- `function`: Default, runs before each test function (most common)
- `class`: Runs once per test class
- `module`: Runs once per module
- `session`: Runs once per test session

✅ **Good:**
```python
@pytest.fixture(scope="session")
def database_engine():
    """Create database engine once per test session."""
    engine = create_engine("postgresql://localhost/test_db")
    yield engine
    engine.dispose()

@pytest.fixture(scope="module")
def database_schema(database_engine):
    """Create database schema once per module."""
    Base.metadata.create_all(database_engine)
    yield
    Base.metadata.drop_all(database_engine)

@pytest.fixture(scope="function")
def database_session(database_engine):
    """Provide a clean database session for each test."""
    connection = database_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

**Scope Selection Guidelines:**
- Use `function` scope for fixtures that need to be fresh for each test
- Use `module` or `session` scope for expensive setup (database connections, API clients)
- NEVER use broader scope for fixtures that maintain state between tests
- Always clean up in broader-scoped fixtures

❌ **Bad:**
```python
@pytest.fixture(scope="session")
def user_list():
    """DON'T DO THIS - mutable state in session scope."""
    return []  # This list will be shared across ALL tests!

def test_add_user(user_list):
    user_list.append("user1")
    assert len(user_list) == 1  # Might fail if other tests run first

def test_remove_user(user_list):
    # Depends on state from other tests
    user_list.remove("user1")
```

**Why bad:** Shared mutable state causes tests to interfere with each other.

#### 3.2 Fixture Dependencies

**Rule:** Fixtures can depend on other fixtures to build complex test scenarios.

✅ **Good:**
```python
@pytest.fixture
def database():
    """Provide database connection."""
    db = Database("test.db")
    yield db
    db.close()

@pytest.fixture
def user(database):
    """Provide a test user in the database."""
    user = User(username="testuser")
    database.save(user)
    return user

@pytest.fixture
def authenticated_user(user):
    """Provide an authenticated user."""
    user.login()
    return user

def test_user_can_access_profile(authenticated_user, database):
    """Test authenticated user can access their profile."""
    profile = database.get_profile(authenticated_user.id)
    assert profile is not None
    assert profile.user_id == authenticated_user.id
```

**Dependency Chain:** `database` → `user` → `authenticated_user`

This approach builds complex test scenarios from simple, reusable fixtures.

#### 3.3 Fixture Naming Conventions

**Rule:** Fixture names should be clear, descriptive nouns or noun phrases.

✅ **Good:**
```python
@pytest.fixture
def database_session():
    """Provide a database session."""
    pass

@pytest.fixture
def mock_email_service():
    """Provide a mocked email service."""
    pass

@pytest.fixture
def sample_user_data():
    """Provide sample user data dictionary."""
    pass

@pytest.fixture
def http_client():
    """Provide an HTTP client for API testing."""
    pass
```

❌ **Bad:**
```python
@pytest.fixture
def get_db():  # Verb, not noun
    pass

@pytest.fixture
def data():  # Too vague
    pass

@pytest.fixture
def fixture1():  # Non-descriptive
    pass

@pytest.fixture
def temp():  # Unclear what it provides
    pass
```

#### 3.4 Fixtures vs Helper Functions

**Rule:** Use fixtures for setup/teardown and state. Use helper functions for operations.

✅ **Good:**
```python
# Fixture for state/setup
@pytest.fixture
def user():
    """Provide a test user."""
    return User(username="test")

# Helper function for operations
def create_post(user, title, content):
    """Helper to create a post for testing."""
    return Post(author=user, title=title, content=content)

def test_user_can_create_post(user):
    """Test that user can create a post."""
    post = create_post(user, "Test Title", "Test Content")

    assert post.author == user
    assert post.title == "Test Title"
```

**When to use fixtures:**
- Setting up test data or objects
- Managing resources (database connections, file handles)
- Setup/teardown logic
- Sharing state across multiple tests

**When to use helper functions:**
- Performing operations in tests
- Reducing code duplication in test bodies
- Complex assertions
- Test data generation with many parameters

#### 3.5 autouse Fixtures

**Rule:** Use `autouse=True` sparingly, only for fixtures that should always run.

✅ **Good:**
```python
@pytest.fixture(autouse=True)
def reset_global_state():
    """Reset global application state before each test."""
    AppConfig.reset()
    Cache.clear()
    yield
    # Cleanup after test

@pytest.fixture(autouse=True, scope="session")
def configure_logging():
    """Configure logging for test session."""
    logging.basicConfig(level=logging.DEBUG)
```

❌ **Bad:**
```python
@pytest.fixture(autouse=True)
def create_test_user():
    """DON'T DO THIS - not all tests need a user."""
    return User(username="test")  # Wastes resources for tests that don't need it
```

**Use autouse when:**
- Resetting global state
- Configuring logging/warnings
- Setting up test environment variables
- Cleanup that should always happen

**Don't use autouse when:**
- Only some tests need the fixture
- The fixture is expensive to create
- It makes test dependencies unclear

#### 3.6 conftest.py Best Practices

**Rule:** Place shared fixtures in `conftest.py` at appropriate levels.

**Directory Structure:**
```
tests/
├── conftest.py              # Shared across ALL tests
├── unit/
│   ├── conftest.py          # Shared across unit tests only
│   └── test_services.py
└── integration/
    ├── conftest.py          # Shared across integration tests only
    └── test_database.py
```

**Example conftest.py:**
```python
"""Shared fixtures for all tests."""

import pytest
from myapp import create_app
from myapp.database import Database

@pytest.fixture(scope="session")
def app():
    """Provide application instance for testing."""
    app = create_app(testing=True)
    return app

@pytest.fixture
def client(app):
    """Provide test client for making HTTP requests."""
    return app.test_client()

@pytest.fixture
def database():
    """Provide clean database for testing."""
    db = Database(":memory:")
    db.create_schema()
    yield db
    db.close()

# Register custom markers
def pytest_configure(config):
    """Register custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
```

### Task 4: Apply Parametrization

**Rule:** Use `@pytest.mark.parametrize` to test multiple inputs without duplicating code.

✅ **Good:**
```python
@pytest.mark.parametrize("value,expected", [
    (0, False),
    (1, True),
    (42, True),
    (-1, True),
    (-42, True),
])
def test_is_non_zero(value, expected):
    """Test is_non_zero function with various inputs."""
    assert is_non_zero(value) == expected
```

**Multiple Parameters:**
```python
@pytest.mark.parametrize("username,email,valid", [
    ("john_doe", "john@example.com", True),
    ("", "john@example.com", False),  # Empty username
    ("john_doe", "", False),  # Empty email
    ("john_doe", "invalid-email", False),  # Invalid email format
    ("ab", "short@example.com", False),  # Username too short
])
def test_user_validation(username, email, valid):
    """Test user validation with various inputs."""
    user = User(username=username, email=email)

    if valid:
        user.validate()  # Should not raise
    else:
        with pytest.raises(ValidationError):
            user.validate()
```

**Using pytest.param for Test IDs:**
```python
@pytest.mark.parametrize("input_data,expected", [
    pytest.param(
        {"username": "john", "age": 30},
        User(username="john", age=30),
        id="valid_user"
    ),
    pytest.param(
        {"username": "", "age": 30},
        ValidationError,
        id="empty_username"
    ),
    pytest.param(
        {"username": "john", "age": -5},
        ValidationError,
        id="negative_age"
    ),
])
def test_user_creation(input_data, expected):
    """Test user creation with various inputs."""
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            User(**input_data)
    else:
        user = User(**input_data)
        assert user.username == expected.username
        assert user.age == expected.age
```

**Parametrizing Fixtures:**
```python
@pytest.fixture(params=["sqlite", "postgresql", "mysql"])
def database(request):
    """Provide different database backends for testing."""
    db_type = request.param

    if db_type == "sqlite":
        db = SQLiteDatabase(":memory:")
    elif db_type == "postgresql":
        db = PostgreSQLDatabase("localhost", "test_db")
    elif db_type == "mysql":
        db = MySQLDatabase("localhost", "test_db")

    db.create_schema()
    yield db
    db.drop_schema()
    db.close()

def test_database_insert(database):
    """Test insert works on all database backends."""
    # This test runs 3 times, once for each database type
    database.insert("users", {"username": "test"})
    assert database.count("users") == 1
```

### Task 5: Implement Mocking and Patching Best Practices

#### 5.1 When to Mock vs When Not to Mock

**Mock:**
- External services (APIs, databases, email services)
- Slow operations (file I/O, network calls)
- Non-deterministic operations (random, datetime)
- Side effects you want to verify (logging, events)

**Don't Mock:**
- Simple data structures (dictionaries, lists)
- Pure functions with no side effects
- Your own internal business logic (test it directly)
- Value objects and entities

✅ **Good (mocking external service):**
```python
def test_send_welcome_email_calls_email_service(mocker):
    """Test that user registration sends welcome email."""
    # Mock external email service
    mock_email = mocker.patch("myapp.services.EmailService.send")

    user_service = UserService()
    user = user_service.register("john@example.com")

    # Verify email service was called
    mock_email.assert_called_once_with(
        to="john@example.com",
        subject="Welcome!",
        template="welcome"
    )
```

❌ **Bad (mocking internal logic):**
```python
def test_calculate_total(mocker):
    """DON'T DO THIS - mocking the thing you're testing."""
    cart = ShoppingCart()

    # Mocking internal method defeats the purpose of testing
    mocker.patch.object(cart, "calculate_total", return_value=100.0)

    assert cart.calculate_total() == 100.0  # Pointless test
```

#### 5.2 unittest.mock Usage

**Basic Mocking:**
```python
from unittest.mock import Mock, MagicMock, patch

def test_user_service_with_mock_database():
    """Test user service with mocked database."""
    # Create a mock database
    mock_db = Mock()
    mock_db.save.return_value = True
    mock_db.get.return_value = User(id=1, username="test")

    user_service = UserService(database=mock_db)
    user = user_service.create_user("test")

    # Verify interactions
    mock_db.save.assert_called_once()
    assert user.username == "test"
```

**Using MagicMock for Magic Methods:**
```python
def test_context_manager():
    """Test code that uses context managers."""
    mock_file = MagicMock()
    mock_file.__enter__.return_value = mock_file
    mock_file.read.return_value = "test content"

    with mock_file as f:
        content = f.read()

    assert content == "test content"
    mock_file.__enter__.assert_called_once()
    mock_file.__exit__.assert_called_once()
```

#### 5.3 pytest-mock Plugin

**Preferred Approach:** Use pytest-mock's `mocker` fixture for cleaner syntax.

✅ **Good:**
```python
def test_get_user_data_from_api(mocker):
    """Test fetching user data from external API."""
    # Mock the requests.get call
    mock_get = mocker.patch("requests.get")
    mock_get.return_value.json.return_value = {
        "id": 1,
        "name": "John Doe"
    }
    mock_get.return_value.status_code = 200

    api_client = APIClient()
    user_data = api_client.get_user(user_id=1)

    # Verify API was called correctly
    mock_get.assert_called_once_with(
        "https://api.example.com/users/1",
        headers={"Authorization": "Bearer token"}
    )
    assert user_data["name"] == "John Doe"
```

**Mocking Class Methods:**
```python
def test_service_calls_repository(mocker):
    """Test that service layer calls repository correctly."""
    # Mock the repository method
    mock_find = mocker.patch("myapp.repositories.UserRepository.find_by_email")
    mock_find.return_value = User(id=1, email="test@example.com")

    service = UserService()
    user = service.get_user_by_email("test@example.com")

    mock_find.assert_called_once_with("test@example.com")
    assert user.email == "test@example.com"
```

#### 5.4 Patching Best Practices

**Rule:** Patch where the object is used, not where it's defined.

✅ **Good:**
```python
# myapp/services.py
from myapp.repositories import UserRepository

class UserService:
    def get_user(self, user_id):
        return UserRepository.find(user_id)

# tests/test_services.py
def test_get_user(mocker):
    """Patch where UserRepository is USED."""
    # Correct: patch in myapp.services where it's imported
    mock_find = mocker.patch("myapp.services.UserRepository.find")
    mock_find.return_value = User(id=1)

    service = UserService()
    user = service.get_user(1)

    assert user.id == 1
```

❌ **Bad:**
```python
def test_get_user(mocker):
    """DON'T DO THIS - patching where it's defined."""
    # Wrong: patch in myapp.repositories where it's defined
    mock_find = mocker.patch("myapp.repositories.UserRepository.find")
    # This won't work because UserService imported it before the patch
```

**Patching Built-ins:**
```python
def test_file_processing(mocker):
    """Test file processing with mocked open."""
    mock_open = mocker.patch("builtins.open", mocker.mock_open(read_data="test data"))

    processor = FileProcessor()
    content = processor.read_file("test.txt")

    mock_open.assert_called_once_with("test.txt", "r")
    assert content == "test data"
```

**Patching datetime:**
```python
from datetime import datetime

def test_timestamp_generation(mocker):
    """Test timestamp generation with frozen time."""
    # Mock datetime.now()
    mock_datetime = mocker.patch("myapp.utils.datetime")
    mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0, 0)

    timestamp = generate_timestamp()

    assert timestamp == "2024-01-01 12:00:00"
```

#### 5.5 Mock Assertions

**Rule:** Always verify that mocks were called correctly.

**Common Assertions:**
```python
def test_mock_assertions(mocker):
    """Demonstrate common mock assertions."""
    mock_service = mocker.Mock()

    # Call the mock
    mock_service.send_email("test@example.com", "Hello")
    mock_service.send_email("other@example.com", "World")

    # Verify it was called
    assert mock_service.send_email.called
    assert mock_service.send_email.call_count == 2

    # Verify specific calls
    mock_service.send_email.assert_called_with("other@example.com", "World")
    mock_service.send_email.assert_any_call("test@example.com", "Hello")

    # Verify all calls
    assert mock_service.send_email.call_args_list == [
        mocker.call("test@example.com", "Hello"),
        mocker.call("other@example.com", "World"),
    ]
```

**Verify Mock Not Called:**
```python
def test_service_does_not_send_email_for_inactive_users(mocker):
    """Test that inactive users don't receive emails."""
    mock_email = mocker.patch("myapp.services.EmailService.send")

    user_service = UserService()
    user_service.notify_user(User(is_active=False))

    # Verify email was NOT sent
    mock_email.assert_not_called()
```

**Side Effects:**
```python
def test_retry_logic_with_failures(mocker):
    """Test retry logic when API calls fail."""
    mock_api = mocker.Mock()
    # First two calls raise exception, third succeeds
    mock_api.fetch.side_effect = [
        ConnectionError("Failed"),
        ConnectionError("Failed"),
        {"status": "success"}
    ]

    client = APIClient(api=mock_api)
    result = client.fetch_with_retry(max_retries=3)

    assert result == {"status": "success"}
    assert mock_api.fetch.call_count == 3
```

### Task 6: Implement Code Coverage Best Practices

#### 6.1 Coverage Thresholds

**Recommended Thresholds:**
- **Overall project**: 80% minimum
- **New code**: 90% minimum (enforce in CI)
- **Critical paths**: 100% (authentication, payment, security)

**pytest.ini Configuration:**
```ini
[pytest]
# Run with coverage by default in CI
addopts = --cov=myapp --cov-report=html --cov-report=term --cov-fail-under=80

# Coverage options
[coverage:run]
omit =
    */tests/*
    */migrations/*
    */venv/*
    */__pycache__/*
    */site-packages/*

[coverage:report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
```

**Running Coverage:**
```bash
# Generate coverage report
pytest --cov=myapp --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html

# Fail if coverage below threshold
pytest --cov=myapp --cov-fail-under=80

# Show missing lines
pytest --cov=myapp --cov-report=term-missing
```

#### 6.2 What to Test (and What Not to Test)

**DO Test:**

✅ **Business Logic:**
```python
def calculate_discount(price, customer_tier):
    """Calculate discount based on customer tier."""
    if customer_tier == "gold":
        return price * 0.20
    elif customer_tier == "silver":
        return price * 0.10
    return 0.0

# TEST THIS - it's core business logic
def test_calculate_discount_for_gold_tier():
    assert calculate_discount(100.0, "gold") == 20.0
```

✅ **Edge Cases and Boundaries:**
```python
def test_get_user_with_nonexistent_id_raises_error():
    """Test that fetching non-existent user raises NotFound."""
    with pytest.raises(NotFoundError):
        user_service.get_user(user_id=999999)

def test_divide_by_zero_raises_error():
    """Test division by zero raises appropriate error."""
    with pytest.raises(ZeroDivisionError):
        calculator.divide(10, 0)
```

✅ **Error Handling:**
```python
def test_invalid_email_format_raises_validation_error():
    """Test that invalid email format raises ValidationError."""
    with pytest.raises(ValidationError, match="Invalid email format"):
        User(email="not-an-email")
```

✅ **Public API/Interface:**
```python
class UserService:
    def register(self, email, password):  # Public API - TEST
        """Register a new user."""
        user = self._create_user(email)  # Private - don't test directly
        self._send_welcome_email(user)  # Private - don't test directly
        return user

# Test the public method, not private helpers
def test_register_creates_user_and_sends_email(mocker):
    mock_email = mocker.patch("myapp.services.EmailService.send")

    user = user_service.register("test@example.com", "password")

    assert user.email == "test@example.com"
    mock_email.assert_called_once()
```

**DON'T Test:**

❌ **Framework/Library Code:**
```python
# DON'T test that Django's ORM works
def test_user_save():
    """DON'T DO THIS - testing Django, not your code."""
    user = User(username="test")
    user.save()
    assert User.objects.filter(username="test").exists()
```

❌ **Trivial Getters/Setters:**
```python
class User:
    @property
    def username(self):
        return self._username  # DON'T test this

    @username.setter
    def username(self, value):
        self._username = value  # DON'T test this
```

❌ **Private Implementation Details:**
```python
class Calculator:
    def add(self, a, b):
        return self._perform_addition(a, b)

    def _perform_addition(self, a, b):  # Private method
        return a + b

# DON'T test _perform_addition directly
# Test the public add() method instead
```

❌ **Generated Code:**
```python
# DON'T test auto-generated migration files, __init__.py, etc.
```

#### 6.3 Coverage Tools

**pytest-cov:**
```bash
# Install
pip install pytest-cov

# Basic usage
pytest --cov=myapp

# With HTML report
pytest --cov=myapp --cov-report=html

# Show missing lines
pytest --cov=myapp --cov-report=term-missing

# Multiple formats
pytest --cov=myapp --cov-report=html --cov-report=term --cov-report=xml
```

**Coverage.py (underlying tool):**
```bash
# Run tests with coverage
coverage run -m pytest

# Generate report
coverage report

# HTML report
coverage html

# Combine coverage from multiple runs
coverage combine
coverage report
```

**Branch Coverage:**
```ini
[coverage:run]
branch = True  # Enable branch coverage (not just line coverage)
```

```python
def example(x):
    if x > 0:  # Branch 1
        return "positive"
    else:  # Branch 2
        return "non-positive"

# Line coverage: 100% if you test with x=1
# Branch coverage: 50% - you need to test both x>0 and x<=0
```

### Task 7: Avoid Common Anti-Patterns

#### 7.1 Anti-Pattern: Testing Implementation Details

❌ **Bad:**
```python
def test_user_service_implementation_details():
    """DON'T DO THIS - testing how it works, not what it does."""
    service = UserService()

    # Testing that internal _validate method is called
    with patch.object(service, "_validate") as mock_validate:
        service.register("test@example.com")
        mock_validate.assert_called_once()
```

✅ **Good:**
```python
def test_user_service_validates_email():
    """Test the behavior: invalid emails are rejected."""
    service = UserService()

    # Test the behavior, not the implementation
    with pytest.raises(ValidationError):
        service.register("invalid-email")
```

**Why:** Implementation details change. Tests should verify behavior, not how the behavior is achieved.

#### 7.2 Anti-Pattern: Overly Complex Test Setup

❌ **Bad:**
```python
def test_complex_scenario():
    """DON'T DO THIS - setup is too complex."""
    # 50 lines of setup code
    db = Database()
    db.connect()
    db.create_tables()
    user1 = User(username="user1")
    user2 = User(username="user2")
    db.save(user1)
    db.save(user2)
    post1 = Post(author=user1, title="Post 1")
    post2 = Post(author=user2, title="Post 2")
    db.save(post1)
    db.save(post2)
    comment1 = Comment(post=post1, author=user2, text="Comment")
    db.save(comment1)
    # ... many more lines

    # Finally, the actual test
    result = service.get_posts()
    assert len(result) == 2
```

✅ **Good:**
```python
@pytest.fixture
def database_with_posts():
    """Provide database with test posts."""
    db = Database()
    db.create_schema()

    users = [User(username=f"user{i}") for i in range(2)]
    posts = [Post(author=users[i], title=f"Post {i}") for i in range(2)]

    for user in users:
        db.save(user)
    for post in posts:
        db.save(post)

    yield db
    db.close()

def test_get_posts(database_with_posts):
    """Test retrieving posts."""
    result = service.get_posts()
    assert len(result) == 2
```

**Why:** Complex setup makes tests hard to read and maintain. Use fixtures and factories.

#### 7.3 Anti-Pattern: Flaky Tests

❌ **Bad:**
```python
import time
import random

def test_flaky_timing():
    """DON'T DO THIS - test depends on timing."""
    start = time.time()
    process_data()
    duration = time.time() - start

    # Flaky: might fail on slow systems
    assert duration < 1.0

def test_flaky_random():
    """DON'T DO THIS - test uses uncontrolled randomness."""
    result = generate_random_value()
    assert result > 5  # Might fail randomly

def test_flaky_order():
    """DON'T DO THIS - test depends on iteration order."""
    users = User.objects.all()  # Order not guaranteed
    assert users[0].username == "alice"
```

✅ **Good:**
```python
def test_with_mocked_time(mocker):
    """Test with controlled time."""
    mock_time = mocker.patch("time.time")
    mock_time.side_effect = [0.0, 0.5]  # Controlled values

    start = time.time()
    process_data()
    duration = time.time() - start

    assert duration == 0.5

def test_with_seeded_random(mocker):
    """Test with controlled randomness."""
    mocker.patch("random.randint", return_value=7)

    result = generate_random_value()
    assert result == 7

def test_with_explicit_order():
    """Test with guaranteed order."""
    users = User.objects.all().order_by("username")
    assert users[0].username == "alice"
```

**Why:** Flaky tests erode trust in the test suite and waste developer time.

#### 7.4 Anti-Pattern: Too Many Assertions in One Test

❌ **Bad:**
```python
def test_user_operations():
    """DON'T DO THIS - testing multiple behaviors."""
    # Test 1: User creation
    user = User(username="test", email="test@example.com")
    assert user.username == "test"
    assert user.email == "test@example.com"

    # Test 2: User validation
    user.validate()
    assert user.is_valid is True

    # Test 3: User saving
    user.save()
    assert user.id is not None

    # Test 4: User updating
    user.username = "updated"
    user.save()
    assert user.username == "updated"

    # Test 5: User deletion
    user.delete()
    assert User.objects.filter(id=user.id).count() == 0
```

✅ **Good:**
```python
def test_user_creation():
    """Test user is created with correct attributes."""
    user = User(username="test", email="test@example.com")

    assert user.username == "test"
    assert user.email == "test@example.com"

def test_user_validation_succeeds_for_valid_data():
    """Test validation succeeds for valid user data."""
    user = User(username="test", email="test@example.com")

    user.validate()

    assert user.is_valid is True

def test_user_save_assigns_id():
    """Test saving user assigns an ID."""
    user = User(username="test", email="test@example.com")

    user.save()

    assert user.id is not None

# ... separate tests for other behaviors
```

**Guideline:** One logical assertion per test. Multiple `assert` statements are okay if they verify the same behavior.

✅ **Acceptable:**
```python
def test_user_creation_sets_all_attributes():
    """Test user creation sets all required attributes."""
    user = User(username="test", email="test@example.com", age=30)

    # Multiple assertions, but all verify the same behavior (creation)
    assert user.username == "test"
    assert user.email == "test@example.com"
    assert user.age == 30
    assert user.is_active is True  # Default value
```

#### 7.5 Anti-Pattern: Not Testing Edge Cases

❌ **Bad:**
```python
def test_divide():
    """Only tests the happy path."""
    assert divide(10, 2) == 5.0
```

✅ **Good:**
```python
def test_divide_positive_numbers():
    """Test division of positive numbers."""
    assert divide(10, 2) == 5.0

def test_divide_negative_numbers():
    """Test division with negative numbers."""
    assert divide(-10, 2) == -5.0
    assert divide(10, -2) == -5.0

def test_divide_by_zero_raises_error():
    """Test division by zero raises ZeroDivisionError."""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_divide_zero_by_number():
    """Test zero divided by number returns zero."""
    assert divide(0, 5) == 0.0

def test_divide_floats():
    """Test division with floating point numbers."""
    assert divide(10.5, 2.0) == 5.25
```

**Common Edge Cases to Test:**
- Empty collections ([], {}, "")
- None values
- Zero
- Negative numbers
- Very large numbers
- Boundary values (max/min)
- Invalid input types
- Special characters in strings

#### 7.6 Anti-Pattern: Missing Negative Test Cases

❌ **Bad:**
```python
def test_create_user():
    """Only tests successful creation."""
    user = user_service.create("test@example.com", "password123")
    assert user is not None
```

✅ **Good:**
```python
def test_create_user_with_valid_data_succeeds():
    """Test user creation succeeds with valid data."""
    user = user_service.create("test@example.com", "password123")
    assert user is not None

def test_create_user_with_invalid_email_raises_error():
    """Test user creation fails with invalid email."""
    with pytest.raises(ValidationError):
        user_service.create("invalid-email", "password123")

def test_create_user_with_short_password_raises_error():
    """Test user creation fails with short password."""
    with pytest.raises(ValidationError):
        user_service.create("test@example.com", "pass")

def test_create_user_with_duplicate_email_raises_error():
    """Test user creation fails with duplicate email."""
    user_service.create("test@example.com", "password123")

    with pytest.raises(DuplicateEmailError):
        user_service.create("test@example.com", "password456")
```

**Why:** Negative tests verify error handling and validation logic.

---

## Best Practices Summary

### 1. One Assertion Per Test (Guideline)

**Guideline:** Each test should verify one logical behavior. Multiple assert statements are acceptable if they all verify the same behavior.

✅ **Good:**
```python
def test_user_registration_creates_complete_user():
    """Test user registration creates user with all attributes."""
    user = register_user("john@example.com", "password")

    # All assertions verify the same behavior (successful registration)
    assert user.email == "john@example.com"
    assert user.is_active is True
    assert user.created_at is not None
```

### 2. Test Names That Describe the Scenario

**Pattern:** `test_<what>_<when>_<expected>`

✅ **Good:**
```python
def test_withdraw_with_insufficient_balance_raises_error():
    """Test withdrawing more than balance raises InsufficientFundsError."""
    pass

def test_login_with_valid_credentials_returns_token():
    """Test login with valid credentials returns auth token."""
    pass
```

### 3. Fast Tests

**Rule:** Unit tests should run in milliseconds, entire suite in seconds.

**Strategies:**
- Use in-memory databases (SQLite `:memory:`)
- Mock external dependencies
- Use fixtures with appropriate scopes
- Avoid unnecessary I/O operations
- Run slow tests separately (`@pytest.mark.slow`)

```python
@pytest.mark.slow
def test_full_database_migration():
    """Slow test - run separately with pytest -m slow."""
    pass

# Run fast tests only
# pytest -m "not slow"
```

### 4. Independent Tests

**Rule:** Tests must not depend on each other or on execution order.

✅ **Good:**
```python
@pytest.fixture(autouse=True)
def reset_database():
    """Reset database before each test."""
    db.clear()
    yield
    db.clear()

def test_create_user():
    """Each test starts with clean state."""
    user = create_user("test")
    assert db.count() == 1

def test_delete_user():
    """Independent of test_create_user."""
    user = create_user("test")
    delete_user(user.id)
    assert db.count() == 0
```

### 5. Repeatable Tests

**Rule:** Tests should produce the same results every time they run.

**Avoid:**
- Uncontrolled randomness
- System time dependencies
- External API calls
- Filesystem dependencies
- Network dependencies

**Use:**
- Mocked random with fixed seed
- Mocked datetime
- Mocked external services
- Temporary directories/files
- In-memory resources

### 6. Self-Validating Tests

**Rule:** Tests should clearly pass or fail without human interpretation.

✅ **Good:**
```python
def test_calculate_total():
    """Test clearly passes or fails."""
    total = calculate_total([10, 20, 30])
    assert total == 60  # Clear pass/fail
```

❌ **Bad:**
```python
def test_calculate_total():
    """Requires human to interpret output."""
    total = calculate_total([10, 20, 30])
    print(f"Total: {total}")  # No assertion - requires manual check
```

---

## Examples

### Example 1: Complete Test File

**File: `tests/unit/test_user_service.py`**

```python
"""Tests for user service."""

import pytest
from myapp.models import User
from myapp.services import UserService
from myapp.exceptions import ValidationError, DuplicateEmailError


@pytest.fixture
def user_service():
    """Provide user service instance."""
    return UserService()


@pytest.fixture
def sample_user_data():
    """Provide sample valid user data."""
    return {
        "email": "john@example.com",
        "password": "SecurePass123!",
        "username": "john_doe"
    }


class TestUserRegistration:
    """Tests for user registration functionality."""

    def test_register_with_valid_data_creates_user(self, user_service, sample_user_data):
        """Test that registration with valid data creates a user."""
        # Arrange
        # (data provided by fixture)

        # Act
        user = user_service.register(**sample_user_data)

        # Assert
        assert user.email == sample_user_data["email"]
        assert user.username == sample_user_data["username"]
        assert user.id is not None
        assert user.is_active is True

    def test_register_with_invalid_email_raises_error(self, user_service):
        """Test that invalid email raises ValidationError."""
        # Arrange
        invalid_data = {
            "email": "not-an-email",
            "password": "SecurePass123!",
            "username": "john_doe"
        }

        # Act & Assert
        with pytest.raises(ValidationError, match="Invalid email format"):
            user_service.register(**invalid_data)

    def test_register_with_duplicate_email_raises_error(self, user_service, sample_user_data):
        """Test that duplicate email raises DuplicateEmailError."""
        # Arrange
        user_service.register(**sample_user_data)

        # Act & Assert
        with pytest.raises(DuplicateEmailError):
            user_service.register(**sample_user_data)

    @pytest.mark.parametrize("password,should_fail", [
        ("short", True),  # Too short
        ("nodigits!", True),  # No digits
        ("NoSpecialChar1", True),  # No special char
        ("Valid1Pass!", False),  # Valid
        ("AnotherGood2@", False),  # Valid
    ])
    def test_register_password_validation(self, user_service, password, should_fail):
        """Test password validation with various inputs."""
        # Arrange
        user_data = {
            "email": "test@example.com",
            "password": password,
            "username": "testuser"
        }

        # Act & Assert
        if should_fail:
            with pytest.raises(ValidationError):
                user_service.register(**user_data)
        else:
            user = user_service.register(**user_data)
            assert user is not None


class TestUserAuthentication:
    """Tests for user authentication functionality."""

    @pytest.fixture
    def registered_user(self, user_service, sample_user_data):
        """Provide a registered user for testing."""
        return user_service.register(**sample_user_data)

    def test_login_with_valid_credentials_returns_token(
        self, user_service, registered_user, sample_user_data
    ):
        """Test that valid credentials return an auth token."""
        # Arrange
        email = sample_user_data["email"]
        password = sample_user_data["password"]

        # Act
        token = user_service.login(email, password)

        # Assert
        assert token is not None
        assert isinstance(token, str)
        assert len(token) > 0

    def test_login_with_invalid_password_raises_error(
        self, user_service, registered_user, sample_user_data
    ):
        """Test that invalid password raises AuthenticationError."""
        # Arrange
        email = sample_user_data["email"]
        wrong_password = "WrongPassword123!"

        # Act & Assert
        with pytest.raises(AuthenticationError):
            user_service.login(email, wrong_password)

    def test_login_with_nonexistent_user_raises_error(self, user_service):
        """Test that non-existent user raises AuthenticationError."""
        # Arrange
        email = "nonexistent@example.com"
        password = "Password123!"

        # Act & Assert
        with pytest.raises(AuthenticationError):
            user_service.login(email, password)


class TestUserEmailNotification:
    """Tests for user email notification functionality."""

    def test_register_sends_welcome_email(self, user_service, sample_user_data, mocker):
        """Test that registration sends welcome email."""
        # Arrange
        mock_email = mocker.patch("myapp.services.EmailService.send")

        # Act
        user = user_service.register(**sample_user_data)

        # Assert
        mock_email.assert_called_once_with(
            to=sample_user_data["email"],
            subject="Welcome to MyApp!",
            template="welcome",
            context={"username": user.username}
        )

    def test_register_does_not_send_email_on_failure(
        self, user_service, sample_user_data, mocker
    ):
        """Test that failed registration does not send email."""
        # Arrange
        mock_email = mocker.patch("myapp.services.EmailService.send")
        invalid_data = {**sample_user_data, "email": "invalid-email"}

        # Act
        with pytest.raises(ValidationError):
            user_service.register(**invalid_data)

        # Assert
        mock_email.assert_not_called()
```

### Example 2: Testing with Fixtures and Factories

```python
"""Example using fixtures and factories for test data."""

import pytest
from myapp.models import User, Post, Comment


@pytest.fixture
def user_factory(db):
    """Provide factory for creating test users."""
    created_users = []

    def _create_user(**kwargs):
        defaults = {
            "username": f"user_{len(created_users)}",
            "email": f"user{len(created_users)}@example.com",
            "is_active": True
        }
        defaults.update(kwargs)
        user = User(**defaults)
        db.save(user)
        created_users.append(user)
        return user

    yield _create_user

    # Cleanup
    for user in created_users:
        db.delete(user)


@pytest.fixture
def post_factory(db, user_factory):
    """Provide factory for creating test posts."""
    created_posts = []

    def _create_post(**kwargs):
        if "author" not in kwargs:
            kwargs["author"] = user_factory()

        defaults = {
            "title": f"Post {len(created_posts)}",
            "content": "Test content"
        }
        defaults.update(kwargs)
        post = Post(**defaults)
        db.save(post)
        created_posts.append(post)
        return post

    yield _create_post

    # Cleanup
    for post in created_posts:
        db.delete(post)


def test_user_can_create_multiple_posts(user_factory, post_factory):
    """Test that user can create multiple posts."""
    # Arrange
    user = user_factory(username="author")

    # Act
    post1 = post_factory(author=user, title="First Post")
    post2 = post_factory(author=user, title="Second Post")

    # Assert
    assert post1.author == user
    assert post2.author == user
    assert user.posts.count() == 2


def test_post_without_author_creates_default_user(post_factory):
    """Test that post without author gets default user."""
    # Act
    post = post_factory(title="Test Post")

    # Assert
    assert post.author is not None
    assert post.author.username.startswith("user_")
```

### Example 3: Integration Test with Database

```python
"""Integration tests with real database."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myapp.models import Base, User
from myapp.repositories import UserRepository


@pytest.fixture(scope="module")
def engine():
    """Create in-memory SQLite engine for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture
def db_session(engine):
    """Provide database session with transaction rollback."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def user_repository(db_session):
    """Provide user repository instance."""
    return UserRepository(session=db_session)


def test_create_user_persists_to_database(user_repository):
    """Test that created user is persisted to database."""
    # Arrange
    user_data = {
        "username": "testuser",
        "email": "test@example.com"
    }

    # Act
    user = user_repository.create(**user_data)
    retrieved_user = user_repository.find_by_id(user.id)

    # Assert
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.email == "test@example.com"


def test_find_by_email_returns_correct_user(user_repository):
    """Test finding user by email returns correct user."""
    # Arrange
    user1 = user_repository.create(username="user1", email="user1@example.com")
    user2 = user_repository.create(username="user2", email="user2@example.com")

    # Act
    found_user = user_repository.find_by_email("user2@example.com")

    # Assert
    assert found_user is not None
    assert found_user.id == user2.id
    assert found_user.username == "user2"
```

---

## Templates

### Template 1: Basic Unit Test

Located at: `templates/unit_test_template.py`

**Purpose:** Template for basic unit tests using AAA pattern.

**Usage:**
1. Copy template to `tests/unit/test_[module_name].py`
2. Replace `[MODULE_NAME]` with actual module name
3. Replace `[function/class]` with code under test
4. Add test cases following the pattern

See: `/Users/clo/developer/gh-clostaunau/holiday-card/.claude/skills/python-testing-standards/templates/unit_test_template.py`

### Template 2: Integration Test with Database

Located at: `templates/integration_test_template.py`

**Purpose:** Template for integration tests with database fixtures.

**Usage:**
1. Copy template to `tests/integration/test_[feature_name].py`
2. Configure database engine for your database
3. Add test cases using `db_session` fixture

See: `/Users/clo/developer/gh-clostaunau/holiday-card/.claude/skills/python-testing-standards/templates/integration_test_template.py`

### Template 3: Test with Mocking

Located at: `templates/mock_test_template.py`

**Purpose:** Template for tests using mocks and patches.

**Usage:**
1. Copy template to appropriate test directory
2. Replace mock targets with actual dependencies
3. Add verification assertions

See: `/Users/clo/developer/gh-clostaunau/holiday-card/.claude/skills/python-testing-standards/templates/mock_test_template.py`

---

## Decision Trees

### When to Mock vs Test Real Implementation

```
Is the dependency external (API, database, file system)?
├─ Yes → Mock it
│   └─ Example: mock requests.get(), EmailService.send()
└─ No → Is it slow (>100ms)?
    ├─ Yes → Mock it
    │   └─ Example: mock expensive computations, large file processing
    └─ No → Is it non-deterministic (random, time)?
        ├─ Yes → Mock it
        │   └─ Example: mock datetime.now(), random.randint()
        └─ No → Is it your internal business logic?
            ├─ Yes → Test it directly (don't mock)
            │   └─ Example: test calculation functions, validators
            └─ No → Is it a framework/library?
                ├─ Yes → Don't test it (trust the framework)
                └─ No → Consider mocking if needed for isolation
```

### Choosing Fixture Scope

```
Does the fixture need to be fresh for each test?
├─ Yes → Use scope="function" (default)
│   └─ Example: test data, mutable objects
└─ No → Is the fixture expensive to create?
    ├─ Yes → Is it stateless/read-only?
    │   ├─ Yes → Use scope="module" or "session"
    │   │   └─ Example: database connection, API client
    │   └─ No → Use scope="function" with cleanup
    │       └─ Example: database with data
    └─ No → Use scope="function" for simplicity
```

### Test Organization Strategy

```
What are you testing?
├─ Single function/method with no dependencies
│   └─ Use standalone test function
│       └─ Example: def test_calculate_sum()
├─ Multiple related functions/methods
│   └─ Use test class for grouping
│       └─ Example: class TestUserAuthentication
├─ Tests sharing setup/teardown
│   └─ Use test class with fixtures
│       └─ Example: class TestDatabaseOperations with setup fixtures
└─ Different test types (unit/integration/e2e)
    └─ Use separate directories
        └─ Example: tests/unit/, tests/integration/, tests/e2e/
```

---

## Common Pitfalls

### Pitfall 1: Mocking Too Much

**Problem:** Over-mocking makes tests brittle and defeats the purpose of testing.

**Why it happens:** Desire for fast tests or lack of understanding of what to mock.

**How to avoid:**
- Only mock external dependencies and slow operations
- Test real implementation of your business logic
- Use integration tests for testing components together

**Example:**

❌ **Bad:**
```python
def test_user_service_register(mocker):
    """Over-mocked test that doesn't test anything real."""
    mock_user = mocker.Mock()
    mock_validator = mocker.patch("myapp.validators.EmailValidator")
    mock_hasher = mocker.patch("myapp.security.hash_password")
    mock_repo = mocker.patch("myapp.repositories.UserRepository")

    # This test doesn't test any real code!
    service = UserService()
    service.register("test@example.com", "password")

    mock_validator.validate.assert_called_once()
    mock_hasher.assert_called_once()
    mock_repo.save.assert_called_once()
```

✅ **Good:**
```python
def test_user_service_register(mocker):
    """Test real logic, mock only external dependencies."""
    # Only mock external dependencies (database, email)
    mock_email = mocker.patch("myapp.services.EmailService.send")

    # Test real validation, hashing, and service logic
    service = UserService()
    user = service.register("test@example.com", "SecurePass123!")

    # Verify real behavior
    assert user.email == "test@example.com"
    assert user.password_hash != "SecurePass123!"  # Password was hashed
    mock_email.assert_called_once()  # Email was sent
```

### Pitfall 2: Testing Private Methods

**Problem:** Tests are coupled to implementation details and break on refactoring.

**Why it happens:** Misconception that 100% coverage requires testing private methods.

**How to avoid:**
- Test public API/interface only
- Private methods are tested indirectly through public methods
- If a private method seems complex enough to test directly, it might deserve to be a separate class

**Example:**

❌ **Bad:**
```python
class UserService:
    def register(self, email, password):
        self._validate_email(email)
        self._validate_password(password)
        return self._create_user(email, password)

    def _validate_email(self, email):
        # Private validation logic
        pass

    def _create_user(self, email, password):
        # Private creation logic
        pass

# DON'T DO THIS
def test_validate_email():
    """Testing private method directly."""
    service = UserService()
    service._validate_email("test@example.com")  # Bad!
```

✅ **Good:**
```python
# Test the public API
def test_register_with_invalid_email_raises_error():
    """Test registration validates email (tests _validate_email indirectly)."""
    service = UserService()

    with pytest.raises(ValidationError):
        service.register("invalid-email", "SecurePass123!")

def test_register_with_valid_data_creates_user():
    """Test registration creates user (tests _create_user indirectly)."""
    service = UserService()

    user = service.register("test@example.com", "SecurePass123!")

    assert user.email == "test@example.com"
```

### Pitfall 3: Shared State Between Tests

**Problem:** Tests fail or pass depending on execution order.

**Why it happens:** Using module-level or class-level mutable state without proper cleanup.

**How to avoid:**
- Use fixtures with proper scope
- Clean up state in fixtures (use yield for teardown)
- Avoid module-level globals
- Use `autouse=True` fixtures for necessary cleanup

**Example:**

❌ **Bad:**
```python
# Module-level shared state
_test_users = []

def test_create_user():
    """Test depends on _test_users being empty."""
    user = User(username="test")
    _test_users.append(user)
    assert len(_test_users) == 1  # Fails if other tests ran first!

def test_delete_user():
    """Test depends on test_create_user."""
    _test_users.pop()
    assert len(_test_users) == 0
```

✅ **Good:**
```python
@pytest.fixture
def user_list():
    """Provide fresh list for each test."""
    users = []
    yield users
    users.clear()  # Cleanup (though not needed with function scope)

def test_create_user(user_list):
    """Test with isolated state."""
    user = User(username="test")
    user_list.append(user)
    assert len(user_list) == 1

def test_delete_user(user_list):
    """Test with isolated state."""
    user = User(username="test")
    user_list.append(user)
    user_list.pop()
    assert len(user_list) == 0
```

### Pitfall 4: Not Cleaning Up Resources

**Problem:** Tests leave behind files, database records, or open connections.

**Why it happens:** Forgetting to add cleanup code or not using fixtures properly.

**How to avoid:**
- Use fixtures with yield for setup/teardown
- Use context managers
- Use temp directories for file tests
- Use transaction rollback for database tests

**Example:**

❌ **Bad:**
```python
def test_file_processing():
    """Test leaves file behind."""
    with open("test_file.txt", "w") as f:
        f.write("test data")

    result = process_file("test_file.txt")
    assert result == "processed"
    # File left behind!
```

✅ **Good:**
```python
import tempfile
import os

@pytest.fixture
def test_file():
    """Provide temporary test file."""
    fd, path = tempfile.mkstemp(suffix=".txt")

    # Write test data
    with os.fdopen(fd, "w") as f:
        f.write("test data")

    yield path

    # Cleanup
    if os.path.exists(path):
        os.remove(path)

def test_file_processing(test_file):
    """Test with automatic cleanup."""
    result = process_file(test_file)
    assert result == "processed"
    # File automatically cleaned up
```

### Pitfall 5: Unclear Test Failure Messages

**Problem:** When test fails, it's not clear what went wrong.

**Why it happens:** Using bare assertions without context or descriptive messages.

**How to avoid:**
- Use descriptive test names
- Add assertion messages for complex checks
- Use pytest's assertion rewriting (automatic for simple assertions)
- Use `pytest.raises()` with `match` parameter

**Example:**

❌ **Bad:**
```python
def test_user():
    """Vague test name."""
    u = User("test@example.com")
    assert u.email == "test@example.org"  # Failure message unclear
```

When this fails:
```
assert 'test@example.com' == 'test@example.org'
```

✅ **Good:**
```python
def test_user_email_is_stored_correctly():
    """Descriptive test name explains what's being tested."""
    # Arrange
    email = "test@example.com"

    # Act
    user = User(email)

    # Assert
    assert user.email == email, f"Expected user email to be {email}, got {user.email}"
```

When this fails:
```
AssertionError: Expected user email to be test@example.com, got test@example.org
```

**For Exceptions:**

✅ **Good:**
```python
def test_invalid_email_raises_validation_error():
    """Test that invalid email raises ValidationError with helpful message."""
    with pytest.raises(ValidationError, match="Invalid email format"):
        User("not-an-email")
```

---

## Checklist

Use this checklist during code reviews to verify test quality:

### Test File Organization
- [ ] Test files named `test_*.py` or `*_test.py`
- [ ] Tests organized in logical directories (`unit/`, `integration/`, `e2e/`)
- [ ] Shared fixtures in `conftest.py` at appropriate levels
- [ ] One test file per module/class being tested

### Test Function/Class Naming
- [ ] Test functions start with `test_`
- [ ] Test classes start with `Test`
- [ ] Names describe the scenario: `test_<what>_<when>_<expected>`
- [ ] Names are clear and self-documenting

### Test Structure
- [ ] Tests follow AAA or Given-When-Then pattern
- [ ] Clear separation between Arrange, Act, Assert
- [ ] Each test verifies one logical behavior
- [ ] Tests are independent and can run in any order

### Fixtures
- [ ] Appropriate fixture scope selected (function/class/module/session)
- [ ] Fixtures have descriptive names
- [ ] Fixtures clean up resources (using yield)
- [ ] Fixture dependencies are logical and clear
- [ ] `autouse` only used when necessary

### Mocking and Patching
- [ ] Only external dependencies are mocked
- [ ] Internal business logic is tested directly
- [ ] Patches target where object is used, not where it's defined
- [ ] Mock assertions verify expected behavior
- [ ] Mocks are reset between tests (automatic with mocker fixture)

### Test Coverage
- [ ] Critical paths have 100% coverage
- [ ] Overall coverage meets project threshold (80%+)
- [ ] Coverage report excludes irrelevant files (migrations, etc.)
- [ ] Business logic is thoroughly tested
- [ ] Edge cases are covered

### Assertions
- [ ] Tests have at least one assertion
- [ ] Assertions are specific and meaningful
- [ ] Exception tests use `pytest.raises()`
- [ ] Assertion messages provided for complex checks
- [ ] No bare `assert` without verification

### Test Quality
- [ ] No testing of implementation details
- [ ] No overly complex test setup
- [ ] Tests are not flaky (deterministic)
- [ ] Edge cases are tested
- [ ] Negative test cases are included
- [ ] Tests are fast (unit tests < 100ms)

### Parametrization
- [ ] `@pytest.mark.parametrize` used for multiple similar test cases
- [ ] Test IDs provided for clarity (using `pytest.param`)
- [ ] Parametrized tests cover full range of inputs

### Code Quality
- [ ] Tests follow PEP 8 style guide
- [ ] Tests have docstrings describing what they test
- [ ] No code duplication (use fixtures/helpers)
- [ ] Imports are organized and minimal
- [ ] No commented-out code

### Documentation
- [ ] README explains how to run tests
- [ ] Complex test scenarios are documented
- [ ] Custom markers are registered and documented
- [ ] Fixture purposes are clear from docstrings

---

## Tools and Commands

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_user_service.py

# Run specific test function
pytest tests/unit/test_user_service.py::test_register_with_valid_data

# Run specific test class
pytest tests/unit/test_user_service.py::TestUserRegistration

# Run tests matching pattern
pytest -k "registration"

# Run tests with specific marker
pytest -m "slow"

# Run tests excluding marker
pytest -m "not slow"

# Verbose output
pytest -v

# Show print statements
pytest -s

# Stop after first failure
pytest -x

# Run last failed tests only
pytest --lf

# Run failed tests first, then rest
pytest --ff

# Show slowest tests
pytest --durations=10
```

### Coverage Commands

```bash
# Run with coverage
pytest --cov=myapp

# HTML report
pytest --cov=myapp --cov-report=html

# Terminal report with missing lines
pytest --cov=myapp --cov-report=term-missing

# XML report (for CI)
pytest --cov=myapp --cov-report=xml

# Fail if coverage below threshold
pytest --cov=myapp --cov-fail-under=80

# Multiple reports
pytest --cov=myapp --cov-report=html --cov-report=term --cov-report=xml
```

### Pytest Configuration

**pytest.ini:**
```ini
[pytest]
# Test discovery patterns
python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

# Default options
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=myapp
    --cov-report=term-missing
    --cov-fail-under=80

# Test paths
testpaths = tests

# Markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
    e2e: marks tests as end-to-end tests

# Coverage options
[coverage:run]
source = myapp
omit =
    */tests/*
    */migrations/*
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
    @abstractmethod
```

### Useful Pytest Plugins

```bash
# Install common plugins
pip install pytest-cov          # Coverage integration
pip install pytest-mock         # Mocking integration
pip install pytest-xdist        # Parallel test execution
pip install pytest-django       # Django integration
pip install pytest-asyncio      # Async test support
pip install pytest-timeout      # Test timeouts
pip install pytest-benchmark    # Performance benchmarking

# Run tests in parallel
pytest -n auto  # Uses all CPU cores
pytest -n 4     # Uses 4 workers

# Set test timeout
pytest --timeout=10  # 10 seconds per test
```

---

## Related Skills

- **uncle-duke-python**: Python code review agent that uses this skill as reference
- **agent-skill-templates**: Templates for creating new skills

---

## References

### Official Documentation
- [pytest Documentation](https://docs.pytest.org/)
- [unittest.mock Documentation](https://docs.python.org/3/library/unittest.mock.html)
- [pytest-cov Documentation](https://pytest-cov.readthedocs.io/)
- [pytest-mock Documentation](https://pytest-mock.readthedocs.io/)

### Best Practices Guides
- [Effective Python Testing with pytest (Book)](https://pragprog.com/titles/bopytest/python-testing-with-pytest/)
- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [AAA Pattern](https://wiki.c2.com/?ArrangeActAssert)
- [Given-When-Then](https://martinfowler.com/bliki/GivenWhenThen.html)

### PEPs Referenced
- [PEP 8 - Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 20 - The Zen of Python](https://peps.python.org/pep-0020/)
- [PEP 484 - Type Hints](https://peps.python.org/pep-0484/)

---

**Version:** 1.0
**Last Updated:** 2025-12-24
**Maintainer:** Development Team
