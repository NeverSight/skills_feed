---
name: svg-logo-creator
description: Create professional SVG logos from concept briefs or descriptions. Use when generating SVG logo files, creating logo variations (horizontal, vertical, icon-only), or implementing logo designs. Triggers on "create SVG logo," "generate logo," "make a logo," "logo SVG," "design a logo," or when given a logo concept brief from logo-ideation.
---

# SVG Logo Creator

Create professional, scalable SVG logos from concept briefs or descriptions.

## Input Requirements

Before creating, gather or confirm:

- **Text**: Exact company/brand name and any tagline
- **Logo type**: Wordmark, lettermark, pictorial, abstract, combination, or emblem
- **Visual concept**: Core imagery, metaphor, or style direction
- **Colors**: Primary and secondary colors (hex values preferred)
- **Typography direction**: Modern/classic, geometric/humanist, bold/light

If working from a logo-ideation concept brief, these details should already be specified.

## Creation Workflow

### 1. Plan the Design

Before writing SVG code:

- Sketch the basic shapes mentally
- Identify reusable elements (define once, reference with `<use>`)
- Plan the viewBox dimensions (typically 100x100 or proportional)
- Determine color palette as CSS custom properties

### 2. Create Primary Logo

Write clean, semantic SVG:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60" role="img" aria-label="Company Name logo">
  <style>
    :root {
      --primary: #2563eb;
      --secondary: #1e40af;
      --text: #0f172a;
    }
  </style>
  <defs>
    <!-- Reusable elements here -->
  </defs>
  <!-- Logo content -->
</svg>
```

### 3. Generate Variations

Create these standard variations:

| Variation | Use case | Notes |
|-----------|----------|-------|
| Primary/horizontal | Default, wide spaces | Full logo with icon and text side-by-side |
| Stacked/vertical | Square spaces, mobile | Icon above text |
| Icon-only | Favicons, app icons, small spaces | Symbol without text |
| Wordmark-only | When icon context is established | Text without symbol |
| Monochrome | Single-color contexts | Black or white version |
| Inverted | Dark backgrounds | Light colors for dark bg |

### 4. Save Files

Use consistent naming:

```
logo-primary.svg
logo-stacked.svg
logo-icon.svg
logo-wordmark.svg
logo-mono-black.svg
logo-mono-white.svg
logo-inverted.svg
```

## SVG Best Practices

### Structure

- Use `viewBox` for scalability, never fixed width/height
- Define colors as CSS custom properties in `<style>`
- Group related elements with `<g>` and descriptive `id` attributes
- Put reusable shapes in `<defs>` and reference with `<use>`

### Optimization

- Remove unnecessary attributes (editor metadata, default values)
- Use simple paths over complex shapes when equivalent
- Combine adjacent paths of same color when possible
- Round coordinates to 1-2 decimal places
- Remove empty groups and unused definitions

### Accessibility

- Add `role="img"` to root `<svg>` element
- Include `aria-label` with descriptive text
- Or use `<title>` as first child for accessible name

### Typography in SVG

For text in logos, prefer:

1. **Convert to paths**: Most reliable across systems
2. **Web-safe fonts**: If text must remain editable
3. **Embedded fonts**: Only if absolutely necessary (increases file size)

Example text-to-path workflow:
```svg
<!-- Instead of <text>, use paths for reliability -->
<path d="M10 20 L10 40 L20 40..." /> <!-- Letter shapes -->
```

## Example: Combination Logo

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 50" role="img" aria-label="Acme Inc logo">
  <style>
    .icon { fill: #2563eb; }
    .text { fill: #0f172a; }
  </style>
  <defs>
    <g id="icon">
      <circle cx="20" cy="25" r="15" />
      <path d="M12 25 L20 18 L28 25 L20 32 Z" fill="#fff" />
    </g>
  </defs>

  <!-- Icon -->
  <use href="#icon" class="icon" />

  <!-- Wordmark (as paths for reliability) -->
  <g class="text" transform="translate(45, 20)">
    <!-- Text paths would go here -->
  </g>
</svg>
```

## Delivery Checklist

Before finalizing:

- [ ] All variations created
- [ ] Colors match specification
- [ ] Scales properly from 16px to 1000px+
- [ ] Accessible labels included
- [ ] Clean, optimized code
- [ ] Consistent naming convention
- [ ] Tested on light and dark backgrounds

## Usage Guidelines Output

After creating logos, provide brief usage guidance:

```markdown
## Logo Usage

**Clear space**: Maintain padding equal to the height of the icon
**Minimum size**: 24px for icon, 80px for full logo
**Backgrounds**: Use primary on light, reversed on dark
**Don't**: Stretch, rotate, change colors, add effects
```
