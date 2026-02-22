---
name: mjml
description: This skill should be used when the user asks about MJML syntax, components, or attributes, when writing or editing MJML email templates, when creating responsive email layouts, when troubleshooting MJML rendering issues, or when asking about email client compatibility.
version: 1.0.0
---

# MJML Expert

MJML (Mailjet Markup Language) is a markup language designed to reduce the pain of coding responsive emails. It compiles to responsive HTML that works across email clients.

## Document Structure

Every MJML document follows this hierarchy:

```xml
<mjml>
  <mj-head>
    <!-- Head components: styles, fonts, attributes, preview text -->
  </mj-head>
  <mj-body>
    <!-- Body components: sections, columns, content -->
  </mj-body>
</mjml>
```

## Component Hierarchy

MJML enforces a strict nesting structure:

```
mjml
├── mj-head
│   ├── mj-attributes (define defaults and classes)
│   ├── mj-style (CSS styles)
│   ├── mj-font (external fonts)
│   ├── mj-title (document title)
│   ├── mj-preview (inbox preview text)
│   └── mj-breakpoint (responsive breakpoint)
│
└── mj-body
    ├── mj-wrapper (optional: wraps multiple sections)
    │   └── mj-section
    │
    └── mj-section (rows)
        ├── mj-group (prevents column stacking on mobile)
        │   └── mj-column
        │
        └── mj-column (responsive columns)
            ├── mj-text
            ├── mj-image
            ├── mj-button
            ├── mj-divider
            ├── mj-spacer
            ├── mj-social
            ├── mj-navbar
            ├── mj-table
            ├── mj-raw
            ├── mj-accordion
            ├── mj-carousel
            └── mj-hero
```

**Critical rule:** Content blocks (text, image, button, etc.) must always be inside `mj-column`. Columns must be inside `mj-section` or `mj-group`.

## Column Sizing

### Auto Sizing
By default, columns divide available width equally. Standard email width is 600px:
- 2 columns = 300px each
- 3 columns = 200px each
- 4 columns = 150px each

### Manual Sizing
Override with explicit `width` attribute:

```xml
<mj-section>
  <mj-column width="33%"><!-- Narrow --></mj-column>
  <mj-column width="67%"><!-- Wide --></mj-column>
</mj-section>
```

Both pixel and percentage values are supported.

## Common Attributes

Most components support these attributes:

| Attribute | Description | Example |
|-----------|-------------|---------|
| `padding` | Spacing inside element | `10px 25px` |
| `background-color` | Background color | `#ffffff` |
| `width` | Element width | `100%` or `300px` |
| `align` | Horizontal alignment | `left`, `center`, `right` |
| `vertical-align` | Vertical alignment | `top`, `middle`, `bottom` |
| `font-family` | Text font | `Arial, sans-serif` |
| `font-size` | Text size | `14px` |
| `color` | Text color | `#333333` |
| `line-height` | Line spacing | `1.5` or `22px` |

## Using Classes

Define reusable styles with `mj-class`:

```xml
<mj-head>
  <mj-attributes>
    <mj-class name="primary" background-color="#4A90D9" color="#ffffff" />
    <mj-class name="heading" font-size="24px" font-weight="bold" />
  </mj-attributes>
</mj-head>

<mj-body>
  <mj-section>
    <mj-column>
      <mj-button mj-class="primary">Click me</mj-button>
      <mj-text mj-class="heading">Welcome</mj-text>
    </mj-column>
  </mj-section>
</mj-body>
```

## Background Images

Sections and wrappers support background images:

```xml
<mj-section background-url="https://example.com/bg.jpg"
            background-size="cover"
            background-repeat="no-repeat">
  <mj-column>
    <mj-text color="#ffffff">Content over image</mj-text>
  </mj-column>
</mj-section>
```

## Full-Width Sections

By default, sections are constrained to 600px. Use `full-width` for edge-to-edge backgrounds:

```xml
<mj-section full-width="full-width" background-color="#f4f4f4">
  <!-- Content still constrained, but background extends full width -->
</mj-section>
```

## Responsive Behavior

- Columns automatically stack vertically on mobile (below breakpoint)
- Use `mj-group` to prevent stacking for specific column groups
- Default breakpoint is 480px; customize with `mj-breakpoint`
- Images scale responsively by default

## Reference Documentation

For complete component specifications with all attributes:
- Body components: `${CLAUDE_SKILL_ROOT}/references/body-components.md`
- Head components: `${CLAUDE_SKILL_ROOT}/references/head-components.md`
- Layout patterns: `${CLAUDE_SKILL_ROOT}/references/patterns.md`
