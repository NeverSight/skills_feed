---
name: django-dev-unfold
description: |
  This skill should be used when the user asks to "set up unfold admin", "django admin",
  "customize admin", "admin dashboard", "htmx admin", "unfold theme", or mentions Django admin
  customization, admin dashboards, or Unfold configuration. Provides Unfold admin patterns
  with 1-admin-per-file organization and HTMX customization.
---

# Unfold Admin Development

Django Unfold admin patterns with modern UI and HTMX customization.

## Core Principles

1. **One admin = one file** - Each ModelAdmin in its own file
2. **Unfold base classes** - Extend UnfoldAdmin classes
3. **HTMX for dynamics** - Use HTMX for interactive features
4. **Dashboard first** - Custom dashboards for data visualization
5. **Tailwind styling** - Consistent Tailwind CSS classes

## Installation

```bash
pip install django-unfold
```

## Configuration

```python
# config/settings.py (with Dynaconf)
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",  # Optional
    "django.contrib.admin",
    # ... other apps
]

# Unfold configuration
UNFOLD = {
    "SITE_TITLE": "My Admin",
    "SITE_HEADER": "My Admin",
    "SITE_URL": "/",
    "SITE_SYMBOL": "speed",  # Material Symbols icon
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "config.settings.environment_callback",
    "COLORS": {
        "primary": {
            "50": "250 245 255",
            "100": "243 232 255",
            "200": "233 213 255",
            "300": "216 180 254",
            "400": "192 132 252",
            "500": "168 85 247",
            "600": "147 51 234",
            "700": "126 34 206",
            "800": "107 33 168",
            "900": "88 28 135",
            "950": "59 7 100",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Navigation",
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": "Users",
                        "icon": "people",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                ],
            },
        ],
    },
}


def environment_callback(request):
    """Show environment badge in admin."""
    from config.settings import settings
    env = settings.current_env
    if env == "production":
        return ["Production", "danger"]
    elif env == "staging":
        return ["Staging", "warning"]
    return ["Development", "info"]
```

## Admin Structure

```
myapp/
└── admin/
    ├── __init__.py           # Register all admins
    ├── base.py               # Base admin classes
    ├── user.py               # UserAdmin
    ├── product.py            # ProductAdmin
    └── order.py              # OrderAdmin
```

## Base Admin Classes

In `admin/base.py`:

```python
from django.contrib import admin
from unfold.admin import ModelAdmin


class BaseModelAdmin(ModelAdmin):
    """Base admin with common configuration."""

    list_per_page = 25
    show_full_result_count = False

    # Unfold features
    compressed_fields = True
    warn_unsaved_form = True

    def get_queryset(self, request):
        """Exclude soft-deleted by default."""
        qs = super().get_queryset(request)
        if hasattr(self.model, "deleted_at"):
            qs = qs.filter(deleted_at__isnull=True)
        return qs


class ReadOnlyModelAdmin(BaseModelAdmin):
    """Admin for read-only models."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
```

## ModelAdmin Template

Each admin in its own file (`admin/user.py`):

```python
from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from unfold.decorators import display

from ..models import User
from .base import BaseModelAdmin


@admin.register(User)
class UserAdmin(BaseModelAdmin):
    list_display = ["email", "name", "display_status", "created_at"]
    list_filter = ["is_active", "created_at"]
    search_fields = ["email", "name"]
    ordering = ["-created_at"]

    readonly_fields = ["id", "created_at", "updated_at"]

    fieldsets = [
        (None, {
            "fields": ["id", "email", "name"],
        }),
        ("Status", {
            "fields": ["is_active"],
            "classes": ["collapse"],
        }),
        ("Timestamps", {
            "fields": ["created_at", "updated_at"],
            "classes": ["collapse"],
        }),
    ]

    @display(
        description="Status",
        label={
            True: "success",
            False: "danger",
        },
    )
    def display_status(self, obj):
        return obj.is_active
```

## Admin Init

Register all admins in `admin/__init__.py`:

```python
from .user import UserAdmin
from .product import ProductAdmin
from .order import OrderAdmin

__all__ = [
    "UserAdmin",
    "ProductAdmin",
    "OrderAdmin",
]
```

## Display Decorators

Unfold provides display decorators for styled output:

```python
from unfold.decorators import display


@display(
    description="Status",
    label={
        "active": "success",
        "pending": "warning",
        "cancelled": "danger",
    },
)
def display_status(self, obj):
    return obj.status


@display(
    description="Amount",
    ordering="total_amount",
)
def display_amount(self, obj):
    return f"${obj.total_amount:,.2f}"


@display(
    description="Actions",
    header=True,  # Show in header row
)
def display_actions(self, obj):
    return format_html(
        '<a href="{}" class="btn btn-sm btn-primary">View</a>',
        obj.get_absolute_url(),
    )
```

## Filters

Unfold filter types:

```python
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RangeDateTimeFilter,
    SingleNumericFilter,
    RangeNumericFilter,
    SliderNumericFilter,
    DropdownFilter,
    ChoicesDropdownFilter,
    RelatedDropdownFilter,
    AutocompleteSelectFilter,
)


@admin.register(Order)
class OrderAdmin(BaseModelAdmin):
    list_filter = [
        ("created_at", RangeDateFilter),
        ("total_amount", RangeNumericFilter),
        ("status", ChoicesDropdownFilter),
        ("user", RelatedDropdownFilter),
    ]
```

## Inline Admin

```python
from unfold.admin import TabularInline, StackedInline


class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ["subtotal"]

    def subtotal(self, obj):
        return obj.quantity * obj.unit_price


@admin.register(Order)
class OrderAdmin(BaseModelAdmin):
    inlines = [OrderItemInline]
```

## HTMX Actions

See `references/customization.md` for HTMX patterns including:
- Dynamic field updates
- Inline actions
- Modal dialogs
- Live search

## Dashboard

Custom dashboard in `admin/dashboard.py`. See `references/customization.md`.

## Additional Resources

### Reference Files

- **`references/customization.md`** - HTMX patterns, dashboard setup, custom widgets

### Related Skills

- **django-dev** - Core Django patterns
- **django-dev-test** - Testing admin functionality
