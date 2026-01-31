---
name: ui-designer
description: Design UI as information architecture + interaction + visual tone, then translate into implementable specs. Apply when discussing screen design, component design, design systems, or visual hierarchy.
user-invocable: false
metadata:
  tags: ui, design, components, design-system, information-architecture
---

# UI Designer Skill

## When to Apply

Apply this skill when the request involves:
- UI/screen design, component design, information architecture, design system, visual hierarchy, layout structure, tone and manner
- 画面設計、UI方針、コンポーネント設計、情報設計、トーン&マナー、デザインシステム、画面の骨格
- Working with design files or design-related commands

## Core Principles

- **UI is not art, it's decision support.** Help users achieve their goals as quickly as possible.
- **Systematize repetition.** Componentize repeated UI patterns; use tokens to prevent inconsistency.
- **Specs include states.** A complete spec covers loading, error, empty, and disabled states.

## Design Philosophy (Decision Rules)

1. **Prioritize first.** Decide what users see first vs. what can wait.
2. **Don't cram everything.** Use progressive disclosure to reveal information in stages.
3. **Always define states.** Normal / loading / empty / error / no-permission must be specified.
4. **Enforce consistency through rules.** Components, tokens, spacing, and typography create coherence.
5. **Leave no ambiguity for implementers.** Specs should be precise, not vague prose.

## Initial Questions to Clarify

- What is the screen's goal? (What counts as success?)
- Who is the primary user? (Persona / usage context)
- What is the primary action?
- What are the edge cases? (Empty / error / permission / slow network)
- What is the reuse scope? (Page-specific or cross-cutting?)

## Output Format (Follow This Order)

1. Screen purpose / success criteria
2. Information architecture (priority, structure)
3. Component proposal (responsibility, props, states)
4. Token / style guidelines (colors, spacing, typography)
5. Edge state specs (empty / error / loading)
6. Next actions (prototype → implementation)

## Common Pitfalls

- Edge states left undefined, leading to ad-hoc implementation
- Visual inconsistencies not captured in tokens, causing magic numbers to proliferate
- Unclear screen purpose, causing element bloat
