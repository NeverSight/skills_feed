---
name: filament-widgets
description: Create FilamentPHP v4 dashboard widgets - stats overviews, charts, and custom components
---

# FilamentPHP Widgets Generation Skill

## Overview

This skill generates FilamentPHP v4 dashboard widgets including stats overview widgets, chart widgets, table widgets, and custom widgets.

## Documentation Reference

**CRITICAL:** Before generating widgets, read:
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/widgets/`

## Creating Widgets

### Generate with Artisan

```bash
# Basic widget
php artisan make:filament-widget StatsOverview

# Stats overview widget
php artisan make:filament-widget StatsOverview --stats-overview

# Chart widget
php artisan make:filament-widget RevenueChart --chart

# Table widget
php artisan make:filament-widget LatestOrders --table

# Resource widget
php artisan make:filament-widget PostStats --resource=PostResource
```

## Stats Overview Widget

```php
<?php

declare(strict_types=1);

namespace App\Filament\Widgets;

use App\Models\Order;
use App\Models\User;
use Filament\Widgets\StatsOverviewWidget as BaseWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class StatsOverview extends BaseWidget
{
    protected static ?int $sort = 1;

    protected function getStats(): array
    {
        return [
            // Basic stat
            Stat::make('Total Users', User::count())
                ->description('All registered users')
                ->descriptionIcon('heroicon-o-users')
                ->color('primary'),

            // Stat with trend
            Stat::make('New Users', User::whereMonth('created_at', now()->month)->count())
                ->description('32% increase')
                ->descriptionIcon('heroicon-m-arrow-trending-up')
                ->color('success')
                ->chart([7, 3, 4, 5, 6, 3, 5, 8])  // Sparkline data
                ->chartColor('success'),

            // Stat with decrease trend
            Stat::make('Bounce Rate', '21%')
                ->description('7% decrease')
                ->descriptionIcon('heroicon-m-arrow-trending-down')
                ->color('danger'),

            // Revenue stat with formatting
            Stat::make('Revenue', '$' . number_format(Order::sum('total'), 2))
                ->description('This month')
                ->descriptionIcon('heroicon-o-currency-dollar')
                ->color('success')
                ->chart([1200, 1400, 1100, 1800, 2200, 1900, 2400])
                ->chartColor('success'),

            // Stat with extra info
            Stat::make('Pending Orders', Order::where('status', 'pending')->count())
                ->description('Requires attention')
                ->descriptionIcon('heroicon-o-clock')
                ->color('warning')
                ->extraAttributes([
                    'class' => 'cursor-pointer',
                    'wire:click' => 'goToOrders',
                ]),
        ];
    }

    // Optional: Make stats live
    protected static ?string $pollingInterval = '15s';

    // Optional: Column span
    protected int | string | array $columnSpan = 'full';
}
```

## Chart Widgets

### Line Chart

```php
<?php

declare(strict_types=1);

namespace App\Filament\Widgets;

use App\Models\Order;
use Filament\Widgets\ChartWidget;
use Illuminate\Support\Carbon;

class RevenueChart extends ChartWidget
{
    protected static ?string $heading = 'Revenue';
    protected static ?int $sort = 2;
    protected int | string | array $columnSpan = 'full';

    protected function getData(): array
    {
        $data = collect(range(1, 12))->map(function ($month) {
            return Order::whereMonth('created_at', $month)
                ->whereYear('created_at', now()->year)
                ->sum('total');
        });

        return [
            'datasets' => [
                [
                    'label' => 'Revenue',
                    'data' => $data->values()->toArray(),
                    'borderColor' => '#10b981',
                    'backgroundColor' => 'rgba(16, 185, 129, 0.1)',
                    'fill' => true,
                ],
            ],
            'labels' => ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        ];
    }

    protected function getType(): string
    {
        return 'line';
    }

    protected function getOptions(): array
    {
        return [
            'plugins' => [
                'legend' => [
                    'display' => false,
                ],
            ],
            'scales' => [
                'y' => [
                    'beginAtZero' => true,
                    'ticks' => [
                        'callback' => '(value) => "$" + value.toLocaleString()',
                    ],
                ],
            ],
        ];
    }
}
```

### Bar Chart

```php
<?php

declare(strict_types=1);

namespace App\Filament\Widgets;

use App\Models\Order;
use Filament\Widgets\ChartWidget;

class OrdersPerCategory extends ChartWidget
{
    protected static ?string $heading = 'Orders by Category';
    protected static ?int $sort = 3;

    protected function getData(): array
    {
        $categories = \App\Models\Category::withCount('orders')->get();

        return [
            'datasets' => [
                [
                    'label' => 'Orders',
                    'data' => $categories->pluck('orders_count')->toArray(),
                    'backgroundColor' => [
                        '#3b82f6',
                        '#10b981',
                        '#f59e0b',
                        '#ef4444',
                        '#8b5cf6',
                    ],
                ],
            ],
            'labels' => $categories->pluck('name')->toArray(),
        ];
    }

    protected function getType(): string
    {
        return 'bar';
    }
}
```

### Doughnut/Pie Chart

```php
<?php

declare(strict_types=1);

namespace App\Filament\Widgets;

use App\Models\Order;
use Filament\Widgets\ChartWidget;

class OrderStatusChart extends ChartWidget
{
    protected static ?string $heading = 'Order Status Distribution';
    protected static ?int $sort = 4;

    protected function getData(): array
    {
        $statuses = Order::selectRaw('status, COUNT(*) as count')
            ->groupBy('status')
            ->pluck('count', 'status');

        return [
            'datasets' => [
                [
                    'data' => $statuses->values()->toArray(),
                    'backgroundColor' => [
                        '#f59e0b',  // pending - warning
                        '#3b82f6',  // processing - primary
                        '#10b981',  // completed - success
                        '#ef4444',  // cancelled - danger
                    ],
                ],
            ],
            'labels' => $statuses->keys()->map(fn ($s) => ucfirst($s))->toArray(),
        ];
    }

    protected function getType(): string
    {
        return 'doughnut';  // or 'pie'
    }

    protected function getOptions(): array
    {
        return [
            'plugins' => [
                'legend' => [
                    'position' => 'bottom',
                ],
            ],
        ];
    }
}
```

### Interactive Chart with Filters

```php
<?php

declare(strict_types=1);

namespace App\Filament\Widgets;

use App\Models\Order;
use Filament\Forms\Components\DatePicker;
use Filament\Forms\Components\Select;
use Filament\Widgets\ChartWidget;

class FilterableRevenueChart extends ChartWidget
{
    protected static ?string $heading = 'Revenue Over Time';

    public ?string $filter = 'week';

    protected function getFilters(): ?array
    {
        return [
            'today' => 'Today',
            'week' => 'Last 7 days',
            'month' => 'This month',
            'year' => 'This year',
        ];
    }

    protected function getData(): array
    {
        $data = match ($this->filter) {
            'today' => $this->getTodayData(),
            'week' => $this->getWeekData(),
            'month' => $this->getMonthData(),
            'year' => $this->getYearData(),
        };

        return [
            'datasets' => [
                [
                    'label' => 'Revenue',
                    'data' => $data['values'],
                    'borderColor' => '#3b82f6',
                ],
            ],
            'labels' => $data['labels'],
        ];
    }

    protected function getType(): string
    {
        return 'line';
    }

    private function getTodayData(): array
    {
        // Implementation
    }

    private function getWeekData(): array
    {
        // Implementation
    }

    private function getMonthData(): array
    {
        // Implementation
    }

    private function getYearData(): array
    {
        // Implementation
    }
}
```

## Table Widget

```php
<?php

declare(strict_types=1);

namespace App\Filament\Widgets;

use App\Models\Order;
use Filament\Tables;
use Filament\Tables\Table;
use Filament\Widgets\TableWidget as BaseWidget;

class LatestOrders extends BaseWidget
{
    protected static ?string $heading = 'Latest Orders';
    protected static ?int $sort = 5;
    protected int | string | array $columnSpan = 'full';

    public function table(Table $table): Table
    {
        return $table
            ->query(
                Order::query()
                    ->latest()
                    ->limit(10)
            )
            ->columns([
                Tables\Columns\TextColumn::make('number')
                    ->searchable(),
                Tables\Columns\TextColumn::make('customer.name')
                    ->label('Customer')
                    ->searchable(),
                Tables\Columns\BadgeColumn::make('status')
                    ->colors([
                        'warning' => 'pending',
                        'primary' => 'processing',
                        'success' => 'completed',
                        'danger' => 'cancelled',
                    ]),
                Tables\Columns\TextColumn::make('total')
                    ->money('usd')
                    ->sortable(),
                Tables\Columns\TextColumn::make('created_at')
                    ->dateTime()
                    ->sortable(),
            ])
            ->actions([
                Tables\Actions\Action::make('view')
                    ->url(fn (Order $record): string => route('filament.admin.resources.orders.view', $record))
                    ->icon('heroicon-o-eye'),
            ])
            ->paginated(false);
    }
}
```

## Custom Widget

```php
<?php

declare(strict_types=1);

namespace App\Filament\Widgets;

use App\Models\Task;
use Filament\Widgets\Widget;

class TasksWidget extends Widget
{
    protected static string $view = 'filament.widgets.tasks-widget';
    protected static ?int $sort = 6;
    protected int | string | array $columnSpan = 1;

    public array $tasks = [];

    public function mount(): void
    {
        $this->tasks = Task::where('user_id', auth()->id())
            ->whereNull('completed_at')
            ->orderBy('due_date')
            ->limit(5)
            ->get()
            ->toArray();
    }

    public function completeTask(int $taskId): void
    {
        Task::find($taskId)->update(['completed_at' => now()]);
        $this->mount(); // Refresh tasks
    }
}
```

Blade view (`resources/views/filament/widgets/tasks-widget.blade.php`):

```blade
<x-filament-widgets::widget>
    <x-filament::section>
        <x-slot name="heading">
            My Tasks
        </x-slot>

        <ul class="divide-y divide-gray-200 dark:divide-gray-700">
            @forelse ($tasks as $task)
                <li class="py-3 flex items-center justify-between">
                    <div>
                        <p class="text-sm font-medium text-gray-900 dark:text-white">
                            {{ $task['title'] }}
                        </p>
                        <p class="text-xs text-gray-500">
                            Due: {{ \Carbon\Carbon::parse($task['due_date'])->format('M j, Y') }}
                        </p>
                    </div>
                    <x-filament::icon-button
                        icon="heroicon-o-check"
                        wire:click="completeTask({{ $task['id'] }})"
                        color="success"
                    />
                </li>
            @empty
                <li class="py-3 text-sm text-gray-500">
                    No pending tasks
                </li>
            @endforelse
        </ul>
    </x-filament::section>
</x-filament-widgets::widget>
```

## Widget Registration

### Dashboard Widgets

```php
// In AdminPanelProvider.php
->widgets([
    Widgets\AccountWidget::class,  // Default
    Widgets\FilamentInfoWidget::class,  // Default
    \App\Filament\Widgets\StatsOverview::class,
    \App\Filament\Widgets\RevenueChart::class,
    \App\Filament\Widgets\LatestOrders::class,
])
```

### Resource Page Widgets

```php
// In resource class
public static function getWidgets(): array
{
    return [
        Widgets\PostStatsOverview::class,
    ];
}

// In ListRecords page
protected function getHeaderWidgets(): array
{
    return [
        Widgets\PostStatsOverview::class,
    ];
}

protected function getFooterWidgets(): array
{
    return [
        Widgets\RecentPosts::class,
    ];
}
```

## Widget Configuration

```php
class MyWidget extends Widget
{
    // Sort order
    protected static ?int $sort = 1;

    // Column span (1, 2, 'full', or responsive array)
    protected int | string | array $columnSpan = [
        'md' => 2,
        'xl' => 3,
    ];

    // Polling interval
    protected static ?string $pollingInterval = '10s';

    // Visibility
    public static function canView(): bool
    {
        return auth()->user()->isAdmin();
    }

    // Lazy loading
    protected static bool $isLazy = true;
}
```

## Output

Generated widgets include:
1. Proper widget type selection
2. Data fetching methods
3. Chart configuration
4. Styling and layout
5. Interactivity (filters, actions)
6. Performance optimizations
