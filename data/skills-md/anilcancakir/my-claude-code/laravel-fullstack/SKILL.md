---
name: laravel-fullstack
description: "Laravel Blade views, Alpine.js, Vue.js integration, TailwindCSS styling, Vite assets. ALWAYS activate when: working with resources/views/, Blade components, frontend forms, UI elements, modals, dropdowns, forms. Triggers on: görünmüyor, gösterilmiyor, sayfa yüklenmiyor, sayfa açılmıyor, form çalışmıyor, form gönderilmiyor, buton çalışmıyor, button not working, style bozuk, CSS bozuk, renk yanlış, color wrong, responsive bozuk, mobile görünüm, dark mode çalışmıyor, layout bozuk, component çalışmıyor, modal açılmıyor, dropdown çalışmıyor, asset yüklenmiyor, image not loading, JS error, JavaScript hatası."
---

# Laravel Fullstack

Blade + Alpine.js + Vue.js + TailwindCSS development for Laravel 12+.

## Stack Overview

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Views** | Blade | Server-rendered templates |
| **Interactivity** | Alpine.js | Lightweight JS framework |
| **SPA (optional)** | Vue.js | Complex client-side apps |
| **Styling** | TailwindCSS v4 | Utility-first CSS |
| **Assets** | Vite | Build tool |

## Blade Components

### Anonymous Components

```blade
{{-- resources/views/components/button.blade.php --}}
@props([
    'type' => 'button',
    'variant' => 'primary',
])

<button 
    type="{{ $type }}"
    {{ $attributes->class([
        'px-4 py-2 rounded-lg font-medium transition-colors',
        'bg-blue-600 text-white hover:bg-blue-700' => $variant === 'primary',
        'bg-gray-200 text-gray-800 hover:bg-gray-300' => $variant === 'secondary',
        'bg-red-600 text-white hover:bg-red-700' => $variant === 'danger',
    ]) }}
>
    {{ $slot }}
</button>

{{-- Usage --}}
<x-button variant="primary">Save</x-button>
<x-button variant="danger" type="submit">Delete</x-button>
```

### Class Components

```php
<?php

namespace App\View\Components;

use Illuminate\View\Component;
use Illuminate\View\View;

final class Alert extends Component
{
    public function __construct(
        public string $type = 'info',
        public ?string $title = null,
    ) {}

    public function render(): View
    {
        return view('components.alert');
    }

    public function iconClass(): string
    {
        return match($this->type) {
            'success' => 'text-green-500',
            'error' => 'text-red-500',
            'warning' => 'text-yellow-500',
            default => 'text-blue-500',
        };
    }
}
```

### Layouts

```blade
{{-- resources/views/layouts/app.blade.php --}}
<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ $title ?? config('app.name') }}</title>
    @vite(['resources/css/app.css', 'resources/js/app.js'])
</head>
<body class="bg-gray-100 dark:bg-gray-900">
    <x-navbar />
    
    <main class="container mx-auto py-8">
        {{ $slot }}
    </main>
    
    <x-footer />
</body>
</html>

{{-- Usage --}}
<x-layouts.app title="Dashboard">
    <h1>Welcome</h1>
</x-layouts.app>
```

## Alpine.js Patterns

### Basic Toggle

```blade
<div x-data="{ open: false }">
    <button @click="open = !open">
        Toggle Menu
    </button>
    
    <div x-show="open" x-transition>
        Menu content
    </div>
</div>
```

### Dropdown

```blade
<div x-data="{ open: false }" @click.away="open = false">
    <button @click="open = !open">
        Options
    </button>
    
    <div 
        x-show="open" 
        x-transition:enter="transition ease-out duration-100"
        x-transition:enter-start="opacity-0 scale-95"
        x-transition:enter-end="opacity-100 scale-100"
        x-transition:leave="transition ease-in duration-75"
        x-transition:leave-start="opacity-100 scale-100"
        x-transition:leave-end="opacity-0 scale-95"
        class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg"
    >
        <a href="#" class="block px-4 py-2 hover:bg-gray-100">Edit</a>
        <a href="#" class="block px-4 py-2 hover:bg-gray-100">Delete</a>
    </div>
</div>
```

### Modal

```blade
<div x-data="{ open: false }">
    <button @click="open = true">Open Modal</button>
    
    <div 
        x-show="open" 
        x-transition:enter="ease-out duration-300"
        x-transition:leave="ease-in duration-200"
        class="fixed inset-0 z-50 flex items-center justify-center"
    >
        {{-- Backdrop --}}
        <div 
            class="fixed inset-0 bg-black/50" 
            @click="open = false"
        ></div>
        
        {{-- Modal Content --}}
        <div class="relative bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h2 class="text-lg font-semibold">Modal Title</h2>
            <p class="mt-2">Modal content here</p>
            
            <div class="mt-4 flex justify-end gap-2">
                <button @click="open = false">Cancel</button>
                <button @click="open = false">Confirm</button>
            </div>
        </div>
    </div>
</div>
```

### Form with Loading State

```blade
<form 
    x-data="{ loading: false }"
    @submit.prevent="loading = true; $el.submit()"
    method="POST"
    action="{{ route('orders.store') }}"
>
    @csrf
    
    <input type="text" name="name" required>
    
    <button type="submit" :disabled="loading">
        <span x-show="!loading">Submit</span>
        <span x-show="loading">Processing...</span>
    </button>
</form>
```

## References

| Topic | Reference | When to Load |
|-------|-----------|--------------|
| Blade advanced | [references/blade.md](references/blade.md) | Slots, stacks, includes |
| Alpine.js patterns | [references/alpine.md](references/alpine.md) | Complex interactions |

## TailwindCSS v4 Quick Reference

```css
/* resources/css/app.css */
@import "tailwindcss";

@theme {
    --color-primary: #3b82f6;
    --color-secondary: #6b7280;
}
```

```blade
{{-- Dark mode --}}
<div class="bg-white dark:bg-gray-800">

{{-- Responsive --}}
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">

{{-- Transitions --}}
<button class="transition-colors duration-200 hover:bg-blue-700">
```

## Vite Setup

```js
// vite.config.js
import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: ['resources/css/app.css', 'resources/js/app.js'],
            refresh: true,
        }),
    ],
});
```

```bash
npm run dev     # Development with HMR
npm run build   # Production build
```
