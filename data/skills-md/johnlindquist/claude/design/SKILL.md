---
name: design
description: Design system and token management. Use for managing design tokens, colors, typography, and maintaining design consistency.
---

# Design System Manager

Manage design tokens and maintain design consistency.

## Design Token Formats

### CSS Variables

```css
:root {
  /* Colors */
  --color-primary: #3b82f6;
  --color-primary-dark: #2563eb;
  --color-secondary: #64748b;
  --color-success: #22c55e;
  --color-warning: #f59e0b;
  --color-error: #ef4444;

  /* Typography */
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;

  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;

  /* Spacing */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* Border Radius */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}
```

### JSON Tokens

```json
{
  "color": {
    "primary": { "value": "#3b82f6" },
    "primary-dark": { "value": "#2563eb" },
    "secondary": { "value": "#64748b" }
  },
  "font": {
    "family": {
      "sans": { "value": "'Inter', system-ui, sans-serif" },
      "mono": { "value": "'JetBrains Mono', monospace" }
    },
    "size": {
      "xs": { "value": "0.75rem" },
      "sm": { "value": "0.875rem" },
      "base": { "value": "1rem" },
      "lg": { "value": "1.125rem" }
    }
  },
  "spacing": {
    "1": { "value": "0.25rem" },
    "2": { "value": "0.5rem" },
    "4": { "value": "1rem" }
  }
}
```

### Tailwind Config

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#3b82f6',
          dark: '#2563eb',
        },
        secondary: '#64748b',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
    },
  },
};
```

## Color Operations

### Generate Color Palette

```bash
gemini -m pro -o text -e "" "Generate a color palette for:

Base color: #3b82f6 (blue)
Purpose: SaaS dashboard

Provide:
1. 10-step shade scale (50-900)
2. Semantic colors (success, warning, error)
3. Neutral grays
4. CSS custom properties format
5. Ensure WCAG AA contrast ratios"
```

### Check Color Contrast

```bash
gemini -m pro -o text -e "" "Check contrast ratios:

Foreground: #ffffff
Backgrounds:
- #3b82f6
- #2563eb
- #1d4ed8

For each:
1. Calculate contrast ratio
2. WCAG AA compliance (4.5:1 normal, 3:1 large)
3. WCAG AAA compliance (7:1 normal, 4.5:1 large)
4. Suggest adjustments if needed"
```

### Convert Color Formats

```bash
gemini -m pro -o text -e "" "Convert this color to all formats:

Input: #3b82f6

Output:
- HEX
- RGB
- RGBA
- HSL
- HSLA
- CSS custom property"
```

## Typography

### Type Scale

```bash
gemini -m pro -o text -e "" "Generate a type scale:

Base: 16px
Ratio: 1.25 (major third)
Steps: 8 (xs to 4xl)

Provide:
1. Sizes in rem
2. Corresponding line-heights
3. Letter-spacing recommendations
4. CSS custom properties"
```

### Font Pairing

```bash
gemini -m pro -o text -e "" "Suggest font pairings for:

Style: Modern, professional SaaS
Needs: Headings, body text, code

For each pairing:
1. Heading font
2. Body font
3. Code font
4. Google Fonts links
5. Fallback stack"
```

## Spacing System

### Generate Scale

```bash
gemini -m pro -o text -e "" "Generate a spacing scale:

Base: 4px
Approach: 4-point grid

Provide:
1. Scale from 0 to 96
2. Named tokens (xs, sm, md, lg, etc.)
3. Use cases for each size
4. CSS custom properties"
```

## Component Tokens

### Button Tokens

```css
:root {
  /* Button Base */
  --btn-padding-x: var(--space-4);
  --btn-padding-y: var(--space-2);
  --btn-font-size: var(--text-sm);
  --btn-font-weight: 500;
  --btn-border-radius: var(--radius-md);

  /* Button Primary */
  --btn-primary-bg: var(--color-primary);
  --btn-primary-text: white;
  --btn-primary-hover-bg: var(--color-primary-dark);

  /* Button Secondary */
  --btn-secondary-bg: transparent;
  --btn-secondary-text: var(--color-primary);
  --btn-secondary-border: var(--color-primary);
}
```

### Input Tokens

```css
:root {
  --input-padding-x: var(--space-3);
  --input-padding-y: var(--space-2);
  --input-font-size: var(--text-base);
  --input-border-width: 1px;
  --input-border-color: var(--color-gray-300);
  --input-border-radius: var(--radius-md);
  --input-focus-ring: 0 0 0 3px rgba(59, 130, 246, 0.3);
}
```

## Exporting Tokens

### To CSS

```bash
cat tokens.json | jq -r '
  to_entries | .[] |
  "--\(.key): \(.value.value);"
' > tokens.css
```

### To JavaScript

```bash
cat tokens.json | jq '
  to_entries | map({(.key): .value.value}) | add
' > tokens.js
```

### To SCSS Variables

```bash
cat tokens.json | jq -r '
  to_entries | .[] |
  "$\(.key): \(.value.value);"
' > _tokens.scss
```

## Design Review

### Audit Colors

```bash
gemini -m pro -o text -e "" "Audit this color system:

$(cat src/styles/tokens.css)

Check:
1. Sufficient contrast ratios
2. Consistent naming
3. Complete semantic colors
4. Dark mode compatibility
5. Accessibility issues"
```

### Audit Typography

```bash
gemini -m pro -o text -e "" "Audit this typography system:

$(cat src/styles/typography.css)

Check:
1. Readable line heights
2. Appropriate scale ratio
3. Responsive considerations
4. Font loading strategy
5. Accessibility"
```

## Best Practices

1. **Use semantic names** - `--color-error` not `--color-red`
2. **Document tokens** - Explain when to use each
3. **Maintain consistency** - Don't create one-offs
4. **Test accessibility** - Check all contrast ratios
5. **Version tokens** - Track changes
6. **Single source of truth** - Generate from one file
7. **Review regularly** - Audit for drift
