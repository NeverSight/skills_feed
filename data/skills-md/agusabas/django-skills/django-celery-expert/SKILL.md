---
name: django-celery-expert
description: Expert Django and Celery guidance for asynchronous task processing. Use when designing background tasks, configuring workers, handling retries and errors, optimizing task performance, implementing periodic tasks, or setting up production monitoring. Follows Celery best practices with Django integration patterns.
---

# Django Celery Expert

## Overview

This skill provides expert guidance for Django applications using Celery for asynchronous task processing. It covers task design patterns, worker configuration, error handling, monitoring, and production deployment strategies.

**Key Capabilities:**
- Task design and implementation patterns
- Worker configuration and scaling
- Error handling and retry strategies
- Periodic/scheduled task management
- Monitoring and observability
- Production deployment best practices

## When to Use

Invoke this skill when you encounter these triggers:

**Task Design:**
- "Create a Celery task for..."
- "Move this to a background job"
- "Process this asynchronously"
- "Handle this outside the request"

**Configuration & Setup:**
- "Configure Celery for Django"
- "Set up task queues"
- "Configure Celery workers"
- "Set up Celery Beat for scheduling"

**Error Handling:**
- "Handle task failures"
- "Implement retry logic"
- "Task keeps failing"
- "Set up dead letter queue"

**Performance & Scaling:**
- "Scale Celery workers"
- "Optimize task throughput"
- "Tasks are too slow"
- "Handle high task volume"

**Monitoring:**
- "Monitor Celery tasks"
- "Set up Flower"
- "Track task progress"
- "Debug stuck tasks"

## Instructions

Follow this workflow when handling Django Celery requests:

### 1. Analyze the Request

**Identify the task type:**
- Simple background task (fire-and-forget)
- Task with result tracking (need to poll for completion)
- Chained/grouped tasks (workflow orchestration)
- Periodic/scheduled tasks (cron-like behavior)
- Long-running tasks (need progress tracking)

**Key questions:**
- Does the caller need the result?
- Should failures be retried?
- Is idempotency required?
- What's the expected execution time?
- How critical is guaranteed execution?

### 2. Load Relevant Reference Documentation

Based on the task type, reference the appropriate bundled documentation:

- **Django-specific patterns** -> `references/django-integration.md`
- **Task implementation** -> `references/task-design-patterns.md`
- **Configuration & setup** -> `references/configuration-guide.md`
- **Error handling & retries** -> `references/error-handling.md`
- **Periodic tasks** -> `references/periodic-tasks.md`
- **Monitoring & debugging** -> `references/monitoring-observability.md`
- **Production deployment** -> `references/production-deployment.md`

### 3. Implement Following Best Practices

**Task design principles:**
- Keep tasks small and focused
- Design for idempotency when possible
- Use explicit task names
- Bind tasks for access to self
- Pass serializable arguments only (IDs, not objects)

**Error handling:**
- Configure appropriate retry behavior
- Use exponential backoff
- Set max retry limits
- Handle specific exceptions appropriately
- Log failures with context

**Performance:**
- Use appropriate serializers (JSON for safety, pickle for Python objects)
- Configure prefetch limits
- Use task routing for prioritization
- Batch operations when appropriate
- Monitor memory usage

### 4. Validate Implementation

Before presenting the solution:
- Verify task is idempotent if retries enabled
- Check serialization of arguments
- Ensure proper error handling
- Verify monitoring/logging is in place
- Consider failure scenarios

## Bundled Resources

**references/** - Comprehensive Celery documentation loaded into context as needed

- **`references/django-integration.md`**
  - transaction.on_commit() for safe task queuing
  - Database as source of truth with recovery tasks
  - Request-task correlation with django-guid
  - Testing Django Celery tasks

- **`references/task-design-patterns.md`**
  - Task signatures and calling patterns
  - Binding and accessing task properties
  - Task inheritance and base classes
  - Workflow patterns (chains, groups, chords)
  - Idempotency and exactly-once delivery

- **`references/configuration-guide.md`**
  - Django-Celery integration setup
  - Broker configuration (Redis, RabbitMQ)
  - Result backend options
  - Worker settings and concurrency
  - Task routing and queues

- **`references/error-handling.md`**
  - Retry strategies and backoff
  - Exception handling patterns
  - Dead letter queues
  - Task rejection and requeue
  - Timeout handling

- **`references/periodic-tasks.md`**
  - Celery Beat configuration
  - Crontab and interval schedules
  - Django database scheduler
  - Dynamic schedule management
  - Timezone considerations

- **`references/monitoring-observability.md`**
  - Flower setup and usage
  - Prometheus/Grafana integration
  - Task event monitoring
  - Logging best practices
  - Debugging stuck tasks

- **`references/production-deployment.md`**
  - Worker deployment patterns
  - Process supervision (systemd, supervisor)
  - Containerized deployments
  - Scaling strategies
  - Health checks and graceful shutdown

## Examples

### Example 1: Basic Background Task

**User Request:**
> "Send welcome emails in the background after user registration"

**Implementation:**
```python
# tasks.py
from celery import shared_task
from django.core.mail import send_mail

@shared_task(bind=True, max_retries=3)
def send_welcome_email(self, user_id):
    from users.models import User

    try:
        user = User.objects.get(id=user_id)
        send_mail(
            subject="Welcome!",
            message=f"Hi {user.name}, welcome to our platform!",
            from_email="noreply@example.com",
            recipient_list=[user.email],
        )
    except User.DoesNotExist:
        pass  # User deleted, skip
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))

# views.py
def register(request):
    user = User.objects.create(...)
    send_welcome_email.delay(user.id)  # Fire and forget
    return redirect('dashboard')
```

### Example 2: Task with Progress Tracking

**User Request:**
> "Process a large CSV import with progress updates"

**Implementation:**
```python
@shared_task(bind=True)
def import_csv(self, file_path, total_rows):
    from myapp.models import Record

    with open(file_path) as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            Record.objects.create(**row)
            if i % 100 == 0:
                self.update_state(
                    state='PROGRESS',
                    meta={'current': i, 'total': total_rows}
                )

    return {'status': 'complete', 'processed': total_rows}

# Check progress
result = import_csv.AsyncResult(task_id)
if result.state == 'PROGRESS':
    progress = result.info.get('current', 0) / result.info.get('total', 1)
```

### Example 3: Workflow with Chains

**User Request:**
> "Process an order: validate inventory, charge payment, then send confirmation"

**Implementation:**
```python
from celery import chain

@shared_task
def validate_inventory(order_id):
    # Returns order_id if valid, raises if not
    order = Order.objects.get(id=order_id)
    if not order.items_in_stock():
        raise ValueError("Items out of stock")
    return order_id

@shared_task
def charge_payment(order_id):
    order = Order.objects.get(id=order_id)
    order.charge()
    return order_id

@shared_task
def send_confirmation(order_id):
    order = Order.objects.get(id=order_id)
    order.send_confirmation_email()

def process_order(order_id):
    workflow = chain(
        validate_inventory.s(order_id),
        charge_payment.s(),
        send_confirmation.s()
    )
    workflow.delay()
```

## Additional Notes

**Common Pitfalls:**
- Passing Django model instances instead of IDs
- Not handling task idempotency with retries
- Missing timeout configuration for long tasks
- Not monitoring task queue depth
- Ignoring result backend cleanup

**Django Integration:**
- Use `django-celery-beat` for database-backed schedules
- Use `django-celery-results` for storing task results in Django
- Configure `CELERY_` settings in Django settings.py
- Use `@shared_task` for reusable apps

**Security:**
- Never pass sensitive data in task arguments
- Use signed serializers if pickle is required
- Restrict Flower access in production
- Validate task arguments
