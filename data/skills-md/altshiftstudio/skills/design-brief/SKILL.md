---
name: design-brief
description: Create strategic design briefs that empower designers. Use when asked to write a design brief, product brief, feature brief for a new product, flow, or a feature. Triggers include "create a design brief", "brief for [feature]", or "design spec".
---

# Design Brief Workflow

Follow this workflow to create a strategic **Design Brief** that empowers designers to do their best work. This document moves beyond "requirements gathering" to define the core problems, the emotional goals, and the creative constraints.

## 1. Context & Setup

- **Alignment**: Consider all relevant details about the product or project you have access to.
- **Visual Baseline**: If a Figma link is provided and Figma MCP is set up, analyze it before writing.
- **The Core Tension**: Before writing, identify the central conflict. Why is this hard? (e.g., "We need to show complex data without overwhelming the user.")

## 2. Create the Design Brief

Create a file `briefs/[name]-brief.md` in the project root. Create the `briefs/` directory if it doesn't exist.

**Writing Guidelines** (unless instructed otherwise):
- Use spare, direct, and powerful writing style.
- Keep sentences under 15 words without losing impact.
- Cut adjectives and adverbs unless removing them changes the meaning.
- **Tone**: Professional, inspiring, precise. Write as a Senior Product Partner.

---

## Brief Structure

### The Problem

Articulate the core issue using this formula:

> "I am **[customer]**. I am trying to **[outcome/job]**. But **[problem/barrier]** because **[root cause]** which makes me feel **[emotion]**."

Fill in all brackets with specifics. The emotion is crucial — it grounds the design in empathy.

### Goals & Success Criteria

Define what success looks like. Pair every goal with a measurable success criterion.

| Goal | Success Criteria |
|------|------------------|
| [What we want to achieve] | [How we'll measure it] |

Example:
| Goal | Success Criteria |
|------|------------------|
| Reduce time to find order status | < 5 minutes per lookup |
| Increase user confidence | NPS score > 40 |

### Anti-Goals

What are we explicitly **NOT** building? Protect scope by listing features or approaches that are out of bounds.

- Not building [X] — that's Phase 2.
- Not replacing [Y] system.

### Job Stories & Personas

**Who**: Describe the target persona with context (e.g., "The Overworked Workshop Manager who juggles 50+ orders daily").

**Job Stories**: Use this format:
> "When [situation], I want to [motivation], so that [outcome]."

### The Narrative Journey

Describe the user flows as short stories. Focus on:
- What the user wants to achieve
- How they feel at each step
- Key decision points and outcomes

Output as a multi-level list. Avoid describing specific UI elements — focus on intent and emotion.

### Edge Cases

Consider non-ideal states the design must handle:

- [ ] **Empty State**: First-time use or no data?
- [ ] **Loading State**: Initial load vs. data refresh?
- [ ] **Error State**: Partial failure vs. total crash?
- [ ] **Partial State**: Minimal data available?
- [ ] **Offline State**: What happens without connectivity?

### Open Questions

List anything that needs clarification from stakeholders before design can proceed.

- [ ] [Question about scope, requirements, or constraints]
- [ ] [Ambiguity that could affect the design direction]
- [ ] [Technical or business question that needs an answer]

---

## 3. Review: The Pre-Mortem

- Ask: "If this design fails, why would it fail?"
- Check: Does this brief solve the "Core Tension"?
- Verify: Are all Open Questions documented?