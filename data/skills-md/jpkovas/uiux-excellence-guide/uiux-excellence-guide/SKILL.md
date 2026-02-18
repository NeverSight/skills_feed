---
name: uiux-excellence-guide
description: Create and refine visually strong interfaces with excellent UX, accessibility, and measurable performance. Use when requests involve designing new screens, redesigning existing UI, defining or evolving design systems/tokens, improving hierarchy/microcopy/motion, raising WCAG 2.2 compliance, improving touch ergonomics, or optimizing Web Vitals (LCP, INP, CLS) in web and app products.
---

# UI UX Excellence Guide

## Overview

Turn vague UI requests into production-ready decisions and implementation guidance.
Prioritize beauty, clarity, usability, accessibility, and responsiveness as one system.

## Workflow Selection

Choose exactly one primary workflow before proposing changes:

1. Use `Greenfield Workflow` when creating a new screen, feature, or app surface.
2. Use `Refactor Workflow` when improving existing UI without breaking product behavior.
3. Use `Audit Workflow` when the user asks for critique, diagnosis, or prioritized fixes.

## Shared Rules

Apply these rules in every workflow:

1. Define UX goals before styling details.
2. Decide layout rhythm early: spacing ramp, grid, and density mode.
3. Use semantic tokens for spacing, typography, color, radius, elevation, and motion.
4. Treat microcopy as interaction design, not garnish.
5. Respect accessibility constraints as non-negotiable.
6. Validate quality with metrics and checks before delivery.

Read `references/uiux-baseline-2026.md` for numeric thresholds and defaults.

## Greenfield Workflow

1. Frame the problem:
- Identify audience, platform, key journeys, and success criteria.
- Confirm if there is an existing design system; if none, create a minimal token contract.

2. Establish structural system:
- Define spacing ramp on base 4.
- Define grid, margins, and gutters by viewport/window class.
- Define density tier (`standard` or `compact`) for data-heavy views.

3. Define readability and hierarchy:
- Define type scale tokens with line-height.
- Enforce contrast and non-text contrast.
- Keep labels concise and state-first.

4. Define motion and state communication:
- Use short, purposeful transitions for state change and spatial continuity.
- Provide reduced-motion fallback behavior.

5. Plan validation:
- Set UX and performance acceptance criteria before implementation.
- Include accessibility and interaction checks in the done definition.

## Refactor Workflow

1. Audit the current surface:
- Map friction points: confusion, misclicks, unreadable content, poor hierarchy.
- Identify inconsistencies in tokens, spacing rhythm, and interaction patterns.

2. Prioritize changes:
- Rank by impact on task success, error reduction, and accessibility risk.
- Prefer low-risk structural improvements before visual polish.

3. Refactor with guardrails:
- Preserve working behavior unless regression is explicitly accepted.
- Normalize onto semantic tokens and remove one-off values.
- Improve copy and feedback loops where users get stuck.

4. Validate and report:
- Document before/after effects and remaining risks.
- Include exact files touched and expected user-visible improvements.

## Audit Workflow

1. Produce findings first, ordered by severity.
2. Attach concrete evidence (component, flow, file, line when applicable).
3. Provide actionable fixes, not vague recommendations.
4. Separate hard blockers from enhancement opportunities.
5. State testing gaps explicitly if validation cannot be completed.

## Output Contract

Return outcomes in this order:

1. `Direction`: concise visual and UX direction statement.
2. `Decisions`: spacing, typography, density, motion, accessibility, and performance choices.
3. `Implementation`: exact edits or code-level plan.
4. `Validation`: checklist and measured/proxy results.
5. `Risks`: what is still unknown or untested.

Use `references/uiux-delivery-template.md` when a complete delivery structure is needed.

## References

- `references/uiux-baseline-2026.md`: implementation defaults and thresholds.
- `references/uiux-delivery-template.md`: reusable response format for design and implementation tasks.
