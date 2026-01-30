---
name: tailwindcss
description: Tailwind CSS utility-first CSS framework. Use when styling web applications with utility classes, building responsive designs, or customizing design systems with theme variables.
metadata:
  author: Hairyf
  version: "2026.1.28"
  source: Generated from https://github.com/tailwindlabs/tailwindcss.com, scripts located at https://github.com/hairyf/skills
---

# Tailwind CSS

> The skill is based on Tailwind CSS v4.1.18, generated at 2026-01-28.

Tailwind CSS is a utility-first CSS framework for rapidly building custom user interfaces. Instead of writing custom CSS, you compose designs using utility classes directly in your markup. Tailwind v4 introduces CSS-first configuration with theme variables, making it easier to customize your design system.

## Core References

| Topic | Description | Reference |
|-------|-------------|-----------|
| Utility Classes | Understanding Tailwind's utility-first approach and styling elements | [core-utility-classes](references/core-utility-classes.md) |
| Theme Variables | Design tokens, customizing theme, and theme variable namespaces | [core-theme](references/core-theme.md) |
| Responsive Design | Mobile-first breakpoints, responsive variants, and container queries | [core-responsive](references/core-responsive.md) |
| Variants | Applying utilities conditionally with state, pseudo-class, and media query variants | [core-variants](references/core-variants.md) |
| Preflight | Tailwind's base styles and how to extend or disable them | [core-preflight](references/core-preflight.md) |

## Layout

### Positioning

| Topic | Description | Reference |
|-------|-------------|-----------|
| Position | Controlling element positioning with static, relative, absolute, fixed, and sticky | [layout-position](references/layout-position.md) |
| Inset | Controlling placement of positioned elements with top, right, bottom, left, and inset utilities | [layout-inset](references/layout-inset.md) |

### Sizing

| Topic | Description | Reference |
|-------|-------------|-----------|
| Width | Setting element width with spacing scale, fractions, container sizes, and viewport units | [layout-width](references/layout-width.md) |
| Height | Setting element height with spacing scale, fractions, viewport units, and content-based sizing | [layout-height](references/layout-height.md) |

### Spacing

| Topic | Description | Reference |
|-------|-------------|-----------|
| Margin | Controlling element margins with spacing scale, negative values, logical properties, and space utilities | [layout-margin](references/layout-margin.md) |
| Padding | Controlling element padding with spacing scale, logical properties, and directional utilities | [layout-padding](references/layout-padding.md) |

### Overflow

| Topic | Description | Reference |
|-------|-------------|-----------|
| Overflow | Controlling how elements handle content that overflows their container | [layout-overflow](references/layout-overflow.md) |

## Transforms

| Topic | Description | Reference |
|-------|-------------|-----------|
| Transform Base | Base transform utilities for enabling transforms, hardware acceleration, and custom transform values | [transform-base](references/transform-base.md) |
| Translate | Translating elements on x, y, and z axes with spacing scale, percentages, and custom values | [transform-translate](references/transform-translate.md) |
| Rotate | Rotating elements in 2D and 3D space with degree values and custom rotations | [transform-rotate](references/transform-rotate.md) |
| Scale | Scaling elements uniformly or on specific axes with percentage values | [transform-scale](references/transform-scale.md) |
| Skew | Skewing elements on x and y axes with degree values | [transform-skew](references/transform-skew.md) |

## Typography

| Topic | Description | Reference |
|-------|-------------|-----------|
| Text Align | Controlling text alignment with left, center, right, justify, and logical properties | [typography-text-align](references/typography-text-align.md) |

## Features

### Dark Mode

| Topic | Description | Reference |
|-------|-------------|-----------|
| Dark Mode | Implementing dark mode with the dark variant and custom strategies | [features-dark-mode](references/features-dark-mode.md) |

### Customization

| Topic | Description | Reference |
|-------|-------------|-----------|
| Custom Styles | Adding custom styles, utilities, variants, and working with arbitrary values | [features-custom-styles](references/features-custom-styles.md) |
| Functions & Directives | Tailwind's CSS directives and functions for working with your design system | [features-functions-directives](references/features-functions-directives.md) |
| Content Detection | How Tailwind detects classes and how to customize content scanning | [features-content-detection](references/features-content-detection.md) |

## Key Recommendations

- **Use utility classes directly in markup** - Compose designs by combining utilities
- **Customize with theme variables** - Use `@theme` directive to define design tokens
- **Mobile-first responsive design** - Use unprefixed utilities for mobile, prefixed for breakpoints
- **Use complete class names** - Never construct classes dynamically with string interpolation
- **Leverage variants** - Stack variants for complex conditional styling
- **Prefer CSS-first configuration** - Use `@theme`, `@utility`, and `@custom-variant` over JavaScript configs
