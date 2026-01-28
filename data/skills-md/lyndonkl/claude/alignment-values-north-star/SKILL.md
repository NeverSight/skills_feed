---
name: alignment-values-north-star
description: Use when teams need shared direction and decision-making alignment. Invoke when starting new teams, scaling organizations, defining culture, establishing product vision, resolving misalignment, creating strategic clarity, or setting behavioral standards. Use when user mentions North Star, team values, mission, principles, guardrails, decision framework, or cultural alignment.
---

# Alignment: Values & North Star

## Table of Contents

- [Purpose](#purpose)
- [When to Use This Skill](#when-to-use-this-skill)
- [What is Values & North Star Alignment?](#what-is-values--north-star-alignment)
- [Workflow](#workflow)
  - [1. Understand Context](#1--understand-context)
  - [2. Choose Framework](#2--choose-framework)
  - [3. Develop Alignment Artifact](#3--develop-alignment-artifact)
  - [4. Validate Quality](#4--validate-quality)
  - [5. Deliver and Socialize](#5--deliver-and-socialize)
- [Common Patterns](#common-patterns)
- [Guardrails](#guardrails)
- [Quick Reference](#quick-reference)

## Purpose

Create clear, actionable alignment frameworks that give teams a shared North Star (direction), values (guardrails), and decision tenets (behavioral standards). This enables autonomous decision-making while maintaining coherence across the organization.

## When to Use This Skill

- Starting new teams or organizations (defining identity)
- Scaling teams (maintaining culture as you grow)
- Resolving misalignment or conflicts (clarifying shared direction)
- Defining product/engineering/design principles
- Creating strategic clarity after pivots or changes
- Establishing decision-making frameworks
- Setting cultural norms and behavioral expectations
- Post-merger integration (aligning different cultures)
- Crisis response (re-centering on what matters)
- Onboarding leaders who need to understand team identity

**Trigger phrases:** "North Star", "team values", "mission", "vision", "principles", "guardrails", "what we stand for", "decision framework", "cultural alignment", "operating principles"

## What is Values & North Star Alignment?

A framework with three layers:

1. **North Star**: The aspirational direction - where are we going and why?
2. **Values/Guardrails**: Core principles that constrain how we operate
3. **Decision Tenets/Behaviors**: Concrete, observable behaviors that demonstrate values

**Quick Example:**

```markdown
# Engineering Team Alignment

## North Star
Build systems that developers love to use and operators trust to run.

## Values
- **Simplicity**: Choose boring technology that works over exciting technology that might
- **Reliability**: Every service has SLOs and we honor them
- **Empathy**: Design for the developer experience, not just system performance

## Decision Tenets
When choosing between options:
✓ Pick the solution with fewer moving parts
✓ Choose managed services over self-hosted when quality is comparable
✓ Optimize for debuggability over micro-optimizations
✓ Document decisions (ADRs) for future context

## Behaviors (What This Looks Like)
- Code reviews comment on operational complexity, not just correctness
- We say no to features that compromise reliability
- Postmortems focus on learning, not blame
- Documentation is part of "done"
```

## Workflow

Copy this checklist and track your progress:

```
Alignment Framework Progress:
- [ ] Step 1: Understand context
- [ ] Step 2: Choose framework
- [ ] Step 3: Develop alignment artifact
- [ ] Step 4: Validate quality
- [ ] Step 5: Deliver and socialize
```

**Step 1: Understand context**

Gather background: team/organization (size, stage, structure), current situation (new team, scaling, misalignment, crisis), trigger (why alignment needed NOW), stakeholders (who needs to align), hard decisions (where misalignment shows up), and existing artifacts (mission, values, culture statements). This ensures the framework addresses real needs.

**Step 2: Choose framework**

For new teams/startups (< 30 people, defining identity from scratch) → Use `resources/template.md`. For scaling organizations (existing values need refinement, multiple teams, need decision framework) → Study `resources/methodology.md`. To see examples → Review `resources/examples/` (engineering-team.md, product-vision.md, company-values.md).

**Step 3: Develop alignment artifact**

Create `alignment-values-north-star.md` with: compelling North Star (1-2 sentences, aspirational but specific), 3-5 core values (specific to this team, not generic), decision tenets ("When X vs Y, we..."), observable behaviors (concrete examples), anti-patterns (optional - what we DON'T do), and context (optional - why these values). See [Common Patterns](#common-patterns) for team-type specific guidance.

**Step 4: Validate quality**

Self-check using `resources/evaluators/rubric_alignment_values_north_star.json`. Verify: North Star is inspiring yet concrete, values are specific and distinctive, decision tenets guide real decisions, behaviors are observable/measurable, usable for decisions TODAY, trade-offs acknowledged, no contradictions, distinguishes this team from others. Minimum standard: Score ≥ 3.5 (aim for 4.5+ if organization-wide).

**Step 5: Deliver and socialize**

Present completed framework with rationale (why these values), examples of application in decisions, rollout/socialization approach (hiring, decision-making, onboarding, team meetings), and review cadence (typically annually). Ensure team can recall and apply key points.

## Common Patterns

**For technical teams:**
- Focus on technical trade-offs (simplicity vs performance, speed vs quality)
- Make architectural principles explicit
- Include operational considerations
- Address technical debt philosophy

**For product teams:**
- Center on user/customer value
- Address feature prioritization philosophy
- Include quality bar and launch criteria
- Make product-market fit assumptions explicit

**For company-wide values:**
- Keep values aspirational but grounded
- Include specific behaviors (not just values)
- Address how values interact (what wins when they conflict?)
- Make hiring/firing implications clear

**For crisis/change:**
- Acknowledge what's changing
- Re-center on core that remains
- Be explicit about new priorities
- Include timeline for transition

## Guardrails

**Do:**
- Make values specific and distinctive (not generic)
- Include concrete behaviors and examples
- Acknowledge trade-offs (what you're NOT optimizing for)
- Test values against real decisions
- Keep it concise (1-2 pages max)
- Make it memorable (people should be able to recall key points)
- Involve the team in creating it (not top-down)

**Don't:**
- Use corporate jargon or buzzwords
- Make it so generic it could apply to any company
- Create laundry list of every good quality
- Ignore tensions between values
- Make it purely aspirational (need concrete behaviors)
- Set it and forget it (values should evolve)
- Weaponize values to shut down dissent

## Quick Reference

- **Standard template**: `resources/template.md`
- **Scaling/complex cases**: `resources/methodology.md`
- **Examples**: `resources/examples/engineering-team.md`, `resources/examples/product-vision.md`, `resources/examples/company-values.md`
- **Quality rubric**: `resources/evaluators/rubric_alignment_values_north_star.json`

**Output naming**: `alignment-values-north-star.md` or `{team-name}-alignment.md`
