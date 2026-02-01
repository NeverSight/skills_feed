---
name: polaris-design
description: Apply Shopify Polaris Design System principles to create professional admin interfaces and dashboards. Use when building React admin panels, data-heavy interfaces, e-commerce dashboards, or when optimizing existing UIs for better usability and data density. Provides color tokens, typography scales, spacing system, and component patterns following Polaris guidelines.
---

# Shopify Polaris Design

Apply Polaris design principles to create efficient, accessible admin interfaces optimized for data-heavy workflows.

## Core Principles

### Color Has Purpose
- Use neutral backgrounds (black/white) to make colored elements stand out
- Red for critical errors, green for success, blue for tips/offers
- Never use color purely for decoration in the UI (only in illustrations)
- Use color WITH other elements (icons, text) - never alone to convey meaning

### Typography Defines Hierarchy
- Use weight, size, and positioning to establish hierarchy
- Never rely only on color for hierarchy
- Mono for code; tabular numbers for currency/amounts
- Consistently style similar or repeating type

### Space Defines Relationships
- Closer objects = stronger perceived relationship
- Group related items in the same card
- Larger/heavier elements attract attention; smaller/lighter for details
- Avoid nesting shapes; avoid divider lines outside of tables

## Design Tokens

For complete token values, see [references/design-tokens.md](references/design-tokens.md).

### Color Palette
```css
/* Neutral Backgrounds */
--p-color-bg: #ffffff;
--p-color-bg-surface: #f1f1f1;
--p-color-bg-surface-secondary: #f7f7f7;
--p-color-bg-surface-hover: #f0f0f0;
--p-color-bg-surface-active: #e8e8e8;

/* Text Colors */
--p-color-text: #1a1a1a;
--p-color-text-secondary: #616161;
--p-color-text-disabled: #8c8c8c;

/* Primary (Interactive) */
--p-color-bg-fill-brand: #008060;
--p-color-text-brand: #008060;

/* Status Colors */
--p-color-bg-fill-success: #008060; /* Green */
--p-color-bg-fill-critical: #d72c0d; /* Red */
--p-color-bg-fill-warning: #ffc453; /* Yellow */
--p-color-bg-fill-info: #0070f3;    /* Blue */
```

### Typography
```css
/* Font Family */
--p-font-family-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
--p-font-family-mono: 'SF Mono', Consolas, 'Liberation Mono', Menlo, monospace;

/* Font Sizes */
--p-font-size-75: 0.75rem;   /* 12px - Caption */
--p-font-size-100: 0.8125rem; /* 13px - Body small */
--p-font-size-200: 0.875rem;  /* 14px - Body */
--p-font-size-300: 1rem;      /* 16px - Body large */
--p-font-size-400: 1.25rem;   /* 20px - Heading */
--p-font-size-500: 1.5rem;    /* 24px - Display */

/* Font Weights */
--p-font-weight-regular: 400;
--p-font-weight-medium: 500;
--p-font-weight-semibold: 600;
--p-font-weight-bold: 700;

/* Line Heights */
--p-font-line-height-1: 1;
--p-font-line-height-2: 1.25;
--p-font-line-height-3: 1.5;
```

### Spacing (4px base unit)
```css
--p-space-050: 0.125rem; /* 2px */
--p-space-100: 0.25rem;  /* 4px */
--p-space-150: 0.375rem; /* 6px */
--p-space-200: 0.5rem;   /* 8px */
--p-space-300: 0.75rem;  /* 12px */
--p-space-400: 1rem;     /* 16px */
--p-space-500: 1.25rem;  /* 20px */
--p-space-600: 1.5rem;   /* 24px */
--p-space-800: 2rem;     /* 32px */
--p-space-1000: 2.5rem;  /* 40px */
```

### Border & Shadow
```css
/* Border Radius */
--p-border-radius-100: 0.25rem; /* 4px */
--p-border-radius-200: 0.5rem;  /* 8px */
--p-border-radius-300: 0.75rem; /* 12px */
--p-border-radius-full: 9999px;

/* Shadows */
--p-shadow-100: 0 1px 0 rgba(0, 0, 0, 0.05);
--p-shadow-200: 0 1px 2px rgba(0, 0, 0, 0.1);
--p-shadow-300: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
--p-shadow-400: 0 10px 15px -3px rgba(0, 0, 0, 0.1);

/* Borders */
--p-border-width-1: 1px;
--p-color-border: #e1e1e1;
--p-color-border-secondary: #d1d1d1;
```

## Component Patterns

For complete component examples, see [references/component-patterns.md](references/component-patterns.md).

### Cards
```css
.polaris-card {
  background: var(--p-color-bg-surface);
  border-radius: var(--p-border-radius-200);
  padding: var(--p-space-400);
  box-shadow: var(--p-shadow-200);
}
```

### Buttons
```css
.polaris-button {
  font-size: var(--p-font-size-200);
  font-weight: var(--p-font-weight-medium);
  padding: var(--p-space-200) var(--p-space-400);
  border-radius: var(--p-border-radius-100);
  transition: background 0.15s ease;
}
.polaris-button--primary {
  background: var(--p-color-bg-fill-brand);
  color: #ffffff;
}
```

### Data Tables
```css
.polaris-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--p-font-size-200);
}
.polaris-table th {
  text-align: left;
  font-weight: var(--p-font-weight-semibold);
  padding: var(--p-space-300) var(--p-space-400);
  border-bottom: var(--p-border-width-1) solid var(--p-color-border);
  color: var(--p-color-text-secondary);
}
.polaris-table td {
  padding: var(--p-space-300) var(--p-space-400);
  border-bottom: var(--p-border-width-1) solid var(--p-color-border);
}
.polaris-table tr:hover {
  background: var(--p-color-bg-surface-hover);
}
```

### Form Inputs
```css
.polaris-input {
  font-size: var(--p-font-size-200);
  padding: var(--p-space-200) var(--p-space-300);
  border: var(--p-border-width-1) solid var(--p-color-border);
  border-radius: var(--p-border-radius-100);
  background: var(--p-color-bg);
  transition: border-color 0.15s ease;
}
.polaris-input:focus {
  outline: none;
  border-color: var(--p-color-bg-fill-brand);
  box-shadow: 0 0 0 1px var(--p-color-bg-fill-brand);
}
```

## Best Practices

### Data Density
- Use 13-14px base font for data-heavy interfaces
- Reduce padding in table cells for scannability
- Group related metrics in cards

### Interaction States
- Always provide visual feedback: hover, focus, active, disabled
- Use consistent timing: 150ms for micro-interactions
- Focus states must be visible (never remove outline without alternative)

### Accessibility
- Maintain minimum 4.5:1 contrast ratio for text
- Use color WITH icons/text, never alone
- All interactive elements must be keyboard accessible
