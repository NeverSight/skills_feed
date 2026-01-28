---
name: accessibility-audit
description: Automated accessibility testing via Playwright MCP and axe-core
requires_mcp: playwright
integrates_with:
  - playwright-automation
  - web-design-guidelines
---

# Accessibility Audit

Automated WCAG compliance checking using Playwright MCP.

## Quick Audit

```javascript
// Run via playwright_evaluate
const axe = await import('https://cdnjs.cloudflare.com/ajax/libs/axe-core/4.8.4/axe.min.js');
const results = await axe.run();
return results.violations;
```

## WCAG Levels

| Level | Requirement | Examples |
|-------|-------------|----------|
| **A** | Must have | Alt text, keyboard nav, form labels |
| **AA** | Should have | Color contrast 4.5:1, resize to 200% |
| **AAA** | Nice to have | Contrast 7:1, sign language |

**Target: AA compliance** (legal standard)

## Common Issues & Fixes

### 1. Missing Alt Text
```html
<!-- Bad -->
<img src="hero.jpg">

<!-- Good -->
<img src="hero.jpg" alt="Team collaborating in modern office">
```

### 2. Poor Color Contrast
```css
/* Bad: 2.5:1 ratio */
color: #999 on #fff;

/* Good: 4.6:1 ratio */
color: #767676 on #fff;
```

### 3. Missing Form Labels
```html
<!-- Bad -->
<input type="email" placeholder="Email">

<!-- Good -->
<label for="email">Email</label>
<input type="email" id="email">
```

### 4. No Focus Indicators
```css
/* Bad */
:focus { outline: none; }

/* Good */
:focus { outline: 2px solid var(--primary); outline-offset: 2px; }
```

### 5. Missing Skip Links
```html
<a href="#main" class="skip-link">Skip to content</a>
```

### 6. Insufficient Touch Targets
```css
/* Minimum 44x44px */
button { min-height: 44px; min-width: 44px; }
```

## Audit Workflow

1. **Navigate**: `playwright_navigate` to target URL
2. **Get Tree**: `playwright_get_content` for accessibility tree
3. **Run axe**: `playwright_evaluate` with axe-core
4. **Screenshot**: Capture current state
5. **Report**: Categorize by severity and WCAG level

## Playwright MCP Commands

```
Navigate to [URL] and run an accessibility audit

Get the accessibility tree of this page

Check color contrast on all text elements

Find all images missing alt text

List all form inputs without labels
```

## Severity Levels

| Severity | Impact | Action |
|----------|--------|--------|
| Critical | Blocks users completely | Fix immediately |
| Serious | Major barriers | Fix before release |
| Moderate | Some difficulty | Fix soon |
| Minor | Inconvenience | Fix when possible |

## Tools Integration

- **axe-core**: Automated scanning
- **Playwright**: Browser automation
- **Lighthouse**: Accessibility score
- **WAVE**: Visual feedback (manual)

## Checklist

- [ ] All images have alt text
- [ ] Color contrast meets 4.5:1
- [ ] All forms have labels
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Skip links present
- [ ] Headings in order (h1->h2->h3)
- [ ] ARIA used correctly
- [ ] No keyboard traps
- [ ] Error messages announced
