---
name: filament-resource
description: Generate FilamentPHP v4 resources with form, table, relation managers, and actions
---

# FilamentPHP Resource Generation Skill

## Overview

This skill generates complete FilamentPHP v4 resources including form schemas, table configurations, relation managers, and custom pages. All generated code follows official documentation patterns.

## Documentation Reference

**CRITICAL:** Before generating any resource, read:
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/general/03-resources/`
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/forms/`
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/tables/`

## Workflow

### Step 1: Gather Requirements

Identify:
- Model name and namespace
- Fields to include in form
- Columns to display in table
- Relationships to manage
- Custom actions needed
- Authorization requirements

### Step 2: Generate Base Resource

Use Laravel artisan to create the resource:

```bash
# Basic resource
php artisan make:filament-resource ModelName

# With generate flag (creates form/table from model)
php artisan make:filament-resource ModelName --generate

# Soft deletes support
php artisan make:filament-resource ModelName --soft-deletes

# View page only
php artisan make:filament-resource ModelName --view

# Simple resource (modal forms instead of pages)
php artisan make:filament-resource ModelName --simple
```

### Step 3: Customize Form Schema

Read form field documentation and implement:

```php
use Filament\Forms;
use Filament\Forms\Form;

public static function form(Form $form): Form
{
    return $form
        ->schema([
            Forms\Components\Section::make('Basic Information')
                ->schema([
                    Forms\Components\TextInput::make('name')
                        ->required()
                        ->maxLength(255),
                    Forms\Components\Textarea::make('description')
                        ->rows(3)
                        ->columnSpanFull(),
                ]),
            Forms\Components\Section::make('Settings')
                ->schema([
                    Forms\Components\Toggle::make('is_active')
                        ->default(true),
                    Forms\Components\Select::make('status')
                        ->options([
                            'draft' => 'Draft',
                            'published' => 'Published',
                        ]),
                ]),
        ]);
}
```

### Step 4: Customize Table

Read table documentation and implement:

```php
use Filament\Tables;
use Filament\Tables\Table;

public static function table(Table $table): Table
{
    return $table
        ->columns([
            Tables\Columns\TextColumn::make('name')
                ->searchable()
                ->sortable(),
            Tables\Columns\IconColumn::make('is_active')
                ->boolean(),
            Tables\Columns\BadgeColumn::make('status')
                ->colors([
                    'warning' => 'draft',
                    'success' => 'published',
                ]),
            Tables\Columns\TextColumn::make('created_at')
                ->dateTime()
                ->sortable()
                ->toggleable(isToggledHiddenByDefault: true),
        ])
        ->filters([
            Tables\Filters\SelectFilter::make('status')
                ->options([
                    'draft' => 'Draft',
                    'published' => 'Published',
                ]),
            Tables\Filters\TernaryFilter::make('is_active'),
        ])
        ->actions([
            Tables\Actions\ViewAction::make(),
            Tables\Actions\EditAction::make(),
            Tables\Actions\DeleteAction::make(),
        ])
        ->bulkActions([
            Tables\Actions\BulkActionGroup::make([
                Tables\Actions\DeleteBulkAction::make(),
            ]),
        ]);
}
```

### Step 5: Add Relation Managers

For relationships, create relation managers:

```bash
php artisan make:filament-relation-manager ResourceName RelationName column_name
```

Register in resource:

```php
public static function getRelations(): array
{
    return [
        RelationManagers\CommentsRelationManager::class,
        RelationManagers\TagsRelationManager::class,
    ];
}
```

### Step 6: Configure Pages

Define resource pages:

```php
public static function getPages(): array
{
    return [
        'index' => Pages\ListModels::route('/'),
        'create' => Pages\CreateModel::route('/create'),
        'view' => Pages\ViewModel::route('/{record}'),
        'edit' => Pages\EditModel::route('/{record}/edit'),
    ];
}
```

### Step 7: Add Authorization

Implement policy methods:

```php
public static function canViewAny(): bool
{
    return auth()->user()->can('view_any_model');
}

public static function canCreate(): bool
{
    return auth()->user()->can('create_model');
}
```

## Form Field Reference

### Text Fields
- `TextInput::make()` - Single line text
- `Textarea::make()` - Multi-line text
- `RichEditor::make()` - WYSIWYG editor
- `MarkdownEditor::make()` - Markdown editor

### Selection Fields
- `Select::make()` - Dropdown select
- `Radio::make()` - Radio buttons
- `Checkbox::make()` - Single checkbox
- `CheckboxList::make()` - Multiple checkboxes
- `Toggle::make()` - Toggle switch

### Date/Time Fields
- `DatePicker::make()` - Date only
- `DateTimePicker::make()` - Date and time
- `TimePicker::make()` - Time only

### File Fields
- `FileUpload::make()` - File upload
- `SpatieMediaLibraryFileUpload::make()` - Media library

### Relationship Fields
- `Select::make()->relationship()` - BelongsTo select
- `CheckboxList::make()->relationship()` - BelongsToMany
- `Repeater::make()->relationship()` - HasMany inline

### Layout Components
- `Section::make()` - Card section
- `Fieldset::make()` - Fieldset grouping
- `Tabs::make()` - Tabbed sections
- `Grid::make()` - Grid layout
- `Split::make()` - Split layout

## Table Column Reference

### Text Columns
- `TextColumn::make()` - Basic text
- `IconColumn::make()` - Boolean icon
- `ImageColumn::make()` - Image thumbnail
- `BadgeColumn::make()` - Badge styling
- `ColorColumn::make()` - Color swatch

### Column Modifiers
- `->searchable()` - Enable search
- `->sortable()` - Enable sort
- `->toggleable()` - Can hide/show
- `->wrap()` - Wrap text
- `->limit()` - Truncate text

## Output

For each resource, generate:

1. **Resource class** - `app/Filament/Resources/ModelResource.php`
2. **Pages** - `app/Filament/Resources/ModelResource/Pages/`
3. **Relation Managers** - `app/Filament/Resources/ModelResource/RelationManagers/`
4. **Test file** - `tests/Feature/Filament/ModelResourceTest.php`
