---
name: django-conventions
description: Comprehensive Django best practices covering project structure, models (field choices, Meta options, managers, QuerySets, migrations), views (CBVs vs FBVs, generic views), Django REST Framework (serializers, ViewSets, permissions), forms, templates, security (CSRF, XSS, SQL injection), performance (N+1 queries, select_related, prefetch_related, caching), testing, and common anti-patterns. Essential reference for Django code reviews and development.
allowed-tools: Read, Write, Grep, Glob
---

# Django Conventions and Best Practices

## Purpose

This skill provides comprehensive Django best practices and conventions to ensure high-quality, secure, and performant Django applications. It serves as a reference guide during code reviews to verify adherence to Django standards and community best practices.

**When to use this skill:**
- Conducting code reviews of Django projects
- Designing Django applications and models
- Writing Django views, serializers, and forms
- Evaluating Django security and performance
- Refactoring Django codebases
- Teaching Django best practices to team members

This skill is designed to be referenced by the `uncle-duke-python` agent during Django code reviews.

## Context

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. This skill documents industry-standard Django practices that emphasize:

- **Convention over Configuration**: Follow Django's conventions for predictability
- **Don't Repeat Yourself (DRY)**: Minimize code duplication
- **Explicit is better than implicit**: Clear, readable code
- **Security by default**: Leverage Django's built-in security features
- **Database efficiency**: Optimize queries and avoid common performance pitfalls
- **Maintainability**: Write code that's easy to understand and modify

## Prerequisites

**Required Knowledge:**
- Python fundamentals and best practices
- Understanding of web development concepts (HTTP, REST, MVC/MTV)
- Basic understanding of Django's MTV (Model-Template-View) architecture
- SQL and database concepts

**Required Tools:**
- Django 3.2+ (LTS recommended)
- Python 3.8+
- Database (PostgreSQL recommended for production)

**Expected Project Structure:**
```
myproject/
├── manage.py
├── myproject/              # Project configuration
│   ├── __init__.py
│   ├── settings/           # Split settings by environment
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── development.py
│   │   ├── production.py
│   │   └── test.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # Django apps
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── managers.py
│   │   ├── tests/
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│   │   │   └── test_serializers.py
│   │   └── migrations/
│   └── core/
├── static/
├── media/
├── templates/
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   ├── production.txt
│   └── test.txt
└── README.md
```

---

## Instructions

### Task 1: Django Project Structure Best Practices

#### 1.1 Project Layout

**Rule:** Organize Django projects with clear separation between project configuration and apps.

✅ **Good Project Structure:**
```
myproject/
├── manage.py
├── myproject/              # Project settings and configuration
│   ├── settings/
│   │   ├── base.py        # Shared settings
│   │   ├── development.py # Dev-specific settings
│   │   ├── production.py  # Production settings
│   │   └── test.py        # Test settings
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── apps/                   # All Django apps
│   ├── users/
│   ├── blog/
│   └── core/              # Shared utilities
├── static/                # Static files
├── media/                 # User-uploaded files
├── templates/             # Shared templates
├── requirements/          # Split requirements
└── docs/                  # Documentation
```

❌ **Bad:**
```
myproject/
├── manage.py
├── settings.py            # All settings in one file
├── users.py               # Apps not properly organized
├── blog.py
└── utils.py               # Mixed concerns
```

**Why:** Clear structure improves maintainability, makes settings management easier, and follows Django community standards.

#### 1.2 App Organization

**Rule:** Each app should be focused on a single domain concept.

✅ **Good App Structure:**
```
users/
├── __init__.py
├── models.py              # User-related models
├── views.py               # User views
├── serializers.py         # DRF serializers
├── urls.py                # App-specific URLs
├── admin.py               # Admin configuration
├── apps.py                # App configuration
├── managers.py            # Custom model managers
├── forms.py               # Forms
├── signals.py             # Signal handlers
├── permissions.py         # Custom permissions
├── utils.py               # App-specific utilities
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_views.py
│   └── factories.py       # Test factories
└── migrations/
```

**App Naming Conventions:**
- Use plural nouns for apps containing models (users, posts, comments)
- Use singular nouns for utility apps (core, common, utils)
- Keep app names short and descriptive
- Use underscores for multi-word names (user_profiles)

#### 1.3 Settings Organization

**Rule:** Split settings by environment for security and flexibility.

✅ **Good Settings Structure:**

**`settings/base.py`:**
```python
"""Base settings shared across all environments."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# This should be overridden in environment-specific settings
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'dev-only-secret-key')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'django_filters',
    # Local apps
    'apps.users',
    'apps.blog',
    'apps.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True  # Always use timezone-aware datetimes

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

**`settings/development.py`:**
```python
"""Development-specific settings."""
from .base import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'myproject_dev',
        'USER': 'myproject_user',
        'PASSWORD': 'dev_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Development-specific apps
INSTALLED_APPS += [
    'debug_toolbar',
    'django_extensions',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

# Django Debug Toolbar
INTERNAL_IPS = ['127.0.0.1']

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**`settings/production.py`:**
```python
"""Production settings."""
import os
from .base import *

DEBUG = False

# SECURITY WARNING: Update this to your domain
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Use environment variables for sensitive data
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,  # Connection pooling
    }
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/myproject/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

#### 1.4 URL Configuration Patterns

**Rule:** Use RESTful URL patterns and include() for app-specific URLs.

✅ **Good:**

**`myproject/urls.py`:**
```python
"""Root URL configuration."""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/users/', include('apps.users.urls')),
    path('api/v1/blog/', include('apps.blog.urls')),
    path('api/v1/', include('apps.core.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

**`apps/users/urls.py`:**
```python
"""User app URL configuration."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'users'  # URL namespace

router = DefaultRouter()
router.register(r'', views.UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
```

**URL Naming Best Practices:**
- Use lowercase with hyphens: `/api/user-profiles/`
- Version your APIs: `/api/v1/`, `/api/v2/`
- Use plural nouns for resources: `/users/`, `/posts/`
- Use nested routes sparingly: `/users/123/posts/` (consider `/posts/?user=123` instead)
- Always name your URLs for reverse lookup

---

### Task 2: Model Best Practices

#### 2.1 Model Design Patterns

**Rule:** Models should be focused, well-documented, and follow Django conventions.

✅ **Good Model Design:**
```python
"""User models."""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser.

    Adds additional fields for user profiles and implements
    business logic related to user accounts.
    """

    class UserRole(models.TextChoices):
        """User role choices."""
        ADMIN = 'ADMIN', _('Administrator')
        MODERATOR = 'MOD', _('Moderator')
        USER = 'USER', _('Regular User')

    # Additional fields
    email = models.EmailField(_('email address'), unique=True)
    role = models.CharField(
        _('role'),
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.USER,
    )
    bio = models.TextField(_('biography'), blank=True, max_length=500)
    birth_date = models.DateField(_('birth date'), null=True, blank=True)
    avatar = models.ImageField(
        _('avatar'),
        upload_to='avatars/%Y/%m/%d/',
        null=True,
        blank=True,
    )
    email_verified = models.BooleanField(_('email verified'), default=False)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        """String representation of user."""
        return f"{self.username} ({self.get_role_display()})"

    def get_full_name(self):
        """Return user's full name or username if not set."""
        full_name = super().get_full_name()
        return full_name if full_name else self.username

    @property
    def is_admin(self):
        """Check if user has admin role."""
        return self.role == self.UserRole.ADMIN

    def verify_email(self):
        """Mark user's email as verified."""
        self.email_verified = True
        self.save(update_fields=['email_verified', 'updated_at'])


class Post(models.Model):
    """Blog post model."""

    class PostStatus(models.TextChoices):
        """Post status choices."""
        DRAFT = 'DRAFT', _('Draft')
        PUBLISHED = 'PUBLISHED', _('Published')
        ARCHIVED = 'ARCHIVED', _('Archived')

    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=200, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        related_query_name='post',
        verbose_name=_('author'),
    )
    content = models.TextField(_('content'))
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=PostStatus.choices,
        default=PostStatus.DRAFT,
        db_index=True,
    )
    featured = models.BooleanField(_('featured'), default=False)
    view_count = models.PositiveIntegerField(_('view count'), default=0)
    published_at = models.DateTimeField(_('published at'), null=True, blank=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    # Use custom manager
    objects = PostManager()

    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['author', '-created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(view_count__gte=0),
                name='post_view_count_non_negative',
            ),
        ]

    def __str__(self):
        """String representation of post."""
        return self.title

    def save(self, *args, **kwargs):
        """Override save to set published_at when status changes to published."""
        if self.status == self.PostStatus.PUBLISHED and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def increment_view_count(self):
        """Increment post view count efficiently."""
        self.__class__.objects.filter(pk=self.pk).update(
            view_count=models.F('view_count') + 1
        )
        # Refresh from database
        self.refresh_from_db(fields=['view_count'])
```

**Key Model Design Principles:**
1. Use verbose field names with gettext_lazy for i18n
2. Add `help_text` for complex fields
3. Use TextChoices/IntegerChoices for choice fields
4. Include timestamps (created_at, updated_at) on most models
5. Use appropriate `on_delete` for ForeignKey
6. Set `related_name` and `related_query_name` on relationships
7. Add database indexes for frequently queried fields
8. Use constraints for data integrity
9. Override `__str__()` for meaningful representations
10. Document the model and complex methods

#### 2.2 Field Choices and Naming

**Rule:** Use TextChoices/IntegerChoices for field choices, follow naming conventions.

✅ **Good:**
```python
class Order(models.Model):
    """Customer order model."""

    class OrderStatus(models.TextChoices):
        """Order status choices using TextChoices."""
        PENDING = 'PENDING', _('Pending Payment')
        PAID = 'PAID', _('Paid')
        PROCESSING = 'PROCESSING', _('Processing')
        SHIPPED = 'SHIPPED', _('Shipped')
        DELIVERED = 'DELIVERED', _('Delivered')
        CANCELLED = 'CANCELLED', _('Cancelled')
        REFUNDED = 'REFUNDED', _('Refunded')

    class PaymentMethod(models.TextChoices):
        """Payment method choices."""
        CREDIT_CARD = 'CC', _('Credit Card')
        DEBIT_CARD = 'DC', _('Debit Card')
        PAYPAL = 'PP', _('PayPal')
        BANK_TRANSFER = 'BT', _('Bank Transfer')

    # Field naming follows snake_case
    order_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    payment_method = models.CharField(
        max_length=2,
        choices=PaymentMethod.choices,
        null=True,
        blank=True,
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    shipping_address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.get_status_display()}"
```

❌ **Bad:**
```python
class Order(models.Model):
    """Bad example - avoid this."""

    # Bad: Tuple choices instead of TextChoices
    STATUS_CHOICES = (
        (1, 'Pending'),
        (2, 'Paid'),
        (3, 'Shipped'),
    )

    # Bad: Using integers without clear meaning
    status = models.IntegerField(choices=STATUS_CHOICES)

    # Bad: camelCase instead of snake_case
    orderNumber = models.CharField(max_length=50)

    # Bad: Vague field names
    amt = models.DecimalField(max_digits=10, decimal_places=2)
    addr = models.TextField()
```

**Field Naming Conventions:**
- Use snake_case for field names
- Be explicit and descriptive (avoid abbreviations)
- Use `_id` suffix sparingly (Django adds it automatically to ForeignKey)
- Use boolean field names that read like questions: `is_active`, `has_paid`, `email_verified`
- Use date/time field names with `_at` or `_date` suffix: `created_at`, `birth_date`

#### 2.3 Meta Class Options

**Rule:** Use Meta class to configure model behavior and database options.

✅ **Good Meta Class:**
```python
class Article(models.Model):
    """Article model with comprehensive Meta configuration."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Verbose names for admin
        verbose_name = _('article')
        verbose_name_plural = _('articles')

        # Default ordering
        ordering = ['-published_at', '-created_at']

        # Get latest by
        get_latest_by = 'published_at'

        # Database table name (optional, Django auto-generates)
        db_table = 'blog_articles'

        # Indexes for query optimization
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['author', '-published_at']),
            models.Index(fields=['category', '-published_at']),
            models.Index(fields=['-published_at'], name='recent_articles_idx'),
        ]

        # Unique together constraints
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'slug'],
                name='unique_author_slug',
            ),
            models.CheckConstraint(
                check=models.Q(published_at__isnull=True) | models.Q(published_at__gte=models.F('created_at')),
                name='published_after_created',
            ),
        ]

        # Permissions
        permissions = [
            ('can_publish', 'Can publish articles'),
            ('can_feature', 'Can feature articles'),
        ]
```

**Common Meta Options:**
- `verbose_name` / `verbose_name_plural`: Admin display names
- `ordering`: Default query ordering
- `indexes`: Database indexes for performance
- `constraints`: UniqueConstraint, CheckConstraint for data integrity
- `permissions`: Custom permissions
- `db_table`: Custom table name (use sparingly)
- `get_latest_by`: Field to use for latest()
- `abstract`: For abstract base models
- `managed`: Whether Django manages database lifecycle

#### 2.4 Managers and QuerySets

**Rule:** Use custom managers for reusable query logic and QuerySets for chainable queries.

✅ **Good Custom Manager and QuerySet:**

**`apps/blog/managers.py`:**
```python
"""Custom managers and querysets for blog app."""
from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    """Custom QuerySet for Post model with reusable query methods."""

    def published(self):
        """Return only published posts."""
        return self.filter(
            status=self.model.PostStatus.PUBLISHED,
            published_at__lte=timezone.now(),
        )

    def drafts(self):
        """Return draft posts."""
        return self.filter(status=self.model.PostStatus.DRAFT)

    def by_author(self, author):
        """Return posts by specific author."""
        return self.filter(author=author)

    def featured(self):
        """Return featured posts."""
        return self.filter(featured=True)

    def recent(self, days=30):
        """Return posts from last N days."""
        cutoff_date = timezone.now() - timezone.timedelta(days=days)
        return self.filter(published_at__gte=cutoff_date)

    def with_author_info(self):
        """Optimize query by selecting related author."""
        return self.select_related('author')

    def with_comments_count(self):
        """Annotate with comment count."""
        return self.annotate(
            comments_count=models.Count('comments', distinct=True)
        )

    def popular(self, min_views=100):
        """Return popular posts above view threshold."""
        return self.filter(view_count__gte=min_views).order_by('-view_count')


class PostManager(models.Manager):
    """Custom manager for Post model."""

    def get_queryset(self):
        """Return custom QuerySet."""
        return PostQuerySet(self.model, using=self._db)

    # Proxy QuerySet methods for convenience
    def published(self):
        """Return published posts."""
        return self.get_queryset().published()

    def drafts(self):
        """Return draft posts."""
        return self.get_queryset().drafts()

    def by_author(self, author):
        """Return posts by author."""
        return self.get_queryset().by_author(author)

    def featured(self):
        """Return featured posts."""
        return self.get_queryset().featured()

    def recent(self, days=30):
        """Return recent posts."""
        return self.get_queryset().recent(days)


class PublishedPostManager(models.Manager):
    """Manager that returns only published posts by default."""

    def get_queryset(self):
        """Return only published posts."""
        return super().get_queryset().filter(
            status='PUBLISHED',
            published_at__lte=timezone.now(),
        )
```

**Usage in models.py:**
```python
from .managers import PostManager, PublishedPostManager

class Post(models.Model):
    # ... fields ...

    # Default manager
    objects = PostManager()

    # Additional manager for published posts only
    published = PublishedPostManager()

    class Meta:
        base_manager_name = 'objects'  # Use for related queries
```

**Usage in views:**
```python
# Chainable QuerySet methods
recent_featured_posts = Post.objects.published().featured().recent(days=7)

# Multiple optimizations
popular_posts = (
    Post.objects
    .published()
    .with_author_info()
    .with_comments_count()
    .popular(min_views=500)
)

# Using alternative manager
all_published = Post.published.all()
```

**Manager Best Practices:**
1. Put query logic in QuerySets for chainability
2. Create manager methods that return QuerySets
3. Use descriptive method names
4. Document what each method does
5. Don't put business logic in managers (use models or services)
6. Use `select_related()` and `prefetch_related()` in manager methods

#### 2.5 Model Methods vs Signals

**Rule:** Use model methods for object-specific logic, signals for cross-cutting concerns.

✅ **Good - Use Model Methods:**
```python
class Order(models.Model):
    """Order model with business logic in methods."""

    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total(self):
        """Calculate order total including tax and discount."""
        subtotal = self.total_amount - self.discount_amount
        return subtotal + self.tax_amount

    def apply_discount(self, discount_code):
        """Apply discount code to order."""
        from .services import DiscountService

        discount = DiscountService.validate_and_get_discount(discount_code, self)
        self.discount_amount = discount.amount
        self.save(update_fields=['discount_amount'])
        return discount

    def mark_as_paid(self):
        """Mark order as paid and trigger fulfillment."""
        self.status = self.OrderStatus.PAID
        self.paid_at = timezone.now()
        self.save(update_fields=['status', 'paid_at'])

        # Trigger fulfillment signal
        from .signals import order_paid
        order_paid.send(sender=self.__class__, order=self)
```

✅ **Good - Use Signals for Cross-Cutting Concerns:**

**`apps/orders/signals.py`:**
```python
"""Order-related signals."""
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver, Signal
from .models import Order

# Custom signal
order_paid = Signal()  # Provides 'order' argument

@receiver(post_save, sender=Order)
def send_order_confirmation_email(sender, instance, created, **kwargs):
    """Send confirmation email when order is created."""
    if created:
        from .tasks import send_order_confirmation_email_task
        send_order_confirmation_email_task.delay(instance.id)

@receiver(order_paid)
def start_order_fulfillment(sender, order, **kwargs):
    """Start fulfillment process when order is paid."""
    from .tasks import start_fulfillment_task
    start_fulfillment_task.delay(order.id)

@receiver(pre_delete, sender=Order)
def log_order_deletion(sender, instance, **kwargs):
    """Log when order is deleted for audit trail."""
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(
        f"Order {instance.order_number} deleted by system",
        extra={'order_id': instance.id}
    )
```

**Connect signals in apps.py:**
```python
from django.apps import AppConfig

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.orders'

    def ready(self):
        """Import signals when app is ready."""
        import apps.orders.signals  # noqa
```

**When to Use Each:**

**Model Methods:**
- Object-specific business logic
- Calculations based on model data
- State transitions
- Data validation
- Simple related object queries

**Signals:**
- Send notifications (email, SMS, webhooks)
- Update caches
- Create audit logs
- Trigger background tasks
- Cross-app communication
- Update denormalized data

❌ **Bad - Business Logic in Signals:**
```python
@receiver(post_save, sender=Order)
def update_order_total(sender, instance, **kwargs):
    """DON'T DO THIS - business logic should be in model method."""
    instance.total = instance.calculate_subtotal() + instance.tax
    instance.save()  # Causes infinite loop!
```

#### 2.6 Related Names and related_query_name

**Rule:** Always set explicit related_name for reverse relationships.

✅ **Good:**
```python
class User(models.Model):
    username = models.CharField(max_length=150)

class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',           # user.posts.all()
        related_query_name='post',      # User.objects.filter(post__title='...')
    )
    title = models.CharField(max_length=200)

class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        related_query_name='comment',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        related_query_name='comment',
    )
    content = models.TextField()

# Usage:
user = User.objects.get(username='john')
user_posts = user.posts.all()  # Uses related_name
user_comments = user.comments.all()

# Query filtering uses related_query_name
users_with_python_posts = User.objects.filter(post__title__contains='Python')
posts_with_comments = Post.objects.filter(comment__isnull=False)
```

❌ **Bad:**
```python
class Post(models.Model):
    # Bad: No related_name, Django generates 'post_set'
    author = models.ForeignKey(User, on_delete=models.CASCADE)

# Unclear usage:
user_posts = user.post_set.all()  # What is post_set?
```

**Related Name Best Practices:**
- Use plural for one-to-many: `related_name='posts'`
- Use singular for one-to-one: `related_name='profile'`
- Use `related_query_name` for clear query filtering
- Use `related_name='+'` to disable reverse relation if not needed
- Avoid name conflicts across apps using `app_label`

#### 2.7 Database Indexing Strategies

**Rule:** Add indexes for fields frequently used in queries, filtering, and ordering.

✅ **Good Indexing:**
```python
class Article(models.Model):
    """Article model with strategic indexing."""

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)  # Unique creates index automatically
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # FK creates index
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices)
    featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            # Index for filtering by status and ordering
            models.Index(fields=['status', '-published_at'], name='status_pub_idx'),

            # Index for author's articles
            models.Index(fields=['author', '-created_at'], name='author_articles_idx'),

            # Index for category browsing
            models.Index(fields=['category', '-published_at'], name='cat_pub_idx'),

            # Index for featured articles
            models.Index(
                fields=['-published_at'],
                condition=models.Q(featured=True),
                name='featured_idx',  # Partial index (PostgreSQL)
            ),

            # Compound index for complex queries
            models.Index(
                fields=['status', 'featured', '-view_count'],
                name='popular_published_idx',
            ),
        ]

        # Text search index (PostgreSQL)
        # For full-text search capabilities
        # Note: Requires GinIndex from django.contrib.postgres.indexes
```

**When to Add Indexes:**
- Foreign keys (automatic in Django)
- Fields in `WHERE` clauses
- Fields in `ORDER BY` clauses
- Fields in `JOIN` conditions
- Unique fields (automatic)
- Fields used in `filter()`, `exclude()`, `get()`

**When NOT to Add Indexes:**
- Small tables (< 10,000 rows)
- Fields that change frequently
- Fields with low cardinality (few unique values like boolean)
- Too many indexes slow down writes

**Index Analysis:**
```python
# Check if query uses indexes
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as queries:
    articles = Article.objects.filter(
        status='PUBLISHED',
        featured=True
    ).order_by('-view_count')[:10]
    list(articles)  # Force evaluation

for query in queries:
    print(query['sql'])
    # Check EXPLAIN output in database
```

#### 2.8 Migration Best Practices

**Rule:** Create focused, reviewable migrations and handle data migrations separately.

✅ **Good Migration Practices:**

**1. Small, Focused Migrations:**
```bash
# Create separate migrations for different changes
python manage.py makemigrations --name add_email_verified_field
python manage.py makemigrations --name add_user_role_choices
```

**2. Data Migration Example:**
```python
# Generated migration file: 0003_populate_user_roles.py
from django.db import migrations

def populate_user_roles(apps, schema_editor):
    """Populate user roles based on is_staff and is_superuser."""
    User = apps.get_model('users', 'User')

    # Update in batches for large datasets
    User.objects.filter(is_superuser=True).update(role='ADMIN')
    User.objects.filter(is_staff=True, is_superuser=False).update(role='MOD')
    User.objects.filter(is_staff=False, is_superuser=False).update(role='USER')

def reverse_populate_user_roles(apps, schema_editor):
    """Reverse operation."""
    User = apps.get_model('users', 'User')
    User.objects.all().update(role='USER')

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0002_user_role'),
    ]

    operations = [
        migrations.RunPython(
            populate_user_roles,
            reverse_code=reverse_populate_user_roles,
        ),
    ]
```

**3. Safe Schema Changes:**
```python
# Safe: Adding nullable field
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]

# Safe: Adding field with default
class Migration(migrations.Migration):
    operations = [
        migrations.AddField(
            model_name='post',
            name='view_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
```

**4. Multi-Step Migrations for Removing Fields:**
```python
# Step 1: Make field nullable (deploy)
field=models.CharField(max_length=100, null=True, blank=True)

# Step 2: Remove from code, create migration (deploy)
# Step 3: Drop column (deploy)
```

**Migration Best Practices:**
1. Review generated migrations before committing
2. Use descriptive migration names (`--name`)
3. Never edit applied migrations in production
4. Use `RunPython` for data migrations with reverse operations
5. Test migrations on production-like data
6. Use `--check` in CI to detect missing migrations
7. Squash old migrations when they pile up
8. Handle large datasets with batching in data migrations
9. Add indexes in separate migrations (can be slow)
10. Use database transactions (default in Django)

---

### Task 3: Views and URLs Best Practices

#### 3.1 Class-Based Views (CBVs) vs Function-Based Views (FBVs)

**Rule:** Use CBVs for CRUD operations, FBVs for simple or unique logic.

✅ **Good - Use CBVs for Standard CRUD:**
```python
"""Blog views using class-based views."""
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm


class PostListView(ListView):
    """List all published posts."""

    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 20

    def get_queryset(self):
        """Return only published posts with author info."""
        return Post.objects.published().with_author_info()

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.featured()[:5]
        return context


class PostDetailView(DetailView):
    """Display single post."""

    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Get post and increment view count."""
        post = super().get_object(queryset)
        post.increment_view_count()
        return post


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create new post."""

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('blog:post-list')

    def form_valid(self, form):
        """Set author to current user."""
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update existing post."""

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        """Check if user is author or admin."""
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

    def get_success_url(self):
        """Redirect to post detail."""
        return self.object.get_absolute_url()


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete post."""

    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post-list')

    def test_func(self):
        """Check if user is author or admin."""
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff
```

✅ **Good - Use FBVs for Unique Logic:**
```python
"""Blog views using function-based views for custom logic."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Post


@login_required
@require_POST
def toggle_post_featured(request, pk):
    """Toggle post featured status (unique logic, FBV appropriate)."""
    post = get_object_or_404(Post, pk=pk)

    # Check permissions
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    # Toggle featured status
    post.featured = not post.featured
    post.save(update_fields=['featured'])

    return JsonResponse({
        'success': True,
        'featured': post.featured,
    })


def search_posts(request):
    """Search posts (custom search logic, FBV appropriate)."""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')

    posts = Post.objects.published()

    if query:
        posts = posts.filter(
            models.Q(title__icontains=query) |
            models.Q(content__icontains=query)
        )

    if category:
        posts = posts.filter(category__slug=category)

    context = {
        'posts': posts,
        'query': query,
        'category': category,
    }
    return render(request, 'blog/search_results.html', context)
```

**When to Use Each:**

**Use CBVs when:**
- Standard CRUD operations
- Need inheritance and mixins
- Working with forms
- Need consistent structure across views

**Use FBVs when:**
- Simple logic
- Unique business logic that doesn't fit CBV pattern
- API endpoints with custom logic
- Complex multi-step flows
- Clearer and more readable as function

#### 3.2 Generic Views

**Rule:** Use Django's generic views for common patterns.

✅ **Good - Using Generic Views:**
```python
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView,
    TemplateView, RedirectView, FormView
)


class HomePageView(TemplateView):
    """Homepage using TemplateView."""
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recent_posts'] = Post.objects.published().recent()[:5]
        context['featured_posts'] = Post.objects.featured()[:3]
        return context


class ContactFormView(FormView):
    """Contact form using FormView."""
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact-success')

    def form_valid(self, form):
        """Send email when form is valid."""
        form.send_email()
        return super().form_valid(form)


class RedirectToLatestPostView(RedirectView):
    """Redirect to latest published post."""
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        latest_post = Post.objects.published().latest('published_at')
        return latest_post.get_absolute_url()
```

**Common Generic Views:**
- `TemplateView`: Render a template
- `ListView`: List objects
- `DetailView`: Display single object
- `CreateView`: Create object with form
- `UpdateView`: Update object with form
- `DeleteView`: Delete object
- `FormView`: Display and process form
- `RedirectView`: Redirect to URL

#### 3.3 View Permissions and Mixins

**Rule:** Use mixins for reusable view behavior and permissions.

✅ **Good - Using Mixins:**
```python
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.views.generic import ListView, UpdateView


class AuthorRequiredMixin(UserPassesTestMixin):
    """Mixin to require user to be object author."""

    def test_func(self):
        """Check if user is object author."""
        obj = self.get_object()
        return obj.author == self.request.user


class AdminOrAuthorMixin(UserPassesTestMixin):
    """Mixin to require user to be admin or author."""

    def test_func(self):
        """Check if user is admin or author."""
        obj = self.get_object()
        return (
            self.request.user.is_staff or
            obj.author == self.request.user
        )


class MyPostsView(LoginRequiredMixin, ListView):
    """List current user's posts (requires login)."""

    model = Post
    template_name = 'blog/my_posts.html'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostPublishView(PermissionRequiredMixin, UpdateView):
    """Publish post (requires permission)."""

    model = Post
    fields = ['status']
    permission_required = 'blog.can_publish'

    def form_valid(self, form):
        form.instance.status = 'PUBLISHED'
        return super().form_valid(form)


class PostEditView(AdminOrAuthorMixin, UpdateView):
    """Edit post (requires author or admin)."""

    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'
```

**Common Mixins:**
- `LoginRequiredMixin`: Require authentication
- `PermissionRequiredMixin`: Require specific permission
- `UserPassesTestMixin`: Custom test function
- `UserOwnerMixin`: Custom mixin for object ownership

**Mixin Order Matters:**
```python
# Correct order: Left to right
class MyView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    # Mixins process left to right
    pass

# Wrong: View class should be last
class MyView(UpdateView, LoginRequiredMixin):  # Don't do this
    pass
```

#### 3.4 Handling Forms in Views

**Rule:** Use Django forms for validation, use form_valid() for custom processing.

✅ **Good Form Handling:**
```python
from django.views.generic.edit import CreateView, UpdateView
from .forms import PostForm, CommentForm


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create post with form."""

    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_form_kwargs(self):
        """Pass user to form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Process valid form."""
        form.instance.author = self.request.user
        response = super().form_valid(form)

        # Send notification
        from .tasks import send_post_created_notification
        send_post_created_notification.delay(self.object.id)

        messages.success(self.request, 'Post created successfully!')
        return response

    def form_invalid(self, form):
        """Handle invalid form."""
        messages.error(self.request, 'Please correct the errors below.')
        return super().form_invalid(form)

    def get_success_url(self):
        """Redirect to post detail."""
        return self.object.get_absolute_url()


class CommentCreateView(LoginRequiredMixin, CreateView):
    """Create comment with AJAX support."""

    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        """Process valid comment form."""
        form.instance.author = self.request.user
        form.instance.post_id = self.kwargs['post_pk']

        response = super().form_valid(form)

        # Return JSON for AJAX requests
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'comment_id': self.object.id,
                'author': self.object.author.username,
                'content': self.object.content,
            })

        return response
```

---

### Task 4: Django REST Framework (DRF) Best Practices

#### 4.1 Serializer Patterns

**Rule:** Use ModelSerializer for models, add validation and custom fields as needed.

✅ **Good Serializer Design:**

**`apps/blog/serializers.py`:**
```python
"""Blog app serializers."""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Category

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """User serializer with limited fields."""

    full_name = serializers.CharField(source='get_full_name', read_only=True)
    post_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name', 'post_count', 'date_joined']
        read_only_fields = ['date_joined']


class CategorySerializer(serializers.ModelSerializer):
    """Category serializer."""

    post_count = serializers.IntegerField(source='posts.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'post_count']
        read_only_fields = ['slug']


class CommentSerializer(serializers.ModelSerializer):
    """Comment serializer with nested author."""

    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'author_id', 'content',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def validate_content(self, value):
        """Validate comment content."""
        if len(value) < 10:
            raise serializers.ValidationError(
                "Comment must be at least 10 characters long."
            )
        return value


class PostListSerializer(serializers.ModelSerializer):
    """Post serializer for list view (minimal fields)."""

    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'category',
            'excerpt', 'status', 'featured', 'view_count',
            'comment_count', 'published_at', 'created_at'
        ]

    def get_excerpt(self, obj):
        """Return first 200 characters of content."""
        return obj.content[:200] + '...' if len(obj.content) > 200 else obj.content


class PostDetailSerializer(serializers.ModelSerializer):
    """Post serializer for detail view (full fields)."""

    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comment_count = serializers.IntegerField(source='comments.count', read_only=True)

    # Write-only fields
    author_id = serializers.IntegerField(write_only=True, required=False)
    category_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author', 'author_id',
            'category', 'category_id', 'content', 'status',
            'featured', 'view_count', 'comments', 'comment_count',
            'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'view_count', 'created_at', 'updated_at']

    def validate(self, attrs):
        """Validate post data."""
        # Set author from request if not provided
        if 'author_id' not in attrs:
            attrs['author_id'] = self.context['request'].user.id

        # Validate published posts have category
        if attrs.get('status') == 'PUBLISHED' and not attrs.get('category_id'):
            raise serializers.ValidationError({
                'category': 'Published posts must have a category.'
            })

        return attrs

    def create(self, validated_data):
        """Create post and set published_at if published."""
        if validated_data.get('status') == 'PUBLISHED':
            from django.utils import timezone
            validated_data['published_at'] = timezone.now()

        return super().create(validated_data)


class PostWriteSerializer(serializers.ModelSerializer):
    """Post serializer for create/update (separate from read)."""

    class Meta:
        model = Post
        fields = [
            'title', 'slug', 'category', 'content',
            'status', 'featured'
        ]

    def validate_slug(self, value):
        """Validate slug uniqueness."""
        # Exclude current instance in update
        queryset = Post.objects.filter(slug=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise serializers.ValidationError("Post with this slug already exists.")

        return value
```

**Serializer Best Practices:**
1. Use separate serializers for list/detail/write when fields differ significantly
2. Use `SerializerMethodField` for computed fields
3. Use `source` parameter to reference model methods/properties
4. Set `read_only=True` for computed fields
5. Use `write_only=True` for password/sensitive input fields
6. Validate in `validate_<field>()` for single field, `validate()` for multi-field
7. Keep business logic in models/services, not serializers
8. Use nested serializers for related objects in read, IDs in write

#### 4.2 ViewSets vs APIView

**Rule:** Use ViewSets for standard CRUD APIs, APIView for custom endpoints.

✅ **Good - Using ViewSets:**
```python
"""Blog API views using ViewSets."""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Comment
from .serializers import (
    PostListSerializer, PostDetailSerializer,
    PostWriteSerializer, CommentSerializer
)
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """ViewSet for Post model with CRUD operations."""

    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'category', 'featured']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'published_at', 'view_count']
    ordering = ['-published_at']

    def get_queryset(self):
        """Return appropriate queryset based on action."""
        queryset = Post.objects.all()

        if self.action == 'list':
            # Optimize list query
            queryset = queryset.select_related('author', 'category')
            queryset = queryset.annotate(
                comment_count=models.Count('comments')
            )

            # Filter by published status for non-staff users
            if not self.request.user.is_staff:
                queryset = queryset.filter(status='PUBLISHED')

        elif self.action == 'retrieve':
            # Optimize detail query
            queryset = queryset.select_related('author', 'category')
            queryset = queryset.prefetch_related('comments__author')

        return queryset

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return PostListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return PostWriteSerializer
        return PostDetailSerializer

    def perform_create(self, serializer):
        """Set author when creating post."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'])
    def publish(self, request, pk=None):
        """Custom action to publish a post."""
        post = self.get_object()

        if post.status == 'PUBLISHED':
            return Response(
                {'detail': 'Post is already published.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        post.status = 'PUBLISHED'
        from django.utils import timezone
        post.published_at = timezone.now()
        post.save()

        serializer = self.get_serializer(post)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get comments for a post."""
        post = self.get_object()
        comments = post.comments.select_related('author')

        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured posts."""
        queryset = self.get_queryset().filter(featured=True)[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet for Comment model."""

    queryset = Comment.objects.select_related('author', 'post')
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        """Set author when creating comment."""
        serializer.save(author=self.request.user)
```

✅ **Good - Using APIView for Custom Logic:**
```python
"""Custom API views using APIView."""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Avg
from .models import Post


class PostStatisticsAPIView(APIView):
    """Custom endpoint for post statistics."""

    def get(self, request):
        """Return post statistics."""
        stats = Post.objects.aggregate(
            total_posts=Count('id'),
            total_views=models.Sum('view_count'),
            avg_views=Avg('view_count'),
            published_posts=Count('id', filter=models.Q(status='PUBLISHED')),
        )

        return Response(stats)


class BulkPublishAPIView(APIView):
    """Bulk publish posts."""

    permission_classes = [IsAdminUser]

    def post(self, request):
        """Publish multiple posts."""
        post_ids = request.data.get('post_ids', [])

        if not post_ids:
            return Response(
                {'detail': 'No post IDs provided.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        from django.utils import timezone
        updated_count = Post.objects.filter(
            id__in=post_ids,
            status='DRAFT'
        ).update(
            status='PUBLISHED',
            published_at=timezone.now()
        )

        return Response({
            'detail': f'{updated_count} posts published.',
            'count': updated_count
        })
```

**When to Use Each:**

**Use ViewSets when:**
- Standard CRUD operations
- Working with a single model
- Need router URL generation
- Want consistent API structure

**Use APIView when:**
- Custom business logic
- Multiple models in one endpoint
- Non-CRUD operations
- Complex request/response handling

#### 4.3 Permission Classes

**Rule:** Use DRF permission classes for access control.

✅ **Good Custom Permissions:**

**`apps/blog/permissions.py`:**
```python
"""Custom permission classes for blog app."""
from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Permission to only allow authors to edit their objects."""

    def has_object_permission(self, request, view, obj):
        """Check object-level permission."""
        # Read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions only for author
        return obj.author == request.user


class IsAdminOrAuthor(permissions.BasePermission):
    """Permission for admin or author."""

    def has_object_permission(self, request, view, obj):
        """Check if user is admin or author."""
        return request.user.is_staff or obj.author == request.user


class CanPublishPost(permissions.BasePermission):
    """Permission to publish posts."""

    message = "You don't have permission to publish posts."

    def has_permission(self, request, view):
        """Check if user has publish permission."""
        return request.user.has_perm('blog.can_publish')


class IsEmailVerified(permissions.BasePermission):
    """Permission requiring verified email."""

    message = "Email must be verified to perform this action."

    def has_permission(self, request, view):
        """Check if user's email is verified."""
        return request.user.is_authenticated and request.user.email_verified
```

**Using Permissions in Views:**
```python
class PostViewSet(viewsets.ModelViewSet):
    """Post ViewSet with multiple permission classes."""

    def get_permissions(self):
        """Return appropriate permissions based on action."""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAuthenticated, IsEmailVerified, IsAuthorOrReadOnly]
        elif self.action == 'publish':
            permission_classes = [IsAuthenticated, CanPublishPost]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]
```

**Common Permission Classes:**
- `AllowAny`: Allow all (default)
- `IsAuthenticated`: Require authentication
- `IsAdminUser`: Require staff status
- `IsAuthenticatedOrReadOnly`: Read for all, write for authenticated
- `DjangoModelPermissions`: Use Django model permissions
- `DjangoObjectPermissions`: Object-level permissions

#### 4.4 Authentication Patterns

**Rule:** Use token-based authentication for APIs, sessions for web.

✅ **Good Authentication Setup:**

**`settings/base.py`:**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

**JWT Authentication (using djangorestframework-simplejwt):**
```python
# settings/base.py
from datetime import timedelta

INSTALLED_APPS += [
    'rest_framework_simplejwt',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

**Authentication Views:**
```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

#### 4.5 Pagination Best Practices

**Rule:** Always paginate list endpoints, provide pagination controls.

✅ **Good Pagination:**

**`apps/core/pagination.py`:**
```python
"""Custom pagination classes."""
from rest_framework.pagination import PageNumberPagination, CursorPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """Standard pagination with page numbers."""

    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        """Custom paginated response."""
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page_size': self.page_size,
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
            'results': data,
        })


class LargeResultsSetPagination(PageNumberPagination):
    """Pagination for large datasets."""

    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class PostCursorPagination(CursorPagination):
    """Cursor pagination for posts (better for infinite scroll)."""

    page_size = 20
    ordering = '-created_at'
    cursor_query_param = 'cursor'
```

**Using in ViewSets:**
```python
class PostViewSet(viewsets.ModelViewSet):
    """Post ViewSet with pagination."""

    pagination_class = StandardResultsSetPagination

    # Override for specific actions
    def get_paginated_response(self, data):
        """Add custom metadata to paginated response."""
        response = super().get_paginated_response(data)
        response.data['meta'] = {
            'total_featured': Post.objects.filter(featured=True).count(),
        }
        return response
```

#### 4.6 Filtering and Searching

**Rule:** Use django-filter for complex filtering, DRF filters for search/ordering.

✅ **Good Filtering Setup:**

**`apps/blog/filters.py`:**
```python
"""Custom filters for blog app."""
from django_filters import rest_framework as filters
from .models import Post


class PostFilter(filters.FilterSet):
    """Custom filter for Post model."""

    title = filters.CharFilter(lookup_expr='icontains')
    author_username = filters.CharFilter(field_name='author__username', lookup_expr='iexact')
    category = filters.CharFilter(field_name='category__slug')
    published_after = filters.DateTimeFilter(field_name='published_at', lookup_expr='gte')
    published_before = filters.DateTimeFilter(field_name='published_at', lookup_expr='lte')
    min_views = filters.NumberFilter(field_name='view_count', lookup_expr='gte')
    featured = filters.BooleanFilter()
    status = filters.ChoiceFilter(choices=Post.PostStatus.choices)

    class Meta:
        model = Post
        fields = ['title', 'author_username', 'category', 'featured', 'status']


class PostViewSet(viewsets.ModelViewSet):
    """Post ViewSet with filtering."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'published_at', 'view_count', 'title']
    ordering = ['-published_at']
```

**Usage:**
```
# Filter examples:
GET /api/posts/?category=django&featured=true
GET /api/posts/?published_after=2024-01-01&min_views=100
GET /api/posts/?search=django&ordering=-view_count
GET /api/posts/?author_username=john
```

#### 4.7 API Versioning

**Rule:** Version your API from the start, use URL path versioning.

✅ **Good API Versioning:**

**`settings/base.py`:**
```python
REST_FRAMEWORK = {
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    'DEFAULT_VERSION': 'v1',
    'ALLOWED_VERSIONS': ['v1', 'v2'],
    'VERSION_PARAM': 'version',
}
```

**`urls.py`:**
```python
from django.urls import path, include

urlpatterns = [
    path('api/v1/', include('apps.api.v1.urls')),
    path('api/v2/', include('apps.api.v2.urls')),
]
```

**Version-specific serializers:**
```python
# apps/api/v1/serializers.py
class PostSerializerV1(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author']

# apps/api/v2/serializers.py
class PostSerializerV2(serializers.ModelSerializer):
    # V2 adds new fields
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'slug', 'category']
```

---

### Task 5: Forms and ModelForms Best Practices

#### 5.1 Form Field Validation

**Rule:** Validate fields with clean_<field>() methods, validate across fields with clean().

✅ **Good Form Validation:**

**`apps/users/forms.py`:**
```python
"""User forms with validation."""
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re

User = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """User registration form with custom validation."""

    email = forms.EmailField(
        required=True,
        help_text='Enter a valid email address.',
    )
    agree_to_terms = forms.BooleanField(
        required=True,
        label='I agree to the terms and conditions',
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'agree_to_terms']

    def clean_username(self):
        """Validate username."""
        username = self.cleaned_data.get('username')

        # Check length
        if len(username) < 3:
            raise ValidationError('Username must be at least 3 characters.')

        # Check format (alphanumeric and underscores only)
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            raise ValidationError(
                'Username can only contain letters, numbers, and underscores.'
            )

        # Check uniqueness
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('This username is already taken.')

        return username.lower()

    def clean_email(self):
        """Validate email."""
        email = self.cleaned_data.get('email')

        # Check uniqueness
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('This email is already registered.')

        # Check domain (example: block certain domains)
        domain = email.split('@')[1]
        blocked_domains = ['tempmail.com', 'throwaway.email']
        if domain in blocked_domains:
            raise ValidationError('Email from this domain is not allowed.')

        return email.lower()

    def clean(self):
        """Cross-field validation."""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        username = cleaned_data.get('username')

        # Check password doesn't contain username
        if password1 and username and username.lower() in password1.lower():
            raise ValidationError('Password cannot contain your username.')

        return cleaned_data

    def save(self, commit=True):
        """Save user with additional processing."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
            # Send verification email
            from .tasks import send_verification_email
            send_verification_email.delay(user.id)

        return user


class PostForm(forms.ModelForm):
    """Post form with validation."""

    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'content', 'status', 'featured']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
            'slug': forms.TextInput(attrs={'placeholder': 'auto-generated-from-title'}),
        }

    def __init__(self, *args, **kwargs):
        """Initialize form with custom behavior."""
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Make slug optional on create (auto-generate from title)
        if not self.instance.pk:
            self.fields['slug'].required = False

        # Limit category choices based on user
        if self.user and not self.user.is_staff:
            self.fields['category'].queryset = Category.objects.filter(public=True)

    def clean_slug(self):
        """Validate and auto-generate slug."""
        slug = self.cleaned_data.get('slug')
        title = self.cleaned_data.get('title')

        # Auto-generate slug if not provided
        if not slug and title:
            from django.utils.text import slugify
            slug = slugify(title)

        # Check uniqueness (excluding current instance)
        queryset = Post.objects.filter(slug=slug)
        if self.instance.pk:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():
            raise ValidationError('Post with this slug already exists.')

        return slug

    def clean_content(self):
        """Validate content."""
        content = self.cleaned_data.get('content')

        # Minimum length
        if len(content) < 100:
            raise ValidationError('Post content must be at least 100 characters.')

        return content

    def clean(self):
        """Cross-field validation."""
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        category = cleaned_data.get('category')

        # Published posts must have category
        if status == 'PUBLISHED' and not category:
            raise ValidationError({
                'category': 'Published posts must have a category.'
            })

        return cleaned_data
```

#### 5.2 ModelForm Usage

**Rule:** Use ModelForm for database-backed forms, Form for non-model forms.

✅ **Good ModelForm:**
```python
class CommentForm(forms.ModelForm):
    """ModelForm for Comment model."""

    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write your comment here...',
                'class': 'form-control',
            }),
        }
        labels = {
            'content': 'Your Comment',
        }
        help_texts = {
            'content': 'Be respectful and constructive.',
        }

    def __init__(self, *args, **kwargs):
        """Initialize form."""
        self.post = kwargs.pop('post', None)
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        """Save comment with post and user."""
        comment = super().save(commit=False)
        if self.post:
            comment.post = self.post
        if self.user:
            comment.author = self.user

        if commit:
            comment.save()

        return comment
```

✅ **Good Form (non-model):**
```python
class ContactForm(forms.Form):
    """Contact form not backed by model."""

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Your Name'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Subject'}),
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Your message...'}),
    )

    def send_email(self):
        """Send contact email."""
        from django.core.mail import send_mail

        send_mail(
            subject=f"Contact Form: {self.cleaned_data['subject']}",
            message=self.cleaned_data['message'],
            from_email=self.cleaned_data['email'],
            recipient_list=['contact@example.com'],
        )
```

#### 5.3 Formsets

**Rule:** Use formsets for handling multiple forms.

✅ **Good Formset Usage:**
```python
from django.forms import modelformset_factory, inlineformset_factory


# ModelFormSet for editing multiple objects
PostFormSet = modelformset_factory(
    Post,
    fields=['title', 'status', 'featured'],
    extra=0,  # No extra empty forms
    can_delete=True,
)

# InlineFormSet for related objects
CommentFormSet = inlineformset_factory(
    Post,
    Comment,
    fields=['content'],
    extra=1,
    can_delete=True,
)

# In view:
def edit_post_with_comments(request, pk):
    """Edit post and its comments."""
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        post_form = PostForm(request.POST, instance=post)
        comment_formset = CommentFormSet(request.POST, instance=post)

        if post_form.is_valid() and comment_formset.is_valid():
            post_form.save()
            comment_formset.save()
            return redirect('post-detail', pk=post.pk)
    else:
        post_form = PostForm(instance=post)
        comment_formset = CommentFormSet(instance=post)

    return render(request, 'post_edit.html', {
        'form': post_form,
        'formset': comment_formset,
    })
```

---

### Task 6: Security Best Practices

#### 6.1 CSRF Protection

**Rule:** Always use CSRF protection, never disable it in production.

✅ **Good CSRF Usage:**
```html
<!-- In templates -->
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

```python
# In AJAX requests
from django.middleware.csrf import get_token

def my_view(request):
    """View that provides CSRF token for AJAX."""
    return JsonResponse({
        'csrfToken': get_token(request),
    })
```

```javascript
// In JavaScript
fetch('/api/endpoint/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken'),
    },
    body: JSON.stringify(data),
});
```

❌ **Bad - Never Do This:**
```python
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # DON'T DO THIS in production
def my_view(request):
    pass
```

#### 6.2 SQL Injection Prevention

**Rule:** Always use Django ORM or parameterized queries, never string concatenation.

✅ **Good - Safe from SQL Injection:**
```python
# Using ORM (automatically escaped)
users = User.objects.filter(username=user_input)

# Using ORM Q objects
from django.db.models import Q
users = User.objects.filter(
    Q(username__icontains=search_term) |
    Q(email__icontains=search_term)
)

# If you must use raw SQL, use parameterization
from django.db import connection
with connection.cursor() as cursor:
    cursor.execute(
        "SELECT * FROM users WHERE username = %s",
        [user_input]  # Parameterized - SAFE
    )
```

❌ **Bad - SQL Injection Vulnerability:**
```python
# DON'T DO THIS - vulnerable to SQL injection
query = f"SELECT * FROM users WHERE username = '{user_input}'"
cursor.execute(query)

# DON'T DO THIS
User.objects.raw(f"SELECT * FROM users WHERE username = '{user_input}'")
```

#### 6.3 XSS Prevention

**Rule:** Use Django's auto-escaping, mark safe only when necessary.

✅ **Good - XSS Protected:**
```html
<!-- Django auto-escapes by default -->
<p>{{ user_comment }}</p>  <!-- Automatically escaped -->

<!-- For trusted HTML -->
<div>{{ trusted_html|safe }}</div>

<!-- In Python code -->
from django.utils.html import escape, format_html

# Escape user input
safe_text = escape(user_input)

# Use format_html for building HTML
html = format_html(
    '<a href="{}">Link</a>',
    user_url  # Automatically escaped
)
```

❌ **Bad - XSS Vulnerability:**
```html
<!-- DON'T DO THIS -->
<p>{{ user_comment|safe }}</p>  <!-- Marks untrusted input as safe -->

<!-- In Python -->
# DON'T DO THIS
html = f'<p>{user_input}</p>'  # Not escaped
```

#### 6.4 SECRET_KEY and Sensitive Settings

**Rule:** Never hardcode secrets, use environment variables.

✅ **Good:**
```python
# settings/production.py
import os

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DATABASE_PASSWORD = os.environ['DB_PASSWORD']
AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_KEY']

# Using python-decouple
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

❌ **Bad:**
```python
# DON'T DO THIS
SECRET_KEY = 'my-secret-key-123'  # Hardcoded secret
DATABASE_PASSWORD = 'password123'  # In source code
```

#### 6.5 DEBUG Settings

**Rule:** Never set DEBUG=True in production.

✅ **Good:**
```python
# settings/production.py
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Custom error pages
ADMINS = [('Admin', 'admin@yourdomain.com')]
MANAGERS = ADMINS
```

#### 6.6 Security Middleware

**Rule:** Enable all security middleware in production.

✅ **Good Production Security:**
```python
# settings/production.py

# Security middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# HTTPS settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# HSTS settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Other security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 12}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
```

---

### Task 7: Performance Optimization

#### 7.1 N+1 Query Prevention

**Rule:** Use select_related() and prefetch_related() to avoid N+1 queries.

✅ **Good - Optimized Queries:**
```python
# N+1 Problem Example (BAD):
posts = Post.objects.all()
for post in posts:
    print(post.author.username)  # Triggers query for each post!

# Solution 1: select_related for ForeignKey/OneToOne
posts = Post.objects.select_related('author', 'category').all()
for post in posts:
    print(post.author.username)  # No additional queries!

# Solution 2: prefetch_related for ManyToMany/Reverse FK
posts = Post.objects.prefetch_related('comments').all()
for post in posts:
    print(post.comments.count())  # No additional queries!

# Complex prefetch with filtering
from django.db.models import Prefetch

posts = Post.objects.prefetch_related(
    Prefetch(
        'comments',
        queryset=Comment.objects.select_related('author').filter(approved=True),
        to_attr='approved_comments'
    )
).all()

for post in posts:
    for comment in post.approved_comments:
        print(comment.author.username)  # All in 3 queries total!
```

**When to Use Each:**
- `select_related()`: For ForeignKey and OneToOneField (SQL JOIN)
- `prefetch_related()`: For ManyToManyField and reverse ForeignKey (separate query + Python join)

#### 7.2 Query Optimization with only() and defer()

**Rule:** Use only() to fetch specific fields, defer() to exclude fields.

✅ **Good:**
```python
# Only fetch needed fields
users = User.objects.only('id', 'username', 'email')

# Defer large fields
posts = Post.objects.defer('content')  # Don't load content field

# Combine with select_related
posts = (
    Post.objects
    .select_related('author')
    .only('id', 'title', 'author__username', 'created_at')
)
```

#### 7.3 Database Query Analysis

**Rule:** Monitor and analyze queries, use django-debug-toolbar.

✅ **Good - Query Analysis:**
```python
# In development, use django-debug-toolbar
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

# Log queries in development
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Check query count in tests
from django.test.utils import override_settings
from django.db import connection
from django.test.utils import CaptureQueriesContext

with CaptureQueriesContext(connection) as queries:
    # Your code here
    list(Post.objects.all())

print(f"Number of queries: {len(queries)}")
for query in queries:
    print(query['sql'])
```

#### 7.4 Caching Strategies

**Rule:** Cache expensive queries and computations.

✅ **Good Caching:**
```python
# Cache decorator for views
from django.views.decorators.cache import cache_page

@cache_page(60 * 15)  # Cache for 15 minutes
def post_list(request):
    posts = Post.objects.published().with_author_info()
    return render(request, 'posts.html', {'posts': posts})

# Low-level cache API
from django.core.cache import cache

def get_popular_posts():
    """Get popular posts with caching."""
    cache_key = 'popular_posts'
    posts = cache.get(cache_key)

    if posts is None:
        posts = list(Post.objects.popular()[:10])
        cache.set(cache_key, posts, 60 * 60)  # Cache for 1 hour

    return posts

# Cache expensive computations
from django.utils.functional import cached_property

class Post(models.Model):
    # ... fields ...

    @cached_property
    def word_count(self):
        """Calculate word count (cached on instance)."""
        return len(self.content.split())

# Template fragment caching
{% load cache %}
{% cache 500 sidebar request.user.username %}
    <!-- Expensive sidebar generation -->
{% endcache %}
```

**Cache Settings:**
```python
# Redis cache (recommended for production)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        },
        'KEY_PREFIX': 'myproject',
        'TIMEOUT': 300,  # 5 minutes default
    }
}

# Memcached cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyMemcacheCache',
        'LOCATION': '127.0.0.1:11211',
    }
}
```

#### 7.5 Database Connection Pooling

**Rule:** Use connection pooling in production for better performance.

✅ **Good:**
```python
# settings/production.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,  # Connection pooling (10 minutes)
        'OPTIONS': {
            'connect_timeout': 10,
        },
    }
}
```

---

### Task 8: Testing Django Applications

**Rule:** Write comprehensive tests for models, views, and APIs.

✅ **Good Django Tests:**

**`apps/blog/tests/test_models.py`:**
```python
"""Tests for blog models."""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.blog.models import Post, Category

User = get_user_model()


class PostModelTest(TestCase):
    """Tests for Post model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )
        self.category = Category.objects.create(
            name='Django',
            slug='django',
        )

    def test_create_post(self):
        """Test creating a post."""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            category=self.category,
            content='Test content',
        )

        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertEqual(str(post), 'Test Post')

    def test_published_posts_manager(self):
        """Test published posts manager."""
        # Create published post
        published = Post.objects.create(
            title='Published Post',
            slug='published-post',
            author=self.user,
            content='Content',
            status='PUBLISHED',
        )

        # Create draft post
        draft = Post.objects.create(
            title='Draft Post',
            slug='draft-post',
            author=self.user,
            content='Content',
            status='DRAFT',
        )

        # Test manager
        published_posts = Post.objects.published()
        self.assertIn(published, published_posts)
        self.assertNotIn(draft, published_posts)
```

**`apps/blog/tests/test_views.py`:**
```python
"""Tests for blog views."""
from django.test import TestCase, Client
from django.urls import reverse
from apps.blog.models import Post


class PostListViewTest(TestCase):
    """Tests for post list view."""

    def setUp(self):
        """Set up test client and data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
        )

    def test_post_list_view(self):
        """Test post list view returns 200."""
        response = self.client.get(reverse('blog:post-list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_post_create_requires_login(self):
        """Test that creating post requires login."""
        response = self.client.get(reverse('blog:post-create'))

        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/login/', response.url)
```

**`apps/blog/tests/test_api.py`:**
```python
"""Tests for blog API."""
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class PostAPITest(APITestCase):
    """Tests for Post API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
        )

    def test_list_posts(self):
        """Test listing posts."""
        url = reverse('api:post-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_requires_authentication(self):
        """Test that creating post requires authentication."""
        url = reverse('api:post-list')
        data = {'title': 'Test Post', 'content': 'Test content'}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_authenticated(self):
        """Test creating post when authenticated."""
        self.client.force_authenticate(user=self.user)

        url = reverse('api:post-list')
        data = {
            'title': 'Test Post',
            'content': 'Test content' * 20,  # Meet minimum length
            'status': 'DRAFT',
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)
```

---

### Task 9: Common Django Anti-Patterns

#### 9.1 Anti-Pattern: Using filter().first() instead of get()

❌ **Bad:**
```python
# Don't do this - less clear intent
user = User.objects.filter(id=user_id).first()
if user is None:
    # Handle not found
    pass
```

✅ **Good:**
```python
# Use get() and handle DoesNotExist
from django.core.exceptions import ObjectDoesNotExist

try:
    user = User.objects.get(id=user_id)
except User.DoesNotExist:
    # Handle not found
    pass

# Or use get_object_or_404 in views
from django.shortcuts.get_object_or_404

user = get_object_or_404(User, id=user_id)
```

#### 9.2 Anti-Pattern: Not Using select_related/prefetch_related

❌ **Bad - N+1 Queries:**
```python
# This generates N+1 queries (1 for posts + 1 per post for author)
posts = Post.objects.all()
for post in posts:
    print(f"{post.title} by {post.author.username}")
```

✅ **Good:**
```python
# This generates 1 query (JOIN)
posts = Post.objects.select_related('author').all()
for post in posts:
    print(f"{post.title} by {post.author.username}")
```

#### 9.3 Anti-Pattern: Using Raw SQL When ORM Would Work

❌ **Bad:**
```python
# Don't use raw SQL for simple queries
from django.db import connection

cursor = connection.cursor()
cursor.execute("SELECT * FROM users WHERE username = %s", [username])
user = cursor.fetchone()
```

✅ **Good:**
```python
# Use the ORM
user = User.objects.get(username=username)
```

**When Raw SQL IS Appropriate:**
- Complex queries that ORM can't express efficiently
- Database-specific features (window functions, CTEs)
- Performance-critical queries where you need full control

#### 9.4 Anti-Pattern: Not Using Transactions

❌ **Bad:**
```python
# Multiple saves without transaction
def transfer_money(from_account, to_account, amount):
    from_account.balance -= amount
    from_account.save()

    to_account.balance += amount
    to_account.save()  # If this fails, first save succeeded!
```

✅ **Good:**
```python
from django.db import transaction

@transaction.atomic
def transfer_money(from_account, to_account, amount):
    """Transfer money atomically."""
    from_account.balance -= amount
    from_account.save()

    to_account.balance += amount
    to_account.save()
    # Both saves succeed or both fail

# Or use context manager
def transfer_money(from_account, to_account, amount):
    """Transfer money atomically."""
    with transaction.atomic():
        from_account.balance -= amount
        from_account.save()

        to_account.balance += amount
        to_account.save()
```

#### 9.5 Anti-Pattern: Storing Secrets in Code

❌ **Bad:**
```python
SECRET_KEY = 'django-insecure-hard-coded-key'
AWS_SECRET_KEY = 'AKIAIOSFODNN7EXAMPLE'
DATABASE_PASSWORD = 'mypassword123'
```

✅ **Good:**
```python
import os
from decouple import config

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
AWS_SECRET_KEY = config('AWS_SECRET_KEY')
DATABASE_PASSWORD = config('DB_PASSWORD')
```

#### 9.6 Anti-Pattern: Not Using Migrations

❌ **Bad:**
```python
# Manually creating database tables
# Editing database schema directly
# Not committing migration files
```

✅ **Good:**
```bash
# Always create migrations for model changes
python manage.py makemigrations
python manage.py migrate

# Commit migration files to version control
git add apps/*/migrations/*.py
git commit -m "Add user profile model"
```

#### 9.7 Anti-Pattern: Circular Imports

❌ **Bad:**
```python
# apps/users/models.py
from apps.blog.models import Post  # Circular import!

class User(models.Model):
    favorite_post = models.ForeignKey(Post, ...)

# apps/blog/models.py
from apps.users.models import User  # Circular import!

class Post(models.Model):
    author = models.ForeignKey(User, ...)
```

✅ **Good:**
```python
# apps/users/models.py
from django.db import models

class User(models.Model):
    favorite_post = models.ForeignKey(
        'blog.Post',  # String reference
        on_delete=models.SET_NULL,
        null=True,
    )

# apps/blog/models.py
from django.conf import settings

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Reference to user model
        on_delete=models.CASCADE,
    )
```

---

## Best Practices Summary

### Django Project Checklist

- [ ] Project structure follows Django conventions
- [ ] Settings split by environment (base, dev, prod, test)
- [ ] SECRET_KEY and sensitive data in environment variables
- [ ] DEBUG=False in production
- [ ] All security middleware enabled in production
- [ ] ALLOWED_HOSTS configured correctly
- [ ] Database connection pooling enabled (CONN_MAX_AGE)
- [ ] Static/media files properly configured

### Model Best Practices

- [ ] Models use verbose field names with gettext_lazy
- [ ] TextChoices/IntegerChoices for choice fields
- [ ] Explicit related_name on ForeignKey/ManyToMany
- [ ] Appropriate on_delete handlers
- [ ] Database indexes on frequently queried fields
- [ ] Timestamps (created_at, updated_at) on models
- [ ] Custom managers for reusable query logic
- [ ] Model methods for business logic
- [ ] Signals for cross-cutting concerns

### View Best Practices

- [ ] CBVs for standard CRUD, FBVs for custom logic
- [ ] Mixins for reusable view behavior
- [ ] Proper permission checks (LoginRequired, etc.)
- [ ] select_related/prefetch_related to avoid N+1
- [ ] Pagination on list views
- [ ] Form validation in forms, not views

### DRF Best Practices

- [ ] Separate serializers for list/detail/write
- [ ] Permission classes for access control
- [ ] Token/JWT authentication configured
- [ ] Pagination enabled on list endpoints
- [ ] Filtering and search configured
- [ ] API versioning implemented
- [ ] Proper error handling and responses

### Security Checklist

- [ ] CSRF protection enabled
- [ ] Using Django ORM (not raw SQL concatenation)
- [ ] Auto-escaping enabled in templates
- [ ] SECRET_KEY in environment variable
- [ ] DEBUG=False in production
- [ ] Security middleware enabled
- [ ] HTTPS enforced (SECURE_SSL_REDIRECT)
- [ ] Password validators configured

### Performance Checklist

- [ ] select_related/prefetch_related used appropriately
- [ ] Database indexes on frequently queried fields
- [ ] Query optimization (only/defer when appropriate)
- [ ] Caching strategy implemented
- [ ] Database connection pooling configured
- [ ] django-debug-toolbar installed in development
- [ ] Query monitoring in place

### Testing Checklist

- [ ] Tests for all models
- [ ] Tests for all views/API endpoints
- [ ] Tests for forms and validation
- [ ] Tests for permissions
- [ ] Test coverage > 80%
- [ ] Integration tests for critical paths

---

## Templates

### Template 1: Django Model

Located at: `templates/django_model_template.py`

See: `/Users/clo/developer/gh-clostaunau/holiday-card/.claude/skills/django-conventions/templates/django_model_template.py`

### Template 2: Django REST Framework ViewSet

Located at: `templates/drf_viewset_template.py`

See: `/Users/clo/developer/gh-clostaunau/holiday-card/.claude/skills/django-conventions/templates/drf_viewset_template.py`

### Template 3: Django Form

Located at: `templates/django_form_template.py`

See: `/Users/clo/developer/gh-clostaunau/holiday-card/.claude/skills/django-conventions/templates/django_form_template.py`

---

## Related Skills

- **python-testing-standards**: Python testing best practices (referenced for Django tests)
- **python-type-hints-guide**: Python type hints (applicable to Django)
- **uncle-duke-python**: Python code review agent that uses this skill

---

## References

### Official Documentation
- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [Django Best Practices](https://docs.djangoproject.com/en/stable/misc/design-philosophies/)

### Security
- [Django Security](https://docs.djangoproject.com/en/stable/topics/security/)
- [OWASP Django Security](https://cheatsheetseries.owasp.org/cheatsheets/Django_Security_Cheat_Sheet.html)

### Performance
- [Django Database Optimization](https://docs.djangoproject.com/en/stable/topics/db/optimization/)
- [Django Caching](https://docs.djangoproject.com/en/stable/topics/cache/)

### Books and Guides
- Two Scoops of Django (Best Practices Book)
- Django for APIs (Django REST Framework)
- High Performance Django

---

**Version:** 1.0
**Last Updated:** 2025-12-24
**Maintainer:** Development Team
