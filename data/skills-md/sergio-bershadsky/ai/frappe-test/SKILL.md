---
name: frappe-test
description: |
  Create comprehensive test suites for Frappe Framework v15 applications. Triggers: "create tests", "add tests", "frappe test", "write tests", "test coverage", "/frappe-test". Generates unit tests, integration tests, fixtures, and factory patterns following testing best practices.
---

# Frappe Testing Suite

Create comprehensive test coverage for Frappe v15 applications using pytest-compatible test classes, fixtures, and factory patterns.

## When to Use

- Adding test coverage to existing code
- Creating tests for new DocTypes/APIs/Services
- Setting up test fixtures and factories
- Writing integration tests with database access
- Creating unit tests without database dependency

## Arguments

```
/frappe-test <target> [--type <unit|integration|e2e>] [--coverage]
```

**Examples:**
```
/frappe-test SalesOrder
/frappe-test inventory_service --type unit
/frappe-test api.orders --type integration --coverage
```

## Procedure

### Step 1: Analyze Test Target

Identify what needs to be tested:

1. **DocType** — Controller lifecycle hooks, validation, business rules
2. **Service** — Business logic, orchestration, error handling
3. **Repository** — Data access patterns, queries
4. **API** — Endpoints, authentication, input validation
5. **Utility** — Helper functions, formatters

### Step 2: Determine Test Strategy

Based on target, determine appropriate test types:

| Component | Unit Test | Integration Test | E2E Test |
|-----------|-----------|------------------|----------|
| DocType Controller | ✓ (hooks) | ✓ (full lifecycle) | — |
| Service Layer | ✓ (logic) | ✓ (with DB) | — |
| Repository | — | ✓ (queries) | — |
| API Endpoint | ✓ (validation) | ✓ (full request) | ✓ |
| Utility Functions | ✓ | — | — |

### Step 3: Generate Test Structure

Create test directory structure:

```
<app>/tests/
├── __init__.py
├── conftest.py           # Pytest fixtures
├── factories/            # Test data factories
│   ├── __init__.py
│   └── <doctype>_factory.py
├── unit/                 # Unit tests (no DB)
│   ├── __init__.py
│   └── test_<module>.py
├── integration/          # Integration tests (with DB)
│   ├── __init__.py
│   └── test_<module>.py
└── e2e/                  # End-to-end tests
    └── test_workflows.py
```

### Step 4: Generate conftest.py (Pytest Configuration)

```python
"""
Pytest configuration and fixtures for <app>.

Usage:
    bench --site test_site run-tests --app <app>
    bench --site test_site run-tests --app <app> -k "test_name"
"""

import pytest
import frappe
from frappe.tests import IntegrationTestCase
from typing import Generator, Any


# ──────────────────────────────────────────────────────────────────────────────
# Session-scoped Fixtures (run once per test session)
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def app_context():
    """Initialize Frappe app context for testing."""
    # Frappe handles this automatically, but explicit setup can be added here
    yield
    # Cleanup after all tests


@pytest.fixture(scope="session")
def test_admin_user() -> str:
    """Get or create admin user for tests."""
    return "Administrator"


# ──────────────────────────────────────────────────────────────────────────────
# Module-scoped Fixtures (run once per test module)
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def test_user() -> Generator[str, None, None]:
    """
    Create a test user for the module.

    Yields:
        User email/name
    """
    email = "test_user@example.com"

    if not frappe.db.exists("User", email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": "Test",
            "last_name": "User",
            "send_welcome_email": 0
        })
        user.insert(ignore_permissions=True)
        user.add_roles("System Manager")

    yield email

    # Cleanup: optionally delete user after module tests
    # frappe.delete_doc("User", email, force=True)


@pytest.fixture(scope="module")
def api_credentials(test_user: str) -> Generator[dict, None, None]:
    """
    Generate API credentials for test user.

    Yields:
        Dict with api_key and api_secret
    """
    user = frappe.get_doc("User", test_user)

    # Generate API keys if not exists
    api_key = user.api_key or frappe.generate_hash(length=15)
    api_secret = frappe.generate_hash(length=15)

    if not user.api_key:
        user.api_key = api_key
        user.api_secret = api_secret
        user.save(ignore_permissions=True)

    yield {
        "api_key": api_key,
        "api_secret": api_secret,
        "authorization": f"token {api_key}:{api_secret}"
    }


# ──────────────────────────────────────────────────────────────────────────────
# Function-scoped Fixtures (run for each test)
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def as_user(test_user: str) -> Generator[str, None, None]:
    """
    Run test as specific user.

    Usage:
        def test_something(as_user):
            # Test runs as test_user
            pass
    """
    original_user = frappe.session.user
    frappe.set_user(test_user)
    yield test_user
    frappe.set_user(original_user)


@pytest.fixture
def as_guest() -> Generator[str, None, None]:
    """Run test as Guest user."""
    original_user = frappe.session.user
    frappe.set_user("Guest")
    yield "Guest"
    frappe.set_user(original_user)


@pytest.fixture
def rollback_db():
    """
    Rollback database after test.

    Useful for tests that modify data but shouldn't persist changes.
    """
    frappe.db.begin()
    yield
    frappe.db.rollback()


# ──────────────────────────────────────────────────────────────────────────────
# Test Data Fixtures
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_<doctype>(rollback_db) -> Generator[Any, None, None]:
    """
    Create sample <DocType> for testing.

    Yields:
        <DocType> document instance
    """
    from <app>.tests.factories.<doctype>_factory import <DocType>Factory

    doc = <DocType>Factory.create()
    yield doc
    # Cleanup handled by rollback_db


# ──────────────────────────────────────────────────────────────────────────────
# Assertion Helpers
# ──────────────────────────────────────────────────────────────────────────────

@pytest.fixture
def assert_doc_exists():
    """Helper to assert document existence."""
    def _assert(doctype: str, name: str, should_exist: bool = True):
        exists = frappe.db.exists(doctype, name)
        if should_exist:
            assert exists, f"{doctype} {name} should exist but doesn't"
        else:
            assert not exists, f"{doctype} {name} should not exist but does"
    return _assert


@pytest.fixture
def assert_permission():
    """Helper to assert permission checks."""
    def _assert(
        doctype: str,
        ptype: str,
        user: str,
        should_have: bool = True,
        doc: Any = None
    ):
        frappe.set_user(user)
        has_perm = frappe.has_permission(doctype, ptype, doc=doc)
        frappe.set_user("Administrator")

        if should_have:
            assert has_perm, f"{user} should have {ptype} permission on {doctype}"
        else:
            assert not has_perm, f"{user} should not have {ptype} permission on {doctype}"
    return _assert
```

### Step 5: Generate Factory Pattern

Create `<app>/tests/factories/<doctype>_factory.py`:

```python
"""
Factory for creating <DocType> test data.

Usage:
    from <app>.tests.factories.<doctype>_factory import <DocType>Factory

    # Create with defaults
    doc = <DocType>Factory.create()

    # Create with custom values
    doc = <DocType>Factory.create(title="Custom Title", status="Completed")

    # Create without saving (for unit tests)
    doc = <DocType>Factory.build()

    # Create multiple
    docs = <DocType>Factory.create_batch(5)
"""

import frappe
from frappe.utils import today, random_string
from typing import Optional, Any
from dataclasses import dataclass, field


@dataclass
class <DocType>Factory:
    """Factory for <DocType> test documents."""

    # Default values
    title: str = field(default_factory=lambda: f"Test {random_string(8)}")
    date: str = field(default_factory=today)
    status: str = "Draft"
    description: Optional[str] = None

    # Related data (Links)
    # customer: Optional[str] = None

    @classmethod
    def build(cls, **kwargs) -> Any:
        """
        Build document instance without saving.

        Returns:
            Unsaved Document instance
        """
        factory = cls(**kwargs)
        return frappe.get_doc({
            "doctype": "<DocType>",
            "title": factory.title,
            "date": factory.date,
            "status": factory.status,
            "description": factory.description,
        })

    @classmethod
    def create(cls, **kwargs) -> Any:
        """
        Create and save document.

        Returns:
            Saved Document instance
        """
        doc = cls.build(**kwargs)
        doc.insert(ignore_permissions=True)
        return doc

    @classmethod
    def create_batch(cls, count: int, **kwargs) -> list[Any]:
        """
        Create multiple documents.

        Args:
            count: Number of documents to create
            **kwargs: Common attributes for all documents

        Returns:
            List of created documents
        """
        return [cls.create(**kwargs) for _ in range(count)]

    @classmethod
    def create_submitted(cls, **kwargs) -> Any:
        """
        Create and submit document (for submittable DocTypes).

        Returns:
            Submitted Document instance
        """
        doc = cls.create(**kwargs)
        doc.submit()
        return doc

    @classmethod
    def create_with_items(
        cls,
        item_count: int = 3,
        **kwargs
    ) -> Any:
        """
        Create document with child table items.

        Args:
            item_count: Number of items to add
            **kwargs: Document attributes

        Returns:
            Document with child items
        """
        doc = cls.build(**kwargs)

        # Add child items
        for i in range(item_count):
            doc.append("items", {
                "item_code": f"ITEM-{i:03d}",
                "qty": i + 1,
                "rate": 100.0 * (i + 1)
            })

        doc.insert(ignore_permissions=True)
        return doc


# ──────────────────────────────────────────────────────────────────────────────
# Sequence Generator for Unique Values
# ──────────────────────────────────────────────────────────────────────────────

class Sequence:
    """Generate unique sequential values for tests."""

    _counters: dict[str, int] = {}

    @classmethod
    def next(cls, name: str = "default") -> int:
        """Get next value in sequence."""
        cls._counters[name] = cls._counters.get(name, 0) + 1
        return cls._counters[name]

    @classmethod
    def reset(cls, name: Optional[str] = None) -> None:
        """Reset sequence counter(s)."""
        if name:
            cls._counters[name] = 0
        else:
            cls._counters.clear()
```

### Step 6: Generate Integration Tests

Create `<app>/tests/integration/test_<target>.py`:

```python
"""
Integration tests for <Target>.

These tests require database access and test full workflows.

Run with:
    bench --site test_site run-tests --app <app> --module <app>.tests.integration.test_<target>
"""

import pytest
import frappe
from frappe.tests import IntegrationTestCase
from <app>.<module>.services.<target>_service import <Target>Service
from <app>.tests.factories.<doctype>_factory import <DocType>Factory


class Test<Target>Integration(IntegrationTestCase):
    """Integration tests for <Target>."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests in class."""
        super().setUpClass()
        cls.service = <Target>Service()

    def setUp(self):
        """Set up before each test."""
        frappe.set_user("Administrator")

    def tearDown(self):
        """Clean up after each test."""
        frappe.db.rollback()

    # ──────────────────────────────────────────────────────────────────────────
    # CRUD Operations
    # ──────────────────────────────────────────────────────────────────────────

    def test_create_document(self):
        """Test creating a new document through service."""
        data = {
            "title": "Integration Test Document",
            "date": frappe.utils.today(),
            "description": "Created via integration test"
        }

        result = self.service.create(data)

        self.assertIsNotNone(result.get("name"))
        self.assertEqual(result.get("title"), data["title"])

        # Verify in database
        self.assertTrue(
            frappe.db.exists("<DocType>", result["name"])
        )

    def test_create_validates_mandatory_fields(self):
        """Test that mandatory field validation works."""
        with self.assertRaises(frappe.ValidationError) as context:
            self.service.create({})

        self.assertIn("required", str(context.exception).lower())

    def test_update_document(self):
        """Test updating existing document."""
        doc = <DocType>Factory.create()

        result = self.service.update(doc.name, {"title": "Updated Title"})

        self.assertEqual(result["title"], "Updated Title")

        # Verify in database
        db_value = frappe.db.get_value("<DocType>", doc.name, "title")
        self.assertEqual(db_value, "Updated Title")

    def test_update_nonexistent_raises_error(self):
        """Test updating non-existent document raises error."""
        with self.assertRaises(Exception):
            self.service.update("NONEXISTENT-001", {"title": "Test"})

    def test_delete_document(self):
        """Test deleting document."""
        doc = <DocType>Factory.create()
        name = doc.name

        self.service.repo.delete(name)

        self.assertFalse(frappe.db.exists("<DocType>", name))

    # ──────────────────────────────────────────────────────────────────────────
    # Business Logic
    # ──────────────────────────────────────────────────────────────────────────

    def test_submit_workflow(self):
        """Test document submission workflow."""
        doc = <DocType>Factory.create()

        result = self.service.submit(doc.name)

        self.assertEqual(result["status"], "Completed")

        # Verify docstatus
        docstatus = frappe.db.get_value("<DocType>", doc.name, "docstatus")
        self.assertEqual(docstatus, 1)

    def test_cancel_reverses_submission(self):
        """Test cancellation reverses submission effects."""
        doc = <DocType>Factory.create_submitted()

        result = self.service.cancel(doc.name, reason="Test cancellation")

        self.assertEqual(result["status"], "Cancelled")

    def test_cannot_modify_completed_documents(self):
        """Test that completed documents cannot be modified."""
        doc = <DocType>Factory.create(status="Completed")

        with self.assertRaises(frappe.ValidationError):
            self.service.update(doc.name, {"title": "Should Fail"})

    # ──────────────────────────────────────────────────────────────────────────
    # Permissions
    # ──────────────────────────────────────────────────────────────────────────

    def test_unauthorized_user_cannot_create(self):
        """Test that unauthorized users cannot create documents."""
        # Create user without create permission
        test_email = "no_create@example.com"
        if not frappe.db.exists("User", test_email):
            frappe.get_doc({
                "doctype": "User",
                "email": test_email,
                "first_name": "No Create",
                "send_welcome_email": 0
            }).insert(ignore_permissions=True)

        frappe.set_user(test_email)

        with self.assertRaises(frappe.PermissionError):
            self.service.create({"title": "Should Fail"})

    def test_owner_can_read_own_document(self):
        """Test that document owner can read their own document."""
        test_email = "owner_test@example.com"
        if not frappe.db.exists("User", test_email):
            user = frappe.get_doc({
                "doctype": "User",
                "email": test_email,
                "first_name": "Owner",
                "send_welcome_email": 0
            }).insert(ignore_permissions=True)
            user.add_roles("System Manager")

        frappe.set_user(test_email)
        doc = <DocType>Factory.create()

        # Should not raise
        result = self.service.repo.get(doc.name)
        self.assertIsNotNone(result)

    # ──────────────────────────────────────────────────────────────────────────
    # Query & List Operations
    # ──────────────────────────────────────────────────────────────────────────

    def test_get_list_returns_paginated_results(self):
        """Test list retrieval with pagination."""
        # Create test data
        <DocType>Factory.create_batch(15)

        results = self.service.repo.get_list(limit=10, offset=0)

        self.assertLessEqual(len(results), 10)

    def test_get_list_filters_by_status(self):
        """Test filtering list by status."""
        <DocType>Factory.create(status="Draft")
        <DocType>Factory.create(status="Completed")
        <DocType>Factory.create(status="Completed")

        results = self.service.repo.get_by_status("Completed")

        for result in results:
            self.assertEqual(result.get("status"), "Completed")

    def test_search_finds_matching_documents(self):
        """Test search functionality."""
        <DocType>Factory.create(title="Unique Search Term XYZ")
        <DocType>Factory.create(title="Another Document")

        results = self.service.repo.search("Unique Search")

        self.assertTrue(len(results) >= 1)
        self.assertTrue(
            any("Unique" in r.get("title", "") for r in results)
        )

    def test_get_dashboard_stats(self):
        """Test dashboard statistics."""
        <DocType>Factory.create(status="Draft")
        <DocType>Factory.create(status="Completed")

        stats = self.service.get_dashboard_stats()

        self.assertIn("total", stats)
        self.assertIn("draft", stats)
        self.assertIn("completed", stats)
        self.assertGreaterEqual(stats["total"], 2)
```

### Step 7: Generate Unit Tests

Create `<app>/tests/unit/test_<target>.py`:

```python
"""
Unit tests for <Target>.

These tests do NOT require database access.
They test pure logic and validation functions.

Run with:
    bench --site test_site run-tests --app <app> --module <app>.tests.unit.test_<target>
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from frappe.tests import UnitTestCase


class Test<Target>Unit(UnitTestCase):
    """Unit tests for <Target> (no database)."""

    def test_validate_mandatory_fields(self):
        """Test mandatory field validation logic."""
        from <app>.<module>.services.base import BaseService

        service = BaseService()

        # Should raise for missing fields
        with self.assertRaises(Exception):
            service.validate_mandatory({}, ["title", "date"])

        # Should pass with all fields
        service.validate_mandatory(
            {"title": "Test", "date": "2024-01-01"},
            ["title", "date"]
        )

    def test_document_summary_format(self):
        """Test document summary returns correct format."""
        # Mock the document
        mock_doc = Mock()
        mock_doc.name = "TEST-001"
        mock_doc.title = "Test Document"
        mock_doc.status = "Draft"
        mock_doc.date = "2024-01-01"

        mock_doc.get_summary = lambda: {
            "name": mock_doc.name,
            "title": mock_doc.title,
            "status": mock_doc.status,
            "date": str(mock_doc.date)
        }

        summary = mock_doc.get_summary()

        self.assertEqual(summary["name"], "TEST-001")
        self.assertIn("title", summary)
        self.assertIn("status", summary)

    @patch("frappe.db.exists")
    def test_repository_exists_check(self, mock_exists):
        """Test repository existence check."""
        from <app>.<module>.repositories.base import BaseRepository

        class TestRepo(BaseRepository):
            doctype = "Test DocType"

        repo = TestRepo()

        # Test when exists
        mock_exists.return_value = True
        self.assertTrue(repo.exists("TEST-001"))

        # Test when not exists
        mock_exists.return_value = False
        self.assertFalse(repo.exists("TEST-002"))

    def test_status_validation(self):
        """Test status values are valid."""
        valid_statuses = ["Draft", "Pending", "Completed", "Cancelled"]
        invalid_status = "InvalidStatus"

        self.assertIn("Draft", valid_statuses)
        self.assertNotIn(invalid_status, valid_statuses)

    def test_date_formatting(self):
        """Test date formatting utilities."""
        from frappe.utils import getdate, formatdate

        date_str = "2024-01-15"
        date_obj = getdate(date_str)

        self.assertEqual(date_obj.year, 2024)
        self.assertEqual(date_obj.month, 1)
        self.assertEqual(date_obj.day, 15)


class Test<Target>Validation(UnitTestCase):
    """Unit tests for validation logic."""

    def test_title_cannot_be_empty(self):
        """Test that empty titles are rejected."""
        invalid_titles = ["", "   ", None]

        for title in invalid_titles:
            with self.subTest(title=title):
                is_valid = bool(title and str(title).strip())
                self.assertFalse(is_valid)

    def test_valid_title_accepted(self):
        """Test that valid titles are accepted."""
        valid_titles = ["Test", "Test Title", "A", "123"]

        for title in valid_titles:
            with self.subTest(title=title):
                is_valid = bool(title and str(title).strip())
                self.assertTrue(is_valid)
```

### Step 8: Show Test Plan and Confirm

```
## Test Suite Preview

**Target:** <Target>
**Coverage Goal:** >80%

### Test Structure:

📁 <app>/tests/
├── 📄 conftest.py (fixtures)
├── 📁 factories/
│   └── 📄 <doctype>_factory.py
├── 📁 unit/
│   └── 📄 test_<target>.py (12 tests)
└── 📁 integration/
    └── 📄 test_<target>.py (15 tests)

### Test Coverage:

| Category | Tests | Description |
|----------|-------|-------------|
| CRUD | 5 | Create, Read, Update, Delete |
| Business Logic | 4 | Submit, Cancel, Workflows |
| Permissions | 3 | Role-based access control |
| Queries | 3 | List, Filter, Search |
| Validation | 5 | Input validation, edge cases |
| Unit | 7 | Pure logic, no database |

### Commands:

```bash
# Run all tests
bench --site test_site run-tests --app <app>

# Run specific module
bench --site test_site run-tests --module <app>.tests.integration.test_<target>

# Run with coverage
bench --site test_site run-tests --app <app> --coverage
```

---
Create this test suite?
```

### Step 9: Execute and Verify

After approval, create files and run tests:

```bash
bench --site test_site run-tests --app <app> -v
```

## Output Format

```
## Test Suite Created

**Target:** <Target>
**Files:** 4

### Files Created:
- ✅ conftest.py (pytest fixtures)
- ✅ factories/<doctype>_factory.py
- ✅ unit/test_<target>.py (7 tests)
- ✅ integration/test_<target>.py (15 tests)

### Run Tests:

```bash
# All tests
bench --site test_site run-tests --app <app>

# With verbose output
bench --site test_site run-tests --app <app> -v

# Specific test
bench --site test_site run-tests --app <app> -k "test_create"
```

### Coverage Report:
Run `bench --site test_site run-tests --app <app> --coverage` for coverage report.
```

## Rules

1. **Test Isolation** — Each test should be independent, use `rollback_db` fixture
2. **Factory Pattern** — Use factories for test data, never hardcode values
3. **Meaningful Names** — Test names should describe what is being tested
4. **AAA Pattern** — Arrange, Act, Assert structure for each test
5. **Unit vs Integration** — Unit tests = no DB, Integration tests = with DB
6. **Permission Tests** — Always test both authorized and unauthorized access
7. **Edge Cases** — Test empty values, nulls, large inputs, special characters
8. **ALWAYS Confirm** — Never create files without explicit user approval

## Mocking Best Practices

**Mock `frappe.db.commit`** — If code under test calls `frappe.db.commit`, mock it to prevent partial commits:
```python
@patch("myapp.mymodule.frappe.db.commit", new=MagicMock)
def test_something(self):
    # commits are mocked, won't persist to DB
    pass
```

**Use `frappe.flags.in_test`** — Check if running in test context:
```python
if frappe.flags.in_test:  # or frappe.in_test in newer versions
    # Skip external API calls, notifications, etc.
    pass
```

**Test Site Naming** — Run tests on sites starting with `test_` to avoid accidental data loss:
```bash
bench --site test_mysite run-tests --app myapp
```
