---
name: bootstrap-layout
description: This skill should be used when the user asks about Bootstrap grid system, Bootstrap containers, Bootstrap breakpoints, Bootstrap columns, Bootstrap rows, Bootstrap gutters, Bootstrap responsive layout, Bootstrap CSS Grid, Bootstrap z-index, Bootstrap row-cols, Bootstrap offset classes, Bootstrap column ordering, how to create responsive layouts with Bootstrap, how to use Bootstrap grid, Bootstrap column sizing, Bootstrap auto-layout columns, or needs help with Bootstrap page layout and responsiveness.
---

# Bootstrap 5.3 Layout System

Bootstrap's layout system is built on flexbox and provides a powerful 12-column grid for creating responsive layouts. This skill covers containers, the grid system, breakpoints, and layout utilities.

## Breakpoints

Bootstrap's responsive design uses six default breakpoints:

| Breakpoint | Class infix | Dimensions |
|------------|-------------|------------|
| Extra small | None | <576px |
| Small | `sm` | ≥576px |
| Medium | `md` | ≥768px |
| Large | `lg` | ≥992px |
| Extra large | `xl` | ≥1200px |
| Extra extra large | `xxl` | ≥1400px |

Breakpoints apply at the specified width **and up** (mobile-first).

## Containers

Containers are the fundamental building block for layouts.

### Container Types

```html
<!-- Fixed-width container (max-width at each breakpoint) -->
<div class="container">...</div>

<!-- Full-width container (100% at all breakpoints) -->
<div class="container-fluid">...</div>

<!-- Responsive containers (100% until specified breakpoint) -->
<div class="container-sm">100% until sm, then fixed</div>
<div class="container-md">100% until md, then fixed</div>
<div class="container-lg">100% until lg, then fixed</div>
<div class="container-xl">100% until xl, then fixed</div>
<div class="container-xxl">100% until xxl, then fixed</div>
```

### Container Max-Widths

| | xs<br><576px | sm<br>≥576px | md<br>≥768px | lg<br>≥992px | xl<br>≥1200px | xxl<br>≥1400px |
|---|---|---|---|---|---|---|
| `.container` | 100% | 540px | 720px | 960px | 1140px | 1320px |
| `.container-sm` | 100% | 540px | 720px | 960px | 1140px | 1320px |
| `.container-md` | 100% | 100% | 720px | 960px | 1140px | 1320px |
| `.container-lg` | 100% | 100% | 100% | 960px | 1140px | 1320px |
| `.container-xl` | 100% | 100% | 100% | 100% | 1140px | 1320px |
| `.container-xxl` | 100% | 100% | 100% | 100% | 100% | 1320px |
| `.container-fluid` | 100% | 100% | 100% | 100% | 100% | 100% |

## Grid System

The grid uses a series of containers, rows, and columns.

### Basic Structure

```html
<div class="container">
  <div class="row">
    <div class="col">Column 1</div>
    <div class="col">Column 2</div>
    <div class="col">Column 3</div>
  </div>
</div>
```

### Equal-Width Columns

```html
<div class="row">
  <div class="col">1 of 2</div>
  <div class="col">2 of 2</div>
</div>

<div class="row">
  <div class="col">1 of 3</div>
  <div class="col">2 of 3</div>
  <div class="col">3 of 3</div>
</div>
```

### Specific Column Widths

Use `.col-{number}` for specific widths (1-12):

```html
<div class="row">
  <div class="col-8">8 columns wide</div>
  <div class="col-4">4 columns wide</div>
</div>

<div class="row">
  <div class="col-3">3 columns</div>
  <div class="col-6">6 columns</div>
  <div class="col-3">3 columns</div>
</div>
```

### Responsive Columns

Combine breakpoint infixes for responsive behavior:

```html
<!-- Stack on mobile, side-by-side on md+ -->
<div class="row">
  <div class="col-12 col-md-6">Left on md+</div>
  <div class="col-12 col-md-6">Right on md+</div>
</div>

<!-- Different widths at different breakpoints -->
<div class="row">
  <div class="col-12 col-sm-6 col-lg-4">Responsive column</div>
</div>
```

### Auto-Layout Columns

```html
<!-- One column width set, others auto -->
<div class="row">
  <div class="col">Auto</div>
  <div class="col-6">6 columns</div>
  <div class="col">Auto</div>
</div>

<!-- Variable width content -->
<div class="row justify-content-center">
  <div class="col-auto">Variable width content</div>
</div>
```

## Row Columns

Control the number of columns per row:

```html
<!-- Always 2 columns per row -->
<div class="row row-cols-2">
  <div class="col">Item 1</div>
  <div class="col">Item 2</div>
  <div class="col">Item 3</div>
  <div class="col">Item 4</div>
</div>

<!-- Responsive: 1 on xs, 2 on sm, 3 on md, 4 on lg -->
<div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 row-cols-lg-4">
  <div class="col">Item</div>
  <!-- More items... -->
</div>
```

## Gutters

Gutters are the gaps between columns. Default is `1.5rem` (24px).

### Horizontal Gutters (gx-*)

```html
<div class="row gx-5">
  <div class="col">Wide horizontal gutters</div>
  <div class="col">Wide horizontal gutters</div>
</div>
```

### Vertical Gutters (gy-*)

```html
<div class="row gy-4">
  <div class="col-6">Vertical gutter when wrapping</div>
  <div class="col-6">Vertical gutter when wrapping</div>
  <div class="col-6">Vertical gutter when wrapping</div>
</div>
```

### Both Gutters (g-*)

```html
<div class="row g-3">
  <div class="col-6">Equal gutters</div>
  <div class="col-6">Equal gutters</div>
</div>

<!-- No gutters -->
<div class="row g-0">
  <div class="col">No gutters</div>
  <div class="col">No gutters</div>
</div>
```

### Responsive Gutters

```html
<div class="row g-2 g-md-4 g-lg-5">
  <div class="col">Responsive gutters</div>
</div>
```

## Column Alignment

### Vertical Alignment

```html
<!-- Align all columns in row -->
<div class="row align-items-start">...</div>
<div class="row align-items-center">...</div>
<div class="row align-items-end">...</div>

<!-- Align individual columns -->
<div class="row">
  <div class="col align-self-start">Top</div>
  <div class="col align-self-center">Middle</div>
  <div class="col align-self-end">Bottom</div>
</div>
```

### Horizontal Alignment

```html
<div class="row justify-content-start">...</div>
<div class="row justify-content-center">...</div>
<div class="row justify-content-end">...</div>
<div class="row justify-content-around">...</div>
<div class="row justify-content-between">...</div>
<div class="row justify-content-evenly">...</div>
```

## Column Ordering

### Order Classes

```html
<div class="row">
  <div class="col order-3">First in DOM, last visually</div>
  <div class="col order-2">Second</div>
  <div class="col order-1">Third in DOM, first visually</div>
</div>

<!-- Responsive ordering -->
<div class="row">
  <div class="col order-md-2">Second on md+</div>
  <div class="col order-md-1">First on md+</div>
</div>
```

### Offset Classes

```html
<!-- Offset by columns -->
<div class="row">
  <div class="col-md-4 offset-md-4">Centered column</div>
</div>

<!-- Margin utilities for offsets -->
<div class="row">
  <div class="col-md-4 ms-auto">Pushed right</div>
</div>
```

## Nesting

Columns can be nested:

```html
<div class="row">
  <div class="col-9">
    Level 1
    <div class="row">
      <div class="col-6">Level 2</div>
      <div class="col-6">Level 2</div>
    </div>
  </div>
</div>
```

## Advanced Grid Behaviors

### Column Wrapping

When more than 12 columns are placed within a single row, the extra columns wrap onto a new line as one unit:

```html
<div class="row">
  <div class="col-9">.col-9</div>
  <div class="col-4">.col-4 (wraps to new line since 9 + 4 = 13 > 12)</div>
  <div class="col-6">.col-6 (continues on the new line)</div>
</div>
```

### Column Breaks

Force columns to a new line by inserting a full-width element:

```html
<div class="row">
  <div class="col-6">Column 1</div>
  <div class="col-6">Column 2</div>
  <!-- Force next columns to break to new line -->
  <div class="w-100"></div>
  <div class="col-6">Column 3 (on new line)</div>
  <div class="col-6">Column 4 (on new line)</div>
</div>
```

Apply breaks at specific breakpoints using display utilities:

```html
<div class="row">
  <div class="col-6 col-sm-4">Column 1</div>
  <div class="col-6 col-sm-4">Column 2</div>
  <!-- Force break only at md breakpoint and up -->
  <div class="w-100 d-none d-md-block"></div>
  <div class="col-6 col-sm-4">Column 3</div>
</div>
```

### Standalone Column Classes

Use `.col-*` classes outside a `.row` to give elements a specific width. When used outside a row, column padding is omitted:

```html
<!-- Element with 25% width (no row wrapper needed) -->
<div class="col-3 p-3 mb-2">
  .col-3: width of 25%
</div>

<!-- Responsive width -->
<div class="col-sm-9 p-3">
  .col-sm-9: width of 75% above sm breakpoint
</div>
```

Combine with float utilities for responsive floated images:

```html
<div class="clearfix">
  <img src="..." class="col-md-6 float-md-end mb-3 ms-md-3" alt="...">
  <p>Text wraps around the floated image...</p>
</div>
```

### Handling Gutter Overflow

Large gutters (like `.gx-5`) can cause horizontal overflow. Two solutions:

Add matching padding to the container:

```html
<div class="container px-4">
  <div class="row gx-5">
    <div class="col">Column with large gutter</div>
    <div class="col">Column with large gutter</div>
  </div>
</div>
```

Or use an `overflow-hidden` wrapper:

```html
<div class="container overflow-hidden">
  <div class="row gx-5">
    <div class="col">Column with large gutter</div>
    <div class="col">Column with large gutter</div>
  </div>
</div>
```

## CSS Grid (Alternative)

> **Note:** Bootstrap's CSS Grid system is experimental and opt-in as of v5.1.0. It's disabled by default and requires enabling in your Sass configuration.

Bootstrap 5.3 also supports CSS Grid:

```html
<div class="grid">
  <div class="g-col-6">Half width</div>
  <div class="g-col-6">Half width</div>
</div>

<!-- Custom column count -->
<div class="grid" style="--bs-columns: 3;">
  <div class="g-col-1">1/3</div>
  <div class="g-col-2">2/3</div>
</div>
```

## Z-Index Utilities

Bootstrap provides z-index utility classes for controlling stacking order.

### Utility Classes

| Class | Value |
|-------|-------|
| `.z-n1` | -1 |
| `.z-0` | 0 |
| `.z-1` | 1 |
| `.z-2` | 2 |
| `.z-3` | 3 |

These low single-digit values (1, 2, 3) are useful for controlling component states like
default, hover, and active within the same stacking context.

### Component Stacking Order

Bootstrap components use a standardized z-index scale with large gaps to prevent conflicts:

| Component | z-index |
|-----------|---------|
| Dropdown | 1000 |
| Sticky | 1020 |
| Fixed | 1030 |
| Offcanvas backdrop | 1040 |
| Offcanvas | 1045 |
| Modal backdrop | 1050 |
| Modal | 1055 |
| Popover | 1070 |
| Tooltip | 1080 |
| Toast | 1090 |

> **Warning:** Avoid customizing individual z-index values. The scale is designed as a
> cohesive system—if you change one value, you likely need to adjust others to maintain
> proper layering. Use Sass variables (`$zindex-dropdown`, `$zindex-modal`, etc.) to
> customize these values consistently.

See `references/grid-reference.md` for position utilities that work with z-index.

## Common Layout Patterns

### Sidebar Layout

```html
<div class="container-fluid">
  <div class="row">
    <nav class="col-md-3 col-lg-2 d-md-block sidebar">
      Sidebar
    </nav>
    <main class="col-md-9 col-lg-10 ms-sm-auto px-md-4">
      Main content
    </main>
  </div>
</div>
```

### Card Grid

```html
<div class="row row-cols-1 row-cols-md-2 row-cols-lg-3 g-4">
  <div class="col">
    <div class="card h-100">Card 1</div>
  </div>
  <div class="col">
    <div class="card h-100">Card 2</div>
  </div>
  <!-- More cards... -->
</div>
```

## Sass Customization

When compiling Bootstrap from source, you can customize the layout system through Sass variables and mixins.

### Key Variables

```scss
// Override before importing Bootstrap
$grid-columns: 12;           // Change to 16 or 24 for finer control
$grid-gutter-width: 1.5rem;  // Adjust column gaps
$enable-cssgrid: true;       // Enable CSS Grid classes
```

### Media Query Mixins

```scss
// Mobile-first (applies at breakpoint and UP)
@include media-breakpoint-up(md) { ... }

// Desktop-first (applies BELOW breakpoint)
@include media-breakpoint-down(lg) { ... }

// Range (applies BETWEEN two breakpoints)
@include media-breakpoint-between(sm, xl) { ... }

// Single breakpoint only
@include media-breakpoint-only(md) { ... }
```

### Grid Mixins

Create semantic grid layouts without utility classes:

```scss
.blog-layout {
  @include make-row();
}

.blog-main {
  @include make-col-ready();
  @include make-col(8);  // 8 of 12 columns
}

.blog-sidebar {
  @include make-col-ready();
  @include make-col(4);  // 4 of 12 columns
}
```

See `references/sass-customization.md` for complete variable reference and mixin documentation.

## Additional Resources

### Reference Files

- `references/grid-reference.md` - Complete grid class reference
- `references/sass-customization.md` - Sass variables and mixins for layout customization

### Example Files

- `examples/responsive-layouts.html` - Responsive layout patterns
- `examples/sass-customization.scss` - Sass customization examples
