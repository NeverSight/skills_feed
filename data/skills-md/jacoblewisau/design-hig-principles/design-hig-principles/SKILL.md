---
name: design-hig-principles
aliases:
  - design-HIG-principles
  - hig-audit
  - hig
description: Audit iOS/macOS UI against Apple Human Interface Guidelines. Provides context-aware, multi-perspective feedback on colors, typography, layout, accessibility, and platform conventions.
---

<objective>
Systematically audit SwiftUI/UIKit interfaces against Apple Human Interface Guidelines using three complementary design perspectives, identifying violations and providing actionable fixes with code examples.
</objective>

<essential_principles>
## The Three Perspectives

Every HIG audit applies these complementary lenses:

**1. Clarity Perspective** — "Does the interface communicate clearly?"
- Content is paramount, UI defers to it
- Every element has a purpose
- Users know what they can do without instructions
- Information hierarchy is obvious

**2. Consistency Perspective** — "Does this feel like an Apple platform app?"
- Standard UI elements and familiar patterns
- Navigation follows platform conventions
- Gestures work as expected
- Components appear in expected locations

**3. Deference Perspective** — "Does the UI stay out of the way?"
- Subtle backgrounds, restrained branding
- Content is the hero
- Controls recede when not needed
- No visual competition with content

**Golden Rule:** "Deference makes an app beautiful by ensuring the content stands out while the surrounding visual elements do not compete with it." — Apple HIG
</essential_principles>

<workflow>
## Step 1: Context Reconnaissance

Before evaluating any UI, gather project intelligence:

1. **Check project type** — What kind of app is this?
   - Productivity tool → Emphasize Clarity + Consistency
   - Media/content app → Emphasize Deference
   - Creative tool → Balance all three
   - Utility → Emphasize Clarity

2. **Scan for common patterns**
   ```
   Search for:
   - Hardcoded colors (.white, .black, Color(red:...))
   - Fixed font sizes (.system(size: 17))
   - Missing accessibility labels
   - Custom touch targets under 44pt
   - Animations without Reduce Motion checks
   ```

3. **Identify platform targets** — iOS, iPadOS, macOS, watchOS, visionOS?

4. **Perform HIG Gap Analysis**
   Search for these anti-patterns:
   - `Color(red:` or `Color(hex:` without asset catalog fallback
   - `.font(.system(size:` without `relativeTo:`
   - `Button` or `Image` without `.accessibilityLabel`
   - `.frame(width:` or `.frame(height:` under 44 for interactive elements
   - `withAnimation` without `@Environment(\.accessibilityReduceMotion)`

**After reconnaissance, present findings and ask user to confirm context weighting before full audit.**

## Step 2: Full Audit

Read the audit checklist, then read perspective-specific references based on project type:

| Project Type | Primary Refs | Secondary Refs |
|--------------|--------------|----------------|
| Productivity | clarity.md, consistency.md | accessibility.md |
| Media/Content | deference.md, colors.md | typography.md |
| Creative | all three perspectives | platform-specific.md |
| Utility | clarity.md, accessibility.md | consistency.md |

**Always include:** accessibility.md review (mandatory for every audit)

## Step 3: Output Format

Present findings with this structure:

```
┌─────────────────────────────────────────┐
│  HIG AUDIT SUMMARY                      │
│  Project: [name] | Platform: [target]   │
│  Critical: X | Important: Y | Minor: Z  │
└─────────────────────────────────────────┘

## Overall Assessment
[2-3 sentence summary of HIG compliance]

## Clarity Perspective
### Working Well
- [items that support clear communication]

### Issues Found
- [specific violations with file:line references]

### Perspective Summary
[How well does the UI communicate its purpose?]

---

## Consistency Perspective
### Working Well
- [items following platform conventions]

### Issues Found
- [specific violations with file:line references]

### Perspective Summary
[How well does this feel like a native app?]

---

## Deference Perspective
### Working Well
- [items that let content shine]

### Issues Found
- [specific violations with file:line references]

### Perspective Summary
[How well does the UI stay out of the way?]

---

## Combined Recommendations

| Priority | Issue | Fix | Effort |
|----------|-------|-----|--------|
| Critical | [issue] | [solution] | [Low/Med/High] |
| Important | [issue] | [solution] | [Low/Med/High] |
| Minor | [issue] | [solution] | [Low/Med/High] |

## Quick Reference
- Clarity: [focused on X]
- Consistency: [focused on Y]
- Deference: [focused on Z]
```
</workflow>

<severity_levels>
## Issue Classification

**Critical (Must Fix)**
- Accessibility violations (contrast, touch targets, missing labels)
- Platform convention breaks (non-standard navigation, gestures)
- Dynamic Type not supported
- Reduce Motion not respected

**Important (Should Fix)**
- Hardcoded colors without dark mode variants
- Fixed font sizes
- Inconsistent spacing/alignment
- Missing semantic colors

**Context-Dependent**
- Branding placement
- Custom animations
- Non-standard controls (may be intentional)

**Nice to Have**
- Optical alignment refinements
- Material thickness optimization
- Platform-specific polish
</severity_levels>

<reference_library>
## Comprehensive Reference Library

This skill has 21 detailed reference documents covering every aspect of Apple HIG:

### Core References (Always Read)
- `references/audit-checklist.md` — Systematic evaluation criteria for all domains
- `references/philosophy.md` — The "why" behind Clarity, Consistency, Deference
- `references/accessibility.md` — Vision, mobility, cognitive, hearing accessibility (MANDATORY)
- `references/common-mistakes.md` — Anti-patterns with fixes

### Visual Design
- `references/colors.md` — Semantic color system, dark mode, contrast requirements
- `references/typography.md` — Text styles, Dynamic Type, font weight guidelines
- `references/sf-symbols.md` — Symbol usage, weights, rendering modes, accessibility
- `references/materials-depth.md` — Blur, vibrancy, materials, visual layers
- `references/dark-mode.md` — Dark mode design, elevation, color adaptation

### Layout & Structure
- `references/layout-spacing.md` — 8pt grid, safe areas, adaptive layout, margins
- `references/lists-collections.md` — List styles, grids, lazy loading, interactions
- `references/navigation-architecture.md` — Navigation patterns, deep linking, state restoration

### Interaction
- `references/controls-inputs.md` — All system controls, forms, pickers, inputs
- `references/gestures-touch.md` — Gesture design, touch targets, hit testing
- `references/modals-sheets.md` — Sheets, alerts, popovers, confirmation dialogs
- `references/motion-animation.md` — Timing, springs, choreography, Reduce Motion
- `references/haptics-feedback.md` — UIFeedbackGenerator, sensory feedback patterns
- `references/feedback-status.md` — Progress, loading, success/error states

### Platform & Polish
- `references/platform-specific.md` — iOS, iPadOS, macOS, watchOS, tvOS, visionOS
- `references/branding.md` — Appropriate branding, launch screens, app icons
- `references/onboarding-ftue.md` — First-run experience, permissions, feature discovery
- `references/localization-rtl.md` — Internationalization, RTL support, formatting
- `references/privacy-ux.md` — Permission requests, Privacy Manifest, data handling
</reference_library>

<required_reading>
## Required Reading by Audit Type

### Full HIG Audit
1. `references/audit-checklist.md` — Start here
2. `references/philosophy.md` — Understand the three perspectives
3. `references/accessibility.md` — ALWAYS required
4. `references/common-mistakes.md` — Know what to look for
5. Platform-specific reference(s) based on target

### Quick Color/Typography Audit
1. `references/colors.md`
2. `references/typography.md`
3. `references/dark-mode.md`

### Accessibility Audit
1. `references/accessibility.md`
2. `references/gestures-touch.md` (touch targets)
3. `references/motion-animation.md` (Reduce Motion)

### Navigation/Flow Audit
1. `references/navigation-architecture.md`
2. `references/modals-sheets.md`
3. `references/platform-specific.md`

### Interaction Audit
1. `references/controls-inputs.md`
2. `references/gestures-touch.md`
3. `references/haptics-feedback.md`
4. `references/feedback-status.md`

### Pre-Release Audit
Read all core references plus:
- `references/privacy-ux.md`
- `references/localization-rtl.md`
- `references/branding.md`
</required_reading>

<context_mapping>
## Project Type → Perspective Priority

| App Category | Primary Focus | Why |
|--------------|---------------|-----|
| Productivity (Linear, Notion) | Clarity + Consistency | Users have clear goals, efficiency matters |
| Media (Photos, Music) | Deference | Content is the hero |
| Social (Messages, Twitter) | Consistency | Familiarity reduces friction |
| Creative (Procreate, Figma) | Balance all | Both tool clarity and canvas deference |
| Utility (Calculator, Weather) | Clarity | Single purpose, immediate understanding |
| Games | Deference | Immersion over conventions |
| Enterprise | Consistency | Training costs, reliability |
</context_mapping>

<success_criteria>
A complete HIG audit:
- Identifies project type and platform targets
- Applies all three perspectives appropriately weighted
- Provides specific file:line references for issues
- Includes working code examples for fixes
- Classifies issues by severity
- Always checks accessibility compliance
- Gives actionable, prioritized recommendations
</success_criteria>
