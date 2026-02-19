---
name: filament-dashboard
description: Create FilamentPHP v4 dashboard pages with single-tab or multi-tab layouts, message callouts, and widget integration
---

# FilamentPHP Dashboard Page Generation Skill

## Overview

This skill generates FilamentPHP v4 dashboard pages that follow a consistent pattern:
- Extends `Filament\Pages\Page`
- Supports single-tab (no tabs UI) or multi-tab layouts
- Includes optional color-coded message callouts
- Renders widgets using the standard Filament widgets component
- Uses Livewire reactive tabs with `$activeTab` state

## Documentation Reference

**CRITICAL:** Before generating dashboard pages, read:
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/general/06-navigation/`
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/widgets/`

## Pattern Architecture

A dashboard page in this style has 3 pieces:

1. **Filament Page class** (PHP)
   - Extends `Filament\Pages\Page`
   - Sets `$view`
   - Declares navigation metadata (icon/label/group/sort)
   - Stores Livewire public state: `$activeTab`
   - Provides `getTabs(): array` and `getActiveTabData(): ?array`

2. **Blade view** (`resources/views/filament/{panel}/pages/{slug}.blade.php`)
   - Renders tabs navigation (optional, for multi-tab)
   - Renders optional message callout (color-coded)
   - Renders widgets using: `<x-filament-widgets::widgets :widgets="$activeTabData['widgets']" />`

3. **Widgets** (Filament Widgets)
   - Each tab is basically "a widget list"
   - Widgets are referenced as `::class` strings

## Tab Schema Contract

Each tab must follow this array schema:

```php
[
    'key' => 'overview',                     // Required: unique identifier
    'title' => 'Overview',                   // Required: display title
    'icon' => 'heroicon-o-chart-bar',        // Optional: Heroicon name
    'message' => '<strong>Note:</strong> ...', // Optional: HTML message
    'messageColor' => 'blue',                // Optional: blue|green|purple|orange|indigo|gray
    'widgets' => [                           // Optional: widget class references
        \App\Filament\Admin\Widgets\SomeWidget::class,
        \App\Filament\Admin\Widgets\AnotherWidget::class,
    ],
],
```

## Multi-Tab Dashboard Page Template

### PHP Class Template

```php
<?php

declare(strict_types=1);

namespace App\Filament\__PANEL__\Pages;

use BackedEnum;
use Filament\Pages\Page;

class __PAGE_CLASS__ extends Page
{
    protected static string $view = 'filament.__PANEL_LOWER__.pages.__VIEW_SLUG__';

    protected static string|BackedEnum|null $navigationIcon = '__HEROICON__';
    protected static ?string $navigationLabel = '__NAV_LABEL__';
    protected static \UnitEnum|string|null $navigationGroup = '__NAV_GROUP__';
    protected static ?int $navigationSort = __NAV_SORT__;

    public string $activeTab = '__DEFAULT_TAB_KEY__';

    /**
     * Get the tabs configuration for this dashboard page.
     *
     * @return array<int, array{
     *   key: string,
     *   title: string,
     *   icon?: string,
     *   message?: string,
     *   messageColor?: string,
     *   widgets?: array<int, class-string>
     * }>
     */
    public function getTabs(): array
    {
        return [
            [
                'key' => '__TAB_KEY__',
                'icon' => '__TAB_ICON__',
                'title' => '__TAB_TITLE__',
                'message' => '__TAB_MESSAGE_HTML__',
                'messageColor' => '__TAB_COLOR__',
                'widgets' => [
                    // \App\Filament\__PANEL__\Widgets\ExampleWidget::class,
                ],
            ],
            // Additional tabs...
        ];
    }

    /**
     * Get the data for the currently active tab.
     */
    public function getActiveTabData(): ?array
    {
        return collect($this->getTabs())->firstWhere('key', $this->activeTab);
    }
}
```

### Blade View Template (Multi-Tab)

```blade
<x-filament-panels::page>
    @php
        $tabs = $this->getTabs();
        $activeTabData = $this->getActiveTabData();

        // If activeTab is invalid, fall back to first tab to avoid empty page.
        if (! $activeTabData && count($tabs) > 0) {
            $this->activeTab = $tabs[0]['key'];
            $activeTabData = $tabs[0];
        }
    @endphp

    <div class="space-y-6">
        {{-- Tabs Navigation --}}
        <div class="border-b border-gray-200 dark:border-gray-700">
            <nav class="-mb-px flex flex-wrap gap-x-8" aria-label="Tabs">
                @foreach($tabs as $tab)
                    <button
                        type="button"
                        wire:click="$set('activeTab', '{{ $tab['key'] }}')"
                        @class([
                            'flex items-center gap-2 whitespace-nowrap border-b-2 py-4 px-1 text-sm font-medium',
                            'border-primary-500 text-primary-600 dark:border-primary-400 dark:text-primary-400' => $activeTab === $tab['key'],
                            'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700 dark:text-gray-400 dark:hover:border-gray-600 dark:hover:text-gray-300' => $activeTab !== $tab['key'],
                        ])
                    >
                        @if(!empty($tab['icon']))
                            <x-filament::icon :icon="$tab['icon']" class="h-5 w-5" />
                        @endif

                        {{ $tab['title'] }}
                    </button>
                @endforeach
            </nav>
        </div>

        {{-- Tab Content --}}
        @if($activeTabData)
            <div class="space-y-6">
                @if(!empty($activeTabData['message']))
                    @php
                        $color = $activeTabData['messageColor'] ?? 'gray';
                    @endphp

                    <div @class([
                        'rounded-lg p-4 border',
                        'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800' => $color === 'blue',
                        'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800' => $color === 'green',
                        'bg-purple-50 dark:bg-purple-900/20 border-purple-200 dark:border-purple-800' => $color === 'purple',
                        'bg-orange-50 dark:bg-orange-900/20 border-orange-200 dark:border-orange-800' => $color === 'orange',
                        'bg-indigo-50 dark:bg-indigo-900/20 border-indigo-200 dark:border-indigo-800' => $color === 'indigo',
                        'bg-gray-50 dark:bg-gray-900/20 border-gray-200 dark:border-gray-800' => $color === 'gray',
                    ])>
                        <p @class([
                            'text-sm',
                            'text-blue-700 dark:text-blue-300' => $color === 'blue',
                            'text-green-700 dark:text-green-300' => $color === 'green',
                            'text-purple-700 dark:text-purple-300' => $color === 'purple',
                            'text-orange-700 dark:text-orange-300' => $color === 'orange',
                            'text-indigo-700 dark:text-indigo-300' => $color === 'indigo',
                            'text-gray-700 dark:text-gray-300' => $color === 'gray',
                        ])>
                            {!! $activeTabData['message'] !!}
                        </p>
                    </div>
                @endif

                @if(!empty($activeTabData['widgets']))
                    <x-filament-widgets::widgets :widgets="$activeTabData['widgets']" />
                @endif
            </div>
        @endif
    </div>
</x-filament-panels::page>
```

## Single-Tab Dashboard Page Template

Use this when you want a page that behaves like "one tab" without showing navigation.

### PHP Class Template (Single-Tab)

```php
<?php

declare(strict_types=1);

namespace App\Filament\__PANEL__\Pages;

use BackedEnum;
use Filament\Pages\Page;

class __PAGE_CLASS__ extends Page
{
    protected static string $view = 'filament.__PANEL_LOWER__.pages.__VIEW_SLUG__';

    protected static string|BackedEnum|null $navigationIcon = '__HEROICON__';
    protected static ?string $navigationLabel = '__NAV_LABEL__';
    protected static \UnitEnum|string|null $navigationGroup = '__NAV_GROUP__';
    protected static ?int $navigationSort = __NAV_SORT__;

    public string $activeTab = 'main';

    /**
     * Get the tabs configuration (single tab for this page).
     *
     * @return array<int, array{
     *   key: string,
     *   title: string,
     *   message?: string,
     *   messageColor?: string,
     *   widgets?: array<int, class-string>
     * }>
     */
    public function getTabs(): array
    {
        return [
            [
                'key' => 'main',
                'title' => '__PAGE_TITLE__',
                'message' => '__MESSAGE_HTML__',
                'messageColor' => '__COLOR__',
                'widgets' => [
                    // \App\Filament\__PANEL__\Widgets\ExampleWidget::class,
                ],
            ],
        ];
    }

    /**
     * Get the data for the active tab (always the single main tab).
     */
    public function getActiveTabData(): ?array
    {
        return $this->getTabs()[0] ?? null;
    }
}
```

### Blade View Template (Single-Tab)

```blade
<x-filament-panels::page>
    @php
        $activeTabData = $this->getActiveTabData();
    @endphp

    <div class="space-y-6">
        @if($activeTabData)
            @if(!empty($activeTabData['message']))
                @php $color = $activeTabData['messageColor'] ?? 'gray'; @endphp

                <div @class([
                    'rounded-lg p-4 border',
                    'bg-blue-50 dark:bg-blue-900/20 border-blue-200 dark:border-blue-800' => $color === 'blue',
                    'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800' => $color === 'green',
                    'bg-purple-50 dark:bg-purple-900/20 border-purple-200 dark:border-purple-800' => $color === 'purple',
                    'bg-orange-50 dark:bg-orange-900/20 border-orange-200 dark:border-orange-800' => $color === 'orange',
                    'bg-indigo-50 dark:bg-indigo-900/20 border-indigo-200 dark:border-indigo-800' => $color === 'indigo',
                    'bg-gray-50 dark:bg-gray-900/20 border-gray-200 dark:border-gray-800' => $color === 'gray',
                ])>
                    <p @class([
                        'text-sm',
                        'text-blue-700 dark:text-blue-300' => $color === 'blue',
                        'text-green-700 dark:text-green-300' => $color === 'green',
                        'text-purple-700 dark:text-purple-300' => $color === 'purple',
                        'text-orange-700 dark:text-orange-300' => $color === 'orange',
                        'text-indigo-700 dark:text-indigo-300' => $color === 'indigo',
                        'text-gray-700 dark:text-gray-300' => $color === 'gray',
                    ])>
                        {!! $activeTabData['message'] !!}
                    </p>
                </div>
            @endif

            @if(!empty($activeTabData['widgets']))
                <x-filament-widgets::widgets :widgets="$activeTabData['widgets']" />
            @endif
        @endif
    </div>
</x-filament-panels::page>
```

## Inputs Required for Generation

When creating a dashboard page, collect or assume defaults for:

| Input | Description | Example |
|-------|-------------|---------|
| Page class name | PascalCase class name | `BillingDashboard` |
| Panel | Panel name (Admin, Support, etc.) | `Admin` |
| View slug | Kebab-case slug for blade file | `billing-dashboard` |
| Navigation label | Display text in sidebar | `Billing` |
| Navigation group | Group in sidebar | `Analytics` |
| Navigation icon | Heroicon name | `heroicon-o-chart-bar` |
| Navigation sort | Numeric sort order | `10` |
| Mode | `single` or `multi` tab | `multi` |
| Tabs | Array of tab definitions | See schema above |
| Default tab key | First active tab | `overview` |

## Generation Workflow

### 1. Parse Requirements
- Identify page name and panel
- Determine single-tab vs multi-tab mode
- List tabs with their widgets

### 2. Generate PHP Class
- Use appropriate template (single or multi)
- Replace all placeholders
- Add widget class references

### 3. Generate Blade View
- Use appropriate template (single or multi)
- Match view path to class `$view` property

### 4. Verify Output
- [ ] `$view` matches the Blade path
- [ ] `activeTab` key exists in `getTabs()`
- [ ] Each tab has `key` and `title`
- [ ] Widgets are valid class strings
- [ ] Blade falls back if `activeTab` invalid
- [ ] Message uses `{!! !!}` only with trusted HTML

## Complete Example: Analytics Dashboard

### PHP Class

```php
<?php

declare(strict_types=1);

namespace App\Filament\Admin\Pages;

use BackedEnum;
use Filament\Pages\Page;

class Analytics extends Page
{
    protected static string $view = 'filament.admin.pages.analytics';

    protected static string|BackedEnum|null $navigationIcon = 'heroicon-o-chart-bar';
    protected static ?string $navigationLabel = 'Analytics';
    protected static \UnitEnum|string|null $navigationGroup = 'Reports';
    protected static ?int $navigationSort = 10;

    public string $activeTab = 'overview';

    /**
     * @return array<int, array{
     *   key: string,
     *   title: string,
     *   icon?: string,
     *   message?: string,
     *   messageColor?: string,
     *   widgets?: array<int, class-string>
     * }>
     */
    public function getTabs(): array
    {
        return [
            [
                'key' => 'overview',
                'icon' => 'heroicon-o-home',
                'title' => 'Overview',
                'message' => '<strong>Overview:</strong> Key metrics and performance indicators at a glance.',
                'messageColor' => 'blue',
                'widgets' => [
                    \App\Filament\Admin\Widgets\StatsOverview::class,
                    \App\Filament\Admin\Widgets\RevenueChart::class,
                ],
            ],
            [
                'key' => 'users',
                'icon' => 'heroicon-o-users',
                'title' => 'Users',
                'message' => '<strong>User Analytics:</strong> Track user growth, engagement, and retention metrics.',
                'messageColor' => 'green',
                'widgets' => [
                    \App\Filament\Admin\Widgets\UserGrowthChart::class,
                    \App\Filament\Admin\Widgets\ActiveUsersWidget::class,
                ],
            ],
            [
                'key' => 'revenue',
                'icon' => 'heroicon-o-currency-dollar',
                'title' => 'Revenue',
                'message' => '<strong>Revenue Analytics:</strong> Monitor income streams and financial performance.',
                'messageColor' => 'purple',
                'widgets' => [
                    \App\Filament\Admin\Widgets\RevenueBreakdown::class,
                    \App\Filament\Admin\Widgets\TopProducts::class,
                ],
            ],
        ];
    }

    public function getActiveTabData(): ?array
    {
        return collect($this->getTabs())->firstWhere('key', $this->activeTab);
    }
}
```

## Conventions

- Tab keys should use **snake_case** or **kebab-case** (be consistent)
- `$activeTab` must match a `key` from `getTabs()`
- `message` is rendered with `{!! !!}` — **only use trusted HTML**
- Widgets are referenced as `::class` strings
- Navigation icons use Heroicon names (e.g., `heroicon-o-chart-bar`)
- Available message colors: `blue`, `green`, `purple`, `orange`, `indigo`, `gray`

## Output

Generated dashboard pages include:
1. Complete PHP Page class
2. Complete Blade view file
3. Proper namespace and imports
4. Navigation configuration
5. Tab definitions with widgets
6. Color-coded message callouts
7. Fallback handling for invalid tabs
