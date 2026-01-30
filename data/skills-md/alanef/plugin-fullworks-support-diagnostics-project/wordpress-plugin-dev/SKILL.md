---
name: wordpress-plugin-dev
description: Professional WordPress plugin development best practices following our project structure with composer, namespaced classes, wp-env testing, WPCS compliance, and proper plugin architecture. Use this when working on WordPress plugin code.
---

# WordPress Plugin Development

## Our Project Structure

We use a specific structure with a root project directory and nested plugin directory:

```
plugin-project-name/               # Root project directory
├── composer.json                  # Dev dependencies (phpcs, phpunit, phpstan)
├── phpcs.xml                      # WordPress-Extra ruleset
├── phpcs_sec.xml                  # Security-specific checks
├── phpstan.neon.dist              # Static analysis config
├── phpunit.xml.dist               # PHPUnit configuration
├── tests/                         # Tests at root level
│   ├── bootstrap.php              # PHPUnit bootstrap
│   ├── Unit/                      # Unit tests
│   └── Integration/               # Integration tests
├── vendor/                        # Composer dev dependencies
└── plugin-name/                   # Actual plugin directory
    ├── plugin-name.php            # Main plugin file
    ├── composer.json              # Plugin-specific dependencies
    ├── src/                       # Namespaced source code
    │   ├── Core/
    │   │   └── Main.php           # Main initialization class
    │   ├── Admin/
    │   │   └── AdminPage.php
    │   ├── Data/
    │   └── REST/
    │       └── DiagnosticsEndpoint.php
    ├── vendor/                    # Plugin dependencies
    ├── languages/                 # Translation files
    └── README.md
```

### Key Points:
- Root level has development tools (phpcs, phpunit, phpstan)
- Plugin lives in subdirectory (e.g., `fullworks-support-diagnostics/`)
- Use namespaced classes in `src/` directory
- Composer autoloading for both dev tools and plugin classes
- Tests at root level, outside plugin directory
- Separate composer.json for plugin distribution vs development

### Main Plugin File Pattern
```php
<?php
/**
 * Plugin Name: Your Plugin Name
 * Description: Brief description
 * Version: 1.0.0
 * Author: Your Name
 * License: GPL-2.0+
 * Text Domain: plugin-text-domain
 * Requires at least: 5.8
 * Requires PHP: 7.4
 */

// Prevent direct access
if (!defined('WPINC')) {
    die;
}

// Define plugin constants
define('PREFIX_PLUGIN_VERSION', '1.0.0');
define('PREFIX_PLUGIN_DIR', plugin_dir_path(__FILE__));
define('PREFIX_PLUGIN_URL', plugin_dir_url(__FILE__));

// Load Composer autoloader
require_once PREFIX_PLUGIN_DIR . 'vendor/autoload.php';

// Initialize the plugin
function prefix_initialize_plugin() {
    new \Vendor\PluginName\Core\Main();
}

add_action('plugins_loaded', 'prefix_initialize_plugin', 5);
```

### Namespaced Class Structure
```php
<?php
namespace Vendor\PluginName\Core;

use Vendor\PluginName\Admin\AdminPage;
use Vendor\PluginName\REST\DiagnosticsEndpoint;

class Main {
    const VERSION = '1.0.0';
    const OPTION_NAME = 'prefix_settings';

    private $settings;
    private $admin_page;

    public function __construct() {
        $this->settings = get_option(self::OPTION_NAME, []);
        $this->init_components();
        $this->setup_hooks();
    }

    private function init_components() {
        $this->admin_page = new AdminPage($this->settings);
    }

    private function setup_hooks() {
        add_action('admin_menu', [$this->admin_page, 'add_admin_menu']);
    }
}
```

## WordPress Coding Standards (WPCS)

### Code Style
- Use tabs for indentation (not spaces)
- Use proper PHPDoc blocks for all classes, methods, and functions
- Follow WordPress naming conventions:
  - Namespaced Classes: `Vendor\PluginName\Feature\ClassName`
  - Functions: `prefix_function_name()`
  - Files in src/: `ClassName.php` (matching class name)
- Use Yoda conditions: `if ( true === $value )`
- Space after control structures: `if ( condition ) {`
- Single quotes for strings unless variables or special characters needed

### Our PHPCS Configuration
We use WordPress-Extra with custom exclusions:
```xml
<rule ref="WordPress-Extra">
    <exclude name="WordPress.Files.FileName.NotHyphenatedLowercase"/>
    <exclude name="Generic.WhiteSpace"/>
    <exclude name="PEAR.NamingConventions"/>
    <exclude name="Universal.Files.SeparateFunctionsFromOO"/>
    <exclude name="Universal.Operators.StrictComparisons"/>
</rule>
```

Run checks with:
```bash
composer phpcs        # Full WPCS check
composer check        # PHP compatibility + WPCS
composer phpcbf       # Auto-fix issues
```

## Security Best Practices

### Input Validation and Sanitization
- **Always sanitize input:**
  - `sanitize_text_field()` - general text
  - `sanitize_email()` - email addresses
  - `sanitize_url()` - URLs
  - `absint()` - positive integers
  - `intval()` - integers
  - `wp_kses()` / `wp_kses_post()` - HTML content

### Output Escaping
- **Always escape output:**
  - `esc_html()` - HTML content
  - `esc_attr()` - HTML attributes
  - `esc_url()` - URLs
  - `esc_js()` - JavaScript strings
  - `wp_kses_post()` - Post content with safe HTML

### Nonce Verification
```php
// Creating nonce
wp_nonce_field( 'action_name', 'nonce_field_name' );

// Verifying nonce
if ( ! isset( $_POST['nonce_field_name'] ) ||
     ! wp_verify_nonce( $_POST['nonce_field_name'], 'action_name' ) ) {
    wp_die( 'Security check failed' );
}
```

### Capability Checks
```php
if ( ! current_user_can( 'manage_options' ) ) {
    wp_die( 'Unauthorized access' );
}
```

### SQL Security
- Use `$wpdb->prepare()` for all SQL queries
- Never concatenate user input into SQL
```php
$wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->prefix}table WHERE id = %d AND name = %s",
    $id,
    $name
) );
```

## WordPress Hooks System

### Actions vs Filters
- **Actions:** Execute code at specific points (side effects)
- **Filters:** Modify data before returning

### Best Practices
```php
// Use unique prefixes to avoid conflicts
add_action( 'init', 'prefix_init_function' );
add_filter( 'the_content', 'prefix_modify_content', 10, 1 );

// Always specify priority (default: 10) and accepted args
add_action( 'save_post', 'prefix_save_post_action', 10, 2 );

// Remove actions/filters when needed
remove_action( 'init', 'prefix_init_function' );
```

### Hook Timing
- `plugins_loaded` - After plugins loaded
- `init` - Initialize plugin features
- `admin_init` - Admin-specific initialization
- `wp_enqueue_scripts` - Enqueue frontend assets
- `admin_enqueue_scripts` - Enqueue admin assets

## Database Operations

### Options API
```php
// Get option with default
$value = get_option( 'prefix_option_name', 'default_value' );

// Update option
update_option( 'prefix_option_name', $value );

// Autoload consideration
add_option( 'prefix_option_name', $value, '', 'no' ); // Don't autoload
```

### Custom Tables
- Use `$wpdb->prefix` for table names
- Create tables on plugin activation with `dbDelta()`
- Include charset and collation

## Internationalization (i18n)

```php
// Text domain should match plugin slug
__( 'Text to translate', 'plugin-text-domain' );
_e( 'Text to echo', 'plugin-text-domain' );
esc_html__( 'Text to translate and escape', 'plugin-text-domain' );
esc_html_e( 'Text to echo and escape', 'plugin-text-domain' );

// With variables
sprintf(
    /* translators: %s: user name */
    __( 'Hello, %s!', 'plugin-text-domain' ),
    $user_name
);
```

## REST API

```php
add_action( 'rest_api_init', 'prefix_register_routes' );

function prefix_register_routes() {
    register_rest_route( 'plugin/v1', '/endpoint', array(
        'methods'             => 'POST',
        'callback'            => 'prefix_endpoint_callback',
        'permission_callback' => 'prefix_permission_check',
    ) );
}
```

## Error Handling

```php
// Use WP_Error for error handling
if ( is_wp_error( $result ) ) {
    return $result;
}

// Create errors
return new WP_Error( 'error_code', __( 'Error message', 'text-domain' ) );
```

## Performance Optimization

- Use transients for caching: `set_transient()`, `get_transient()`
- Lazy load when possible
- Minimize database queries
- Use `wp_cache_*` functions for object caching
- Enqueue minified assets in production

## Testing with wp-env

We use `@wordpress/env` (wp-env) for local development and testing:

### Setup
```bash
# Install wp-env globally (if not already installed)
npm -g install @wordpress/env

# Start WordPress environment
wp-env start

# Stop environment
wp-env stop

# Clean/reset environment
wp-env clean
```

### Running Tests
```bash
# Set up test environment variable
export WP_PHPUNIT__TESTS_CONFIG=/path/to/wp-tests-config.php

# Run PHPUnit tests
composer test

# Or run directly with wp-env
wp-env run tests-cli --env-cwd=wp-content/plugins/plugin-name vendor/bin/phpunit
```

### PHPUnit Configuration
Our `phpunit.xml.dist` defines two test suites:
- **unit**: Unit tests in `tests/Unit/` (no WordPress dependencies)
- **integration**: Integration tests in `tests/Integration/` (with WordPress)

### Test Bootstrap
The `tests/bootstrap.php` file:
- Loads Composer autoloader
- Checks for `WP_PHPUNIT__TESTS_CONFIG` environment variable
- Requires WordPress test configuration

### Writing Tests
```php
<?php
namespace Tests\Unit;

use PHPUnit\Framework\TestCase;
use Yoast\PHPUnitPolyfills\Polyfills\AssertEqualsCanonicalizing;

class SampleTest extends TestCase {
    use AssertEqualsCanonicalizing;

    public function test_sample() {
        $this->assertTrue(true);
    }
}
```

## Static Analysis

### PHPStan
```bash
composer phpstan      # Run static analysis
```

Configuration in `phpstan.neon.dist` with WordPress-specific rules via `szepeviktor/phpstan-wordpress`.

## Build and Distribution

### Building Plugin
```bash
composer build
```

This will:
1. Clean `zipped` directory
2. Install production dependencies in plugin directory
3. Create zip file in `zipped/` directory

### Composer Scripts
- `composer phpcs` - Run coding standards check
- `composer check` - Run PHP compatibility checks (7.4-8.3) + WPCS
- `composer phpcbf` - Auto-fix coding standards issues
- `composer phpstan` - Run static analysis
- `composer test` - Run PHPUnit tests
- `composer build` - Build distribution zip

## Testing Checklist

- [ ] All tests pass (`composer test`)
- [ ] No coding standards violations (`composer check`)
- [ ] No static analysis errors (`composer phpstan`)
- [ ] Test in wp-env with WP_DEBUG enabled
- [ ] Test with multiple PHP versions (7.4-8.3)
- [ ] Verify compatibility with latest WordPress version
- [ ] Check that plugin works after building (`composer build`)