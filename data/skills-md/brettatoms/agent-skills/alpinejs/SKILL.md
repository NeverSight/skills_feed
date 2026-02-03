---
name: alpinejs
description: AlpineJS best practices and patterns. Use when writing HTML with Alpine.js directives to avoid common mistakes like long inline JavaScript strings.
---

# AlpineJS Best Practices

## Golden Rule: Keep Attributes Short

**Never** put complex logic in HTML attributes. If your `x-data`, `x-init`, or any directive exceeds ~50 characters, extract it.

## Directive Cheatsheet

| Directive | Purpose | Example |
|-----------|---------|---------|
| `x-data` | Declare reactive component state | `x-data="{ open: false }"` |
| `x-init` | Run code on component init | `x-init="fetchData()"` |
| `x-show` | Toggle visibility (CSS display) | `x-show="open"` |
| `x-if` | Conditional rendering (must wrap `<template>`) | `<template x-if="show">` |
| `x-for` | Loop (must wrap `<template>`) | `<template x-for="item in items">` |
| `x-bind:` / `:` | Bind attribute to expression | `:class="{ active: isActive }"` |
| `x-on:` / `@` | Listen to events | `@click="open = !open"` |
| `x-model` | Two-way bind form inputs | `x-model="email"` |
| `x-text` | Set text content | `x-text="message"` |
| `x-html` | Set inner HTML | `x-html="htmlContent"` |
| `x-ref` | Reference element via `$refs` | `x-ref="input"` |
| `x-cloak` | Hide until Alpine initializes | `x-cloak` (add CSS: `[x-cloak] { display: none; }`) |
| `x-transition` | Apply enter/leave transitions | `x-transition` or `x-transition.duration.300ms` |
| `x-effect` | Run reactive side effects | `x-effect="console.log(count)"` |
| `x-ignore` | Skip Alpine initialization | `x-ignore` |
| `x-teleport` | Move element to another location | `x-teleport="#modals"` |
| `x-modelable` | Expose property for external binding | `x-modelable="value"` |

## Magic Properties

| Property | Description |
|----------|-------------|
| `$el` | Current DOM element |
| `$refs` | Access elements with `x-ref` |
| `$store` | Access global Alpine stores |
| `$watch` | Watch a property for changes |
| `$dispatch` | Dispatch custom events |
| `$nextTick` | Run after DOM updates |
| `$root` | Root element of component |
| `$data` | Access component data object |
| `$id` | Generate unique IDs |

## Patterns

### ❌ BAD: Long Inline JavaScript

```html
<!-- DON'T DO THIS -->
<div x-data="{ items: [], loading: true, error: null, async fetchItems() { this.loading = true; try { const res = await fetch('/api/items'); this.items = await res.json(); } catch (e) { this.error = e.message; } finally { this.loading = false; } } }" x-init="fetchItems()">
```

### ✅ GOOD: Extract to Function

```html
<script>
function itemList() {
  return {
    items: [],
    loading: true,
    error: null,
    
    async fetchItems() {
      this.loading = true;
      try {
        const res = await fetch('/api/items');
        this.items = await res.json();
      } catch (e) {
        this.error = e.message;
      } finally {
        this.loading = false;
      }
    }
  };
}
</script>

<div x-data="itemList()" x-init="fetchItems()">
  <!-- template -->
</div>
```

### ✅ GOOD: Simple Inline State

```html
<!-- Simple state is fine inline -->
<div x-data="{ open: false, count: 0 }">
  <button @click="open = !open">Toggle</button>
  <div x-show="open" x-transition>Content</div>
</div>
```

### ✅ GOOD: Global Store for Shared State

```html
<script>
document.addEventListener('alpine:init', () => {
  Alpine.store('cart', {
    items: [],
    add(item) { this.items.push(item); },
    get total() { return this.items.reduce((sum, i) => sum + i.price, 0); }
  });
});
</script>

<div x-data>
  <span x-text="$store.cart.total"></span>
</div>
```

### ✅ GOOD: Reusable Component with Alpine.data()

```html
<script>
document.addEventListener('alpine:init', () => {
  Alpine.data('dropdown', () => ({
    open: false,
    toggle() { this.open = !this.open; },
    close() { this.open = false; }
  }));
});
</script>

<div x-data="dropdown" @click.outside="close()">
  <button @click="toggle()">Menu</button>
  <ul x-show="open" x-transition>
    <li>Item 1</li>
  </ul>
</div>
```

### ✅ GOOD: Form with Validation

```html
<script>
function contactForm() {
  return {
    email: '',
    message: '',
    errors: {},
    
    validate() {
      this.errors = {};
      if (!this.email.includes('@')) this.errors.email = 'Invalid email';
      if (this.message.length < 10) this.errors.message = 'Too short';
      return Object.keys(this.errors).length === 0;
    },
    
    submit() {
      if (this.validate()) {
        // submit logic
      }
    }
  };
}
</script>

<form x-data="contactForm()" @submit.prevent="submit()">
  <input x-model="email" type="email">
  <span x-show="errors.email" x-text="errors.email" class="error"></span>
  
  <textarea x-model="message"></textarea>
  <span x-show="errors.message" x-text="errors.message" class="error"></span>
  
  <button type="submit">Send</button>
</form>
```

### Event Modifiers

```html
@click.prevent     <!-- preventDefault() -->
@click.stop        <!-- stopPropagation() -->
@click.outside     <!-- Click outside element -->
@click.window      <!-- Listen on window -->
@click.document    <!-- Listen on document -->
@click.once        <!-- Fire once -->
@click.debounce    <!-- Debounce (default 250ms) -->
@click.throttle    <!-- Throttle -->
@keydown.enter     <!-- Specific key -->
@keydown.escape    <!-- Escape key -->
```

### Transition Modifiers

```html
x-transition                           <!-- Default fade -->
x-transition.duration.300ms            <!-- Custom duration -->
x-transition.opacity                   <!-- Opacity only -->
x-transition.scale.90                  <!-- Scale from 90% -->
x-transition:enter.duration.500ms      <!-- Enter duration -->
x-transition:leave.duration.200ms      <!-- Leave duration -->
```

## Quick Decision Guide

1. **State is 1-3 simple properties?** → Inline `x-data="{ open: false }"`
2. **Has methods or complex logic?** → Extract to `function componentName() { return {...} }`
3. **Reused across pages?** → Use `Alpine.data('name', () => ({...}))`
4. **Shared global state?** → Use `Alpine.store('name', {...})`
5. **Long attribute string?** → You're doing it wrong. Extract it.
