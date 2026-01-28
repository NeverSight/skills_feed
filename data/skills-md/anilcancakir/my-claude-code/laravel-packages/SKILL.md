---
name: laravel-packages
description: "Laravel Filament v4 admin panel, Debugbar development, SEOTools, third-party packages. ALWAYS activate when: working with admin panel, Filament resources, forms, tables, SEO meta tags, debugging. Triggers on: Filament form field, admin CRUD, resource table, action button, widget, Debugbar query log, N+1 detected, SEO title, meta description, OpenGraph, sitemap, admin paneli, debugbar göstermiyor, SEO ayarları, meta tag, Filament çalışmıyor, admin sayfası, resource oluşturma."
---

# Laravel Packages

Filament v4, Debugbar, and SEOTools patterns for Laravel 12+.

## Filament v4 Admin Panel

> **v4 Changes from v3:**
>
> - `Form` renamed to `Schema` in method signatures
> - TailwindCSS v4 required for custom themes
> - TipTap editor replaces Trix (RichEditor)
> - New fields: Slider, CodeEditor, TableRepeater
> - Performance: 2-3x faster table rendering
> - Automatic tenant scoping for multi-tenancy

### Installation

```bash
composer require filament/filament:"^4.0"
php artisan filament:install --panels
```

### Creating Resources

```bash
php artisan make:filament-resource Order --generate
```

### Resource Example (v4 Syntax)

```php
<?php

namespace App\Filament\Resources;

use App\Filament\Resources\OrderResource\Pages;
use App\Models\Order;
use Filament\Forms;
use Filament\Schemas\Schema;  // v4: Schema instead of Form
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;

class OrderResource extends Resource
{
    protected static ?string $model = Order::class;

    protected static ?string $navigationIcon = 'heroicon-o-shopping-cart';

    protected static ?string $navigationGroup = 'Shop';

    /**
     * v4: Method signature uses Schema instead of Form
     */
    public static function form(Schema $schema): Schema
    {
        return $schema
            ->components([
                Forms\Components\Section::make('Order Details')
                    ->schema([
                        Forms\Components\Select::make('user_id')
                            ->relationship('user', 'name')
                            ->searchable()
                            ->required(),

                        Forms\Components\Select::make('status')
                            ->options([
                                'pending' => 'Pending',
                                'processing' => 'Processing',
                                'completed' => 'Completed',
                                'cancelled' => 'Cancelled',
                            ])
                            ->required(),

                        Forms\Components\TextInput::make('total')
                            ->numeric()
                            ->prefix('£')
                            ->required(),
                    ])
                    ->columns(3),

                Forms\Components\Repeater::make('items')
                    ->relationship()
                    ->schema([
                        Forms\Components\Select::make('product_id')
                            ->relationship('product', 'name')
                            ->required(),
                        Forms\Components\TextInput::make('quantity')
                            ->numeric()
                            ->required(),
                    ])
                    ->columns(2),
            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('id')
                    ->sortable(),

                Tables\Columns\TextColumn::make('user.name')
                    ->searchable(),

                Tables\Columns\TextColumn::make('status')
                    ->badge()
                    ->color(fn (string $state): string => match ($state) {
                        'pending' => 'warning',
                        'processing' => 'primary',
                        'completed' => 'success',
                        'cancelled' => 'danger',
                        default => 'gray',
                    }),

                Tables\Columns\TextColumn::make('total')
                    ->money('GBP')
                    ->sortable(),

                Tables\Columns\TextColumn::make('created_at')
                    ->dateTime()
                    ->sortable(),
            ])
            ->filters([
                Tables\Filters\SelectFilter::make('status')
                    ->options([
                        'pending' => 'Pending',
                        'completed' => 'Completed',
                    ]),
            ])
            ->actions([
                Tables\Actions\ViewAction::make(),
                Tables\Actions\EditAction::make(),
            ])
            ->bulkActions([
                Tables\Actions\BulkActionGroup::make([
                    Tables\Actions\DeleteBulkAction::make(),
                ]),
            ]);
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ListOrders::route('/'),
            'create' => Pages\CreateOrder::route('/create'),
            'edit' => Pages\EditOrder::route('/{record}/edit'),
        ];
    }
}
```

### New v4 Form Fields

```php
use Filament\Forms\Components;

// Slider (NEW in v4)
Components\Slider::make('rating')
    ->min(1)
    ->max(5)
    ->step(1);

// Code Editor (NEW in v4)
Components\CodeEditor::make('code')
    ->language('php');

// Table Repeater (NEW in v4)
Components\TableRepeater::make('items')
    ->schema([
        Components\TextInput::make('name'),
        Components\TextInput::make('quantity')->numeric(),
    ]);

// RichEditor (v4 uses TipTap instead of Trix)
Components\RichEditor::make('content')
    ->toolbarButtons(['bold', 'italic', 'link', 'bulletList'])
    ->fileAttachmentsDisk('public');

// Image with aspect ratio (v4)
Components\FileUpload::make('avatar')
    ->image()
    ->imageEditor()
    ->imageEditorAspectRatios(['1:1', '4:3', '16:9']);
```

### v4 JavaScript Optimizations

```php
// Reduce network requests with JS methods
Forms\Components\TextInput::make('name')
    ->live()
    ->afterStateUpdatedJs('
        $set("slug", $state.toLowerCase().replace(/ /g, "-"));
    ');

// Hide/show without server round-trip
Forms\Components\Toggle::make('has_discount')
    ->live();

Forms\Components\TextInput::make('discount')
    ->hiddenJs('!$get("has_discount")');
```

### Widgets

```php
<?php

namespace App\Filament\Widgets;

use App\Models\Order;
use Filament\Widgets\StatsOverviewWidget as BaseWidget;
use Filament\Widgets\StatsOverviewWidget\Stat;

class OrderStats extends BaseWidget
{
    protected function getStats(): array
    {
        return [
            Stat::make('Total Orders', Order::count())
                ->description('All time')
                ->descriptionIcon('heroicon-m-arrow-trending-up')
                ->color('success'),

            Stat::make('Pending Orders', Order::where('status', 'pending')->count())
                ->description('Requires attention')
                ->color('warning'),

            Stat::make('Revenue', '£' . number_format(Order::sum('total'), 2))
                ->description('This month')
                ->color('primary'),
        ];
    }
}
```

---

## Laravel Debugbar

### Installation

```bash
composer require barryvdh/laravel-debugbar --dev
```

### Configuration

```php
// config/debugbar.php
'enabled' => env('DEBUGBAR_ENABLED', null),  // Auto-detect based on APP_DEBUG
'collectors' => [
    'queries' => true,
    'models' => true,
    'views' => true,
    'route' => true,
    'memory' => true,
    'time' => true,
],
```

### Usage in Code

```php
use Barryvdh\Debugbar\Facades\Debugbar;

// Manual messages
Debugbar::info('Info message');
Debugbar::warning('Warning');
Debugbar::error('Error');

// Measure time
Debugbar::startMeasure('render', 'Time for rendering');
// ... code ...
Debugbar::stopMeasure('render');

// Add custom data
Debugbar::addMessage(['user' => $user->toArray()], 'custom');
```

### N+1 Query Detection

Debugbar automatically shows query counts. Look for:

- Duplicate queries (same query repeated)
- High query counts on single page load
- Missing eager loading

---

## SEOTools (artesaos/seotools)

### Installation

```bash
composer require artesaos/seotools
php artisan vendor:publish --provider="Artesaos\SEOTools\Providers\SEOToolsServiceProvider"
```

### Basic Usage

```php
<?php

namespace App\Http\Controllers;

use Artesaos\SEOTools\Facades\SEOMeta;
use Artesaos\SEOTools\Facades\OpenGraph;
use Artesaos\SEOTools\Facades\TwitterCard;
use Artesaos\SEOTools\Facades\SEOTools;

class ProductController extends Controller
{
    public function show(Product $product)
    {
        // All-in-one
        SEOTools::setTitle($product->name);
        SEOTools::setDescription($product->description);
        SEOTools::opengraph()->setUrl(url()->current());
        SEOTools::opengraph()->addProperty('type', 'product');
        SEOTools::twitter()->setSite('@mysite');
        SEOTools::jsonLd()->addImage($product->image_url);

        return view('products.show', compact('product'));
    }
}
```

### In Blade Layout

```blade
<head>
    {!! SEO::generate() !!}
</head>
```

### Configuration

```php
// config/seotools.php
'meta' => [
    'defaults' => [
        'title' => 'My Site',
        'titleSeparator' => ' | ',
        'description' => 'Default description',
        'robots' => 'index,follow',
    ],
],
'opengraph' => [
    'defaults' => [
        'title' => 'My Site',
        'type' => 'website',
        'site_name' => 'My Site',
    ],
],
```

### Structured Data (JSON-LD)

```php
use Artesaos\SEOTools\Facades\JsonLd;

JsonLd::setType('Product');
JsonLd::setTitle($product->name);
JsonLd::setDescription($product->description);
JsonLd::addValue('sku', $product->sku);
JsonLd::addValue('offers', [
    '@type' => 'Offer',
    'price' => $product->price,
    'priceCurrency' => 'GBP',
]);
```

## References

| Topic | Reference | When to Load |
|-------|-----------|--------------|
| Filament forms | [references/filament.md](references/filament.md) | Advanced forms, actions |
| SEOTools patterns | [references/seotools.md](references/seotools.md) | Sitemap, canonical, i18n |

## Quick Commands

```bash
# Filament
php artisan make:filament-resource User --generate
php artisan make:filament-widget StatsOverview
php artisan make:filament-page Settings

# Clear caches after changes
php artisan filament:cache-components
php artisan filament:clear-cached-components
```
