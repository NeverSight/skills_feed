---
name: css-performance
description: Optimize CSS performance - critical CSS, code splitting, purging, bundle analysis
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-12-30"
bonded_agent: 06-css-performance
bond_type: PRIMARY_BOND
---

# CSS Performance Skill

Optimize CSS performance with critical CSS extraction, code splitting, purging, and bundle analysis.

## Overview

This skill provides atomic, focused guidance on CSS performance optimization with measurable metrics and production-ready configurations.

## Skill Metadata

| Property | Value |
|----------|-------|
| **Category** | Optimization |
| **Complexity** | Advanced to Expert |
| **Dependencies** | css-fundamentals, css-architecture |
| **Bonded Agent** | 06-css-performance |

## Usage

```
Skill("css-performance")
```

## Parameter Schema

```yaml
parameters:
  optimization_type:
    type: string
    required: true
    enum: [critical-css, purging, minification, code-splitting, selectors]
    description: Type of optimization to implement

  tool:
    type: string
    required: false
    enum: [purgecss, cssnano, critical, webpack, postcss]
    description: Specific tool configuration

  metrics:
    type: boolean
    required: false
    default: true
    description: Include measurement recommendations

validation:
  - rule: optimization_type_required
    message: "optimization_type parameter is required"
  - rule: valid_optimization
    message: "optimization_type must be one of: critical-css, purging..."
```

## Topics Covered

### Critical CSS
- Above-the-fold extraction
- Inline critical, defer rest
- Tools: Critical, Penthouse

### Purging (Tree-shaking)
- PurgeCSS configuration
- Safelist patterns
- Dynamic class handling

### Minification
- cssnano optimization
- clean-css alternatives
- Safe vs unsafe optimizations

### Code Splitting
- Route-based splitting
- Component-level CSS
- Dynamic imports

## Retry Logic

```yaml
retry_config:
  max_attempts: 3
  backoff_type: exponential
  initial_delay_ms: 1000
  max_delay_ms: 10000
```

## Logging & Observability

```yaml
logging:
  entry_point: skill_invoked
  exit_point: skill_completed
  metrics:
    - invocation_count
    - optimization_type_distribution
    - tool_usage
```

## Quick Reference

### Performance Targets

| Metric | Target | Tool |
|--------|--------|------|
| CSS Size (gzip) | < 50KB | DevTools |
| Unused CSS | < 20% | Coverage |
| Critical CSS | < 14KB | Penthouse |
| FCP | < 1.8s | Lighthouse |

### PurgeCSS Configuration

```javascript
// postcss.config.js
module.exports = {
  plugins: [
    require('@fullhuman/postcss-purgecss')({
      content: [
        './src/**/*.{js,jsx,ts,tsx}',
        './public/index.html',
      ],
      defaultExtractor: content =>
        content.match(/[\w-/:]+(?<!:)/g) || [],
      safelist: {
        standard: [/^is-/, /^has-/, 'active', 'open'],
        deep: [/^data-/],
        greedy: [/modal$/, /tooltip$/],
      },
    }),
  ],
}
```

### Critical CSS Setup

```javascript
// critical.config.js
const critical = require('critical');

critical.generate({
  base: 'dist/',
  src: 'index.html',
  css: ['dist/styles.css'],
  width: 1300,
  height: 900,
  inline: true,
  extract: true,
});
```

### cssnano Configuration

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    cssnano: {
      preset: ['default', {
        discardComments: { removeAll: true },
        normalizeWhitespace: true,
        colormin: true,
        minifyFontValues: true,
        // Unsafe optimizations (test carefully)
        reduceIdents: false,
        mergeIdents: false,
      }],
    },
  },
}
```

### Async CSS Loading

```html
<!-- Inline critical CSS -->
<style>/* Critical CSS here */</style>

<!-- Async load full CSS -->
<link rel="preload" href="styles.css" as="style"
      onload="this.onload=null;this.rel='stylesheet'">
<noscript>
  <link rel="stylesheet" href="styles.css">
</noscript>
```

## Selector Performance

```css
/* FAST */
.button { }           /* Single class */
#header { }           /* ID */

/* MODERATE */
.nav .link { }        /* Descendant */
.nav > .link { }      /* Child */

/* SLOW (avoid) */
.container * { }                    /* Universal descendant */
[class*="btn-"][class$="-lg"] { }   /* Complex attribute */
```

## Measurement Commands

```bash
# Lighthouse CI
npx lighthouse-ci https://example.com --collect

# CSS Coverage in Chrome DevTools
# 1. Open DevTools → More Tools → Coverage
# 2. Reload page
# 3. Check CSS usage percentage

# Bundle analysis
npx webpack-bundle-analyzer stats.json
```

## Optimization Checklist

```
Pre-deployment:
├─ [ ] CSS minified
├─ [ ] Unused CSS purged (< 20% unused)
├─ [ ] Critical CSS inlined
├─ [ ] Non-critical CSS async loaded
├─ [ ] Source maps excluded from production
├─ [ ] gzip/Brotli compression enabled
└─ [ ] Cache headers configured
```

## Test Template

```javascript
describe('CSS Performance Skill', () => {
  test('validates optimization_type parameter', () => {
    expect(() => skill({ optimization_type: 'invalid' }))
      .toThrow('optimization_type must be one of: critical-css...');
  });

  test('returns PurgeCSS config for purging type', () => {
    const result = skill({ optimization_type: 'purging', tool: 'purgecss' });
    expect(result).toContain('safelist');
    expect(result).toContain('content');
  });

  test('includes metrics when flag is true', () => {
    const result = skill({ optimization_type: 'critical-css', metrics: true });
    expect(result).toContain('14KB');
    expect(result).toContain('Lighthouse');
  });
});
```

## Error Handling

| Error Code | Cause | Recovery |
|------------|-------|----------|
| INVALID_OPTIMIZATION | Unknown optimization type | Show valid options |
| TOOL_NOT_INSTALLED | Tool package missing | Show install command |
| OVER_PURGING | Styles missing in production | Expand safelist |

## Related Skills

- css-fundamentals (selector efficiency)
- css-architecture (file organization)
- css-tailwind (purge configuration)
