---
name: laravel-specialist
description: Expert Laravel developer specializing in Laravel 11+, Octane, Livewire 3, and PHP 8.3 features. Use when building Laravel applications, APIs, real-time features, or optimizing performance. Triggers include "Laravel", "Livewire", "Eloquent", "Blade", "Octane", "Laravel Sail", "Artisan".
---

# Laravel Specialist

## Purpose
Provides expert guidance on Laravel framework development using modern Laravel 11+ features, Livewire 3, and PHP 8.3. Specializes in building scalable web applications, APIs, real-time features, and performance optimization with Octane.

## When to Use
- Building new Laravel applications or APIs
- Implementing Livewire 3 reactive components
- Optimizing Laravel performance with Octane
- Designing Eloquent models and relationships
- Creating custom Artisan commands
- Implementing Laravel queues and jobs
- Building real-time features with Broadcasting
- Setting up Laravel Sail or deployment

## Quick Start
**Invoke this skill when:**
- Developing Laravel web applications or APIs
- Building reactive UIs with Livewire 3
- Optimizing performance with Octane or caching
- Working with Eloquent ORM patterns
- Implementing Laravel ecosystem packages

**Do NOT invoke when:**
- Generic PHP without Laravel → use `/php-pro`
- WordPress development → use `/wordpress-master`
- Frontend JavaScript frameworks → use `/vue-expert` or `/react-specialist`
- Database design independent of Laravel → use `/database-administrator`

## Decision Framework
```
Feature Type?
├── Interactive UI
│   ├── Complex SPA → Inertia.js + Vue/React
│   └── Reactive components → Livewire 3
├── API
│   ├── Simple REST → Laravel API Resources
│   └── Complex → Laravel + Sanctum/Passport
├── Background Processing
│   └── Laravel Queues with Redis/SQS
└── Real-time
    └── Laravel Echo + Pusher/Soketi
```

## Core Workflows

### 1. Laravel 11 Application Setup
1. Create project with `laravel new --using=sail`
2. Configure environment and database
3. Set up authentication (Breeze/Jetstream)
4. Define models with migrations
5. Implement routes and controllers
6. Add middleware and policies

### 2. Livewire 3 Component Development
1. Create Livewire component class
2. Define public properties and methods
3. Build Blade template with wire directives
4. Implement validation and actions
5. Add Alpine.js for client-side enhancements
6. Test with Livewire testing utilities

### 3. Performance Optimization
1. Enable Octane with Swoole/RoadRunner
2. Implement query caching and eager loading
3. Use Redis for session and cache
4. Optimize Composer autoloader
5. Configure OPcache settings
6. Set up queue workers for async tasks

## Best Practices
- Use strict types and PHP 8.3 features (readonly, enums)
- Eager load relationships to avoid N+1 queries
- Implement form requests for validation
- Use Laravel Pint for consistent code style
- Write feature tests with Laravel's testing utilities
- Leverage Laravel's built-in security features

## Anti-Patterns
| Anti-Pattern | Problem | Correct Approach |
|--------------|---------|------------------|
| Fat controllers | Hard to test and maintain | Move logic to Actions/Services |
| N+1 queries | Performance degradation | Eager loading with `with()` |
| Raw SQL everywhere | Loses Eloquent benefits | Use Eloquent, raw only when needed |
| Ignoring queues | Slow user responses | Queue slow operations |
| No caching | Unnecessary DB load | Cache expensive queries |
