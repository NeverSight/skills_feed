---
name: Django Framework
description: Build production-ready web applications with Django MVC, ORM, authentication, and REST APIs
version: "2.1.0"
sasmp_version: "1.3.0"
bonded_agent: 02-web-development
bond_type: PRIMARY_BOND

# Skill Configuration
retry_strategy: exponential_backoff
observability:
  logging: true
  metrics: request_latency
---

# Django Framework

## Overview

Master Django, the high-level Python web framework that encourages rapid development and clean, pragmatic design. Learn to build secure, scalable web applications with Django's batteries-included approach.

## Learning Objectives

- Build full-stack web applications using Django MVC pattern
- Design and implement database models with Django ORM
- Implement user authentication and authorization
- Create RESTful APIs with Django REST Framework
- Deploy Django applications to production

## Core Topics

### 1. Django Basics & Project Structure
- Django project setup and configuration
- Understanding MVT (Model-View-Template) pattern
- URL routing and views
- Django settings and environment variables
- Static files and media handling

**Code Example:**
```python
# myapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})

def product_api(request):
    products = Product.objects.values('id', 'name', 'price')
    return JsonResponse(list(products), safe=False)
```

### 2. Django ORM & Database Models
- Model definition and field types
- Relationships (ForeignKey, ManyToMany, OneToOne)
- QuerySets and database queries
- Migrations and schema management
- Database optimization (select_related, prefetch_related)

**Code Example:**
```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Efficient querying
products = Product.objects.select_related('category', 'created_by').filter(is_active=True)
```

### 3. Authentication & Authorization
- User registration and login
- Password management
- Session management
- Permissions and groups
- Custom user models
- Social authentication

**Code Example:**
```python
# views.py
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
    return render(request, 'login.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@permission_required('products.add_product')
def add_product(request):
    # Only users with 'add_product' permission can access
    return render(request, 'products/add.html')
```

### 4. Django REST Framework
- Serializers and validation
- ViewSets and routers
- Authentication (JWT, Token)
- Permissions and throttling
- Pagination and filtering

**Code Example:**
```python
# serializers.py
from rest_framework import serializers
from .models import Product, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'category', 'category_id', 'created_at']

# views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        return queryset
```

## Hands-On Practice

### Project 1: Blog Application
Build a full-featured blog with user authentication.

**Requirements:**
- User registration and login
- Create, edit, delete posts
- Comments system
- Categories and tags
- Search functionality
- Admin interface

**Key Skills:** Django models, views, forms, authentication

### Project 2: E-commerce API
Create a RESTful API for an e-commerce platform.

**Requirements:**
- Product catalog with categories
- Shopping cart management
- Order processing
- User authentication with JWT
- API documentation
- Rate limiting

**Key Skills:** Django REST Framework, serializers, authentication

### Project 3: Task Management System
Build a collaborative task management application.

**Requirements:**
- User registration and teams
- Create and assign tasks
- Task status tracking
- File attachments
- Real-time notifications
- Permission-based access

**Key Skills:** Complex models, permissions, file handling

## Assessment Criteria

- [ ] Set up Django projects with proper structure
- [ ] Design normalized database schemas
- [ ] Implement CRUD operations efficiently
- [ ] Secure applications with authentication
- [ ] Build RESTful APIs following best practices
- [ ] Write Django tests (unit and integration)
- [ ] Deploy to production environment

## Resources

### Official Documentation
- [Django Docs](https://docs.djangoproject.com/) - Official documentation
- [Django REST Framework](https://www.django-rest-framework.org/) - DRF documentation
- [Django Girls Tutorial](https://tutorial.djangogirls.org/) - Beginner-friendly

### Learning Platforms
- [Django for Beginners](https://djangoforbeginners.com/) - Book and tutorials
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x) - Best practices
- [TestDriven.io](https://testdriven.io/) - Django with TDD

### Tools
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/) - Debugging
- [django-extensions](https://django-extensions.readthedocs.io/) - Useful utilities
- [Celery](https://docs.celeryproject.org/) - Async tasks
- [PostgreSQL](https://www.postgresql.org/) - Recommended database

## Next Steps

After mastering Django, explore:
- **FastAPI** - Modern, fast web framework
- **Celery** - Asynchronous task queue
- **Docker** - Containerization for deployment
- **AWS/Heroku** - Cloud deployment platforms
