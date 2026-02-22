---
name: laravel-livewire
description: "Full-stack Laravel framework for building dynamic, reactive interfaces using PHP without writing JavaScript. Use when creating or modifying Livewire components, implementing data binding with wire:model, working with lifecycle hooks, building forms with validation, handling events and parent-child communication, implementing file uploads/pagination/lazy loading, writing tests, or optimizing performance. Supports Laravel Livewire v4+ development. Keywords: Livewire, wire:model, wire:click, livewire component, Alpine.js integration, wire:submit, real-time validation, computed properties, Laravel Livewire."
---

# Laravel Livewire

## Overview

Build dynamic, reactive Laravel interfaces using only PHP. Livewire v4+ handles server-side rendering with automatic client-side updates via hydration/dehydration—no JavaScript required.

## Quick Start

### Installation

```bash
composer require livewire/livewire
php artisan livewire:layout  # Creates resources/views/layouts/app.blade.php
```

### Create a Component

```bash
# Single-file component (default)
php artisan make:livewire CreatePost

# Page component
php artisan make:livewire pages::post.create

# Multi-file component
php artisan make:livewire CreatePost --mfc

# Class-based component (traditional)
php artisan make:livewire CreatePost --class
```

### Basic Component Pattern

```php
<?php
use Livewire\Component;
new class extends Component {
    public string $title = '';
    public string $content = '';

    public function save()
    {
        $this->validate([
            'title' => 'required|max:255',
            'content' => 'required',
        ]);

        Post::create($this->only(['title', 'content']));
        return $this->redirect('/posts');
    }
};
?>
```

```blade
<form wire:submit="save">
    <input type="text" wire:model="title">
    @error('title') <span class="error">{{ $message }}</span> @enderror

    <textarea wire:model="content"></textarea>
    @error('content') <span class="error">{{ $message }}</span> @enderror

    <button type="submit">Save</button>
</form>
```

## Core Concepts

### Component Structure

**Single-file components** (`resources/views/components/post/⚡create.blade.php`):
- PHP class and Blade template in one file
- Lightning bolt (⚡) is optional and can be disabled in config

**Multi-file components** (`resources/views/components/post/⚡create/`):
- Separate files for PHP, Blade, JS, CSS
- Better for large components with significant JavaScript

**Class-based components** (`app/Livewire/CreatePost.php`):
- Traditional Laravel structure
- Familiar for Livewire v2/v3 developers

### Property Management

```php
// Public properties - accessible in template as $property
public $title = '';

// Protected properties - accessible as $this->property, not sent to client
protected $apiKey = 'secret';

// Typed properties
public string $email = '';
public int $count = 0;
public ?Post $post;  // Auto-locks ID

// Reset properties
$this->reset('title', 'content');
$value = $this->pull('title');  // Get and reset
```

### Lifecycle Hooks

| Hook | When It Runs |
|------|--------------|
| `mount()` | First load only - receive props/route params |
| `boot()` | Every request (initial + subsequent) |
| `hydrate()` | Beginning of subsequent requests |
| `dehydrate()` | End of every request |
| `updating($prop)` | Before property update |
| `updated($prop)` | After property update |
| `rendering()` | Before render() |
| `rendered()` | After render() |
| `exception($e)` | When exception thrown |

```php
public function mount(Post $post)
{
    $this->post = $post;
    $this->title = $post->title;
}

public function updatedTitle($value)
{
    $this->title = strtolower($value);
}
```

### Computed Properties

Memoized derived values—accessed via `$this->property`.

```php
use Livewire\Attributes\Computed;

#[Computed]
public function posts()
{
    return Post::all(); // Runs once per request
}

#[Computed(persist: true, seconds: 3600)]
public function cachedData()
{
    return ExpensiveModel::all();
}
```

Usage in blade: `@foreach ($this->posts as $post)`

## Data Binding

### wire:model Modifiers

| Modifier | Behavior |
|----------|----------|
| (default) | Updates only on action submit |
| `.live` | Updates as user types (150ms debounce) |
| `.blur` | Updates when user clicks away |
| `.change` | Updates immediately on selection |
| `.debounce.500ms` | Custom debounce duration |
| `.number` | Cast to int on server |
| `.boolean` | Cast to bool on server |

```blade
<input type="text" wire:model="title">
<input type="email" wire:model.live="email">  <!-- Live validation -->
<input type="text" wire:model.blur="title">   <!-- On blur -->
<input type="text" wire:model.live.debounce.500ms="search">
```

### Dependent Selects (Important!)

Use `wire:key` when one select depends on another.

```blade
<select wire:model.live="selectedState">
    @foreach(State::all() as $state)
        <option value="{{ $state->id }}">{{ $state->label }}</option>
    @endforeach
</select>

<select wire:model.live="selectedCity" wire:key="{{ $selectedState }}">
    @foreach(City::whereStateId($selectedState)->get() as $city)
        <option value="{{ $city->id }}">{{ $city->label }}</option>
    @endforeach
</select>
```

## Actions & Events

### Event Listeners

```blade
<button wire:click="save">Save</button>
<input wire:keydown.enter="search">
<form wire:submit="submitForm">
<button wire:click="delete({{ $post->id }})">Delete</button>
```

### Event Modifiers

```blade
<!-- Key modifiers -->
<input wire:keydown.enter="search">
<input wire:keydown.shift.enter="...">

<!-- Event modifiers -->
<button wire:click.prevent="save">
<button wire:click.stop="...">
<button wire:click.window="...">
<button wire:click.once="...">
<button wire:click.debounce.250ms="...">
```

### Dispatching Events

**From PHP:**
```php
$this->dispatch('post-created', postId: $post->id);
$this->dispatch('post-created')->to(Dashboard::class);  // Direct to component
```

**From Blade (client-side):**
```blade
<button wire:click="$dispatch('post-created', { id: {{ $post->id }} })">
```

**Listening in PHP:**
```php
use Livewire\Attributes\On;

#[On('post-created')]
public function handlePostCreated($postId)
{
    // Handle event
}
```

**Listening in Blade:**
```blade
<livewire:post-list @post-created="$refresh" />
```

### Parent-Child Communication

```blade
<!-- Passing props -->
<livewire:todo-item :$post />

<!-- Reactive props (child updates when parent changes) -->
<?php
use Livewire\Attributes\Reactive;
#[Reactive]
public $todos;
?>

<!-- Direct parent access -->
<button wire:click="$parent.remove({{ $id }})">Remove</button>
```

## Forms & Validation

### Validation with Attributes

```php
use Livewire\Attributes\Validate;

new class extends Component {
    #[Validate('required|min:5')]
    public $title = '';

    #[Validate('required|email', message: 'Please enter a valid email')]
    public $email = '';

    public function save()
    {
        $this->validate(); // Runs all rules
        Post::create($this->only(['title', 'email']));
    }
};
```

### Real-Time Validation

```blade
<input type="text" wire:model.live="title">
@error('title') <span class="error">{{ $message }}</span> @enderror
```

```php
public function updated($property)
{
    $this->validateOnly($property);
}
```

### Form Objects

Extract form logic into reusable classes:

```bash
php artisan livewire:form PostForm
```

```php
// app/Livewire/Forms/PostForm.php
namespace App\Livewire\Forms;
use Livewire\Attributes\Validate;
use Livewire\Form;

class PostForm extends Form
{
    #[Validate('required|min:5')]
    public $title = '';

    #[Validate('required|min:5')]
    public $content = '';

    public function store()
    {
        $this->validate();
        Post::create($this->only(['title', 'content']));
    }
}
```

```blade
<input type="text" wire:model="form.title">
@error('form.title') <span class="error">{{ $message }}</span> @enderror
```

## Loading States

```blade
<button wire:click="save">
    Save
    <span wire:loading>Saving...</span>
</button>

<!-- Target specific action -->
<div wire:loading wire:target="removePhoto">Removing...</div>

<!-- CSS attribute -->
<button class="data-loading:opacity-50">Save</button>
```

## Advanced Features

### Lazy Loading

```blade
<livewire:revenue-chart lazy />
```

```php
use Livewire\Attributes\Lazy;

#[Lazy]
class RevenueChart extends Component
{
    public function placeholder()
    {
        return view('livewire.placeholders.skeleton');
    }
}
```

### Polling

```blade
<div wire:poll>{{ $count }}</div>           <!-- Every 2.5s -->
<div wire:poll.15s>{{ $count }}</div>       <!-- Custom interval -->
<div wire:poll.visible>{{ $count }}</div>   <!-- Only when visible -->
<div wire:poll.keep-alive>{{ $count }}</div> <!-- Keep in background -->
```

### File Uploads

```php
use Livewire\WithFileUploads;

class UploadPhoto extends Component
{
    use WithFileUploads;

    #[Validate('image|max:1024')] // 1MB max
    public $photo;

    public function save()
    {
        $this->photo->store(path: 'photos');
    }
}
```

```blade
<form wire:submit="save">
    @if ($photo)
        <img src="{{ $photo->temporaryUrl() }}">
    @endif
    <input type="file" wire:model="photo">
</form>
```

### Pagination

```php
use Livewire\WithPagination;

class ShowPosts extends Component
{
    use WithPagination;

    public function render()
    {
        return view('livewire.show-posts', [
            'posts' => Post::paginate(10),
        ]);
    }
}
```

```blade
{{ $posts->links() }}
```

### Alpine.js Integration

```blade
<div x-data="{ expanded: false }">
    <button @click="expanded = !expanded">Toggle</button>
    <div x-show="expanded">
        {{ $content }}
    </div>
</div>
```

**Access Livewire from Alpine:**
```blade
<input x-on:blur="$wire.save()">
<span x-text="$wire.title.length"></span>
```

## Testing

```php
use Livewire\Livewire;

test('component renders', function () {
    Livewire::test(CreatePost::class)
        ->assertStatus(200);
});

test('can create post', function () {
    Livewire::test(CreatePost::class)
        ->set('title', 'Test Post')
        ->call('save')
        ->assertRedirect('/posts');
});

test('validation works', function () {
    Livewire::test(CreatePost::class)
        ->set('title', '')
        ->call('save')
        ->assertHasErrors('title');
});
```

## Routing

```php
// routes/web.php
Route::livewire('/posts/create', 'pages::post.create');
Route::livewire('/posts/{id}', 'pages::post.show');
Route::livewire('/posts/{post}', 'pages::post.edit'); // Model binding
```

## PHP Attributes Reference

| Attribute | Purpose |
|-----------|---------|
| `#[Validate('rule')]` | Add validation rules to properties |
| `#[Computed]` | Create memoized derived properties |
| `#[Computed(persist: true)]` | Cache computed across requests |
| `#[Locked]` | Prevent client-side modification |
| `#[Reactive]` | Props update when parent changes |
| `#[On('event')]` | Listen for dispatched events |
| `#[Lazy]` | Defer component loading |
| `#[Session]` | Persist properties in session |
| `#[Url]` | Sync with query string |
| `#[Renderless]` | Skip re-render after action |
| `#[Async]` | Execute action in parallel |
| `#[Layout('name')]` | Specify custom layout |
| `#[Title('Title')]` | Set page title |
| `#[Js]` | Return JSON for JavaScript consumption |

## Common Gotchas

1. **Computed properties require `$this`** — use `$this->posts`, not `$posts`
2. **Default wire:model doesn't update as you type** — use `.live` modifier
3. **Dependent selects need wire:key** — prevents stale options
4. **Props aren't reactive by default** — use `#[Reactive]` attribute
5. **Always validate/authorize properties** — treat as user input
6. **Use `only()` or `except()`** to limit data sent to client

## Security Best Practices

1. **Always authorize action parameters** — users can call any public method
2. **Use `#[Locked]`** for sensitive IDs to prevent manipulation
3. **Mark dangerous methods as protected/private** — prevents client access
4. **Validate all input** — use `#[Validate]` or `rules()` method
5. **Never trust client-side data** — properties are user input

## Performance Tips

1. Use computed properties for expensive queries
2. Lazy load components below the fold
3. Use `.blur` instead of `.live` when real-time isn't needed
4. Avoid storing large Eloquent collections as properties
5. Use `wire:key` for list items to prevent DOM thrashing
6. Debounce live updates for better performance
7. Cache expensive operations with `#[Computed(persist: true)]`

## Resources

### For Component Architecture
See [references/core.md](references/core.md) — components, properties, lifecycle, actions

### For Forms & Validation
See [references/forms.md](references/forms.md) — form handling, validation, file uploads

### For Advanced Features
See [references/advanced.md](references/advanced.md) — nesting, events, computed properties, pagination

### For Directives
See [references/directives.md](references/directives.md) — all wire:* directives

### For Attributes
See [references/attributes.md](references/attributes.md) — all PHP attributes

### For Integration
See [references/integration.md](references/integration.md) — Alpine.js, JavaScript, security

### For Testing
See [references/testing.md](references/testing.md) — Pest/PHPUnit patterns
