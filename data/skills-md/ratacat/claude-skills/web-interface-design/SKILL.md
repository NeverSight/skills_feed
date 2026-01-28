---
name: web-interface-design
description: Use when designing or reviewing web UI, implementing forms/buttons/inputs, fixing visual hierarchy issues, creating color systems, building layouts, or when interface feels cluttered, hard to read, or users don't know what to click.
---

# Web Interface Design

## Overview

Design exists to **separate the primary from the secondary**. Users should instantly recognize what matters. Good interface design is invisible—users accomplish goals without noticing the interface.

This skill orchestrates domain-specific reference files. Read only what you need for the task.

## Reference File Index

| Task | Load Reference |
|------|----------------|
| Font sizes, line spacing, heading hierarchy, vertical rhythm | `references/typography.md` |
| Input fields, validation, checkboxes, radios, selects, textareas | `references/forms-and-inputs.md` |
| Button hierarchy, sizing, states, CTAs, ghost buttons | `references/buttons.md` |
| Color palettes, dark mode, tints/shades, state colors | `references/color-systems.md` |
| Navigation, cards, tabs, accordions, modals, tables, toasts | `references/ui-components.md` |
| Grids, spacing scales, responsive patterns, whitespace | `references/layout-and-spacing.md` |
| Focus techniques, hierarchy principles, action pyramid | `references/visual-hierarchy.md` |
| Contrast ratios, focus states, screen readers, WCAG | `references/accessibility.md` |
| CSS implementation patterns, variables, common styles | `references/css-patterns.md` |

## Quick Decision: Which Reference?

```
What's the problem?
├─ Text hard to read, spacing feels off → typography.md
├─ Form not working well, validation issues → forms-and-inputs.md
├─ Users don't know what to click → buttons.md OR visual-hierarchy.md
├─ Colors look wrong, dark mode broken → color-systems.md
├─ Need nav/cards/tabs/modals/tables → ui-components.md
├─ Spacing inconsistent, layout cramped → layout-and-spacing.md
├─ Everything competes for attention → visual-hierarchy.md
├─ Accessibility audit or contrast issues → accessibility.md
└─ Need CSS implementation → css-patterns.md
```

## Universal Quick Reference

### Spacing Scale (4px base)
`4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96`

### Typography Baseline
- Body: 16px, line-height 1.5
- Heading:body ratio max 1:3 (48px heading for 16px body)
- Paragraph spacing: line-height ÷ 1.5

### Touch Targets
- Minimum: 44×44px
- Recommended: 48×48px

### Contrast Minimums (WCAG)
- Normal text: 4.5:1
- Large text (18px+ or 14px+ bold): 3:1
- UI components: 3:1

### Button Hierarchy
| Level | Use For | Treatment |
|-------|---------|-----------|
| Primary | Main action (ONE per view) | Solid fill, high contrast |
| Secondary | Alternative actions | Outlined or subtle fill |
| Tertiary | Minor actions | Text-only or ghost |

### Dark Mode Essentials
- Background: #121212 (not pure black)
- Text: #E0E0E0 (not pure white)
- Reduce color saturation

## Common Mistakes Checklist

- [ ] Multiple primary buttons per view
- [ ] Placeholder used as only label
- [ ] Pure white on pure black
- [ ] Thin/light font weights
- [ ] Color-only error indicators
- [ ] Long centered text
- [ ] Inconsistent spacing values

## Design Review Protocol

1. **Hierarchy**: Is primary action obvious? Can you tell what matters?
2. **Readability**: Text contrast OK? Line length reasonable (45-75 chars)?
3. **Forms**: Labels above fields? Touch targets 44px+? Helpful errors?
4. **Spacing**: Consistent scale? Breathing room around elements?
5. **Accessibility**: Color not sole indicator? Focus states visible?

## When NOT to Use This Skill

- Pure visual branding/identity work
- Marketing copy decisions
- Backend architecture
- Mobile native patterns (iOS/Android differ)

## Sources

- **Web Interface Handbook** by Aleksei Baranov (Imperavi)
- **User Interface Typography** by Imperavi
- **Refactoring UI** by Wathan & Schoger
- WCAG 2.1 accessibility guidelines
