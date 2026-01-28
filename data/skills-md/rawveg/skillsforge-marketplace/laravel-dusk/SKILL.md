---
name: laravel-dusk
description: Laravel Dusk - Browser automation and testing API for Laravel applications. Use when writing browser tests, automating UI testing, testing JavaScript interactions, or implementing end-to-end tests in Laravel.
---

# Laravel Dusk Skill

Comprehensive assistance with Laravel Dusk browser automation and testing, providing expert guidance on writing expressive, easy-to-use browser tests for your Laravel applications.

## When to Use This Skill

This skill should be triggered when:
- Writing or debugging browser automation tests for Laravel
- Testing user interfaces and JavaScript interactions
- Implementing end-to-end (E2E) testing workflows
- Setting up automated UI testing in Laravel applications
- Working with form submissions, authentication flows, or page navigation tests
- Configuring ChromeDriver or alternative browser drivers
- Using the Page Object pattern for test organization
- Testing Vue.js components or waiting for JavaScript events
- Troubleshooting browser test failures or timing issues

## Quick Reference

### 1. Basic Browser Test

```php
public function testBasicExample(): void
{
    $this->browse(function (Browser $browser) {
        $browser->visit('/login')
            ->type('email', 'user@example.com')
            ->type('password', 'password')
            ->press('Login')
            ->assertPathIs('/home');
    });
}
```

### 2. Using Dusk Selectors (Recommended)

```html
<!-- In your Blade template -->
<button dusk="login-button">Login</button>
<input dusk="email-input" name="email" />
```

```php
// In your test - use @ prefix for dusk selectors
$browser->type('@email-input', 'user@example.com')
    ->click('@login-button');
```

### 3. Testing Multiple Browsers

```php
public function testMultiUserInteraction(): void
{
    $this->browse(function (Browser $first, Browser $second) {
        $first->loginAs(User::find(1))
            ->visit('/home');

        $second->loginAs(User::find(2))
            ->visit('/home');
    });
}
```

### 4. Waiting for Elements

```php
// Wait for element to appear
$browser->waitFor('.modal')
    ->assertSee('Confirmation Required');

// Wait for text to appear
$browser->waitForText('Hello World');

// Wait for JavaScript condition
$browser->waitUntil('App.data.servers.length > 0');

// Wait when element is available
$browser->whenAvailable('.modal', function (Browser $modal) {
    $modal->assertSee('Delete Account')
        ->press('OK');
});
```

### 5. Form Interactions

```php
// Text input
$browser->type('email', 'user@example.com')
    ->append('notes', 'Additional text')
    ->clear('description');

// Dropdown selection
$browser->select('size', 'Large')
    ->select('categories', ['Art', 'Music']); // Multiple

// Checkboxes and radio buttons
$browser->check('terms')
    ->radio('gender', 'male');

// File upload
$browser->attach('photo', __DIR__.'/photos/profile.jpg');
```

### 6. Page Object Pattern

```php
// Generate page object
// php artisan dusk:page Login

// app/tests/Browser/Pages/Login.php
class Login extends Page
{
    public function url(): string
    {
        return '/login';
    }

    public function elements(): array
    {
        return [
            '@email' => 'input[name=email]',
            '@password' => 'input[name=password]',
            '@submit' => 'button[type=submit]',
        ];
    }

    public function login(Browser $browser, $email, $password): void
    {
        $browser->type('@email', $email)
            ->type('@password', $password)
            ->press('@submit');
    }
}

// Use in test
$browser->visit(new Login)
    ->login('user@example.com', 'password')
    ->assertPathIs('/dashboard');
```

### 7. Browser Macros (Reusable Methods)

```php
// In AppServiceProvider or DuskServiceProvider
use Laravel\Dusk\Browser;

Browser::macro('scrollToElement', function (string $element) {
    $this->script("$('html, body').animate({
        scrollTop: $('{$element}').offset().top
    }, 0);");

    return $this;
});

// Use in tests
$browser->scrollToElement('#footer')
    ->assertSee('Copyright 2024');
```

### 8. Database Management in Tests

```php
use Illuminate\Foundation\Testing\DatabaseMigrations;
use Illuminate\Foundation\Testing\DatabaseTruncation;

class ExampleTest extends DuskTestCase
{
    // Option 1: Run migrations before each test (slower)
    use DatabaseMigrations;

    // Option 2: Truncate tables after first migration (faster)
    use DatabaseTruncation;

    // Exclude specific tables from truncation
    protected $exceptTables = ['migrations'];
}
```

### 9. JavaScript Execution

```php
// Execute JavaScript
$browser->script('document.documentElement.scrollTop = 0');

// Get JavaScript return value
$path = $browser->script('return window.location.pathname');

// Wait for reload after action
$browser->waitForReload(function (Browser $browser) {
    $browser->press('Submit');
})->assertSee('Success');
```

### 10. Common Assertions

```php
// Page assertions
$browser->assertPathIs('/dashboard')
    ->assertRouteIs('dashboard')
    ->assertTitle('Dashboard')
    ->assertSee('Welcome Back')
    ->assertDontSee('Error');

// Form assertions
$browser->assertInputValue('email', 'user@example.com')
    ->assertChecked('remember')
    ->assertSelected('role', 'admin')
    ->assertEnabled('submit-button');

// Element assertions
$browser->assertVisible('.success-message')
    ->assertMissing('.error-alert')
    ->assertPresent('button[type=submit]');

// Authentication assertions
$browser->assertAuthenticated()
    ->assertAuthenticatedAs($user);
```

## Key Concepts

### Dusk Selectors vs CSS Selectors

**Dusk selectors** (recommended) use HTML `dusk` attributes that won't change with UI updates:
- More stable than CSS classes or IDs
- Explicitly mark elements for testing
- Use `@` prefix in tests: `$browser->click('@submit-button')`
- Add to HTML: `<button dusk="submit-button">Submit</button>`

**CSS selectors** are more brittle but sometimes necessary:
- `.class-name`, `#id`, `div > button`
- Can break when HTML structure changes
- Use when you don't control the HTML

### Waiting Strategies

**Always wait explicitly** rather than using arbitrary pauses:
- `waitFor('.selector')` - Wait for element to exist
- `waitUntilMissing('.selector')` - Wait for element to disappear
- `waitForText('text')` - Wait for text to appear
- `waitUntil('condition')` - Wait for JavaScript condition
- `whenAvailable('.selector', callback)` - Run callback when available

### Page Objects

Organize complex test logic into **Page classes**:
- Define URL, assertions, and element selectors
- Create reusable methods for page-specific actions
- Improve test readability and maintainability
- Generate with: `php artisan dusk:page PageName`

### Browser Macros

Define **reusable browser methods** for common patterns:
- Register in service provider's `boot()` method
- Use across all tests
- Chain like built-in methods
- Example: scrolling, modal interactions, custom assertions

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **other.md** - Complete Laravel Dusk documentation covering:
  - Installation and configuration
  - ChromeDriver management
  - Test generation and execution
  - Browser interaction methods
  - Form handling and file uploads
  - Waiting strategies and assertions
  - Page Objects and Components patterns
  - CI/CD integration examples

Use the reference file when you need:
- Detailed API documentation for specific methods
- Complete list of available assertions (70+)
- Configuration options for different environments
- Advanced topics like iframes, JavaScript dialogs, or keyboard macros

## Working with This Skill

### For Beginners

1. **Start with basic tests**: Use simple `visit()`, `type()`, `press()`, and `assertSee()` methods
2. **Use Dusk selectors**: Add `dusk` attributes to your HTML for stable selectors
3. **Learn waiting**: Always use `waitFor()` instead of `pause()` for reliable tests
4. **Run tests**: Execute with `php artisan dusk` to see results

### For Intermediate Users

1. **Implement Page Objects**: Organize complex tests with the Page pattern
2. **Use database traits**: Choose between `DatabaseMigrations` or `DatabaseTruncation`
3. **Create browser macros**: Define reusable methods for common workflows
4. **Test authentication**: Use `loginAs()` to bypass login screens
5. **Handle JavaScript**: Use `waitUntil()` for dynamic content and AJAX

### For Advanced Users

1. **Multi-browser testing**: Test real-time features with multiple browsers
2. **Custom waiting logic**: Use `waitUsing()` for complex conditions
3. **Component pattern**: Create reusable components for shared UI elements
4. **CI/CD integration**: Set up Dusk in GitHub Actions, Travis CI, or other platforms
5. **Alternative drivers**: Configure Selenium Grid or other browsers beyond ChromeDriver

### Navigation Tips

- **Quick examples**: Check the Quick Reference section above for common patterns
- **Method documentation**: See `other.md` for complete API reference
- **Assertions list**: Reference file contains all 70+ available assertions
- **Configuration**: Check reference file for environment setup and driver options
- **Best practices**: Look for "Best Practices" section in reference documentation

## Installation & Setup

```bash
# Install Laravel Dusk
composer require laravel/dusk --dev

# Run installation
php artisan dusk:install

# Update ChromeDriver
php artisan dusk:chrome-driver

# Make binaries executable (Unix)
chmod -R 0755 vendor/laravel/dusk/bin/

# Run tests
php artisan dusk
```

## Common Commands

```bash
# Generate new test
php artisan dusk:make LoginTest

# Generate page object
php artisan dusk:page Dashboard

# Generate component
php artisan dusk:component Modal

# Run all tests
php artisan dusk

# Run specific test
php artisan dusk tests/Browser/LoginTest.php

# Run failed tests only
php artisan dusk:fails

# Run with filter
php artisan dusk --group=authentication

# Update ChromeDriver
php artisan dusk:chrome-driver --detect
```

## Resources

### Official Documentation
- Laravel Dusk Documentation: https://laravel.com/docs/12.x/dusk
- API Reference: See `references/other.md` for complete method listings

### Common Patterns in Reference Files

The reference documentation includes:
- 70+ assertion methods with descriptions
- Complete form interaction API
- Waiting strategies and timing best practices
- Page Object pattern examples
- Browser macro definitions
- CI/CD configuration examples
- Environment-specific test setup

## Best Practices

1. **Use Dusk selectors** (`dusk` attributes) instead of CSS classes for stability
2. **Wait explicitly** with `waitFor()` methods instead of arbitrary `pause()`
3. **Organize with Page Objects** for complex test scenarios
4. **Leverage database truncation** for faster test execution
5. **Create browser macros** for frequently repeated actions
6. **Scope selectors** with `with()` or `elsewhere()` for specific page regions
7. **Test user behavior** rather than implementation details
8. **Use authentication shortcuts** like `loginAs()` to skip login flows
9. **Take screenshots** with `screenshot()` for debugging failures
10. **Group related tests** and use `--group` flag for targeted execution

## Troubleshooting

### Common Issues

**ChromeDriver version mismatch:**
```bash
php artisan dusk:chrome-driver --detect
```

**Elements not found:**
- Use `waitFor('.selector')` before interacting
- Check if element is in an iframe
- Verify selector with browser dev tools

**Tests failing randomly:**
- Replace `pause()` with explicit waits
- Increase timeout: `waitFor('.selector', 10)`
- Use `waitUntil()` for JavaScript conditions

**Database state issues:**
- Use `DatabaseTruncation` trait
- Reset data in `setUp()` method
- Check for transactions in application code

## Notes

- Laravel Dusk uses ChromeDriver by default (no Selenium/JDK required)
- Supports alternative browsers via Selenium WebDriver protocol
- Tests are stored in `tests/Browser` directory
- Page objects go in `tests/Browser/Pages`
- Screenshots saved to `tests/Browser/screenshots` on failure
- Console logs saved to `tests/Browser/console` for debugging
