---
name: wp-performance-review
description: "Use when reviewing WordPress PHP code for performance issues, auditing themes/plugins for scalability, optimizing WP_Query, analyzing caching strategies, or detecting anti-patterns in database queries, hooks, object caching, AJAX, and template loading."
compatibility: "Targets WordPress 6.9+ (PHP 8.0+). Filesystem-based agent with bash."
---

# WP Performance Review

## When to use

Use this skill when:

- Reviewing PR/code for WordPress theme or plugin
- User reports slow page loads, timeouts, or 500 errors
- Auditing before high-traffic event (launch, sale, viral moment)
- Optimizing WP_Query or database operations
- Investigating memory exhaustion or DB locks

## Inputs required

- Files or directories to review.
- Context: dev/staging/prod environment.
- Any constraints: read-only access, no plugin installs.
- Symptoms: slow TTFB, specific URL, admin vs frontend.

## Procedure

### 0) Identify scope and file types

1. Identify file type and apply relevant checks
2. Note hosting environment (managed, self-hosted, shared)
3. Determine if this is admin-only or frontend code

### 1) Scan for critical patterns first

Run quick detection scans:

```bash
# Unbounded queries - CRITICAL
grep -rn "posts_per_page.*-1\|numberposts.*-1" .

# query_posts - CRITICAL
grep -rn "query_posts\s*(" .

# Session start - CRITICAL (bypasses page cache)
grep -rn "session_start\s*(" .

# Polling patterns - CRITICAL (self-DDoS)
grep -rn "setInterval.*fetch\|setInterval.*ajax" .
```

Read:
- `references/anti-patterns.md`

### 2) Check warnings (inefficient but not catastrophic)

```bash
# DB writes on frontend
grep -rn "update_option\|add_option" . | grep -v "admin\|activate"

# Uncached expensive functions
grep -rn "url_to_postid\|attachment_url_to_postid" .

# External HTTP without caching
grep -rn "wp_remote_get\|wp_remote_post" .

# Cache bypass
grep -rn "cache_results.*false" .
```

### 3) Check file-type specific patterns

**WP_Query / Database Code:**
- Missing `posts_per_page` argument
- `meta_query` with `value` comparisons (unindexed)
- `post__not_in` with large arrays
- `LIKE '%term%'` (leading wildcard)

**AJAX Handlers:**
- POST method for read operations (bypasses cache)
- Missing nonce verification

**Template Files:**
- Database queries inside loops (N+1)
- `wp_remote_get` in templates

Read:
- `references/file-type-checks.md`

### 4) Report findings with severity

Structure findings as:

```markdown
## Performance Review: [filename]

### Critical Issues
- **Line X**: [Issue] - [Explanation] - [Fix]

### Warnings
- **Line X**: [Issue] - [Explanation] - [Fix]

### Recommendations
- [Optimization opportunities]
```

Read:
- `references/output-format.md`

## Verification

- All critical issues have been identified
- Line numbers are accurate
- Fixes are actionable and WordPress-specific
- Context is considered (admin vs frontend)

## Failure modes / debugging

- False positive on admin-only code:
  - Check context - admin, CLI, cron are lower risk
- Missing `session_start()` in plugin:
  - Always grep across ALL code including plugins
- Ignoring JS polling patterns:
  - Review `.js` files for `setInterval` + fetch

Read:
- `references/common-mistakes.md`

## WordPress 6.9 Performance Improvements

Be aware of these 6.9 changes when profiling:

**On-demand CSS for classic themes:**
- Classic themes now get on-demand CSS loading (previously only block themes)
- Reduces CSS payload by 30-65% by only loading styles for blocks actually used
- If profiling a classic theme, this should already be helping

**Block themes with no render-blocking resources:**
- Block themes without custom stylesheets (like Twenty Twenty-Three/Four) can now load with zero render-blocking CSS
- Styles come from global styles (theme.json) and separate block styles, all inlined
- Significantly improves LCP (Largest Contentful Paint)

**Inline CSS limit increased:**
- The threshold for inlining small stylesheets has been raised
- Reduces render-blocking resources

## WP-CLI Profiling Commands

If WP-CLI is available, use these for deep profiling:

```bash
# See where time goes (bootstrap/main_query/template)
wp profile stage --url=https://example.com/page/

# Find slow hooks/callbacks
wp profile hook --url=https://example.com/page/

# Profile specific code path
wp profile eval 'do_action("init");'

# Run health checks
wp doctor check
```

## Query Monitor Headless Usage

For backend-only debugging, Query Monitor works via REST API:

1. Authenticate (nonce or Application Password)
2. Request with `?_envelope` parameter
3. Inspect `x-qm-*` headers or `qm` property in response

## Escalation

- If production and no explicit approval, do NOT: install plugins, enable `SAVEQUERIES`, run load tests, or flush caches during traffic
- For system-level profiling (APM, PHP profilers), coordinate with ops/hosting

Consult:
- [WordPress Performance Team Handbook](https://make.wordpress.org/performance/)
- [Query Monitor Plugin](https://querymonitor.com/)
- [WP 6.9 Frontend Performance Field Guide](https://make.wordpress.org/core/2025/11/18/wordpress-6-9-frontend-performance-field-guide/)
