---
name: frappe-service
description: |
  Design and implement service layer classes for Frappe Framework v15 with proper business logic separation. Triggers: "create service", "add service layer", "frappe service", "business logic", "/frappe-service". Generates service classes with validation, orchestration, and integration patterns.
---

# Frappe Service Layer Design

Create well-structured service layer classes that encapsulate business logic, coordinate between repositories, and provide clean interfaces for controllers and APIs.

## When to Use

- Implementing complex business logic
- Coordinating operations across multiple DocTypes
- Creating reusable business operations
- Separating concerns between controllers and data access
- Building transaction-aware operations

## Arguments

```
/frappe-service <service_name> [--doctype <doctype>] [--operations <op1,op2>]
```

**Examples:**
```
/frappe-service OrderProcessing --doctype "Sales Order"
/frappe-service InventoryManagement --operations allocate,release,transfer
/frappe-service PaymentGateway
```

## Procedure

### Step 1: Gather Service Requirements

Ask the user for:

1. **Service Name** (PascalCase, e.g., `OrderProcessingService`)
2. **Primary DocType** (if applicable)
3. **Key Operations** to implement
4. **External Integrations** (APIs, payment gateways, etc.)
5. **Transaction Requirements** (atomic operations, rollback needs)

### Step 2: Design Service Architecture

Determine the service pattern:

| Pattern | Use Case | Example |
|---------|----------|---------|
| CRUD Service | Basic DocType operations | `CustomerService` |
| Workflow Service | State transitions, approvals | `ApprovalService` |
| Integration Service | External API calls | `PaymentGatewayService` |
| Orchestration Service | Multi-DocType coordination | `OrderFulfillmentService` |
| Batch Service | Bulk operations | `BulkImportService` |

### Step 3: Generate Service Class

Create `<app>/<module>/services/<service_name>.py`:

```python
"""
<Service Name> Service

<Detailed description of what this service handles>

Responsibilities:
    - <Responsibility 1>
    - <Responsibility 2>
    - <Responsibility 3>

Usage:
    from <app>.<module>.services.<service_name> import <ServiceName>Service

    service = <ServiceName>Service()
    result = service.process_order(order_data)
"""

import frappe
from frappe import _
from frappe.utils import now, today, flt, cint, cstr
from typing import TYPE_CHECKING, Optional, Any, Callable
from contextlib import contextmanager
from functools import wraps

from <app>.<module>.services.base import BaseService
from <app>.<module>.repositories.<doctype>_repository import <DocType>Repository

if TYPE_CHECKING:
    from frappe.model.document import Document


# ──────────────────────────────────────────────────────────────────────────────
# Decorators
# ──────────────────────────────────────────────────────────────────────────────

def require_permission(doctype: str, ptype: str = "read"):
    """Decorator to check permission before method execution."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not frappe.has_permission(doctype, ptype):
                frappe.throw(
                    _("Permission denied: {0} {1}").format(ptype, doctype),
                    frappe.PermissionError
                )
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def with_transaction(func: Callable):
    """Decorator to wrap method in database transaction."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            result = func(self, *args, **kwargs)
            frappe.db.commit()
            return result
        except Exception:
            frappe.db.rollback()
            raise
    return wrapper


def log_operation(operation_name: str):
    """Decorator to log service operation."""
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            frappe.logger().info(f"[{operation_name}] Starting...")
            try:
                result = func(self, *args, **kwargs)
                frappe.logger().info(f"[{operation_name}] Completed successfully")
                return result
            except Exception as e:
                frappe.logger().error(f"[{operation_name}] Failed: {str(e)}")
                raise
        return wrapper
    return decorator


# ──────────────────────────────────────────────────────────────────────────────
# Service Implementation
# ──────────────────────────────────────────────────────────────────────────────

class <ServiceName>Service(BaseService):
    """
    Service for <description>.

    This service handles:
        - <Operation 1>
        - <Operation 2>
        - <Operation 3>

    Architecture:
        Controller/API → Service → Repository → Database

    Example:
        service = <ServiceName>Service()
        order = service.create_order(customer="CUST-001", items=[...])
        service.submit_order(order.name)
    """

    def __init__(self, user: Optional[str] = None):
        super().__init__(user)
        self.repo = <DocType>Repository()
        # Initialize other repositories as needed
        # self.item_repo = ItemRepository()
        # self.customer_repo = CustomerRepository()

    # ──────────────────────────────────────────────────────────────────────────
    # Public Operations (Business Logic)
    # ──────────────────────────────────────────────────────────────────────────

    @require_permission("<DocType>", "create")
    @with_transaction
    @log_operation("create_<doctype>")
    def create(self, data: dict) -> dict:
        """
        Create a new <DocType>.

        Args:
            data: Document data containing:
                - title (str): Required title
                - date (str): Date in YYYY-MM-DD format
                - description (str): Optional description

        Returns:
            Created document summary

        Raises:
            frappe.ValidationError: If validation fails
            frappe.PermissionError: If user lacks permission

        Example:
            service.create({
                "title": "New Order",
                "date": "2024-01-15"
            })
        """
        # 1. Validate input
        self._validate_create_data(data)

        # 2. Apply business rules
        data = self._apply_defaults(data)
        data = self._apply_business_rules(data)

        # 3. Create via repository
        doc = self.repo.create(data)

        # 4. Post-creation actions
        self._on_create(doc)

        # 5. Return summary
        return doc.get_summary()

    @require_permission("<DocType>", "write")
    @with_transaction
    def update(self, name: str, data: dict) -> dict:
        """
        Update existing <DocType>.

        Args:
            name: Document name
            data: Fields to update

        Returns:
            Updated document summary
        """
        doc = self.repo.get_or_throw(name, for_update=True)

        # Validate update is allowed
        self._validate_can_update(doc)

        # Apply update
        doc.update(data)
        doc.save()

        return doc.get_summary()

    @require_permission("<DocType>", "submit")
    @with_transaction
    @log_operation("submit_<doctype>")
    def submit(self, name: str) -> dict:
        """
        Submit document for processing.

        This triggers:
            1. Pre-submission validation
            2. Document submission
            3. Post-submission actions (e.g., stock updates, GL entries)

        Args:
            name: Document name

        Returns:
            Submitted document summary

        Raises:
            frappe.ValidationError: If submission requirements not met
        """
        doc = self.repo.get_or_throw(name, for_update=True)

        # Pre-submission checks
        self._validate_submission(doc)

        # Submit
        doc.submit()

        # Post-submission processing
        self._on_submit(doc)

        return doc.get_summary()

    @require_permission("<DocType>", "cancel")
    @with_transaction
    @log_operation("cancel_<doctype>")
    def cancel(self, name: str, reason: Optional[str] = None) -> dict:
        """
        Cancel submitted document.

        Args:
            name: Document name
            reason: Cancellation reason (recommended)

        Returns:
            Cancelled document summary
        """
        doc = self.repo.get_or_throw(name, for_update=True)

        # Validate cancellation
        self._validate_cancellation(doc)

        # Store reason
        if reason:
            doc.db_set("cancellation_reason", reason, update_modified=False)

        # Cancel
        doc.cancel()

        # Post-cancellation processing
        self._on_cancel(doc)

        return doc.get_summary()

    # ──────────────────────────────────────────────────────────────────────────
    # Complex Business Operations
    # ──────────────────────────────────────────────────────────────────────────

    @with_transaction
    def process_workflow(
        self,
        name: str,
        action: str,
        comment: Optional[str] = None
    ) -> dict:
        """
        Process workflow action on document.

        Args:
            name: Document name
            action: Workflow action (e.g., "Approve", "Reject")
            comment: Optional comment for the action

        Returns:
            Updated document with new workflow state
        """
        doc = self.repo.get_or_throw(name, for_update=True)

        # Validate action is allowed
        allowed_actions = self._get_allowed_workflow_actions(doc)
        if action not in allowed_actions:
            frappe.throw(
                _("Action '{0}' not allowed. Allowed: {1}").format(
                    action, ", ".join(allowed_actions)
                )
            )

        # Apply workflow action
        from frappe.model.workflow import apply_workflow
        apply_workflow(doc, action)

        # Add comment
        if comment:
            doc.add_comment("Workflow", f"{action}: {comment}")

        return doc.get_summary()

    def calculate_totals(self, name: str) -> dict:
        """
        Calculate and update document totals.

        Args:
            name: Document name

        Returns:
            Calculated totals
        """
        doc = self.repo.get_or_throw(name)

        subtotal = sum(
            flt(item.qty) * flt(item.rate)
            for item in doc.get("items", [])
        )

        tax_amount = flt(subtotal) * flt(doc.tax_rate or 0) / 100
        grand_total = flt(subtotal) + flt(tax_amount)

        return {
            "subtotal": subtotal,
            "tax_amount": tax_amount,
            "grand_total": grand_total
        }

    def bulk_operation(
        self,
        names: list[str],
        operation: str,
        **kwargs
    ) -> dict:
        """
        Perform bulk operation on multiple documents.

        Args:
            names: List of document names
            operation: Operation to perform (update_status, submit, cancel)
            **kwargs: Operation-specific arguments

        Returns:
            Results summary
        """
        results = {"success": [], "failed": []}

        for name in names:
            try:
                if operation == "update_status":
                    self.update(name, {"status": kwargs.get("status")})
                elif operation == "submit":
                    self.submit(name)
                elif operation == "cancel":
                    self.cancel(name, kwargs.get("reason"))

                results["success"].append(name)
            except Exception as e:
                results["failed"].append({
                    "name": name,
                    "error": str(e)
                })

        return results

    # ──────────────────────────────────────────────────────────────────────────
    # Query Methods
    # ──────────────────────────────────────────────────────────────────────────

    def get_pending_items(self, limit: int = 50) -> list[dict]:
        """Get items pending action."""
        return self.repo.get_list(
            filters={"status": "Pending", "docstatus": 0},
            fields=["name", "title", "date", "owner", "creation"],
            order_by="creation asc",
            limit=limit
        )

    def get_statistics(self, period: str = "month") -> dict:
        """
        Get statistics for dashboard.

        Args:
            period: Time period (day, week, month, year)

        Returns:
            Statistics dict
        """
        from frappe.utils import add_days, add_months, get_first_day

        today_date = today()

        if period == "day":
            from_date = today_date
        elif period == "week":
            from_date = add_days(today_date, -7)
        elif period == "month":
            from_date = get_first_day(today_date)
        else:  # year
            from_date = add_months(get_first_day(today_date), -12)

        return {
            "total": self.repo.get_count(),
            "period_total": self.repo.get_count(
                {"creation": [">=", from_date]}
            ),
            "by_status": self._get_counts_by_status(),
            "period": period,
            "from_date": from_date
        }

    # ──────────────────────────────────────────────────────────────────────────
    # Private Methods (Internal Logic)
    # ──────────────────────────────────────────────────────────────────────────

    def _validate_create_data(self, data: dict) -> None:
        """Validate data for document creation."""
        self.validate_mandatory(data, ["title"])

        # Custom validations
        if data.get("date") and data["date"] < today():
            frappe.throw(_("Date cannot be in the past"))

    def _validate_can_update(self, doc: "Document") -> None:
        """Validate document can be updated."""
        if doc.docstatus == 2:
            frappe.throw(_("Cannot update cancelled document"))

        if doc.status == "Completed":
            frappe.throw(_("Cannot update completed document"))

    def _validate_submission(self, doc: "Document") -> None:
        """Validate all requirements for submission."""
        if doc.docstatus != 0:
            frappe.throw(_("Document is not in draft state"))

        # Add more validations as needed
        # if not doc.get("items"):
        #     frappe.throw(_("Cannot submit without items"))

    def _validate_cancellation(self, doc: "Document") -> None:
        """Validate document can be cancelled."""
        if doc.docstatus != 1:
            frappe.throw(_("Only submitted documents can be cancelled"))

        # Check for linked documents
        # linked = self._get_linked_submitted_docs(doc.name)
        # if linked:
        #     frappe.throw(_("Cannot cancel. Linked documents exist: {0}").format(linked))

    def _apply_defaults(self, data: dict) -> dict:
        """Apply default values to data."""
        if not data.get("date"):
            data["date"] = today()

        if not data.get("status"):
            data["status"] = "Draft"

        return data

    def _apply_business_rules(self, data: dict) -> dict:
        """Apply business rules to data."""
        # Example: Set posting date to today if not specified
        # Example: Calculate derived fields
        return data

    def _on_create(self, doc: "Document") -> None:
        """Post-creation hook for additional processing."""
        # Send notification
        # frappe.publish_realtime("new_document", {"name": doc.name})
        pass

    def _on_submit(self, doc: "Document") -> None:
        """Post-submission processing."""
        # Create linked records (GL entries, stock ledger, etc.)
        # Update inventory
        # Send notifications
        pass

    def _on_cancel(self, doc: "Document") -> None:
        """Post-cancellation processing."""
        # Reverse linked records
        # Update inventory
        pass

    def _get_allowed_workflow_actions(self, doc: "Document") -> list[str]:
        """Get allowed workflow actions for document."""
        from frappe.model.workflow import get_transitions
        return [t.action for t in get_transitions(doc)]

    def _get_counts_by_status(self) -> dict:
        """Get document counts grouped by status."""
        result = frappe.db.sql("""
            SELECT status, COUNT(*) as count
            FROM `tab<DocType>`
            WHERE docstatus < 2
            GROUP BY status
        """, as_dict=True)

        return {row.status: row.count for row in result}


# ──────────────────────────────────────────────────────────────────────────────
# Service Factory (for dependency injection)
# ──────────────────────────────────────────────────────────────────────────────

def get_<service_name>_service(user: Optional[str] = None) -> <ServiceName>Service:
    """
    Factory function for <ServiceName>Service.

    Use this instead of direct instantiation for easier testing/mocking.

    Args:
        user: Optional user context

    Returns:
        Service instance
    """
    return <ServiceName>Service(user=user)
```

### Step 4: Generate Integration Service Pattern (Optional)

For services that integrate with external APIs:

```python
"""
External Integration Service

Handles communication with external APIs with retry logic,
error handling, and response normalization.
"""

import frappe
from frappe import _
from typing import Optional, Any
import requests
from tenacity import retry, stop_after_attempt, wait_exponential


class <Integration>Service:
    """
    Service for integrating with <External Service>.

    Configuration:
        - API Key: System Settings > <Integration> API Key
        - Base URL: System Settings > <Integration> Base URL
    """

    def __init__(self):
        self.api_key = frappe.db.get_single_value("System Settings", "<integration>_api_key")
        self.base_url = frappe.db.get_single_value("System Settings", "<integration>_base_url")

        if not self.api_key:
            frappe.throw(_("<Integration> API key not configured"))

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None
    ) -> dict:
        """
        Make HTTP request with retry logic.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Request payload

        Returns:
            Response data

        Raises:
            frappe.ValidationError: On API error
        """
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.request(
                method=method,
                url=url,
                json=data,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.Timeout:
            frappe.throw(_("Request timed out. Please try again."))

        except requests.exceptions.HTTPError as e:
            error_msg = self._parse_error_response(e.response)
            frappe.throw(_("API Error: {0}").format(error_msg))

        except requests.exceptions.RequestException as e:
            frappe.throw(_("Connection error: {0}").format(str(e)))

    def _parse_error_response(self, response) -> str:
        """Parse error message from API response."""
        try:
            data = response.json()
            return data.get("message") or data.get("error") or response.text
        except Exception:
            return response.text

    # Public API methods
    def create_external_record(self, data: dict) -> dict:
        """Create record in external system."""
        return self._make_request("POST", "records", data)

    def get_external_record(self, external_id: str) -> dict:
        """Get record from external system."""
        return self._make_request("GET", f"records/{external_id}")

    def sync_records(self) -> dict:
        """Sync records with external system."""
        # Implementation
        pass
```

### Step 5: Show Service Design and Confirm

```
## Service Layer Preview

**Service:** <ServiceName>Service
**Module:** <app>.<module>.services.<service_name>

### Architecture:

```
┌─────────────────────┐
│   Controller/API    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   <ServiceName>     │ ← Business Logic
│      Service        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   <DocType>         │ ← Data Access
│   Repository        │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│     Database        │
└─────────────────────┘
```

### Operations:

| Method | Permission | Description |
|--------|------------|-------------|
| create() | create | Create new document |
| update() | write | Update document |
| submit() | submit | Submit for processing |
| cancel() | cancel | Cancel document |
| process_workflow() | write | Execute workflow action |
| get_statistics() | read | Dashboard stats |

### Features:

- ✅ Permission decorators
- ✅ Transaction management
- ✅ Operation logging
- ✅ Validation layer
- ✅ Business rules separation
- ✅ Factory function for DI

---
Create this service?
```

### Step 6: Execute and Verify

After approval, create service file and run tests.

## Output Format

```
## Service Created

**Name:** <ServiceName>Service
**Path:** <app>/<module>/services/<service_name>.py

### Features:
- ✅ Base service inheritance
- ✅ Repository integration
- ✅ Permission checking
- ✅ Transaction management
- ✅ Business logic methods
- ✅ Factory function

### Usage:

```python
from <app>.<module>.services.<service_name> import <ServiceName>Service

service = <ServiceName>Service()

# Create
result = service.create({"title": "New Record"})

# Submit
service.submit(result["name"])

# Get statistics
stats = service.get_statistics(period="month")
```
```

## Rules

1. **Single Responsibility** — Each service handles one domain/aggregate
2. **Use Repositories** — Services call repositories for data access; repositories handle `frappe.db`/`frappe.get_doc`
3. **Transaction Awareness** — Frappe auto-commits on success; use `@with_transaction` only for explicit rollback needs
4. **Permission Checks** — Always check permissions at service boundary
5. **Validation First** — Validate before any business logic
6. **Factory Pattern** — Use factory function for easier testing/mocking
7. **ALWAYS Confirm** — Never create files without explicit user approval

## Security Guidelines

1. **SQL Injection Prevention** — Use `frappe.db.sql()` with parameterized queries:
   ```python
   # CORRECT: Parameterized
   frappe.db.sql("SELECT name FROM tabUser WHERE email=%s", [email])

   # WRONG: String formatting (SQL injection risk)
   frappe.db.sql(f"SELECT name FROM tabUser WHERE email='{email}'")
   ```

2. **Avoid eval/exec** — Never use `eval()` or `exec()` with user input. Use `frappe.safe_eval()` if code evaluation is absolutely required.

3. **Permission Bypass Awareness** — `frappe.db.set_value()` and `frappe.get_all()` bypass permissions. Use only for system operations, never for user-facing code.

4. **Input Sanitization** — Validate and sanitize all user inputs. Use type annotations for automatic v15 validation.
