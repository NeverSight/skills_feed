---
name: laravel-tdd
description: Test-Driven Development specifically for Laravel applications using Pest PHP. Use when implementing any Laravel feature or bugfix - write the test first, watch it fail, write minimal code to pass.
---

# Test-Driven Development for Laravel

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

This skill adapts TDD principles specifically for Laravel applications using Pest PHP, Laravel's testing features, and framework-specific patterns.

## When to Use

**Always for Laravel:**
- New features (controllers, models, services)
- Bug fixes
- API endpoints
- Database migrations and models
- Form validation
- Authorization policies
- Queue jobs
- Artisan commands
- Middleware

**Exceptions (ask your human partner):**
- Throwaway prototypes
- Configuration files
- View-only changes (no logic)

## The Laravel TDD Cycle

```
RED → Verify RED → GREEN → Verify GREEN → REFACTOR → Repeat
```

### RED - Write Failing Test

Write one minimal test showing what the Laravel feature should do.

**Feature Test Example:**
```php
<?php

use App\Models\User;
use App\Models\Post;

test('authenticated user can create post', function () {
    $user = User::factory()->create();
    
    $this->actingAs($user)
        ->post('/posts', [
            'title' => 'My First Post',
            'content' => 'Post content here',
        ])
        ->assertRedirect('/posts');
    
    expect(Post::where('title', 'My First Post')->exists())->toBeTrue();
    expect(Post::first()->user_id)->toBe($user->id);
});
```

### Verify RED - Watch It Fail

```bash
php artisan test --filter=authenticated_user_can_create_post
```

### GREEN - Minimal Laravel Code

Write simplest Laravel code to pass the test.

### Verify GREEN - Watch It Pass

```bash
php artisan test
```

### REFACTOR - Clean Up Laravel Code

After green only:
- Extract services for complex logic
- Create policies for authorization
- Add query scopes for reusability
- Use events for side effects

## Laravel-Specific Test Patterns

### Database Testing
```php
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);

test('creates post in database', function () {
    $user = User::factory()->create();
    
    $this->actingAs($user)
        ->post('/posts', ['title' => 'Test', 'content' => 'Content']);
    
    $this->assertDatabaseHas('posts', ['title' => 'Test']);
});
```

### Authorization Testing
```php
test('user cannot delete others posts', function () {
    $user = User::factory()->create();
    $post = Post::factory()->create();
    
    $this->actingAs($user)
        ->delete("/posts/{$post->id}")
        ->assertForbidden();
});
```

### API Testing
```php
test('creates post via API', function () {
    $user = User::factory()->create();
    
    $this->actingAs($user, 'sanctum')
        ->postJson('/api/posts', ['title' => 'API Post', 'content' => 'Content'])
        ->assertCreated();
});
```

## Verification Checklist

- [ ] Migration test passes
- [ ] Model relationships tested
- [ ] Controller actions tested
- [ ] Validation rules tested
- [ ] Authorization tested
- [ ] Database state verified
- [ ] All tests passing
- [ ] Used RefreshDatabase
- [ ] Used factories

## Remember

```
Every Laravel feature → Test exists and failed first
Otherwise → Not TDD
```
