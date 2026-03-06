---
name: shop-theme-development
description: "Shop theme development in Bagisto. Activates when creating custom storefront themes, modifying shop layouts, building theme packages, or working with Vite-powered assets for the customer-facing side of the application."
license: MIT
metadata:
  author: bagisto
---

# Shop Theme Development

## Overview

Shop theme development in Bagisto involves creating custom storefront themes packaged as Laravel packages. The end result is a self-contained package that can be distributed and maintained independently.

## When to Apply

Activate this skill when:
- Creating custom storefront themes as packages
- Building theme packages for distribution
- Working with Vite-powered assets
- Customizing customer-facing pages
- Overriding default shop templates

## Bagisto Shop Theme Architecture

### Core Components

| Component | Purpose | Location |
|-----------|---------|----------|
| **Theme Configuration** | Defines available themes | `config/themes.php` |
| **Views Path** | Blade template files | Defined in theme config |
| **Assets Path** | CSS, JS, images | Defined in theme config |
| **Theme Middleware** | Resolves active theme | `packages/Webkul/Shop/src/Http/Middleware/Theme.php` |
| **Theme Facade** | Manages theme operations | `packages/Webkul/Theme/src/Themes.php` |

### Key Configuration Properties

```php
// config/themes.php
'shop-default' => 'default',

'shop' => [
    'default' => [
        'name' => 'Default',
        'assets_path' => 'public/themes/shop/default',
        'views_path' => 'resources/themes/default/views',
        'vite' => [
            'hot_file' => 'shop-default-vite.hot',
            'build_directory' => 'themes/shop/default/build',
            'package_assets_directory' => 'src/Resources/assets',
        ],
    ],
],
```

## Creating Shop Theme Package

### Goal: Complete Self-Contained Package

The end result should be a complete package with:
- All views inside the package
- All assets inside the package
- Service provider for publishing
- Vite configuration for asset compilation

### Step 1: Create Package Structure

```bash
mkdir -p packages/Webkul/CustomTheme/src/{Providers,Resources/views}
```

### Step 2: Copy Complete Shop Assets

Copy all shop assets to your package to have full control:

```bash
# Copy complete shop assets folder
cp -r packages/Webkul/Shop/src/Resources/assets/* packages/Webkul/CustomTheme/src/Resources/assets/

# Copy complete shop views folder
cp -r packages/Webkul/Shop/src/Resources/views/* packages/Webkul/CustomTheme/src/Resources/views/

# Copy shop package.json for dependencies
cp packages/Webkul/Shop/package.json packages/Webkul/CustomTheme/
```

This gives you:
- Complete CSS foundation with Tailwind
- All JavaScript functionality
- Shop components and layouts
- Images, fonts, and static assets
- Complete Blade template structure
- Dependencies for asset compilation

### Step 3: Add Custom Home Page (Boilerplate)

After copying, create a custom home page to show it's a new theme:

**File:** `packages/Webkul/CustomTheme/src/Resources/views/home/index.blade.php`

```blade
<x-shop::layouts>
    <x-slot:title>
        Custom Theme Home
    </x-slot>

    {{-- Hero Section --}}
    <div class="hero-section bg-gradient-to-r from-blue-600 to-purple-600 text-white py-20">
        <div class="container mx-auto px-4 text-center">
            <h1 class="text-5xl font-bold mb-6">
                Welcome to Our Store
            </h1>
            
            <p class="text-xl mb-8 opacity-90">
                Professional theme with modern design
            </p>
            
            <a href="{{ route('shop.search.index') }}" 
               class="bg-white text-blue-600 font-bold py-3 px-8 rounded-lg hover:bg-gray-100 transition duration-300">
                Start Shopping
            </a>
        </div>
    </div>

    {{-- Featured Products --}}
    <div class="container mx-auto px-4 py-16">
        <h2 class="text-3xl font-bold text-center mb-12">
            Featured Products
        </h2>
        
        <!-- Product grid -->
    </div>
</x-shop::layouts>
```

### Step 4: Create Custom Layout (Optional)

Create your own master layout for complete control:

**File:** `packages/Webkul/CustomTheme/src/Resources/views/layouts/master.blade.php`

```blade
<!DOCTYPE html>
<html lang="{{ app()->getLocale() }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title ?? config('app.name') }}</title>
    
    {{-- Load theme assets manually --}}
    @bagistoVite([
        'src/Resources/assets/css/app.css',
        'src/Resources/assets/js/app.js'
    ])
    
    @stack('meta')
    @stack('styles')
</head>
<body class="{{ $bodyClass ?? '' }}">
    @if($hasHeader ?? true)
        @include('custom-theme::layouts.header')
    @endif
    
    <main class="main-content">
        {{ $slot }}
    </main>
    
    @if($hasFooter ?? true)
        @include('custom-theme::layouts.footer')
    @endif
    
    @stack('scripts')
</body>
</html>
```

### Step 5: Create Service Provider

**File:** `packages/Webkul/CustomTheme/src/Providers/CustomThemeServiceProvider.php`

```php
<?php

namespace Webkul\CustomTheme\Providers;

use Illuminate\Support\ServiceProvider;

class CustomThemeServiceProvider extends ServiceProvider
{
    /**
     * Register services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap services.
     */
    public function boot(): void
    {
        // Publish views to resources/themes/custom-theme/views
        $this->publishes([
            __DIR__ . '/../Resources/views' => resource_path('themes/custom-theme/views'),
        ], 'custom-theme-views');
    }
}
```

### Step 6: Configure Autoloading

Update `composer.json`:

```json
"autoload": {
    "psr-4": {
        "Webkul\\CustomTheme\\": "packages/Webkul/CustomTheme/src"
    }
}
```

Run: `composer dump-autoload`

### Step 7: Register Service Provider

Add to `bootstrap/providers.php`:

```php
Webkul\CustomTheme\Providers\CustomThemeServiceProvider::class,
```

### Step 8: Update Theme Configuration

**File:** `config/themes.php`

```php
'shop-default' => 'custom-theme',

'shop' => [
    'default' => [
        'name' => 'Default',
        'assets_path' => 'public/themes/shop/default',
        'views_path' => 'resources/themes/default/views',
        'vite' => [
            'hot_file' => 'shop-default-vite.hot',
            'build_directory' => 'themes/shop/default/build',
            'package_assets_directory' => 'src/Resources/assets',
        ],
    ],
    'custom-theme' => [
        'name' => 'Custom Theme Package',
        'assets_path' => 'public/themes/shop/custom-theme',
        'views_path' => 'resources/themes/custom-theme/views',
        'vite' => [
            'hot_file' => 'custom-theme-vite.hot',
            'build_directory' => 'themes/custom-theme/build',
            'package_assets_directory' => 'src/Resources/assets',
        ],
    ],
],
```

### Step 9: Publish Views

```bash
php artisan vendor:publish --provider="Webkul\CustomTheme\Providers\CustomThemeServiceProvider"
```

### Step 10: Clear Cache

```bash
php artisan optimize:clear
```

### Step 11: Activate Theme

1. Login to admin panel
2. Go to Settings → Channels
3. Edit channel and select your theme
4. Save

### Step 12: Build Assets

```bash
# Navigate to package
cd packages/Webkul/CustomTheme

# Install dependencies
npm install

# Build assets for production
npm run build
```

This will compile your theme assets and create the build directory. After building, your custom theme will be ready to use with the custom home page you created.

## Vite-Powered Assets

### Step 1: Create Asset Configuration Files

Create in your package root:

**File:** `package.json`

```json
{
    "name": "custom-theme",
    "private": true,
    "description": "Custom Theme Package for Bagisto",
    "scripts": {
        "dev": "vite",
        "build": "vite build"
    },
    "devDependencies": {
        "autoprefixer": "^10.4.14",
        "axios": "^1.1.2",
        "laravel-vite-plugin": "^0.7.2",
        "postcss": "^8.4.23",
        "tailwindcss": "^3.3.2",
        "vite": "^4.0.0"
    }
}
```

**File:** `vite.config.js`

```javascript
import { defineConfig, loadEnv } from "vite";
import laravel from "laravel-vite-plugin";
import path from "path";

export default defineConfig(({ mode }) => {
    const envDir = "../../../";

    Object.assign(process.env, loadEnv(mode, envDir));

    return {
        build: {
            emptyOutDir: true,
        },
        envDir,
        server: {
            host: process.env.VITE_HOST || "localhost",
            port: process.env.VITE_PORT || 5173,
            cors: true,
        },
        plugins: [
            laravel({
                hotFile: "../../../public/custom-theme-vite.hot",
                publicDirectory: "../../../public",
                buildDirectory: "themes/custom-theme/build",
                input: [
                    "src/Resources/assets/css/app.css",
                    "src/Resources/assets/js/app.js",
                ],
                refresh: true,
            }),
        ],
    };
});
```

**File:** `tailwind.config.js`

```javascript
module.exports = {
    content: [
        "./src/Resources/**/*.blade.php",
        "../../../resources/themes/custom-theme/**/*.blade.php"
    ],
    theme: {
        container: {
            center: true,
            screens: { "2xl": "1440px" },
            padding: { DEFAULT: "90px" },
        },
        screens: {
            sm: "525px",
            md: "768px",
            lg: "1024px",
            xl: "1240px",
            "2xl": "1440px",
            1180: "1180px",
            1060: "1060px",
            991: "991px",
        },
        extend: {
            colors: {
                navyBlue: "#060C3B",
                darkGreen: "#40994A",
            },
            fontFamily: {
                poppins: ["Poppins"],
                dmserif: ["DM Serif Display"],
            },
        },
    },
    plugins: [],
    safelist: [{ pattern: /icon-/ }],
};
```

**File:** `postcss.config.js`

```javascript
module.exports = {
    plugins: {
        tailwindcss: {},
        autoprefixer: {},
    },
}
```

### Step 2: Add to Bagisto Vite Config

**File:** `config/bagisto-vite.php`

```php
'custom-theme' => [
    'hot_file' => 'custom-theme-vite.hot',
    'build_directory' => 'themes/custom-theme/build',
    'package_assets_directory' => 'src/Resources/assets',
],
```

### Development Commands

```bash
# Navigate to package
cd packages/Webkul/CustomTheme

# Install dependencies
npm install

# Start dev server with hot reload
npm run dev

# Build for production
npm run build
```

## Development Workflow

### Option A: Symlink (Recommended)

Create symlink for real-time development without republishing:

```bash
# Remove published views
rm -rf resources/themes/custom-theme/views

# Create symlink from package to resources
ln -s $(pwd)/packages/Webkul/CustomTheme/src/Resources/views resources/themes/custom-theme/views
```

### Option B: Direct Package Development

Work directly in package and republish when needed:

```bash
# After making changes
php artisan vendor:publish --provider="Webkul\CustomTheme\Providers\CustomThemeServiceProvider" --force
```

## Shop Layouts

### Using Shop Layout

```blade
<x-shop::layouts>
    <x-slot:title>
        Page Title
    </x-slot>

    {{-- Page content --}}
</x-shop::layouts>
```

### Layout Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `has-header` | Boolean | true | Include header navigation |
| `has-feature` | Boolean | true | Show featured section |
| `has-footer` | Boolean | true | Include footer |

### Minimal Page Example

```blade
<x-shop::layouts
    :has-header="false"
    :has-footer="false"
>
    <x-slot:title>
        Minimal Page
    </x-slot>

    {{-- Content without header/footer --}}
</x-shop::layouts>
```

## Shop Blade Components

### Available Components

| Component | Usage | Description |
|-----------|-------|-------------|
| `<x-shop::accordion>` | Collapsible sections | Toggle content visibility |
| `<x-shop::breadcrumbs>` | Navigation trail | Show current page path |
| `<x-shop::button>` | Action buttons | Loading states supported |
| `<x-shop::datagrid>` | Data tables | Sorting, filtering, pagination |
| `<x-shop::drawer>` | Slide-out panels | Position: top/bottom/left/right |
| `<x-shop::dropdown>` | Dropdown menus | Position: top-left, bottom-right, etc. |
| `<x-shop::flat-picker.date>` | Date picker | Based on Flatpickr |
| `<x-shop::flat-picker.datetime>` | Date-time picker | Based on Flatpickr |
| `<x-shop::media.images>` | Image upload | Multiple images support |
| `<x-shop::modal>` | Dialog boxes | Header, content, footer slots |
| `<x-shop::quantity-changer>` | Quantity input | +/- buttons |
| `<x-shop::table>` | Data tables | Customizable thead/tbody |
| `<x-shop::tabs>` | Tab navigation | Position: left/right/center |
| `<x-shop::shimmer.*>` | Loading effects | Skeleton loaders |

## Custom Layouts

### Creating Custom Layout

**File:** `packages/Webkul/CustomTheme/src/Resources/views/layouts/master.blade.php`

```blade
<!DOCTYPE html>
<html lang="{{ app()->getLocale() }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ $title ?? config('app.name') }}</title>
    
    {{-- Load assets manually for custom layouts --}}
    @bagistoVite([
        'src/Resources/assets/css/app.css',
        'src/Resources/assets/js/app.js'
    ])
</head>
<body>
    @if($hasHeader ?? true)
        @include('custom-theme::layouts.header')
    @endif
    
    <main>
        {{ $slot }}
    </main>
    
    @if($hasFooter ?? true)
        @include('custom-theme::layouts.footer')
    @endif
</body>
</html>
```

## Complete Package Structure

```
packages/Webkul/CustomTheme/
├── src/
│   ├── Providers/
│   │   └── CustomThemeServiceProvider.php
│   └── Resources/
│       ├── assets/
│       │   ├── css/
│       │   │   └── app.css
│       │   ├── js/
│       │   │   └── app.js
│       │   ├── images/
│       │   └── fonts/
│       └── views/
│           ├── layouts/
│           │   └── master.blade.php
│           ├── home/
│           │   └── index.blade.php
│           ├── components/
│           └── ...
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Key Files Reference

| File | Purpose |
|------|---------|
| `config/themes.php` | Theme configuration |
| `config/bagisto-vite.php` | Vite asset configuration |
| `packages/Webkul/Shop/src/Providers/ShopServiceProvider.php` | Shop package registration |
| `packages/Webkul/Shop/src/Http/Middleware/Theme.php` | Theme resolution |
| `packages/Webkul/Theme/src/Themes.php` | Theme facade |
| `packages/Webkul/Shop/src/Resources/views/components/*` | Shop components |

## Common Pitfalls

- Not clearing cache after theme config changes
- Forgetting to run composer dump-autoload after package registration
- Not copying complete shop assets (views and assets)
- Using custom layouts without manually loading @bagistoVite assets
- Working in published files instead of package source files
- Missing symlink setup for development workflow

## Testing

Test your theme by:
1. Activating theme in channel settings
2. Visiting storefront pages
3. Checking responsive design
4. Verifying all shop functionality works
5. Testing hot reload during development
