---
name: django-clean-drf
description: Create production-quality Django REST Framework APIs using Clean Architecture and SOLID principles. Covers layered architecture (views, use cases, services, models), query optimization (N+1 prevention), pagination/filtering, JWT authentication, permissions, and production deployment. Use when building new Django APIs, implementing domain-driven design, optimizing queries, or configuring authentication. Applies Python 3.12+ and Django 5+ patterns.
---

# Django Clean DRF Architect

## Overview

This skill provides expert guidance for creating Django REST Framework applications following Clean Architecture principles. It enforces a strict layered architecture that separates concerns, maximizes testability, and produces maintainable production-quality code.

**Architecture Layers:**
```
HTTP Layer (Views/Serializers)
    ↓
Application Layer (Use Cases + DTOs)
    ↓
Domain Layer (Services + Models)
    ↓
Infrastructure Layer (ORM, External APIs, Cache)
```

**Key Capabilities:**
- Layered architecture with strict dependency rules (dependencies flow inward only)
- Use Case pattern with dataclass Input/Output DTOs
- Service layer for domain logic (static queries, instance mutations)
- Thin views that delegate to use cases
- Separate Read vs Create/Update serializers
- Explicit error handling without exceptions for business logic
- Modern Python 3.12+ and Django 5+ features
- Full type hints and testability by design

## When to Use

Invoke this skill when you encounter these triggers:

**New Application Setup:**
- "Create a new Django API for..."
- "Start a new DRF project with clean architecture"
- "Set up a new app with layered architecture"
- "Initialize a domain-driven Django application"
- "Scaffold a Django app following SOLID"

**Use Case Implementation:**
- "Create a use case for..."
- "Implement the business logic for..."
- "Add a new operation/action for..."
- "Handle this transaction atomically"

**Service Layer:**
- "Create a service for..."
- "Where should this business logic go?"
- "Implement domain validation for..."
- "Query data following clean architecture"

**Architecture Questions:**
- "How do I structure this Django app?"
- "What layer should handle..."
- "How do I avoid fat views/models?"
- "How do I make this testable?"
- "Apply SOLID principles to Django"

**API Design:**
- "Create API endpoints for..."
- "Design the serializers for..."
- "Implement CRUD for this entity"

## Instructions

Follow this workflow when handling Django Clean DRF requests:

### 1. Analyze Requirements and Establish Context

**Understand the domain:**
- What entities/models are involved?
- What operations/actions are needed?
- What business rules must be enforced?
- Are there external dependencies (APIs, queues)?

**Check existing project structure:**
- Review existing apps and their organization
- Identify patterns already in use
- Check Django/Python versions for feature availability

**Determine scope:**
- Single use case or full CRUD?
- New app or extending existing?
- API-only or includes admin?

### 2. Load Relevant Reference Documentation

Based on the task, reference the appropriate bundled documentation:

**Architecture:**
- **New app setup** → `references/project-structure.md`
- **Use case implementation** → `references/use-cases-pattern.md`
- **Service layer** → `references/services-pattern.md`
- **Models and domain logic** → `references/models-domain.md`
- **Views and serializers** → `references/views-serializers.md`
- **Testing** → `references/testing-clean-arch.md`
- **Complete examples** → `references/examples.md`

**API Development:**
- **Query optimization / N+1** → `references/query-optimization.md`
- **Pagination, filtering, search** → `references/api-patterns.md`
- **Authentication / JWT / Permissions** → `references/authentication.md`
- **Production deployment** → `references/production-api.md`
- **Django Admin for APIs** → `references/django-admin.md`

**Code Quality:**
- **Coding standards / Ruff / Security** → `references/coding-standards.md`

### 3. Implement Following Clean Architecture Principles

**CRITICAL: Layer Dependency Rules**
```
Views → Use Cases → Services → Models
  ↓         ↓           ↓         ↓
Serializers  DTOs    (internal)   ORM
```
- Dependencies flow INWARD only (outer layers depend on inner)
- Never import views in use cases, or use cases in services

**Use Case Pattern:**
```python
from dataclasses import dataclass
from uuid import UUID
from django.db import transaction

@dataclass(frozen=True, slots=True)
class CreateOrderInput:
    customer_id: UUID
    items: list['OrderItemInput']
    notes: str | None = None

@dataclass(frozen=True, slots=True)
class CreateOrderOutput:
    success: bool
    order_id: UUID | None = None
    error: str | None = None

class CreateOrderUseCase:
    def __init__(
        self,
        order_service: OrderService,
        inventory_service: InventoryService,
    ):
        self._order_service = order_service
        self._inventory_service = inventory_service

    @transaction.atomic
    def execute(self, input_dto: CreateOrderInput) -> CreateOrderOutput:
        # Validate
        is_valid, error = self._inventory_service.validate_availability(input_dto.items)
        if not is_valid:
            return CreateOrderOutput(success=False, error=error)

        # Execute
        order = self._order_service.create(
            customer_id=input_dto.customer_id,
            items=input_dto.items,
        )
        return CreateOrderOutput(success=True, order_id=order.id)
```

**Service Pattern:**
```python
class OrderService:
    # STATIC methods for QUERIES (no state changes)
    @staticmethod
    def get_by_id(order_id: UUID) -> Order | None:
        return Order.objects.select_related('customer').filter(id=order_id).first()

    # INSTANCE methods for MUTATIONS (state changes)
    def create(self, customer_id: UUID, items: list[OrderItemInput]) -> Order:
        order = Order.objects.create(customer_id=customer_id)
        for item in items:
            OrderItem.objects.create(order=order, **item.__dict__)
        return order

    # VALIDATION returns tuple[bool, str]
    def validate_can_cancel(self, order: Order) -> tuple[bool, str]:
        if order.status == Order.Status.SHIPPED:
            return False, "Cannot cancel shipped orders"
        return True, ""
```

**Thin View Pattern:**
```python
class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        serializer = CreateOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = CreateOrderUseCase(
            order_service=OrderService(),
            inventory_service=InventoryService(),
        )
        input_dto = CreateOrderInput(**serializer.validated_data)
        output = use_case.execute(input_dto)

        if not output.success:
            return Response({'error': output.error}, status=400)
        return Response({'order_id': str(output.order_id)}, status=201)
```

**Serializer Separation:**
```python
# WRITE serializer (input validation)
class CreateOrderSerializer(serializers.Serializer):
    items = OrderItemInputSerializer(many=True, min_length=1)
    notes = serializers.CharField(max_length=500, required=False)

# READ serializer (output display)
class OrderReadSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.name', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'status', 'created_at']
        read_only_fields = fields
```

**Model with Domain Logic:**
```python
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        SHIPPED = 'shipped', 'Shipped'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['customer', 'status'])]

    @property
    def is_cancellable(self) -> bool:
        return self.status in (self.Status.PENDING, self.Status.CONFIRMED)
```

### 4. Validate and Finalize

**Architecture Checklist:**
- [ ] Views are thin (< 20 lines of logic)
- [ ] Use cases handle single operations
- [ ] Services contain reusable domain logic
- [ ] Dependencies flow inward only
- [ ] No circular imports between layers

**Code Quality Checklist:**
- [ ] Type hints on all public interfaces
- [ ] Dataclass DTOs are frozen with slots
- [ ] No exceptions for business logic errors → return Output
- [ ] Validation returns `tuple[bool, str]`
- [ ] `@transaction.atomic` wraps state changes

**Performance Checklist:**
- [ ] `select_related` for ForeignKey access
- [ ] `prefetch_related` for reverse relations
- [ ] Indexes on frequently queried fields
- [ ] No N+1 queries in serializers

## Directory Structure

```
apps/<app_name>/
├── __init__.py
├── models.py              # Domain entities with @property logic
├── views.py               # Thin HTTP handlers
├── serializers.py         # Read and Write serializers
├── urls.py                # Route definitions
├── admin.py               # Django Admin
├── services/
│   ├── __init__.py        # Export services
│   └── <entity>_service.py
├── use_cases/
│   ├── __init__.py        # Export use cases
│   └── <action>_<entity>.py  # One file per use case
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_services.py
│   ├── test_use_cases.py
│   ├── test_views.py
│   └── factories.py       # Factory Boy factories
└── migrations/
```

## Bundled Resources

**references/** - Comprehensive Clean Architecture and API documentation

### Architecture Patterns

- **`references/project-structure.md`**
  Directory layout, file naming, module organization, dependency rules

- **`references/use-cases-pattern.md`**
  Input/Output DTOs, constructor injection, transaction handling, error handling

- **`references/services-pattern.md`**
  Static vs instance methods, validation patterns, cross-service communication

- **`references/models-domain.md`**
  Domain logic in models, TextChoices, UUID keys, indexes

- **`references/views-serializers.md`**
  Thin views, permissions, Read vs Write serializers

- **`references/testing-clean-arch.md`**
  Unit testing use cases, mocking services, integration tests

- **`references/examples.md`**
  Complete CRUD example, complex workflows, testing examples

### API Best Practices

- **`references/query-optimization.md`**
  N+1 queries, select_related/prefetch_related, indexes, bulk operations, aggregations

- **`references/api-patterns.md`**
  Pagination, filtering, searching, ordering, API versioning, error handling, throttling

- **`references/authentication.md`**
  JWT authentication, permissions, API keys, role-based access, security headers

- **`references/production-api.md`**
  Settings structure, database config, caching, logging, Sentry, health checks, Docker

- **`references/django-admin.md`**
  ModelAdmin configuration, inlines, custom actions, query optimization, permissions, security

### Code Quality

- **`references/coding-standards.md`**
  Ruff configuration, import ordering, security practices, YAGNI, logging, documentation

## Core Principles

### No Exceptions for Business Logic
```python
# BAD
def create_order(self, data):
    if not self.can_create():
        raise ValidationError("Cannot create order")
    return Order.objects.create(**data)

# GOOD
def create_order(self, data) -> CreateOrderOutput:
    if not self.can_create():
        return CreateOrderOutput(success=False, error="Cannot create order")
    order = Order.objects.create(**data)
    return CreateOrderOutput(success=True, order_id=order.id)
```

### Validation Returns Tuples
```python
# BAD
def validate(self, order) -> bool:
    return order.status != 'shipped'

# GOOD
def validate(self, order) -> tuple[bool, str]:
    if order.status == 'shipped':
        return False, "Cannot modify shipped orders"
    return True, ""
```

### Constructor Injection for Testability
```python
# BAD - Hard to test
class CreateOrderUseCase:
    def execute(self, input_dto):
        service = OrderService()  # Hardcoded dependency
        return service.create(input_dto)

# GOOD - Easy to mock
class CreateOrderUseCase:
    def __init__(self, order_service: OrderService):
        self._order_service = order_service

    def execute(self, input_dto):
        return self._order_service.create(input_dto)
```

## Additional Notes

**Python Version:** 3.10+ required (for `X | None` union syntax), 3.12+ recommended
**Django Version:** 4.2 LTS minimum, 5.0+ recommended

**Naming Conventions:**
- Use cases: `<action>_<entity>.py` (e.g., `create_order.py`)
- Services: `<entity>_service.py` (e.g., `order_service.py`)
- Serializers: `<Entity>ReadSerializer`, `<Entity>CreateSerializer`

**Integration with Other Skills:**
- Use `django-celery-expert` for background tasks
- Use `refactordjango` to migrate existing code to this architecture
