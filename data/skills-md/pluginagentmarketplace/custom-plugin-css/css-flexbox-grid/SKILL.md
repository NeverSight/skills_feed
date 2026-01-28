---
name: css-flexbox-grid
description: Master Flexbox and CSS Grid layouts for modern responsive design
sasmp_version: "1.3.0"
version: "2.0.0"
updated: "2025-12-30"
bonded_agent: 02-css-layout-master
bond_type: PRIMARY_BOND
---

# CSS Flexbox & Grid Skill

Master modern CSS layout systems: Flexbox for 1D layouts and CSS Grid for 2D layouts.

## Overview

This skill provides atomic, focused guidance on CSS layout techniques with comprehensive parameter validation and practical examples.

## Skill Metadata

| Property | Value |
|----------|-------|
| **Category** | Layout |
| **Complexity** | Intermediate to Advanced |
| **Dependencies** | css-fundamentals |
| **Bonded Agent** | 02-css-layout-master |

## Usage

```
Skill("css-flexbox-grid")
```

## Parameter Schema

```yaml
parameters:
  layout_type:
    type: string
    required: true
    enum: [flexbox, grid, comparison, responsive]
    description: Layout system to explore

  pattern:
    type: string
    required: false
    enum: [centering, sidebar, card-grid, holy-grail, navbar, gallery]
    description: Common layout pattern

  include_responsive:
    type: boolean
    required: false
    default: true
    description: Include responsive adaptations

validation:
  - rule: layout_type_required
    message: "layout_type parameter is required"
  - rule: valid_pattern
    message: "pattern must be a recognized layout pattern"
```

## Topics Covered

### Flexbox
- Container properties: display, flex-direction, flex-wrap
- Alignment: justify-content, align-items, align-content
- Item properties: flex-grow, flex-shrink, flex-basis
- Gap, order, and self-alignment

### CSS Grid
- Grid template: columns, rows, areas
- Grid placement: lines, spans, named areas
- Auto-fit, auto-fill, minmax()
- Subgrid and masonry (where supported)

### Responsive Patterns
- Mobile-first approach
- Breakpoint strategies
- Container queries integration
- Fluid layouts with clamp()

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
```

## Logging & Observability

```yaml
logging:
  entry_point: skill_invoked
  exit_point: skill_completed
  log_parameters: true
  metrics:
    - invocation_count
    - pattern_usage
    - layout_type_distribution
```

## Quick Reference

### Flexbox Cheatsheet

```css
.container {
  display: flex;
  flex-direction: row;      /* row | column | row-reverse | column-reverse */
  flex-wrap: wrap;          /* nowrap | wrap | wrap-reverse */
  justify-content: center;  /* flex-start | flex-end | center | space-between | space-around | space-evenly */
  align-items: center;      /* flex-start | flex-end | center | stretch | baseline */
  gap: 1rem;
}

.item {
  flex: 1 1 auto;          /* grow shrink basis */
  align-self: flex-start;
  order: 0;
}
```

### Grid Cheatsheet

```css
.container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  grid-template-rows: auto 1fr auto;
  grid-template-areas:
    "header header header"
    "sidebar main aside"
    "footer footer footer";
  gap: 1rem;
}

.item {
  grid-column: 1 / 3;      /* start / end */
  grid-row: span 2;
  grid-area: header;
}
```

### Decision Matrix

```
Need 2D control?
├─ YES → CSS Grid
└─ NO
    ├─ Content determines size? → Flexbox
    ├─ Equal sizing needed? → Grid
    └─ Simple row/column → Flexbox
```

## Common Patterns

### Center Anything

```css
/* Flexbox centering */
.flex-center {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Grid centering */
.grid-center {
  display: grid;
  place-items: center;
}
```

### Responsive Card Grid

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.5rem;
}
```

### Sidebar Layout

```css
.sidebar-layout {
  display: grid;
  grid-template-columns: minmax(200px, 25%) 1fr;
  min-height: 100vh;
}

@media (max-width: 768px) {
  .sidebar-layout {
    grid-template-columns: 1fr;
  }
}
```

## Test Template

```javascript
describe('CSS Flexbox Grid Skill', () => {
  test('validates layout_type parameter', () => {
    expect(() => skill({ layout_type: 'invalid' }))
      .toThrow('layout_type must be one of: flexbox, grid...');
  });

  test('returns flexbox properties for flexbox type', () => {
    const result = skill({ layout_type: 'flexbox' });
    expect(result).toContain('display: flex');
    expect(result).toContain('justify-content');
  });

  test('includes responsive code when flag is true', () => {
    const result = skill({
      layout_type: 'grid',
      pattern: 'card-grid',
      include_responsive: true
    });
    expect(result).toContain('@media');
  });
});
```

## Error Handling

| Error Code | Cause | Recovery |
|------------|-------|----------|
| INVALID_LAYOUT_TYPE | Unknown layout type | Show valid options |
| INCOMPATIBLE_PATTERN | Pattern doesn't fit layout type | Suggest alternative |
| MISSING_DEPENDENCY | Fundamentals not understood | Link to css-fundamentals |

## Related Skills

- css-fundamentals (prerequisite)
- css-modern (container queries)
- css-architecture (component layout patterns)
