---
name: filament-infolists
description: Create FilamentPHP v4 infolists with entries, sections, and layouts for view pages
---

# FilamentPHP Infolists Generation Skill

## Overview

This skill generates FilamentPHP v4 infolists for displaying read-only data in view pages and modals.

## Documentation Reference

**CRITICAL:** Before generating infolists, read:
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/infolists/`

## Basic Infolist Structure

```php
use Filament\Infolists;
use Filament\Infolists\Infolist;

public static function infolist(Infolist $infolist): Infolist
{
    return $infolist
        ->schema([
            // Entries here
        ]);
}
```

## Entry Types

### Text Entry

```php
// Basic text
Infolists\Components\TextEntry::make('name')
    ->label('Name');

// With formatting
Infolists\Components\TextEntry::make('price')
    ->money('usd');

// Date formatting
Infolists\Components\TextEntry::make('created_at')
    ->dateTime('F j, Y H:i');

// Relative date
Infolists\Components\TextEntry::make('updated_at')
    ->since();

// With limit
Infolists\Components\TextEntry::make('description')
    ->limit(100)
    ->tooltip(fn ($record) => $record->description);

// HTML content
Infolists\Components\TextEntry::make('content')
    ->html()
    ->prose();

// Markdown content
Infolists\Components\TextEntry::make('readme')
    ->markdown();

// Copyable
Infolists\Components\TextEntry::make('uuid')
    ->copyable()
    ->copyMessage('Copied!')
    ->copyMessageDuration(1500);

// With color
Infolists\Components\TextEntry::make('status')
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'gray',
        'published' => 'success',
        default => 'primary',
    });

// With icon
Infolists\Components\TextEntry::make('email')
    ->icon('heroicon-o-envelope')
    ->iconColor('primary');

// With badge
Infolists\Components\TextEntry::make('status')
    ->badge()
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'warning',
        'published' => 'success',
        default => 'gray',
    });

// List of values
Infolists\Components\TextEntry::make('tags.name')
    ->listWithLineBreaks()
    ->bulleted();

// With URL
Infolists\Components\TextEntry::make('website')
    ->url(fn ($record) => $record->website)
    ->openUrlInNewTab();
```

### Icon Entry

```php
// Boolean icon
Infolists\Components\IconEntry::make('is_active')
    ->boolean();

// Custom icons
Infolists\Components\IconEntry::make('status')
    ->icon(fn (string $state): string => match ($state) {
        'draft' => 'heroicon-o-pencil',
        'reviewing' => 'heroicon-o-clock',
        'published' => 'heroicon-o-check-circle',
    })
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'info',
        'reviewing' => 'warning',
        'published' => 'success',
        default => 'gray',
    });
```

### Image Entry

```php
// Basic image
Infolists\Components\ImageEntry::make('avatar')
    ->circular()
    ->size(80);

// Multiple images
Infolists\Components\ImageEntry::make('images')
    ->stacked()
    ->limit(3)
    ->limitedRemainingText();

// Square image
Infolists\Components\ImageEntry::make('logo')
    ->square()
    ->size(100);

// With default
Infolists\Components\ImageEntry::make('photo')
    ->defaultImageUrl(url('/images/placeholder.png'));
```

### Color Entry

```php
Infolists\Components\ColorEntry::make('color')
    ->copyable();
```

### Key-Value Entry

```php
Infolists\Components\KeyValueEntry::make('metadata');
```

### Repeatable Entry (For HasMany)

```php
Infolists\Components\RepeatableEntry::make('comments')
    ->schema([
        Infolists\Components\TextEntry::make('author.name')
            ->label('Author'),
        Infolists\Components\TextEntry::make('content')
            ->columnSpanFull(),
        Infolists\Components\TextEntry::make('created_at')
            ->dateTime(),
    ])
    ->columns(2);
```

### View Entry (Custom)

```php
Infolists\Components\ViewEntry::make('custom')
    ->view('filament.infolists.entries.custom-entry');
```

## Layout Components

### Section

```php
Infolists\Components\Section::make('Personal Information')
    ->description('Basic user details')
    ->icon('heroicon-o-user')
    ->collapsible()
    ->schema([
        Infolists\Components\TextEntry::make('name'),
        Infolists\Components\TextEntry::make('email'),
        Infolists\Components\TextEntry::make('phone'),
    ])
    ->columns(3);
```

### Fieldset

```php
Infolists\Components\Fieldset::make('Address')
    ->schema([
        Infolists\Components\TextEntry::make('street'),
        Infolists\Components\TextEntry::make('city'),
        Infolists\Components\TextEntry::make('state'),
        Infolists\Components\TextEntry::make('zip'),
    ])
    ->columns(2);
```

### Tabs

```php
Infolists\Components\Tabs::make('Tabs')
    ->tabs([
        Infolists\Components\Tabs\Tab::make('Overview')
            ->icon('heroicon-o-information-circle')
            ->schema([
                Infolists\Components\TextEntry::make('name'),
                Infolists\Components\TextEntry::make('email'),
            ]),
        Infolists\Components\Tabs\Tab::make('Details')
            ->icon('heroicon-o-document-text')
            ->schema([
                Infolists\Components\TextEntry::make('bio')
                    ->columnSpanFull(),
            ]),
        Infolists\Components\Tabs\Tab::make('Settings')
            ->icon('heroicon-o-cog')
            ->badge(3)
            ->schema([
                Infolists\Components\IconEntry::make('is_active')
                    ->boolean(),
            ]),
    ])
    ->columnSpanFull();
```

### Grid

```php
Infolists\Components\Grid::make()
    ->schema([
        Infolists\Components\TextEntry::make('name')
            ->columnSpan(1),
        Infolists\Components\TextEntry::make('email')
            ->columnSpan(1),
        Infolists\Components\TextEntry::make('bio')
            ->columnSpanFull(),
    ])
    ->columns(2);
```

### Split

```php
Infolists\Components\Split::make([
    Infolists\Components\Section::make('Main Content')
        ->schema([
            Infolists\Components\TextEntry::make('title'),
            Infolists\Components\TextEntry::make('content')
                ->html()
                ->prose(),
        ]),
    Infolists\Components\Section::make('Metadata')
        ->schema([
            Infolists\Components\TextEntry::make('created_at')
                ->dateTime(),
            Infolists\Components\TextEntry::make('author.name'),
        ])
        ->grow(false),
]);
```

### Group

```php
Infolists\Components\Group::make([
    Infolists\Components\TextEntry::make('first_name'),
    Infolists\Components\TextEntry::make('last_name'),
])
->columns(2);
```

## Complete Infolist Example

```php
<?php

declare(strict_types=1);

namespace App\Filament\Resources\PostResource\Pages;

use App\Filament\Resources\PostResource;
use Filament\Infolists;
use Filament\Infolists\Infolist;
use Filament\Resources\Pages\ViewRecord;

class ViewPost extends ViewRecord
{
    protected static string $resource = PostResource::class;

    public function infolist(Infolist $infolist): Infolist
    {
        return $infolist
            ->schema([
                Infolists\Components\Split::make([
                    // Main content
                    Infolists\Components\Group::make([
                        Infolists\Components\Section::make('Post Details')
                            ->schema([
                                Infolists\Components\TextEntry::make('title')
                                    ->size(Infolists\Components\TextEntry\TextEntrySize::Large)
                                    ->weight(\Filament\Support\Enums\FontWeight::Bold),
                                Infolists\Components\TextEntry::make('slug')
                                    ->icon('heroicon-o-link')
                                    ->copyable(),
                                Infolists\Components\TextEntry::make('excerpt')
                                    ->columnSpanFull(),
                            ])
                            ->columns(2),

                        Infolists\Components\Section::make('Content')
                            ->schema([
                                Infolists\Components\TextEntry::make('content')
                                    ->html()
                                    ->prose()
                                    ->columnSpanFull(),
                            ]),

                        Infolists\Components\Section::make('Comments')
                            ->schema([
                                Infolists\Components\RepeatableEntry::make('comments')
                                    ->schema([
                                        Infolists\Components\TextEntry::make('author.name')
                                            ->label('Author')
                                            ->weight(\Filament\Support\Enums\FontWeight::Bold),
                                        Infolists\Components\TextEntry::make('created_at')
                                            ->since()
                                            ->color('gray'),
                                        Infolists\Components\TextEntry::make('content')
                                            ->columnSpanFull(),
                                    ])
                                    ->columns(2),
                            ])
                            ->collapsible(),
                    ]),

                    // Sidebar
                    Infolists\Components\Group::make([
                        Infolists\Components\Section::make('Meta')
                            ->schema([
                                Infolists\Components\TextEntry::make('status')
                                    ->badge()
                                    ->color(fn (string $state): string => match ($state) {
                                        'draft' => 'warning',
                                        'published' => 'success',
                                        default => 'gray',
                                    }),
                                Infolists\Components\TextEntry::make('author.name')
                                    ->icon('heroicon-o-user'),
                                Infolists\Components\TextEntry::make('category.name')
                                    ->icon('heroicon-o-folder'),
                                Infolists\Components\TextEntry::make('tags.name')
                                    ->badge()
                                    ->separator(','),
                            ]),

                        Infolists\Components\Section::make('Image')
                            ->schema([
                                Infolists\Components\ImageEntry::make('featured_image')
                                    ->hiddenLabel()
                                    ->grow(false),
                            ]),

                        Infolists\Components\Section::make('Dates')
                            ->schema([
                                Infolists\Components\TextEntry::make('published_at')
                                    ->dateTime()
                                    ->icon('heroicon-o-calendar'),
                                Infolists\Components\TextEntry::make('created_at')
                                    ->dateTime()
                                    ->icon('heroicon-o-clock'),
                                Infolists\Components\TextEntry::make('updated_at')
                                    ->since()
                                    ->icon('heroicon-o-arrow-path'),
                            ]),
                    ])
                    ->grow(false),
                ])
                ->from('md')
                ->columnSpanFull(),
            ]);
    }

    protected function getHeaderActions(): array
    {
        return [
            \Filament\Actions\EditAction::make(),
            \Filament\Actions\DeleteAction::make(),
        ];
    }
}
```

## Entry Modifiers

```php
Infolists\Components\TextEntry::make('name')
    // Label
    ->label('Full Name')
    ->hiddenLabel()

    // Visibility
    ->visible(fn ($record) => $record->is_public)
    ->hidden(fn ($record) => $record->is_private)

    // Placeholder for empty
    ->placeholder('Not specified')
    ->default('N/A')

    // Column span
    ->columnSpan(2)
    ->columnSpanFull()

    // Weight and size
    ->weight(\Filament\Support\Enums\FontWeight::Bold)
    ->size(Infolists\Components\TextEntry\TextEntrySize::Large)

    // Extra attributes
    ->extraAttributes(['class' => 'my-custom-class']);
```

## Output

Generated infolists include:
1. Proper entry type selection
2. Layout structure
3. Relationship handling
4. Formatting and styling
5. Conditional visibility
6. Section organization
