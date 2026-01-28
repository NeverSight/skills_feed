---
name: css-tokens
description: Provides foundational CSS design tokens (custom properties) for typography, spacing, colors, borders, z-index, and transitions. Use when setting up a base token system for a web project.
---

# CSS Design Tokens Skill

## Purpose

This skill provides a comprehensive set of CSS design tokens (custom properties) to establish a consistent design foundation for web projects. Use this skill when the user requests a base token system or design tokens for their CSS.

## When to Use This Skill

Use this skill when the user asks for:

- "Add design tokens to my project"
- "Set up CSS tokens"
- "Create a tokens file"
- "Add base CSS variables"
- Similar requests for foundational CSS custom properties

## When NOT to Use This Skill

- User already has an existing design token system (suggest modifications instead)
- User specifically requests a framework-specific token system (e.g., Tailwind config, CSS-in-JS tokens)
- User only needs a subset of tokens (offer to extract specific categories)

## What This Skill Provides

A complete `tokens.css` file with a comprehensive design token system:

- **Typography**: Font families, weights, and a modular size scale (xs to 4xl)
- **Spacing**: Consistent size scale from 4px to 96px, named by pixel value
- **Colors**: Using `oklch()` color space for perceptually uniform colors with light/dark mode variants for surfaces, text, brand, interactive elements, and semantic states
- **Borders**: Radius values derived from the size scale (sm to full)
- **Z-index**: Named layers for stacking context (dropdown, modal, toast, etc.)
- **Transitions**: Standard timing values (fast, base, slow)

Users can reference individual tokens using CSS custom property syntax: `var(--token-name)`

## Token Content

The complete token definitions are located in `references/tokens.css` within this skill directory. This file contains all the CSS custom property declarations organized by category.

## How to Use This Skill

### 1. Detect CSS Directory

Search the project for common CSS directory names:

- `css/`
- `styles/`
- `assets/css/`
- `stylesheets/`
- `src/css/`
- `src/styles/`

Check directories at multiple levels (root, `src/`, `public/`, `assets/`).

### 2. Confirm Location with User

**If a CSS directory is found:**

Present the discovered location and ask for confirmation:

```text
I found a CSS directory at [path]. Should I add the design tokens to this directory in a file named `tokens.css`?

If you'd like a different location or filename, please specify both.
```

**If no CSS directory is found:**

Ask the user directly:

```text
I couldn't find an existing CSS directory in your project. Please specify:
1. The directory path where you'd like the tokens file (I can create it if needed)
2. The filename (e.g., `tokens.css`, `design-tokens.css`)
```

### 3. Write the Tokens File

Once confirmed, write the complete tokens file to the specified location. Use the exact content from `references/tokens.css` in this skill directory.

### 4. Inform User About Import

After successfully writing the file, inform the user:

✓ Design tokens written to [full-path]

To use these tokens in your project, import this file in your main CSS file or HTML:

**In CSS:**

```css
@import url('path/to/tokens.css');
```

**In HTML:**

```html
<link rel="stylesheet" href="path/to/tokens.css" />
```

The tokens are now available as CSS custom properties throughout your project (e.g., `var(--color-primary)`, `var(--size-16)`).

## Customization

These tokens provide a solid foundation but are meant to be customized for your project:

- Adjust color values to match your brand
- Modify the spacing scale to fit your design system
- Add project-specific tokens as needed
- Extend categories with additional tokens (animations, shadows, etc.)

This is a **scaffolding skill** - it sets up the initial structure but doesn't handle ongoing modifications.

## Important Notes

- **Do NOT make assumptions** about directory structure or filename if the user hasn't specified
- **Always confirm** the location before writing
- **Create directories** if needed and confirmed by user
- The tokens file includes both light and dark mode color schemes using `prefers-color-scheme`
- The `oklch()` color space provides perceptually uniform colors for better accessibility and consistency
