---
name: django-development
description: Comprehensive guide for building Django web applications following Django 5.2 standards and industry best practices. Use when developing Django projects, implementing models/views/templates, configuring settings, handling forms, ensuring security, or deploying Django applications.
domain: web-development, python, django
---

# Django Development Guide

This skill provides comprehensive guidance for building robust Django web applications following Django 5.2 standards and industry-proven best practices.

## When to Use This Skill

Use this skill when:
- Starting a new Django project or app
- Implementing models, views, templates, or forms
- Configuring Django settings or URL routing
- Addressing security concerns in Django applications
- Writing tests or deploying Django applications
- Following Django conventions and best practices
- Troubleshooting Django-specific issues

## Core Principles

**Convention Over Configuration**: Django follows established conventions that reduce boilerplate and decision fatigue. Follow Django patterns rather than reinventing solutions.

**DRY (Don't Repeat Yourself)**: Extract reusable code into models, managers, mixins, template tags, and middleware.

**Security by Default**: Django provides built-in protection against common vulnerabilities. Never disable security features without understanding the implications.

**Explicit is Better Than Implicit**: Code should be clear and self-documenting. Use descriptive names and follow Django naming conventions.

---

# Development Workflow

## Phase 1: Project Planning and Setup

### 1.1 Understand Requirements

Before creating a Django project, clarify:
- **Data models**: What entities exist and how do they relate?
- **User interactions**: What actions can users perform?
- **Authentication needs**: Who can access what?
- **Third-party integrations**: External APIs or services needed?

### 1.2 Initialize Project Structure

**Create a new Django project:**

```bash
# Create project directory
mkdir myproject
cd myproject

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Django
pip install django

# Start project
django-admin startproject config .
```

**Key distinction**: A project contains configuration and settings, while apps contain specific functionality.

### 1.3 Configure Initial Settings

**Load the detailed configuration guide:**
[⚙️ Settings Configuration Reference](./reference/settings_configuration.md)

Essential initial settings:
- `SECRET_KEY`: Must be 50+ characters, use environment variables, never commit to version control
- `DEBUG`: Set to `False` in production
- `ALLOWED_HOSTS`: Configure for your domain
- `DATABASES`: Configure database connection
- `INSTALLED_APPS`: Register Django apps and third-party packages
- `MIDDLEWARE`: Ensure SecurityMiddleware is enabled and properly ordered

---

## Phase 2: Data Modeling

### 2.1 Design Your Models

Models are the single source of truth for your data. Before coding:
- Identify entities (User, Post, Comment, etc.)
- Define relationships (one-to-many, many-to-many, one-to-one)
- Determine required fields and constraints
- Plan for data validation and business logic

### 2.2 Implement Models

**Load the comprehensive models guide:**
[📊 Models and Database Reference](./reference/models_database.md)

**Model implementation checklist:**
- [ ] Use appropriate field types (`CharField`, `IntegerField`, `ForeignKey`, etc.)
- [ ] Set field options (`null`, `blank`, `default`, `unique`)
- [ ] Define relationships with proper `related_name`
- [ ] Implement `__str__()` method for readable representation
- [ ] Add `get_absolute_url()` for object URLs
- [ ] Configure `Meta` class (`ordering`, `verbose_name`, constraints)
- [ ] Create custom managers for reusable queries
- [ ] Override `save()` or `delete()` for custom behavior (call `super()`)

### 2.3 Create and Apply Migrations

After defining or modifying models:

```bash
# Create migration files
python manage.py makemigrations

# Review generated migrations
python manage.py sqlmigrate appname 0001

# Apply migrations
python manage.py migrate
```

**Migration best practices:**
- Review migrations before applying
- Use descriptive migration names with `--name`
- Never edit applied migrations
- Handle data migrations separately
- Test migrations on development data first

---

## Phase 3: Views and URL Routing

### 3.1 Plan Your Views

Views handle request processing and response generation. Determine:
- Which views are needed (list, detail, create, update, delete)
- Function-based views (FBVs) vs class-based views (CBVs)
- Authentication and permission requirements
- Template rendering vs API responses

### 3.2 Implement Views

**Load the comprehensive views guide:**
[🎯 Views and URL Routing Reference](./reference/views_urls.md)

**View patterns:**

**Function-Based Views (FBVs):**
- Simple, explicit, good for unique logic
- Full control over request handling
- Use for complex or non-standard workflows

**Class-Based Views (CBVs):**
- Reusable, extensible, built-in functionality
- Generic views for common patterns (ListView, DetailView, CreateView)
- Use for standard CRUD operations

### 3.3 Configure URL Routing

**URL configuration best practices:**
- Use descriptive URL patterns with meaningful names
- Organize URLs by app using `include()`
- Use path converters (`<int:pk>`, `<slug:slug>`)
- Name all URL patterns for `reverse()` and `{% url %}`
- Keep URLs RESTful and intuitive

---

## Phase 4: Templates and Forms

### 4.1 Create Templates

**Load the templates and forms guide:**
[🎨 Templates and Forms Reference](./reference/templates_forms.md)

**Template best practices:**
- Use template inheritance (base template + child templates)
- Leverage template tags and filters
- Keep logic minimal (belongs in views/models)
- Use `{% static %}` for static files
- Take advantage of automatic XSS protection

### 4.2 Build Forms

**Form implementation checklist:**
- [ ] Use `ModelForm` when tied to models
- [ ] Use `Form` for non-model forms
- [ ] Implement custom validation with `clean_<field>()` methods
- [ ] Add form-level validation with `clean()`
- [ ] Use `widgets` to customize form rendering
- [ ] Handle file uploads with proper validation
- [ ] Include CSRF token in templates (`{% csrf_token %}`)

---

## Phase 5: Security Implementation

Security must be considered throughout development, not as an afterthought.

**Load the comprehensive security guide:**
[🔒 Security Best Practices Reference](./reference/security.md)

**Security checklist:**
- [ ] Keep `SECRET_KEY` secure and environment-specific
- [ ] Set `DEBUG = False` in production
- [ ] Configure `ALLOWED_HOSTS` appropriately
- [ ] Enable HTTPS and secure cookies
- [ ] Use CSRF protection (enabled by default)
- [ ] Leverage built-in XSS protection
- [ ] Use QuerySet parameterization (avoid raw SQL)
- [ ] Validate and sanitize user input
- [ ] Implement proper authentication and authorization
- [ ] Limit file upload sizes and types
- [ ] Set appropriate Content Security Policy headers
- [ ] Enable clickjacking protection

---

## Phase 6: Testing

**Load the testing guide:**
[✅ Testing and Quality Assurance Reference](./reference/testing_deployment.md)

**Testing best practices:**
- Write tests alongside code development
- Test models, views, forms, and custom logic
- Use `TestCase` for database-touching tests
- Use `SimpleTestCase` for non-database tests
- Mock external services and APIs
- Aim for high coverage of critical paths
- Use Django's test client for view testing
- Test authentication and permissions

**Run tests:**
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test myapp

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

---

## Phase 7: Deployment Preparation

Before deploying to production:

**Load the deployment guide:**
[🚀 Testing and Deployment Reference](./reference/testing_deployment.md)

**Deployment checklist:**
- [ ] Run `python manage.py check --deploy`
- [ ] Set `DEBUG = False`
- [ ] Configure production database
- [ ] Set up static file serving (use `collectstatic`)
- [ ] Configure media file storage
- [ ] Set secure cookies and HTTPS settings
- [ ] Configure logging
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Configure caching strategy
- [ ] Review and optimize database queries
- [ ] Set up backup procedures
- [ ] Document deployment process

---

# Reference Documentation

Load these comprehensive guides as needed during development:

## Core References

- [⚙️ Settings Configuration](./reference/settings_configuration.md) - Complete settings guide including database configuration, static files, middleware, internationalization, and environment-specific settings

- [📊 Models and Database](./reference/models_database.md) - Comprehensive model development guide covering field types, relationships, Meta options, custom managers, model methods, inheritance patterns, and migrations

- [🎯 Views and URL Routing](./reference/views_urls.md) - Complete guide to function-based and class-based views, generic views, URL configuration, request/response handling, and middleware

- [🎨 Templates and Forms](./reference/templates_forms.md) - Template inheritance, template tags/filters, context processors, form creation, validation, widgets, and formsets

- [🔒 Security Best Practices](./reference/security.md) - Comprehensive security guide covering CSRF, XSS, SQL injection, clickjacking, authentication, HTTPS configuration, and common vulnerabilities

- [✅ Testing and Deployment](./reference/testing_deployment.md) - Testing strategies, test types, coverage, deployment preparation, production configuration, and monitoring

---

# Common Patterns and Quick Reference

## Creating a New App

```bash
python manage.py startapp myapp
```

Then add to `INSTALLED_APPS` in settings.

## Basic Model Pattern

```python
from django.db import models

class MyModel(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "My Models"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('mymodel-detail', args=[str(self.id)])
```

## Basic View Pattern

```python
from django.views.generic import ListView, DetailView
from .models import MyModel

class MyModelListView(ListView):
    model = MyModel
    template_name = 'myapp/mymodel_list.html'
    context_object_name = 'items'
    paginate_by = 20

class MyModelDetailView(DetailView):
    model = MyModel
    template_name = 'myapp/mymodel_detail.html'
```

## Basic URL Pattern

```python
from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.MyModelListView.as_view(), name='list'),
    path('<int:pk>/', views.MyModelDetailView.as_view(), name='detail'),
]
```

## Basic Template Pattern

```django
{% extends "base.html" %}
{% load static %}

{% block title %}{{ object.name }}{% endblock %}

{% block content %}
<h1>{{ object.name }}</h1>
<p>Created: {{ object.created_at|date:"F d, Y" }}</p>
{% endblock %}
```

---

# Progressive Workflow

Django development is iterative. For new features:

1. **Design the data model** → Create/update models → Make migrations
2. **Create views** → Implement business logic → Handle requests
3. **Configure URLs** → Map URLs to views → Name patterns
4. **Build templates** → Create HTML with Django template language
5. **Add forms** → Handle user input → Validate data
6. **Write tests** → Test models, views, forms → Ensure quality
7. **Review security** → Check for vulnerabilities → Follow best practices

Remember: Django documentation at https://docs.djangoproject.com/en/5.2/ is comprehensive and should be consulted for detailed API references and advanced topics.
