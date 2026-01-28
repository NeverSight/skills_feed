---
name: wordpress-plugin-core
description: |
  This skill provides comprehensive knowledge for WordPress plugin development, covering core patterns, security best practices, database interactions, hooks/filters, Settings API, custom post types, REST API, and AJAX. This skill should be used when creating WordPress plugins, troubleshooting security issues, implementing custom post types/taxonomies, building admin interfaces, or working with the WordPress database.

  Use when: Creating new WordPress plugins, implementing nonces/sanitization/escaping, working with $wpdb and prepared statements, building Settings API pages, registering custom post types or taxonomies, implementing REST API endpoints, handling AJAX requests, debugging plugin activation/deactivation issues, preventing SQL injection/XSS/CSRF vulnerabilities.

  Keywords: wordpress plugin development, wordpress security, wordpress hooks, wordpress filters, wordpress database, wpdb prepare, sanitize_text_field, esc_html, wp_nonce, custom post type, register_post_type, settings api, rest api, admin-ajax, wordpress sql injection, wordpress xss, wordpress csrf, plugin header, activation hook, deactivation hook, wordpress coding standards, wordpress plugin architecture
license: MIT
---

# WordPress Plugin Development (Core)

**Status**: Production Ready
**Last Updated**: 2025-11-06
**Dependencies**: None (WordPress 5.9+, PHP 7.4+)
**Latest Versions**: WordPress 6.7+, PHP 8.0+ recommended

---

## Quick Start (10 Minutes)

### 1. Choose Your Plugin Structure

WordPress plugins can use three architecture patterns:

- **Simple** (functions only) - For small plugins with <5 functions
- **OOP** (Object-Oriented) - For medium plugins with related functionality
- **PSR-4** (Namespaced + Composer autoload) - For large/modern plugins

**Why this matters:**
- Simple plugins are easiest to start but don't scale well
- OOP provides organization without modern PHP features
- PSR-4 is the modern standard (2025) and most maintainable

### 2. Create Plugin Header

Every plugin MUST have a header comment in the main file:

```php
<?php
/**
 * Plugin Name:       My Awesome Plugin
 * Plugin URI:        https://example.com/my-plugin/
 * Description:       Brief description of what this plugin does.
 * Version:           1.0.0
 * Requires at least: 5.9
 * Requires PHP:      7.4
 * Author:            Your Name
 * Author URI:        https://yoursite.com/
 * License:           GPL v2 or later
 * License URI:       https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain:       my-plugin
 * Domain Path:       /languages
 */

// Exit if accessed directly
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
```

**CRITICAL:**
- Plugin Name is the ONLY required field
- Text Domain must match plugin slug exactly (for translations)
- Always add ABSPATH check to prevent direct file access

### 3. Implement The Security Foundation

Before writing ANY functionality, implement these 5 security essentials:

```php
// 1. Unique Prefix (4-5 chars minimum)
define( 'MYPL_VERSION', '1.0.0' );

function mypl_init() {
    // Your code
}
add_action( 'init', 'mypl_init' );

// 2. ABSPATH Check (every PHP file)
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// 3. Nonces for Forms
<input type="hidden" name="mypl_nonce" value="<?php echo wp_create_nonce( 'mypl_action' ); ?>" />

// 4. Sanitize Input, Escape Output
$clean = sanitize_text_field( $_POST['input'] );
echo esc_html( $output );

// 5. Prepared Statements for Database
global $wpdb;
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->prefix}table WHERE id = %d",
        $id
    )
);
```

---

## The 5-Step Security Foundation

WordPress plugin security has THREE components that must ALL be present:

### Step 1: Use Unique Prefix for Everything

**Why**: Prevents naming conflicts with other plugins and WordPress core.

**Rules**:
- 4-5 characters minimum
- Apply to: functions, classes, constants, options, transients, meta keys, global variables
- Avoid: `wp_`, `__`, `_`, "WordPress"

```php
// GOOD
function mypl_function_name() {}
class MyPL_Class_Name {}
define( 'MYPL_CONSTANT', 'value' );
add_option( 'mypl_option', 'value' );
set_transient( 'mypl_cache', $data, HOUR_IN_SECONDS );

// BAD
function function_name() {}  // No prefix, will conflict
class Settings {}  // Too generic
```

### Step 2: Check Capabilities, Not Just Admin Status

**ERROR**: Using `is_admin()` for permission checks

```php
// WRONG - Anyone can access admin area URLs
if ( is_admin() ) {
    // Delete user data - SECURITY HOLE
}

// CORRECT - Check user capability
if ( current_user_can( 'manage_options' ) ) {
    // Delete user data - Now secure
}
```

**Common Capabilities**:
- `manage_options` - Administrator
- `edit_posts` - Editor/Author
- `publish_posts` - Author
- `edit_pages` - Editor
- `read` - Subscriber

### Step 3: The Security Trinity

**Input → Processing → Output** each require different functions:

```php
// SANITIZATION (Input) - Clean user data
$name = sanitize_text_field( $_POST['name'] );
$email = sanitize_email( $_POST['email'] );
$url = esc_url_raw( $_POST['url'] );
$html = wp_kses_post( $_POST['content'] );  // Allow safe HTML
$key = sanitize_key( $_POST['option'] );
$ids = array_map( 'absint', $_POST['ids'] );  // Array of integers

// VALIDATION (Logic) - Verify it meets requirements
if ( ! is_email( $email ) ) {
    wp_die( 'Invalid email' );
}

// ESCAPING (Output) - Make safe for display
echo esc_html( $name );
echo '<a href="' . esc_url( $url ) . '">';
echo '<div class="' . esc_attr( $class ) . '">';
echo '<textarea>' . esc_textarea( $content ) . '</textarea>';
```

**Critical Rule**: Sanitize on INPUT, escape on OUTPUT. Never trust user data.

### Step 4: Nonces (CSRF Protection)

**What**: One-time tokens that prove requests came from your site.

**Form Pattern**:

```php
// Generate nonce in form
<form method="post">
    <?php wp_nonce_field( 'mypl_action', 'mypl_nonce' ); ?>
    <input type="text" name="data" />
    <button type="submit">Submit</button>
</form>

// Verify nonce in handler
if ( ! isset( $_POST['mypl_nonce'] ) || ! wp_verify_nonce( $_POST['mypl_nonce'], 'mypl_action' ) ) {
    wp_die( 'Security check failed' );
}

// Now safe to proceed
$data = sanitize_text_field( $_POST['data'] );
```

**AJAX Pattern**:

```javascript
// JavaScript
jQuery.ajax({
    url: ajaxurl,
    data: {
        action: 'mypl_ajax_action',
        nonce: mypl_ajax_object.nonce,
        data: formData
    }
});
```

```php
// PHP Handler
function mypl_ajax_handler() {
    check_ajax_referer( 'mypl-ajax-nonce', 'nonce' );

    // Safe to proceed
    wp_send_json_success( array( 'message' => 'Success' ) );
}
add_action( 'wp_ajax_mypl_ajax_action', 'mypl_ajax_handler' );

// Localize script with nonce
wp_localize_script( 'mypl-script', 'mypl_ajax_object', array(
    'ajaxurl' => admin_url( 'admin-ajax.php' ),
    'nonce'   => wp_create_nonce( 'mypl-ajax-nonce' ),
) );
```

### Step 5: Prepared Statements for Database

**CRITICAL**: Always use `$wpdb->prepare()` for queries with user input.

```php
global $wpdb;

// WRONG - SQL Injection vulnerability
$results = $wpdb->get_results( "SELECT * FROM {$wpdb->prefix}table WHERE id = {$_GET['id']}" );

// CORRECT - Prepared statement
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->prefix}table WHERE id = %d",
        $_GET['id']
    )
);
```

**Placeholders**:
- `%s` - String
- `%d` - Integer
- `%f` - Float

**LIKE Queries** (Special Case):

```php
$search = '%' . $wpdb->esc_like( $term ) . '%';
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->prefix}posts WHERE post_title LIKE %s",
        $search
    )
);
```

---

## Critical Rules

### Always Do

✅ **Use unique prefix** (4-5 chars) for all global code (functions, classes, options, transients)
✅ **Add ABSPATH check** to every PHP file: `if ( ! defined( 'ABSPATH' ) ) exit;`
✅ **Check capabilities** (`current_user_can()`) not just `is_admin()`
✅ **Verify nonces** for all forms and AJAX requests
✅ **Use $wpdb->prepare()** for all database queries with user input
✅ **Sanitize input** with `sanitize_*()` functions before saving
✅ **Escape output** with `esc_*()` functions before displaying
✅ **Flush rewrite rules** on activation when registering custom post types
✅ **Use uninstall.php** for permanent cleanup (not deactivation hook)
✅ **Follow WordPress Coding Standards** (tabs for indentation, Yoda conditions)

### Never Do

❌ **Never use extract()** - Creates security vulnerabilities
❌ **Never trust $_POST/$_GET** without sanitization
❌ **Never concatenate user input into SQL** - Always use prepare()
❌ **Never use `is_admin()` alone** for permission checks
❌ **Never output unsanitized data** - Always escape
❌ **Never use generic function/class names** - Always prefix
❌ **Never use short PHP tags** `<?` or `<?=` - Use `<?php` only
❌ **Never delete user data on deactivation** - Only on uninstall
❌ **Never register uninstall hook repeatedly** - Only once on activation
❌ **Never use `register_uninstall_hook()` in main flow** - Use uninstall.php instead

---

## Known Issues Prevention

This skill prevents **20** documented issues:

### Issue #1: SQL Injection
**Error**: Database compromised via unescaped user input
**Source**: https://patchstack.com/articles/sql-injection/ (15% of all vulnerabilities)
**Why It Happens**: Direct concatenation of user input into SQL queries
**Prevention**: Always use `$wpdb->prepare()` with placeholders

```php
// VULNERABLE
$wpdb->query( "DELETE FROM {$wpdb->prefix}table WHERE id = {$_GET['id']}" );

// SECURE
$wpdb->query( $wpdb->prepare( "DELETE FROM {$wpdb->prefix}table WHERE id = %d", $_GET['id'] ) );
```

### Issue #2: XSS (Cross-Site Scripting)
**Error**: Malicious JavaScript executed in user browsers
**Source**: https://patchstack.com (35% of all vulnerabilities)
**Why It Happens**: Outputting unsanitized user data to HTML
**Prevention**: Always escape output with context-appropriate function

```php
// VULNERABLE
echo $_POST['name'];
echo '<div class="' . $_POST['class'] . '">';

// SECURE
echo esc_html( $_POST['name'] );
echo '<div class="' . esc_attr( $_POST['class'] ) . '">';
```

### Issue #3: CSRF (Cross-Site Request Forgery)
**Error**: Unauthorized actions performed on behalf of users
**Source**: https://blog.nintechnet.com/25-wordpress-plugins-vulnerable-to-csrf-attacks/
**Why It Happens**: No verification that requests originated from your site
**Prevention**: Use nonces with `wp_nonce_field()` and `wp_verify_nonce()`

```php
// VULNERABLE
if ( $_POST['action'] == 'delete' ) {
    delete_user( $_POST['user_id'] );
}

// SECURE
if ( ! wp_verify_nonce( $_POST['nonce'], 'mypl_delete_user' ) ) {
    wp_die( 'Security check failed' );
}
delete_user( absint( $_POST['user_id'] ) );
```

### Issue #4: Missing Capability Checks
**Error**: Regular users can access admin functions
**Source**: WordPress Security Review Guidelines
**Why It Happens**: Using `is_admin()` instead of `current_user_can()`
**Prevention**: Always check capabilities, not just admin context

```php
// VULNERABLE
if ( is_admin() ) {
    // Any logged-in user can trigger this
}

// SECURE
if ( current_user_can( 'manage_options' ) ) {
    // Only administrators can trigger this
}
```

### Issue #5: Direct File Access
**Error**: PHP files executed outside WordPress context
**Source**: WordPress Plugin Handbook
**Why It Happens**: No ABSPATH check at top of file
**Prevention**: Add ABSPATH check to every PHP file

```php
// Add to top of EVERY PHP file
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}
```

### Issue #6: Prefix Collision
**Error**: Functions/classes conflict with other plugins
**Source**: WordPress Coding Standards
**Why It Happens**: Generic names without unique prefix
**Prevention**: Use 4-5 character prefix on ALL global code

```php
// CAUSES CONFLICTS
function init() {}
class Settings {}
add_option( 'api_key', $value );

// SAFE
function mypl_init() {}
class MyPL_Settings {}
add_option( 'mypl_api_key', $value );
```

### Issue #7: Rewrite Rules Not Flushed
**Error**: Custom post types return 404 errors
**Source**: WordPress Plugin Handbook
**Why It Happens**: Forgot to flush rewrite rules after registering CPT
**Prevention**: Flush on activation, clear on deactivation

```php
function mypl_activate() {
    mypl_register_cpt();
    flush_rewrite_rules();
}
register_activation_hook( __FILE__, 'mypl_activate' );

function mypl_deactivate() {
    flush_rewrite_rules();
}
register_deactivation_hook( __FILE__, 'mypl_deactivate' );
```

### Issue #8: Transients Not Cleaned
**Error**: Database accumulates expired transients
**Source**: WordPress Transients API Documentation
**Why It Happens**: No cleanup on uninstall
**Prevention**: Delete transients in uninstall.php

```php
// uninstall.php
if ( ! defined( 'WP_UNINSTALL_PLUGIN' ) ) {
    exit;
}

global $wpdb;
$wpdb->query( "DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_mypl_%'" );
$wpdb->query( "DELETE FROM {$wpdb->options} WHERE option_name LIKE '_transient_timeout_mypl_%'" );
```

### Issue #9: Scripts Loaded Everywhere
**Error**: Performance degraded by unnecessary asset loading
**Source**: WordPress Performance Best Practices
**Why It Happens**: Enqueuing scripts/styles without conditional checks
**Prevention**: Only load assets where needed

```php
// BAD - Loads on every page
add_action( 'wp_enqueue_scripts', function() {
    wp_enqueue_script( 'mypl-script', $url );
} );

// GOOD - Only loads on specific page
add_action( 'wp_enqueue_scripts', function() {
    if ( is_page( 'my-page' ) ) {
        wp_enqueue_script( 'mypl-script', $url, array( 'jquery' ), '1.0', true );
    }
} );
```

### Issue #10: Missing Sanitization on Save
**Error**: Malicious data stored in database
**Source**: WordPress Data Validation
**Why It Happens**: Saving $_POST data without sanitization
**Prevention**: Always sanitize before saving

```php
// VULNERABLE
update_option( 'mypl_setting', $_POST['value'] );

// SECURE
update_option( 'mypl_setting', sanitize_text_field( $_POST['value'] ) );
```

### Issue #11: Incorrect LIKE Queries
**Error**: SQL syntax errors or injection vulnerabilities
**Source**: WordPress $wpdb Documentation
**Why It Happens**: LIKE wildcards not escaped properly
**Prevention**: Use `$wpdb->esc_like()`

```php
// WRONG
$search = '%' . $term . '%';

// CORRECT
$search = '%' . $wpdb->esc_like( $term ) . '%';
$results = $wpdb->get_results( $wpdb->prepare( "... WHERE title LIKE %s", $search ) );
```

### Issue #12: Using extract()
**Error**: Variable collision and security vulnerabilities
**Source**: WordPress Coding Standards
**Why It Happens**: extract() creates variables from array keys
**Prevention**: Never use extract(), access array elements directly

```php
// DANGEROUS
extract( $_POST );
// Now $any_array_key becomes a variable

// SAFE
$name = isset( $_POST['name'] ) ? sanitize_text_field( $_POST['name'] ) : '';
```

### Issue #13: Missing Permission Callback in REST API
**Error**: Endpoints accessible to everyone
**Source**: WordPress REST API Handbook
**Why It Happens**: No `permission_callback` specified
**Prevention**: Always add permission_callback

```php
// VULNERABLE
register_rest_route( 'myplugin/v1', '/data', array(
    'callback' => 'my_callback',
) );

// SECURE
register_rest_route( 'myplugin/v1', '/data', array(
    'callback'            => 'my_callback',
    'permission_callback' => function() {
        return current_user_can( 'edit_posts' );
    },
) );
```

### Issue #14: Uninstall Hook Registered Repeatedly
**Error**: Option written on every page load
**Source**: WordPress Plugin Handbook
**Why It Happens**: register_uninstall_hook() called in main flow
**Prevention**: Use uninstall.php file instead

```php
// BAD - Runs on every page load
register_uninstall_hook( __FILE__, 'mypl_uninstall' );

// GOOD - Use uninstall.php file (preferred method)
// Create uninstall.php in plugin root
```

### Issue #15: Data Deleted on Deactivation
**Error**: Users lose data when temporarily disabling plugin
**Source**: WordPress Plugin Development Best Practices
**Why It Happens**: Confusion about deactivation vs uninstall
**Prevention**: Only delete data in uninstall.php, never on deactivation

```php
// WRONG - Deletes user data on deactivation
register_deactivation_hook( __FILE__, function() {
    delete_option( 'mypl_user_settings' );
} );

// CORRECT - Only clear temporary data on deactivation
register_deactivation_hook( __FILE__, function() {
    delete_transient( 'mypl_cache' );
} );

// CORRECT - Delete all data in uninstall.php
```

### Issue #16: Using Deprecated Functions
**Error**: Plugin breaks on WordPress updates
**Source**: WordPress Deprecated Functions List
**Why It Happens**: Using functions removed in newer WordPress versions
**Prevention**: Enable WP_DEBUG during development

```php
// In wp-config.php (development only)
define( 'WP_DEBUG', true );
define( 'WP_DEBUG_LOG', true );
define( 'WP_DEBUG_DISPLAY', false );
```

### Issue #17: Text Domain Mismatch
**Error**: Translations don't load
**Source**: WordPress Internationalization
**Why It Happens**: Text domain doesn't match plugin slug
**Prevention**: Use exact plugin slug everywhere

```php
// Plugin header
// Text Domain: my-plugin

// In code - MUST MATCH EXACTLY
__( 'Text', 'my-plugin' );
_e( 'Text', 'my-plugin' );
```

### Issue #18: Missing Plugin Dependencies
**Error**: Fatal error when required plugin is inactive
**Source**: WordPress Plugin Dependencies
**Why It Happens**: No check for required plugins
**Prevention**: Check for dependencies on plugins_loaded

```php
add_action( 'plugins_loaded', function() {
    if ( ! class_exists( 'WooCommerce' ) ) {
        add_action( 'admin_notices', function() {
            echo '<div class="error"><p>My Plugin requires WooCommerce.</p></div>';
        } );
        return;
    }
    // Initialize plugin
} );
```

### Issue #19: Autosave Triggering Meta Save
**Error**: Meta saved multiple times, performance issues
**Source**: WordPress Post Meta
**Why It Happens**: No autosave check in save_post hook
**Prevention**: Check for DOING_AUTOSAVE constant

```php
add_action( 'save_post', function( $post_id ) {
    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }

    // Safe to save meta
} );
```

### Issue #20: admin-ajax.php Performance
**Error**: Slow AJAX responses
**Source**: https://deliciousbrains.com/comparing-wordpress-rest-api-performance-admin-ajax-php/
**Why It Happens**: admin-ajax.php loads entire WordPress core
**Prevention**: Use REST API for new projects (10x faster)

```php
// OLD: admin-ajax.php (still works but slower)
add_action( 'wp_ajax_mypl_action', 'mypl_ajax_handler' );

// NEW: REST API (10x faster, recommended)
add_action( 'rest_api_init', function() {
    register_rest_route( 'myplugin/v1', '/endpoint', array(
        'methods'             => 'POST',
        'callback'            => 'mypl_rest_handler',
        'permission_callback' => function() {
            return current_user_can( 'edit_posts' );
        },
    ) );
} );
```

---

## Plugin Architecture Patterns

### Pattern 1: Simple Plugin (Functions Only)

**When to use**: Small plugins with <5 functions, no complex state

```php
<?php
/**
 * Plugin Name: Simple Plugin
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

function mypl_init() {
    // Your code here
}
add_action( 'init', 'mypl_init' );

function mypl_admin_menu() {
    add_options_page(
        'My Plugin',
        'My Plugin',
        'manage_options',
        'my-plugin',
        'mypl_settings_page'
    );
}
add_action( 'admin_menu', 'mypl_admin_menu' );

function mypl_settings_page() {
    ?>
    <div class="wrap">
        <h1>My Plugin Settings</h1>
    </div>
    <?php
}
```

### Pattern 2: OOP Plugin

**When to use**: Medium plugins with related functionality, need organization

```php
<?php
/**
 * Plugin Name: OOP Plugin
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

class MyPL_Plugin {

    private static $instance = null;

    public static function get_instance() {
        if ( null === self::$instance ) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        $this->define_constants();
        $this->init_hooks();
    }

    private function define_constants() {
        define( 'MYPL_VERSION', '1.0.0' );
        define( 'MYPL_PLUGIN_DIR', plugin_dir_path( __FILE__ ) );
        define( 'MYPL_PLUGIN_URL', plugin_dir_url( __FILE__ ) );
    }

    private function init_hooks() {
        add_action( 'init', array( $this, 'init' ) );
        add_action( 'admin_menu', array( $this, 'admin_menu' ) );
    }

    public function init() {
        // Initialization code
    }

    public function admin_menu() {
        add_options_page(
            'My Plugin',
            'My Plugin',
            'manage_options',
            'my-plugin',
            array( $this, 'settings_page' )
        );
    }

    public function settings_page() {
        ?>
        <div class="wrap">
            <h1>My Plugin Settings</h1>
        </div>
        <?php
    }
}

// Initialize plugin
function mypl() {
    return MyPL_Plugin::get_instance();
}
mypl();
```

### Pattern 3: PSR-4 Plugin (Modern, Recommended)

**When to use**: Large/modern plugins, team development, 2025+ best practice

**Directory Structure**:
```
my-plugin/
├── my-plugin.php       # Main file
├── composer.json       # Autoloading config
├── src/                # PSR-4 autoloaded classes
│   ├── Admin.php
│   ├── Frontend.php
│   └── Settings.php
├── languages/
└── uninstall.php
```

**composer.json**:
```json
{
    "name": "my-vendor/my-plugin",
    "autoload": {
        "psr-4": {
            "MyPlugin\\": "src/"
        }
    },
    "require": {
        "php": ">=7.4"
    }
}
```

**my-plugin.php**:
```php
<?php
/**
 * Plugin Name: PSR-4 Plugin
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// Composer autoloader
require_once __DIR__ . '/vendor/autoload.php';

use MyPlugin\Admin;
use MyPlugin\Frontend;

class MyPlugin {

    private static $instance = null;

    public static function get_instance() {
        if ( null === self::$instance ) {
            self::$instance = new self();
        }
        return self::$instance;
    }

    private function __construct() {
        $this->init();
    }

    private function init() {
        new Admin();
        new Frontend();
    }
}

MyPlugin::get_instance();
```

**src/Admin.php**:
```php
<?php

namespace MyPlugin;

class Admin {

    public function __construct() {
        add_action( 'admin_menu', array( $this, 'add_menu' ) );
    }

    public function add_menu() {
        add_options_page(
            'My Plugin',
            'My Plugin',
            'manage_options',
            'my-plugin',
            array( $this, 'settings_page' )
        );
    }

    public function settings_page() {
        ?>
        <div class="wrap">
            <h1>My Plugin Settings</h1>
        </div>
        <?php
    }
}
```

---

## Common Patterns

### Pattern 1: Custom Post Types

```php
function mypl_register_cpt() {
    register_post_type( 'book', array(
        'labels' => array(
            'name'          => 'Books',
            'singular_name' => 'Book',
            'add_new_item'  => 'Add New Book',
        ),
        'public'       => true,
        'has_archive'  => true,
        'show_in_rest' => true,  // Gutenberg support
        'supports'     => array( 'title', 'editor', 'thumbnail', 'excerpt' ),
        'rewrite'      => array( 'slug' => 'books' ),
        'menu_icon'    => 'dashicons-book',
    ) );
}
add_action( 'init', 'mypl_register_cpt' );

// CRITICAL: Flush rewrite rules on activation
function mypl_activate() {
    mypl_register_cpt();
    flush_rewrite_rules();
}
register_activation_hook( __FILE__, 'mypl_activate' );

function mypl_deactivate() {
    flush_rewrite_rules();
}
register_deactivation_hook( __FILE__, 'mypl_deactivate' );
```

### Pattern 2: Custom Taxonomies

```php
function mypl_register_taxonomy() {
    register_taxonomy( 'genre', 'book', array(
        'labels' => array(
            'name'          => 'Genres',
            'singular_name' => 'Genre',
        ),
        'hierarchical' => true,  // Like categories
        'show_in_rest' => true,
        'rewrite'      => array( 'slug' => 'genre' ),
    ) );
}
add_action( 'init', 'mypl_register_taxonomy' );
```

### Pattern 3: Meta Boxes

```php
function mypl_add_meta_box() {
    add_meta_box(
        'book_details',
        'Book Details',
        'mypl_meta_box_html',
        'book',
        'normal',
        'high'
    );
}
add_action( 'add_meta_boxes', 'mypl_add_meta_box' );

function mypl_meta_box_html( $post ) {
    $isbn = get_post_meta( $post->ID, '_book_isbn', true );

    wp_nonce_field( 'mypl_save_meta', 'mypl_meta_nonce' );
    ?>
    <label for="book_isbn">ISBN:</label>
    <input type="text" id="book_isbn" name="book_isbn" value="<?php echo esc_attr( $isbn ); ?>" />
    <?php
}

function mypl_save_meta( $post_id ) {
    // Security checks
    if ( ! isset( $_POST['mypl_meta_nonce'] )
         || ! wp_verify_nonce( $_POST['mypl_meta_nonce'], 'mypl_save_meta' ) ) {
        return;
    }

    if ( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) {
        return;
    }

    if ( ! current_user_can( 'edit_post', $post_id ) ) {
        return;
    }

    // Save data
    if ( isset( $_POST['book_isbn'] ) ) {
        update_post_meta(
            $post_id,
            '_book_isbn',
            sanitize_text_field( $_POST['book_isbn'] )
        );
    }
}
add_action( 'save_post_book', 'mypl_save_meta' );
```

### Pattern 4: Settings API

```php
function mypl_add_menu() {
    add_options_page(
        'My Plugin Settings',
        'My Plugin',
        'manage_options',
        'my-plugin',
        'mypl_settings_page'
    );
}
add_action( 'admin_menu', 'mypl_add_menu' );

function mypl_register_settings() {
    register_setting( 'mypl_options', 'mypl_api_key', array(
        'type'              => 'string',
        'sanitize_callback' => 'sanitize_text_field',
        'default'           => '',
    ) );

    add_settings_section(
        'mypl_section',
        'API Settings',
        'mypl_section_callback',
        'my-plugin'
    );

    add_settings_field(
        'mypl_api_key',
        'API Key',
        'mypl_field_callback',
        'my-plugin',
        'mypl_section'
    );
}
add_action( 'admin_init', 'mypl_register_settings' );

function mypl_section_callback() {
    echo '<p>Configure your API settings.</p>';
}

function mypl_field_callback() {
    $value = get_option( 'mypl_api_key' );
    ?>
    <input type="text" name="mypl_api_key" value="<?php echo esc_attr( $value ); ?>" />
    <?php
}

function mypl_settings_page() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }
    ?>
    <div class="wrap">
        <h1><?php echo esc_html( get_admin_page_title() ); ?></h1>
        <form method="post" action="options.php">
            <?php
            settings_fields( 'mypl_options' );
            do_settings_sections( 'my-plugin' );
            submit_button();
            ?>
        </form>
    </div>
    <?php
}
```

### Pattern 5: REST API Endpoints

```php
add_action( 'rest_api_init', function() {
    register_rest_route( 'myplugin/v1', '/data', array(
        'methods'             => WP_REST_Server::READABLE,
        'callback'            => 'mypl_rest_callback',
        'permission_callback' => function() {
            return current_user_can( 'edit_posts' );
        },
        'args'                => array(
            'id' => array(
                'required'          => true,
                'validate_callback' => function( $param ) {
                    return is_numeric( $param );
                },
                'sanitize_callback' => 'absint',
            ),
        ),
    ) );
} );

function mypl_rest_callback( $request ) {
    $id = $request->get_param( 'id' );

    // Process...

    return new WP_REST_Response( array(
        'success' => true,
        'data'    => $data,
    ), 200 );
}
```

### Pattern 6: AJAX Handlers (Legacy)

```php
// Enqueue script with localized data
function mypl_enqueue_ajax_script() {
    wp_enqueue_script( 'mypl-ajax', plugins_url( 'js/ajax.js', __FILE__ ), array( 'jquery' ), '1.0', true );

    wp_localize_script( 'mypl-ajax', 'mypl_ajax_object', array(
        'ajaxurl' => admin_url( 'admin-ajax.php' ),
        'nonce'   => wp_create_nonce( 'mypl-ajax-nonce' ),
    ) );
}
add_action( 'wp_enqueue_scripts', 'mypl_enqueue_ajax_script' );

// AJAX handler (logged-in users)
function mypl_ajax_handler() {
    check_ajax_referer( 'mypl-ajax-nonce', 'nonce' );

    $data = sanitize_text_field( $_POST['data'] );

    // Process...

    wp_send_json_success( array( 'message' => 'Success' ) );
}
add_action( 'wp_ajax_mypl_action', 'mypl_ajax_handler' );

// AJAX handler (logged-out users)
add_action( 'wp_ajax_nopriv_mypl_action', 'mypl_ajax_handler' );
```

**JavaScript (js/ajax.js)**:
```javascript
jQuery(document).ready(function($) {
    $('#my-button').on('click', function() {
        $.ajax({
            url: mypl_ajax_object.ajaxurl,
            type: 'POST',
            data: {
                action: 'mypl_action',
                nonce: mypl_ajax_object.nonce,
                data: 'value'
            },
            success: function(response) {
                console.log(response.data.message);
            }
        });
    });
});
```

### Pattern 7: Custom Database Tables

```php
function mypl_create_tables() {
    global $wpdb;

    $table_name = $wpdb->prefix . 'mypl_data';
    $charset_collate = $wpdb->get_charset_collate();

    $sql = "CREATE TABLE $table_name (
        id bigint(20) NOT NULL AUTO_INCREMENT,
        user_id bigint(20) NOT NULL,
        data text NOT NULL,
        created datetime DEFAULT CURRENT_TIMESTAMP NOT NULL,
        PRIMARY KEY  (id),
        KEY user_id (user_id)
    ) $charset_collate;";

    require_once ABSPATH . 'wp-admin/includes/upgrade.php';
    dbDelta( $sql );

    add_option( 'mypl_db_version', '1.0' );
}

// Create tables on activation
register_activation_hook( __FILE__, 'mypl_create_tables' );
```

### Pattern 8: Transients for Caching

```php
function mypl_get_expensive_data() {
    // Try to get cached data
    $data = get_transient( 'mypl_expensive_data' );

    if ( false === $data ) {
        // Not cached - regenerate
        $data = perform_expensive_operation();

        // Cache for 12 hours
        set_transient( 'mypl_expensive_data', $data, 12 * HOUR_IN_SECONDS );
    }

    return $data;
}

// Clear cache when data changes
function mypl_clear_cache() {
    delete_transient( 'mypl_expensive_data' );
}
add_action( 'save_post', 'mypl_clear_cache' );
```

---

## Using Bundled Resources

### Templates (templates/)

Use these production-ready templates to scaffold plugins quickly:

- `templates/plugin-simple/` - Simple plugin with functions
- `templates/plugin-oop/` - Object-oriented plugin structure
- `templates/plugin-psr4/` - Modern PSR-4 plugin with Composer
- `templates/examples/meta-box.php` - Meta box implementation
- `templates/examples/settings-page.php` - Settings API page
- `templates/examples/custom-post-type.php` - CPT registration
- `templates/examples/rest-endpoint.php` - REST API endpoint
- `templates/examples/ajax-handler.php` - AJAX implementation

**When Claude should use these**: When creating new plugins or implementing specific functionality patterns.

### Scripts (scripts/)

- `scripts/scaffold-plugin.sh` - Interactive plugin scaffolding
- `scripts/check-security.sh` - Security audit for common issues
- `scripts/validate-headers.sh` - Verify plugin headers

**Example Usage:**
```bash
# Scaffold new plugin
./scripts/scaffold-plugin.sh my-plugin simple

# Check for security issues
./scripts/check-security.sh my-plugin.php

# Validate plugin headers
./scripts/validate-headers.sh my-plugin.php
```

### References (references/)

Detailed documentation that Claude can load when needed:

- `references/security-checklist.md` - Complete security audit checklist
- `references/hooks-reference.md` - Common WordPress hooks and filters
- `references/sanitization-guide.md` - All sanitization/escaping functions
- `references/wpdb-patterns.md` - Database query patterns
- `references/common-errors.md` - Extended error prevention guide

**When Claude should load these**: When dealing with security issues, choosing the right hook, sanitizing specific data types, writing database queries, or debugging common errors.

---

## Advanced Topics

### Internationalization (i18n)

```php
// Load text domain
function mypl_load_textdomain() {
    load_plugin_textdomain( 'my-plugin', false, dirname( plugin_basename( __FILE__ ) ) . '/languages' );
}
add_action( 'plugins_loaded', 'mypl_load_textdomain' );

// Translatable strings
__( 'Text', 'my-plugin' );  // Returns translated string
_e( 'Text', 'my-plugin' );  // Echoes translated string
_n( 'One item', '%d items', $count, 'my-plugin' );  // Plural forms
esc_html__( 'Text', 'my-plugin' );  // Translate and escape
esc_html_e( 'Text', 'my-plugin' );  // Translate, escape, and echo
```

### WP-CLI Commands

```php
if ( defined( 'WP_CLI' ) && WP_CLI ) {

    class MyPL_CLI_Command {

        /**
         * Process data
         *
         * ## EXAMPLES
         *
         *     wp mypl process --limit=100
         *
         * @param array $args
         * @param array $assoc_args
         */
        public function process( $args, $assoc_args ) {
            $limit = isset( $assoc_args['limit'] ) ? absint( $assoc_args['limit'] ) : 10;

            WP_CLI::line( "Processing $limit items..." );

            // Process...

            WP_CLI::success( 'Processing complete!' );
        }
    }

    WP_CLI::add_command( 'mypl', 'MyPL_CLI_Command' );
}
```

### Scheduled Events (Cron)

```php
// Schedule event on activation
function mypl_activate() {
    if ( ! wp_next_scheduled( 'mypl_daily_task' ) ) {
        wp_schedule_event( time(), 'daily', 'mypl_daily_task' );
    }
}
register_activation_hook( __FILE__, 'mypl_activate' );

// Clear event on deactivation
function mypl_deactivate() {
    wp_clear_scheduled_hook( 'mypl_daily_task' );
}
register_deactivation_hook( __FILE__, 'mypl_deactivate' );

// Hook to scheduled event
function mypl_do_daily_task() {
    // Perform task
}
add_action( 'mypl_daily_task', 'mypl_do_daily_task' );
```

### Plugin Dependencies Check

```php
add_action( 'admin_init', function() {
    // Check for WooCommerce
    if ( ! class_exists( 'WooCommerce' ) ) {
        deactivate_plugins( plugin_basename( __FILE__ ) );

        add_action( 'admin_notices', function() {
            echo '<div class="error"><p><strong>My Plugin</strong> requires WooCommerce to be installed and active.</p></div>';
        } );

        if ( isset( $_GET['activate'] ) ) {
            unset( $_GET['activate'] );
        }
    }
} );
```

---

## Distribution & Auto-Updates

### Enabling GitHub Auto-Updates

Plugins hosted outside WordPress.org can still provide automatic updates using **Plugin Update Checker** by YahnisElsts. This is the recommended solution for most use cases.

**Quick Start:**

```php
// 1. Install library (git submodule or Composer)
git submodule add https://github.com/YahnisElsts/plugin-update-checker.git

// 2. Add to main plugin file
require plugin_dir_path( __FILE__ ) . 'plugin-update-checker/plugin-update-checker.php';
use YahnisElsts\PluginUpdateChecker\v5\PucFactory;

$updateChecker = PucFactory::buildUpdateChecker(
    'https://github.com/yourusername/your-plugin/',
    __FILE__,
    'your-plugin-slug'
);

// Use GitHub Releases (recommended)
$updateChecker->getVcsApi()->enableReleaseAssets();

// For private repos, use token from wp-config.php
if ( defined( 'YOUR_PLUGIN_GITHUB_TOKEN' ) ) {
    $updateChecker->setAuthentication( YOUR_PLUGIN_GITHUB_TOKEN );
}
```

**Deployment:**

```bash
# 1. Update version in plugin header
# 2. Commit and tag
git add my-plugin.php
git commit -m "Bump version to 1.0.1"
git tag 1.0.1
git push origin main
git push origin 1.0.1

# 3. Create GitHub Release (optional but recommended)
# - Upload pre-built ZIP file (exclude .git, tests, etc.)
# - Add release notes for users
```

**Key Features:**

✅ Works with GitHub, GitLab, BitBucket, or custom servers
✅ Supports public and private repositories
✅ Uses GitHub Releases or tags for versioning
✅ Secure HTTPS-based updates
✅ Optional license key integration
✅ Professional release notes and changelogs
✅ ~100KB library footprint

**Alternative Solutions:**

1. **Git Updater** (user-installable plugin, no coding required)
2. **Custom Update Server** (full control, requires hosting)
3. **Freemius** (commercial, includes licensing and payments)

**Comprehensive Resources:**

- **Complete Guide**: See `references/github-auto-updates.md` (21 pages, all approaches)
- **Implementation Examples**: See `examples/github-updater.php` (10 examples)
- **Security Best Practices**: Checksums, signing, token storage, rate limiting
- **Template Integration**: All 3 plugin templates include setup instructions

**Security Considerations:**

- ✅ Always use HTTPS for repository URLs
- ✅ Never hardcode authentication tokens (use wp-config.php)
- ✅ Implement license validation before offering updates
- ✅ Optional: Add checksums for file verification
- ✅ Rate limit update checks to avoid API throttling
- ✅ Clear cached update data after installation

**When to Use Each Approach:**

| Use Case | Recommended Solution |
|----------|---------------------|
| Open source, public repo | Plugin Update Checker |
| Private plugin, client work | Plugin Update Checker + private repo |
| Commercial plugin | Freemius or Custom Server |
| Multi-platform Git hosting | Git Updater |
| Custom licensing needs | Custom Update Server |

**ZIP Structure Requirement:**

```
plugin.zip
└── my-plugin/       ← Plugin folder MUST be inside ZIP
    ├── my-plugin.php
    ├── readme.txt
    └── ...
```

Incorrect structure will cause WordPress to create a random folder name and break the plugin!

---

## Dependencies

**Required**:
- WordPress 5.9+ (recommend 6.7+)
- PHP 7.4+ (recommend 8.0+)

**Optional**:
- Composer 2.0+ - For PSR-4 autoloading
- WP-CLI 2.0+ - For command-line plugin management
- Query Monitor - For debugging and performance analysis

---

## Official Documentation

- **WordPress Plugin Handbook**: https://developer.wordpress.org/plugins/
- **WordPress Coding Standards**: https://developer.wordpress.org/coding-standards/
- **WordPress REST API**: https://developer.wordpress.org/rest-api/
- **WordPress Database Class ($wpdb)**: https://developer.wordpress.org/reference/classes/wpdb/
- **WordPress Security**: https://developer.wordpress.org/apis/security/
- **Settings API**: https://developer.wordpress.org/plugins/settings/settings-api/
- **Custom Post Types**: https://developer.wordpress.org/plugins/post-types/
- **Transients API**: https://developer.wordpress.org/apis/transients/
- **Context7 Library ID**: /websites/developer_wordpress

---

## Troubleshooting

### Problem: Plugin causes fatal error
**Solution**:
1. Enable WP_DEBUG in wp-config.php
2. Check error log at wp-content/debug.log
3. Verify all class/function names are prefixed
4. Check for missing dependencies

### Problem: 404 errors on custom post type pages
**Solution**: Flush rewrite rules
```php
// Temporarily add to wp-admin
flush_rewrite_rules();
// Remove after visiting wp-admin once
```

### Problem: Nonce verification always fails
**Solution**:
1. Check nonce name matches in field and verification
2. Verify using correct action name
3. Ensure nonce hasn't expired (24 hour default)

### Problem: AJAX returns 0 or -1
**Solution**:
1. Verify action name matches hook: `wp_ajax_{action}`
2. Check nonce is being sent and verified
3. Ensure handler function exists and is hooked correctly

### Problem: Sanitization stripping HTML
**Solution**: Use `wp_kses_post()` instead of `sanitize_text_field()` to allow safe HTML

### Problem: Database queries not working
**Solution**:
1. Always use `$wpdb->prepare()` for queries with variables
2. Check table name includes `$wpdb->prefix`
3. Verify column names and syntax

---

## Complete Setup Checklist

Use this checklist to verify your plugin:

- [ ] Plugin header complete with all fields
- [ ] ABSPATH check at top of every PHP file
- [ ] All functions/classes use unique prefix
- [ ] All forms have nonce verification
- [ ] All user input is sanitized
- [ ] All output is escaped
- [ ] All database queries use $wpdb->prepare()
- [ ] Capability checks (not just is_admin())
- [ ] Custom post types flush rewrite rules on activation
- [ ] Deactivation hook only clears temporary data
- [ ] uninstall.php handles permanent cleanup
- [ ] Text domain matches plugin slug
- [ ] Scripts/styles only load where needed
- [ ] WP_DEBUG enabled during development
- [ ] Tested with Query Monitor for performance
- [ ] No deprecated function warnings
- [ ] Works with latest WordPress version

---

**Questions? Issues?**

1. Check `references/common-errors.md` for extended troubleshooting
2. Verify all steps in the security foundation
3. Check official docs: https://developer.wordpress.org/plugins/
4. Enable WP_DEBUG and check debug.log
5. Use Query Monitor plugin to debug hooks and queries
