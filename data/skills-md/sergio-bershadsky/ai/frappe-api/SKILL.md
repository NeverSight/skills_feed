---
name: frappe-api
description: |
  Create secure REST API endpoints for Frappe Framework v15 with proper authentication, permissions, and validation. Triggers: "create api", "new endpoint", "frappe api", "rest api", "whitelist method", "/frappe-api". Generates v2 API compatible endpoints with type validation and security best practices.
---

# Frappe REST API Development

Create secure, well-documented REST API endpoints for Frappe Framework v15 following best practices for authentication, permission checking, and input validation.

## When to Use

- Building custom REST API endpoints
- Exposing service layer methods via HTTP
- Creating public/private API routes
- Implementing webhook handlers
- Building integrations with external systems

## Arguments

```
/frappe-api <endpoint_name> [--doctype <doctype>] [--public]
```

**Examples:**
```
/frappe-api get_dashboard_stats
/frappe-api create_order --doctype "Sales Order"
/frappe-api webhook_handler --public
```

## Procedure

### Step 1: Gather API Requirements

Ask the user for:

1. **Endpoint Name** (snake_case, e.g., `get_dashboard_stats`)
2. **HTTP Methods** supported (GET, POST, PUT, DELETE)
3. **Authentication Type:**
   - Token (API Key + Secret)
   - Session (Cookie-based)
   - OAuth 2.0
   - Public (no auth required - use sparingly)
4. **Parameters** - Input parameters with types
5. **Related DocType** (if applicable)
6. **Allowed Roles** (who can access this endpoint)

### Step 2: Design API Contract

Create the API specification:

```yaml
Endpoint: /api/method/<app>.<module>.api.<endpoint_name>
Methods: GET, POST
Auth: Token | Session
Rate Limit: 100 req/min (if applicable)

Parameters:
  - name: param1
    type: string
    required: true
    description: Description of param1
  - name: param2
    type: integer
    required: false
    default: 10

Response:
  200:
    description: Success
    schema:
      message: object
  400:
    description: Validation Error
  403:
    description: Permission Denied
```

### Step 3: Generate API Module Structure

Create `<app>/<module>/api/<endpoint_name>.py`:

```python
"""
<Endpoint Name> API

<Brief description of what this API does>

Endpoints:
    GET/POST /api/method/<app>.<module>.api.<endpoint_name>.<method_name>

Authentication:
    Token: Authorization: token api_key:api_secret
    Session: Cookie-based after login

Example:
    curl -X POST "https://site.com/api/method/<app>.<module>.api.<endpoint_name>.create" \
        -H "Authorization: token api_key:api_secret" \
        -H "Content-Type: application/json" \
        -d '{"title": "Test"}'
"""

import frappe
from frappe import _
from frappe.utils import cint, cstr, flt
from typing import Optional, Any
from <app>.<module>.services.<service>_service import <Service>Service


# ──────────────────────────────────────────────────────────────────────────────
# API Endpoints
#
# v15 TYPE ANNOTATION VALIDATION:
# Frappe v15 automatically validates function parameter types based on
# Python type hints. For example, if you declare `limit: int`, passing
# a non-integer will raise a validation error automatically.
#
# TRANSACTION HANDLING:
# Frappe automatically commits on successful POST/PUT requests and
# rolls back on exceptions. Manual frappe.db.commit() is rarely needed.
# ──────────────────────────────────────────────────────────────────────────────

@frappe.whitelist()
def get(name: str) -> dict:
    """
    Get single document by name.

    Args:
        name: Document name/ID

    Returns:
        Document data

    Raises:
        frappe.DoesNotExistError: Document not found
        frappe.PermissionError: No read permission

    Example:
        GET /api/method/<app>.<module>.api.<endpoint>.get?name=DOC-00001
    """
    _check_permission("<DocType>", "read")

    service = <Service>Service()
    return {
        "success": True,
        "data": service.get(name)
    }


@frappe.whitelist()
def get_list(
    status: Optional[str] = None,
    limit: int = 20,
    offset: int = 0
) -> dict:
    """
    Get list of documents with optional filtering.

    Args:
        status: Filter by status
        limit: Maximum records to return (default: 20, max: 100)
        offset: Skip N records for pagination

    Returns:
        List of documents with pagination info

    Example:
        GET /api/method/<app>.<module>.api.<endpoint>.get_list?status=Draft&limit=10
    """
    _check_permission("<DocType>", "read")

    # Validate and sanitize inputs
    limit = min(cint(limit) or 20, 100)  # Cap at 100
    offset = max(cint(offset), 0)

    service = <Service>Service()
    filters = {}
    if status:
        filters["status"] = status

    data = service.repo.get_list(
        filters=filters,
        fields=["name", "title", "status", "date", "modified"],
        limit=limit,
        offset=offset
    )
    total = service.repo.get_count(filters)

    return {
        "success": True,
        "data": data,
        "pagination": {
            "total": total,
            "limit": limit,
            "offset": offset,
            "has_more": (offset + limit) < total
        }
    }


@frappe.whitelist(methods=["POST"])
def create(
    title: str,
    date: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Create new document.

    Args:
        title: Document title (required)
        date: Date in YYYY-MM-DD format
        description: Optional description

    Returns:
        Created document data

    Raises:
        frappe.ValidationError: Invalid input data
        frappe.PermissionError: No create permission

    Example:
        POST /api/method/<app>.<module>.api.<endpoint>.create
        Body: {"title": "New Document", "date": "2024-01-15"}
    """
    _check_permission("<DocType>", "create")

    # Validate required fields
    if not title or not cstr(title).strip():
        frappe.throw(_("Title is required"), frappe.ValidationError)

    service = <Service>Service()
    result = service.create({
        "title": cstr(title).strip(),
        "date": date or frappe.utils.today(),
        "description": description
    })

    frappe.db.commit()

    return {
        "success": True,
        "message": _("Document created successfully"),
        "data": result
    }


@frappe.whitelist(methods=["PUT", "POST"])
def update(
    name: str,
    title: Optional[str] = None,
    status: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Update existing document.

    Args:
        name: Document name (required)
        title: New title
        status: New status
        description: New description

    Returns:
        Updated document data

    Example:
        PUT /api/method/<app>.<module>.api.<endpoint>.update
        Body: {"name": "DOC-00001", "title": "Updated Title"}
    """
    _check_permission("<DocType>", "write")

    if not name:
        frappe.throw(_("Document name is required"), frappe.ValidationError)

    # Build update data from provided fields
    update_data = {}
    if title is not None:
        update_data["title"] = cstr(title).strip()
    if status is not None:
        update_data["status"] = status
    if description is not None:
        update_data["description"] = description

    if not update_data:
        frappe.throw(_("No fields to update"), frappe.ValidationError)

    service = <Service>Service()
    result = service.update(name, update_data)

    frappe.db.commit()

    return {
        "success": True,
        "message": _("Document updated successfully"),
        "data": result
    }


@frappe.whitelist(methods=["DELETE", "POST"])
def delete(name: str) -> dict:
    """
    Delete document.

    Args:
        name: Document name to delete

    Returns:
        Success confirmation

    Example:
        DELETE /api/method/<app>.<module>.api.<endpoint>.delete?name=DOC-00001
    """
    _check_permission("<DocType>", "delete")

    if not name:
        frappe.throw(_("Document name is required"), frappe.ValidationError)

    service = <Service>Service()
    service.repo.delete(name)

    frappe.db.commit()

    return {
        "success": True,
        "message": _("Document deleted successfully")
    }


@frappe.whitelist(methods=["POST"])
def submit(name: str) -> dict:
    """
    Submit document for processing.

    Args:
        name: Document name to submit

    Returns:
        Submitted document data

    Example:
        POST /api/method/<app>.<module>.api.<endpoint>.submit
        Body: {"name": "DOC-00001"}
    """
    _check_permission("<DocType>", "submit")

    service = <Service>Service()
    result = service.submit(name)

    frappe.db.commit()

    return {
        "success": True,
        "message": _("Document submitted successfully"),
        "data": result
    }


@frappe.whitelist(methods=["POST"])
def cancel(name: str, reason: Optional[str] = None) -> dict:
    """
    Cancel submitted document.

    Args:
        name: Document name to cancel
        reason: Cancellation reason

    Returns:
        Cancelled document data

    Example:
        POST /api/method/<app>.<module>.api.<endpoint>.cancel
        Body: {"name": "DOC-00001", "reason": "Customer request"}
    """
    _check_permission("<DocType>", "cancel")

    service = <Service>Service()
    result = service.cancel(name, reason)

    frappe.db.commit()

    return {
        "success": True,
        "message": _("Document cancelled successfully"),
        "data": result
    }


# ──────────────────────────────────────────────────────────────────────────────
# Bulk Operations
# ──────────────────────────────────────────────────────────────────────────────

@frappe.whitelist(methods=["POST"])
def bulk_update_status(names: list[str], status: str) -> dict:
    """
    Bulk update status for multiple documents.

    Args:
        names: List of document names
        status: New status to set

    Returns:
        Number of documents updated

    Example:
        POST /api/method/<app>.<module>.api.<endpoint>.bulk_update_status
        Body: {"names": ["DOC-001", "DOC-002"], "status": "Completed"}
    """
    _check_permission("<DocType>", "write")

    if not names or not isinstance(names, list):
        frappe.throw(_("Names must be a non-empty list"), frappe.ValidationError)

    valid_statuses = ["Draft", "Pending", "Completed", "Cancelled"]
    if status not in valid_statuses:
        frappe.throw(
            _("Invalid status. Must be one of: {0}").format(", ".join(valid_statuses)),
            frappe.ValidationError
        )

    service = <Service>Service()
    count = service.repo.bulk_update_status(names, status)

    frappe.db.commit()

    return {
        "success": True,
        "message": _("{0} documents updated").format(count),
        "data": {"updated_count": count}
    }


# ──────────────────────────────────────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────────────────────────────────────

def _check_permission(doctype: str, ptype: str, doc: Any = None) -> None:
    """
    Check if current user has permission.

    Args:
        doctype: DocType to check
        ptype: Permission type (read, write, create, delete, submit, cancel)
        doc: Optional specific document

    Raises:
        frappe.PermissionError: If permission denied
    """
    if not frappe.has_permission(doctype, ptype, doc=doc):
        frappe.throw(
            _("You don't have permission to {0} {1}").format(ptype, doctype),
            frappe.PermissionError
        )


def _validate_request_data(data: dict, required: list[str]) -> None:
    """
    Validate request data has required fields.

    Args:
        data: Request data dict
        required: List of required field names

    Raises:
        frappe.ValidationError: If required fields missing
    """
    missing = [f for f in required if not data.get(f)]
    if missing:
        frappe.throw(
            _("Missing required fields: {0}").format(", ".join(missing)),
            frappe.ValidationError
        )


# ──────────────────────────────────────────────────────────────────────────────
# Public Endpoints (No Auth Required - Use with Caution!)
# ──────────────────────────────────────────────────────────────────────────────

@frappe.whitelist(allow_guest=True)
def ping() -> dict:
    """
    Health check endpoint (public).

    Returns:
        Server status

    Example:
        GET /api/method/<app>.<module>.api.<endpoint>.ping
    """
    return {
        "success": True,
        "message": "pong",
        "timestamp": frappe.utils.now()
    }
```

### Step 4: Generate API v2 Endpoints (Optional)

For v2 REST API pattern, create custom routes in `hooks.py`:

```python
# hooks.py

# Override standard DocType REST endpoints
override_doctype_dashboards = {
    "<DocType>": "<app>.<module>.api.<endpoint>.get_doctype_dashboard"
}

# Custom website routes for cleaner URLs
website_route_rules = [
    {"from_route": "/api/v2/<app>/<endpoint>", "to_route": "<app>.<module>.api.<endpoint>.handle_v2"},
]
```

### Step 5: Generate API Tests

Create `<app>/<module>/api/test_<endpoint_name>.py`:

```python
"""
Tests for <Endpoint Name> API
"""

import frappe
from frappe.tests import IntegrationTestCase


class TestAPI<EndpointName>(IntegrationTestCase):
    """API integration tests."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_user = cls._create_test_user()
        cls.test_doc = cls._create_test_document()

    @classmethod
    def _create_test_user(cls):
        """Create test user with API access."""
        if frappe.db.exists("User", "test_api@example.com"):
            return frappe.get_doc("User", "test_api@example.com")

        user = frappe.get_doc({
            "doctype": "User",
            "email": "test_api@example.com",
            "first_name": "Test",
            "last_name": "API User",
            "send_welcome_email": 0
        }).insert(ignore_permissions=True)
        user.add_roles("System Manager")
        return user

    @classmethod
    def _create_test_document(cls):
        """Create test document."""
        return frappe.get_doc({
            "doctype": "<DocType>",
            "title": "API Test Document",
            "date": frappe.utils.today()
        }).insert()

    def test_get_returns_document(self):
        """Test GET endpoint returns document."""
        from <app>.<module>.api.<endpoint_name> import get

        frappe.set_user(self.test_user.name)
        result = get(self.test_doc.name)

        self.assertTrue(result.get("success"))
        self.assertIsNotNone(result.get("data"))

    def test_get_list_with_pagination(self):
        """Test GET list with pagination."""
        from <app>.<module>.api.<endpoint_name> import get_list

        frappe.set_user(self.test_user.name)
        result = get_list(limit=5, offset=0)

        self.assertTrue(result.get("success"))
        self.assertIn("pagination", result)
        self.assertLessEqual(len(result["data"]), 5)

    def test_create_validates_input(self):
        """Test CREATE validates required fields."""
        from <app>.<module>.api.<endpoint_name> import create

        frappe.set_user(self.test_user.name)

        with self.assertRaises(frappe.ValidationError):
            create(title="")  # Empty title should fail

    def test_create_returns_document(self):
        """Test CREATE returns new document."""
        from <app>.<module>.api.<endpoint_name> import create

        frappe.set_user(self.test_user.name)
        result = create(title="New Test Doc", date=frappe.utils.today())

        self.assertTrue(result.get("success"))
        self.assertIsNotNone(result["data"].get("name"))

    def test_unauthorized_access_denied(self):
        """Test unauthenticated access is denied."""
        from <app>.<module>.api.<endpoint_name> import get

        frappe.set_user("Guest")

        with self.assertRaises(frappe.PermissionError):
            get(self.test_doc.name)

    def test_ping_public_access(self):
        """Test ping endpoint is publicly accessible."""
        from <app>.<module>.api.<endpoint_name> import ping

        frappe.set_user("Guest")
        result = ping()

        self.assertTrue(result.get("success"))
        self.assertEqual(result.get("message"), "pong")
```

### Step 6: Show API Documentation Preview

```
## API Endpoint Preview

**Module:** <app>.<module>.api.<endpoint_name>
**Base URL:** /api/method/<app>.<module>.api.<endpoint_name>

### Endpoints:

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | .get | Token/Session | Get single document |
| GET | .get_list | Token/Session | List with pagination |
| POST | .create | Token/Session | Create document |
| PUT | .update | Token/Session | Update document |
| DELETE | .delete | Token/Session | Delete document |
| POST | .submit | Token/Session | Submit for processing |
| POST | .cancel | Token/Session | Cancel document |
| POST | .bulk_update_status | Token/Session | Bulk status update |
| GET | .ping | Public | Health check |

### Authentication:

```bash
# Token auth (recommended for integrations)
curl -H "Authorization: token api_key:api_secret" \
     https://site.com/api/method/<endpoint>

# Session auth (for browser clients)
# First login, then use session cookie
```

### Files to Create:

📁 <module>/api/
├── 📄 __init__.py
├── 📄 <endpoint_name>.py
└── 📄 test_<endpoint_name>.py

---
Create this API module?
```

### Step 7: Execute and Verify

After approval, create files and run tests:

```bash
bench --site <site> run-tests --module "<app>.<module>.api.test_<endpoint_name>"
```

## Output Format

```
## API Created

**Module:** <app>.<module>.api.<endpoint_name>
**Endpoints:** 9

### Files Created:
- ✅ <endpoint_name>.py (API endpoints)
- ✅ test_<endpoint_name>.py (API tests)
- ✅ Updated __init__.py

### cURL Examples:

```bash
# Get document
curl -X GET "https://site.com/api/method/<app>.<module>.api.<endpoint>.get?name=DOC-001" \
     -H "Authorization: token api_key:api_secret"

# Create document
curl -X POST "https://site.com/api/method/<app>.<module>.api.<endpoint>.create" \
     -H "Authorization: token api_key:api_secret" \
     -H "Content-Type: application/json" \
     -d '{"title": "New Document"}'
```

### Next Steps:
1. Create API keys: Setup > User > API Access
2. Test endpoints with curl or Postman
3. Run API tests: `bench --site <site> run-tests --module <test_module>`
```

## Rules

1. **Always Check Permissions** — Every endpoint must call `_check_permission()` first
2. **Validate All Input** — Never trust user input, validate and sanitize everything
3. **Type Annotations** — Use Python type hints for v15 auto-validation
4. **Transaction Handling** — Frappe auto-commits on successful requests; manual `frappe.db.commit()` rarely needed except in background jobs
5. **Public Endpoints** — Use `allow_guest=True` sparingly, only for truly public data
6. **Error Handling** — Use `frappe.throw()` with appropriate exception types
7. **Documentation** — Every endpoint must have docstring with Args/Returns/Example
8. **ALWAYS Confirm** — Never create files without explicit user approval
