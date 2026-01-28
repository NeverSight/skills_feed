---
name: laravel-prompts
description: Laravel Prompts - Beautiful and user-friendly forms for command-line applications with browser-like features including placeholder text and validation
---

# Laravel Prompts Skill

Laravel Prompts is a PHP package for adding beautiful and user-friendly forms to your command-line applications, with browser-like features including placeholder text and validation. It's pre-installed in Laravel and supports macOS, Linux, and Windows with WSL.

## When to Use This Skill

This skill should be triggered when:
- Building Laravel Artisan commands with interactive prompts
- Creating user-friendly CLI applications in PHP
- Implementing form validation in command-line tools
- Adding text input, select menus, or confirmation dialogs to console commands
- Working with progress bars, loading spinners, or tables in CLI applications
- Testing Laravel console commands with prompts
- Converting simple console input to modern, validated, interactive prompts

## Quick Reference

### Basic Text Input

```php
use function Laravel\Prompts\text;

// Simple text input
$name = text('What is your name?');

// With placeholder and validation
$name = text(
    label: 'What is your name?',
    placeholder: 'E.g. Taylor Otwell',
    required: true,
    validate: fn (string $value) => match (true) {
        strlen($value) < 3 => 'The name must be at least 3 characters.',
        strlen($value) > 255 => 'The name must not exceed 255 characters.',
        default => null
    }
);
```

### Password Input

```php
use function Laravel\Prompts\password;

$password = password(
    label: 'What is your password?',
    placeholder: 'password',
    hint: 'Minimum 8 characters.',
    required: true,
    validate: fn (string $value) => match (true) {
        strlen($value) < 8 => 'The password must be at least 8 characters.',
        default => null
    }
);
```

### Select (Single Choice)

```php
use function Laravel\Prompts\select;

// Simple select
$role = select(
    label: 'What role should the user have?',
    options: ['Member', 'Contributor', 'Owner']
);

// With associative array (returns key)
$role = select(
    label: 'What role should the user have?',
    options: [
        'member' => 'Member',
        'contributor' => 'Contributor',
        'owner' => 'Owner',
    ],
    default: 'owner'
);

// From database with custom scroll
$role = select(
    label: 'Which category would you like to assign?',
    options: Category::pluck('name', 'id'),
    scroll: 10
);
```

### Multiselect (Multiple Choices)

```php
use function Laravel\Prompts\multiselect;

$permissions = multiselect(
    label: 'What permissions should be assigned?',
    options: ['Read', 'Create', 'Update', 'Delete'],
    default: ['Read', 'Create'],
    hint: 'Permissions may be updated at any time.'
);

// With validation
$permissions = multiselect(
    label: 'What permissions should the user have?',
    options: [
        'read' => 'Read',
        'create' => 'Create',
        'update' => 'Update',
        'delete' => 'Delete',
    ],
    validate: fn (array $values) => ! in_array('read', $values)
        ? 'All users require the read permission.'
        : null
);
```

### Confirmation Dialog

```php
use function Laravel\Prompts\confirm;

// Simple yes/no
$confirmed = confirm('Do you accept the terms?');

// With custom labels
$confirmed = confirm(
    label: 'Do you accept the terms?',
    default: false,
    yes: 'I accept',
    no: 'I decline',
    hint: 'The terms must be accepted to continue.'
);

// Require "Yes"
$confirmed = confirm(
    label: 'Do you accept the terms?',
    required: true
);
```

### Search (Searchable Select)

```php
use function Laravel\Prompts\search;

$id = search(
    label: 'Search for the user that should receive the mail',
    placeholder: 'E.g. Taylor Otwell',
    options: fn (string $value) => strlen($value) > 0
        ? User::whereLike('name', "%{$value}%")->pluck('name', 'id')->all()
        : [],
    hint: 'The user will receive an email immediately.',
    scroll: 10
);
```

### Suggest (Auto-completion)

```php
use function Laravel\Prompts\suggest;

// Static options
$name = suggest('What is your name?', ['Taylor', 'Dayle']);

// Dynamic filtering
$name = suggest(
    label: 'What is your name?',
    options: fn ($value) => collect(['Taylor', 'Dayle'])
        ->filter(fn ($name) => Str::contains($name, $value, ignoreCase: true))
);
```

### Multi-step Forms

```php
use function Laravel\Prompts\form;

$responses = form()
    ->text('What is your name?', required: true, name: 'name')
    ->password(
        label: 'What is your password?',
        validate: ['password' => 'min:8'],
        name: 'password'
    )
    ->confirm('Do you accept the terms?')
    ->submit();

// Access named responses
echo $responses['name'];
echo $responses['password'];

// Dynamic forms with previous responses
$responses = form()
    ->text('What is your name?', required: true, name: 'name')
    ->add(function ($responses) {
        return text("How old are you, {$responses['name']}?");
    }, name: 'age')
    ->submit();
```

### Progress Bar

```php
use function Laravel\Prompts\progress;

// Simple usage
$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: fn ($user) => $this->performTask($user)
);

// With dynamic labels
$users = progress(
    label: 'Updating users',
    steps: User::all(),
    callback: function ($user, $progress) {
        $progress
            ->label("Updating {$user->name}")
            ->hint("Created on {$user->created_at}");
        return $this->performTask($user);
    },
    hint: 'This may take some time.'
);
```

### Loading Spinner

```php
use function Laravel\Prompts\spin;

$response = spin(
    callback: fn () => Http::get('http://example.com'),
    message: 'Fetching response...'
);
```

## Key Concepts

### Input Types

Laravel Prompts provides several input types for different use cases:

- **text()** - Single-line text input with optional placeholder and validation
- **textarea()** - Multi-line text input for longer content
- **password()** - Masked text input for sensitive data
- **confirm()** - Yes/No confirmation dialog
- **select()** - Single selection from a list of options
- **multiselect()** - Multiple selections from a list
- **suggest()** - Text input with auto-completion suggestions
- **search()** - Searchable single selection with dynamic options
- **multisearch()** - Searchable multiple selections
- **pause()** - Pause execution until user presses ENTER

### Output Types

For displaying information without input:

- **info()** - Display informational message
- **note()** - Display a note
- **warning()** - Display warning message
- **error()** - Display error message
- **alert()** - Display alert message
- **table()** - Display tabular data

### Validation

Three ways to validate prompts:

1. **Closure validation**: Custom logic with match expressions
   ```php
   validate: fn (string $value) => match (true) {
       strlen($value) < 3 => 'Too short.',
       default => null
   }
   ```

2. **Laravel validation rules**: Standard Laravel validation
   ```php
   validate: ['email' => 'required|email|unique:users']
   ```

3. **Required flag**: Simple requirement check
   ```php
   required: true
   ```

### Transformation

Use the `transform` parameter to modify input before validation:

```php
$name = text(
    label: 'What is your name?',
    transform: fn (string $value) => trim($value),
    validate: fn (string $value) => strlen($value) < 3
        ? 'The name must be at least 3 characters.'
        : null
);
```

### Terminal Features

- **Scrolling**: Configure visible items with `scroll` parameter (default: 5)
- **Navigation**: Use arrow keys, j/k keys, or vim-style navigation
- **Forms**: Press CTRL + U in forms to return to previous prompts
- **Width**: Keep labels under 74 characters for 80-character terminals

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **other.md** - Complete Laravel Prompts documentation including:
  - All prompt types (text, password, select, search, etc.)
  - Validation strategies and examples
  - Form API for multi-step input
  - Progress bars and loading indicators
  - Informational messages (info, warning, error, alert)
  - Tables for displaying data
  - Testing strategies for console commands
  - Fallback configuration for unsupported environments

Use `view` to read the reference file when detailed information is needed.

## Working with This Skill

### For Beginners

Start with basic prompts:
1. Use `text()` for simple input
2. Add `required: true` for mandatory fields
3. Try `confirm()` for yes/no questions
4. Use `select()` for predefined choices

Example beginner command:
```php
$name = text('What is your name?', required: true);
$confirmed = confirm('Is this correct?');
if ($confirmed) {
    $this->info("Hello, {$name}!");
}
```

### For Intermediate Users

Combine multiple prompts and add validation:
1. Use the `form()` API for multi-step input
2. Add custom validation with closures
3. Use `search()` for database queries
4. Implement progress bars for long operations

Example intermediate command:
```php
$responses = form()
    ->text('Name', required: true, name: 'name')
    ->select('Role', options: ['Member', 'Admin'], name: 'role')
    ->confirm('Create user?')
    ->submit();

if ($responses) {
    progress(
        label: 'Creating user',
        steps: 5,
        callback: fn () => sleep(1)
    );
}
```

### For Advanced Users

Leverage advanced features:
1. Dynamic form fields based on previous responses
2. Complex validation with Laravel validation rules
3. Custom searchable prompts with database integration
4. Transformation functions for data normalization
5. Testing strategies for command prompts

Example advanced command:
```php
$responses = form()
    ->text('Email', validate: ['email' => 'required|email|unique:users'], name: 'email')
    ->add(function ($responses) {
        return search(
            label: 'Select manager',
            options: fn ($value) => User::where('email', 'like', "%{$value}%")
                ->where('email', '!=', $responses['email'])
                ->pluck('name', 'id')
                ->all()
        );
    }, name: 'manager_id')
    ->multiselect(
        label: 'Permissions',
        options: Permission::pluck('name', 'id'),
        validate: fn ($values) => count($values) === 0 ? 'Select at least one permission.' : null,
        name: 'permissions'
    )
    ->submit();
```

### Navigation Tips

- **Arrow keys** or **j/k** - Navigate options in select/multiselect
- **Space** - Select/deselect in multiselect
- **Enter** - Confirm selection or submit input
- **CTRL + U** - Go back to previous prompt (in forms)
- **Type to search** - In search/multisearch prompts
- **Tab** - Auto-complete in suggest prompts

## Testing

Test commands with prompts using Laravel's built-in assertions:

```php
use function Pest\Laravel\artisan;

test('user creation command', function () {
    artisan('users:create')
        ->expectsQuestion('What is your name?', 'Taylor Otwell')
        ->expectsQuestion('What is your email?', '[email protected]')
        ->expectsConfirmation('Create this user?', 'yes')
        ->expectsPromptsInfo('User created successfully!')
        ->assertExitCode(0);
});

test('displays warnings and errors', function () {
    artisan('report:generate')
        ->expectsPromptsWarning('This action cannot be undone')
        ->expectsPromptsError('Something went wrong')
        ->expectsPromptsTable(
            headers: ['Name', 'Email'],
            rows: [
                ['Taylor Otwell', '[email protected]'],
                ['Jason Beggs', '[email protected]'],
            ]
        )
        ->assertExitCode(0);
});
```

## Best Practices

### Design Guidelines
- Keep labels concise (under 74 characters for 80-column terminals)
- Use `hint` parameter for additional context
- Set appropriate `default` values when sensible
- Configure `scroll` for lists with many options (default: 5)

### Validation Strategy
- Use `required: true` for mandatory fields
- Apply Laravel validation rules for standard checks (email, min/max, etc.)
- Use closures for complex business logic validation
- Provide clear, actionable error messages

### User Experience
- Add placeholders to show expected input format
- Use `pause()` before destructive operations
- Show progress bars for operations taking >2 seconds
- Display informational messages after actions complete
- Group related prompts in forms for better flow

### Performance
- Use `search()` callbacks with length checks to avoid expensive queries:
  ```php
  options: fn (string $value) => strlen($value) > 0
      ? User::where('name', 'like', "%{$value}%")->pluck('name', 'id')->all()
      : []
  ```
- Limit database results with pagination or top-N queries
- Cache frequently-accessed option lists
- Use `spin()` for HTTP requests and long operations

## Common Patterns

### User Registration Flow
```php
$responses = form()
    ->text('Name', required: true, name: 'name')
    ->text('Email', validate: ['email' => 'required|email|unique:users'], name: 'email')
    ->password('Password', validate: ['password' => 'required|min:8'], name: 'password')
    ->submit();
```

### Confirmation Before Destructive Action
```php
$confirmed = confirm(
    label: 'Are you sure you want to delete all users?',
    default: false,
    hint: 'This action cannot be undone.'
);

if (! $confirmed) {
    $this->info('Operation cancelled.');
    return;
}
```

### Dynamic Multi-step Form
```php
$responses = form()
    ->select('User type', options: ['Regular', 'Admin'], name: 'type')
    ->add(function ($responses) {
        if ($responses['type'] === 'Admin') {
            return password('Admin password', required: true);
        }
    }, name: 'admin_password')
    ->submit();
```

### Batch Processing with Progress
```php
$items = Item::all();

$results = progress(
    label: 'Processing items',
    steps: $items,
    callback: function ($item, $progress) {
        $progress->hint("Processing: {$item->name}");
        return $this->process($item);
    }
);
```

## Resources

### Official Documentation
- Laravel Prompts Documentation: https://laravel.com/docs/12.x/prompts
- Laravel Console Testing: https://laravel.com/docs/12.x/console-tests

### Platform Support
- **Supported**: macOS, Linux, Windows with WSL
- **Fallback**: Configure fallback behavior for unsupported environments

## Notes

- Laravel Prompts is pre-installed in Laravel framework
- Supports Laravel validation rules for easy integration
- Uses terminal control codes for interactive UI
- All prompts return values that can be used immediately
- Forms support revisiting previous prompts with CTRL + U
- Validation runs on every input change for immediate feedback
- Progress bars can be manually controlled or automated

## Updating

This skill was generated from the official Laravel Prompts documentation. To refresh with updated information, re-scrape the Laravel documentation site.
