---
name: performance-analyzer
description: Automatically analyze performance issues when user mentions slow pages, performance problems, or optimization needs. Performs focused performance checks on specific code, queries, or components. Invoke when user says "this is slow", "performance issue", "optimize", or asks about speed.
---

# Performance Analyzer

Automatically analyze and suggest performance improvements for specific code.

## Philosophy

Fast code is user-friendly code. Every millisecond counts.

### Core Beliefs

1. **Measure Before Optimizing**: Profile to find actual bottlenecks, don't guess
2. **User Perception Matters Most**: A 100ms delay feels instant, 1s feels slow
3. **Progressive Enhancement**: Start fast (mobile), enhance for desktop
4. **Performance is a Feature**: Users notice and appreciate speed

### Why Performance Matters

- **User Experience**: Fast sites feel professional and responsive
- **Conversion Rates**: Every 100ms delay costs conversions
- **SEO Rankings**: Core Web Vitals directly impact search visibility
- **Accessibility**: Performance improvements help users on slow connections/devices

## When to Use This Skill

Activate this skill when the user:
- Says "this is slow" or "performance issue"
- Shows code and asks "how can I optimize this?"
- Mentions "page speed", "load time", or "Core Web Vitals"
- Asks "why is this query slow?"
- References "N+1 problem", "caching", or "optimization"
- Shows performance profiler output

## Decision Framework

Before analyzing performance, determine:

### What's Slow?

1. **Page load** → Check Core Web Vitals (LCP, INP, CLS)
2. **Database queries** → Check query count, N+1 problems
3. **API calls** → Check response times, external dependencies
4. **Asset loading** → Check CSS/JS/image sizes
5. **Server processing** → Check PHP/Node execution time

### What's the Baseline?

**Measure first**:
- Run Lighthouse for Core Web Vitals
- Profile with browser DevTools
- Check database query logs
- Measure actual load times

**Don't optimize without data** - Profile to find real bottlenecks

### What's the Target?

**Core Web Vitals targets**:
- **LCP** (Largest Contentful Paint): < 2.5s (good), < 4.0s (needs improvement)
- **INP** (Interaction to Next Paint): < 200ms (good), < 500ms (needs improvement)
- **CLS** (Cumulative Layout Shift): < 0.1 (good), < 0.25 (needs improvement)

**General targets**:
- **Page load**: < 3s ideal, < 5s acceptable
- **API response**: < 100ms ideal, < 500ms acceptable
- **Database query**: < 50ms ideal, < 200ms acceptable

### What's the Impact?

**Prioritize fixes by impact**:
1. **High** - Affects all users on every page load
2. **Medium** - Affects specific user flows or features
3. **Low** - Edge cases or infrequent operations

### What Optimizations Apply?

**Common patterns**:
- **N+1 queries** → Add eager loading
- **Large assets** → Compress, lazy load, CDN
- **No caching** → Add caching layers
- **Blocking resources** → Async/defer scripts
- **Unoptimized images** → Compress, WebP, responsive images
- **Too many HTTP requests** → Combine, bundle
- **Slow external APIs** → Cache, background jobs

### Decision Tree

```
User reports performance issue
    ↓
Measure baseline (Lighthouse, profiler)
    ↓
Identify bottleneck (queries/assets/processing)
    ↓
Assess impact (all users vs. edge case)
    ↓
Recommend specific optimizations
    ↓
Provide before/after metrics
```

## Quick Analysis Types

### 1. Database Query Analysis

**What to check:**
- N+1 queries
- Missing indexes
- SELECT * instead of specific fields
- Unnecessary JOINs
- Large result sets without pagination

**Example Response:**
```markdown
## Query Performance Issue: N+1 Problem

**Current Code:**
```php
$users = User::loadMultiple();
foreach ($users as $user) {
  $profile = $user->get('field_profile')->entity; // N+1!
}
```

**Problem**: Loading 100 users triggers 101 queries (1 + 100)

**Solution**: Use EntityQuery with eager loading
```php
$query = \Drupal::entityQuery('user')
  ->accessCheck(TRUE);
$uids = $query->execute();
$users = User::loadMultiple($uids);

// Preload profiles in one query
$profile_ids = [];
foreach ($users as $user) {
  $profile_ids[] = $user->get('field_profile')->target_id;
}
$profiles = Profile::loadMultiple($profile_ids);
```

**Impact**: Reduces queries from 101 to 2 (~98% improvement)
```

### 2. Asset Optimization

**What to check:**
- Large unoptimized images
- Unminified CSS/JS
- Blocking resources
- Missing lazy loading
- No CDN usage

### 3. Caching Analysis

**What to check:**
- Missing cache tags
- Cache invalidation issues
- No page cache
- Expensive uncached operations

### 4. Core Web Vitals

**Quick checks:**
- **LCP** (Largest Contentful Paint): Target < 2.5s
- **INP** (Interaction to Next Paint): Target < 200ms
- **CLS** (Cumulative Layout Shift): Target < 0.1

## Response Format

```markdown
## Performance Analysis

**Component**: [What was analyzed]
**Issue**: [Performance problem]
**Impact**: [How it affects users]

### Current Performance
- Metric: [value]
- Grade: [A-F]

### Optimization Recommendations

1. **[Recommendation]** (Priority: High)
   - Current: [problem]
   - Improved: [solution]
   - Expected gain: [percentage/time]

2. **[Next recommendation]**
   ...

### Code Example
[Provide optimized code]
```

## Common Performance Patterns

### Drupal

**Problem**: Lazy loading causing N+1
```php
// Bad
foreach ($nodes as $node) {
  $author = $node->getOwner()->getDisplayName(); // N+1
}

// Good
$nodes = \Drupal::entityTypeManager()
  ->getStorage('node')
  ->loadMultiple($nids);
User::loadMultiple(array_column($nodes, 'uid')); // Preload
```

### WordPress

**Problem**: Inefficient WP_Query
```php
// Bad
$posts = new WP_Query(['posts_per_page' => -1]); // Loads everything

// Good
$posts = new WP_Query([
  'posts_per_page' => 20,
  'fields' => 'ids', // Only IDs
  'no_found_rows' => true, // Skip counting
  'update_post_meta_cache' => false,
  'update_post_term_cache' => false,
]);
```

## Integration with /audit-perf Command

- **This Skill**: Focused code-level analysis
  - "This query is slow"
  - "Optimize this function"
  - Single component performance

- **`/audit-perf` Command**: Comprehensive site audit
  - Full performance analysis
  - Core Web Vitals testing
  - Lighthouse reports

## Quick Tips

💡 **Database**: Index foreign keys, avoid SELECT *
💡 **Caching**: Cache expensive operations, use cache tags
💡 **Assets**: Optimize images, minify CSS/JS, lazy load
💡 **Queries**: Limit results, use eager loading, avoid N+1
