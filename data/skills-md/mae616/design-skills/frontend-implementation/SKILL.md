---
name: frontend-implementation
description: Translate designs and UI requirements into robust, extensible implementations. Apply when converting designs to code, implementing components, fixing broken UI, or handling responsive layouts.
user-invocable: false
metadata:
  tags: frontend, implementation, design-to-code, responsive, css, layout
---

# Frontend Implementation Skill

## When to Apply

Apply this skill when the request involves:
- UI implementation, design-to-code, Figma to code, component implementation, styling, responsive design, fixing broken UI
- UI実装、デザインから実装、Figmaから実装、コンポーネント実装、スタイル調整、レスポンシブ対応、UIの崩れ修正
- Translating any design tool output (Figma/Pencil/Canva/sketches) to code

## Core Principles

- **Goal is not pixel-perfect copying, but maintaining ratios, alignment, resilience, and consistency.**
- **Translate, don't transcribe.** Design tool values (px) are references; implementation uses scales, ratios, and structure.
- **Fixed values are exceptions.** If using fixed values, articulate why (spec requirement, media, tap target, etc.).

## Design Philosophy (Decision Rules)

1. **UI is a set of constraints, not a picture.** Include states (loading/error/empty/disabled) to be complete.
2. **Don't create alignment with margin tweaks.** Use structure (flex/grid) and `gap`.
3. **Avoid fixed heights.** Consider `min/max/overflow` first.
4. **Typography is role-based.** Don't proliferate by copying values.
5. **Handle exceptions upfront.** Long text, zero items, failures, delays—no afterthoughts.
6. **Articulate design intent first** (what to emphasize, how to guide the eye), then create structure that preserves it.
7. **Width follows the viewport.** UI should adapt to screen width (SCALE/FILL intent); don't just crop from the left.

## Translation Process (Design Tool → Code)

### 1) Read Intent Before Numbers

- Purpose (what should users understand/do first on this screen)
- Visual flow (first → second → last thing to see)
- Emphasis (hero / supporting / background elements)
- Hierarchy (parent-child, groupings)
- Stretch/state intent (Auto Layout / Constraints / Variants)
- Spacing rules (gap/padding patterns)
- Alignment (what aligns to what)
- Variable elements (text length, list count, image ratio, input values)

### 2) Convert to Implementation

- px → **Round to scale** (e.g., 4/8/12/16/24/32/40/48)
- font-size → **Map to roles** (heading/body/caption)
- Local margin tweaks → **Convert to layout structure** (flex/grid/gap, clarify parent-child responsibilities)
- Fixed width/height → **Convert to constraints** (min/max, wrap, ellipsis, overflow)
- Width design → **Separate background/container/content responsibilities**

### 3) Alignment Decisions

**When to align:**
- Repeated elements (cards/lists/forms) for comparison
- Main column (body/primary input/CTA) for clear visual path
- Reducing confusion (admin panels, settings, heavy input screens)

**When breaking alignment is acceptable:**
- Intentionally floating a hero element
- Emphasizing section boundaries
- Media/decoration as the focus (but ensure resilience)

**Rules when breaking alignment:**
- Keep at least one baseline
- Limit offset patterns to 1-2
- On narrow viewports, favor alignment

### 4) Preserve Width Distribution (Weights)

- **Width distribution IS visual guidance.** Column weights (primary/secondary/tertiary) are intentional.
- **Don't accidentally equalize.** Applying `flex: 1` to everything makes supporting elements as prominent as heroes.
- **Separate baseline alignment from width distribution.** They can differ.

## Implementation Guidelines

### Typography
- Use `rem` (or `clamp()`). Use `em` only when relating to parent size.
- `line-height` should be unitless (e.g., 1.5–1.7).
- Body text readability: aim for `max-width: 60ch`.

### Spacing
- Round to scale (avoid fractional values).
- Prefer parent's `gap/padding` over scattering margins on children.

### Proportions
- Maintain look through ratios, not exact numbers (column width ratios, spacing steps, type scale).
- Prefer max-width + spacing rules over fixed widths.

### Layout
- One-dimensional: flex. Two-dimensional: grid. Spacing: gap.
- `position: absolute` only for overlays/decorations with clear purpose.
- Images: preserve aspect ratio by default; use `aspect-ratio` when needed.

### Fixed Values (Exceptions)
- Icons, thumbnails, tap targets, spec-defined header heights, etc.
- Even for breakage prevention, consider `min/max` before going fixed.

## States and Resilience (Required)

- Include: default / hover / active / focus / disabled / loading / error / empty
- Handle long text, zero items, network failure, delays from the start—no afterthoughts.

## Output Format (Follow This Order)

1. Purpose (what this UI achieves)
2. Prerequisites (design input type, existing conventions, constraints)
3. Translation results (hierarchy, alignment, spacing rules, variable elements)
4. Implementation approach (layout structure, scale, exception conditions)
5. State design (default/hover/active/focus/disabled/loading/error/empty)
6. Checklist self-assessment (OK / needs work)

## Checklist

- [ ] Has empty / loading / error states
- [ ] Has disabled conditions (prevent double-submit, invalid states)
- [ ] Doesn't break on long text (wrap/ellipsis/max-width/overflow)
- [ ] Has keyboard operation and visible focus
- [ ] Doesn't break on narrow/mobile viewports
- [ ] Spacing, typography, colors follow conventions (tokens/scale)

## Common Pitfalls

- Pixel-perfect copying from design data, breaking on edge states and responsiveness
- Margin tweaks proliferating, becoming unmaintainable
- Prioritizing "visual match" while states (loading/error/empty) become afterthoughts
