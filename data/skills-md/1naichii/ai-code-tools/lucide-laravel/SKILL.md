---
name: lucide-laravel
description: Lucide icon library integration for Laravel Blade templates. Use when working with Lucide icons in Laravel applications, Blade components with the x-lucide- prefix, icon styling with Tailwind CSS, dynamic icon rendering in Blade, or any Laravel view work requiring SVG icons. Keywords include lucide icons, blade icons, x-lucide, SVG icons Laravel, blade-lucide-icons, mallardduck/blade-lucide-icons.
---

# Lucide Laravel

Laravel Blade integration for the [Lucide](https://lucide.dev) icon library - 1,666+ beautiful, consistent SVG icons.

## Installation

```bash
composer require mallardduck/blade-lucide-icons
```

Clear view cache if icons don't appear:

```bash
php artisan view:clear
```

## Quick Start

### Basic Usage

Icons use the `x-lucide-` prefix with kebab-case naming:

```blade
<x-lucide-activity />
<x-lucide-heart />
<x-lucide-shopping-cart />
<x-lucide-circle-check />
```

### Naming Convention

Convert PascalCase icon names to kebab-case:

| Icon Name | Blade Component |
|-----------|----------------|
| Activity | `<x-lucide-activity />` |
| ShoppingCart | `<x-lucide-shopping-cart />` |
| CircleCheck | `<x-lucide-circle-check />` |
| ArrowRight | `<x-lucide-arrow-right />` |

## Styling

### Tailwind CSS

```blade
<!-- Size and color -->
<x-lucide-album class="w-6 h-6 text-gray-500"/>

<!-- Responsive sizing -->
<x-lucide-heart class="w-4 h-4 md:w-6 md:h-6 text-red-500"/>

<!-- Hover effects -->
<x-lucide-star class="w-5 h-5 text-yellow-400 hover:text-yellow-500 cursor-pointer"/>

<!-- Transitions -->
<x-lucide-bell class="w-6 h-6 text-gray-700 hover:text-gray-900 transition-colors duration-200"/>
```

### Inline Styles

```blade
<x-lucide-anchor style="color: #555"/>
<x-lucide-heart style="color: #ff0000; width: 48px; height: 48px;"/>
<x-lucide-activity style="color: var(--primary-color); stroke-width: 1.5;"/>
```

## Common Patterns

### Navigation Menus

```blade
<nav>
    <div class="flex items-center gap-6">
        <a href="/dashboard" class="flex items-center gap-2">
            <x-lucide-layout-dashboard class="w-5 h-5"/>
            <span>Dashboard</span>
        </a>
        <a href="/products" class="flex items-center gap-2">
            <x-lucide-package class="w-5 h-5"/>
            <span>Products</span>
        </a>
        <a href="/settings" class="flex items-center gap-2">
            <x-lucide-settings class="w-5 h-5"/>
            <span>Settings</span>
        </a>
    </div>
</nav>
```

### Form Inputs

```blade
<div class="relative">
    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
        <x-lucide-search class="w-5 h-5 text-gray-400"/>
    </div>
    <input type="text" class="pl-10 w-full border rounded-lg" placeholder="Search..."/>
</div>
```

### Alerts

```blade
<!-- Success -->
<div class="flex items-start gap-3 p-4 bg-green-50 border-l-4 border-green-500 rounded">
    <x-lucide-check-circle class="w-6 h-6 text-green-600 flex-shrink-0"/>
    <div>
        <h4 class="font-semibold text-green-800">Success!</h4>
        <p class="text-green-700">Your changes have been saved.</p>
    </div>
</div>

<!-- Error -->
<div class="flex items-start gap-3 p-4 bg-red-50 border-l-4 border-red-500 rounded">
    <x-lucide-alert-circle class="w-6 h-6 text-red-600 flex-shrink-0"/>
    <div>
        <h4 class="font-semibold text-red-800">Error</h4>
        <p class="text-red-700">Something went wrong.</p>
    </div>
</div>

<!-- Info -->
<div class="flex items-start gap-3 p-4 bg-blue-50 border-l-4 border-blue-500 rounded">
    <x-lucide-info class="w-6 h-6 text-blue-600 flex-shrink-0"/>
    <p class="text-blue-700">Please review your changes before submitting.</p>
</div>
```

### Action Buttons

```blade
<!-- Icon-only button with aria-label -->
<button class="p-2 hover:bg-gray-100 rounded" aria-label="Delete">
    <x-lucide-trash class="w-5 h-5 text-red-600"/>
</button>

<!-- Button with icon and text -->
<button class="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
    <x-lucide-save class="w-5 h-5"/>
    <span>Save</span>
</button>

<!-- Primary action -->
<button class="flex items-center gap-2 bg-green-600 text-white px-4 py-2 rounded-lg">
    <x-lucide-plus class="w-5 h-5"/>
    <span>Add New</span>
</button>
```

### With Livewire

```blade
<!-- Loading states -->
<button wire:click="refresh" class="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg">
    <x-lucide-refresh-cw class="w-5 h-5" wire:loading.class="animate-spin"/>
    <span wire:loading.remove>Refresh Data</span>
    <span wire:loading>Loading...</span>
</button>

<!-- Toggle icon based on state -->
<div class="flex items-center gap-2">
    @if($isFavorited)
        <x-lucide-heart class="w-5 h-5 text-red-500 fill-current" wire:click="unfavorite"/>
    @else
        <x-lucide-heart class="w-5 h-5 text-gray-400" wire:click="favorite"/>
    @endif
</div>
```

## Dynamic Icons

Use `<x-dynamic-component>` for dynamic icon names:

```blade
@php
    $iconName = 'heart';
    $iconComponent = 'lucide-' . $iconName;
@endphp

<x-dynamic-component :component="$iconComponent" class="w-6 h-6" />
```

Common use case - icon from database:

```blade
<x-dynamic-component
    :component="'lucide-' . $menu->icon"
    class="w-5 h-5"
/>
```

## Best Practices

### Consistent Sizing

| Context | Size |
|---------|------|
| Navigation | `w-5 h-5` |
| Button (small) | `w-4 h-4` |
| Button (medium) | `w-5 h-5` |
| Feature icons | `w-12 h-12` |
| Hero icons | `w-16 h-16` |

### Semantic Icon Usage

Choose icons that clearly represent their action:

```blade
<x-lucide-trash />        <!-- Delete -->
<x-lucide-edit />         <!-- Edit -->
<x-lucide-download />     <!-- Download -->
<x-lucide-upload />       <!-- Upload -->
<x-lucide-copy />         <!-- Copy -->
<x-lucide-share />        <!-- Share -->
<x-lucide-settings />     <!-- Settings -->
<x-lucide-user />         <!-- User/Profile -->
<x-lucide-home />         <!-- Home -->
```

### Color Semantics

```blade
<!-- Primary actions -->
<x-lucide-save class="w-5 h-5 text-blue-600"/>

<!-- Success states -->
<x-lucide-check class="w-5 h-5 text-green-600"/>
<x-lucide-check-circle class="w-5 h-5 text-green-600"/>

<!-- Danger/warning -->
<x-lucide-trash class="w-5 h-5 text-red-600"/>
<x-lucide-alert-triangle class="w-5 h-5 text-yellow-600"/>

<!-- Neutral/secondary -->
<x-lucide-info class="w-5 h-5 text-gray-600"/>
```

### Accessibility

```blade
<!-- Icon-only button - always include aria-label -->
<button aria-label="Close dialog">
    <x-lucide-x class="w-6 h-6"/>
</button>

<!-- Decorative icon - hide from screen readers -->
<x-lucide-star class="w-5 h-5" aria-hidden="true"/>

<!-- Icon with visible text - accessible by default -->
<button class="flex items-center gap-2">
    <x-lucide-download class="w-5 h-5"/>
    <span>Download</span>
</button>
```

## Icon Reference

**Total Icons:** 1,666 across 43 categories

### Quick Reference

| Category | Count | File | Common Icons |
|----------|-------|------|--------------|
| Accessibility | 30 | [accessibility.md](references/categories/accessibility.md) | `accessibility`, `eye`, `ear`, `glasses`, `sun`, `moon` |
| Accounts & access | 133 | [accounts-access.md](references/categories/accounts-access.md) | `user`, `users`, `shield`, `key`, `lock`, `log-in`, `log-out` |
| Animals | 23 | [animals.md](references/categories/animals.md) | `dog`, `cat`, `bird`, `bug`, `fish`, `paw-print` |
| Arrows | 209 | [arrows.md](references/categories/arrows.md) | `arrow-up`, `arrow-down`, `chevron-left`, `chevron-right` |
| Brands | 21 | [brands.md](references/categories/brands.md) | `github`, `twitter`, `facebook`, `instagram`, `youtube` |
| Buildings | 25 | [buildings.md](references/categories/buildings.md) | `building`, `building-2`, `home`, `warehouse`, `store` |
| Charts | 31 | [charts.md](references/categories/charts.md) | `bar-chart`, `line-chart`, `pie-chart`, `trending-up`, `trending-down` |
| Coding & development | 243 | [coding-development.md](references/categories/coding-development.md) | `code`, `terminal`, `git-branch`, `git-commit`, `bug`, `cpu` |
| Communication | 54 | [communication.md](references/categories/communication.md) | `mail`, `message-circle`, `phone`, `send`, `bell`, `rss` |
| Connectivity | 90 | [connectivity.md](references/categories/connectivity.md) | `wifi`, `bluetooth`, `usb`, `cast`, `radio`, `signal` |
| Cursors | 33 | [cursors.md](references/categories/cursors.md) | `mouse-pointer`, `hand`, `move`, `crosshair`, `pointer` |
| Design | 145 | [design.md](references/categories/design.md) | `palette`, `paintbrush`, `eraser`, `pen-tool`, `selection` |
| Devices | 164 | [devices.md](references/categories/devices.md) | `laptop`, `monitor`, `smartphone`, `tablet`, `keyboard`, `hard-drive` |
| Emoji | 28 | [emoji.md](references/categories/emoji.md) | `smile`, `frown`, `meh`, `heart`, `thumbs-up`, `thumbs-down` |
| File icons | 162 | [file-icons.md](references/categories/file-icons.md) | `file`, `file-text`, `folder`, `upload`, `download`, `copy` |
| Finance | 56 | [finance.md](references/categories/finance.md) | `dollar-sign`, `credit-card`, `wallet`, `banknote`, `coins`, `piggy-bank` |
| Food & beverage | 69 | [food-beverage.md](references/categories/food-beverage.md) | `coffee`, `utensils`, `pizza`, `burger`, `beer`, `cake` |
| Gaming | 148 | [gaming.md](references/categories/gaming.md) | `gamepad`, `gamepad-2`, `trophy`, `dice`, `puzzle`, `sword` |
| Home | 57 | [home.md](references/categories/home.md) | `couch`, `chair`, `bed`, `lamp`, `tv`, `bathtub` |
| Layout | 139 | [layout.md](references/categories/layout.md) | `layout`, `panel-left`, `panel-right`, `columns`, `sidebar`, `grid` |
| Mail | 26 | [mail.md](references/categories/mail.md) | `mail`, `inbox`, `send`, `at-sign`, `mail-open`, `mail-check` |
| Mathematics | 74 | [mathematics.md](references/categories/mathematics.md) | `equal`, `plus`, `minus`, `divide`, `percent`, `infinity` |
| Medical | 42 | [medical.md](references/categories/medical.md) | `heart-pulse`, `activity`, `pill`, `syringe`, `stethoscope`, `bone` |
| Multimedia | 138 | [multimedia.md](references/categories/multimedia.md) | `play`, `pause`, `volume`, `music`, `image`, `video` |
| Nature | 23 | [nature.md](references/categories/nature.md) | `tree`, `flower`, `leaf`, `sun`, `cloud`, `mountain` |
| Navigation, Maps, POIs | 84 | [navigation-maps-pois.md](references/categories/navigation-maps-pois.md) | `map`, `map-pin`, `compass`, `navigation`, `route`, `flag` |
| Notification | 39 | [notification.md](references/categories/notification.md) | `bell`, `bell-ring`, `alert-circle`, `alert-triangle`, `info` |
| People | 3 | [people.md](references/categories/people.md) | `user`, `users`, `user-plus` |
| Photography | 75 | [photography.md](references/categories/photography.md) | `camera`, `image`, `aperture`, `shutter`, `lens`, `film` |
| Science | 32 | [science.md](references/categories/science.md) | `flask`, `microscope`, `atom`, `beaker`, `magnet`, `dna` |
| Seasons | 5 | [seasons.md](references/categories/seasons.md) | `sun`, `cloud-rain`, `snowflake`, `thermometer` |
| Security | 55 | [security.md](references/categories/security.md) | `shield`, `lock`, `unlock`, `key`, `fingerprint`, `eye-off` |
| Shapes | 48 | [shapes.md](references/categories/shapes.md) | `circle`, `square`, `triangle`, `star`, `hexagon`, `diamond` |
| Shopping | 27 | [shopping.md](references/categories/shopping.md) | `shopping-cart`, `shopping-bag`, `credit-card`, `tag`, `package` |
| Social | 119 | [social.md](references/categories/social.md) | `heart`, `thumbs-up`, `share`, `bookmark`, `user-plus`, `link` |
| Sports | 13 | [sports.md](references/categories/sports.md) | `football`, `basketball`, `tennis`, `golf`, `trophy`, `medal` |
| Sustainability | 24 | [sustainability.md](references/categories/sustainability.md) | `recycle`, `leaf`, `tree`, `sun`, `wind`, `droplet` |
| Text formatting | 246 | [text-formatting.md](references/categories/text-formatting.md) | `bold`, `italic`, `underline`, `align-left`, `list`, `quote` |
| Time & calendar | 58 | [time-calendar.md](references/categories/time-calendar.md) | `calendar`, `clock`, `timer`, `hourglass`, `watch`, `alarm` |
| Tools | 66 | [tools.md](references/categories/tools.md) | `hammer`, `wrench`, `screwdriver`, `saw`, `drill`, `measure` |
| Transportation | 64 | [transportation.md](references/categories/transportation.md) | `car`, `bus`, `train`, `plane`, `bike`, `ship` |
| Travel | 67 | [travel.md](references/categories/travel.md) | `suitcase`, `plane`, `hotel`, `map`, `compass`, `passport` |
| Weather | 45 | [weather.md](references/categories/weather.md) | `sun`, `cloud`, `cloud-rain`, `snowflake`, `lightning`, `wind` |

### Finding Icons

1. **Browse by category:** Read the category reference files for complete icon lists
2. **Search visually:** Visit [lucide.dev/icons](https://lucide.dev/icons/)
3. **Use autocomplete:** IDEs with Blade autocomplete can suggest available icons

### Category File Format

Each category file contains:
- Icon count and description
- Complete table of icons with Blade component syntax
- Related categories for each icon
- Usage examples specific to that category

## Troubleshooting

**Icons not displaying:**
```bash
php artisan view:clear
```

**Styling not applied:**
- Ensure Tailwind processes Blade files
- Check icon names use kebab-case

**Publish raw SVGs (optional):**
```bash
php artisan vendor:publish --tag=blade-lucide-icons --force
```
