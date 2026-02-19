---
name: filament-tables
description: Create FilamentPHP v4 tables with columns, filters, sorting, search, and bulk actions
---

# FilamentPHP Tables Generation Skill

## Overview

This skill generates FilamentPHP v4 table configurations with columns, filters, actions, and bulk operations following official documentation patterns.

## Documentation Reference

**CRITICAL:** Before generating tables, read:
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/tables/`
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/tables/02-columns/`
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/tables/03-filters/`

## Workflow

### Step 1: Analyze Requirements

Identify:
- Columns to display
- Searchable fields
- Sortable fields
- Filter requirements
- Row actions
- Bulk actions
- Relationships to display

### Step 2: Read Documentation

Navigate to table documentation and extract:
- Column class names and options
- Filter configurations
- Action patterns
- Performance considerations

### Step 3: Generate Table

Build table configuration:

```php
use Filament\Tables;
use Filament\Tables\Table;

public static function table(Table $table): Table
{
    return $table
        ->columns([
            // Columns
        ])
        ->filters([
            // Filters
        ])
        ->actions([
            // Row actions
        ])
        ->bulkActions([
            // Bulk actions
        ]);
}
```

## Column Types Reference

### Text Column

```php
// Basic text
Tables\Columns\TextColumn::make('name')
    ->searchable()
    ->sortable();

// With limit and tooltip
Tables\Columns\TextColumn::make('description')
    ->limit(50)
    ->tooltip(fn ($record): string => $record->description);

// Formatted
Tables\Columns\TextColumn::make('price')
    ->money('usd')
    ->sortable();

// Date formatting
Tables\Columns\TextColumn::make('created_at')
    ->dateTime('M j, Y H:i')
    ->sortable()
    ->since();  // Shows "2 hours ago"

// Copyable
Tables\Columns\TextColumn::make('uuid')
    ->copyable()
    ->copyMessage('UUID copied!')
    ->copyMessageDuration(1500);

// With color
Tables\Columns\TextColumn::make('status')
    ->color(fn (string $state): string => match ($state) {
        'draft' => 'gray',
        'reviewing' => 'warning',
        'published' => 'success',
        default => 'gray',
    });

// HTML content
Tables\Columns\TextColumn::make('content')
    ->html()
    ->wrap();

// Word/character count
Tables\Columns\TextColumn::make('bio')
    ->words(10);

// List values (array)
Tables\Columns\TextColumn::make('tags')
    ->listWithLineBreaks()
    ->bulleted();
```

### Icon Column

```php
// Boolean icon
Tables\Columns\IconColumn::make('is_active')
    ->boolean();

// Custom icons
Tables\Columns\IconColumn::make('status')
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

### Image Column

```php
// Basic image
Tables\Columns\ImageColumn::make('avatar')
    ->circular()
    ->size(40);

// Multiple images (stacked)
Tables\Columns\ImageColumn::make('images')
    ->circular()
    ->stacked()
    ->limit(3)
    ->limitedRemainingText();

// With default
Tables\Columns\ImageColumn::make('logo')
    ->defaultImageUrl(url('/images/default-logo.png'))
    ->square()
    ->size(60);
```

### Badge Column

```php
Tables\Columns\BadgeColumn::make('status')
    ->colors([
        'danger' => 'draft',
        'warning' => 'reviewing',
        'success' => 'published',
    ])
    ->icons([
        'heroicon-o-pencil' => 'draft',
        'heroicon-o-clock' => 'reviewing',
        'heroicon-o-check' => 'published',
    ]);

// Or with closure
Tables\Columns\BadgeColumn::make('priority')
    ->color(fn (string $state): string => match ($state) {
        'low' => 'gray',
        'medium' => 'warning',
        'high' => 'danger',
    });
```

### Color Column

```php
Tables\Columns\ColorColumn::make('color')
    ->copyable()
    ->copyMessage('Color code copied');
```

### Toggle Column

```php
// Editable inline toggle
Tables\Columns\ToggleColumn::make('is_active')
    ->onColor('success')
    ->offColor('danger')
    ->afterStateUpdated(fn () => Notification::make()
        ->title('Status updated')
        ->success()
        ->send()
    );
```

### Select Column

```php
// Editable inline select
Tables\Columns\SelectColumn::make('status')
    ->options([
        'draft' => 'Draft',
        'published' => 'Published',
    ]);
```

### Text Input Column

```php
// Editable inline text
Tables\Columns\TextInputColumn::make('sort_order')
    ->rules(['required', 'numeric']);
```

### Checkbox Column

```php
// Editable inline checkbox
Tables\Columns\CheckboxColumn::make('is_featured');
```

### Relationship Columns

```php
// BelongsTo
Tables\Columns\TextColumn::make('author.name')
    ->label('Author')
    ->searchable()
    ->sortable();

// HasMany count
Tables\Columns\TextColumn::make('comments_count')
    ->counts('comments')
    ->label('Comments')
    ->sortable();

// HasMany sum
Tables\Columns\TextColumn::make('items_sum_quantity')
    ->sum('items', 'quantity')
    ->label('Total Quantity');

// BelongsToMany list
Tables\Columns\TextColumn::make('tags.name')
    ->badge()
    ->separator(',');
```

### View Column (Custom)

```php
Tables\Columns\ViewColumn::make('custom')
    ->view('filament.tables.columns.custom-column');
```

## Column Modifiers

```php
Tables\Columns\TextColumn::make('name')
    // Search
    ->searchable()
    ->searchable(isIndividual: true)

    // Sort
    ->sortable()
    ->sortable(['first_name', 'last_name'])

    // Visibility
    ->toggleable()
    ->toggleable(isToggledHiddenByDefault: true)
    ->visible(fn (): bool => auth()->user()->isAdmin())
    ->hidden(fn ($record): bool => $record->is_private)

    // Sizing
    ->grow(false)
    ->width('200px')
    ->alignCenter()
    ->alignEnd()

    // Styling
    ->weight(FontWeight::Bold)
    ->size(TextColumn\TextColumnSize::Large)
    ->color('primary')
    ->extraAttributes(['class' => 'custom-class']);
```

## Filters Reference

### Select Filter

```php
Tables\Filters\SelectFilter::make('status')
    ->options([
        'draft' => 'Draft',
        'reviewing' => 'Reviewing',
        'published' => 'Published',
    ]);

// Multiple selection
Tables\Filters\SelectFilter::make('status')
    ->multiple()
    ->options([
        'draft' => 'Draft',
        'published' => 'Published',
    ]);

// Relationship filter
Tables\Filters\SelectFilter::make('author')
    ->relationship('author', 'name')
    ->searchable()
    ->preload();
```

### Ternary Filter (Boolean)

```php
Tables\Filters\TernaryFilter::make('is_active')
    ->label('Active')
    ->boolean()
    ->trueLabel('Active only')
    ->falseLabel('Inactive only')
    ->native(false);
```

### Date Filter

```php
Tables\Filters\Filter::make('created_at')
    ->form([
        Forms\Components\DatePicker::make('created_from'),
        Forms\Components\DatePicker::make('created_until'),
    ])
    ->query(function (Builder $query, array $data): Builder {
        return $query
            ->when(
                $data['created_from'],
                fn (Builder $query, $date): Builder => $query->whereDate('created_at', '>=', $date),
            )
            ->when(
                $data['created_until'],
                fn (Builder $query, $date): Builder => $query->whereDate('created_at', '<=', $date),
            );
    })
    ->indicateUsing(function (array $data): array {
        $indicators = [];
        if ($data['created_from'] ?? null) {
            $indicators['created_from'] = 'From ' . Carbon::parse($data['created_from'])->toFormattedDateString();
        }
        if ($data['created_until'] ?? null) {
            $indicators['created_until'] = 'Until ' . Carbon::parse($data['created_until'])->toFormattedDateString();
        }
        return $indicators;
    });
```

### Trashed Filter (Soft Deletes)

```php
Tables\Filters\TrashedFilter::make();
```

### Query Builder Filter

```php
Tables\Filters\QueryBuilder::make()
    ->constraints([
        Tables\Filters\QueryBuilder\Constraints\TextConstraint::make('name'),
        Tables\Filters\QueryBuilder\Constraints\NumberConstraint::make('price'),
        Tables\Filters\QueryBuilder\Constraints\DateConstraint::make('created_at'),
        Tables\Filters\QueryBuilder\Constraints\RelationshipConstraint::make('author')
            ->icon('heroicon-o-user')
            ->multiple(),
    ]);
```

## Actions Reference

### Row Actions

```php
->actions([
    Tables\Actions\ViewAction::make(),
    Tables\Actions\EditAction::make(),
    Tables\Actions\DeleteAction::make()
        ->requiresConfirmation(),

    // Custom action
    Tables\Actions\Action::make('publish')
        ->icon('heroicon-o-check')
        ->color('success')
        ->requiresConfirmation()
        ->action(fn (Model $record) => $record->publish())
        ->visible(fn (Model $record): bool => $record->status === 'draft'),

    // Action with modal form
    Tables\Actions\Action::make('send_email')
        ->icon('heroicon-o-envelope')
        ->form([
            Forms\Components\TextInput::make('subject')
                ->required(),
            Forms\Components\RichEditor::make('body')
                ->required(),
        ])
        ->action(function (Model $record, array $data): void {
            Mail::to($record->email)->send(new CustomEmail($data));
        }),

    // Grouped actions
    Tables\Actions\ActionGroup::make([
        Tables\Actions\ViewAction::make(),
        Tables\Actions\EditAction::make(),
        Tables\Actions\DeleteAction::make(),
    ])->dropdown(),

    // Replicate action
    Tables\Actions\ReplicateAction::make()
        ->excludeAttributes(['slug', 'published_at'])
        ->beforeReplicaSaved(function (Model $replica): void {
            $replica->name = $replica->name . ' (Copy)';
        }),
]);
```

### Bulk Actions

```php
->bulkActions([
    Tables\Actions\BulkActionGroup::make([
        Tables\Actions\DeleteBulkAction::make(),
        Tables\Actions\ForceDeleteBulkAction::make(),
        Tables\Actions\RestoreBulkAction::make(),

        // Custom bulk action
        Tables\Actions\BulkAction::make('publish')
            ->icon('heroicon-o-check')
            ->requiresConfirmation()
            ->action(fn (Collection $records) => $records->each->publish())
            ->deselectRecordsAfterCompletion(),

        // Export bulk action
        Tables\Actions\BulkAction::make('export')
            ->icon('heroicon-o-arrow-down-tray')
            ->action(fn (Collection $records) => static::export($records)),
    ]),
]);
```

### Header Actions

```php
->headerActions([
    Tables\Actions\CreateAction::make(),
    Tables\Actions\AttachAction::make()
        ->preloadRecordSelect(),

    // Import action
    Tables\Actions\Action::make('import')
        ->icon('heroicon-o-arrow-up-tray')
        ->form([
            Forms\Components\FileUpload::make('file')
                ->acceptedFileTypes(['text/csv']),
        ])
        ->action(fn (array $data) => static::import($data['file'])),
]);
```

## Table Configuration

```php
public static function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->filters([...])
        ->actions([...])
        ->bulkActions([...])

        // Pagination
        ->paginated([10, 25, 50, 100])
        ->defaultPaginationPageOption(25)

        // Default sort
        ->defaultSort('created_at', 'desc')

        // Reordering
        ->reorderable('sort_order')
        ->defaultSort('sort_order')

        // Grouping
        ->groups([
            Tables\Grouping\Group::make('status')
                ->label('Status')
                ->collapsible(),
            Tables\Grouping\Group::make('author.name')
                ->label('Author'),
        ])

        // Striped rows
        ->striped()

        // Poll for updates
        ->poll('10s')

        // Empty state
        ->emptyStateHeading('No posts yet')
        ->emptyStateDescription('Create your first post to get started.')
        ->emptyStateIcon('heroicon-o-document-text')
        ->emptyStateActions([
            Tables\Actions\CreateAction::make()
                ->label('Create Post'),
        ])

        // Modals
        ->modals([
            'view' => true,
        ])

        // Persist filters
        ->filtersFormColumns(3)
        ->persistFiltersInSession();
}
```

## Output

Generated tables include:
1. Complete column configuration
2. Search and sort settings
3. Filter definitions
4. Row and bulk actions
5. Relationship handling
6. Performance optimizations
