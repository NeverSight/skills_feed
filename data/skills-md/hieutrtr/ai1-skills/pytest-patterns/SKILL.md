---
name: pytest-patterns
description: >-
  Python backend testing patterns with pytest for FastAPI applications. Use when writing
  Python tests: unit tests for services and repositories, integration tests for API
  endpoints with httpx.AsyncClient, fixture creation, factory setup with factory_boy,
  async testing with pytest-asyncio, mocking strategies, and parametrized tests.
  Covers test organization (tests/unit, tests/integration), conftest hierarchy, and
  coverage requirements. Does NOT cover frontend tests (use react-testing-patterns)
  or E2E browser tests (use e2e-testing).
license: MIT
compatibility: 'Python 3.12+, pytest 8+, pytest-asyncio, httpx, factory_boy'
metadata:
  author: platform-team
  version: '1.0.0'
  sdlc-phase: testing
allowed-tools: Read Edit Write Bash(pytest:*) Bash(python:*)
context: fork
---

# Pytest Patterns

## When to Use

Activate this skill when:
- Writing unit tests for service or repository classes
- Writing integration tests for FastAPI endpoints with httpx.AsyncClient
- Creating or refactoring pytest fixtures and conftest files
- Setting up factory_boy factories for test data
- Testing async code with pytest-asyncio
- Mocking external services (HTTP APIs, email, queues)
- Adding parametrized tests for input variations
- Auditing or improving test coverage

Do NOT use this skill for:
- Frontend React component or hook tests (use `react-testing-patterns`)
- E2E browser tests with Playwright (use `e2e-testing`)
- TDD red-green-refactor workflow enforcement (use `tdd-workflow`)
- Writing application code (use `python-backend-expert`)

## Instructions

### Test Organization

```
tests/
├── conftest.py              # Root conftest: DB session, async client, auth helpers
├── unit/
│   ├── conftest.py          # Unit-specific fixtures (mocked repos, services)
│   ├── services/
│   │   ├── test_user_service.py
│   │   └── test_order_service.py
│   └── repositories/
│       └── test_user_repository.py
├── integration/
│   ├── conftest.py          # Integration-specific fixtures (test DB, seeding)
│   ├── test_users_api.py
│   └── test_orders_api.py
└── factories/
    ├── __init__.py
    ├── user_factory.py
    └── order_factory.py
```

**Naming conventions:**
- Test files: `test_<module>.py`
- Test classes: `Test<Feature>` (group related tests, no `__init__`)
- Test functions: `test_<action>_<expected_outcome>` or `test_<scenario>`
- Fixtures: descriptive noun (`db_session`, `authenticated_client`, `sample_user`)

**Marker conventions:**
```python
# pyproject.toml
[tool.pytest.ini_options]
markers = [
    "unit: Unit tests (no DB, no network)",
    "integration: Integration tests (real DB, real HTTP)",
    "slow: Tests that take > 1 second",
]
asyncio_mode = "auto"
```

Run subsets: `pytest -m unit`, `pytest -m integration`, `pytest -m "not slow"`.

### Fixture Architecture

#### Conftest Hierarchy

Fixtures cascade: root `conftest.py` provides shared fixtures; subdirectory conftest files add layer-specific fixtures.

**Root conftest (tests/conftest.py):**
```python
import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.main import app
from app.database import get_db

@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"

@pytest.fixture(scope="session")
async def engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def db_session(engine):
    async with async_sessionmaker(engine, class_=AsyncSession)() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db_session):
    async def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

#### Fixture Scopes

| Scope | Use For | Example |
|-------|---------|---------|
| `function` (default) | Isolated per-test data | `db_session`, `sample_user` |
| `class` | Shared across test class | `service_instance` |
| `module` | Shared across test file | `seeded_database` |
| `session` | Shared across entire run | `engine`, `anyio_backend` |

**Rules:**
- Default to `function` scope for data isolation
- Use `session` scope only for expensive, stateless resources (engine, event loop)
- Never use `session` scope for mutable data -- tests will interfere with each other
- Fixtures that yield must clean up (rollback, delete, close)

#### Auth Fixtures

```python
@pytest.fixture
def auth_headers():
    """Return authorization headers for a standard test user."""
    token = create_test_token(user_id=1, role="member")
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
async def authenticated_client(client, auth_headers):
    """AsyncClient pre-configured with auth headers."""
    client.headers.update(auth_headers)
    return client

@pytest.fixture
def admin_headers():
    """Return authorization headers for an admin user."""
    token = create_test_token(user_id=99, role="admin")
    return {"Authorization": f"Bearer {token}"}
```

### Factory Pattern

Use `factory_boy` for consistent, overridable test data.

```python
import factory
from app.models import User, Order

class UserFactory(factory.Factory):
    class Meta:
        model = User

    id = factory.Sequence(lambda n: n + 1)
    email = factory.LazyAttribute(lambda o: f"user{o.id}@example.com")
    display_name = factory.Faker("name")
    role = "member"
    is_active = True

class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    id = factory.Sequence(lambda n: n + 1)
    user_id = factory.LazyAttribute(lambda o: UserFactory().id)
    total_cents = factory.Faker("random_int", min=100, max=100000)
    status = "pending"
```

**Usage in tests:**
```python
def test_user_defaults():
    user = UserFactory()
    assert user.is_active is True
    assert user.role == "member"

def test_user_override():
    admin = UserFactory(role="admin", display_name="Admin User")
    assert admin.role == "admin"

def test_user_batch():
    users = UserFactory.build_batch(5)
    assert len(users) == 5
```

**SQLAlchemy integration** (for integration tests that persist to DB):
```python
class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = None  # Set per-test via conftest

    # ... fields same as above
```

Set session in conftest:
```python
@pytest.fixture(autouse=True)
def set_factory_session(db_session):
    UserFactory._meta.sqlalchemy_session = db_session
    OrderFactory._meta.sqlalchemy_session = db_session
```

### API Integration Tests

Test FastAPI endpoints with `httpx.AsyncClient` against the real app, but with a test database.

```python
import pytest
from httpx import AsyncClient

class TestUsersAPI:
    """Integration tests for /api/v1/users endpoints."""

    async def test_create_user_success(self, authenticated_client: AsyncClient):
        response = await authenticated_client.post("/api/v1/users", json={
            "email": "new@example.com",
            "display_name": "New User",
        })
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert "id" in data

    async def test_create_user_duplicate_email(self, authenticated_client, sample_user):
        response = await authenticated_client.post("/api/v1/users", json={
            "email": sample_user.email,
            "display_name": "Duplicate",
        })
        assert response.status_code == 409
        assert "already exists" in response.json()["detail"]

    async def test_list_users_pagination(self, authenticated_client):
        response = await authenticated_client.get("/api/v1/users?limit=10&cursor=0")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "next_cursor" in data

    async def test_get_user_not_found(self, authenticated_client):
        response = await authenticated_client.get("/api/v1/users/99999")
        assert response.status_code == 404

    async def test_unauthenticated_request(self, client):
        response = await client.get("/api/v1/users")
        assert response.status_code == 401
```

**Key patterns:**
- Use `authenticated_client` for protected endpoints, plain `client` for auth testing
- Assert status code first, then response body
- Test error paths: 404, 409, 422, 401, 403
- Test pagination parameters
- Never assert on exact timestamps or auto-generated IDs (use `"id" in data`)

### Async Tests

With `asyncio_mode = "auto"` in pyproject.toml, all `async def test_*` functions run automatically.

```python
async def test_async_service_call(db_session):
    service = UserService(db_session)
    user = await service.create_user(email="test@example.com", display_name="Test")
    assert user.id is not None

async def test_concurrent_operations(db_session):
    service = UserService(db_session)
    import asyncio
    results = await asyncio.gather(
        service.get_user(1),
        service.get_user(2),
        service.get_user(3),
    )
    assert len(results) == 3
```

**Common pitfalls:**
- Do NOT mix `sync` and `async` fixtures carelessly -- an async fixture can only be used by async tests
- Always use `pytest-asyncio` (not `anyio` directly) for consistency
- If a test hangs, check for un-awaited coroutines or missing `async` keywords

### Mocking Strategy

**Mock external services -- YES:**
```python
from unittest.mock import AsyncMock, patch

async def test_send_notification(db_session):
    with patch("app.services.notification.EmailClient") as mock_email:
        mock_email.return_value.send = AsyncMock(return_value=True)
        service = NotificationService(db_session)
        result = await service.notify_user(user_id=1, message="Hello")
        assert result is True
        mock_email.return_value.send.assert_called_once()
```

**Mock the database -- NO:**
```python
# BAD: Mocking the database hides real query issues
async def test_user_service(mock_db):
    mock_db.execute.return_value = MockResult([user_dict])  # Don't do this

# GOOD: Use a real test database (SQLite or PostgreSQL in Docker)
async def test_user_service(db_session):
    service = UserService(db_session)
    user = await service.create_user(email="test@example.com", display_name="Test")
    fetched = await service.get_user(user.id)
    assert fetched.email == "test@example.com"
```

**What to mock:**
| Mock | Do Not Mock |
|------|-------------|
| HTTP APIs (use `respx` or `unittest.mock`) | Database queries |
| Email/SMS services | SQLAlchemy sessions |
| File storage (S3, GCS) | Repository methods (in integration tests) |
| Message queues (Redis, RabbitMQ) | Pydantic validation |
| Time/datetime (`freezegun`) | FastAPI dependency injection |
| Random/UUID generation | ORM relationships |

**`respx` for HTTP mocking:**
```python
import respx
from httpx import Response

@respx.mock
async def test_external_api_call():
    respx.get("https://api.example.com/data").mock(
        return_value=Response(200, json={"key": "value"})
    )
    service = ExternalDataService()
    result = await service.fetch_data()
    assert result["key"] == "value"
```

### Parametrized Tests

Use `@pytest.mark.parametrize` for testing multiple input/output combinations:

```python
@pytest.mark.parametrize("email,is_valid", [
    ("user@example.com", True),
    ("user@sub.domain.com", True),
    ("user+tag@example.com", True),
    ("", False),
    ("not-an-email", False),
    ("@missing-local.com", False),
    ("user@", False),
])
def test_email_validation(email, is_valid):
    if is_valid:
        assert validate_email(email) is True
    else:
        with pytest.raises(ValidationError):
            validate_email(email)
```

**Parametrize with IDs for readable output:**
```python
@pytest.mark.parametrize("status,expected_code", [
    pytest.param("active", 200, id="active-user-ok"),
    pytest.param("suspended", 403, id="suspended-user-forbidden"),
    pytest.param("deleted", 404, id="deleted-user-not-found"),
])
async def test_user_access_by_status(authenticated_client, status, expected_code):
    ...
```

**Parametrize multiple fixtures:**
```python
@pytest.mark.parametrize("role,can_delete", [
    ("admin", True),
    ("member", False),
    ("viewer", False),
])
async def test_delete_permission(client, role, can_delete):
    headers = {"Authorization": f"Bearer {create_test_token(role=role)}"}
    response = await client.delete("/api/v1/users/1", headers=headers)
    if can_delete:
        assert response.status_code == 204
    else:
        assert response.status_code == 403
```

### Coverage Requirements

**Minimum thresholds:**
- Overall: 80% line coverage
- Service layer: 90% (critical business logic)
- Repository layer: 70% (straightforward CRUD)
- Routes: 80% (all success + primary error paths)

**pyproject.toml configuration:**
```toml
[tool.coverage.run]
source = ["app"]
omit = ["app/migrations/*", "app/main.py", "app/__init__.py"]

[tool.coverage.report]
fail_under = 80
show_missing = true
exclude_lines = [
    "pragma: no cover",
    "if TYPE_CHECKING:",
    "if __name__ ==",
    "@overload",
]
```

**Running coverage:**
```bash
pytest --cov=app --cov-report=term-missing --cov-report=html --cov-fail-under=80
```

Use `scripts/check-test-coverage.sh` to automate coverage checks with report output.

### Test Anti-Patterns

**1. Testing implementation details:**
```python
# BAD: Tests internal method calls
def test_service_calls_repo(mock_repo):
    service.create_user(data)
    mock_repo.insert.assert_called_once_with(...)

# GOOD: Tests observable behavior
async def test_create_user(db_session):
    service = UserService(db_session)
    user = await service.create_user(email="a@b.com", display_name="A")
    fetched = await service.get_user(user.id)
    assert fetched is not None
```

**2. Shared mutable state between tests:**
```python
# BAD: Module-level mutable data
users = []

def test_add_user():
    users.append(User(id=1))  # Leaks to other tests

# GOOD: Use fixtures with function scope
@pytest.fixture
def users():
    return [UserFactory()]
```

**3. Overly broad assertions:**
```python
# BAD
assert response.status_code == 200  # Only checks status

# GOOD
assert response.status_code == 200
data = response.json()
assert data["email"] == "test@example.com"
assert data["role"] == "member"
```

**4. Missing error path tests:**
Every endpoint should have tests for at least: success, not found, validation error, and unauthorized.

## Examples

See `references/conftest-template.py` for production conftest setup.
See `references/factory-template.py` for factory_boy patterns.
See `references/api-test-template.py` for API integration test patterns.
See `references/service-test-template.py` for service unit test patterns.
See `references/integration-test-template.py` for full integration test patterns.
