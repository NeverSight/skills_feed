---
name: web-design-guidelines
description: Review UI code for Web Interface Guidelines compliance - accessibility, forms, animation, performance
requires_mcp: playwright
integrates_with:
  - playwright-automation
  - accessibility-audit
  - frontend-aesthetic
impact: HIGH
impactMetrics:
  - "100+ rules covering accessibility and UX"
  - "15 categories from accessibility to i18n"
  - "Catches common UI anti-patterns"
categories:
  - name: "Accessibility"
    impact: CRITICAL
  - name: "Focus States"
    impact: HIGH
  - name: "Forms"
    impact: HIGH
  - name: "Animation"
    impact: MEDIUM
  - name: "Typography"
    impact: MEDIUM
  - name: "Images"
    impact: HIGH
  - name: "Performance"
    impact: HIGH
  - name: "Navigation & State"
    impact: MEDIUM
  - name: "Dark Mode & Theming"
    impact: LOW
  - name: "Touch & Interaction"
    impact: MEDIUM
  - name: "Locale & i18n"
    impact: MEDIUM
allowed-tools:
  - Read
  - WebFetch
  - Grep
---

# Web Interface Guidelines

Review files for compliance with Vercel Web Interface Guidelines.

## How It Works

1. Fetch the latest guidelines from the source URL below
2. Read the specified files (or prompt user for files/pattern)
3. Check against all rules in the fetched guidelines
4. Output findings in the terse `file:line` format

## Guidelines Source

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

## Usage

When a user provides a file or pattern argument:
1. Fetch guidelines from the source URL above
2. Read the specified files
3. Apply all rules from the fetched guidelines
4. Output findings using the format specified in the guidelines

If no files specified, ask the user which files to review.

## Categories

See `rules/` directory for detailed rules by category:
- `accessibility.md` - CRITICAL: Screen readers, ARIA, semantic HTML
- `focus-states.md` - HIGH: Keyboard navigation, focus rings
- `forms.md` - HIGH: Input handling, validation, autocomplete
- `animation.md` - MEDIUM: Motion preferences, performance
- `typography.md` - MEDIUM: Quotes, ellipsis, numeric formatting
- `images.md` - HIGH: Alt text, dimensions, lazy loading
- `performance.md` - HIGH: Virtualization, layout thrashing
- `navigation.md` - MEDIUM: URL state, deep linking
- `theming.md` - LOW: Dark mode, color scheme
- `touch.md` - MEDIUM: Tap targets, safe areas
- `i18n.md` - MEDIUM: Intl API, locale detection

## Output Format

Group by file. Use `file:line` format (VS Code clickable). Terse findings.

```text
## src/Button.tsx

src/Button.tsx:42 - icon button missing aria-label
src/Button.tsx:18 - input lacks label
src/Button.tsx:55 - animation missing prefers-reduced-motion

## src/Card.tsx

pass
```

## Playwright Validation

Use Playwright MCP to validate guidelines in real browsers:

### Automated Checks

| Guideline | Playwright Command |
|-----------|-------------------|
| Focus visible | Navigate, tab through, screenshot focus states |
| Touch targets | Get element sizes, check ≥44x44px |
| Color contrast | Evaluate computed styles, check ratios |
| Form labels | Get accessibility tree, verify label associations |
| Loading states | Interact, screenshot during loading |
| Error states | Submit invalid input, screenshot errors |

### Validation Workflow

1. `playwright_navigate` to the page
2. `playwright_get_content` for accessibility tree
3. `playwright_evaluate` to check specific rules
4. `playwright_screenshot` for visual evidence
5. Report violations with specific line numbers

### Example: Form Validation Check

```
Navigate to /signup
Get the accessibility tree
Check if all inputs have associated labels
Fill email with "invalid" and submit
Screenshot the error state
Verify error message is announced to screen readers
```
