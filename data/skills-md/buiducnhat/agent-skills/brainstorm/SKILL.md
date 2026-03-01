---
name: brainstorm
description: Collaborative discovery and design framing for ambiguous or high-risk work. Use when requirements are unclear, multiple approaches are possible, or you need to turn an idea into a validated design brief before planning or coding.
---

# Brainstorm

## Overview

Use this skill to convert rough ideas into clear, reviewable design outputs through structured dialogue.

The goal is to:

1. Clarify requirements and constraints
2. Explore alternatives with trade-offs
3. Produce a concrete, validated design brief in `docs/brainstorms/...`
4. Hand off cleanly to `write-plan` when the user is ready

This skill is for exploration and specification only. Do not implement code changes.

## Workflow

### Step 1: Gather Project Context

Before asking design questions, inspect enough project context to avoid proposing incompatible solutions.

- Review `docs/` first, especially:
  - `docs/project-pdr.md`
  - `docs/architecture.md`
  - `docs/codebase.md`
  - `docs/code-standard.md`
- Check key implementation files relevant to the idea
- Note constraints from existing architecture, dependencies, and conventions

Keep this pass focused. Only gather what is needed for the current idea.

### Step 2: Clarify Requirements (One Question at a Time)

Ask targeted questions sequentially to remove ambiguity.

- Ask exactly one question per message
- Prefer multiple-choice options when practical
- Use open-ended questions only when necessary
- Focus on:
  - Objective and user value
  - Scope boundaries
  - Constraints (technical, UX, performance, timeline)
  - Success criteria
  - Non-goals

Do not jump to implementation details too early.

### Step 3: Explore Approaches

Propose 2-5 viable approaches.

For each approach, include:

- Short summary
- Pros
- Cons / risks
- Complexity estimate
- Recommended use conditions

Lead with your recommended option and explain why it best fits the project context and constraints.

### Step 4: Present the Design Incrementally

Once requirements are clear, present the design in small sections (about 200-300 words each), validating after each section.

Suggested section order:

1. Problem framing and goals
2. Proposed architecture / flow
3. Data model and interfaces
4. Error handling and edge cases
5. Testing and verification strategy
6. Rollout considerations (if applicable)

After each section, ask whether to proceed or adjust.

### Step 5: Write Brainstorm Artifacts

Persist results to the standardized location:

- Directory: `docs/brainstorms/YYMMDD-HHmm-<topic-slug>/`
- Main file (required): `docs/brainstorms/YYMMDD-HHmm-<topic-slug>/SUMMARY.md`
- Optional supporting files:
  - `docs/brainstorms/YYMMDD-HHmm-<topic-slug>/section-01-<slug>.md`
  - `docs/brainstorms/YYMMDD-HHmm-<topic-slug>/section-02-<slug>.md`
  - etc.

`SUMMARY.md` should contain:

- Title
- Created timestamp
- Context
- Goals / non-goals
- Chosen approach and rationale
- Alternatives considered
- Risks and mitigations
- Open questions
- Next step recommendation

### Step 6: Close the Loop

After writing artifacts:

1. Ask the user to review and provide feedback
2. If feedback exists, revise artifacts
3. If no feedback, ask whether to proceed to planning
4. If approved, hand off to `write-plan` using the brainstorm output as source context

## Rules

- Do not write production code or make implementation changes in this skill in the brainstorm session
- Keep interaction lightweight and iterative
- Prefer clarity over completeness when uncertain; ask a follow-up question
- Apply YAGNI: remove unnecessary features from proposals
- Align all recommendations with project documentation and standards
- Keep assumptions explicit; do not guess silently

## Output Quality Checklist

Before finalizing `SUMMARY.md`, confirm:

- Requirements are explicit and testable
- Scope and non-goals are clear
- Recommended approach is justified with trade-offs
- Risks and unknowns are documented
- Handoff to planning is actionable

## Integration

- Use `scripts/get-time.sh` to generate:
  - `YYMMDD-HHmm` for folder naming
  - `YYYY-MM-DD HH:mm:ss` for document timestamps
