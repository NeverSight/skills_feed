---
name: pr-review
description: WordPress-focused pull request review with double verification checklist. Use when reviewing PRs, performing code audits, or ensuring quality before merging.
---

# PR Review Skill

Systematic pull request review process with double verification for WordPress development teams.

## Review Philosophy

### The Three Lenses

1. **Security Lens** - Could this be exploited?
2. **Quality Lens** - Is this maintainable?
3. **User Lens** - Does this work well for users?

### Review Mindset

- You're a teammate, not a gatekeeper
- Catch bugs, but also celebrate wins
- Ask questions before assuming mistakes
- Suggest improvements, don't demand perfection

## Double Verification Checklist

### First Pass: Security (Blocking)

These MUST be fixed before merge:

#### Input Handling
- [ ] `$_GET`, `$_POST`, `$_REQUEST` sanitized before use
- [ ] `sanitize_text_field()` for strings
- [ ] `absint()` or `intval()` for integers
- [ ] `sanitize_email()` for emails
- [ ] `esc_url_raw()` for URLs being stored

#### Output Escaping
- [ ] `esc_html()` for text content
- [ ] `esc_attr()` for HTML attributes
- [ ] `esc_url()` for URLs in href/src
- [ ] `wp_kses_post()` for allowed HTML
- [ ] `esc_js()` for inline JavaScript

#### Database Security
- [ ] All queries use `$wpdb->prepare()`
- [ ] No raw `$_GET`/`$_POST` in queries
- [ ] LIKE queries use `$wpdb->esc_like()`

#### Authentication
- [ ] Forms have `wp_nonce_field()`
- [ ] Submissions verify with `wp_verify_nonce()`
- [ ] AJAX uses `check_ajax_referer()`
- [ ] `current_user_can()` before privileged actions
- [ ] REST endpoints have `permission_callback`

#### File Security
- [ ] No `eval()`, `assert()`, `create_function()`
- [ ] No unsanitized `include`/`require`
- [ ] File uploads validate MIME type
- [ ] No hardcoded credentials/API keys

### Second Pass: Quality (Non-blocking but important)

#### Code Standards
- [ ] Follows WordPress PHP coding standards
- [ ] Consistent naming conventions
- [ ] Functions are focused (<50 lines ideal)
- [ ] No duplicate code (DRY principle)
- [ ] Meaningful variable/function names

#### Documentation
- [ ] Functions have DocBlocks
- [ ] Complex logic has explanatory comments
- [ ] "Why" is documented, not just "what"
- [ ] Translatable strings use `__()` or `_e()`

#### Performance
- [ ] No `posts_per_page => -1` on frontend
- [ ] Expensive operations cached
- [ ] Database queries optimized
- [ ] Assets conditionally loaded
- [ ] No N+1 query patterns

#### Error Handling
- [ ] Functions return WP_Error for failures
- [ ] Errors are logged, not displayed to users
- [ ] Graceful degradation for edge cases
- [ ] Null checks before property access

## Review Comments Template

### Requesting Changes (Security)

```markdown
🔒 **Security: Input Sanitization Required**

Line 45 uses `$_POST['email']` directly. This could allow malicious input.

**Suggestion:**
\`\`\`php
$email = sanitize_email( $_POST['email'] );
if ( ! is_email( $email ) ) {
    return new WP_Error( 'invalid_email', __( 'Please provide a valid email.', 'textdomain' ) );
}
\`\`\`

Happy to help if you have questions about this! 😊
```

### Requesting Changes (Logic)

```markdown
🐛 **Bug: Potential Issue Found**

The condition on line 23 might not handle the case where `$user_id` is 0 (logged out user).

**Current:**
\`\`\`php
if ( $user_id ) { // 0 is falsy, but might be intentional?
\`\`\`

**Suggestion:**
\`\`\`php
if ( $user_id > 0 ) { // Explicit check for logged-in user
\`\`\`

Could you clarify the intended behavior here? Thanks! 🙏
```

### Suggesting Improvement (Non-blocking)

```markdown
💡 **Suggestion: Performance Optimization**

This query runs on every page load. We could cache it to improve performance:

\`\`\`php
$cache_key = 'featured_posts_' . get_locale();
$posts = wp_cache_get( $cache_key );

if ( false === $posts ) {
    $posts = get_posts( $args );
    wp_cache_set( $cache_key, $posts, '', HOUR_IN_SECONDS );
}
\`\`\`

Not blocking - just an idea for future optimization! 🚀
```

### Asking Questions

```markdown
❓ **Question: Clarification Needed**

I see we're using `update_option()` here on line 67. This runs on every save, which could be slow with many concurrent users.

Was there a specific reason for using options instead of post meta? Just want to understand the context before suggesting alternatives.

Thanks! 😊
```

### Celebrating Good Code

```markdown
✨ **Nice Work!**

Love how you structured this! The early return pattern on line 12-15 makes the logic really clear. Also, great use of `wp_cache_get()` - that'll help performance significantly.

Clean, readable, and secure. Approved! 🎉
```

## PR Description Template

When creating PRs, use this format:

```markdown
## Summary

Brief description of what this PR does and why.

## Type of Change

- [ ] 🐛 Bug fix (non-breaking change fixing an issue)
- [ ] ✨ New feature (non-breaking change adding functionality)
- [ ] 💥 Breaking change (fix or feature causing existing functionality to change)
- [ ] 📚 Documentation update
- [ ] 🔧 Refactor (code change that neither fixes a bug nor adds a feature)

## Changes Made

- Change 1: What and why
- Change 2: What and why
- Change 3: What and why

## How to Test

1. Step to reproduce/test
2. Expected behavior
3. Any specific areas to focus on

## Security Checklist

- [ ] Input sanitization implemented
- [ ] Output escaping implemented
- [ ] Nonce verification for forms
- [ ] Capability checks for actions
- [ ] No sensitive data exposed

## Screenshots (if applicable)

| Before | After |
|--------|-------|
| image  | image |

## Related Issues

Closes #123

## Reviewer Notes

Any specific areas you'd like feedback on?
```

## Review Workflow

### Step 1: Understand Context

1. Read PR description thoroughly
2. Check linked issues/tickets
3. Understand the "why" before reviewing the "how"

### Step 2: First Pass - Security

Run through security checklist above. These are **blocking issues**.

Comment format:
```
🔒 **Security: [Issue Type]**
[Description and fix]
```

### Step 3: Second Pass - Quality

Run through quality checklist. These are **suggestions**.

Comment format:
```
💡 **Suggestion: [Topic]**
[Description and suggestion]
```

### Step 4: Summary Comment

```markdown
## Review Summary

### ✅ What's Good
- [Positive observations]
- [Good patterns used]
- [Clean code highlights]

### 🔒 Security (Must Fix)
- [ ] [Issue 1 - line X]
- [ ] [Issue 2 - line Y]

### 💡 Suggestions (Optional)
- [ ] [Suggestion 1]
- [ ] [Suggestion 2]

### 📝 Questions
- [Any clarifications needed]

---

**Overall:** [Approve / Request Changes / Approve with suggestions]

[Encouraging closing message] 😊
```

## Quick Reference

### Common Security Issues

| Issue | Bad | Good |
|-------|-----|------|
| XSS | `echo $_GET['q']` | `echo esc_html( $_GET['q'] )` |
| SQL Injection | `WHERE id = $_GET['id']` | `$wpdb->prepare( 'WHERE id = %d', $id )` |
| CSRF | Form without nonce | `wp_nonce_field( 'action' )` |
| Broken Auth | No capability check | `current_user_can( 'edit_posts' )` |

### Approval Decision Tree

```
Is there a security issue?
├── Yes → Request Changes (blocking)
└── No → Continue

Are there bugs or logic errors?
├── Yes → Request Changes (blocking)
└── No → Continue

Does it follow standards?
├── Mostly → Approve with suggestions
└── Yes → Approve! 🎉
```

### Response Time Goals

- **Critical bugs/security**: Same day
- **Normal PRs**: Within 24 hours
- **Small fixes**: Within 4 hours

### Friendly Phrases

- "Great catch on..."
- "Nice solution! One thought..."
- "What do you think about..."
- "I learned something from this!"
- "Clean and readable! 🎉"
- "Happy to pair on this if helpful!"
