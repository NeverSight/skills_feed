---
name: accessibility-checker
description: Automatically check specific elements or code for accessibility issues when user asks if something is accessible or mentions WCAG compliance. Performs focused accessibility checks on individual components, forms, or pages. Invoke when user asks "is this accessible?", "WCAG compliant?", or shows code/elements asking about accessibility.
---

# Accessibility Checker

Automatically check code and elements for accessibility issues.

## Accessibility Philosophy

Accessibility is not a checklist—it's a mindset of inclusive design.

### Core Beliefs

1. **Universal Design**: Build for everyone from the start, not as an afterthought
2. **Progressive Enhancement**: Core functionality works for all, enhancements are optional
3. **Semantic First**: Meaningful HTML structure over ARIA workarounds
4. **Real Users**: Test with actual assistive technology users when possible

### Scope Balance

- **Quick checks** (this skill): Fast feedback on specific components (60-70% of issues)
- **Comprehensive audits** (`/audit-a11y` command): Full site analysis with parallel specialists (85-90% coverage)
- **Manual testing**: Keyboard, screen readers, user testing (catches remaining 10-15%, irreplaceable)

This skill provides rapid feedback during development. For production readiness, use comprehensive audits + manual testing.

## When to Use This Skill

Activate this skill when the user:
- Asks "is this accessible?"
- Shows an element and asks "does this meet WCAG?"
- Mentions "accessibility issue", "a11y", or "screen reader"
- Asks "will this work for keyboard users?"
- Questions contrast, ARIA, alt text, or form labels
- Says "check this for accessibility"

## Decision Framework

Before checking accessibility, assess:

### What Element Type Is This?

1. **Interactive** (buttons, links, forms) → Check keyboard access, focus indicators, ARIA
2. **Content** (text, headings, images) → Check contrast, hierarchy, alt text
3. **Structure** (navigation, landmarks) → Check semantic HTML, skip links
4. **Dynamic** (modals, dropdowns, tabs) → Check keyboard traps, ARIA states
5. **Media** (images, video, audio) → Check captions, transcripts, alt text

### What WCAG Level Is Required?

**WCAG 2.1 Level AA** (industry standard):
- ✅ Color contrast: 4.5:1 (normal text), 3:1 (large text)
- ✅ Keyboard navigation: All functionality accessible
- ✅ Focus indicators: Visible on all interactive elements
- ✅ Form labels: All inputs have associated labels
- ✅ Alt text: Meaningful for content images, empty for decorative

**WCAG AAA** (enhanced):
- Higher contrast ratios (7:1 for normal text)
- More stringent requirements

### What's the Scope?

- **Single element** - User shows specific component → Check that element
- **Page section** - User mentions component → Check related elements
- **Entire page** - User says "check this page" → Full page audit
- **Interactive flow** - User shows user journey → Test keyboard flow

### What Are Common Issues?

**Quick wins** (easy to fix):
- Missing alt text on images
- Low contrast text
- Missing form labels
- Missing focus indicators

**Complex issues** (need design changes):
- Keyboard traps
- Complex ARIA patterns
- Dynamic content announcements
- Touch target sizes

### What Testing Method?

1. **Code review** → Check semantic HTML, ARIA attributes
2. **Manual keyboard test** → Tab through page, test interactions
3. **Contrast calculation** → Calculate exact ratios
4. **Screen reader test** → Test with VoiceOver/NVDA (if comprehensive audit)
5. **Automated tools** → Run axe-core or pa11y (for full audits)

### Decision Tree

```
User asks about accessibility
    ↓
Identify element type (interactive/content/structure)
    ↓
Determine WCAG level (AA standard)
    ↓
Check specific criteria (contrast/keyboard/ARIA)
    ↓
Test manually if needed
    ↓
Report issues with confidence scores
    ↓
Provide exact fixes (colors, ARIA, HTML)
```

## Best Practices

### DO:

- ✅ Use semantic HTML5 elements first (header, nav, main, article, button, etc.)
- ✅ Provide visible labels for all form controls (label element, not placeholder)
- ✅ Ensure 4.5:1 contrast for normal text, 3:1 for large text (WCAG AA)
- ✅ Make all interactive elements keyboard accessible (tab, enter, space, arrows)
- ✅ Provide text alternatives for non-text content (alt, aria-label, captions)
- ✅ Test with keyboard only (no mouse) before submitting
- ✅ Use ARIA to enhance, not replace, semantic HTML
- ✅ Ensure focus indicators are visible (2px minimum, high contrast)
- ✅ Structure content with proper heading hierarchy (h1 → h2 → h3)

### DON'T:

- ❌ Use div/span with click handlers instead of button/link
- ❌ Rely on color alone to convey information
- ❌ Use placeholder as label replacement
- ❌ Trap keyboard focus in modals without escape mechanism
- ❌ Hide content with display:none when it should be screen-reader accessible
- ❌ Use positive tabindex (tabindex="1", "2", etc.) - breaks natural tab order
- ❌ Add ARIA when semantic HTML would suffice
- ❌ Remove focus outlines without providing alternative indicators
- ❌ Auto-play media without user control
- ❌ Use complex ARIA patterns when simple alternatives exist

## Quick Checks

This skill performs **focused accessibility checks** on specific elements, unlike `/audit-a11y` which does comprehensive site-wide audits.

### Common Checks

**Button Accessibility:**
- Has accessible name (text, aria-label, or aria-labelledby)
- Keyboard focusable
- Proper ARIA role if custom button
- Sufficient color contrast

**Form Accessibility:**
- All inputs have associated labels
- Error messages properly linked
- Required fields indicated
- Fieldsets for related inputs

**Image Accessibility:**
- Alt text present and descriptive
- Decorative images have alt=""
- Complex images have detailed descriptions

**Link Accessibility:**
- Descriptive link text (not "click here")
- Links distinguishable from text
- Keyboard accessible

### Response Format

```markdown
## Accessibility Check: [Element Type]

### ✅ Passes
- Has proper ARIA label
- Keyboard accessible
- Sufficient color contrast (4.8:1)

### ❌ Issues Found
1. **Missing focus indicator** (WCAG 2.4.7 Level AA)
   - Current: No visible focus state
   - Fix: Add `:focus` styles with outline

2. **Low contrast** (WCAG 1.4.3 Level AA)
   - Current: 3.2:1
   - Required: 4.5:1
   - Fix: Use darker text color #333

### Suggested Code

[Provide fixed code example]
```

## Common Issues by Component Type

### Forms
- Missing <label> elements (use for attribute)
- Placeholder as label (violates 3.3.2 Labels or Instructions)
- No error messages associated (use aria-describedby)
- Required fields not marked (use required + aria-required)

### Modals/Dialogs
- No focus trap (keyboard escapes modal)
- No ESC key handler (violates 2.1.2 No Keyboard Trap)
- Missing role="dialog" or role="alertdialog"
- No aria-labelledby pointing to title
- Focus not moved to modal on open

### Buttons/Links
- Div/span with onClick (use <button> or <a>)
- No visible label (use text content or aria-label)
- Button used for navigation (use <a>)
- Link used for action (use <button>)

### Images
- Missing alt attribute (violates 1.1.1 Non-text Content)
- Decorative images with alt text (should be alt="")
- Complex images without long description (use aria-describedby)
- Icon buttons without text alternative (use aria-label)

## Integration with /audit-a11y Command

- **This Skill**: Quick element-specific checks
  - "Is this button accessible?"
  - "Check this form for a11y"
  - Single component analysis

- **`/audit-a11y` Command**: Comprehensive site audit
  - Full WCAG 2.1 Level AA audit
  - Multiple pages analyzed
  - Detailed compliance reports

## Resources

- WCAG 2.1 Guidelines: https://www.w3.org/WAI/WCAG21/quickref/
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/
- WebAIM Keyboard Testing: https://webaim.org/articles/keyboard/
