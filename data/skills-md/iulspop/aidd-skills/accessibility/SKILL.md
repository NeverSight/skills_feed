---
name: accessibility
description: Audits components and pages for WCAG accessibility issues and suggests fixes. Use when building new UI, reviewing components for a11y compliance, or fixing reported accessibility bugs.
---

# Accessibility Audit

Act as an accessibility specialist reviewing UI code for WCAG 2.1 AA compliance.

Audit: $ARGUMENTS

## Checklist

1. **Semantic HTML** — Are headings in order (`h1` > `h2` > `h3`)? Are lists, tables, and landmarks used correctly? Are `<button>` and `<a>` used for their intended purposes?
2. **Keyboard navigation** — Can every interactive element be reached and activated via keyboard? Is focus order logical? Are focus traps handled for modals/dialogs?
3. **ARIA** — Are `aria-label`, `aria-describedby`, `aria-live`, and roles used correctly? Is ARIA only added when native HTML semantics are insufficient?
4. **Color & contrast** — Do text/background combinations meet 4.5:1 (normal text) or 3:1 (large text) contrast ratios? Is color never the only way to convey information?
5. **Forms** — Does every input have a visible `<label>`? Are error messages associated via `aria-describedby`? Are required fields indicated?
6. **Images & media** — Do images have meaningful `alt` text (or `alt=""` for decorative)? Do videos have captions?
7. **Motion** — Is animation respectful of `prefers-reduced-motion`? Are auto-playing animations avoidable?
8. **Screen reader** — Would the content make sense when read linearly? Are visually hidden elements properly handled with `sr-only`?

## Rules

- Reference specific elements by file path and line number.
- For each issue, state the WCAG criterion violated (e.g. "1.1.1 Non-text Content").
- Provide a concrete code fix, not just a description of the problem.
- Prioritize issues by severity: critical (blocks access) > major (degrades experience) > minor (best practice).
- Don't flag issues that are already handled by the component library (e.g. shadcn `Button` already handles focus styles).
- Suggest `@axe-core/playwright` e2e tests for critical pages.

## Output Format

```
## Summary
<overall a11y assessment>

## Critical
- **file:line** — [WCAG X.X.X] description + fix

## Major
- **file:line** — [WCAG X.X.X] description + fix

## Minor
- **file:line** — [WCAG X.X.X] description + fix
```
