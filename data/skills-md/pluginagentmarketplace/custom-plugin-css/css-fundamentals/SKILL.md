---
name: css-fundamentals
description: CSS fundamentals - selectors, specificity, box model, positioning, units
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-12-30"
bonded_agent: 01-css-fundamentals
bond_type: PRIMARY_BOND
---

# CSS Fundamentals Skill

Master core CSS concepts: selectors, specificity, box model, positioning, and units.

## Overview

This skill provides atomic, focused guidance on CSS fundamentals with type-safe parameters and comprehensive validation.

## Skill Metadata

| Property | Value |
|----------|-------|
| **Category** | Core CSS |
| **Complexity** | Beginner to Intermediate |
| **Dependencies** | None |
| **Bonded Agent** | 01-css-fundamentals |

## Usage

```
Skill("css-fundamentals")
```

## Parameter Schema

```yaml
parameters:
  topic:
    type: string
    required: true
    enum: [selectors, specificity, box-model, positioning, units, display]
    description: The CSS fundamental topic to explore

  level:
    type: string
    required: false
    default: beginner
    enum: [beginner, intermediate, advanced]
    description: Depth of explanation

  include_examples:
    type: boolean
    required: false
    default: true
    description: Include code examples

validation:
  - rule: topic_required
    message: "Topic parameter is required"
  - rule: valid_enum
    message: "Topic must be one of: selectors, specificity, box-model, positioning, units, display"
```

## Topics Covered

### Selectors
- Element, class, ID selectors
- Attribute selectors `[attr]`, `[attr=value]`
- Pseudo-classes `:hover`, `:focus`, `:nth-child()`
- Pseudo-elements `::before`, `::after`
- Combinator selectors `>`, `+`, `~`

### Specificity
- Specificity calculation (0,0,0,0)
- Cascade order rules
- `!important` usage and pitfalls
- Inheritance patterns

### Box Model
- Content, padding, border, margin
- `box-sizing: border-box` vs `content-box`
- Margin collapse behavior
- Inline vs block dimensions

### Positioning
- `static`, `relative`, `absolute`, `fixed`, `sticky`
- Stacking context and z-index
- Containing block rules
- Offset properties (top, right, bottom, left)

### Units
- Absolute: px, pt, cm
- Relative: em, rem, %, vh, vw
- Newer units: ch, lh, cqi, cqw
- When to use which unit

## Retry Logic

```yaml
retry_config:
  max_attempts: 3
  backoff_type: exponential
  initial_delay_ms: 1000
  max_delay_ms: 10000
  retryable_errors:
    - TIMEOUT
    - RATE_LIMIT
    - TEMPORARY_FAILURE
```

## Logging & Observability

```yaml
logging:
  entry_point: skill_invoked
  exit_point: skill_completed
  log_parameters: true
  log_response_size: true
  metrics:
    - invocation_count
    - success_rate
    - avg_response_time
```

## Quick Reference

### Specificity Calculator

```
Inline styles    → 1,0,0,0
ID selectors     → 0,1,0,0
Classes/attrs    → 0,0,1,0
Elements         → 0,0,0,1

Example: div#header .nav a:hover
         0,1,2,2 (ID=1, class+pseudo=2, elements=2)
```

### Box Model Visual

```
┌─────────────────────────────────┐
│           MARGIN                │
│   ┌─────────────────────────┐   │
│   │        BORDER           │   │
│   │   ┌─────────────────┐   │   │
│   │   │    PADDING      │   │   │
│   │   │   ┌─────────┐   │   │   │
│   │   │   │ CONTENT │   │   │   │
│   │   │   └─────────┘   │   │   │
│   │   └─────────────────┘   │   │
│   └─────────────────────────┘   │
└─────────────────────────────────┘
```

### Unit Recommendations

| Use Case | Recommended Unit |
|----------|------------------|
| Typography | rem |
| Spacing | rem or em |
| Borders | px |
| Viewport layouts | vh, vw, % |
| Container layouts | % or fr |

## Code Examples

### Selector Efficiency

```css
/* Efficient: Single class */
.nav-link { }

/* Less efficient: Descendant chain */
nav ul li a { }

/* Prefer attribute selectors */
[data-state="active"] { }
```

### Box Model Reset

```css
*, *::before, *::after {
  box-sizing: border-box;
}

* {
  margin: 0;
  padding: 0;
}
```

## Test Template

```javascript
describe('CSS Fundamentals Skill', () => {
  test('validates topic parameter', () => {
    expect(() => skill({ topic: 'invalid' }))
      .toThrow('Topic must be one of: selectors, specificity...');
  });

  test('returns selector examples for selectors topic', () => {
    const result = skill({ topic: 'selectors', level: 'beginner' });
    expect(result).toContain('.class');
    expect(result).toContain('#id');
  });

  test('handles missing optional parameters', () => {
    const result = skill({ topic: 'box-model' });
    expect(result.level).toBe('beginner');
    expect(result.include_examples).toBe(true);
  });
});
```

## Error Handling

| Error Code | Cause | Recovery |
|------------|-------|----------|
| INVALID_TOPIC | Unknown topic | Show valid topics list |
| LEVEL_MISMATCH | Level too advanced for topic | Suggest appropriate level |
| PARAM_VALIDATION | Invalid parameter type | Return validation message |

## Related Skills

- css-flexbox-grid (layout builds on fundamentals)
- css-architecture (naming builds on selectors)
- css-modern (extends selector knowledge)
