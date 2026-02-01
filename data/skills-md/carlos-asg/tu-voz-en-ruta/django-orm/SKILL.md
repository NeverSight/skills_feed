---
name: django-orm
description: >
  Django ORM patterns and best practices with QuerySets, managers, migrations, and django-tenants database operations.
  Trigger: When working with Django models, queries, database operations, or migrations.
license: Apache-2.0
metadata:
  author: Carlos
  version: "1.0"
  scope: [root]
  auto_invoke: "Writing Django ORM queries/models"
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, WebFetch, WebSearch, Task
---

## Django Models with Type Hints (REQUIRED)

```python
from django.db import models
from typing import TypeAlias, Self
from django.utils import timezone

# Type aliases for QuerySets
UserQuerySet: TypeAlias = models.QuerySet["User"]

class Status(models.TextChoices):
    """Use TextChoices for model choices."""
    ACTIVE = "active", "Active"
    INACTIVE = "inactive", "Inactive"
    PENDING = "pending", "Pending"

class User(models.Model):
    # Fields
    name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(unique=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["status", "created_at"]),
        ]
        verbose_name = "User"
        verbose_name_plural = "Users"
        constraints = [
            models.CheckConstraint(
                check=models.Q(name__length__gte=2),
                name="name_min_length"
            )
        ]

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"<User: {self.name} ({self.email})>"

    # Class methods for queries
    @classmethod
    def get_active(cls) -> UserQuerySet:
        """Get all active users."""
        return cls.objects.filter(status=Status.ACTIVE)

    @classmethod
    def get_by_email(cls, email: str) -> Self | None:
        """Get user by email or None."""
        try:
            return cls.objects.get(email=email)
        except cls.DoesNotExist:
            return None

    # Instance methods
    def activate(self) -> None:
        """Activate user and save."""
        self.status = Status.ACTIVE
        self.save(update_fields=["status", "updated_at"])

    def is_active(self) -> bool:
        """Check if user is active."""
        return self.status == Status.ACTIVE
```

## Custom Managers (REQUIRED)

```python
from django.db import models
from django.db.models import QuerySet, Q
from typing import Self

class UserQuerySet(models.QuerySet["User"]):
    """Custom QuerySet with chainable methods."""

    def active(self) -> Self:
        """Filter active users."""
        return self.filter(status=Status.ACTIVE)

    def inactive(self) -> Self:
        """Filter inactive users."""
        return self.filter(status=Status.INACTIVE)

    def search(self, query: str) -> Self:
        """Search users by name or email."""
        return self.filter(
            Q(name__icontains=query) | Q(email__icontains=query)
        )

class UserManager(models.Manager["User"]):
    """Custom manager for User model."""

    def get_queryset(self) -> UserQuerySet:
        """Return custom QuerySet."""
        return UserQuerySet(self.model, using=self._db)

    def active(self) -> UserQuerySet:
        """Proxy to QuerySet method."""
        return self.get_queryset().active()

    def create_user(self, name: str, email: str) -> "User":
        """Create user with defaults."""
        return self.create(
            name=name,
            email=email.lower(),
            status=Status.ACTIVE
        )

# Use in model
class User(models.Model):
    # ... fields ...

    objects = UserManager()  # Replace default manager

    # Usage:
    # User.objects.active()
    # User.objects.active().search("carlos")
```

## QuerySet Operations (REQUIRED)

```python
# Basic queries
users = User.objects.all()
user = User.objects.get(id=1)
users = User.objects.filter(status="active")
users = User.objects.exclude(status="inactive")

# Field lookups
users = User.objects.filter(name__icontains="carlos")  # Case-insensitive
users = User.objects.filter(email__startswith="test")
users = User.objects.filter(created_at__gte=date)
users = User.objects.filter(id__in=[1, 2, 3])

# Q objects for complex queries
from django.db.models import Q

users = User.objects.filter(
    Q(status="active") & (Q(name__icontains="carlos") | Q(email__icontains="carlos"))
)
users = User.objects.filter(~Q(status="inactive"))  # NOT query

# Ordering
users = User.objects.order_by("-created_at")  # Descending
users = User.objects.order_by("name", "-created_at")  # Multiple

# Slicing
users = User.objects.all()[:10]  # First 10
first_user = User.objects.first()  # First or None
last_user = User.objects.last()  # Last or None

# Aggregation
from django.db.models import Count, Avg, Sum, Min, Max

user_count = User.objects.count()
stats = User.objects.aggregate(
    total=Count("id"),
    min_date=Min("created_at"),
    max_date=Max("created_at")
)

# Annotation
users = User.objects.annotate(
    address_count=Count("addresses")
).filter(address_count__gt=1)

# Values and values_list
user_dicts = User.objects.values("id", "name", "email")  # List of dicts
user_tuples = User.objects.values_list("id", "name")  # List of tuples
user_ids = User.objects.values_list("id", flat=True)  # Flat list

# Exists
has_active = User.objects.filter(status="active").exists()

# Bulk operations
User.objects.bulk_create([
    User(name="User 1", email="user1@example.com"),
    User(name="User 2", email="user2@example.com"),
])

User.objects.filter(status="pending").update(status="active")
User.objects.filter(status="inactive").delete()
```

## Select Related and Prefetch Related (REQUIRED)

```python
# ❌ N+1 query problem
users = User.objects.all()
for user in users:
    print(user.profile.bio)  # One query per user!

# ✅ select_related (for ForeignKey and OneToOne)
users = User.objects.select_related("profile").all()
for user in users:
    print(user.profile.bio)  # Single JOIN query

# ✅ Multiple relations
users = User.objects.select_related("profile", "company").all()

# ✅ prefetch_related (for ManyToMany and reverse ForeignKey)
users = User.objects.prefetch_related("addresses").all()
for user in users:
    for address in user.addresses.all():  # No extra queries
        print(address.street)

# ✅ Prefetch with filtering
from django.db.models import Prefetch

users = User.objects.prefetch_related(
    Prefetch(
        "addresses",
        queryset=Address.objects.filter(is_primary=True),
        to_attr="primary_addresses"
    )
).all()

# ✅ Combining both
users = User.objects.select_related("profile").prefetch_related("tags").all()
```

## Transactions (REQUIRED)

```python
from django.db import transaction

# Atomic decorator
@transaction.atomic
def create_user_with_profile(name: str, email: str, bio: str) -> User:
    """Create user and profile in single transaction."""
    user = User.objects.create(name=name, email=email)
    UserProfile.objects.create(user=user, bio=bio)
    return user

# Context manager
def transfer_data(from_user: User, to_user: User) -> None:
    try:
        with transaction.atomic():
            # All or nothing
            from_user.balance -= 100
            to_user.balance += 100
            from_user.save()
            to_user.save()
    except Exception as e:
        # Transaction rolled back automatically
        print(f"Transfer failed: {e}")

# Manual savepoints
def complex_operation() -> None:
    with transaction.atomic():
        sid = transaction.savepoint()
        try:
            user = User.objects.create(name="Test", email="test@example.com")
        except Exception:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
```

## Database Migrations (REQUIRED)

```bash
# Create migration for model changes
python manage.py makemigrations
python manage.py makemigrations users

# django-tenants migration commands
python manage.py migrate_schemas  # All schemas (public + tenants)
python manage.py migrate_schemas --shared  # Public schema only
python manage.py migrate_schemas --schema=tenant1  # Specific tenant
python manage.py migrate_schemas users  # Specific app for all tenants
```

```python
# Data migration with tenant awareness
from django.db import migrations

def populate_tenant_data(apps, schema_editor):
    """Populate data for each tenant."""
    User = apps.get_model("users", "User")

    # This will run once per tenant schema
    User.objects.create(
        name="Tenant Admin",
        email=f"admin@{schema_editor.connection.schema_name}.com",
        status="active"
    )

class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(populate_tenant_data),
    ]
```

## Performance Best Practices

```python
# ✅ Use select_related and prefetch_related
users = User.objects.select_related("profile").prefetch_related("addresses")

# ✅ Use only() to select specific fields
users = User.objects.only("id", "name", "email")

# ✅ Use defer() to exclude fields
users = User.objects.defer("bio", "avatar")

# ✅ Use iterator() for large querysets
for user in User.objects.iterator(chunk_size=1000):
    process_user(user)

# ✅ Use bulk_create for multiple inserts
User.objects.bulk_create([
    User(name=f"User {i}", email=f"user{i}@example.com")
    for i in range(1000)
], batch_size=100)

# ✅ Use update() instead of save() for bulk updates
User.objects.filter(status="pending").update(status="active")

# ✅ Use count() instead of len()
count = User.objects.filter(status="active").count()  # Good
count = len(User.objects.filter(status="active"))  # Bad

# ✅ Use exists() for boolean checks
has_users = User.objects.filter(status="active").exists()  # Good
has_users = User.objects.filter(status="active").count() > 0  # Bad

# ❌ Avoid N+1 queries
# Bad
for user in User.objects.all():
    print(user.profile.bio)  # Query per user

# Good
for user in User.objects.select_related("profile"):
    print(user.profile.bio)  # Single JOIN query
```

## Django ORM Best Practices Checklist

**ALWAYS:**

- ✅ Use type hints for QuerySets with `TypeAlias`
- ✅ Create custom managers and QuerySets for reusable queries
- ✅ Use `select_related` for ForeignKey/OneToOne relationships
- ✅ Use `prefetch_related` for ManyToMany/reverse ForeignKey
- ✅ Use `only()` and `defer()` for field-level optimization
- ✅ Use `update_fields` in save() for partial updates
- ✅ Use `bulk_create()` and `bulk_update()` for batch operations
- ✅ Use `transaction.atomic()` for data consistency
- ✅ Use `exists()` instead of `count() > 0`
- ✅ Use `iterator()` for processing large datasets
- ✅ Create indexes on frequently queried fields
- ✅ Use `django-tenants` migration commands for multi-tenant apps
- ✅ Use `Q` objects for complex queries

**NEVER:**

- ❌ Use `objects.all()` without filtering in production
- ❌ Iterate over querysets without checking count first
- ❌ Use raw SQL unless absolutely necessary
- ❌ Forget to add indexes on foreign keys
- ❌ Use `len()` when `count()` or `exists()` suffices
