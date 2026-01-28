---
name: css-sass
description: Use Sass/SCSS for advanced CSS preprocessing with modern @use/@forward syntax
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-12-30"
bonded_agent: 05-css-preprocessors
bond_type: PRIMARY_BOND
---

# CSS Sass/SCSS Skill

Master Sass/SCSS preprocessing with modern @use/@forward syntax, mixins, functions, and modular architecture.

## Overview

This skill provides atomic, focused guidance on Sass/SCSS with current dart-sass syntax and migration patterns from deprecated @import.

## Skill Metadata

| Property | Value |
|----------|-------|
| **Category** | Preprocessing |
| **Complexity** | Intermediate to Advanced |
| **Dependencies** | css-fundamentals, css-architecture |
| **Bonded Agent** | 05-css-preprocessors |

## Usage

```
Skill("css-sass")
```

## Parameter Schema

```yaml
parameters:
  feature:
    type: string
    required: true
    enum: [variables, mixins, functions, nesting, modules, extends]
    description: Sass feature to explore

  syntax:
    type: string
    required: false
    default: scss
    enum: [scss, sass]
    description: Sass syntax format

  modern_syntax:
    type: boolean
    required: false
    default: true
    description: Use @use/@forward instead of deprecated @import

validation:
  - rule: feature_required
    message: "feature parameter is required"
  - rule: valid_feature
    message: "feature must be one of: variables, mixins, functions, nesting, modules, extends"
```

## Topics Covered

### Variables
- Declaration and usage
- Scope rules (local vs global)
- Default values and !default flag
- Maps and lists

### Mixins
- Declaration with @mixin
- Parameters and default values
- Content blocks with @content
- Responsive mixins

### Functions
- Built-in functions
- Custom functions with @function
- Return values
- Pure vs impure functions

### Modules (@use/@forward)
- Module loading with @use
- Namespace handling
- Forwarding with @forward
- Configuring defaults

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
    - feature_usage
    - modern_syntax_adoption
```

## Quick Reference

### Module System (Modern)

```scss
// _variables.scss
$primary-color: #3b82f6 !default;
$spacing-unit: 8px !default;

// _mixins.scss
@use 'variables' as vars;

@mixin button-base {
  padding: vars.$spacing-unit * 2;
  background: vars.$primary-color;
}

// main.scss
@use 'variables' as v;
@use 'mixins' as m;

.button {
  @include m.button-base;
  color: v.$primary-color;
}
```

### @forward for Library Exports

```scss
// abstracts/_index.scss
@forward 'variables';
@forward 'mixins';
@forward 'functions';

// main.scss
@use 'abstracts';

.element {
  color: abstracts.$primary-color;
}
```

### Common Mixins

```scss
// Responsive breakpoints
@mixin respond-to($breakpoint) {
  @if $breakpoint == 'sm' {
    @media (min-width: 640px) { @content; }
  } @else if $breakpoint == 'md' {
    @media (min-width: 768px) { @content; }
  } @else if $breakpoint == 'lg' {
    @media (min-width: 1024px) { @content; }
  }
}

// Flexbox center
@mixin flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

// Typography scale
@mixin text-style($size, $weight: 400) {
  font-size: $size;
  font-weight: $weight;
  line-height: 1.5;
}
```

### Useful Functions

```scss
// Rem conversion
@function rem($pixels, $base: 16) {
  @return #{$pixels / $base}rem;
}

// Color manipulation
@function tint($color, $percentage) {
  @return mix(white, $color, $percentage);
}

@function shade($color, $percentage) {
  @return mix(black, $color, $percentage);
}
```

## Migration Guide: @import to @use

```scss
/* OLD (deprecated) */
@import 'variables';
@import 'mixins';

.button {
  color: $primary-color;
  @include button-base;
}

/* NEW (recommended) */
@use 'variables' as v;
@use 'mixins' as m;

.button {
  color: v.$primary-color;
  @include m.button-base;
}
```

## File Structure

```
scss/
├── abstracts/
│   ├── _index.scss      # @forward all
│   ├── _variables.scss
│   ├── _mixins.scss
│   └── _functions.scss
├── base/
│   ├── _index.scss
│   ├── _reset.scss
│   └── _typography.scss
├── components/
│   ├── _index.scss
│   ├── _button.scss
│   └── _card.scss
├── layouts/
│   ├── _index.scss
│   └── _grid.scss
└── main.scss
```

## Test Template

```javascript
describe('CSS Sass Skill', () => {
  test('validates feature parameter', () => {
    expect(() => skill({ feature: 'invalid' }))
      .toThrow('feature must be one of: variables, mixins...');
  });

  test('returns @use syntax when modern_syntax is true', () => {
    const result = skill({ feature: 'modules', modern_syntax: true });
    expect(result).toContain('@use');
    expect(result).not.toContain('@import');
  });

  test('includes namespace examples for modules', () => {
    const result = skill({ feature: 'modules' });
    expect(result).toContain('as');
  });
});
```

## Error Handling

| Error Code | Cause | Recovery |
|------------|-------|----------|
| INVALID_FEATURE | Unknown feature | Show valid options |
| DEPRECATED_SYNTAX | Using @import | Show @use migration |
| NAMESPACE_CONFLICT | Duplicate namespace | Suggest unique alias |

## Related Skills

- css-fundamentals (prerequisite)
- css-architecture (file organization)
- css-performance (compilation optimization)
