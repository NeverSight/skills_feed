---
name: css-architecture
description: Implement scalable CSS architecture patterns - BEM, SMACSS, ITCSS, design tokens
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-12-30"
bonded_agent: 04-css-architecture
bond_type: PRIMARY_BOND
---

# CSS Architecture Skill

Implement scalable CSS architecture patterns for maintainable, organized codebases.

## Overview

This skill provides atomic, focused guidance on CSS architecture methodologies with practical implementation patterns and migration strategies.

## Skill Metadata

| Property | Value |
|----------|-------|
| **Category** | Organization |
| **Complexity** | Intermediate to Expert |
| **Dependencies** | css-fundamentals |
| **Bonded Agent** | 04-css-architecture |

## Usage

```
Skill("css-architecture")
```

## Parameter Schema

```yaml
parameters:
  methodology:
    type: string
    required: true
    enum: [bem, smacss, oocss, itcss, atomic, css-modules]
    description: CSS architecture methodology

  project_size:
    type: string
    required: false
    default: medium
    enum: [small, medium, large, enterprise]
    description: Project scale for appropriate recommendations

  include_tokens:
    type: boolean
    required: false
    default: true
    description: Include design token patterns

validation:
  - rule: methodology_required
    message: "methodology parameter is required"
  - rule: valid_methodology
    message: "methodology must be one of: bem, smacss, oocss, itcss, atomic, css-modules"
```

## Topics Covered

### BEM (Block Element Modifier)
- Block: Standalone component
- Element: Part of block (__)
- Modifier: Variant/state (--)

### SMACSS
- Base, Layout, Module, State, Theme

### ITCSS (Inverted Triangle CSS)
- Settings, Tools, Generic, Elements, Objects, Components, Utilities

### Design Tokens
- Primitive, semantic, component tokens
- CSS custom properties organization

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
    - methodology_distribution
    - project_size_distribution
```

## Quick Reference

### BEM Naming

```css
/* Block */
.card { }

/* Element */
.card__header { }
.card__body { }
.card__footer { }

/* Modifier */
.card--featured { }
.card--compact { }
.card__header--large { }
```

### ITCSS Layers

```
/styles
├── 1-settings/     → $variables, tokens
├── 2-tools/        → @mixins, functions
├── 3-generic/      → reset, normalize
├── 4-elements/     → h1, p, a (bare HTML)
├── 5-objects/      → .o-grid, .o-container
├── 6-components/   → .c-card, .c-button
└── 7-utilities/    → .u-hidden, .u-text-center
```

### Design Token Hierarchy

```css
/* 1. Primitive Tokens */
:root {
  --color-blue-500: #3b82f6;
  --color-gray-900: #111827;
  --space-4: 1rem;
  --font-size-lg: 1.125rem;
}

/* 2. Semantic Tokens */
:root {
  --color-primary: var(--color-blue-500);
  --color-text: var(--color-gray-900);
  --spacing-md: var(--space-4);
}

/* 3. Component Tokens */
.button {
  --button-bg: var(--color-primary);
  --button-padding: var(--spacing-md);
}
```

## File Structure Templates

### Small Project

```
styles/
├── base.css
├── components.css
├── utilities.css
└── main.css
```

### Medium Project

```
styles/
├── base/
│   ├── reset.css
│   └── typography.css
├── components/
│   ├── button.css
│   └── card.css
├── layouts/
│   └── grid.css
├── utilities/
│   └── helpers.css
└── main.css
```

### Large/Enterprise Project

```
styles/
├── settings/
│   ├── _tokens.scss
│   └── _breakpoints.scss
├── tools/
│   ├── _mixins.scss
│   └── _functions.scss
├── generic/
│   └── _reset.scss
├── elements/
│   └── _typography.scss
├── objects/
│   └── _grid.scss
├── components/
│   ├── _button.scss
│   └── _card.scss
├── utilities/
│   └── _helpers.scss
└── main.scss
```

## Naming Convention Comparison

| Methodology | Example | Best For |
|-------------|---------|----------|
| BEM | `.block__element--modifier` | Component systems |
| SMACSS | `.l-grid`, `.is-active` | Multi-page sites |
| OOCSS | `.media`, `.media-body` | Reusable patterns |
| Atomic | `.flex`, `.p-4`, `.text-center` | Utility-first |

## Test Template

```javascript
describe('CSS Architecture Skill', () => {
  test('validates methodology parameter', () => {
    expect(() => skill({ methodology: 'invalid' }))
      .toThrow('methodology must be one of: bem, smacss...');
  });

  test('returns BEM examples for bem methodology', () => {
    const result = skill({ methodology: 'bem' });
    expect(result).toContain('__');
    expect(result).toContain('--');
  });

  test('scales recommendations based on project_size', () => {
    const smallResult = skill({ methodology: 'itcss', project_size: 'small' });
    const largeResult = skill({ methodology: 'itcss', project_size: 'large' });
    expect(largeResult.layers).toBeGreaterThan(smallResult.layers);
  });
});
```

## Error Handling

| Error Code | Cause | Recovery |
|------------|-------|----------|
| INVALID_METHODOLOGY | Unknown methodology | Show valid options |
| SIZE_MISMATCH | Methodology too complex for project size | Suggest simpler alternative |
| TOKEN_CONFLICT | Conflicting token names | Show naming resolution |

## Related Skills

- css-fundamentals (prerequisite)
- css-sass (preprocessor integration)
- css-tailwind (utility-first approach)
