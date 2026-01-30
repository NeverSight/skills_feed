---
name: wp-security
description: WordPress security best practices and vulnerability prevention for plugin development. Use when reviewing code for security issues or implementing security-sensitive features.
---

# WordPress Security Best Practices

## OWASP Top 10 for WordPress

### 1. SQL Injection Prevention
```php
// WRONG - Never do this
$wpdb->query( "SELECT * FROM table WHERE id = " . $_GET['id'] );

// CORRECT - Always use prepare()
$wpdb->get_results( $wpdb->prepare(
    "SELECT * FROM {$wpdb->prefix}table WHERE id = %d",
    absint( $_GET['id'] )
) );
```

### 2. Cross-Site Scripting (XSS) Prevention
```php
// Escape all output
echo esc_html( $user_input );
echo '<a href="' . esc_url( $url ) . '">' . esc_html( $text ) . '</a>';
echo '<input value="' . esc_attr( $value ) . '" />';

// For allowed HTML
echo wp_kses_post( $content );

// For custom allowed tags
$allowed_html = array(
    'a' => array(
        'href'  => array(),
        'title' => array(),
    ),
);
echo wp_kses( $content, $allowed_html );
```

### 3. Cross-Site Request Forgery (CSRF) Prevention
```php
// Form protection
<form method="post">
    <?php wp_nonce_field( 'my_action', 'my_nonce' ); ?>
    <!-- form fields -->
</form>

// Verification
if ( ! isset( $_POST['my_nonce'] ) ||
     ! wp_verify_nonce( $_POST['my_nonce'], 'my_action' ) ) {
    wp_die( __( 'Security check failed', 'text-domain' ) );
}

// AJAX nonce
wp_localize_script( 'my-script', 'myAjax', array(
    'nonce' => wp_create_nonce( 'my-ajax-nonce' ),
) );

// AJAX verification
check_ajax_referer( 'my-ajax-nonce', 'nonce' );
```

### 4. Authentication and Authorization
```php
// Always check capabilities
if ( ! current_user_can( 'manage_options' ) ) {
    wp_die( __( 'Unauthorized access', 'text-domain' ) );
}

// Check user owns resource
if ( get_current_user_id() !== $post->post_author &&
     ! current_user_can( 'edit_others_posts' ) ) {
    wp_die( __( 'Unauthorized', 'text-domain' ) );
}

// For AJAX
if ( ! is_user_logged_in() ) {
    wp_send_json_error( 'Not logged in' );
}
```

### 5. Sensitive Data Exposure
```php
// Never output sensitive data
// Use constants in wp-config.php
define( 'MY_API_KEY', 'secret_key' );

// Store securely
update_option( 'prefix_api_key', sanitize_text_field( $_POST['api_key'] ), 'no' );

// Never log sensitive data
if ( WP_DEBUG ) {
    error_log( 'Error occurred' ); // Don't log passwords, API keys, etc.
}
```

### 6. File Upload Security
```php
// Validate file type
$allowed_types = array( 'image/jpeg', 'image/png' );
$file_type = wp_check_filetype( $_FILES['file']['name'] );

if ( ! in_array( $file_type['type'], $allowed_types, true ) ) {
    wp_die( __( 'Invalid file type', 'text-domain' ) );
}

// Use WordPress upload functions
$upload = wp_handle_upload( $_FILES['file'], array(
    'test_form' => false,
    'mimes'     => array( 'jpg|jpeg|png' => 'image/jpeg' ),
) );

// Validate file size
if ( $_FILES['file']['size'] > 5000000 ) { // 5MB
    wp_die( __( 'File too large', 'text-domain' ) );
}
```

### 7. Directory Traversal Prevention
```php
// Validate paths
$file = basename( $_GET['file'] ); // Remove directory components
$file_path = plugin_dir_path( __FILE__ ) . 'uploads/' . $file;

// Verify file is within allowed directory
$real_path = realpath( $file_path );
$allowed_dir = realpath( plugin_dir_path( __FILE__ ) . 'uploads/' );

if ( strpos( $real_path, $allowed_dir ) !== 0 ) {
    wp_die( __( 'Invalid file path', 'text-domain' ) );
}
```

## Input Sanitization Cheat Sheet

```php
// Text input
sanitize_text_field( $_POST['text'] );

// Textarea
sanitize_textarea_field( $_POST['textarea'] );

// Email
sanitize_email( $_POST['email'] );

// URL
esc_url_raw( $_POST['url'] ); // For database
esc_url( $url );              // For output

// Filename
sanitize_file_name( $_FILES['file']['name'] );

// HTML class
sanitize_html_class( $_POST['class'] );

// Key (alphanumeric, dashes, underscores)
sanitize_key( $_POST['key'] );

// Integer
absint( $_POST['id'] );        // Positive integer
intval( $_POST['number'] );    // Any integer

// HTML content
wp_kses_post( $_POST['content'] );

// Array of integers
array_map( 'absint', $_POST['ids'] );
```

## Output Escaping Cheat Sheet

```php
// HTML content
esc_html( $text );
esc_html__( 'Text', 'text-domain' );  // With translation
esc_html_e( 'Text', 'text-domain' );  // Echo with translation

// HTML attributes
esc_attr( $attribute );

// URLs
esc_url( $url );

// JavaScript
esc_js( $js_string );

// SQL (with $wpdb->prepare)
$wpdb->prepare( "SELECT * FROM table WHERE id = %d AND name = %s", $id, $name );

// Textarea
esc_textarea( $text );

// Allowed HTML
wp_kses_post( $content );
```

## REST API Security

```php
add_action( 'rest_api_init', 'prefix_register_secure_route' );

function prefix_register_secure_route() {
    register_rest_route( 'plugin/v1', '/secure-endpoint', array(
        'methods'             => WP_REST_Server::CREATABLE,
        'callback'            => 'prefix_secure_callback',
        'permission_callback' => 'prefix_secure_permission_check',
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
}

function prefix_secure_permission_check( $request ) {
    // Verify nonce for logged-in users
    if ( ! current_user_can( 'edit_posts' ) ) {
        return new WP_Error(
            'rest_forbidden',
            __( 'You do not have permission', 'text-domain' ),
            array( 'status' => 403 )
        );
    }
    return true;
}
```

## File Access Protection

```php
// Add to index.php in plugin directories
<?php
// Silence is golden.

// Or prevent direct access in all PHP files
if ( ! defined( 'ABSPATH' ) ) {
    exit; // Exit if accessed directly
}
```

## Secure AJAX Handlers

```php
// Register AJAX handler
add_action( 'wp_ajax_my_action', 'prefix_ajax_handler' );
add_action( 'wp_ajax_nopriv_my_action', 'prefix_ajax_handler' ); // For logged-out users

function prefix_ajax_handler() {
    // Verify nonce
    check_ajax_referer( 'my-ajax-nonce', 'nonce' );

    // Check capabilities
    if ( ! current_user_can( 'edit_posts' ) ) {
        wp_send_json_error( 'Unauthorized' );
    }

    // Sanitize input
    $data = sanitize_text_field( $_POST['data'] );

    // Process and return
    wp_send_json_success( array( 'result' => $data ) );
}
```

## Security Headers

```php
// Add security headers
add_action( 'send_headers', 'prefix_add_security_headers' );

function prefix_add_security_headers() {
    header( 'X-Content-Type-Options: nosniff' );
    header( 'X-Frame-Options: SAMEORIGIN' );
    header( 'X-XSS-Protection: 1; mode=block' );
    header( 'Referrer-Policy: strict-origin-when-cross-origin' );
}
```

## Common Vulnerability Patterns to Avoid

1. **Trusting user input** - Always sanitize and validate
2. **Direct file includes** - Validate file paths
3. **Unprotected AJAX** - Always verify nonce and capabilities
4. **SQL concatenation** - Always use `$wpdb->prepare()`
5. **Missing output escaping** - Escape everything
6. **Weak nonce checks** - Always verify before processing
7. **Missing capability checks** - Check permissions
8. **Exposed error messages** - Don't reveal system information
9. **Unvalidated redirects** - Use `wp_safe_redirect()`
10. **Hardcoded secrets** - Use constants and environment variables