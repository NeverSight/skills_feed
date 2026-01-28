---
name: wp-security-review
description: WordPress security audit and vulnerability analysis. Use when reviewing WordPress code for security issues, auditing themes/plugins for vulnerabilities, checking authentication/authorization, analyzing input validation, or detecting security anti-patterns, or when user mentions "security review", "security audit", "vulnerability", "XSS", "SQL injection", "CSRF", "nonce", "sanitize", "escape", "validate", "authentication", "authorization", "permissions", "capabilities", "hacked", or "malware".
---

# WordPress Security Review Skill

## Overview

Systematic security code review for WordPress themes, plugins, and custom code. **Core principle:** Scan for critical vulnerabilities first (SQL injection, XSS, authentication bypass), then authorization issues, then hardening opportunities. Report with line numbers and severity levels.

## When to Use

**Use when:**
- Reviewing PR/code for WordPress theme or plugin security
- User reports suspected hack, malware, or security breach
- Auditing before public release or security certification
- Checking authentication, authorization, or capability checks
- Investigating suspicious code or backdoors

**Don't use for:**
- Performance-only reviews (use wp-performance-review)
- General PHP code review not specific to WordPress
- Server/infrastructure security (focus is on code)

## Code Review Workflow

1. **Identify file type** and apply relevant checks below
2. **Scan for critical vulnerabilities first** (SQLi, XSS, RCE, auth bypass)
3. **Check authorization issues** (missing capability checks, IDOR)
4. **Note hardening opportunities** (security headers, configuration)
5. **Report with line numbers** using output format below

## OWASP Top 10 WordPress Mapping

| OWASP Risk | WordPress Manifestation |
|------------|------------------------|
| A01 Broken Access Control | Missing `current_user_can()`, direct file access, IDOR |
| A02 Cryptographic Failures | Weak hashing, exposed secrets, insecure cookies |
| A03 Injection | SQL injection, XSS, command injection, LDAP injection |
| A04 Insecure Design | Logic flaws, race conditions, predictable tokens |
| A05 Security Misconfiguration | Debug enabled, directory listing, default credentials |
| A06 Vulnerable Components | Outdated plugins, known CVEs, abandoned libraries |
| A07 Auth Failures | Weak passwords, session fixation, brute force |
| A08 Data Integrity Failures | Insecure deserialization, missing integrity checks |
| A09 Logging Failures | Missing audit trails, excessive error exposure |
| A10 SSRF | Unvalidated URLs in `wp_remote_get()`, redirects |

## File-Type Specific Checks

### Plugin/Theme PHP Files (`functions.php`, `plugin.php`, `*.php`)
Scan for:
- `$_GET`, `$_POST`, `$_REQUEST` without sanitization → CRITICAL: Input validation
- `$wpdb->query()` with string concatenation → CRITICAL: SQL injection
- `echo`, `print` without escaping → CRITICAL: XSS vulnerability
- Missing `wp_verify_nonce()` in form handlers → CRITICAL: CSRF
- Missing `current_user_can()` before privileged actions → CRITICAL: Auth bypass
- `eval()`, `assert()`, `create_function()` → CRITICAL: Code execution
- `unserialize()` with user input → CRITICAL: Object injection
- `include`, `require` with user input → CRITICAL: LFI/RFI

### Database Operations
Scan for:
- `$wpdb->prepare()` not used with variables → CRITICAL: SQL injection
- `esc_sql()` used instead of `prepare()` → WARNING: Prefer prepare()
- `LIKE` queries without `$wpdb->esc_like()` → WARNING: Wildcard injection
- Direct table creation without `dbDelta()` → INFO: Schema management

### AJAX & REST Handlers
Scan for:
- `wp_ajax_nopriv_*` without rate limiting → WARNING: Abuse potential
- Missing `permission_callback` in REST routes → CRITICAL: Auth bypass
- `'permission_callback' => '__return_true'` → WARNING: Public endpoint
- Missing nonce in AJAX actions → CRITICAL: CSRF vulnerability

### File Operations
Scan for:
- `file_get_contents()`, `file_put_contents()` with user paths → CRITICAL: Path traversal
- `move_uploaded_file()` without validation → CRITICAL: Arbitrary upload
- Missing MIME type validation → WARNING: Upload bypass
- `unlink()`, `rmdir()` with user input → CRITICAL: Arbitrary deletion

### Authentication & Sessions
Scan for:
- Custom authentication instead of `wp_authenticate()` → WARNING: Security bypass
- `wp_set_auth_cookie()` without proper validation → CRITICAL: Auth bypass
- Session handling outside WordPress → WARNING: Session fixation
- Plain text password storage → CRITICAL: Credential exposure

### External Requests
Scan for:
- `wp_remote_get()` with user-supplied URL → CRITICAL: SSRF
- Missing URL validation before requests → WARNING: SSRF potential
- `allow_redirects => true` with external URLs → WARNING: Open redirect

### Cron & Scheduled Tasks
Scan for:
- Cron hook name same as internal `do_action()` in callback → CRITICAL: Infinite recursion (DoS)
- `wp_schedule_event()` without `wp_next_scheduled()` check → WARNING: Duplicate events
- Missing `wp_clear_scheduled_hook()` on deactivation → WARNING: Orphaned events
- Long-running cron without `set_time_limit()` → WARNING: Timeout issues
- Cron callbacks without try-catch → WARNING: Silent failures

**Detection pattern for infinite recursion:**
```php
// Check if any cron hook name matches a do_action() call in its callback
// Example: wp_schedule_event( time(), 'hourly', 'my_hook' );
//          add_action( 'my_hook', 'callback' );
//          function callback() { do_action( 'my_hook' ); } // INFINITE LOOP!
```

## Search Patterns for Quick Detection

```bash
# Critical: SQL Injection patterns
grep -rn '\$wpdb->query\s*(' . | grep -v 'prepare'
grep -rn '\$wpdb->get_' . | grep -v 'prepare'
grep -rn "esc_sql\s*(" .

# Critical: XSS patterns (unescaped output)
grep -rn 'echo\s*\$_' .
grep -rn 'print\s*\$_' .
grep -rn '<?=\s*\$' . | grep -v 'esc_'

# Critical: Missing nonce verification
grep -rn 'wp_ajax_' . | grep -l 'wp_ajax' | xargs grep -L 'wp_verify_nonce\|check_ajax_referer'

# Critical: Dangerous functions
grep -rn '\beval\s*(' .
grep -rn '\bassert\s*(' .
grep -rn 'create_function\s*(' .
grep -rn 'unserialize\s*(' .
grep -rn 'call_user_func.*\$_' .

# Critical: File inclusion vulnerabilities
grep -rn 'include.*\$_\|require.*\$_' .
grep -rn 'file_get_contents.*\$_' .

# Critical: Missing capability checks
grep -rn 'update_option\|delete_option' . | grep -v 'current_user_can'
grep -rn 'wp_delete_post\|wp_update_post' . | grep -v 'current_user_can'

# Warning: Unsafe input usage
grep -rn '\$_GET\[' . | grep -v 'sanitize_\|esc_\|intval\|absint'
grep -rn '\$_POST\[' . | grep -v 'sanitize_\|esc_\|intval\|absint'

# Warning: REST API without permissions
grep -rn 'register_rest_route' . | grep -v 'permission_callback'
grep -rn '__return_true.*permission_callback\|permission_callback.*__return_true' .

# Info: Debug/development code left in
grep -rn 'WP_DEBUG.*true' .
grep -rn 'error_reporting\|display_errors' .
grep -rn 'var_dump\|print_r\|debug_backtrace' .
```

## Quick Reference: Security Anti-Patterns

### SQL Injection

```php
// ❌ CRITICAL: SQL injection via string concatenation.
$results = $wpdb->get_results(
    "SELECT * FROM {$wpdb->posts} WHERE post_title = '$title'"
);

// ❌ CRITICAL: SQL injection via sprintf (still vulnerable).
$results = $wpdb->get_results(
    sprintf( "SELECT * FROM %s WHERE ID = %s", $wpdb->posts, $id )
);

// ✅ GOOD: Use $wpdb->prepare() for all variable data.
$results = $wpdb->get_results(
    $wpdb->prepare(
        "SELECT * FROM {$wpdb->posts} WHERE post_title = %s",
        $title
    )
);

// ❌ WARNING: esc_sql() is not sufficient for complex queries.
$title = esc_sql( $_GET['title'] );
$wpdb->query( "SELECT * FROM wp_posts WHERE post_title = '$title'" );

// ✅ GOOD: Always use prepare(), even for "safe" looking queries.
$wpdb->get_var(
    $wpdb->prepare(
        "SELECT COUNT(*) FROM {$wpdb->posts} WHERE post_author = %d",
        $user_id
    )
);

// ❌ WARNING: LIKE queries need esc_like() in addition to prepare().
$wpdb->prepare( "SELECT * FROM {$wpdb->posts} WHERE post_title LIKE %s", '%' . $search . '%' );

// ✅ GOOD: Use esc_like() for LIKE wildcards.
$wpdb->prepare(
    "SELECT * FROM {$wpdb->posts} WHERE post_title LIKE %s",
    '%' . $wpdb->esc_like( $search ) . '%'
);
```

### Cross-Site Scripting (XSS)

```php
// ❌ CRITICAL: Unescaped output - XSS vulnerability.
echo $_GET['search'];
echo $user_input;
echo $post->post_title; // Even "safe" data should be escaped.

// ✅ GOOD: Always escape output based on context.
echo esc_html( $_GET['search'] );           // HTML context.
echo esc_attr( $value );                     // HTML attributes.
echo esc_url( $url );                        // URLs.
echo esc_js( $string );                      // JavaScript strings.
echo wp_kses_post( $content );              // Allow safe HTML.

// ❌ CRITICAL: Unescaped in HTML attribute.
<input value="<?php echo $value; ?>">

// ✅ GOOD: Escape for attribute context.
<input value="<?php echo esc_attr( $value ); ?>">

// ❌ CRITICAL: Unescaped URL - JavaScript injection.
<a href="<?php echo $url; ?>">Link</a>

// ✅ GOOD: Validate and escape URLs.
<a href="<?php echo esc_url( $url ); ?>">Link</a>

// ❌ WARNING: wp_kses_post() in wrong context.
<input value="<?php echo wp_kses_post( $value ); ?>">

// ✅ GOOD: Use appropriate escaping for context.
<input value="<?php echo esc_attr( wp_strip_all_tags( $value ) ); ?>">

// ❌ CRITICAL: JSON output without escaping.
<script>var data = <?php echo json_encode( $data ); ?>;</script>

// ✅ GOOD: Use wp_json_encode() and proper escaping.
<script>var data = <?php echo wp_json_encode( $data ); ?>;</script>
```

### Cross-Site Request Forgery (CSRF)

```php
// ❌ CRITICAL: Form without nonce - CSRF vulnerable.
<form method="post" action="">
    <input type="submit" value="Delete">
</form>
<?php
if ( isset( $_POST['submit'] ) ) {
    delete_data();
}

// ✅ GOOD: Add nonce field and verify on submission.
<form method="post" action="">
    <?php wp_nonce_field( 'delete_action', 'delete_nonce' ); ?>
    <input type="submit" name="submit" value="Delete">
</form>
<?php
if ( isset( $_POST['submit'] ) ) {
    if ( ! wp_verify_nonce( $_POST['delete_nonce'], 'delete_action' ) ) {
        wp_die( 'Security check failed' );
    }
    delete_data();
}

// ❌ CRITICAL: AJAX handler without nonce verification.
add_action( 'wp_ajax_delete_item', 'handle_delete' );
function handle_delete() {
    $id = intval( $_POST['id'] );
    wp_delete_post( $id );
    wp_die();
}

// ✅ GOOD: Verify nonce in AJAX handlers.
add_action( 'wp_ajax_delete_item', 'handle_delete' );
function handle_delete() {
    check_ajax_referer( 'delete_item_nonce', 'security' );

    if ( ! current_user_can( 'delete_posts' ) ) {
        wp_send_json_error( 'Unauthorized' );
    }

    $id = intval( $_POST['id'] );
    wp_delete_post( $id );
    wp_send_json_success();
}
```

### Authorization & Capability Checks

```php
// ❌ CRITICAL: No capability check before privileged action.
function delete_all_posts() {
    $wpdb->query( "TRUNCATE TABLE {$wpdb->posts}" );
}

// ✅ GOOD: Always verify capabilities.
function delete_all_posts() {
    if ( ! current_user_can( 'manage_options' ) ) {
        wp_die( 'Unauthorized access' );
    }
    // ... proceed with action.
}

// ❌ CRITICAL: Checking wrong capability.
if ( current_user_can( 'read' ) ) {
    update_option( 'critical_setting', $value );
}

// ✅ GOOD: Use appropriate capability for the action.
if ( current_user_can( 'manage_options' ) ) {
    update_option( 'critical_setting', $value );
}

// ❌ CRITICAL: IDOR - no ownership verification.
function get_user_data() {
    $user_id = intval( $_GET['user_id'] );
    return get_user_meta( $user_id, 'private_data', true );
}

// ✅ GOOD: Verify the user owns the resource or has permission.
function get_user_data() {
    $user_id = intval( $_GET['user_id'] );

    if ( get_current_user_id() !== $user_id && ! current_user_can( 'edit_users' ) ) {
        wp_die( 'Unauthorized access' );
    }

    return get_user_meta( $user_id, 'private_data', true );
}

// ❌ WARNING: REST endpoint with no permission check.
register_rest_route( 'myplugin/v1', '/data', array(
    'methods'  => 'GET',
    'callback' => 'get_sensitive_data',
) );

// ✅ GOOD: Always define permission_callback.
register_rest_route( 'myplugin/v1', '/data', array(
    'methods'             => 'GET',
    'callback'            => 'get_sensitive_data',
    'permission_callback' => function() {
        return current_user_can( 'edit_posts' );
    },
) );
```

### Input Validation & Sanitization

```php
// ❌ CRITICAL: Using raw input directly.
$email = $_POST['email'];
$name  = $_GET['name'];

// ✅ GOOD: Sanitize all input based on expected type.
$email = sanitize_email( $_POST['email'] );
$name  = sanitize_text_field( $_GET['name'] );
$html  = wp_kses_post( $_POST['content'] );
$int   = absint( $_GET['id'] );
$url   = esc_url_raw( $_POST['website'] );

// ❌ WARNING: Sanitizing but not validating.
$email = sanitize_email( $_POST['email'] );
update_user_meta( $user_id, 'email', $email );

// ✅ GOOD: Validate after sanitizing.
$email = sanitize_email( $_POST['email'] );
if ( ! is_email( $email ) ) {
    wp_die( 'Invalid email address' );
}
update_user_meta( $user_id, 'email', $email );

// ❌ CRITICAL: Trusting hidden form fields.
$user_role = $_POST['user_role']; // User can modify this!

// ✅ GOOD: Validate against allowed values.
$allowed_roles = array( 'subscriber', 'contributor' );
$user_role     = sanitize_text_field( $_POST['user_role'] );
if ( ! in_array( $user_role, $allowed_roles, true ) ) {
    wp_die( 'Invalid role' );
}

// ❌ WARNING: Using sanitize_text_field for file paths.
$file = sanitize_text_field( $_GET['file'] );
include $file;

// ✅ GOOD: Validate file paths against whitelist.
$allowed_files = array( 'header.php', 'footer.php' );
$file          = basename( $_GET['file'] ); // Strip path traversal.
if ( ! in_array( $file, $allowed_files, true ) ) {
    wp_die( 'Invalid file' );
}
include get_template_directory() . '/' . $file;
```

### File Upload Security

```php
// ❌ CRITICAL: No validation on file upload.
$target = wp_upload_dir()['path'] . '/' . $_FILES['file']['name'];
move_uploaded_file( $_FILES['file']['tmp_name'], $target );

// ✅ GOOD: Use WordPress upload handling with validation.
$allowed_types = array( 'image/jpeg', 'image/png', 'image/gif' );

// Verify MIME type.
$file_type = wp_check_filetype( $_FILES['file']['name'] );
if ( ! in_array( $file_type['type'], $allowed_types, true ) ) {
    wp_die( 'Invalid file type' );
}

// Use WordPress media handling.
require_once ABSPATH . 'wp-admin/includes/file.php';
require_once ABSPATH . 'wp-admin/includes/media.php';
require_once ABSPATH . 'wp-admin/includes/image.php';

$attachment_id = media_handle_upload( 'file', 0 );
if ( is_wp_error( $attachment_id ) ) {
    wp_die( $attachment_id->get_error_message() );
}

// ❌ CRITICAL: Extension-only check (bypassable).
$ext = pathinfo( $_FILES['file']['name'], PATHINFO_EXTENSION );
if ( $ext === 'jpg' ) {
    // Allows "malware.php.jpg" renamed to "malware.php".
}

// ✅ GOOD: Check both extension and MIME type.
$file_info    = wp_check_filetype_and_ext(
    $_FILES['file']['tmp_name'],
    $_FILES['file']['name']
);
$allowed_mimes = array( 'jpg|jpeg|jpe' => 'image/jpeg' );
if ( ! in_array( $file_info['type'], $allowed_mimes, true ) ) {
    wp_die( 'Invalid file' );
}
```

### Dangerous Functions

```php
// ❌ CRITICAL: Code execution via eval().
eval( $_POST['code'] );

// ❌ CRITICAL: Code execution via assert().
assert( $_GET['assertion'] );

// ❌ CRITICAL: Deprecated and dangerous.
create_function( '$a', $_POST['code'] );

// ❌ CRITICAL: Object injection via unserialize().
$data = unserialize( $_COOKIE['data'] );

// ✅ GOOD: Use JSON for data serialization.
$data = json_decode( $_COOKIE['data'], true );
if ( json_last_error() !== JSON_ERROR_NONE ) {
    $data = array();
}

// ❌ CRITICAL: Command injection.
system( 'ls ' . $_GET['dir'] );
exec( $_POST['command'] );
shell_exec( $user_input );
passthru( $command );

// ✅ GOOD: Avoid shell commands; if necessary, escape properly.
$safe_dir = escapeshellarg( $dir );
$output   = shell_exec( "ls $safe_dir" );

// ❌ CRITICAL: Dynamic function calls with user input.
$func = $_GET['callback'];
$func(); // Arbitrary function execution!
call_user_func( $_POST['function'], $args );

// ✅ GOOD: Whitelist allowed functions.
$allowed_callbacks = array(
    'format_date'   => 'my_format_date',
    'format_number' => 'my_format_number',
);
$callback_key = sanitize_key( $_GET['callback'] );
if ( isset( $allowed_callbacks[ $callback_key ] ) ) {
    call_user_func( $allowed_callbacks[ $callback_key ], $args );
}
```

### Server-Side Request Forgery (SSRF)

```php
// ❌ CRITICAL: SSRF - user controls URL destination.
$url      = $_GET['url'];
$response = wp_remote_get( $url );

// ✅ GOOD: Validate URL against whitelist.
$url         = esc_url_raw( $_GET['url'] );
$allowed     = array( 'api.example.com', 'cdn.example.com' );
$parsed_host = wp_parse_url( $url, PHP_URL_HOST );

if ( ! in_array( $parsed_host, $allowed, true ) ) {
    wp_die( 'URL not allowed' );
}

$response = wp_remote_get( $url, array(
    'timeout'     => 5,
    'redirection' => 0, // Disable redirects to prevent bypass.
) );

// ❌ WARNING: Allowing redirects can bypass host validation.
wp_remote_get( $url, array( 'redirection' => 5 ) );

// ✅ GOOD: Disable redirects or re-validate after redirect.
wp_remote_get( $url, array( 'redirection' => 0 ) );
```

### Information Disclosure

```php
// ❌ WARNING: Exposing debug info in production.
if ( WP_DEBUG ) {
    echo $wpdb->last_query;
    echo $wpdb->last_error;
}

// ✅ GOOD: Log errors instead of displaying.
if ( WP_DEBUG ) {
    error_log( $wpdb->last_error );
}

// ❌ WARNING: Exposing full paths.
wp_die( 'Error in ' . __FILE__ );

// ✅ GOOD: Generic error messages.
wp_die( 'An error occurred. Please try again.' );

// ❌ WARNING: Version exposure in headers/source.
<meta name="generator" content="WordPress <?php bloginfo( 'version' ); ?>">

// ✅ GOOD: Remove version information.
remove_action( 'wp_head', 'wp_generator' );

// ❌ WARNING: Exposing user enumeration.
// Accessible: /?author=1 redirects to /author/admin/

// ✅ GOOD: Block user enumeration.
add_action( 'template_redirect', function() {
    if ( isset( $_GET['author'] ) && ! is_admin() ) {
        wp_redirect( home_url(), 301 );
        exit;
    }
} );
```

### Secure Cookies & Sessions

```php
// ❌ WARNING: Cookie without security flags.
setcookie( 'user_pref', $value );

// ✅ GOOD: Set secure cookie flags.
setcookie(
    'user_pref',
    $value,
    array(
        'expires'  => time() + DAY_IN_SECONDS,
        'path'     => COOKIEPATH,
        'domain'   => COOKIE_DOMAIN,
        'secure'   => is_ssl(),
        'httponly' => true,
        'samesite' => 'Strict',
    )
);

// ❌ CRITICAL: Storing sensitive data in cookies.
setcookie( 'user_password', $password );
setcookie( 'api_key', $api_key );

// ✅ GOOD: Store sensitive data server-side, use session reference.
$session_token = wp_generate_password( 32, false );
set_transient( 'session_' . $session_token, $user_data, HOUR_IN_SECONDS );
setcookie( 'session_token', $session_token, /* secure flags */ );
```

## Security Headers

```php
// ✅ GOOD: Add security headers.
add_action( 'send_headers', function() {
    // Prevent clickjacking.
    header( 'X-Frame-Options: SAMEORIGIN' );

    // Prevent MIME type sniffing.
    header( 'X-Content-Type-Options: nosniff' );

    // Enable XSS filter.
    header( 'X-XSS-Protection: 1; mode=block' );

    // Referrer policy.
    header( 'Referrer-Policy: strict-origin-when-cross-origin' );

    // Content Security Policy (customize as needed).
    // header( "Content-Security-Policy: default-src 'self'" );
} );
```

## Severity Definitions

| Severity | Description |
|----------|-------------|
| **Critical** | Direct exploitation possible (SQLi, XSS, RCE, auth bypass) |
| **Warning** | Requires specific conditions to exploit |
| **Info** | Security hardening opportunity |

## Output Format

Structure findings as:

```markdown
## Security Review: [filename/component]

### Critical Vulnerabilities
- **Line X**: [Issue] - [Vulnerability type] - [Fix]

### Warnings
- **Line X**: [Issue] - [Risk] - [Fix]

### Hardening Recommendations
- [Security improvements]

### Summary
- Total issues: X Critical, Y Warnings, Z Info
- Risk level: [Critical/High/Medium/Low]
- Requires immediate attention: [Yes/No]
```

## Common Mistakes

| Mistake | Why It's Wrong | Fix |
|---------|----------------|-----|
| Using `esc_sql()` for injection protection | Doesn't handle all cases | Use `$wpdb->prepare()` |
| Escaping input instead of output | Data may be used in multiple contexts | Sanitize input, escape output |
| Nonce in GET request URL | Nonces can be logged/cached | Use POST for sensitive actions |
| Capability check in view, not controller | Can be bypassed via direct request | Check in action handler |
| Trusting `is_admin()` for security | Only checks context, not permissions | Use `current_user_can()` |
| Cron hook name = internal action name | Infinite recursion, fatal error, DoS | Use different names: `my_cron` vs `my_do_cron` |
| Not clearing cron on deactivation | Orphaned events continue running | Use `wp_clear_scheduled_hook()` |
| Checkbox not in sanitize callback | Setting won't save when unchecked | Explicitly set `false` for missing checkbox |

## Deep-Dive References

Load these references based on the task:

| Task | Reference to Load |
|------|-------------------|
| Reviewing code for vulnerabilities | `references/vulnerabilities.md` |
| Implementing authentication | `references/authentication-guide.md` |
| Securing file operations | `references/file-security.md` |
| Hardening configuration | `references/hardening-checklist.md` |
