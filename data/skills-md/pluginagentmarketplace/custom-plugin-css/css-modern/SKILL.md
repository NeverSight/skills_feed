---
name: css-modern
description: Use modern CSS features - custom properties, container queries, :has(), @layer, CSS nesting
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-12-30"
bonded_agent: 07-css-modern-features
bond_type: PRIMARY_BOND
---

# CSS Modern Features Skill

Master cutting-edge CSS features: custom properties, container queries, :has(), @layer, and native CSS nesting.

## Overview

This skill provides atomic, focused guidance on modern CSS features (2022-2025) with browser compatibility information and fallback strategies.

## Skill Metadata

| Property | Value |
|----------|-------|
| **Category** | Modern CSS |
| **Complexity** | Advanced to Expert |
| **Dependencies** | css-fundamentals |
| **Bonded Agent** | 07-css-modern-features |

## Usage

```
Skill("css-modern")
```

## Parameter Schema

```yaml
parameters:
  feature:
    type: string
    required: true
    enum: [custom-properties, container-queries, has-selector, layers, nesting, logical-properties]
    description: Modern CSS feature to explore

  include_fallback:
    type: boolean
    required: false
    default: true
    description: Include browser fallback patterns

  browser_support:
    type: boolean
    required: false
    default: true
    description: Include compatibility information

validation:
  - rule: feature_required
    message: "feature parameter is required"
  - rule: valid_feature
    message: "feature must be one of: custom-properties, container-queries..."
```

## Topics Covered

### Custom Properties (CSS Variables)
- Declaration and inheritance
- Computed values with calc()
- Theming systems
- JavaScript integration

### Container Queries
- container-type and container-name
- @container syntax
- Container query units (cqi, cqw)
- Style queries

### :has() Selector
- Parent selection patterns
- Form state styling
- Previous sibling selection
- Performance considerations

### @layer (Cascade Layers)
- Layer definition and ordering
- Third-party CSS management
- Specificity without !important

### CSS Nesting
- Native nesting syntax
- & selector usage
- Media queries in nesting

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
    - fallback_requests
```

## Quick Reference

### Custom Properties

```css
/* Definition */
:root {
  --color-primary: #3b82f6;
  --spacing-md: 1rem;
}

/* Usage */
.button {
  background: var(--color-primary);
  padding: var(--spacing-md);
}

/* With fallback */
color: var(--text-color, black);

/* With calc() */
margin: calc(var(--spacing-md) * 2);
```

### Container Queries

```css
/* Define container */
.card-wrapper {
  container-type: inline-size;
  container-name: card;
}

/* Query container */
@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

/* Container units */
.card-title {
  font-size: clamp(1rem, 5cqi, 2rem);
}
```

### :has() Selector

```css
/* Style parent based on child */
.card:has(.card-image) {
  padding-top: 0;
}

/* Form validation styling */
.form:has(:invalid) .submit-btn {
  opacity: 0.5;
  pointer-events: none;
}

/* Style previous sibling */
.item:has(+ .item:hover) {
  transform: translateX(-5px);
}

/* Check for empty state */
.list:not(:has(li)) {
  display: none;
}
```

### @layer

```css
/* Define layer order */
@layer reset, base, components, utilities;

@layer reset {
  *, *::before, *::after {
    margin: 0;
    box-sizing: border-box;
  }
}

@layer components {
  .button {
    padding: 0.5rem 1rem;
  }
}

@layer utilities {
  .hidden { display: none !important; }
}
```

### CSS Nesting

```css
.card {
  background: white;
  border-radius: 8px;

  & .card-header {
    padding: 1rem;
    border-bottom: 1px solid #eee;
  }

  &:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  }

  @media (min-width: 768px) {
    display: grid;
    grid-template-columns: 1fr 2fr;
  }
}
```

## Browser Support (2025)

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| Custom Properties | 49+ | 31+ | 9.1+ | 15+ |
| Container Queries | 105+ | 110+ | 16+ | 105+ |
| :has() | 105+ | 121+ | 15.4+ | 105+ |
| @layer | 99+ | 97+ | 15.4+ | 99+ |
| CSS Nesting | 120+ | 117+ | 17.2+ | 120+ |

## Fallback Patterns

### @supports Usage

```css
/* Feature detection */
@supports (container-type: inline-size) {
  .wrapper {
    container-type: inline-size;
  }
}

/* Fallback for :has() */
@supports not selector(:has(*)) {
  /* JavaScript-based alternative styles */
  .card.has-image {
    padding-top: 0;
  }
}
```

### Progressive Enhancement

```css
/* Base experience */
.card {
  padding: 1rem;
}

/* Enhanced for modern browsers */
@supports (container-type: inline-size) {
  .card-wrapper {
    container-type: inline-size;
  }

  @container (min-width: 400px) {
    .card {
      display: grid;
    }
  }
}
```

## Test Template

```javascript
describe('CSS Modern Skill', () => {
  test('validates feature parameter', () => {
    expect(() => skill({ feature: 'invalid' }))
      .toThrow('feature must be one of: custom-properties...');
  });

  test('includes fallback when flag is true', () => {
    const result = skill({ feature: 'container-queries', include_fallback: true });
    expect(result).toContain('@supports');
  });

  test('includes browser support when flag is true', () => {
    const result = skill({ feature: 'has-selector', browser_support: true });
    expect(result).toContain('Chrome');
    expect(result).toContain('Safari');
  });
});
```

## Error Handling

| Error Code | Cause | Recovery |
|------------|-------|----------|
| INVALID_FEATURE | Unknown feature | Show valid options |
| BROWSER_UNSUPPORTED | Feature not available | Provide @supports fallback |
| PERFORMANCE_WARNING | :has() used broadly | Suggest scope limitation |

## Related Skills

- css-fundamentals (selector knowledge)
- css-flexbox-grid (container query layouts)
- css-performance (feature impact on performance)
