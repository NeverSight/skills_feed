---
name: design
description: "Comprehensive workflow for creating and reviewing high-craft digital and visual design. Use when designing or refining web interfaces (landing pages, websites, dashboards, admin panels, SaaS apps, components), implementing interaction and motion systems, producing static visual artifacts (.png/.pdf posters or compositions), defining design-system tokens and reusable patterns, or auditing UI/UX/accessibility quality. Triggers: design ui, refine interface, design landing page, create visual artifact, design audit, define design tokens."
---

# Design

## Overview

Create distinctive, production-grade design outcomes without defaulting to generic templates.
Select the right mode, anchor decisions in user intent and product context, and ship with system consistency, interaction polish, and quality checks.

## Workflow Integration

In this repo's delivery flow, `design` is an optional step between `prd` and `implement` for UI/UX-heavy features.

- Use the feature PRD (`tasks/f-##-*.md`) as the scope source when available.
- Do not change feature scope in `design`; route scope changes back through `prd`.
- If `tasks/context.md` exists, record durable design decisions that implementation or review will depend on.
- Produce implementation-ready outputs (states, tokens, interaction notes).
- Let `implement` execute with minimal reinterpretation.

## Core Workflow

1. Select the mode from `references/modes.md`.
2. Check for project-specific design-system patterns in `tasks/context.md` and follow them.
3. Write a mandatory design brief.
4. Run domain exploration before proposing direction.
5. Build with `references/craft-system.md`.
6. Apply `references/motion.md` when interaction is in scope.
7. For static artifacts, follow `references/static-canvas.md`.
8. For reviews/audits, follow `references/design-audit.md`.
9. Run quality gates before presenting output.

## Pattern Memory

When `tasks/context.md` records design-system patterns, treat them as source-of-truth.
Examples: established spacing, depth, or component rules.

Add patterns to memory when all conditions are true:

1. the component appears 2+ times
2. the pattern is reusable
3. the pattern has concrete measurements worth preserving

Do not store one-off experiments.

## Mode Selection

- `product-ui`: Dashboards, admin panels, tools, app screens, settings, data-heavy interfaces.
- `marketing-web`: Landing pages, brand websites, campaign pages.
- `interaction-motion`: Microinteractions, transitions, loading states, feedback loops, gestures.
- `static-canvas`: Posters, editorial pages, visual artifacts in `.png` or `.pdf`.
- `design-audit`: Review existing UI code or screens for craft, accessibility, and guideline compliance.

When a request spans multiple modes, pick one primary mode and one secondary mode.
Use the stricter constraint when rules conflict.

## Mandatory Design Brief

Complete this before writing code or visual output:

```text
Mode:
Human:
Primary task:
Context and constraints:
Desired tone:
Signature element:
Three defaults to reject:
```

If critical context is missing, ask concise follow-up questions first.
When asking for user choices (mode, constraints, direction), provide numbered options and accept short replies like `1`, `2`, or `1A`.
If answers are unavailable, make explicit assumptions and proceed.

## Mandatory Domain Exploration

Produce all four before proposing direction:

1. `Domain`: at least 5 domain concepts, metaphors, or vocabulary terms.
2. `Color world`: at least 5 domain-grounded colors from the product or brand world.
3. `Signature`: one design element that feels specific to this problem.
4. `Defaults and replacements`: 3 default patterns to avoid and what replaces them.

## Per-Component Checkpoint

Before implementing each major component, state:

```text
Intent:
Palette:
Depth:
Surfaces:
Typography:
Spacing:
```

If any line has no clear reason, revise before coding.

## Design Principles

1. Make every major decision explainable with a concrete `why`.
2. Keep color, typography, spacing, and depth inside one coherent system.
3. Prefer expressive originality without sacrificing usability.
4. Keep hierarchy legible when squinting or stepping back.
5. Include complete interaction states when relevant.
   States: default, hover, active, focus, disabled, loading, empty, error.
6. Preserve accessibility and performance as non-negotiable constraints.
7. Present decisions and outcomes directly; avoid unnecessary process narration.

## Conflict Resolution Rules

1. Professional utility interfaces prioritize clarity over theatrics.
   Use subtle layering, restrained motion, and low-noise color.
2. Marketing and brand-forward pages can use stronger expression.
   Use bolder type, richer backgrounds, and dramatic composition.
3. Use non-bouncy easing for serious product flows.
4. Use spring-like motion for playful or direct-manipulation moments only.
5. Scale motion intensity with context:
   utility workflows need restraint, hero moments can carry more expression.
6. Decoration is valid only when it supports hierarchy, emphasis, comprehension, or brand story.
7. Use native controls by default for semantics and accessibility.
   Use custom controls only when native rendering blocks required styling/behavior.
   Preserve accessibility semantics when custom controls are used.

## Quality Gates

Run all gates before final output:

1. `Swap test`: replacing major choices with defaults should clearly degrade the concept.
2. `Squint test`: hierarchy remains clear; no harsh visual noise dominates.
3. `Signature test`: signature appears in at least 5 concrete design decisions.
4. `Token test`: color, spacing, and type values map to a coherent token system.
5. `Content coherence`: text, data, and context read as one believable story.
6. `State completeness`: interactive and data states are fully covered.
7. `Accessibility`: contrast, keyboard reachability, focus visibility, reduced-motion support.
8. `Responsiveness`: layout and type remain intentional on mobile and desktop.
9. `Performance`: animation relies on `transform` and `opacity` where possible.

## References

- `references/modes.md`: mode map, output contracts, and complexity budget.
- `references/craft-system.md`: token architecture, depth, typography, spacing, and anti-default craft checks.
- `references/motion.md`: timing scales, easing decisions, motion patterns, and reduced-motion requirements.
- `references/static-canvas.md`: static artifact workflow for philosophy-led visual compositions.
- `references/design-audit.md`: audit workflow, checklist, and guideline-based review instructions.
