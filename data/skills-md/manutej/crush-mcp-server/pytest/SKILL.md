---
name: pytest
version: 2.0.0
description: Advanced Python unit testing framework for customer support tech enablement, covering FastAPI, SQLAlchemy, PostgreSQL, async operations, mocking, fixtures, parametrization, coverage, and comprehensive testing strategies for backend support systems
tags:
  - python
  - testing
  - pytest
  - unit-testing
  - fastapi
  - sqlalchemy
  - postgresql
  - mocking
  - fixtures
  - async
  - customer-support
  - backend
  - data-curation
  - coverage
  - ci-cd
  - integration-testing
  - parametrization
use_cases:
  - Testing customer support ticket APIs and workflows
  - Validating database operations and transactions with PostgreSQL
  - Testing authentication and authorization flows for support systems
  - Mocking external services like email, SMS, webhooks, and CRM integrations
  - Testing async background tasks and queue processing
  - Data validation and curation testing for customer records
  - Integration testing with PostgreSQL and SQLAlchemy ORM
  - API endpoint testing for ticketing and knowledge base systems
  - Testing error handling and edge cases in support applications
  - Coverage reporting for support applications with quality gates
  - Testing multi-tenant customer support architectures
  - Validating SLA calculations and escalation logic
  - Testing notification systems and email templates
  - Database migration testing with Alembic
  - Performance and load testing for support APIs
dependencies:
  - pytest>=8.0.0
  - pytest-asyncio>=0.23.0
  - pytest-cov>=4.1.0
  - pytest-mock>=3.12.0
  - pytest-postgresql>=5.0.0
  - pytest-benchmark>=4.0.0
  - httpx>=0.26.0
  - fastapi>=0.109.0
  - sqlalchemy>=2.0.0
  - psycopg2-binary>=2.9.9
  - pydantic>=2.0.0
author: Claude Support Team
created: 2025-10-18
updated: 2025-10-18
---

# pytest - Advanced Python Unit Testing for Customer Support

## Overview

pytest is the industry-standard testing framework for Python applications, offering powerful features that enable comprehensive, maintainable, and scalable test suites. This skill focuses specifically on customer support tech enablement, providing patterns and practices for testing backend support systems, ticketing platforms, knowledge bases, and customer data platforms.

Customer support systems require rigorous testing due to their mission-critical nature. Downtime or bugs directly impact customer satisfaction, agent productivity, and business operations. This skill provides comprehensive guidance on testing all aspects of support systems using pytest.

## Why pytest for Customer Support Systems

### Unique Requirements

Customer support applications have specific testing needs:

1. **High Reliability**: Support systems are mission-critical; failures directly affect customer experience
2. **Complex Data Relationships**: Tickets, customers, agents, comments, attachments, and knowledge articles
3. **External Integrations**: Email services (SendGrid, AWS SES), CRM systems (Salesforce, HubSpot), payment processors
4. **Async Operations**: Background jobs, email queues, notification services, webhook deliveries
5. **Data Validation**: Strict validation for customer PII, ticket priorities, SLA requirements, escalation rules
6. **Multi-tenancy**: Isolation between different customer organizations or workspaces
7. **API-First Design**: RESTful APIs requiring comprehensive endpoint coverage
8. **Real-time Features**: WebSocket connections, live chat, real-time ticket updates
9. **Compliance**: GDPR, CCPA, data retention policies, audit logging

### pytest Advantages

pytest addresses these needs through:

- **Powerful Fixture System**: Manage complex database setups, API clients, and test data
- **Parametrization**: Test multiple scenarios efficiently (various ticket types, priority levels, user roles)
- **Rich Plugin Ecosystem**: pytest-asyncio for async testing, pytest-mock for mocking, pytest-cov for coverage
- **Excellent Integration**: Works seamlessly with FastAPI, SQLAlchemy, PostgreSQL, Pydantic
- **Clear Output**: Readable test results and comprehensive error reporting
- **Scalability**: Handles small test suites to thousands of tests with parallel execution
- **Flexibility**: Supports unit, integration, and end-to-end testing in one framework

## Core Competencies

### 1. Fixtures and Dependency Injection

Fixtures are pytest's killer feature, providing reusable setup/teardown logic and dependency injection. For customer support systems, fixtures manage databases, API clients, test data, and external service mocks.

#### Basic Fixtures

```python
import pytest
from app.models import Ticket, Customer, Agent

@pytest.fixture
def support_ticket():
    """Provide a basic support ticket dictionary."""
    return {
        "id": 1,
        "title": "Cannot access account",
        "description": "User unable to login after password reset",
        "status": "open",
        "priority": "high",
        "customer_email": "user@example.com",
        "category": "authentication"
    }

def test_ticket_structure(support_ticket):
    """Test ticket has required fields."""
    assert support_ticket["status"] == "open"
    assert support_ticket["priority"] in ["low", "medium", "high", "critical"]
    assert "@" in support_ticket["customer_email"]
```

#### Fixture Scopes

Control when fixtures are created and destroyed using scopes:

- **function** (default): Created once per test function, destroyed after test completes
- **class**: Created once per test class, shared across all methods
- **module**: Created once per module file, shared across all tests in file
- **package**: Created once per package, shared across all tests in package
- **session**: Created once per entire test session, shared across all tests

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator

@pytest.fixture(scope="session")
def database_engine():
    """Create database engine once per session."""
    engine = create_engine(
        "postgresql://support_user:password@localhost/support_test",
        echo=False,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20
    )
    # Create all tables
    from app.database import Base
    Base.metadata.create_all(engine)

    yield engine

    # Cleanup: drop all tables and dispose engine
    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(database_engine) -> Generator[Session, None, None]:
    """Create a new database session for each test with automatic rollback."""
    SessionLocal = sessionmaker(bind=database_engine)
    session = SessionLocal()

    try:
        yield session
    finally:
        session.rollback()  # Rollback any changes
        session.close()
```

#### Autouse Fixtures

Fixtures that run automatically without being explicitly requested:

```python
@pytest.fixture(autouse=True)
def reset_caches():
    """Clear all caches before each test."""
    from app.cache import ticket_cache, customer_cache, agent_cache
    ticket_cache.clear()
    customer_cache.clear()
    agent_cache.clear()
    yield
    # Optional cleanup after test
    ticket_cache.clear()
    customer_cache.clear()
    agent_cache.clear()

@pytest.fixture(autouse=True, scope="session")
def configure_logging():
    """Configure logging for test session."""
    import logging
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.ERROR)
```

#### Fixture Dependencies and Composition

Fixtures can depend on other fixtures, creating dependency chains:

```python
@pytest.fixture
def database_url():
    """Provide database URL for testing."""
    return "postgresql://test:test@localhost:5432/support_test"

@pytest.fixture
def engine(database_url):
    """Create SQLAlchemy engine from database URL."""
    from sqlalchemy import create_engine
    return create_engine(database_url, echo=False)

@pytest.fixture
def session(engine):
    """Create database session from engine."""
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

@pytest.fixture
def sample_customer(session):
    """Create a sample customer using database session."""
    customer = Customer(
        email="test@example.com",
        name="Test Customer",
        tier="premium",
        company="Acme Corp"
    )
    session.add(customer)
    session.commit()
    return customer

@pytest.fixture
def sample_ticket(session, sample_customer):
    """Create a sample ticket linked to sample customer."""
    ticket = Ticket(
        title="Test Ticket",
        description="Test description",
        priority="high",
        status="open",
        customer_id=sample_customer.id
    )
    session.add(ticket)
    session.commit()
    return ticket
```

#### Factory Fixtures

Create fixtures that return factory functions for flexible test data creation:

```python
@pytest.fixture
def ticket_factory(db_session):
    """Factory for creating tickets with custom attributes."""
    created_tickets = []

    def _create_ticket(
        title="Default Ticket",
        description="Default description",
        priority="medium",
        status="open",
        **kwargs
    ):
        ticket = Ticket(
            title=title,
            description=description,
            priority=priority,
            status=status,
            **kwargs
        )
        db_session.add(ticket)
        db_session.commit()
        created_tickets.append(ticket)
        return ticket

    yield _create_ticket

    # Cleanup: delete all created tickets
    for ticket in created_tickets:
        db_session.delete(ticket)
    db_session.commit()

def test_multiple_tickets(ticket_factory):
    """Test using factory to create multiple tickets."""
    high_priority = ticket_factory(priority="high", title="Urgent Issue")
    low_priority = ticket_factory(priority="low", title="Minor Request")

    assert high_priority.priority == "high"
    assert low_priority.priority == "low"
```

### 2. Parametrization

Parametrization allows running the same test with different inputs, essential for comprehensive testing of customer support systems with various priority levels, statuses, user roles, and edge cases.

#### Basic Parametrization

```python
@pytest.mark.parametrize("priority,expected_sla_hours", [
    ("critical", 1),
    ("high", 4),
    ("medium", 24),
    ("low", 72)
])
def test_sla_calculation(priority, expected_sla_hours):
    """Test SLA hours calculation for different priorities."""
    from app.services.sla import calculate_sla_hours
    sla = calculate_sla_hours(priority)
    assert sla == expected_sla_hours

@pytest.mark.parametrize("email,is_valid", [
    ("user@example.com", True),
    ("user.name+tag@example.co.uk", True),
    ("user@localhost", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("user@", False),
    ("", False),
    ("user @example.com", False),
    ("user@example .com", False),
])
def test_email_validation(email, is_valid):
    """Test email validation with various valid and invalid inputs."""
    from app.validators import is_valid_email
    assert is_valid_email(email) == is_valid
```

#### Multiple Parameters

```python
@pytest.mark.parametrize("status,priority,assigned,expected_urgent", [
    ("open", "critical", False, True),   # Unassigned critical = urgent
    ("open", "high", False, True),       # Unassigned high = urgent
    ("open", "medium", False, False),    # Unassigned medium = not urgent
    ("open", "low", False, False),       # Unassigned low = not urgent
    ("in_progress", "critical", True, False),  # Assigned critical = not urgent
    ("in_progress", "high", True, False),      # Assigned high = not urgent
    ("closed", "critical", True, False),       # Closed tickets never urgent
    ("resolved", "high", True, False),         # Resolved tickets never urgent
])
def test_urgent_ticket_identification(status, priority, assigned, expected_urgent):
    """Test identification of urgent tickets requiring immediate attention."""
    from app.models import Ticket
    ticket = Ticket(status=status, priority=priority)
    if assigned:
        ticket.assigned_agent_id = 123

    assert ticket.is_urgent() == expected_urgent
```

#### Parametrizing Fixtures

```python
@pytest.fixture(params=["sqlite", "postgresql"])
def database_type(request):
    """Parametrized fixture for different database types."""
    return request.param

def test_database_connection(database_type):
    """Test runs twice: once with SQLite, once with PostgreSQL."""
    from app.database import get_connection
    connection = get_connection(database_type)
    assert connection.is_connected()
    connection.close()

@pytest.fixture(params=[
    {"role": "admin", "can_delete": True, "can_reassign": True},
    {"role": "agent", "can_delete": False, "can_reassign": True},
    {"role": "viewer", "can_delete": False, "can_reassign": False},
])
def user_permissions(request):
    """Parametrized fixture for different user roles and permissions."""
    return request.param

def test_permission_checks(user_permissions):
    """Test permission validation for different roles."""
    from app.auth import check_permission

    can_delete = check_permission(user_permissions["role"], "delete_ticket")
    can_reassign = check_permission(user_permissions["role"], "reassign_ticket")

    assert can_delete == user_permissions["can_delete"]
    assert can_reassign == user_permissions["can_reassign"]
```

#### Using pytest.param for Complex Cases

```python
@pytest.mark.parametrize("email,expected_valid,reason", [
    pytest.param("user@example.com", True, "valid", id="valid-standard-email"),
    pytest.param("user+tag@example.com", True, "valid", id="valid-with-plus"),
    pytest.param("invalid", False, "missing-at", id="no-at-symbol"),
    pytest.param("@example.com", False, "no-user", id="missing-username"),
    pytest.param("user@", False, "no-domain", id="missing-domain"),
    pytest.param("user@.com", False, "invalid-domain", id="dot-at-domain-start"),
])
def test_email_validation_detailed(email, expected_valid, reason):
    """Test email validation with detailed reasoning."""
    from app.validators import validate_email_detailed
    result = validate_email_detailed(email)
    assert result.is_valid == expected_valid
    if not expected_valid:
        assert reason in result.error_code.lower()
```

#### Parametrization with IDs

```python
@pytest.mark.parametrize("ticket_data,expected_status", [
    ({"priority": "critical", "auto_assign": True}, "assigned"),
    ({"priority": "high", "auto_assign": True}, "assigned"),
    ({"priority": "medium", "auto_assign": False}, "open"),
    ({"priority": "low", "auto_assign": False}, "open"),
], ids=["critical-auto", "high-auto", "medium-manual", "low-manual"])
def test_auto_assignment(ticket_data, expected_status):
    """Test automatic ticket assignment based on priority."""
    from app.services.assignment import process_new_ticket
    ticket = process_new_ticket(**ticket_data)
    assert ticket.status == expected_status
```

### 3. Mocking with pytest-mock

Mocking is essential for isolating units of code from external dependencies like email services, payment gateways, CRM systems, and third-party APIs. The pytest-mock plugin provides a clean interface to Python's unittest.mock.

#### Basic Mocking

```python
def test_ticket_notification(mocker, db_session):
    """Test that creating a ticket sends email notification."""
    # Mock the email service
    mock_send = mocker.patch('app.services.email.EmailService.send_email')
    mock_send.return_value = {"status": "sent", "message_id": "msg_123"}

    # Create ticket
    from app.services.ticket import TicketService
    service = TicketService(db_session)
    ticket = service.create_ticket(
        title="Login Issue",
        description="Cannot access account",
        customer_email="customer@example.com",
        priority="high"
    )

    # Verify email was sent
    mock_send.assert_called_once()
    call_args = mock_send.call_args
    assert call_args.kwargs['to'] == "customer@example.com"
    assert "Login Issue" in call_args.kwargs['subject']
    assert ticket.id is not None
```

#### Mocking Return Values

```python
def test_customer_tier_lookup(mocker, api_client):
    """Test customer tier lookup from external CRM."""
    # Mock external CRM API response
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "customer_id": "CRM_12345",
        "tier": "enterprise",
        "support_plan": "24/7 premium",
        "account_manager": "jane@company.com"
    }

    mocker.patch('requests.get', return_value=mock_response)

    # Test endpoint that uses CRM data
    response = api_client.get("/api/customers/customer@example.com/tier")

    assert response.status_code == 200
    data = response.json()
    assert data["tier"] == "enterprise"
    assert data["support_plan"] == "24/7 premium"
```

#### Mocking Side Effects

```python
def test_retry_logic_on_api_failure(mocker):
    """Test retry mechanism when external API fails temporarily."""
    from app.services.external import call_with_retry

    mock_api = mocker.patch('app.services.external.call_external_api')
    # First two calls fail, third succeeds
    mock_api.side_effect = [
        ConnectionError("Connection timeout"),
        ConnectionError("Connection timeout"),
        {"success": True, "data": "response"}
    ]

    result = call_with_retry(max_attempts=3, backoff_seconds=0)

    assert result["success"] is True
    assert result["data"] == "response"
    assert mock_api.call_count == 3

def test_email_fallback_on_primary_failure(mocker):
    """Test email service fallback when primary provider fails."""
    from app.services.email import send_email_with_fallback

    mock_primary = mocker.patch('app.services.email.sendgrid_send')
    mock_fallback = mocker.patch('app.services.email.ses_send')

    # Primary fails, fallback succeeds
    mock_primary.side_effect = Exception("SendGrid API error")
    mock_fallback.return_value = {"status": "sent", "provider": "ses"}

    result = send_email_with_fallback(
        to="customer@example.com",
        subject="Ticket Update",
        body="Your ticket has been updated"
    )

    assert result["status"] == "sent"
    assert result["provider"] == "ses"
    mock_primary.assert_called_once()
    mock_fallback.assert_called_once()
```

#### Spying on Real Methods

```python
def test_cache_utilization(mocker, db_session):
    """Spy on cache to verify it's being used correctly."""
    from app.cache import ticket_cache

    spy_get = mocker.spy(ticket_cache, 'get')
    spy_set = mocker.spy(ticket_cache, 'set')

    from app.services.ticket import get_ticket

    # First call: cache miss, should query database
    ticket1 = get_ticket(123)
    assert spy_get.call_count == 1
    assert spy_set.call_count == 1

    # Second call: cache hit, should not query database
    ticket2 = get_ticket(123)
    assert spy_get.call_count == 2
    assert spy_set.call_count == 1  # Not called again

    assert ticket1.id == ticket2.id
```

#### Mocking Database Operations

```python
def test_ticket_creation_business_logic(mocker):
    """Test ticket creation logic without database."""
    mock_session = mocker.Mock()
    mock_session.add = mocker.Mock()
    mock_session.commit = mocker.Mock()
    mock_session.refresh = mocker.Mock(side_effect=lambda obj: setattr(obj, 'id', 123))

    from app.services.ticket import create_ticket_entity
    ticket = create_ticket_entity(
        mock_session,
        title="Test Ticket",
        priority="high"
    )

    assert ticket.id == 123
    assert ticket.priority == "high"
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
```

#### Async Mocking

```python
import pytest
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_async_notification_service(mocker):
    """Test async notification service with proper async mocking."""
    mock_send = mocker.patch(
        'app.services.notification.send_push_notification',
        new_callable=AsyncMock
    )
    mock_send.return_value = {
        "delivered": True,
        "notification_id": "notif_789"
    }

    from app.services.notification import NotificationService
    service = NotificationService()
    result = await service.notify_agent(
        agent_id=456,
        message="New high-priority ticket assigned to you",
        priority="high"
    )

    assert result["delivered"] is True
    assert result["notification_id"] is not None
    mock_send.assert_awaited_once()

    # Verify call arguments
    call_kwargs = mock_send.call_args.kwargs
    assert call_kwargs["agent_id"] == 456
    assert "high-priority" in call_kwargs["message"]
```

### 4. Coverage Reporting

Code coverage measures what percentage of your code is executed during testing. For customer support systems, comprehensive coverage ensures reliability and helps identify untested edge cases.

#### Basic Coverage Setup

```bash
# Install pytest-cov
pip install pytest-cov

# Run tests with coverage
pytest --cov=app tests/

# Generate HTML report
pytest --cov=app --cov-report=html tests/

# Show lines not covered
pytest --cov=app --cov-report=term-missing tests/

# Fail if coverage below threshold
pytest --cov=app --cov-fail-under=80 tests/
```

#### Configuration in pytest.ini

```ini
[pytest]
addopts =
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-report=xml
    --cov-fail-under=80
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow running tests
```

#### Coverage Configuration (.coveragerc)

```ini
[run]
source = app
omit =
    */tests/*
    */migrations/*
    */__init__.py
    */config.py
    */venv/*
    */.venv/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    def __str__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
    if TYPE_CHECKING:
    @abstractmethod
    @abc.abstractmethod
    except ImportError
precision = 2
show_missing = True

[html]
directory = htmlcov
title = Customer Support API Coverage Report
```

#### Branch Coverage

```ini
[run]
source = app
branch = True  # Enable branch coverage

[report]
show_missing = True
skip_covered = False
```

```bash
# Run with branch coverage
pytest --cov=app --cov-branch --cov-report=html
```

### 5. Async Testing

Modern customer support systems use asynchronous operations for better performance and scalability. Testing async code requires special handling to properly await coroutines.

#### Basic Async Tests

```python
import pytest

@pytest.mark.asyncio
async def test_async_ticket_creation():
    """Test asynchronous ticket creation service."""
    from app.services.ticket import create_ticket_async

    ticket = await create_ticket_async(
        title="Async Test Ticket",
        description="Testing async operations",
        priority="high",
        customer_email="async@example.com"
    )

    assert ticket.id is not None
    assert ticket.status == "open"
    assert ticket.priority == "high"
```

#### Async Fixtures

```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

@pytest.fixture
async def async_db_session():
    """Provide async database session."""
    engine = create_async_engine(
        "postgresql+asyncpg://user:pass@localhost/support_test",
        echo=False,
        future=True
    )

    async_session_maker = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session_maker() as session:
        yield session
        await session.rollback()

    await engine.dispose()

@pytest.mark.asyncio
async def test_async_database_operation(async_db_session):
    """Test async database operations."""
    from app.models import Ticket
    from sqlalchemy import select

    # Create ticket
    ticket = Ticket(title="Async DB Test", priority="medium")
    async_db_session.add(ticket)
    await async_db_session.commit()

    # Query ticket
    result = await async_db_session.execute(
        select(Ticket).where(Ticket.title == "Async DB Test")
    )
    found_ticket = result.scalar_one()

    assert found_ticket.id is not None
    assert found_ticket.priority == "medium"
```

#### Testing Async Background Tasks

```python
@pytest.mark.asyncio
async def test_background_email_task(mocker):
    """Test async background task for sending emails."""
    from app.tasks.email import process_ticket_notifications

    mock_send = mocker.patch(
        'app.tasks.email.send_email_async',
        new_callable=AsyncMock
    )
    mock_send.return_value = {"status": "sent", "message_id": "msg_456"}

    await process_ticket_notifications(ticket_id=123)

    mock_send.assert_awaited_once()
    call_kwargs = mock_send.call_args.kwargs
    assert "ticket_id" in call_kwargs or call_kwargs.get("ticket_id") == 123
```

#### Testing Concurrent Operations

```python
import asyncio

@pytest.mark.asyncio
async def test_concurrent_ticket_updates():
    """Test handling of concurrent ticket updates."""
    from app.services.ticket import update_ticket_async, add_comment_async

    ticket_id = 1

    async def update_status():
        return await update_ticket_async(ticket_id, status="in_progress")

    async def add_comment():
        return await add_comment_async(ticket_id, "Working on this issue")

    async def assign_agent():
        return await update_ticket_async(ticket_id, assigned_agent_id=42)

    # Execute concurrently
    results = await asyncio.gather(
        update_status(),
        add_comment(),
        assign_agent()
    )

    assert results[0]["status"] == "in_progress"
    assert results[1]["comment_count"] >= 1
    assert results[2]["assigned_agent_id"] == 42
```

#### Async Test Configuration

```python
# pytest.ini or pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"  # Automatically detect and run async tests

# Or in pytest.ini
[pytest]
asyncio_mode = auto
```

### 6. FastAPI Testing

FastAPI is widely used for customer support APIs. Testing endpoints ensures proper request/response handling, validation, authentication, and business logic.

#### Basic FastAPI Testing

```python
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """Provide FastAPI test client."""
    return TestClient(app)

def test_create_ticket_endpoint(client):
    """Test ticket creation via POST endpoint."""
    response = client.post(
        "/api/v1/tickets",
        json={
            "title": "Cannot login to application",
            "description": "User receives 'invalid credentials' error",
            "priority": "high",
            "customer_email": "frustrated@example.com",
            "category": "authentication"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Cannot login to application"
    assert data["priority"] == "high"
    assert "id" in data
    assert "created_at" in data

def test_get_ticket_by_id(client, sample_tickets):
    """Test retrieving specific ticket by ID."""
    ticket_id = sample_tickets[0].id

    response = client.get(f"/api/v1/tickets/{ticket_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == ticket_id
    assert data["title"] == sample_tickets[0].title

def test_update_ticket_status(client, sample_tickets):
    """Test updating ticket status via PATCH."""
    ticket_id = sample_tickets[0].id

    response = client.patch(
        f"/api/v1/tickets/{ticket_id}",
        json={"status": "in_progress"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "in_progress"
    assert data["id"] == ticket_id
```

#### Dependency Override

FastAPI's dependency injection can be overridden for testing:

```python
from app.dependencies import get_db, get_current_user
from app.models import User

@pytest.fixture
def authenticated_client(client, mocker):
    """Provide authenticated test client."""
    mock_user = User(
        id=1,
        email="agent@support.com",
        role="agent",
        name="Test Agent"
    )

    async def override_get_current_user():
        return mock_user

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield client
    app.dependency_overrides.clear()

def test_protected_endpoint(authenticated_client):
    """Test endpoint requiring authentication."""
    response = authenticated_client.get("/api/v1/admin/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.fixture
def admin_client(client, mocker):
    """Provide client authenticated as admin."""
    mock_admin = User(
        id=1,
        email="admin@support.com",
        role="admin",
        permissions=["read", "write", "delete", "admin"]
    )

    async def override_get_current_user():
        return mock_admin

    app.dependency_overrides[get_current_user] = override_get_current_user
    yield client
    app.dependency_overrides.clear()

def test_admin_only_endpoint(admin_client):
    """Test endpoint requiring admin privileges."""
    response = admin_client.delete("/api/v1/tickets/123")
    assert response.status_code in [200, 204, 404]  # Success or not found
```

#### Testing with Database

```python
@pytest.fixture
def client_with_db(db_session):
    """Provide FastAPI client with database session override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_ticket_lifecycle(client_with_db, db_session):
    """Test complete ticket lifecycle with database persistence."""
    # Create ticket
    create_response = client_with_db.post(
        "/api/v1/tickets",
        json={
            "title": "Lifecycle Test",
            "description": "Testing full CRUD cycle",
            "priority": "medium"
        }
    )
    assert create_response.status_code == 201
    ticket_id = create_response.json()["id"]

    # Read ticket
    get_response = client_with_db.get(f"/api/v1/tickets/{ticket_id}")
    assert get_response.status_code == 200
    assert get_response.json()["title"] == "Lifecycle Test"

    # Update ticket
    update_response = client_with_db.patch(
        f"/api/v1/tickets/{ticket_id}",
        json={"status": "resolved", "priority": "low"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["status"] == "resolved"

    # Verify in database
    from app.models import Ticket
    ticket = db_session.query(Ticket).filter_by(id=ticket_id).first()
    assert ticket is not None
    assert ticket.status == "resolved"
    assert ticket.priority == "low"

    # Delete ticket
    delete_response = client_with_db.delete(f"/api/v1/tickets/{ticket_id}")
    assert delete_response.status_code in [200, 204]

    # Verify deletion
    get_deleted = client_with_db.get(f"/api/v1/tickets/{ticket_id}")
    assert get_deleted.status_code == 404
```

#### Testing Request Validation

```python
def test_invalid_ticket_creation(client):
    """Test that invalid ticket data returns proper validation errors."""
    # Missing required field
    response = client.post(
        "/api/v1/tickets",
        json={"description": "Missing title"}
    )
    assert response.status_code == 422

    # Invalid priority
    response = client.post(
        "/api/v1/tickets",
        json={
            "title": "Test",
            "description": "Test",
            "priority": "invalid_priority"
        }
    )
    assert response.status_code == 422
    errors = response.json()["detail"]
    assert any("priority" in str(e).lower() for e in errors)

    # Invalid email format
    response = client.post(
        "/api/v1/tickets",
        json={
            "title": "Test",
            "description": "Test",
            "customer_email": "not_an_email"
        }
    )
    assert response.status_code == 422
```

### 7. SQLAlchemy Testing

Testing database models, queries, relationships, and operations ensures data integrity in customer support systems.

#### Model Testing

```python
from app.models import Ticket, Comment, User, Customer

def test_ticket_model_creation(db_session):
    """Test creating and persisting ticket model."""
    customer = Customer(
        email="customer@example.com",
        name="John Doe",
        tier="enterprise"
    )
    db_session.add(customer)
    db_session.flush()

    ticket = Ticket(
        title="Database Connection Error",
        description="Cannot connect to production database",
        priority="critical",
        status="open",
        customer_id=customer.id,
        category="technical"
    )
    db_session.add(ticket)
    db_session.commit()

    assert ticket.id is not None
    assert ticket.created_at is not None
    assert ticket.customer.email == "customer@example.com"

def test_ticket_model_defaults(db_session):
    """Test default values on ticket model."""
    ticket = Ticket(title="Test", description="Test")
    db_session.add(ticket)
    db_session.commit()

    assert ticket.status == "open"  # Default status
    assert ticket.priority == "medium"  # Default priority
    assert ticket.created_at is not None
    assert ticket.updated_at is not None
```

#### Relationship Testing

```python
def test_ticket_comments_relationship(db_session):
    """Test one-to-many relationship between tickets and comments."""
    ticket = Ticket(
        title="Test Ticket",
        description="Testing relationships",
        priority="low"
    )
    db_session.add(ticket)
    db_session.flush()

    # Add multiple comments
    comment1 = Comment(
        ticket_id=ticket.id,
        content="First comment",
        author_email="agent1@support.com"
    )
    comment2 = Comment(
        ticket_id=ticket.id,
        content="Second comment",
        author_email="agent2@support.com"
    )
    db_session.add_all([comment1, comment2])
    db_session.commit()

    # Reload ticket and verify relationship
    db_session.expire(ticket)
    assert len(ticket.comments) == 2
    assert ticket.comments[0].content == "First comment"
    assert ticket.comments[1].content == "Second comment"

def test_customer_tickets_relationship(db_session):
    """Test one-to-many relationship between customers and tickets."""
    customer = Customer(
        email="loyal@customer.com",
        name="Loyal Customer"
    )
    db_session.add(customer)
    db_session.flush()

    # Create multiple tickets for same customer
    for i in range(3):
        ticket = Ticket(
            title=f"Issue #{i+1}",
            description=f"Description {i+1}",
            customer_id=customer.id
        )
        db_session.add(ticket)

    db_session.commit()

    # Verify customer has all tickets
    db_session.expire(customer)
    assert len(customer.tickets) == 3
    assert all(t.customer_id == customer.id for t in customer.tickets)
```

#### Query Testing

```python
def test_filter_tickets_by_status(db_session):
    """Test filtering tickets by status."""
    # Create tickets with different statuses
    tickets = [
        Ticket(title=f"Ticket {i}", status="open" if i % 2 == 0 else "closed")
        for i in range(10)
    ]
    db_session.add_all(tickets)
    db_session.commit()

    # Query open tickets
    open_tickets = db_session.query(Ticket).filter_by(status="open").all()
    assert len(open_tickets) == 5
    assert all(t.status == "open" for t in open_tickets)

    # Query closed tickets
    closed_tickets = db_session.query(Ticket).filter_by(status="closed").all()
    assert len(closed_tickets) == 5
    assert all(t.status == "closed" for t in closed_tickets)

def test_complex_ticket_query(db_session):
    """Test complex multi-filter ticket query."""
    from sqlalchemy import and_, or_
    from datetime import datetime, timedelta

    # Create diverse set of tickets
    old_critical = Ticket(
        title="Old Critical",
        priority="critical",
        status="open",
        created_at=datetime.utcnow() - timedelta(days=7)
    )
    recent_high = Ticket(
        title="Recent High",
        priority="high",
        status="open",
        created_at=datetime.utcnow() - timedelta(hours=2)
    )
    old_low = Ticket(
        title="Old Low",
        priority="low",
        status="open",
        created_at=datetime.utcnow() - timedelta(days=30)
    )

    db_session.add_all([old_critical, recent_high, old_low])
    db_session.commit()

    # Query: open tickets that are either critical OR created in last 24 hours
    cutoff = datetime.utcnow() - timedelta(days=1)
    urgent_tickets = db_session.query(Ticket).filter(
        and_(
            Ticket.status == "open",
            or_(
                Ticket.priority == "critical",
                Ticket.created_at >= cutoff
            )
        )
    ).all()

    assert len(urgent_tickets) == 2
    ticket_titles = [t.title for t in urgent_tickets]
    assert "Old Critical" in ticket_titles
    assert "Recent High" in ticket_titles
    assert "Old Low" not in ticket_titles
```

#### Transaction Testing

```python
def test_transaction_rollback_on_error(db_session):
    """Test that failed transactions are properly rolled back."""
    from sqlalchemy.exc import IntegrityError

    # Create initial ticket
    ticket1 = Ticket(title="First Ticket", description="Test")
    db_session.add(ticket1)
    db_session.commit()

    initial_count = db_session.query(Ticket).count()

    # Attempt to create invalid ticket (will fail)
    try:
        ticket2 = Ticket(title="Second Ticket", description="Test")
        db_session.add(ticket2)
        db_session.flush()

        # Simulate constraint violation
        ticket3 = Ticket(
            title="Third Ticket",
            external_id="DUPLICATE_ID"  # Assuming unique constraint
        )
        db_session.add(ticket3)

        ticket4 = Ticket(
            title="Fourth Ticket",
            external_id="DUPLICATE_ID"  # Will violate unique constraint
        )
        db_session.add(ticket4)
        db_session.commit()
    except IntegrityError:
        db_session.rollback()

    # Verify count hasn't changed
    final_count = db_session.query(Ticket).count()
    assert final_count == initial_count
```

### 8. Database Fixtures

Well-designed database fixtures are crucial for testing customer support systems with complex data relationships.

#### Comprehensive Database Fixture

```python
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from app.database import Base

@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine for entire session."""
    engine = create_engine(
        "postgresql://test:test@localhost:5432/support_test",
        echo=False,
        pool_pre_ping=True
    )

    # Create all tables
    Base.metadata.create_all(engine)

    yield engine

    # Cleanup: drop all tables
    Base.metadata.drop_all(engine)
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    """Provide clean database session with automatic rollback."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    # Enable savepoints for nested transactions
    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            session.begin_nested()

    session.begin_nested()

    yield session

    # Cleanup
    session.close()
    transaction.rollback()
    connection.close()
```

#### Sample Data Fixtures

```python
@pytest.fixture
def sample_customers(db_session):
    """Create sample customers with various tiers."""
    customers = [
        Customer(email="free@example.com", name="Free User", tier="free"),
        Customer(email="basic@example.com", name="Basic User", tier="basic"),
        Customer(email="premium@example.com", name="Premium User", tier="premium"),
        Customer(email="enterprise@example.com", name="Enterprise User", tier="enterprise"),
    ]
    db_session.add_all(customers)
    db_session.commit()
    return customers

@pytest.fixture
def sample_agents(db_session):
    """Create sample support agents."""
    agents = [
        User(email="agent1@support.com", name="Agent One", role="agent"),
        User(email="agent2@support.com", name="Agent Two", role="agent"),
        User(email="senior@support.com", name="Senior Agent", role="senior_agent"),
    ]
    db_session.add_all(agents)
    db_session.commit()
    return agents

@pytest.fixture
def sample_tickets(db_session, sample_customers):
    """Create diverse set of sample tickets."""
    tickets = []
    priorities = ["low", "medium", "high", "critical"]
    statuses = ["open", "in_progress", "resolved", "closed"]

    for i in range(12):
        ticket = Ticket(
            title=f"Sample Ticket #{i+1}",
            description=f"Description for ticket {i+1}",
            priority=priorities[i % len(priorities)],
            status=statuses[i % len(statuses)],
            customer_id=sample_customers[i % len(sample_customers)].id,
            category=["technical", "billing", "account"][i % 3]
        )
        tickets.append(ticket)

    db_session.add_all(tickets)
    db_session.commit()
    return tickets
```

#### Factory Pattern Fixtures

```python
@pytest.fixture
def customer_factory(db_session):
    """Factory for creating customers with custom attributes."""
    created = []

    def _create_customer(
        email=None,
        name=None,
        tier="basic",
        **kwargs
    ):
        import uuid
        customer = Customer(
            email=email or f"customer{uuid.uuid4().hex[:8]}@example.com",
            name=name or f"Customer {uuid.uuid4().hex[:8]}",
            tier=tier,
            **kwargs
        )
        db_session.add(customer)
        db_session.commit()
        created.append(customer)
        return customer

    yield _create_customer

    # Cleanup
    for customer in created:
        db_session.delete(customer)
    db_session.commit()

@pytest.fixture
def ticket_factory(db_session, customer_factory):
    """Factory for creating tickets with automatic customer creation."""
    created = []

    def _create_ticket(
        title=None,
        customer=None,
        priority="medium",
        status="open",
        **kwargs
    ):
        import uuid

        if customer is None:
            customer = customer_factory()

        ticket = Ticket(
            title=title or f"Ticket {uuid.uuid4().hex[:8]}",
            description=kwargs.pop("description", "Test ticket description"),
            customer_id=customer.id,
            priority=priority,
            status=status,
            **kwargs
        )
        db_session.add(ticket)
        db_session.commit()
        created.append(ticket)
        return ticket

    yield _create_ticket

    # Cleanup
    for ticket in created:
        db_session.delete(ticket)
    db_session.commit()

# Usage in tests
def test_with_factories(customer_factory, ticket_factory):
    """Test using factory fixtures for flexible test data creation."""
    # Create premium customer
    premium_customer = customer_factory(tier="enterprise", name="Big Corp")

    # Create multiple tickets for same customer
    critical_ticket = ticket_factory(
        customer=premium_customer,
        priority="critical",
        title="Production outage"
    )
    normal_ticket = ticket_factory(
        customer=premium_customer,
        priority="low",
        title="Feature request"
    )

    assert critical_ticket.customer_id == premium_customer.id
    assert normal_ticket.customer_id == premium_customer.id
    assert premium_customer.tier == "enterprise"
```

### 9. Customer Support Testing Scenarios

Real-world testing scenarios specific to customer support systems.

#### Testing Ticket Assignment Logic

```python
def test_round_robin_assignment(db_session, sample_agents):
    """Test round-robin ticket assignment to available agents."""
    from app.services.assignment import assign_ticket_round_robin

    tickets = []
    for i in range(9):
        ticket = Ticket(
            title=f"Assignment Test {i}",
            priority="medium",
            status="open"
        )
        db_session.add(ticket)
        db_session.flush()

        assign_ticket_round_robin(ticket, db_session)
        tickets.append(ticket)

    db_session.commit()

    # Verify even distribution
    for agent in sample_agents:
        assigned_count = len([t for t in tickets if t.assigned_agent_id == agent.id])
        assert assigned_count == 3  # 9 tickets / 3 agents = 3 each

def test_priority_based_assignment(db_session, sample_agents):
    """Test that critical tickets go to senior agents."""
    from app.services.assignment import assign_ticket_by_priority

    critical_ticket = Ticket(
        title="Critical Issue",
        priority="critical",
        status="open"
    )
    db_session.add(critical_ticket)
    db_session.flush()

    assign_ticket_by_priority(critical_ticket, db_session)
    db_session.commit()

    # Find senior agent
    senior_agent = next(a for a in sample_agents if a.role == "senior_agent")
    assert critical_ticket.assigned_agent_id == senior_agent.id
```

#### Testing SLA Compliance

```python
from datetime import datetime, timedelta

def test_sla_breach_detection(db_session):
    """Test detection of SLA breaches for different priorities."""
    from app.services.sla import find_sla_breaches

    now = datetime.utcnow()

    # Critical ticket created 2 hours ago (SLA: 1 hour) - BREACHED
    breached_critical = Ticket(
        title="Critical - Breached",
        priority="critical",
        status="open",
        created_at=now - timedelta(hours=2)
    )

    # High priority created 5 hours ago (SLA: 4 hours) - BREACHED
    breached_high = Ticket(
        title="High - Breached",
        priority="high",
        status="open",
        created_at=now - timedelta(hours=5)
    )

    # Medium priority created 2 hours ago (SLA: 24 hours) - OK
    ok_medium = Ticket(
        title="Medium - OK",
        priority="medium",
        status="open",
        created_at=now - timedelta(hours=2)
    )

    # Critical ticket but already assigned (not breached)
    assigned_critical = Ticket(
        title="Critical - Assigned",
        priority="critical",
        status="in_progress",
        created_at=now - timedelta(hours=2),
        assigned_agent_id=1
    )

    db_session.add_all([breached_critical, breached_high, ok_medium, assigned_critical])
    db_session.commit()

    breaches = find_sla_breaches(db_session)
    breach_titles = [b.title for b in breaches]

    assert len(breaches) == 2
    assert "Critical - Breached" in breach_titles
    assert "High - Breached" in breach_titles
    assert "Medium - OK" not in breach_titles
    assert "Critical - Assigned" not in breach_titles

def test_sla_time_remaining_calculation(db_session):
    """Test calculation of remaining SLA time."""
    from app.services.sla import calculate_sla_remaining

    now = datetime.utcnow()

    # High priority ticket created 1 hour ago (SLA: 4 hours)
    ticket = Ticket(
        title="SLA Test",
        priority="high",
        status="open",
        created_at=now - timedelta(hours=1)
    )
    db_session.add(ticket)
    db_session.commit()

    remaining = calculate_sla_remaining(ticket)

    # Should have ~3 hours remaining (4 hour SLA - 1 hour elapsed)
    assert 2.9 <= remaining.total_seconds() / 3600 <= 3.1
```

#### Testing Escalation Rules

```python
def test_automatic_escalation(db_session):
    """Test automatic ticket escalation for overdue tickets."""
    from app.services.escalation import escalate_overdue_tickets

    now = datetime.utcnow()

    # Medium priority ticket open for 3 days without assignment
    overdue_ticket = Ticket(
        title="Overdue Ticket",
        priority="medium",
        status="open",
        created_at=now - timedelta(days=3)
    )

    # Recent ticket (should not escalate)
    recent_ticket = Ticket(
        title="Recent Ticket",
        priority="medium",
        status="open",
        created_at=now - timedelta(hours=2)
    )

    db_session.add_all([overdue_ticket, recent_ticket])
    db_session.commit()

    # Run escalation logic
    escalated_count = escalate_overdue_tickets(db_session)

    db_session.refresh(overdue_ticket)
    db_session.refresh(recent_ticket)

    assert escalated_count == 1
    assert overdue_ticket.priority == "high"  # Escalated from medium
    assert overdue_ticket.escalated is True
    assert recent_ticket.priority == "medium"  # Unchanged
    assert recent_ticket.escalated is False
```

#### Testing Customer Notifications

```python
def test_status_change_notification(mocker, db_session):
    """Test email notification sent when ticket status changes."""
    from app.services.ticket import update_ticket_status

    mock_send_email = mocker.patch('app.services.email.send_email')
    mock_send_email.return_value = {"status": "sent"}

    ticket = Ticket(
        title="Notification Test",
        customer_email="customer@example.com",
        status="open"
    )
    db_session.add(ticket)
    db_session.commit()

    # Update status
    update_ticket_status(ticket.id, "resolved", db_session)

    # Verify notification sent
    mock_send_email.assert_called_once()
    call_kwargs = mock_send_email.call_args.kwargs
    assert call_kwargs["to"] == "customer@example.com"
    assert "resolved" in call_kwargs["template_name"].lower()
    assert call_kwargs["template_data"]["ticket_id"] == ticket.id

def test_assignment_notification(mocker, db_session, sample_agents):
    """Test notification sent to agent when ticket assigned."""
    from app.services.ticket import assign_ticket

    mock_notify = mocker.patch('app.services.notification.notify_agent')

    ticket = Ticket(title="Assignment Notification Test", status="open")
    db_session.add(ticket)
    db_session.commit()

    agent = sample_agents[0]
    assign_ticket(ticket.id, agent.id, db_session)

    mock_notify.assert_called_once()
    call_args = mock_notify.call_args
    assert call_args[0][0] == agent.id  # First arg is agent_id
    assert "assigned" in call_args[0][1].lower()  # Second arg is message
```

### 10. Integration Patterns

Testing integrations with external services and systems.

#### Testing External API Integration

```python
@pytest.mark.integration
def test_crm_sync_integration(mocker, db_session):
    """Test synchronization with external CRM system."""
    from app.services.crm import sync_customer_to_crm

    # Mock external CRM API
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "crm_customer_id": "CRM_98765",
        "sync_status": "success",
        "last_sync": "2025-01-15T10:30:00Z"
    }

    mocker.patch('requests.post', return_value=mock_response)

    customer = Customer(
        email="crm.test@example.com",
        name="CRM Test Customer",
        tier="enterprise"
    )
    db_session.add(customer)
    db_session.commit()

    result = sync_customer_to_crm(customer.id, db_session)

    assert result["sync_status"] == "success"
    assert result["crm_customer_id"] == "CRM_98765"

    # Verify customer record updated
    db_session.refresh(customer)
    assert customer.crm_id == "CRM_98765"
```

#### Testing Webhook Delivery

```python
def test_webhook_delivery_on_ticket_created(mocker, db_session):
    """Test webhook delivery when new ticket is created."""
    from app.services.webhooks import deliver_webhook

    # Setup webhook subscription
    webhook = WebhookSubscription(
        url="https://customer-app.example.com/webhooks/support",
        events=["ticket.created", "ticket.updated"],
        active=True
    )
    db_session.add(webhook)
    db_session.commit()

    mock_post = mocker.patch('requests.post')
    mock_post.return_value.status_code = 200

    ticket = Ticket(
        title="Webhook Test Ticket",
        priority="high"
    )
    db_session.add(ticket)
    db_session.commit()

    # Trigger webhook delivery
    from app.services.webhooks import trigger_webhooks
    trigger_webhooks("ticket.created", ticket.to_dict(), db_session)

    # Verify webhook called
    assert mock_post.call_count == 1
    call_kwargs = mock_post.call_args.kwargs
    assert call_kwargs["url"] == "https://customer-app.example.com/webhooks/support"
    assert call_kwargs["json"]["event"] == "ticket.created"
    assert call_kwargs["json"]["data"]["id"] == ticket.id
```

#### Testing Background Job Processing

```python
@pytest.mark.asyncio
async def test_background_export_job(db_session, sample_tickets):
    """Test asynchronous ticket export background job."""
    from app.tasks.export import export_tickets_job

    job = Job(
        type="export_tickets",
        status="pending",
        params={
            "format": "csv",
            "date_range": "last_7_days",
            "filters": {"priority": ["high", "critical"]}
        }
    )
    db_session.add(job)
    db_session.commit()

    # Process job
    result = await export_tickets_job(job.id, db_session)

    db_session.refresh(job)

    assert job.status == "completed"
    assert job.result is not None
    assert "file_url" in job.result
    assert "row_count" in job.result
    assert result["success"] is True
```

### 11. Best Practices

#### Test Organization

Structure tests to mirror application architecture:

```
tests/
├── unit/                   # Fast, isolated unit tests
│   ├── test_models.py
│   ├── test_validators.py
│   ├── test_utils.py
│   └── services/
│       ├── test_ticket_service.py
│       ├── test_email_service.py
│       └── test_sla_service.py
├── integration/           # Tests with database/external deps
│   ├── test_api_tickets.py
│   ├── test_api_customers.py
│   ├── test_database_ops.py
│   └── test_external_apis.py
├── e2e/                   # End-to-end workflow tests
│   ├── test_ticket_lifecycle.py
│   └── test_customer_journey.py
├── performance/           # Performance/load tests
│   └── test_api_performance.py
└── conftest.py           # Shared fixtures
```

#### Descriptive Test Names

```python
# Good - clear, specific test names
def test_high_priority_ticket_sends_immediate_notification_to_assigned_agent():
    pass

def test_ticket_auto_closes_after_7_days_without_customer_response():
    pass

def test_sla_breach_alert_sent_to_team_lead_when_critical_ticket_unassigned_for_1_hour():
    pass

# Bad - vague test names
def test_ticket_notification():
    pass

def test_auto_close():
    pass

def test_sla():
    pass
```

#### AAA Pattern (Arrange-Act-Assert)

```python
def test_ticket_assignment():
    # Arrange: Set up test data and conditions
    agent = create_agent(name="Test Agent", role="agent")
    ticket = create_ticket(title="Test", priority="high", status="open")

    # Act: Perform the action being tested
    result = assign_ticket(ticket.id, agent.id)

    # Assert: Verify expected outcomes
    assert result.assigned_agent_id == agent.id
    assert result.status == "assigned"
    assert result.assigned_at is not None
```

#### Test Isolation

```python
# Each test should be independent and not rely on others

# Bad - tests depend on execution order
def test_create_user():
    create_user("test@example.com")

def test_get_user():
    user = get_user("test@example.com")  # Relies on test_create_user
    assert user is not None

# Good - each test is self-contained
@pytest.fixture
def test_user(db_session):
    user = User(email="test@example.com")
    db_session.add(user)
    db_session.commit()
    return user

def test_get_user_by_email(db_session, test_user):
    found_user = get_user(test_user.email, db_session)
    assert found_user.email == test_user.email
```

#### Testing Guidelines

1. **Test one thing per test:**

```python
# Good
def test_ticket_creation_sets_default_status():
    ticket = create_ticket(title="Test")
    assert ticket.status == "open"

def test_ticket_creation_sets_created_timestamp():
    ticket = create_ticket(title="Test")
    assert ticket.created_at is not None

# Bad
def test_ticket_creation():
    ticket = create_ticket(title="Test")
    assert ticket.status == "open"
    assert ticket.created_at is not None
    assert ticket.priority == "medium"
    assert ticket.category is None
```

2. **Use fixtures for setup:**

```python
# Good
@pytest.fixture
def authenticated_user(db_session):
    user = User(email="auth@example.com", role="agent")
    db_session.add(user)
    db_session.commit()
    return user

def test_authenticated_endpoint(authenticated_user, api_client):
    response = api_client.get("/api/tickets", user=authenticated_user)
    assert response.status_code == 200

# Less ideal - setup in test
def test_authenticated_endpoint(api_client):
    user = User(email="auth@example.com", role="agent")
    # ... more setup ...
    response = api_client.get("/api/tickets", user=user)
    assert response.status_code == 200
```

3. **Mock external dependencies:**

```python
def test_email_notification_on_ticket_creation(mocker):
    """Always mock external services like email."""
    mock_send = mocker.patch('app.services.email.send_email')
    mock_send.return_value = {"status": "sent"}

    ticket = create_ticket(title="Test", customer_email="user@example.com")

    mock_send.assert_called_once()
    assert ticket.id is not None
```

### 12. Common Pitfalls and Solutions

#### Problem: Database State Leakage

Tests affecting each other due to shared database state.

**Solution:** Use transaction rollback in fixtures.

```python
@pytest.fixture
def db_session(db_engine):
    """Isolate database state per test with rollback."""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    yield session

    session.close()
    transaction.rollback()  # Rollback all changes
    connection.close()
```

#### Problem: Async Test Hanging

Forgetting to mark async tests or improper event loop handling.

**Solution:** Always use @pytest.mark.asyncio and await coroutines.

```python
# Wrong - test will hang
async def test_async_operation():
    result = await async_function()
    assert result is not None

# Correct
@pytest.mark.asyncio
async def test_async_operation():
    result = await async_function()
    assert result is not None
```

#### Problem: Fixture Scope Issues

Session-scoped fixtures with mutable state causing test pollution.

**Solution:** Use appropriate scope and reset state.

```python
# Problematic
@pytest.fixture(scope="session")
def user_cache():
    return {}  # Shared dict across all tests

# Better
@pytest.fixture(scope="function")
def user_cache():
    return {}  # New dict per test

# Or reset state
@pytest.fixture(scope="session")
def user_cache():
    cache = {}
    yield cache
    cache.clear()  # Clean up after each test
```

#### Problem: Over-Mocking

Mocking too much makes tests meaningless.

**Solution:** Only mock external boundaries.

```python
# Over-mocked - testing nothing real
def test_ticket_creation(mocker):
    mocker.patch('app.services.create_ticket', return_value=Ticket(id=1))
    ticket = create_ticket(title="Test")
    assert ticket.id == 1  # Just testing the mock

# Better - test actual logic
def test_ticket_creation(db_session):
    ticket = create_ticket_service(db_session, title="Test", priority="high")
    assert ticket.id is not None
    assert ticket.status == "open"
    assert ticket.priority == "high"
```

#### Problem: Slow Test Suite

Tests taking too long to run.

**Solution:** Use appropriate markers and parallel execution.

```bash
# Run only fast tests
pytest -m "not slow"

# Run tests in parallel
pytest -n auto  # Requires pytest-xdist

# Run specific test file
pytest tests/unit/test_validators.py -v
```

### 13. PostgreSQL Integration

#### Testing with Real PostgreSQL

```python
@pytest.fixture(scope="session")
def postgres_engine():
    """Create PostgreSQL engine with test database."""
    from sqlalchemy import create_engine

    # Connect to default database to create test database
    admin_url = "postgresql://postgres:password@localhost/postgres"
    admin_engine = create_engine(admin_url, isolation_level="AUTOCOMMIT")

    with admin_engine.connect() as conn:
        # Drop and recreate test database
        conn.execute("DROP DATABASE IF EXISTS support_test")
        conn.execute("CREATE DATABASE support_test")

    # Connect to test database
    test_url = "postgresql://postgres:password@localhost/support_test"
    test_engine = create_engine(test_url)

    from app.database import Base
    Base.metadata.create_all(test_engine)

    yield test_engine

    # Cleanup
    test_engine.dispose()
    with admin_engine.connect() as conn:
        conn.execute("DROP DATABASE support_test")
    admin_engine.dispose()
```

#### Testing PostgreSQL-Specific Features

```python
def test_full_text_search(db_session):
    """Test PostgreSQL full-text search on tickets."""
    from sqlalchemy import func

    tickets = [
        Ticket(title="Cannot login", description="Password reset not working"),
        Ticket(title="Slow performance", description="Dashboard loading slowly"),
        Ticket(title="Email issues", description="Not receiving notifications"),
    ]
    db_session.add_all(tickets)
    db_session.commit()

    # Search using PostgreSQL full-text search
    search_term = "login password"
    results = db_session.query(Ticket).filter(
        func.to_tsvector('english', Ticket.title + ' ' + Ticket.description).match(search_term)
    ).all()

    assert len(results) >= 1
    assert any("login" in t.title.lower() for t in results)

def test_jsonb_field_operations(db_session):
    """Test JSONB field operations in PostgreSQL."""
    from sqlalchemy.dialects.postgresql import JSONB

    ticket = Ticket(
        title="JSONB Test",
        metadata_={"tags": ["urgent", "billing"], "source": "email"}
    )
    db_session.add(ticket)
    db_session.commit()

    # Query using JSONB operations
    from sqlalchemy import cast
    results = db_session.query(Ticket).filter(
        Ticket.metadata_['tags'].astext.contains('urgent')
    ).all()

    assert len(results) >= 1
    assert results[0].metadata_["tags"] == ["urgent", "billing"]
```

### 14. CI/CD Integration

#### GitHub Actions Configuration

```yaml
name: Test Suite

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: test_user
          POSTGRES_PASSWORD: test_password
          POSTGRES_DB: support_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov pytest-asyncio pytest-mock

      - name: Run migrations
        env:
          DATABASE_URL: postgresql://test_user:test_password@localhost:5432/support_test
        run: |
          alembic upgrade head

      - name: Run tests
        env:
          DATABASE_URL: postgresql://test_user:test_password@localhost:5432/support_test
        run: |
          pytest -v \
            --cov=app \
            --cov-report=xml \
            --cov-report=term-missing \
            --cov-fail-under=80

      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

## Troubleshooting

### Common Issues

1. **Import errors:** Ensure PYTHONPATH includes project root or use `pip install -e .`
2. **Fixture not found:** Check conftest.py location and fixture name spelling
3. **Database locked:** Use PostgreSQL instead of SQLite for concurrent tests
4. **Async tests hanging:** Verify pytest-asyncio installed and asyncio_mode configured
5. **Mocks not working:** Patch where function is used, not where it's defined

## Summary

pytest provides comprehensive testing capabilities for customer support systems:

- **Fixtures** for reusable setup and dependency injection
- **Parametrization** for testing multiple scenarios
- **Mocking** to isolate external dependencies
- **Async support** for modern async applications
- **Coverage** to measure test completeness
- **FastAPI integration** for API testing
- **SQLAlchemy/PostgreSQL** for database testing

This skill enables support teams to build reliable, well-tested backend systems that serve customers effectively.
