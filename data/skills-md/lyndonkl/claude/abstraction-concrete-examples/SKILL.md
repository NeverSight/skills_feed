---
name: abstraction-concrete-examples
description: Use when explaining concepts at different expertise levels, moving between abstract principles and concrete implementation, identifying edge cases by testing ideas against scenarios, designing layered documentation, decomposing complex problems into actionable steps, or bridging strategy-execution gaps. Invoke when user mentions abstraction levels, making concepts concrete, or explaining at different depths.
---

# Abstraction Ladder Framework

## Table of Contents

- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [What is an Abstraction Ladder?](#what-is-an-abstraction-ladder)
- [Workflow](#workflow)
  - [1. Gather Requirements](#1-gather-requirements)
  - [2. Choose Approach](#2-choose-approach)
  - [3. Build the Ladder](#3-build-the-ladder)
  - [4. Validate Quality](#4-validate-quality)
  - [5. Deliver and Explain](#5-deliver-and-explain)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Create structured abstraction ladders showing how concepts translate from high-level principles to concrete, actionable examples. This bridges communication gaps, reveals hidden assumptions, and tests whether abstract ideas work in practice.

## When to Use This Skill

- User needs to explain same concept to different expertise levels
- Task requires moving between "why" (abstract) and "how" (concrete)
- Identifying edge cases by testing principles against specific scenarios
- Designing layered documentation (overview → details → specifics)
- Decomposing complex problems into actionable steps
- Validating that high-level goals translate to concrete actions
- Bridging strategy and execution gaps

**Trigger phrases:** "abstraction levels", "make this concrete", "explain at different levels", "from principles to implementation", "high-level and detailed view"

## What is an Abstraction Ladder?

A multi-level structure (typically 3-5 levels) connecting universal principles to concrete details:

- **Level 1 (Abstract)**: Universal principles, theories, values
- **Level 2**: Frameworks, standards, categories
- **Level 3 (Middle)**: Methods, approaches, general examples
- **Level 4**: Specific implementations, concrete instances
- **Level 5 (Concrete)**: Precise details, measurements, edge cases

**Quick Example:**
- L1: "Software should be maintainable"
- L2: "Use modular architecture"
- L3: "Apply dependency injection"
- L4: "UserService injects IUserRepository"
- L5: `constructor(private repo: IUserRepository) {}`

## Workflow

Copy this checklist and track your progress:

```
Abstraction Ladder Progress:
- [ ] Step 1: Gather requirements
- [ ] Step 2: Choose approach
- [ ] Step 3: Build the ladder
- [ ] Step 4: Validate quality
- [ ] Step 5: Deliver and explain
```

**Step 1: Gather requirements**

Ask the user to clarify topic, purpose, audience, scope (suggest 4 levels), and starting point (top-down, bottom-up, or middle-out). This ensures the ladder serves the user's actual need.

**Step 2: Choose approach**

For straightforward cases with clear topics → Use `resources/template.md`. For complex cases with multiple parallel ladders or unusual constraints → Study `resources/methodology.md`. To see examples → Show user `resources/examples/` (api-design.md, hiring-process.md).

**Step 3: Build the ladder**

Create `abstraction-concrete-examples.md` with topic, 3-5 distinct abstraction levels, connections between levels, and 2-3 edge cases. Ensure top level is universal, bottom level has measurable specifics, and transitions are logical. Direction options: top-down (principle → examples), bottom-up (observations → principles), or middle-out (familiar → both directions).

**Step 4: Validate quality**

Self-assess using `resources/evaluators/rubric_abstraction_concrete_examples.json`. Check: each level is distinct, transitions are clear, top level is universal, bottom level is specific, edge cases reveal insights, assumptions are stated, no topic drift, serves stated purpose. Minimum standard: Average score ≥ 3.5. If any criterion < 3, revise before delivering.

**Step 5: Deliver and explain**

Present the completed `abstraction-concrete-examples.md` file. Highlight key insights revealed by the ladder, note interesting edge cases or tensions discovered, and suggest applications based on their original purpose.

## Common Patterns

**For communication across levels:**
- Share L1-L2 with executives (strategy/principles)
- Share L2-L3 with managers (approaches/methods)
- Share L3-L5 with implementers (details/specifics)

**For validation:**
- Check if L5 reality matches L1 principles
- Identify gaps between adjacent levels
- Find where principles break down

**For design:**
- Use L1-L2 to guide decisions
- Use L3-L4 to specify requirements
- Use L5 for actual implementation

## Guardrails

**Do:**
- State assumptions explicitly at each level
- Test edge cases that challenge the principles
- Make concrete levels truly concrete (numbers, measurements, specifics)
- Make abstract levels broadly applicable (not domain-locked)
- Ensure each level is understandable given the previous level

**Don't:**
- Use vague language ("good", "better", "appropriate") without defining terms
- Make huge conceptual jumps between levels
- Let different levels drift to different topics
- Skip the validation step (rubric is required)
- Front-load expertise - explain clearly for the target audience

## Quick Reference

- **Template for standard cases**: `resources/template.md`
- **Methodology for complex cases**: `resources/methodology.md`
- **Examples to study**: `resources/examples/api-design.md`, `resources/examples/hiring-process.md`
- **Quality rubric**: `resources/evaluators/rubric_abstraction_concrete_examples.json`
