---
name: filament-forms
description: Create FilamentPHP v4 forms with fields, validation, sections, tabs, and relationships
---

# FilamentPHP Forms Generation Skill

## Overview

This skill generates FilamentPHP v4 form schemas with proper field configurations, validation rules, relationships, and layout components.

## Documentation Reference

**CRITICAL:** Before generating forms, read:
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/forms/`
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/schemas/`

## Workflow

### Step 1: Analyze Requirements

Identify:
- Field types needed
- Validation rules
- Relationships (belongsTo, hasMany, etc.)
- Layout preferences (sections, tabs, columns)
- Conditional visibility
- Custom formatting

### Step 2: Read Documentation

Navigate to forms documentation and extract:
- Exact field class names
- Available methods and options
- Validation integration patterns
- Relationship handling

### Step 3: Generate Schema

Build the form schema with proper structure:

```php
use Filament\Forms;
use Filament\Forms\Form;
use Filament\Forms\Components\Section;
use Filament\Forms\Components\Fieldset;
use Filament\Forms\Components\Grid;
use Filament\Forms\Components\TextInput;
use Filament\Forms\Components\Select;

public static function form(Form $form): Form
{
    return $form
        ->schema([
            // Fields organized in sections/fieldsets
        ]);
}
```

## Schema Organization Requirement

**CRITICAL:** All form schemas MUST be organized using layout components. Never place fields directly at the root level of a form schema.

### Minimum Organization Rules

1. **Always use Sections or Fieldsets** - Every form must have at least one Section or Fieldset wrapping its fields
2. **Group related fields** - Fields that belong together logically should be in the same Section/Fieldset
3. **Use descriptive labels** - Sections and Fieldsets should have meaningful titles
4. **Consider collapsibility** - Make sections collapsible when forms are long

### Recommended Hierarchy

```
Form Schema
├── Section: "Primary Information"
│   ├── Fieldset: "Basic Details" (optional grouping)
│   │   ├── TextInput: name
│   │   └── TextInput: email
│   └── Fieldset: "Contact" (optional grouping)
│       ├── TextInput: phone
│       └── TextInput: address
├── Section: "Settings"
│   ├── Toggle: is_active
│   └── Select: status
└── Section: "Media" (collapsible)
    └── FileUpload: avatar
```

### Bad Example (DO NOT DO THIS)

```php
// ❌ WRONG: Fields at root level without organization
public static function form(Form $form): Form
{
    return $form
        ->schema([
            TextInput::make('name'),
            TextInput::make('email'),
            TextInput::make('phone'),
            Toggle::make('is_active'),
            FileUpload::make('avatar'),
        ]);
}
```

### Good Example (ALWAYS DO THIS)

```php
// ✅ CORRECT: Fields organized in sections
public static function form(Form $form): Form
{
    return $form
        ->schema([
            Section::make('Personal Information')
                ->description('Basic user details')
                ->schema([
                    TextInput::make('name')
                        ->required()
                        ->maxLength(255),
                    TextInput::make('email')
                        ->email()
                        ->required(),
                    TextInput::make('phone')
                        ->tel(),
                ]),

            Section::make('Settings')
                ->schema([
                    Toggle::make('is_active')
                        ->label('Active')
                        ->default(true),
                ]),

            Section::make('Profile Image')
                ->collapsible()
                ->schema([
                    FileUpload::make('avatar')
                        ->image()
                        ->disk('public')
                        ->directory('avatars'),
                ]),
        ]);
}
```

### When to Use Section vs Fieldset

| Component | Use Case |
|-----------|----------|
| **Section** | Major logical groupings, can have description, icon, collapsible |
| **Fieldset** | Smaller sub-groupings within a section, lighter visual weight |
| **Tabs** | When sections are numerous and would cause scrolling |
| **Grid** | Column layout within sections (not a replacement for sections) |

### Complex Form Example

```php
public static function form(Form $form): Form
{
    return $form
        ->schema([
            Section::make('Product Details')
                ->icon('heroicon-o-cube')
                ->schema([
                    Fieldset::make('Basic Information')
                        ->schema([
                            TextInput::make('name')
                                ->required()
                                ->maxLength(255),
                            TextInput::make('sku')
                                ->required()
                                ->unique(ignoreRecord: true),
                        ])
                        ->columns(2),

                    Fieldset::make('Pricing')
                        ->schema([
                            TextInput::make('price')
                                ->numeric()
                                ->prefix('$')
                                ->required(),
                            TextInput::make('compare_at_price')
                                ->numeric()
                                ->prefix('$'),
                        ])
                        ->columns(2),

                    RichEditor::make('description')
                        ->columnSpanFull(),
                ]),

            Section::make('Inventory')
                ->icon('heroicon-o-archive-box')
                ->collapsible()
                ->schema([
                    TextInput::make('quantity')
                        ->numeric()
                        ->default(0),
                    Toggle::make('track_inventory')
                        ->default(true),
                ]),

            Section::make('Media')
                ->icon('heroicon-o-photo')
                ->collapsible()
                ->collapsed()
                ->schema([
                    FileUpload::make('images')
                        ->multiple()
                        ->image()
                        ->reorderable(),
                ]),
        ]);
}
```

## Complete Field Reference

### Text Input Fields

```php
// Basic text input
TextInput::make('name')
    ->required()
    ->maxLength(255)
    ->placeholder('Enter name...')
    ->helperText('This will be displayed publicly')
    ->prefixIcon('heroicon-o-user');

// Email input
TextInput::make('email')
    ->email()
    ->required()
    ->unique(ignoreRecord: true);

// Password input
TextInput::make('password')
    ->password()
    ->required()
    ->confirmed()
    ->minLength(8);

// Numeric input
TextInput::make('price')
    ->numeric()
    ->prefix('$')
    ->minValue(0)
    ->maxValue(10000)
    ->step(0.01);

// Phone input
TextInput::make('phone')
    ->tel()
    ->telRegex('/^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\/0-9]*$/');

// URL input
TextInput::make('website')
    ->url()
    ->suffixIcon('heroicon-o-globe-alt');
```

### Textarea Fields

```php
// Basic textarea
Textarea::make('description')
    ->rows(5)
    ->cols(20)
    ->minLength(10)
    ->maxLength(1000)
    ->columnSpanFull();

// Auto-resize textarea
Textarea::make('content')
    ->autosize()
    ->columnSpanFull();
```

### Rich Text Editors

```php
// Rich editor
RichEditor::make('content')
    ->toolbarButtons([
        'blockquote',
        'bold',
        'bulletList',
        'codeBlock',
        'h2',
        'h3',
        'italic',
        'link',
        'orderedList',
        'redo',
        'strike',
        'underline',
        'undo',
    ])
    ->columnSpanFull();

// Markdown editor
MarkdownEditor::make('content')
    ->toolbarButtons([
        'bold',
        'bulletList',
        'codeBlock',
        'edit',
        'italic',
        'link',
        'orderedList',
        'preview',
        'strike',
    ])
    ->columnSpanFull();
```

### Select Fields

```php
// Basic select
Select::make('status')
    ->options([
        'draft' => 'Draft',
        'reviewing' => 'Reviewing',
        'published' => 'Published',
    ])
    ->default('draft')
    ->required();

// Searchable select
Select::make('country')
    ->options(Country::pluck('name', 'id'))
    ->searchable()
    ->preload();

// Multiple select
Select::make('tags')
    ->multiple()
    ->options(Tag::pluck('name', 'id'))
    ->searchable();

// BelongsTo relationship
Select::make('author_id')
    ->relationship('author', 'name')
    ->searchable()
    ->preload()
    ->createOptionForm([
        TextInput::make('name')
            ->required(),
        TextInput::make('email')
            ->email()
            ->required(),
    ]);

// BelongsToMany relationship
Select::make('categories')
    ->relationship('categories', 'name')
    ->multiple()
    ->preload();
```

### Boolean Fields

```php
// Toggle switch
Toggle::make('is_active')
    ->label('Active')
    ->default(true)
    ->onColor('success')
    ->offColor('danger');

// Checkbox
Checkbox::make('terms_accepted')
    ->label('I accept the terms and conditions')
    ->required()
    ->accepted();

// Checkbox list
CheckboxList::make('permissions')
    ->options([
        'create' => 'Create',
        'read' => 'Read',
        'update' => 'Update',
        'delete' => 'Delete',
    ])
    ->columns(2);

// Radio buttons
Radio::make('plan')
    ->options([
        'basic' => 'Basic Plan',
        'pro' => 'Pro Plan',
        'enterprise' => 'Enterprise Plan',
    ])
    ->descriptions([
        'basic' => 'Best for individuals',
        'pro' => 'Best for small teams',
        'enterprise' => 'Best for large organizations',
    ])
    ->required();
```

### Date and Time Fields

```php
// Date picker
DatePicker::make('birth_date')
    ->native(false)
    ->displayFormat('d/m/Y')
    ->maxDate(now())
    ->closeOnDateSelection();

// DateTime picker
DateTimePicker::make('published_at')
    ->native(false)
    ->displayFormat('d/m/Y H:i')
    ->seconds(false)
    ->timezone('America/New_York');

// Time picker
TimePicker::make('start_time')
    ->native(false)
    ->seconds(false)
    ->minutesStep(15);
```

### File Upload Fields

```php
// Basic file upload
FileUpload::make('attachment')
    ->disk('public')
    ->directory('attachments')
    ->acceptedFileTypes(['application/pdf', 'image/*'])
    ->maxSize(10240)
    ->downloadable()
    ->openable();

// Image upload with preview
FileUpload::make('avatar')
    ->image()
    ->imageEditor()
    ->circleCropper()
    ->disk('public')
    ->directory('avatars')
    ->visibility('public');

// Multiple files
FileUpload::make('gallery')
    ->multiple()
    ->reorderable()
    ->appendFiles()
    ->image()
    ->disk('public')
    ->directory('gallery');

// Spatie Media Library
SpatieMediaLibraryFileUpload::make('images')
    ->collection('images')
    ->multiple()
    ->reorderable();
```

### Complex Fields

```php
// Repeater (HasMany inline editing)
Repeater::make('items')
    ->relationship()
    ->schema([
        TextInput::make('name')
            ->required(),
        TextInput::make('quantity')
            ->numeric()
            ->required(),
        TextInput::make('price')
            ->numeric()
            ->prefix('$'),
    ])
    ->columns(3)
    ->defaultItems(1)
    ->addActionLabel('Add Item')
    ->reorderable()
    ->collapsible();

// Builder (flexible content)
Builder::make('content')
    ->blocks([
        Builder\Block::make('heading')
            ->schema([
                TextInput::make('content')
                    ->label('Heading')
                    ->required(),
                Select::make('level')
                    ->options([
                        'h2' => 'H2',
                        'h3' => 'H3',
                        'h4' => 'H4',
                    ]),
            ]),
        Builder\Block::make('paragraph')
            ->schema([
                RichEditor::make('content')
                    ->required(),
            ]),
        Builder\Block::make('image')
            ->schema([
                FileUpload::make('url')
                    ->image()
                    ->required(),
                TextInput::make('alt')
                    ->label('Alt text'),
            ]),
    ])
    ->columnSpanFull();

// Key-Value pairs
KeyValue::make('metadata')
    ->keyLabel('Property')
    ->valueLabel('Value')
    ->addActionLabel('Add Property')
    ->reorderable();

// Tags input
TagsInput::make('tags')
    ->suggestions([
        'laravel',
        'filament',
        'php',
    ])
    ->splitKeys(['Tab', ',']);
```

### Hidden and Special Fields

```php
// Hidden field
Hidden::make('user_id')
    ->default(auth()->id());

// Placeholder (display only)
Placeholder::make('created_at')
    ->label('Created')
    ->content(fn ($record): string => $record?->created_at?->diffForHumans() ?? '-');

// View field (custom blade view)
View::make('custom-field')
    ->view('filament.forms.custom-field');
```

## Layout Components

### Section

```php
Section::make('Personal Information')
    ->description('Enter your personal details')
    ->icon('heroicon-o-user')
    ->collapsible()
    ->collapsed(false)
    ->schema([
        // Fields
    ]);
```

### Fieldset

```php
Fieldset::make('Address')
    ->schema([
        TextInput::make('street'),
        TextInput::make('city'),
        TextInput::make('state'),
        TextInput::make('zip'),
    ])
    ->columns(2);
```

### Tabs

```php
Tabs::make('Tabs')
    ->tabs([
        Tabs\Tab::make('General')
            ->icon('heroicon-o-information-circle')
            ->schema([
                // General fields
            ]),
        Tabs\Tab::make('Media')
            ->icon('heroicon-o-photo')
            ->schema([
                // Media fields
            ]),
        Tabs\Tab::make('SEO')
            ->icon('heroicon-o-magnifying-glass')
            ->schema([
                // SEO fields
            ]),
    ])
    ->columnSpanFull();
```

### Grid and Columns

```php
Grid::make()
    ->schema([
        TextInput::make('first_name')
            ->columnSpan(1),
        TextInput::make('last_name')
            ->columnSpan(1),
        TextInput::make('email')
            ->columnSpanFull(),
    ])
    ->columns(2);
```

### Split Layout

```php
Split::make([
    Section::make('Main Content')
        ->schema([
            // Primary fields
        ]),
    Section::make('Sidebar')
        ->schema([
            // Secondary fields
        ])
        ->grow(false),
]);
```

## Validation

```php
TextInput::make('email')
    ->email()
    ->required()
    ->unique(table: User::class, ignoreRecord: true)
    ->rules(['required', 'email', 'max:255']);

TextInput::make('slug')
    ->required()
    ->unique(ignoreRecord: true)
    ->rules([
        fn (): Closure => function (string $attribute, $value, Closure $fail) {
            if (str_contains($value, ' ')) {
                $fail('Slug cannot contain spaces.');
            }
        },
    ]);
```

## Conditional Visibility

```php
Select::make('type')
    ->options([
        'individual' => 'Individual',
        'company' => 'Company',
    ])
    ->live();

TextInput::make('company_name')
    ->visible(fn (Get $get): bool => $get('type') === 'company');

TextInput::make('tax_id')
    ->hidden(fn (Get $get): bool => $get('type') !== 'company');
```

## Output

Generated forms include:
1. Proper imports (including Section, Fieldset as needed)
2. Type declarations
3. **Schema organized in Sections/Fieldsets** (mandatory)
4. Validation rules
5. Layout structure with columns where appropriate
6. Relationship handling
7. Conditional logic
8. Collapsible sections for optional/secondary content
