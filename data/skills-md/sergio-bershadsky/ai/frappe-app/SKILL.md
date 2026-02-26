---
name: frappe-app
description: |
  Scaffold a new Frappe Framework v15 application with multi-layer architecture. Triggers: "create frappe app", "new frappe app", "scaffold frappe", "frappe app structure", "/frappe-app". Creates production-ready app structure with service layer, repository pattern, proper module organization, and v15 best practices.
---

# Frappe App Scaffolding

Create a professional Frappe Framework v15 application with multi-layer architecture following enterprise best practices.

## When to Use

- Starting a new Frappe/ERPNext custom application
- Need production-ready app structure with proper separation of concerns
- Want multi-layer architecture (Controller → Service → Repository)
- Building apps that require clean, maintainable code organization

## Arguments

```
/frappe-app <app_name> [--module <module_name>]
```

**Examples:**
```
/frappe-app inventory_management
/frappe-app hr_extension --module Human Resources
```

## Procedure

### Step 1: Gather Requirements

Ask the user for:

1. **App name** (snake_case, e.g., `inventory_pro`)
2. **App title** (human-readable, e.g., "Inventory Pro")
3. **Primary module name** (e.g., "Inventory", "HR", "Sales")
4. **Brief description** of the app's purpose

Verify the current working directory is within a `frappe-bench/apps` folder:

```bash
pwd
ls -la
```

### Step 2: Generate App Structure

Create the following multi-layer architecture:

```
<app_name>/
├── <app_name>/
│   ├── __init__.py
│   ├── hooks.py                    # App hooks and integrations
│   ├── modules.txt                 # Module definitions
│   ├── patches.txt                 # Database migrations
│   ├── <module_name>/              # Primary module
│   │   ├── __init__.py
│   │   ├── doctype/               # DocType definitions
│   │   │   └── __init__.py
│   │   ├── api/                   # REST API endpoints (v2)
│   │   │   └── __init__.py
│   │   ├── services/              # Business logic layer
│   │   │   └── __init__.py
│   │   ├── repositories/          # Data access layer
│   │   │   └── __init__.py
│   │   └── report/                # Custom reports
│   │       └── __init__.py
│   ├── public/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   │   ├── includes/
│   │   └── pages/
│   ├── www/                       # Portal pages
│   └── tests/
│       ├── __init__.py
│       └── test_utils.py
├── pyproject.toml
├── README.md
└── license.txt
```

### Step 3: Create Core Files

#### pyproject.toml

```toml
[project]
name = "<app_name>"
version = "0.0.1"
description = "<description>"
authors = [
    {name = "<author>", email = "<email>"}
]
requires-python = ">=3.10"
readme = "README.md"
license = {text = "MIT"}

dependencies = [
    "frappe>=15.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0.0",
    "pytest-cov>=4.0.0",
]

[build-system]
requires = ["flit_core>=3.9"]
build-backend = "flit_core.buildapi"

[tool.pytest.ini_options]
testpaths = ["<app_name>/tests"]
python_files = "test_*.py"
```

#### hooks.py

```python
app_name = "<app_name>"
app_title = "<App Title>"
app_publisher = "<Author>"
app_description = "<Description>"
app_email = "<email>"
app_license = "MIT"

# Required Frappe version
required_apps = ["frappe"]

# v15: Enable type annotations in controllers
export_python_type_annotations = True

# Includes in <head>
# app_include_css = "/assets/<app_name>/css/<app_name>.css"
# app_include_js = "/assets/<app_name>/js/<app_name>.js"

# Document Events - prefer controller methods over hooks when possible
# doc_events = {
#     "DocType Name": {
#         "validate": "<app_name>.<module>.services.validation.validate_document",
#         "on_submit": "<app_name>.<module>.services.workflow.on_submit",
#     }
# }

# Scheduled Tasks
# scheduler_events = {
#     "daily": [
#         "<app_name>.<module>.tasks.daily_cleanup"
#     ],
#     "cron": {
#         "0 9 * * *": [
#             "<app_name>.<module>.tasks.morning_report"
#         ]
#     }
# }

# Permissions - override for custom logic
# has_permission = {
#     "DocType Name": "<app_name>.<module>.permissions.has_permission"
# }

# Fixtures - data to export/import
# fixtures = [
#     {"dt": "Custom Field", "filters": [["module", "=", "<module_name>"]]},
#     {"dt": "Property Setter", "filters": [["module", "=", "<module_name>"]]},
# ]

# User Data Protection
# user_data_fields = [
#     {"doctype": "DocType Name", "match_field": "owner", "personal_fields": ["email", "phone"]}
# ]
```

#### Base Service Class

Create `<app_name>/<module>/services/base.py`:

```python
"""
Base service class providing common functionality for all services.
Services contain business logic and orchestrate operations.
"""

import frappe
from frappe import _
from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from frappe.model.document import Document


class BaseService:
    """
    Base class for all service layer classes.

    Services should:
    - Contain business logic
    - Coordinate between repositories
    - Handle transactions
    - Validate business rules
    """

    def __init__(self, user: Optional[str] = None):
        self.user = user or frappe.session.user

    def check_permission(
        self,
        doctype: str,
        ptype: str = "read",
        doc: Optional["Document"] = None,
        throw: bool = True
    ) -> bool:
        """Check if current user has permission."""
        return frappe.has_permission(
            doctype=doctype,
            ptype=ptype,
            doc=doc,
            user=self.user,
            throw=throw
        )

    def validate_mandatory(self, data: dict, fields: list[str]) -> None:
        """Validate that mandatory fields are present."""
        missing = [f for f in fields if not data.get(f)]
        if missing:
            frappe.throw(
                _("Missing required fields: {0}").format(", ".join(missing))
            )

    def log_activity(
        self,
        doctype: str,
        docname: str,
        action: str,
        details: Optional[dict] = None
    ) -> None:
        """Log service activity for audit trail."""
        frappe.get_doc({
            "doctype": "Comment",
            "comment_type": "Info",
            "reference_doctype": doctype,
            "reference_name": docname,
            "content": f"{action}: {details}" if details else action
        }).insert(ignore_permissions=True)
```

#### Base Repository Class

Create `<app_name>/<module>/repositories/base.py`:

```python
"""
Base repository class for data access operations.
Repositories handle all database interactions.
"""

import frappe
from frappe.query_builder import DocType
from typing import TYPE_CHECKING, Optional, Any, TypeVar, Generic

if TYPE_CHECKING:
    from frappe.model.document import Document

T = TypeVar("T", bound="Document")


class BaseRepository(Generic[T]):
    """
    Base class for all repository layer classes.

    Repositories should:
    - Handle all database operations
    - Provide clean data access interface
    - Abstract SQL/ORM details
    - Never contain business logic

    Performance Notes:
    - Use get_cached() for repeated reads of same document
    - Use get_value() when you only need 1-2 fields (faster than get_doc)
    - get_list() applies user permissions; use get_all() to bypass (internal use only)
    """

    doctype: str = ""

    def __init__(self):
        if not self.doctype:
            raise ValueError("Repository must define doctype attribute")

    def get(self, name: str, for_update: bool = False) -> Optional[T]:
        """
        Get document by name. Fetches ALL fields and child tables.

        For better performance when reading 1-2 fields, use get_value() instead.
        For repeated reads of same document, use get_cached() instead.
        """
        if not frappe.db.exists(self.doctype, name):
            return None
        return frappe.get_doc(self.doctype, name, for_update=for_update)

    def get_cached(self, name: str) -> Optional[T]:
        """
        Get document with caching. Use for repeated reads within same request.

        Returns cached version if available, otherwise fetches and caches.
        Cache is automatically invalidated when document is saved.
        Can provide 10000x+ performance improvement for repeated reads.
        """
        if not frappe.db.exists(self.doctype, name):
            return None
        return frappe.get_cached_doc(self.doctype, name)

    def get_or_throw(self, name: str, for_update: bool = False) -> T:
        """Get document by name or throw if not found."""
        doc = self.get(name, for_update=for_update)
        if not doc:
            frappe.throw(f"{self.doctype} {name} not found")
        return doc

    def exists(self, name: str) -> bool:
        """Check if document exists."""
        return frappe.db.exists(self.doctype, name)

    def get_list(
        self,
        filters: Optional[dict] = None,
        fields: Optional[list[str]] = None,
        order_by: str = "modified desc",
        limit: int = 20,
        offset: int = 0
    ) -> list[dict]:
        """
        Get list of documents with user permission filtering.

        Note: This applies user permissions automatically.
        For internal/admin queries without permission checks, use get_all().
        """
        return frappe.get_list(
            self.doctype,
            filters=filters,
            fields=fields or ["name"],
            order_by=order_by,
            limit_page_length=limit,
            limit_start=offset
        )

    def get_all(
        self,
        filters: Optional[dict] = None,
        fields: Optional[list[str]] = None,
        order_by: str = "modified desc",
        limit: int = 20,
        offset: int = 0
    ) -> list[dict]:
        """
        Get list of documents WITHOUT permission filtering.

        WARNING: Use only for internal/system operations.
        For user-facing queries, use get_list() instead.
        """
        return frappe.get_all(
            self.doctype,
            filters=filters,
            fields=fields or ["name"],
            order_by=order_by,
            limit_page_length=limit,
            limit_start=offset
        )

    def get_count(self, filters: Optional[dict] = None) -> int:
        """Get count of documents matching filters."""
        return frappe.db.count(self.doctype, filters=filters)

    def create(self, data: dict) -> T:
        """Create new document."""
        doc = frappe.get_doc({"doctype": self.doctype, **data})
        doc.insert()
        return doc

    def update(self, name: str, data: dict) -> T:
        """Update existing document."""
        doc = self.get_or_throw(name, for_update=True)
        doc.update(data)
        doc.save()
        return doc

    def delete(self, name: str) -> None:
        """Delete document."""
        frappe.delete_doc(self.doctype, name)

    def get_value(
        self,
        name: str,
        fieldname: str | list[str]
    ) -> Any:
        """Get specific field value(s) from document."""
        return frappe.db.get_value(self.doctype, name, fieldname)

    def set_value(self, name: str, fieldname: str, value: Any) -> None:
        """
        Set specific field value directly in database.

        WARNING: This bypasses controller validations and hooks.
        Use doc.save() if you need validations to run.
        """
        frappe.db.set_value(self.doctype, name, fieldname, value)
```

### Step 4: Create Test Utilities

Create `<app_name>/tests/test_utils.py`:

```python
"""
Test utilities and fixtures for <app_name>.
"""

import frappe
from frappe.tests import IntegrationTestCase, UnitTestCase


class <AppName>TestCase(IntegrationTestCase):
    """
    Base test case for <app_name> integration tests.

    Usage:
        class TestMyFeature(<AppName>TestCase):
            def test_something(self):
                # Test with full database access
                pass
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Setup test data

    @classmethod
    def tearDownClass(cls):
        # Cleanup test data
        super().tearDownClass()

    def create_test_user(self, email: str, roles: list[str] = None) -> str:
        """Create a test user with specified roles."""
        if frappe.db.exists("User", email):
            return email

        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": "Test",
            "last_name": "User",
            "send_welcome_email": 0
        })
        user.insert(ignore_permissions=True)

        for role in (roles or []):
            user.add_roles(role)

        return email


class <AppName>UnitTestCase(UnitTestCase):
    """
    Base test case for <app_name> unit tests (no database).
    """
    pass
```

### Step 5: Show Summary and Confirm

Present the complete structure to user:

```
## App Structure Preview

**App:** <app_name>
**Title:** <App Title>
**Module:** <Module Name>

### Files to Create:

📁 <app_name>/
├── 📁 <app_name>/
│   ├── 📄 __init__.py
│   ├── 📄 hooks.py
│   ├── 📄 modules.txt
│   ├── 📄 patches.txt
│   ├── 📁 <module>/
│   │   ├── 📁 api/
│   │   ├── 📁 services/
│   │   │   └── 📄 base.py
│   │   ├── 📁 repositories/
│   │   │   └── 📄 base.py
│   │   └── 📁 doctype/
│   ├── 📁 public/
│   ├── 📁 templates/
│   └── 📁 tests/
│       └── 📄 test_utils.py
├── 📄 pyproject.toml
├── 📄 README.md
└── 📄 license.txt

### Architecture Layers:

1. **Controllers** (doctype/) - Handle HTTP requests, call services
2. **Services** (services/) - Business logic, validation, orchestration
3. **Repositories** (repositories/) - Data access, database queries

---
Create this app structure?
```

Wait for user confirmation.

### Step 6: Execute Creation

After approval:

1. Create all directories
2. Create all files with proper content
3. Replace all placeholders with actual values

### Step 7: Verify and Guide

```bash
ls -la <app_name>/
```

Provide next steps:

```
## App Created Successfully

**Next Steps:**

1. Install the app:
   ```bash
   bench get-app /path/to/<app_name>
   bench --site <site> install-app <app_name>
   ```

2. Create your first DocType:
   ```
   /frappe-doctype <doctype_name>
   ```

3. Add API endpoints:
   ```
   /frappe-api <endpoint_name>
   ```

4. Run tests:
   ```bash
   bench --site <site> run-tests --app <app_name>
   ```

**Documentation:**
- Frappe v15 Docs: https://docs.frappe.io/framework/v15
- Migration Guide: https://github.com/frappe/frappe/wiki/Migrating-to-version-15
```

## Rules

1. **v15 Compatibility** — All generated code must be compatible with Frappe Framework v15
2. **Type Annotations** — Use Python type hints for all function signatures
3. **Multi-Layer Architecture** — Enforce Controller → Service → Repository pattern
4. **No Business Logic in Controllers** — Controllers should only call services
5. **ALWAYS Confirm** — Never create files without explicit user approval
6. **snake_case** — App names must be snake_case
7. **Module Organization** — Each module should be self-contained with its own services/repositories
