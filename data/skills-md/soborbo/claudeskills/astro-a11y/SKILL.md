---
name: astro-a11y
description: Accessibility patterns for Astro lead generation sites. WCAG 2.1 AA compliance, screen readers, keyboard navigation, focus management, ARIA. Use for all accessibility implementation.
---

# Astro Accessibility Skill

## Purpose

Ensures WCAG 2.1 AA compliance for lead generation websites. Legal requirement under UK Equality Act 2010. Provides essential patterns for keyboard navigation, screen readers, focus management, and ARIA implementation.

## Core Rules

1. **Keyboard navigable** — All interactive elements reachable via Tab
2. **Screen reader friendly** — Semantic HTML, proper ARIA
3. **Visible focus** — Clear focus indicators on all elements
4. **Sufficient contrast** — 4.5:1 text, 3:1 UI components
5. **No motion harm** — Respect `prefers-reduced-motion`
6. **Semantic HTML first** — Use native elements before ARIA
7. **Labels required** — Every form input must have a label
8. **Alternative text** — All images need appropriate alt text

## Buttons vs Links

| Element | Use For |
|---------|---------|
| `<button>` | Actions (submit, toggle, open modal) |
| `<a href>` | Navigation (go to page, section) |

## Color Contrast Requirements

| Element | Minimum Ratio |
|---------|---------------|
| Body text | 4.5:1 |
| Large text (18px+ or 14px bold) | 3:1 |
| UI components | 3:1 |
| Disabled elements | No requirement |

## Testing Tools

- Chrome DevTools → Rendering → Emulate vision deficiencies
- axe DevTools extension
- WAVE extension
- Screen readers: NVDA (Windows), VoiceOver (Mac), JAWS

## References

- [Semantic HTML Patterns](references/semantic-html.md)
- [Focus Management](references/focus-management.md) — Skip links, focus traps, focus visible styles
- [ARIA Patterns](references/aria-patterns.md) — Live regions, mobile menus
- [Form Accessibility](references/forms.md) — Labels, error messages, required fields
- [Image Accessibility](references/images.md) — Alt text patterns
- [Motion & Animation](references/motion-animation.md) — Reduced motion support
- [Screen Reader Only Utility](references/screen-reader-only.md) — SR-only CSS class

## Testing Checklist

### Keyboard
- [ ] Tab through entire page — logical order?
- [ ] All interactive elements reachable?
- [ ] Focus visible on every element?
- [ ] Can escape modals with Escape key?
- [ ] Skip link works?

### Screen Reader
- [ ] Page title announced?
- [ ] Headings hierarchy correct?
- [ ] Images have alt text?
- [ ] Form labels announced?
- [ ] Errors announced (aria-live)?

### Visual
- [ ] Contrast passes (4.5:1)?
- [ ] Text resizes to 200% without breaking?
- [ ] Works without color alone?
- [ ] Reduced motion respected?

## Forbidden

- ❌ `<div>` or `<span>` for interactive elements
- ❌ `outline: none` without replacement focus style
- ❌ `tabindex` greater than 0
- ❌ Missing form labels
- ❌ Color as only indicator
- ❌ Auto-playing video/audio
- ❌ CAPTCHA without alternative

## Definition of Done

- [ ] Skip link present on page
- [ ] All forms have proper labels
- [ ] Contrast ratios pass WCAG AA
- [ ] Keyboard navigation works completely
- [ ] axe DevTools shows 0 errors
- [ ] Screen reader test passed
- [ ] Reduced motion media query implemented
- [ ] All images have appropriate alt text
