---
name: ui-craft
description: Cross-cutting UI quality and dashboard-design skill. Covers the three tells of an amateur dashboard (data shapes the UI, progressive disclosure, hidden UI), plus the Refactoring UI principles (hierarchy, spacing, typography, color, depth, finishing touches) and how to apply each in Angular projects using Spartan/ng, PrimeNG, NG-ZORRO, or Angular Material. Use when the user asks to polish, refine, redesign, or "make this look better"; when building a dashboard, table, KPI surface, or data-heavy view; when the project has visual quality issues (low hierarchy, ambiguous spacing, grey-on-color text, color used as the only signal); or when the user mentions hierarchy, density, spacing, typography, palette, shadows, or empty states. Pairs with one of the library-specific skills (spartan-ng-developer, primeng-developer, ng-zorro-developer, angular-material-developer) for the implementation surface, and with angular-developer for the Angular fundamentals.
license: MIT
metadata:
  author: Mofiro Jean
  version: '0.0.1'
---

# UI Craft

> **Cross-cutting skill.** Pair this with one of the library-specific skills (`spartan-ng-developer`, `primeng-developer`, `ng-zorro-developer`, `angular-material-developer`) plus the base `angular-developer`. This skill teaches *what good looks like* and *why*. The library skill teaches *which component to reach for*. Both load together when the user wants polished UI.

## When this skill should fire

Activate eagerly when the user says any of:

- "Make this look better / cleaner / more polished"
- "This feels generic" / "looks like a template"
- "Improve the dashboard" / "redesign this page"
- "Why does this look amateur"
- Specific topics: "hierarchy", "spacing", "typography", "color palette", "shadows", "empty state", "tooltip", "hover state", "loading state"

Also activate proactively (without being asked) when you see:

- A dashboard or data-heavy surface being built
- A table with all-grey text, no alignment, no muted/active distinction
- Form labels in the same weight and color as the values
- Color used as the only signal (no icon, no text, no shape backup)
- Hover-only actions with no affordance hinting at them
- Zero empty states / zero loading states for an async surface

## The three tells of an amateur dashboard

These are the patterns that immediately give away a UI built without intent. Each gets its own reference file because each is a discipline, not a single rule.

1. **Data drives the UI.** Not the other way around. The shape, density, alignment, color, and chart-vs-table choice all come *from the data being displayed*, not from a default table template. Read [data-driven-ui.md](references/data-driven-ui.md).

2. **Progressive disclosure.** Most actions, controls, and metadata don't belong permanently on screen. They belong tucked behind hover, popover, sheet, or context menu, with a clear affordance. The "spectrum of explicitness" runs from always-visible global actions to on-hover row actions to right-click-revealed power-user actions. Read [progressive-disclosure.md](references/progressive-disclosure.md).

3. **UI is what you can't see.** Tooltips on every icon-only button, hover affordances on every clickable area, empty states, loading states, error states, the right-click menu, the keyboard shortcut, the toast on save. These hidden surfaces are most of the actual UI. Read [hidden-ui.md](references/hidden-ui.md).

## The Refactoring UI principles

The book *Refactoring UI* by Adam Wathan and Steve Schoger gives the vocabulary for *why* a layout feels right. Each chapter maps to a reference here.

- **Hierarchy**, Not all elements are equal. Emphasize by de-emphasizing. Labels are a last resort. Separate visual from document hierarchy. Read [hierarchy.md](references/hierarchy.md).
- **Spacing**, Start with too much whitespace, then use a sizing system. Don't fill the screen for the sake of filling it. Avoid ambiguous gaps. Read [spacing.md](references/spacing.md).
- **Typography**, Establish a type scale. Keep line-length in check (45-75ch). Line-height is proportional to font-size. Baseline-align, not center. Read [typography.md](references/typography.md).
- **Color**, Ditch hex for HSL or OKLCH. Define a 9-step shade system per hue. Don't let lightness kill saturation. Greys don't have to be neutral. Color is never the only signal. Read [color.md](references/color.md).
- **Depth**, Emulate a light source. Shadows convey elevation. Two-part shadows (close + ambient). Flat designs can still have depth via overlap and value contrast. Read [depth.md](references/depth.md).
- **Finishing touches**, Supercharge defaults. Add accent borders. Decorate empty backgrounds. Never skip empty states. Use fewer borders, more value contrast. Read [finishing.md](references/finishing.md).

## Dashboard-specific patterns

When you're building or improving a dashboard, table, KPI surface, or data-heavy view, also read [dashboard-patterns.md](references/dashboard-patterns.md). It covers:

- KPI card patterns (label, value, delta, sparkline)
- Table polish (chips for enumerated values, right-aligned numerics, truncated long text, muted inactive rows, sticky headers, hidden hover actions)
- Filter bar conventions (toggle groups, comboboxes, date-range, save-as-view)
- Sidebar nav density
- When to use a chart instead of a table (any time the data has a meaningful x-axis)

## Bridging to the library skills

The four library skills tell you *which Helm / Aura / NG-ZORRO / Material component to use*. This skill tells you *how to make it look good*. The bridge file maps each principle onto the four libraries, including which design tokens to override, which density mode to pick, and which common defaults are wrong out of the box. Read [library-bridge.md](references/library-bridge.md).

## Working principles

1. **Critique before you generate.** If the user has existing code, read it and call out the specific tells (grey-on-color label, no truncation, no muted state) before refactoring. Naming the flaw teaches the user too.

2. **Show before/after when it matters.** When you change spacing, hierarchy, or color, describe the *why* in one line so the change isn't mysterious. "Reviewers column trimmed from 152px to 96px so the avatars sit flush against the row's right padding instead of floating with empty space."

3. **Tailwind-first, design-token-aware.** All four library skills compose with Tailwind. Use utility classes for one-off polish, but reach for theme tokens (`text-muted-foreground`, `border-border`, `bg-card`) so dark mode and theming come for free. Never hard-code hex.

4. **Density is a choice, not a default.** Default densities from component libraries are usually too loose for dashboards. Tighten via the library's density token (Material: `density-3`, Spartan: smaller `size` variants, PrimeNG: `--p-form-field-padding`, ZORRO: `nzSize="small"`). See `library-bridge.md`.

5. **No new components without reason.** If a Helm/PrimeNG/NG-ZORRO/Material component covers it, use it. Custom components ship with their own bugs.

6. **Empty, loading, and error states are not optional.** Every async surface gets all three. Use the library's Skeleton / Empty / Alert primitives.

7. **Accessibility is part of craft.** Focus rings, ARIA labels on icon-only buttons, keyboard shortcuts, contrast ratios. The `accessibility.md` in each library skill covers the mechanics; the *intent* lives here.
