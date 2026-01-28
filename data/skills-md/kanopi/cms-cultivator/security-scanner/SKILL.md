---
name: security-scanner
description: Automatically scan code for security vulnerabilities when user asks if code is secure or shows potentially unsafe code. Performs focused security checks on specific code, functions, or patterns. Invoke when user asks "is this secure?", "security issue?", mentions XSS, SQL injection, or shows security-sensitive code.
---

# Security Scanner

Automatically scan code for security vulnerabilities.

## Security Philosophy

Security is a continuous practice, not a one-time fix.

### Core Beliefs

1. **Defense in Depth**: Multiple layers of security controls
2. **Least Privilege**: Grant minimum access necessary
3. **Secure by Default**: Safe configurations out of the box
4. **Fail Securely**: Errors should deny access, not grant it

### Scope Balance

- **Quick checks** (this skill): Fast feedback on specific code patterns (catches common vulnerabilities)
- **Comprehensive audits** (`/audit-security` command): Full OWASP Top 10 scan with dependency checks
- **Penetration testing**: Professional security testing (irreplaceable for production systems)

This skill provides rapid feedback during development. For production readiness, use comprehensive audits + professional pentesting.

## When to Use This Skill

Activate this skill when the user:
- Asks "is this secure?"
- Shows code handling user input
- Mentions "security vulnerability", "exploit", or "hack"
- References XSS, SQL injection, CSRF, or authentication
- Shows database queries or file operations
- Asks "could this be exploited?"

## Decision Framework

Before scanning for security issues, assess:

### What's the Attack Surface?

1. **User input** → Check for injection vulnerabilities (SQL, XSS, command injection)
2. **Authentication** → Check for weak passwords, session handling, brute force protection
3. **Authorization** → Check for privilege escalation, IDOR, access control
4. **File operations** → Check for path traversal, unrestricted uploads
5. **API endpoints** → Check for rate limiting, authentication, CORS

### What's the Risk Level?

**Critical risks** (prioritize first):
- SQL injection in authentication
- XSS on admin pages
- Authentication bypass
- Remote code execution
- Data exposure (PII, passwords)

**High risks**:
- CSRF on state-changing operations
- Authorization flaws
- Insecure file uploads
- Weak session management

**Medium/Low risks**:
- Information disclosure
- Missing security headers
- Weak error messages

### What Type of Code Is This?

**User-facing**:
- Forms → Check input validation, CSRF tokens
- Search → Check SQL injection, XSS
- File uploads → Check file type, size, path validation

**Backend**:
- Database queries → Check parameterization
- File system → Check path traversal
- External API calls → Check credential handling

**Authentication/Authorization**:
- Login → Check brute force protection, password requirements
- Sessions → Check secure flags, timeout
- Permissions → Check role-based access control

### What Platform Standards Apply?

**Drupal**:
- Use database API (no raw queries)
- Use Form API (built-in CSRF)
- Use Render API (auto-escaping)
- Check permissions with `hasPermission()`

**WordPress**:
- Use `wpdb->prepare()` for queries
- Use `wp_nonce_field()` for CSRF
- Use `esc_html()`, `esc_attr()` for output
- Check permissions with `current_user_can()`

### Decision Tree

```
User shows code or asks about security
    ↓
Identify attack surface (input/auth/files)
    ↓
Assess risk level (Critical/High/Medium)
    ↓
Check against OWASP Top 10
    ↓
Apply platform-specific patterns
    ↓
Report vulnerabilities with fixes
    ↓
Prioritize by exploitability and impact
```

## Best Practices

### DO:

- ✅ Always validate and sanitize user input
- ✅ Use parameterized queries or ORM for database operations
- ✅ Escape output based on context (HTML, JavaScript, URL, CSS)
- ✅ Implement CSRF protection on all state-changing operations
- ✅ Check permissions before sensitive operations
- ✅ Use strong, unique API keys and rotate them regularly
- ✅ Log security-relevant events (failed logins, permission denials)
- ✅ Keep dependencies updated and scan for CVEs
- ✅ Use HTTPS for all data transmission

### DON'T:

- ❌ Trust user input without validation
- ❌ Build SQL queries with string concatenation
- ❌ Echo user input directly without escaping
- ❌ Store passwords in plain text or use weak hashing
- ❌ Hard-code secrets, API keys, or credentials in code
- ❌ Use `eval()`, `unserialize()`, or `exec()` with user input
- ❌ Disable security features (CSRF protection, XSS filters)
- ❌ Expose detailed error messages to end users
- ❌ Use outdated cryptographic algorithms (MD5, SHA1 for passwords)
- ❌ Assume data from database or API is safe (defense in depth)

## Quick Security Checks

### 1. SQL Injection

**Vulnerable Pattern:**
```php
// ❌ DANGEROUS
$query = "SELECT * FROM users WHERE id = " . $_GET['id'];
db_query($query);
```

**Secure Pattern:**
```php
// ✅ SECURE
$query = db_select('users', 'u')
  ->condition('id', $id, '=')
  ->execute();

// Or with placeholders
$query = "SELECT * FROM users WHERE id = :id";
db_query($query, [':id' => $id]);
```

### 2. Cross-Site Scripting (XSS)

**Vulnerable Pattern:**
```php
// ❌ DANGEROUS
echo "<div>" . $_POST['name'] . "</div>";
```

**Secure Pattern:**
```php
// ✅ SECURE (Drupal)
echo "<div>" . Html::escape($_POST['name']) . "</div>";

// ✅ SECURE (WordPress)
echo "<div>" . esc_html( $_POST['name'] ) . "</div>";
```

### 3. CSRF (Cross-Site Request Forgery)

**Vulnerable Pattern:**
```php
// ❌ DANGEROUS - No CSRF protection
if ($_POST['action'] === 'delete') {
  delete_user($_POST['user_id']);
}
```

**Secure Pattern:**
```php
// ✅ SECURE (Drupal) - CSRF token validation
if ($_POST['form_token'] && \Drupal::csrfToken()->validate($_POST['form_token'])) {
  delete_user($_POST['user_id']);
}

// ✅ SECURE (WordPress) - Nonce validation
if (wp_verify_nonce($_POST['_wpnonce'], 'delete_user')) {
  delete_user($_POST['user_id']);
}
```

### 4. Authentication Bypass

**Check for:**
- Missing permission checks
- Hardcoded credentials
- Weak password requirements
- Session fixation vulnerabilities

### 5. File Upload Vulnerabilities

**Vulnerable Pattern:**
```php
// ❌ DANGEROUS - No validation
move_uploaded_file($_FILES['file']['tmp_name'], 'uploads/' . $_FILES['file']['name']);
```

**Secure Pattern:**
```php
// ✅ SECURE
$allowed_types = ['jpg', 'png', 'pdf'];
$extension = pathinfo($_FILES['file']['name'], PATHINFO_EXTENSION);

if (in_array(strtolower($extension), $allowed_types)) {
  $safe_name = preg_replace('/[^a-zA-Z0-9_-]/', '', basename($_FILES['file']['name']));
  move_uploaded_file($_FILES['file']['tmp_name'], 'uploads/' . $safe_name);
}
```

## Response Format

```markdown
## Security Scan Results

### 🔴 Critical Issues (Fix Immediately)

**1. SQL Injection Vulnerability**
- **Location**: `src/Controller/UserController.php:45`
- **Risk**: Critical - Allows database manipulation
- **Code**:
  ```php
  $query = "SELECT * FROM users WHERE id = " . $_GET['id'];
  ```
- **Fix**:
  ```php
  $query = $connection->select('users', 'u')
    ->condition('id', $id, '=')
    ->execute();
  ```
- **OWASP**: [A03:2021 – Injection](https://owasp.org/Top10/A03_2021-Injection/)

### 🟠 High Priority

**2. Missing CSRF Protection**
- **Location**: `src/Form/DeleteForm.php:67`
- **Risk**: High - Allows unauthorized actions
- **Fix**: Add CSRF token validation

### 🟡 Medium Priority

**3. Weak Password Policy**
- **Current**: Minimum 6 characters
- **Recommended**: Minimum 12 characters + complexity rules

### ✅ Secure Patterns Found

- ✅ Output properly escaped (XSS protection)
- ✅ Access checks on admin routes
- ✅ File upload validation present
```

## OWASP Top 10 Quick Check

1. **Injection** - SQL, command, LDAP injection
2. **Broken Authentication** - Weak passwords, session management
3. **Sensitive Data Exposure** - Unencrypted data, weak crypto
4. **XML External Entities (XXE)** - XML parsing vulnerabilities
5. **Broken Access Control** - Missing permission checks
6. **Security Misconfiguration** - Default configs, verbose errors
7. **XSS** - Unescaped user input
8. **Insecure Deserialization** - Unsafe object deserialization
9. **Known Vulnerabilities** - Outdated dependencies
10. **Insufficient Logging** - No audit trail

## Platform-Specific Security

### Drupal Security

**Use**:
- `\Drupal\Component\Utility\Html::escape()` for output
- `\Drupal::database()->select()` for queries
- `\Drupal::csrfToken()->validate()` for forms
- `$this->currentUser()->hasPermission()` for access checks

### WordPress Security

**Use**:
- `esc_html()`, `esc_attr()`, `esc_url()` for output
- `$wpdb->prepare()` for queries
- `wp_verify_nonce()` for forms
- `current_user_can()` for permissions

## Integration with /audit-security Command

- **This Skill**: Focused code-level security checks
  - "Is this query secure?"
  - "Check this form for vulnerabilities"
  - Single function/file analysis

- **`/audit-security` Command**: Comprehensive security audit
  - Full OWASP Top 10 scan
  - Dependency vulnerability check
  - File permission analysis
  - Secrets detection

## Common Vulnerabilities

### Input Validation
```php
// ❌ No validation
$age = $_POST['age'];

// ✅ Validated
$age = filter_var($_POST['age'], FILTER_VALIDATE_INT, [
  'options' => ['min_range' => 1, 'max_range' => 120]
]);
```

### Output Escaping
```php
// ❌ Unescaped
echo $user_input;

// ✅ Escaped (context-appropriate)
echo Html::escape($user_input);           // HTML context
echo Html::escape($user_input, ENT_QUOTES); // Attribute context
echo json_encode($user_input);            // JSON context
```

### Access Control
```php
// ❌ No permission check
function deleteUser($uid) {
  User::load($uid)->delete();
}

// ✅ Permission checked
function deleteUser($uid) {
  if (!\Drupal::currentUser()->hasPermission('delete users')) {
    throw new AccessDeniedHttpException();
  }
  User::load($uid)->delete();
}
```

## Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Drupal Security Best Practices](https://www.drupal.org/docs/security-in-drupal)
- [WordPress Security](https://developer.wordpress.org/apis/security/)
