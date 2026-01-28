---
name: tailwind-validator
description: Validate Tailwind CSS v4 configuration and detect/prevent Tailwind v3 patterns. Use this skill when setting up Tailwind, auditing CSS configuration, or when you suspect outdated Tailwind patterns are being used. Ensures CSS-first configuration with @theme blocks.
version: 1.0.0
tags:
  - tailwind
  - css
  - validation
  - frontend
  - configuration
---

# Tailwind 4 Validator

Validates that a project uses Tailwind CSS v4 with proper CSS-first configuration. Detects and flags Tailwind v3 patterns that should be migrated.

## Purpose

**CRITICAL**: Claude and other AI assistants often default to Tailwind v3 patterns. This skill ensures:

- Projects use Tailwind v4 CSS-first configuration
- Old `tailwind.config.js` patterns are detected and flagged
- Proper `@theme` blocks are used instead of JS config
- Dependencies are v4+

## When to Use

- **Before any Tailwind work**: Run validation first
- **New project setup**: Ensure v4 is installed correctly
- **After AI generates Tailwind code**: Verify no v3 patterns snuck in
- **Auditing existing projects**: Check for migration needs
- **CI/CD pipelines**: Prevent v3 regressions

## Quick Start

```bash
# Validate current project
python3 ~/.claude/skills/tailwind-validator/scripts/validate.py --root .

# Validate with auto-fix suggestions
python3 ~/.claude/skills/tailwind-validator/scripts/validate.py --root . --suggest-fixes

# Strict mode (fail on any v3 pattern)
python3 ~/.claude/skills/tailwind-validator/scripts/validate.py --root . --strict
```

## What Gets Checked

### 1. Package Version

```json
// GOOD: v4+
"tailwindcss": "^4.0.0"

// BAD: v3
"tailwindcss": "^3.4.0"
```

### 2. CSS Configuration (v4 CSS-first)

**GOOD - Tailwind v4:**

```css
/* app.css or globals.css */
@import "tailwindcss";

@theme {
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  --font-sans: "Inter", sans-serif;
  --breakpoint-3xl: 1920px;
}
```

**BAD - Tailwind v3:**

```css
/* Old v3 directives */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 3. Config Files

**BAD - Should not exist in v4:**

- `tailwind.config.js`
- `tailwind.config.ts`
- `tailwind.config.mjs`
- `tailwind.config.cjs`

**Note**: These files are deprecated in v4. All configuration should be in CSS using `@theme`.

### 4. PostCSS Configuration

**GOOD - v4:**

```js
// postcss.config.js (minimal or not needed)
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
};
```

**BAD - v3:**

```js
// postcss.config.js
module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

### 5. Import Patterns

**GOOD:**

```css
@import "tailwindcss";
@import "tailwindcss/preflight";
@import "tailwindcss/utilities";
```

**BAD:**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Validation Output

```
=== Tailwind 4 Validation Report ===

Package Version: tailwindcss@4.0.14 ✓

CSS Configuration:
  ✓ Found @import "tailwindcss" in src/app/globals.css
  ✓ Found @theme block with 12 custom properties
  ✗ Found @tailwind directive in src/styles/legacy.css (line 3)

Config Files:
  ✗ Found tailwind.config.ts - should migrate to CSS @theme

PostCSS:
  ✓ Using @tailwindcss/postcss plugin

Summary: 2 issues found
  - Migrate tailwind.config.ts to @theme in CSS
  - Remove @tailwind directives from src/styles/legacy.css
```

## Migration Guide

### From Tailwind v3 to v4

1. **Update package.json:**

```bash
bun remove tailwindcss autoprefixer
bun add tailwindcss@latest @tailwindcss/postcss
```

1. **Update postcss.config.js:**

```js
export default {
  plugins: {
    '@tailwindcss/postcss': {},
  },
};
```

1. **Convert tailwind.config.js to CSS @theme:**

**Before (v3):**

```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: '#3b82f6',
        secondary: '#64748b',
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
};
```

**After (v4):**

```css
/* globals.css */
@import "tailwindcss";

@theme {
  --color-primary: #3b82f6;
  --color-secondary: #64748b;
  --font-sans: "Inter", sans-serif;
}
```

1. **Replace @tailwind directives:**

**Before:**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

**After:**

```css
@import "tailwindcss";
```

1. **Delete old config files:**

```bash
rm tailwind.config.js tailwind.config.ts
```

## Common v3 Patterns to Avoid

| v3 Pattern | v4 Replacement |
|------------|----------------|
| `@tailwind base` | `@import "tailwindcss"` |
| `@tailwind utilities` | `@import "tailwindcss/utilities"` |
| `tailwind.config.js` | `@theme` block in CSS |
| `theme.extend.colors` | `--color-*` CSS variables |
| `theme.extend.spacing` | `--spacing-*` CSS variables |
| `theme.extend.fontFamily` | `--font-*` CSS variables |
| `content: ['./src/**/*.tsx']` | Not needed (auto-detected) |
| `plugins: [require('@tailwindcss/forms')]` | `@plugin "@tailwindcss/forms"` |

## v4 @theme Reference

```css
@import "tailwindcss";

@theme {
  /* Colors */
  --color-primary: #3b82f6;
  --color-primary-50: #eff6ff;
  --color-primary-900: #1e3a8a;

  /* Typography */
  --font-sans: "Inter", system-ui, sans-serif;
  --font-mono: "JetBrains Mono", monospace;

  /* Spacing (extends default scale) */
  --spacing-128: 32rem;

  /* Breakpoints */
  --breakpoint-3xl: 1920px;

  /* Animations */
  --animate-fade-in: fade-in 0.3s ease-out;

  /* Shadows */
  --shadow-glow: 0 0 20px rgba(59, 130, 246, 0.5);

  /* Border radius */
  --radius-4xl: 2rem;
}

@keyframes fade-in {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

## Using with shadcn/ui

shadcn/ui v2+ supports Tailwind v4. After running the shadcn CLI:

1. Verify `components.json` uses CSS variables
2. Check that generated components use v4 patterns
3. Ensure `@theme` includes shadcn color tokens:

```css
@theme {
  --color-background: hsl(0 0% 100%);
  --color-foreground: hsl(222.2 84% 4.9%);
  --color-card: hsl(0 0% 100%);
  --color-card-foreground: hsl(222.2 84% 4.9%);
  --color-popover: hsl(0 0% 100%);
  --color-popover-foreground: hsl(222.2 84% 4.9%);
  --color-primary: hsl(222.2 47.4% 11.2%);
  --color-primary-foreground: hsl(210 40% 98%);
  --color-secondary: hsl(210 40% 96.1%);
  --color-secondary-foreground: hsl(222.2 47.4% 11.2%);
  --color-muted: hsl(210 40% 96.1%);
  --color-muted-foreground: hsl(215.4 16.3% 46.9%);
  --color-accent: hsl(210 40% 96.1%);
  --color-accent-foreground: hsl(222.2 47.4% 11.2%);
  --color-destructive: hsl(0 84.2% 60.2%);
  --color-destructive-foreground: hsl(210 40% 98%);
  --color-border: hsl(214.3 31.8% 91.4%);
  --color-input: hsl(214.3 31.8% 91.4%);
  --color-ring: hsl(222.2 84% 4.9%);
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
}
```

## CI/CD Integration

Add to your CI pipeline:

```yaml
# .github/workflows/lint.yml
- name: Validate Tailwind v4
  run: |
    python3 ~/.claude/skills/tailwind-validator/scripts/validate.py \
      --root . \
      --strict \
      --ci
```

## Troubleshooting

### "Found tailwind.config.js but using v4"

Some tools still generate v3 configs. Delete the file and use `@theme` instead.

### "@tailwind directives found"

Replace with `@import "tailwindcss"`. The old directives are not supported in v4.

### "autoprefixer in postcss.config"

Remove autoprefixer - it's built into `@tailwindcss/postcss`.

### "content array in config"

v4 auto-detects content files. Remove the `content` config entirely.
