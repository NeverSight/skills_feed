---
name: css-tailwind
description: Build with Tailwind CSS utility-first framework - configuration, customization, best practices
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-12-30"
bonded_agent: 05-css-preprocessors
bond_type: PRIMARY_BOND
---

# CSS Tailwind Skill

Master Tailwind CSS utility-first framework with configuration, customization, and production optimization.

## Overview

This skill provides atomic, focused guidance on Tailwind CSS with v3+ patterns, custom configuration, and purge optimization.

## Skill Metadata

| Property | Value |
|----------|-------|
| **Category** | Framework |
| **Complexity** | Intermediate to Advanced |
| **Dependencies** | css-fundamentals |
| **Bonded Agent** | 05-css-preprocessors |

## Usage

```
Skill("css-tailwind")
```

## Parameter Schema

```yaml
parameters:
  topic:
    type: string
    required: true
    enum: [setup, configuration, utilities, components, plugins, optimization]
    description: Tailwind topic to explore

  framework:
    type: string
    required: false
    enum: [nextjs, vite, react, vue, vanilla]
    description: Framework integration

  include_examples:
    type: boolean
    required: false
    default: true
    description: Include practical code examples

validation:
  - rule: topic_required
    message: "topic parameter is required"
  - rule: valid_topic
    message: "topic must be one of: setup, configuration, utilities..."
```

## Topics Covered

### Setup & Configuration
- Installation for different frameworks
- tailwind.config.js customization
- Content path configuration

### Utilities
- Spacing, colors, typography
- Flexbox and Grid utilities
- Responsive prefixes
- State variants (hover, focus, dark)

### Components
- Component extraction with @apply
- Plugin-based components
- Headless UI integration

### Optimization
- Content purging
- JIT mode
- Production builds

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
    - topic_distribution
    - framework_usage
```

## Quick Reference

### Configuration Template

```javascript
// tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{js,ts,jsx,tsx,html,vue}',
    './components/**/*.{js,ts,jsx,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          900: '#1e3a8a',
        },
      },
      spacing: {
        '128': '32rem',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
}
```

### Common Utility Patterns

```html
<!-- Flexbox centering -->
<div class="flex items-center justify-center">

<!-- Responsive grid -->
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

<!-- Card component -->
<div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">

<!-- Button -->
<button class="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:ring-2 focus:ring-blue-500 focus:ring-offset-2">

<!-- Typography -->
<h1 class="text-3xl font-bold text-gray-900 dark:text-white">
```

### Responsive Prefixes

```
sm:  → 640px+
md:  → 768px+
lg:  → 1024px+
xl:  → 1280px+
2xl: → 1536px+

Example: class="text-sm md:text-base lg:text-lg"
```

### State Variants

```html
<!-- Hover -->
<div class="bg-white hover:bg-gray-50">

<!-- Focus -->
<input class="border focus:ring-2 focus:ring-blue-500">

<!-- Dark mode -->
<div class="bg-white dark:bg-gray-800">

<!-- Group hover -->
<div class="group">
  <span class="group-hover:text-blue-500">
</div>
```

## Component Extraction

```css
/* Using @apply for component classes */
@layer components {
  .btn {
    @apply px-4 py-2 rounded-md font-medium transition-colors;
  }

  .btn-primary {
    @apply btn bg-blue-500 text-white hover:bg-blue-600;
  }

  .btn-secondary {
    @apply btn bg-gray-200 text-gray-800 hover:bg-gray-300;
  }
}
```

## Arbitrary Values

```html
<!-- Arbitrary values with [] -->
<div class="top-[117px]">
<div class="bg-[#1da1f2]">
<div class="w-[calc(100%-2rem)]">
<div class="grid-cols-[1fr_2fr_1fr]">
```

## Production Optimization

```javascript
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    ...(process.env.NODE_ENV === 'production' ? { cssnano: {} } : {})
  },
}
```

## Test Template

```javascript
describe('CSS Tailwind Skill', () => {
  test('validates topic parameter', () => {
    expect(() => skill({ topic: 'invalid' }))
      .toThrow('topic must be one of: setup, configuration...');
  });

  test('returns framework-specific setup', () => {
    const result = skill({ topic: 'setup', framework: 'nextjs' });
    expect(result).toContain('next.config');
  });

  test('includes content paths for configuration', () => {
    const result = skill({ topic: 'configuration' });
    expect(result).toContain('content:');
  });
});
```

## Error Handling

| Error Code | Cause | Recovery |
|------------|-------|----------|
| INVALID_TOPIC | Unknown topic | Show valid options |
| MISSING_CONTENT_PATH | Styles not applying | Check content array |
| PLUGIN_NOT_FOUND | Plugin import error | Verify installation |

## Related Skills

- css-fundamentals (utility understanding)
- css-architecture (component organization)
- css-performance (purge optimization)
