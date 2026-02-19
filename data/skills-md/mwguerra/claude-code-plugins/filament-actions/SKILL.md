---
name: filament-actions
description: Create FilamentPHP v4 actions with modals, confirmation, forms, and bulk operations
---

# FilamentPHP Actions Generation Skill

## Overview

This skill generates FilamentPHP v4 actions for resources, pages, and tables including modal actions, form actions, bulk operations, and custom workflows.

## Documentation Reference

**CRITICAL:** Before generating actions, read:
- `/home/mwguerra/projects/mwguerra/claude-code-plugins/filament-specialist/skills/filament-docs/references/actions/`

## Action Types

### Standard CRUD Actions

```php
use Filament\Actions;

// Create action
Actions\CreateAction::make()
    ->label('New Post')
    ->icon('heroicon-o-plus');

// Edit action
Actions\EditAction::make()
    ->label('Edit')
    ->icon('heroicon-o-pencil');

// View action
Actions\ViewAction::make()
    ->label('View Details')
    ->icon('heroicon-o-eye');

// Delete action
Actions\DeleteAction::make()
    ->requiresConfirmation()
    ->modalHeading('Delete post')
    ->modalDescription('Are you sure you want to delete this post? This action cannot be undone.')
    ->modalSubmitActionLabel('Yes, delete');

// Force delete (soft deletes)
Actions\ForceDeleteAction::make()
    ->requiresConfirmation();

// Restore (soft deletes)
Actions\RestoreAction::make();
```

### Custom Actions with Modals

```php
// Simple confirmation action
Actions\Action::make('publish')
    ->label('Publish')
    ->icon('heroicon-o-check-circle')
    ->color('success')
    ->requiresConfirmation()
    ->modalHeading('Publish Post')
    ->modalDescription('Are you sure you want to publish this post?')
    ->modalSubmitActionLabel('Yes, publish')
    ->action(function (Model $record): void {
        $record->update(['status' => 'published', 'published_at' => now()]);

        Notification::make()
            ->title('Post published')
            ->success()
            ->send();
    });

// Action with form modal
Actions\Action::make('send_email')
    ->label('Send Email')
    ->icon('heroicon-o-envelope')
    ->color('info')
    ->form([
        Forms\Components\TextInput::make('subject')
            ->label('Subject')
            ->required()
            ->maxLength(255),
        Forms\Components\Select::make('template')
            ->label('Template')
            ->options([
                'welcome' => 'Welcome Email',
                'reminder' => 'Reminder',
                'promotion' => 'Promotion',
            ])
            ->required(),
        Forms\Components\RichEditor::make('body')
            ->label('Message')
            ->required()
            ->columnSpanFull(),
    ])
    ->action(function (Model $record, array $data): void {
        Mail::to($record->email)->send(new CustomEmail(
            subject: $data['subject'],
            template: $data['template'],
            body: $data['body'],
        ));

        Notification::make()
            ->title('Email sent successfully')
            ->success()
            ->send();
    });

// Wizard action (multi-step)
Actions\Action::make('create_order')
    ->label('Create Order')
    ->icon('heroicon-o-shopping-cart')
    ->steps([
        Forms\Components\Wizard\Step::make('Customer')
            ->schema([
                Forms\Components\Select::make('customer_id')
                    ->relationship('customer', 'name')
                    ->required()
                    ->searchable(),
            ]),
        Forms\Components\Wizard\Step::make('Products')
            ->schema([
                Forms\Components\Repeater::make('items')
                    ->schema([
                        Forms\Components\Select::make('product_id')
                            ->relationship('product', 'name')
                            ->required(),
                        Forms\Components\TextInput::make('quantity')
                            ->numeric()
                            ->required()
                            ->default(1),
                    ])
                    ->columns(2),
            ]),
        Forms\Components\Wizard\Step::make('Shipping')
            ->schema([
                Forms\Components\Textarea::make('address')
                    ->required(),
                Forms\Components\Select::make('shipping_method')
                    ->options([
                        'standard' => 'Standard',
                        'express' => 'Express',
                    ]),
            ]),
    ])
    ->action(function (array $data): void {
        Order::create($data);
    });
```

### Action Visibility and Authorization

```php
Actions\Action::make('approve')
    // Visible only for specific status
    ->visible(fn (Model $record): bool => $record->status === 'pending')

    // Hidden in certain conditions
    ->hidden(fn (Model $record): bool => $record->is_archived)

    // Authorization check
    ->authorize('approve')

    // Or with closure
    ->authorized(fn (): bool => auth()->user()->can('approve_posts'));
```

### Actions with Side Effects

```php
// Action that refreshes data
Actions\Action::make('refresh')
    ->icon('heroicon-o-arrow-path')
    ->action(fn () => null)  // No action needed
    ->after(fn ($livewire) => $livewire->dispatch('refresh'));

// Action with redirect
Actions\Action::make('view_invoice')
    ->icon('heroicon-o-document')
    ->url(fn (Model $record): string => route('invoices.show', $record->invoice_id))
    ->openUrlInNewTab();

// Action with download
Actions\Action::make('download_pdf')
    ->icon('heroicon-o-arrow-down-tray')
    ->action(function (Model $record) {
        return response()->download(
            storage_path("invoices/{$record->invoice_id}.pdf")
        );
    });
```

## Table Row Actions

```php
use Filament\Tables\Actions;

public static function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->actions([
            // Icon-only actions
            Actions\ActionGroup::make([
                Actions\ViewAction::make(),
                Actions\EditAction::make(),
                Actions\DeleteAction::make(),
            ])->dropdownPlacement('bottom-end'),

            // Or inline
            Actions\ViewAction::make()
                ->iconButton(),
            Actions\EditAction::make()
                ->iconButton(),

            // Custom inline action
            Actions\Action::make('duplicate')
                ->icon('heroicon-o-document-duplicate')
                ->iconButton()
                ->action(function (Model $record): void {
                    $replica = $record->replicate();
                    $replica->name = $record->name . ' (Copy)';
                    $replica->save();
                }),
        ]);
}
```

## Bulk Actions

```php
use Filament\Tables\Actions;

->bulkActions([
    Actions\BulkActionGroup::make([
        // Standard bulk delete
        Actions\DeleteBulkAction::make(),

        // Custom bulk action
        Actions\BulkAction::make('publish')
            ->label('Publish Selected')
            ->icon('heroicon-o-check-circle')
            ->color('success')
            ->requiresConfirmation()
            ->action(function (Collection $records): void {
                $records->each->update(['status' => 'published']);

                Notification::make()
                    ->title(count($records) . ' posts published')
                    ->success()
                    ->send();
            })
            ->deselectRecordsAfterCompletion(),

        // Bulk action with form
        Actions\BulkAction::make('assign_category')
            ->label('Assign Category')
            ->icon('heroicon-o-tag')
            ->form([
                Forms\Components\Select::make('category_id')
                    ->label('Category')
                    ->relationship('category', 'name')
                    ->required(),
            ])
            ->action(function (Collection $records, array $data): void {
                $records->each->update(['category_id' => $data['category_id']]);
            }),

        // Export bulk action
        Actions\BulkAction::make('export')
            ->label('Export to CSV')
            ->icon('heroicon-o-arrow-down-tray')
            ->action(function (Collection $records) {
                return Excel::download(
                    new RecordsExport($records),
                    'records.csv'
                );
            }),
    ]),
]);
```

## Header Actions

```php
use Filament\Tables\Actions;

->headerActions([
    // Create action
    Actions\CreateAction::make()
        ->label('New Post'),

    // Import action
    Actions\Action::make('import')
        ->label('Import')
        ->icon('heroicon-o-arrow-up-tray')
        ->form([
            Forms\Components\FileUpload::make('file')
                ->label('CSV File')
                ->acceptedFileTypes(['text/csv'])
                ->required(),
        ])
        ->action(function (array $data): void {
            // Import logic
        }),

    // Attach action (for relationships)
    Actions\AttachAction::make()
        ->preloadRecordSelect()
        ->recordSelectSearchColumns(['name', 'email']),
]);
```

## Relation Manager Actions

```php
// In RelationManager class

protected function getHeaderActions(): array
{
    return [
        Tables\Actions\CreateAction::make(),
        Tables\Actions\AttachAction::make()
            ->preloadRecordSelect()
            ->form(fn (Tables\Actions\AttachAction $action): array => [
                $action->getRecordSelect(),
                Forms\Components\TextInput::make('role')
                    ->required(),
            ]),
        Tables\Actions\AssociateAction::make(),
    ];
}

public function table(Table $table): Table
{
    return $table
        ->columns([...])
        ->actions([
            Tables\Actions\EditAction::make(),
            Tables\Actions\DetachAction::make(),
            Tables\Actions\DissociateAction::make(),
            Tables\Actions\DeleteAction::make(),
        ])
        ->bulkActions([
            Tables\Actions\BulkActionGroup::make([
                Tables\Actions\DetachBulkAction::make(),
                Tables\Actions\DeleteBulkAction::make(),
            ]),
        ]);
}
```

## Page Actions

```php
// In resource page classes

protected function getHeaderActions(): array
{
    return [
        Actions\EditAction::make(),
        Actions\DeleteAction::make(),

        // Custom action
        Actions\Action::make('preview')
            ->icon('heroicon-o-eye')
            ->url(fn (): string => route('posts.show', $this->record))
            ->openUrlInNewTab(),
    ];
}

// For List page
protected function getHeaderActions(): array
{
    return [
        Actions\CreateAction::make(),

        // Global action
        Actions\Action::make('settings')
            ->icon('heroicon-o-cog')
            ->url(fn (): string => route('filament.admin.pages.settings')),
    ];
}
```

## Action Styling and Configuration

```php
Actions\Action::make('custom')
    // Label and icon
    ->label('Custom Action')
    ->icon('heroicon-o-star')
    ->iconPosition(IconPosition::After)

    // Colors
    ->color('success')  // primary, secondary, success, warning, danger, info, gray

    // Size
    ->size(ActionSize::Large)

    // Button style
    ->button()
    ->outlined()
    ->iconButton()
    ->link()

    // Keyboard shortcut
    ->keyBindings(['mod+s'])

    // Extra attributes
    ->extraAttributes([
        'class' => 'my-custom-class',
        'data-action' => 'custom',
    ])

    // Badge
    ->badge(fn () => 5)
    ->badgeColor('danger')

    // Tooltip
    ->tooltip('Click to perform action');
```

## Notifications with Actions

```php
use Filament\Notifications\Notification;
use Filament\Notifications\Actions\Action;

Notification::make()
    ->title('Post created successfully')
    ->success()
    ->body('Your post has been created.')
    ->actions([
        Action::make('view')
            ->button()
            ->url(route('posts.show', $record)),
        Action::make('undo')
            ->color('gray')
            ->action(fn () => $record->delete()),
    ])
    ->send();
```

## Output

Generated actions include:
1. Proper action type selection
2. Modal configurations
3. Form schemas for modal forms
4. Authorization checks
5. Notifications
6. Proper styling and icons
