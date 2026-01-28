---
name: wp-debugging
description: WordPress debugging, dependency checking, and local development patterns. Use when debugging WordPress issues, checking plugin dependencies, setting up local environments, resolving conflicts, or troubleshooting errors in themes and plugins.
---

# WordPress Debugging & Dependency Management

Comprehensive debugging techniques, dependency checking, local development patterns, and conflict resolution for WordPress themes and plugins.

## When to Use

**Use when:**
- Debugging PHP errors, warnings, notices
- Checking if required plugins are active
- Setting up local development environments
- Resolving plugin/theme conflicts
- Troubleshooting performance issues
- Setting up wp-config.php debug options
- Using Query Monitor, Debug Bar, or other tools

---

## Debug Mode Configuration

### wp-config.php Debug Settings

```php
<?php
/**
 * WordPress debugging configuration.
 * Place these BEFORE "That's all, stop editing!" line.
 */

// ======================
// DEVELOPMENT ENVIRONMENT
// ======================

// Enable debug mode
define( 'WP_DEBUG', true );

// Log errors to wp-content/debug.log
define( 'WP_DEBUG_LOG', true );

// Display errors on screen (disable in production!)
define( 'WP_DEBUG_DISPLAY', true );

// Use dev versions of core JS and CSS (non-minified)
define( 'SCRIPT_DEBUG', true );

// Save database queries for analysis
define( 'SAVEQUERIES', true );

// Disable concatenation of admin scripts
define( 'CONCATENATE_SCRIPTS', false );

// ======================
// PRODUCTION ENVIRONMENT
// ======================

/*
define( 'WP_DEBUG', false );
define( 'WP_DEBUG_LOG', false );
define( 'WP_DEBUG_DISPLAY', false );
define( 'SCRIPT_DEBUG', false );
*/

// ======================
// CUSTOM LOG FILE LOCATION
// ======================

// Log to custom location (must be writable)
define( 'WP_DEBUG_LOG', '/path/to/custom/debug.log' );

// Or in uploads directory
define( 'WP_DEBUG_LOG', WP_CONTENT_DIR . '/uploads/debug.log' );
```

### Environment-Based Configuration

```php
<?php
/**
 * Environment-aware wp-config.php
 * Detects local development vs production
 */

// Detect local development environment
$is_local = (
    isset( $_SERVER['HTTP_HOST'] ) && (
        strpos( $_SERVER['HTTP_HOST'], '.local' ) !== false ||
        strpos( $_SERVER['HTTP_HOST'], '.test' ) !== false ||
        strpos( $_SERVER['HTTP_HOST'], 'localhost' ) !== false ||
        $_SERVER['HTTP_HOST'] === '127.0.0.1'
    )
);

// Or use environment variable
$is_local = getenv( 'WP_ENVIRONMENT_TYPE' ) === 'local';

if ( $is_local ) {
    // Local/Development settings
    define( 'WP_DEBUG', true );
    define( 'WP_DEBUG_LOG', true );
    define( 'WP_DEBUG_DISPLAY', true );
    define( 'SCRIPT_DEBUG', true );
    define( 'SAVEQUERIES', true );
    define( 'WP_ENVIRONMENT_TYPE', 'local' );
} else {
    // Production settings
    define( 'WP_DEBUG', false );
    define( 'WP_DEBUG_LOG', true ); // Still log errors
    define( 'WP_DEBUG_DISPLAY', false );
    define( 'SCRIPT_DEBUG', false );
    define( 'WP_ENVIRONMENT_TYPE', 'production' );
}
```

### WordPress Environment Types (5.5+)

```php
<?php
// Set environment type (local, development, staging, production)
define( 'WP_ENVIRONMENT_TYPE', 'local' );

// Usage in code
if ( wp_get_environment_type() === 'local' ) {
    // Local development only code
}

if ( wp_get_environment_type() === 'production' ) {
    // Production only code
}

// Check if development environment
function is_development_environment() {
    return in_array( wp_get_environment_type(), array( 'local', 'development' ), true );
}
```

---

## Error Logging

### Custom Error Logging

```php
<?php
/**
 * Custom error logging utility.
 *
 * @package Plugin_Name
 */

/**
 * Log message to debug.log with context.
 *
 * @param mixed  $message Message to log.
 * @param string $level   Log level (debug, info, warning, error).
 * @param array  $context Additional context data.
 */
function plugin_name_log( $message, $level = 'debug', $context = array() ) {
    // Only log if WP_DEBUG is enabled
    if ( ! defined( 'WP_DEBUG' ) || ! WP_DEBUG ) {
        return;
    }

    $timestamp = current_time( 'Y-m-d H:i:s' );
    $level     = strtoupper( $level );

    // Format message
    if ( is_array( $message ) || is_object( $message ) ) {
        $message = print_r( $message, true );
    }

    // Build log entry
    $log_entry = sprintf(
        "[%s] [%s] [Plugin Name] %s",
        $timestamp,
        $level,
        $message
    );

    // Add context if provided
    if ( ! empty( $context ) ) {
        $log_entry .= ' | Context: ' . wp_json_encode( $context );
    }

    // Add backtrace for errors
    if ( $level === 'ERROR' ) {
        $backtrace  = debug_backtrace( DEBUG_BACKTRACE_IGNORE_ARGS, 5 );
        $log_entry .= "\nBacktrace:\n";
        foreach ( $backtrace as $i => $trace ) {
            $log_entry .= sprintf(
                "  #%d %s:%d %s()\n",
                $i,
                $trace['file'] ?? 'unknown',
                $trace['line'] ?? 0,
                $trace['function'] ?? 'unknown'
            );
        }
    }

    error_log( $log_entry );
}

// Usage examples
plugin_name_log( 'Plugin initialized' );
plugin_name_log( 'User action', 'info', array( 'user_id' => 123 ) );
plugin_name_log( $user_data, 'debug' ); // Arrays/objects
plugin_name_log( 'Something went wrong', 'error' ); // Includes backtrace
```

### Conditional Logging

```php
<?php
/**
 * Debug logging with conditional output.
 */

class Plugin_Name_Logger {

    /**
     * Log only in development.
     */
    public static function dev( $message, $context = array() ) {
        if ( wp_get_environment_type() !== 'production' ) {
            self::log( $message, 'DEBUG', $context );
        }
    }

    /**
     * Always log (for errors).
     */
    public static function error( $message, $context = array() ) {
        self::log( $message, 'ERROR', $context );
    }

    /**
     * Log with SQL query details.
     */
    public static function query( $query, $time = null ) {
        if ( defined( 'SAVEQUERIES' ) && SAVEQUERIES ) {
            $message = sprintf( 'SQL Query (%.4fs): %s', $time, $query );
            self::log( $message, 'QUERY' );
        }
    }

    /**
     * Core logging method.
     */
    private static function log( $message, $level, $context = array() ) {
        if ( ! defined( 'WP_DEBUG_LOG' ) || ! WP_DEBUG_LOG ) {
            return;
        }

        $entry = sprintf(
            '[%s] [%s] %s',
            current_time( 'c' ),
            $level,
            is_string( $message ) ? $message : print_r( $message, true )
        );

        if ( ! empty( $context ) ) {
            $entry .= ' ' . wp_json_encode( $context );
        }

        error_log( $entry );
    }
}

// Usage
Plugin_Name_Logger::dev( 'Processing started' );
Plugin_Name_Logger::error( 'Failed to save', array( 'id' => 123 ) );
```

---

## Dependency Checking

### Check Required Plugins

```php
<?php
/**
 * Plugin dependency checker.
 *
 * @package Plugin_Name
 */

class Plugin_Name_Dependencies {

    /**
     * Required plugins.
     * Format: 'plugin-folder/plugin-file.php' => 'Display Name'
     *
     * @var array
     */
    private static $required_plugins = array(
        'woocommerce/woocommerce.php'        => 'WooCommerce',
        'advanced-custom-fields/acf.php'     => 'Advanced Custom Fields',
        'buddypress/bp-loader.php'           => 'BuddyPress',
    );

    /**
     * Optional plugins (enhanced features).
     *
     * @var array
     */
    private static $optional_plugins = array(
        'query-monitor/query-monitor.php' => 'Query Monitor',
    );

    /**
     * Minimum PHP version.
     *
     * @var string
     */
    private static $min_php_version = '8.0';

    /**
     * Minimum WordPress version.
     *
     * @var string
     */
    private static $min_wp_version = '6.0';

    /**
     * Check all dependencies.
     *
     * @return bool True if all dependencies met.
     */
    public static function check() {
        $errors = array();

        // Check PHP version
        if ( version_compare( PHP_VERSION, self::$min_php_version, '<' ) ) {
            $errors[] = sprintf(
                /* translators: 1: Required PHP version, 2: Current PHP version */
                __( 'PHP %1$s or higher is required. You are running PHP %2$s.', 'plugin-name' ),
                self::$min_php_version,
                PHP_VERSION
            );
        }

        // Check WordPress version
        if ( version_compare( get_bloginfo( 'version' ), self::$min_wp_version, '<' ) ) {
            $errors[] = sprintf(
                /* translators: 1: Required WP version, 2: Current WP version */
                __( 'WordPress %1$s or higher is required. You are running WordPress %2$s.', 'plugin-name' ),
                self::$min_wp_version,
                get_bloginfo( 'version' )
            );
        }

        // Check required plugins
        $missing_plugins = self::get_missing_plugins();
        if ( ! empty( $missing_plugins ) ) {
            $errors[] = sprintf(
                /* translators: %s: List of missing plugins */
                __( 'The following required plugins are missing or inactive: %s', 'plugin-name' ),
                implode( ', ', $missing_plugins )
            );
        }

        if ( ! empty( $errors ) ) {
            add_action( 'admin_notices', function() use ( $errors ) {
                self::display_admin_notice( $errors );
            });
            return false;
        }

        return true;
    }

    /**
     * Get list of missing required plugins.
     *
     * @return array Missing plugin names.
     */
    public static function get_missing_plugins() {
        if ( ! function_exists( 'is_plugin_active' ) ) {
            require_once ABSPATH . 'wp-admin/includes/plugin.php';
        }

        $missing = array();

        foreach ( self::$required_plugins as $plugin_path => $plugin_name ) {
            if ( ! is_plugin_active( $plugin_path ) ) {
                $missing[] = $plugin_name;
            }
        }

        return $missing;
    }

    /**
     * Check if a specific plugin is active.
     *
     * @param string $plugin_path Plugin path (e.g., 'woocommerce/woocommerce.php').
     * @return bool
     */
    public static function is_plugin_active( $plugin_path ) {
        if ( ! function_exists( 'is_plugin_active' ) ) {
            require_once ABSPATH . 'wp-admin/includes/plugin.php';
        }
        return is_plugin_active( $plugin_path );
    }

    /**
     * Check if WooCommerce is active.
     *
     * @return bool
     */
    public static function is_woocommerce_active() {
        return self::is_plugin_active( 'woocommerce/woocommerce.php' );
    }

    /**
     * Check if BuddyPress is active.
     *
     * @return bool
     */
    public static function is_buddypress_active() {
        return self::is_plugin_active( 'buddypress/bp-loader.php' )
            || function_exists( 'buddypress' );
    }

    /**
     * Check if ACF is active.
     *
     * @return bool
     */
    public static function is_acf_active() {
        return self::is_plugin_active( 'advanced-custom-fields/acf.php' )
            || self::is_plugin_active( 'advanced-custom-fields-pro/acf.php' )
            || class_exists( 'ACF' );
    }

    /**
     * Check if Elementor is active.
     *
     * @return bool
     */
    public static function is_elementor_active() {
        return defined( 'ELEMENTOR_VERSION' );
    }

    /**
     * Display admin notice for missing dependencies.
     *
     * @param array $errors Error messages.
     */
    private static function display_admin_notice( $errors ) {
        ?>
        <div class="notice notice-error is-dismissible">
            <p>
                <strong><?php esc_html_e( 'Plugin Name - Missing Requirements:', 'plugin-name' ); ?></strong>
            </p>
            <ul style="list-style: disc; padding-left: 20px;">
                <?php foreach ( $errors as $error ) : ?>
                    <li><?php echo esc_html( $error ); ?></li>
                <?php endforeach; ?>
            </ul>
            <p>
                <?php esc_html_e( 'Please install and activate the required plugins.', 'plugin-name' ); ?>
            </p>
        </div>
        <?php
    }
}

// Usage in main plugin file
add_action( 'plugins_loaded', function() {
    if ( ! Plugin_Name_Dependencies::check() ) {
        return; // Don't initialize plugin if dependencies not met
    }

    // Initialize plugin
    Plugin_Name::instance();
});
```

### Plugin Version Checking

```php
<?php
/**
 * Check plugin version requirements.
 */

class Plugin_Name_Version_Check {

    /**
     * Required plugin versions.
     *
     * @var array
     */
    private static $required_versions = array(
        'woocommerce' => array(
            'path'     => 'woocommerce/woocommerce.php',
            'name'     => 'WooCommerce',
            'version'  => '8.0.0',
            'constant' => 'WC_VERSION',
        ),
        'elementor' => array(
            'path'     => 'elementor/elementor.php',
            'name'     => 'Elementor',
            'version'  => '3.18.0',
            'constant' => 'ELEMENTOR_VERSION',
        ),
        'buddypress' => array(
            'path'     => 'buddypress/bp-loader.php',
            'name'     => 'BuddyPress',
            'version'  => '12.0.0',
            'function' => 'bp_get_version',
        ),
    );

    /**
     * Check if plugin meets version requirement.
     *
     * @param string $plugin Plugin key from $required_versions.
     * @return bool|string True if met, error message if not.
     */
    public static function check_version( $plugin ) {
        if ( ! isset( self::$required_versions[ $plugin ] ) ) {
            return true;
        }

        $config = self::$required_versions[ $plugin ];

        // Check if plugin is active
        if ( ! function_exists( 'is_plugin_active' ) ) {
            require_once ABSPATH . 'wp-admin/includes/plugin.php';
        }

        if ( ! is_plugin_active( $config['path'] ) ) {
            return sprintf(
                '%s is not active.',
                $config['name']
            );
        }

        // Get current version
        $current_version = null;

        if ( isset( $config['constant'] ) && defined( $config['constant'] ) ) {
            $current_version = constant( $config['constant'] );
        } elseif ( isset( $config['function'] ) && function_exists( $config['function'] ) ) {
            $current_version = call_user_func( $config['function'] );
        }

        if ( ! $current_version ) {
            return true; // Can't determine version, assume OK
        }

        // Compare versions
        if ( version_compare( $current_version, $config['version'], '<' ) ) {
            return sprintf(
                '%s version %s or higher is required. You have version %s.',
                $config['name'],
                $config['version'],
                $current_version
            );
        }

        return true;
    }

    /**
     * Check all required versions.
     *
     * @return array Errors array (empty if all OK).
     */
    public static function check_all() {
        $errors = array();

        foreach ( array_keys( self::$required_versions ) as $plugin ) {
            $result = self::check_version( $plugin );
            if ( true !== $result ) {
                $errors[] = $result;
            }
        }

        return $errors;
    }
}

// Usage
$version_errors = Plugin_Name_Version_Check::check_all();
if ( ! empty( $version_errors ) ) {
    // Display admin notice with errors
}
```

### Conditional Feature Loading

```php
<?php
/**
 * Load features based on available plugins.
 */

class Plugin_Name_Features {

    /**
     * Initialize features based on available dependencies.
     */
    public static function init() {
        // Core features (always load)
        require_once PLUGIN_NAME_PATH . 'includes/core-features.php';

        // WooCommerce integration
        if ( self::is_woocommerce_ready() ) {
            require_once PLUGIN_NAME_PATH . 'includes/woocommerce-integration.php';
            add_action( 'init', array( __CLASS__, 'init_woocommerce' ) );
        }

        // BuddyPress integration
        if ( self::is_buddypress_ready() ) {
            require_once PLUGIN_NAME_PATH . 'includes/buddypress-integration.php';
            add_action( 'bp_include', array( __CLASS__, 'init_buddypress' ) );
        }

        // Elementor widgets
        if ( self::is_elementor_ready() ) {
            add_action( 'elementor/widgets/register', array( __CLASS__, 'register_elementor_widgets' ) );
        }

        // Gutenberg blocks (check if block editor is available)
        if ( self::is_gutenberg_ready() ) {
            add_action( 'init', array( __CLASS__, 'register_blocks' ) );
        }
    }

    /**
     * Check if WooCommerce is ready.
     */
    private static function is_woocommerce_ready() {
        return class_exists( 'WooCommerce' ) && defined( 'WC_VERSION' );
    }

    /**
     * Check if BuddyPress is ready.
     */
    private static function is_buddypress_ready() {
        return function_exists( 'buddypress' ) && bp_is_active( 'members' );
    }

    /**
     * Check if Elementor is ready.
     */
    private static function is_elementor_ready() {
        return did_action( 'elementor/loaded' );
    }

    /**
     * Check if Gutenberg/block editor is available.
     */
    private static function is_gutenberg_ready() {
        return function_exists( 'register_block_type' );
    }

    // Feature initialization methods...
}

// Hook early to check dependencies
add_action( 'plugins_loaded', array( 'Plugin_Name_Features', 'init' ), 20 );
```

---

## Local Development Patterns

### Environment Detection

```php
<?php
/**
 * Environment detection utilities.
 */

class Plugin_Name_Environment {

    /**
     * Detect if running on local development.
     *
     * @return bool
     */
    public static function is_local() {
        // Check WP_ENVIRONMENT_TYPE first (5.5+)
        if ( function_exists( 'wp_get_environment_type' ) ) {
            return wp_get_environment_type() === 'local';
        }

        // Check for common local development patterns
        $host = $_SERVER['HTTP_HOST'] ?? '';

        $local_patterns = array(
            '.local',
            '.test',
            '.dev',
            '.localhost',
            'localhost',
            '127.0.0.1',
            '::1',
        );

        foreach ( $local_patterns as $pattern ) {
            if ( strpos( $host, $pattern ) !== false ) {
                return true;
            }
        }

        // Check for common local development tools
        $local_tools = array(
            'C:/laragon',      // Laragon
            '/Applications/MAMP',  // MAMP
            '/Applications/Local', // Local by Flywheel
            'vagrant',             // Vagrant
        );

        foreach ( $local_tools as $tool ) {
            if ( strpos( ABSPATH, $tool ) !== false ) {
                return true;
            }
        }

        return false;
    }

    /**
     * Detect specific local development tool.
     *
     * @return string|null Tool name or null.
     */
    public static function get_local_tool() {
        if ( strpos( ABSPATH, 'Local Sites' ) !== false ) {
            return 'localwp';
        }

        if ( strpos( ABSPATH, 'laragon' ) !== false ) {
            return 'laragon';
        }

        if ( strpos( ABSPATH, 'MAMP' ) !== false ) {
            return 'mamp';
        }

        if ( strpos( ABSPATH, 'vagrant' ) !== false ) {
            return 'vagrant';
        }

        if ( defined( 'WPENGINE_ACCOUNT' ) ) {
            return 'wpengine';
        }

        if ( isset( $_SERVER['PANTHEON_ENVIRONMENT'] ) ) {
            return 'pantheon';
        }

        return null;
    }

    /**
     * Check if running on staging.
     *
     * @return bool
     */
    public static function is_staging() {
        if ( function_exists( 'wp_get_environment_type' ) ) {
            return wp_get_environment_type() === 'staging';
        }

        $host = $_SERVER['HTTP_HOST'] ?? '';

        $staging_patterns = array(
            'staging.',
            'stage.',
            '.staging',
            '-staging',
            'dev.',
            '.dev',
        );

        foreach ( $staging_patterns as $pattern ) {
            if ( strpos( $host, $pattern ) !== false ) {
                return true;
            }
        }

        return false;
    }

    /**
     * Check if running on production.
     *
     * @return bool
     */
    public static function is_production() {
        if ( function_exists( 'wp_get_environment_type' ) ) {
            return wp_get_environment_type() === 'production';
        }

        return ! self::is_local() && ! self::is_staging();
    }

    /**
     * Get environment name.
     *
     * @return string
     */
    public static function get_environment() {
        if ( function_exists( 'wp_get_environment_type' ) ) {
            return wp_get_environment_type();
        }

        if ( self::is_local() ) {
            return 'local';
        }

        if ( self::is_staging() ) {
            return 'staging';
        }

        return 'production';
    }
}

// Usage examples
if ( Plugin_Name_Environment::is_local() ) {
    // Enable verbose logging
    define( 'PLUGIN_NAME_DEBUG', true );
}

if ( Plugin_Name_Environment::is_production() ) {
    // Disable debug features
}
```

### Local WP Configuration

```php
<?php
/**
 * Local by Flywheel specific configurations.
 */

// Detect Local WP
if ( strpos( ABSPATH, 'Local Sites' ) !== false ) {

    // Enable debug features
    define( 'WP_DEBUG', true );
    define( 'WP_DEBUG_LOG', true );
    define( 'WP_DEBUG_DISPLAY', true );
    define( 'SCRIPT_DEBUG', true );
    define( 'SAVEQUERIES', true );

    // Disable external HTTP for faster local development
    // define( 'WP_HTTP_BLOCK_EXTERNAL', true );
    // define( 'WP_ACCESSIBLE_HOSTS', 'api.wordpress.org,*.github.com' );

    // Increase memory for development
    define( 'WP_MEMORY_LIMIT', '512M' );
    define( 'WP_MAX_MEMORY_LIMIT', '512M' );

    // Disable cron for local (run manually)
    // define( 'DISABLE_WP_CRON', true );

    // Use local SSL
    // define( 'FORCE_SSL_ADMIN', false );
}
```

---

## Debugging Tools

### Query Monitor Integration

```php
<?php
/**
 * Query Monitor integration for debugging.
 */

class Plugin_Name_Query_Monitor {

    /**
     * Add custom panels/data to Query Monitor.
     */
    public static function init() {
        // Only if Query Monitor is active
        if ( ! class_exists( 'QM' ) ) {
            return;
        }

        // Add custom timer
        add_action( 'plugins_loaded', array( __CLASS__, 'start_timer' ), 1 );
        add_action( 'wp_loaded', array( __CLASS__, 'end_timer' ) );

        // Log custom data
        add_filter( 'qm/output/panel', array( __CLASS__, 'add_custom_panel' ), 10, 2 );
    }

    /**
     * Start performance timer.
     */
    public static function start_timer() {
        do_action( 'qm/start', 'plugin_name_init' );
    }

    /**
     * End performance timer.
     */
    public static function end_timer() {
        do_action( 'qm/stop', 'plugin_name_init' );
    }

    /**
     * Log debug data to Query Monitor.
     *
     * @param string $message Message to log.
     * @param mixed  $data    Data to log.
     */
    public static function log( $message, $data = null ) {
        if ( function_exists( 'do_action' ) ) {
            do_action( 'qm/debug', $message, $data );
        }
    }

    /**
     * Log warning to Query Monitor.
     */
    public static function warning( $message ) {
        do_action( 'qm/warning', $message );
    }

    /**
     * Log error to Query Monitor.
     */
    public static function error( $message ) {
        do_action( 'qm/error', $message );
    }
}

// Usage
Plugin_Name_Query_Monitor::log( 'Processing order', $order_data );
Plugin_Name_Query_Monitor::warning( 'Deprecated function called' );
Plugin_Name_Query_Monitor::error( 'Failed to connect to API' );
```

### Debug Bar Integration

```php
<?php
/**
 * Debug Bar panel for plugin.
 */

class Plugin_Name_Debug_Bar_Panel extends Debug_Bar_Panel {

    public function init() {
        $this->title( 'Plugin Name' );
    }

    public function prerender() {
        $this->set_visible( true );
    }

    public function render() {
        $data = Plugin_Name::get_debug_data();
        ?>
        <div id="debug-bar-plugin-name">
            <h3>Plugin Name Debug Info</h3>

            <h4>Settings</h4>
            <pre><?php print_r( get_option( 'plugin_name_settings' ) ); ?></pre>

            <h4>Active Features</h4>
            <ul>
                <?php foreach ( $data['features'] as $feature => $active ) : ?>
                    <li>
                        <?php echo esc_html( $feature ); ?>:
                        <?php echo $active ? '✅' : '❌'; ?>
                    </li>
                <?php endforeach; ?>
            </ul>

            <h4>Performance</h4>
            <table>
                <tr>
                    <td>Queries:</td>
                    <td><?php echo esc_html( $data['query_count'] ); ?></td>
                </tr>
                <tr>
                    <td>Load Time:</td>
                    <td><?php echo esc_html( $data['load_time'] ); ?>ms</td>
                </tr>
            </table>
        </div>
        <?php
    }
}

// Register panel
add_filter( 'debug_bar_panels', function( $panels ) {
    if ( class_exists( 'Plugin_Name_Debug_Bar_Panel' ) ) {
        $panels[] = new Plugin_Name_Debug_Bar_Panel();
    }
    return $panels;
});
```

### Custom Debug Helper

```php
<?php
/**
 * Debug helper function for development.
 */

if ( ! function_exists( 'dd' ) ) {
    /**
     * Dump and die - for debugging.
     *
     * @param mixed ...$vars Variables to dump.
     */
    function dd( ...$vars ) {
        if ( ! defined( 'WP_DEBUG' ) || ! WP_DEBUG ) {
            return;
        }

        foreach ( $vars as $var ) {
            echo '<pre style="background: #1e1e1e; color: #dcdcdc; padding: 15px; margin: 10px; border-radius: 5px; overflow: auto;">';
            var_dump( $var );
            echo '</pre>';
        }

        die();
    }
}

if ( ! function_exists( 'dump' ) ) {
    /**
     * Dump without dying.
     *
     * @param mixed ...$vars Variables to dump.
     */
    function dump( ...$vars ) {
        if ( ! defined( 'WP_DEBUG' ) || ! WP_DEBUG ) {
            return;
        }

        foreach ( $vars as $var ) {
            echo '<pre style="background: #1e1e1e; color: #dcdcdc; padding: 15px; margin: 10px; border-radius: 5px; overflow: auto;">';
            var_dump( $var );
            echo '</pre>';
        }
    }
}

if ( ! function_exists( 'console_log' ) ) {
    /**
     * Log to browser console.
     *
     * @param mixed  $data  Data to log.
     * @param string $label Optional label.
     */
    function console_log( $data, $label = '' ) {
        if ( ! defined( 'WP_DEBUG' ) || ! WP_DEBUG ) {
            return;
        }

        $js_data = wp_json_encode( $data );
        $label   = esc_js( $label );

        add_action( 'wp_footer', function() use ( $js_data, $label ) {
            echo "<script>console.log('{$label}', {$js_data});</script>";
        });

        add_action( 'admin_footer', function() use ( $js_data, $label ) {
            echo "<script>console.log('{$label}', {$js_data});</script>";
        });
    }
}

// Usage
dump( $user_data );
dd( $query_results ); // Stops execution
console_log( $ajax_response, 'API Response' );
```

---

## Conflict Detection

### Plugin Conflict Checker

```php
<?php
/**
 * Plugin conflict detection and resolution.
 */

class Plugin_Name_Conflict_Checker {

    /**
     * Known conflicting plugins.
     *
     * @var array
     */
    private static $known_conflicts = array(
        'plugin-that-conflicts/plugin.php' => array(
            'name'    => 'Conflicting Plugin',
            'reason'  => 'Uses same shortcode [example]',
            'resolve' => 'Deactivate one of the plugins or use the filter to change shortcode.',
        ),
        'another-conflict/plugin.php' => array(
            'name'    => 'Another Plugin',
            'reason'  => 'Overrides same hooks with different priority',
            'resolve' => 'Adjust hook priority using filters.',
        ),
    );

    /**
     * Check for known conflicts.
     *
     * @return array Active conflicts.
     */
    public static function check_conflicts() {
        if ( ! function_exists( 'is_plugin_active' ) ) {
            require_once ABSPATH . 'wp-admin/includes/plugin.php';
        }

        $conflicts = array();

        foreach ( self::$known_conflicts as $plugin_path => $info ) {
            if ( is_plugin_active( $plugin_path ) ) {
                $conflicts[ $plugin_path ] = $info;
            }
        }

        return $conflicts;
    }

    /**
     * Display conflict warnings in admin.
     */
    public static function display_conflict_notices() {
        $conflicts = self::check_conflicts();

        if ( empty( $conflicts ) ) {
            return;
        }

        add_action( 'admin_notices', function() use ( $conflicts ) {
            ?>
            <div class="notice notice-warning is-dismissible">
                <p>
                    <strong><?php esc_html_e( 'Plugin Name - Potential Conflicts Detected:', 'plugin-name' ); ?></strong>
                </p>
                <?php foreach ( $conflicts as $path => $info ) : ?>
                    <p>
                        <strong><?php echo esc_html( $info['name'] ); ?>:</strong>
                        <?php echo esc_html( $info['reason'] ); ?>
                        <br>
                        <em><?php esc_html_e( 'Resolution:', 'plugin-name' ); ?></em>
                        <?php echo esc_html( $info['resolve'] ); ?>
                    </p>
                <?php endforeach; ?>
            </div>
            <?php
        });
    }

    /**
     * Check for JavaScript conflicts.
     */
    public static function check_js_conflicts() {
        add_action( 'admin_footer', function() {
            if ( ! current_user_can( 'manage_options' ) || ! defined( 'WP_DEBUG' ) || ! WP_DEBUG ) {
                return;
            }
            ?>
            <script>
            jQuery(document).ready(function($) {
                // Check for common JS conflicts
                var conflicts = [];

                // Check if jQuery is loaded multiple times
                if (window.jQuery && window.jQuery.fn.jquery !== $.fn.jquery) {
                    conflicts.push('Multiple jQuery versions detected');
                }

                // Check for undefined required globals
                var required = ['wp', 'wpApiSettings'];
                required.forEach(function(global) {
                    if (typeof window[global] === 'undefined') {
                        conflicts.push('Missing global: ' + global);
                    }
                });

                // Log conflicts
                if (conflicts.length > 0) {
                    console.warn('[Plugin Name] Potential JS conflicts:', conflicts);
                }
            });
            </script>
            <?php
        });
    }
}

// Initialize conflict checking
add_action( 'admin_init', array( 'Plugin_Name_Conflict_Checker', 'display_conflict_notices' ) );
add_action( 'admin_init', array( 'Plugin_Name_Conflict_Checker', 'check_js_conflicts' ) );
```

### Hook Conflict Detection

```php
<?php
/**
 * Detect hook conflicts and priority issues.
 */

class Plugin_Name_Hook_Debug {

    /**
     * Log all hooks for a specific tag.
     *
     * @param string $tag Hook tag to inspect.
     */
    public static function inspect_hook( $tag ) {
        global $wp_filter;

        if ( ! isset( $wp_filter[ $tag ] ) ) {
            error_log( sprintf( '[Plugin Name] Hook "%s" has no callbacks', $tag ) );
            return;
        }

        $callbacks = $wp_filter[ $tag ]->callbacks;

        error_log( sprintf( '[Plugin Name] Hook "%s" callbacks:', $tag ) );

        foreach ( $callbacks as $priority => $hooks ) {
            foreach ( $hooks as $id => $hook ) {
                $callback = $hook['function'];

                // Get callback name
                if ( is_array( $callback ) ) {
                    if ( is_object( $callback[0] ) ) {
                        $name = get_class( $callback[0] ) . '->' . $callback[1];
                    } else {
                        $name = $callback[0] . '::' . $callback[1];
                    }
                } elseif ( is_string( $callback ) ) {
                    $name = $callback;
                } else {
                    $name = 'closure';
                }

                error_log( sprintf(
                    '  Priority %d: %s (args: %d)',
                    $priority,
                    $name,
                    $hook['accepted_args']
                ) );
            }
        }
    }

    /**
     * Find plugins that hook into a specific action/filter.
     *
     * @param string $tag Hook tag.
     * @return array Plugins using this hook.
     */
    public static function find_hook_users( $tag ) {
        global $wp_filter;

        $users = array();

        if ( ! isset( $wp_filter[ $tag ] ) ) {
            return $users;
        }

        foreach ( $wp_filter[ $tag ]->callbacks as $priority => $hooks ) {
            foreach ( $hooks as $hook ) {
                $callback = $hook['function'];

                // Try to determine source
                if ( is_array( $callback ) && is_object( $callback[0] ) ) {
                    $reflection = new ReflectionClass( $callback[0] );
                    $file = $reflection->getFileName();
                } elseif ( is_array( $callback ) && is_string( $callback[0] ) ) {
                    $reflection = new ReflectionMethod( $callback[0], $callback[1] );
                    $file = $reflection->getFileName();
                } elseif ( is_string( $callback ) && function_exists( $callback ) ) {
                    $reflection = new ReflectionFunction( $callback );
                    $file = $reflection->getFileName();
                } else {
                    continue;
                }

                // Determine if it's a plugin
                if ( strpos( $file, 'wp-content/plugins/' ) !== false ) {
                    preg_match( '/wp-content\/plugins\/([^\/]+)/', $file, $matches );
                    if ( ! empty( $matches[1] ) ) {
                        $users[] = array(
                            'plugin'   => $matches[1],
                            'priority' => $priority,
                            'file'     => $file,
                        );
                    }
                }
            }
        }

        return $users;
    }
}

// Debug usage
if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
    add_action( 'wp_loaded', function() {
        // Inspect hooks your plugin uses
        Plugin_Name_Hook_Debug::inspect_hook( 'woocommerce_checkout_process' );
    });
}
```

---

## Common Debugging Scenarios

### AJAX Debugging

```php
<?php
/**
 * Debug AJAX requests.
 */

// Add debugging to AJAX handlers
add_action( 'wp_ajax_my_action', function() {
    // Log incoming request
    if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
        error_log( 'AJAX Request: ' . print_r( $_POST, true ) );
    }

    // Validate
    if ( ! wp_verify_nonce( $_POST['nonce'], 'my_action' ) ) {
        error_log( 'AJAX Error: Invalid nonce' );
        wp_send_json_error( 'Invalid nonce' );
    }

    // Process...
    $result = process_data( $_POST );

    // Log response
    if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
        error_log( 'AJAX Response: ' . print_r( $result, true ) );
    }

    wp_send_json_success( $result );
});

// JavaScript debugging
add_action( 'admin_footer', function() {
    if ( ! defined( 'WP_DEBUG' ) || ! WP_DEBUG ) {
        return;
    }
    ?>
    <script>
    (function($) {
        // Intercept all AJAX calls for debugging
        $(document).ajaxSend(function(event, jqxhr, settings) {
            console.group('AJAX Request');
            console.log('URL:', settings.url);
            console.log('Type:', settings.type);
            console.log('Data:', settings.data);
            console.groupEnd();
        });

        $(document).ajaxComplete(function(event, jqxhr, settings) {
            console.group('AJAX Response');
            console.log('URL:', settings.url);
            console.log('Status:', jqxhr.status);
            console.log('Response:', jqxhr.responseJSON || jqxhr.responseText);
            console.groupEnd();
        });

        $(document).ajaxError(function(event, jqxhr, settings, error) {
            console.error('AJAX Error:', {
                url: settings.url,
                status: jqxhr.status,
                error: error,
                response: jqxhr.responseText
            });
        });
    })(jQuery);
    </script>
    <?php
});
```

### REST API Debugging

```php
<?php
/**
 * Debug REST API requests.
 */

add_filter( 'rest_pre_dispatch', function( $result, $server, $request ) {
    if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
        error_log( sprintf(
            'REST Request: %s %s',
            $request->get_method(),
            $request->get_route()
        ));
        error_log( 'REST Params: ' . print_r( $request->get_params(), true ) );
    }
    return $result;
}, 10, 3 );

add_filter( 'rest_post_dispatch', function( $response, $server, $request ) {
    if ( defined( 'WP_DEBUG' ) && WP_DEBUG ) {
        error_log( sprintf(
            'REST Response: %s %s - Status: %d',
            $request->get_method(),
            $request->get_route(),
            $response->get_status()
        ));
    }
    return $response;
}, 10, 3 );
```

### Database Query Debugging

```php
<?php
/**
 * Debug database queries.
 */

add_action( 'shutdown', function() {
    if ( ! defined( 'SAVEQUERIES' ) || ! SAVEQUERIES ) {
        return;
    }

    global $wpdb;

    // Filter to only your plugin's queries
    $plugin_queries = array_filter( $wpdb->queries, function( $query ) {
        return strpos( $query[2], 'plugin_name' ) !== false ||
               strpos( $query[0], 'plugin_name' ) !== false;
    });

    if ( empty( $plugin_queries ) ) {
        return;
    }

    error_log( '=== Plugin Name Database Queries ===' );

    $total_time = 0;
    foreach ( $plugin_queries as $query ) {
        error_log( sprintf(
            "Query: %s\nTime: %.4fs\nCaller: %s\n",
            $query[0],
            $query[1],
            $query[2]
        ));
        $total_time += $query[1];
    }

    error_log( sprintf(
        'Total: %d queries, %.4fs',
        count( $plugin_queries ),
        $total_time
    ));
});
```

---

## Debugging Checklist

### Before Debugging

- [ ] Enable WP_DEBUG in wp-config.php
- [ ] Enable WP_DEBUG_LOG
- [ ] Install Query Monitor plugin
- [ ] Clear all caches
- [ ] Disable caching plugins temporarily

### Common Issues

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| White screen | PHP fatal error | Check debug.log |
| 500 error | Server/PHP error | Check server error logs |
| AJAX fails | Nonce/permission | Log AJAX data |
| Styles broken | Caching | Clear cache, check priority |
| Plugin conflict | Hook priority | Check hook order |
| Memory exhausted | Too much data | Increase memory limit |
| Timeout | Slow queries | Profile with SAVEQUERIES |

### Useful WP-CLI Commands

```bash
# Check WordPress configuration
wp config list

# Check active plugins
wp plugin list --status=active

# Check for PHP errors
wp eval "error_reporting(E_ALL); ini_set('display_errors', 1);"

# Verify plugin dependencies
wp plugin verify-checksums plugin-name

# Test REST API
wp rest GET /wp/v2/posts

# Clear transients
wp transient delete --all

# Check cron events
wp cron event list

# Debug mode toggle
wp config set WP_DEBUG true --raw
wp config set WP_DEBUG_LOG true --raw
```

### Debug Log Analysis

```bash
# View recent log entries
tail -f wp-content/debug.log

# Search for specific errors
grep -i "fatal error" wp-content/debug.log

# Search for plugin-specific logs
grep "Plugin Name" wp-content/debug.log

# Count errors by type
grep -oP '\[\w+\]' wp-content/debug.log | sort | uniq -c

# Clear debug log
> wp-content/debug.log
```
