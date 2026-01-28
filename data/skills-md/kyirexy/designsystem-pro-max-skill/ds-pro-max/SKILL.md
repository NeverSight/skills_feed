---
name: ds-pro-max
description: "Design system intelligence. Search AntD, Material-UI, Figma, Bootstrap, Tailwind specs. Generate compliant CSS code. Audit for violations. Components, colors, typography, spacing, tokens. Actions: search, generate, audit, review, fix, implement, migrate. Projects: React, Vue, web apps, dashboards, admin panels."
---

# DesignSystem-Pro-Max - Design System Intelligence

Searchable database of design system specifications, component guidelines, color tokens, typography scales, and framework-specific best practices.

## Prerequisites

Check if Python is installed:

```bash
python3 --version || python --version
```

If Python is not installed, install it based on user's OS:

**macOS:**
```bash
brew install python3
```

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install python3
```

**Windows:**
```powershell
winget install Python.Python.3.12
```

---

## How to Use This Skill

When user requests design system work (search specs, generate code, audit compliance), follow this workflow:

### Step 1: Analyze User Requirements

Extract key information from user request:
- **Component type**: Button, Input, Modal, Table, etc.
- **Framework**: AntD, Material-UI, Bootstrap, Tailwind, Chakra, Elements, Figma
- **Task type**: Search specs, generate code, audit violations
- **Output format**: CSS (primary), component code

### Step 2: Search Design Specifications

Use `search.py` to gather comprehensive information:

```bash
python3 .claude/skills/ds-pro-max/scripts/search.py "<keyword>" --domain <domain> [--max-results <n>]
python3 .claude/skills/ds-pro-max/scripts/search.py "<keyword>" --stack <stack> [--max-results <n>]
```

**Available Domains:**

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `component` | UI component specs | button, input, modal, table, card, select |
| `color` | Color tokens | primary, success, warning, error, theme |
| `typography` | Font specs | heading, body, font-size, weight, line-height |
| `spacing` | Spacing tokens | padding, margin, gap, spacing scale |
| `tokens` | Design tokens | design token, CSS variable, theme |

**Available Stacks:**

| Stack | Framework | Docs |
|-------|-----------|------|
| `react-antd` | Ant Design (React) | https://ant.design |
| `material-ui` | Material-UI (MUI) | https://mui.com |
| `figma-tokens` | Figma Design Tokens | https://figma.com |
| `bootstrap` | Bootstrap CSS | https://getbootstrap.com |
| `tailwind` | Tailwind CSS | https://tailwindcss.com |
| `chakra` | Chakra UI | https://chakra-ui.com |
| `elements` | Adobe I/O Elements | https://opensource.adobe.com |

### Step 3: Generate Compliant Code

Use `generate.py` to generate CSS code based on specifications:

```bash
python3 .claude/skills/ds-pro-max/scripts/generate.py "<query>" --stack <stack> --output <file.css>
```

**Example:**
```bash
# Generate color token CSS for Ant Design
python3 .claude/skills/ds-pro-max/scripts/generate.py "primary color tokens" --stack react-antd --output colors.css

# Generate spacing scale for Tailwind
python3 .claude/skills/ds-pro-max/scripts/generate.py "spacing scale" --stack tailwind --output spacing.css
```

### Step 4: Audit Code for Compliance

Use `audit.py` to check code for design system compliance:

```bash
python3 .claude/skills/ds-pro-max/scripts/audit.py <file.css> --stack <stack>
```

**Audit checks include:**
- Naming conventions (kebab-case, CSS variables)
- Property value validity (colors, spacing tokens)
- Accessibility (color contrast, focus states)
- Best practices (shorthands, specificity)

---

## Example Workflows

### Example 1: Create a Primary Button

**User request:** "Create a primary button using Ant Design"

**AI should:**

```bash
# 1. Search component specs
python3 .claude/skills/ds-pro-max/scripts/search.py "primary button" --domain component --stack react-antd

# 2. Search color specs
python3 .claude/skills/ds-pro-max/scripts/search.py "primary color" --domain color --stack react-antd

# 3. Generate CSS if needed
python3 .claude/skills/ds-pro-max/scripts/generate.py "primary button styles" --stack react-antd --output button.css
```

**Then:** Synthesize results and implement:
```jsx
import { Button } from 'antd';

<Button type="primary">Primary Button</Button>
```

### Example 2: Migrate Bootstrap to Tailwind

**User request:** "Convert Bootstrap button to Tailwind"

**AI should:**

```bash
# 1. Search Bootstrap button spec
python3 .claude/skills/ds-pro-max/scripts/search.py "button" --stack bootstrap

# 2. Search Tailwind button spec
python3 .claude/skills/ds-pro-max/scripts/search.py "button utility classes" --stack tailwind

# 3. Generate Tailwind CSS
python3 .claude/skills/ds-pro-max/scripts/generate.py "button styles" --stack tailwind --output tailwind-button.css
```

**Then:** Provide migration:
```html
<!-- Before (Bootstrap) -->
<button class="btn btn-primary">Click</button>

<!-- After (Tailwind) -->
<button class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600">Click</button>
```

### Example 3: Audit CSS for Compliance

**User request:** "Check this CSS for Ant Design compliance"

**AI should:**

```bash
# Audit the CSS file
python3 .claude/skills/ds-pro-max/scripts/audit.py styles.css --stack react-antd
```

**Then:** Report violations with fixes:
```css
/* Violation: Using non-standard color */
.btn-primary { background: #1890; }
/* Fix: Use standard color token */
.btn-primary { background: var(--primary-color); }
```

---

## Common Design System Rules

### Naming Conventions

| Rule | Do | Don't |
|------|----|----- |
| **CSS variables** | `--primary-color`, `--spacing-md` | `$primaryColor`, `PRIMARY_COLOR` |
| **Kebab-case** | `primary-button`, `font-size-lg` | `primaryButton`, `font_size_lg` |
| **Semantic names** | `--color-success`, `--spacing-content` | `--color-green`, `--spacing-16px` |

### Color Tokens

| Rule | Do | Don't |
|------|----|----- |
| **Use variables** | `color: var(--primary-color)` | `color: #1890ff` |
| **Semantic names** | `--color-primary`, `--color-error` | `--color-blue`, `--color-red` |
| **Contrast ratios** | 4.5:1 minimum for text | Low contrast colors |

### Spacing Scale

| Rule | Do | Don't |
|------|----|----- |
| **Consistent base** | 4px, 8px, 12px, 16px, 24px | 5px, 7px, 9px, 11px |
| **Use tokens** | `padding: var(--spacing-md)` | `padding: 16px` |
| **Semantic names** | `--spacing-content`, `--spacing-section` | `--spacing-16` |

### Accessibility

| Rule | Do | Don't |
|------|----|----- |
| **Focus states** | Always define `:focus` styles | Skip focus indicators |
| **Color contrast** | 4.5:1 for normal text, 3:1 for large | Low contrast ratios |
| **ARIA labels** | Add `aria-label` for icon buttons | Rely on visuals only |
| **Keyboard nav** | Ensure all interactive elements work | Mouse-only interactions |

---

## Pre-Delivery Checklist

Before delivering design system code, verify:

### Compliance
- [ ] All colors use CSS variables/tokens
- [ ] Spacing follows the defined scale
- [ ] Naming follows framework conventions
- [ ] Component props match framework API

### Accessibility
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Focus states are visible
- [ ] ARIA labels present where needed
- [ ] Keyboard navigation works

### Best Practices
- [ ] No hardcoded values (use tokens)
- [ ] Consistent naming across files
- [ ] Proper component composition
- [ ] Framework-specific patterns followed

---

## Tips for Better Results

1. **Be specific** - "AntD primary button" > "button"
2. **Use stack flag** - Get framework-specific guidelines
3. **Search multiple domains** - Component + Color + Typography = Complete spec
4. **Generate before implementing** - Get CSS structure from generate.py
5. **Audit your code** - Check for violations before delivery
6. **Reference official docs** - Always link to framework documentation

---

## CLI Reference

### search.py

```bash
python3 scripts/search.py "<query>" [options]

Options:
  --domain, -d    Domain to search (component, color, typography, spacing, tokens)
  --stack, -s     Stack to search (react-antd, material-ui, figma-tokens, etc.)
  --max-results, -n  Maximum results (default: 3)
  --json          Output as JSON
  --list-domains  List available domains
  --list-stacks   List available stacks
```

### generate.py

```bash
python3 scripts/generate.py "<query>" [options]

Options:
  --stack, -s     Stack for code generation (required)
  --output, -o    Output file path (required)
  --format, -f    Output format (default: css)
```

### audit.py

```bash
python3 scripts/audit.py <file.css> [options]

Options:
  --stack, -s     Stack for compliance check (required)
  --format, -f    Output format (default: text)
  --fixes         Include suggested fixes
```
