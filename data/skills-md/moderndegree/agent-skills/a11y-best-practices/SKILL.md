---
name: a11y-best-practices
description: Comprehensive accessibility patterns for building, testing, and fixing accessible interfaces. Use when building UI components, forms, pages, or auditing code for accessibility issues.
version: 1.0.0
---

# Accessibility Best Practices

This skill covers comprehensive accessibility patterns for building inclusive interfaces — from prevention to identification to remediation. It addresses the most common accessibility issues found on the web (based on WebAIM Million reports showing 95% of sites fail WCAG AA).

## Use-When

This skill activates when:
- Agent builds new UI components (buttons, forms, modals, menus)
- Agent creates page layouts or content structures
- Agent adds images, media, or interactive elements
- Agent audits existing code for accessibility issues
- Agent fixes accessibility bugs or violations
- Agent writes tests that should verify accessibility

## Core Rules

### Prevention (Building Accessible)

- ALWAYS ensure minimum 4.5:1 contrast ratio for normal text (3:1 for large text)
- ALWAYS use semantic HTML elements over custom divs
- ALWAYS provide explicit, visible labels for all form inputs
- ALWAYS make all interactive elements keyboard accessible
- ALWAYS include visible focus indicators
- ALWAYS use proper heading hierarchy (no skipping levels)
- ALWAYS provide alt text for meaningful images
- ALWAYS use buttons for actions, links for navigation
- PREFER semantic HTML over ARIA (ARIA is a supplement, not a replacement)

### Identification (Finding Issues)

- ALWAYS test with automated tools (axe, WAVE) to catch common issues
- ALWAYS test with keyboard-only navigation
- ALWAYS test with a screen reader (NVDA, VoiceOver)
- REMEMBER: Automated tools catch only 30-57% of accessibility issues

### Remediation (Fixing Issues)

- NEVER rely on color alone to convey information
- NEVER use placeholder text as a replacement for labels
- NEVER have empty links or buttons
- NEVER use generic text like "click here" for links
- NEVER create keyboard traps (focus must be escapable)

## Common Agent Mistakes

- Using divs with onClick instead of buttons
- Adding role="button" to divs (still not keyboard accessible)
- Using placeholder as the only label (disappears on focus)
- Forgetting to associate error messages with form fields
- Adding redundant ARIA to native HTML elements
- Using aria-label when visible text would work
- Creating heading hierarchies that skip levels (h1 → h3)
- Making focus indicators invisible (outline: none without replacement)
- Using color as the only indicator of state (need text/icon too)
- Not providing way to escape modals/keyboard traps

## Examples

### ✅ Correct

```tsx
// Semantic elements with proper contrast
<button className="bg-slate-900 text-white focus-visible:ring-2">
  Submit
</button>

// Explicit form labels
<label htmlFor="email">Email address</label>
<input id="email" type="email" aria-describedby="email-hint" />
<p id="email-hint">We'll never share your email.</p>

// Image with alt text
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2" />

// Proper heading hierarchy
<h1>Page Title</h1>
<h2>Section</h2>
<h3>Subsection</h3>

// Skip link
<a href="#main" className="sr-only focus:not-sr-only">Skip to content</a>
<main id="main">
```

### ❌ Wrong

```tsx
// Using div as button (not keyboard accessible)
<div onClick={submit}>Submit</div>

// Placeholder only (invisible on focus)
<input placeholder="Enter email" />

// Missing alt text
<img src="photo.jpg" />

// Heading skip (h1 → h3)
<h1>Title</h1>
<h3>Subtitle</h3>

// Generic link text
<a href="/details">Click here</a> to learn more

// No focus indicator
<button className="outline-none">Action</button>
```

## Testing Overview

Accessibility testing requires multiple approaches:

1. **Automated Testing** - Catches ~30-57% of issues (contrast, labels, ARIA)
2. **Keyboard Testing** - All interactions must work without a mouse
3. **Screen Reader Testing** - Content must make sense when read aloud

Run validation on all changes to ensure no regressions.

## References

- [WCAG 2.2 Guidelines](https://www.w3.org/WAI/standards-guidelines/wcag/)
- [WebAIM Accessibility](https://webaim.org/)
- [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- [WebAIM Million Report](https://webaim.org/projects/million/)
- [A11y Project Checklist](https://www.a11yproject.com/checklist/)
